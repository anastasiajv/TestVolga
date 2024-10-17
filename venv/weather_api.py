import requests
from sqlalchemy.orm import sessionmaker
from database import WeatherData, engine

Session = sessionmaker(bind=engine)
session = Session()

# Функция для преобразования градусов в направление ветра
def degrees_to_wind_direction(degrees):
    """
    Преобразовывает градусы в направление ветра
    """
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    index = round(degrees / 45) % 8  # Делим на 45 для восьми направлений
    return directions[index]

def fetch_weather_data_openweathermap():
    """
    Отправляем запрос о погоде через OpenWeatherMap API для получения данных
    """

    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 55.123456,  # Замените на реальные координаты
        "lon": 37.654321,  # Замените на реальные координаты
        "appid": "d9cf21cadbb021f5e1fac6f1ba2deabc",  # Вставьте ваш ключ OpenWeatherMap
        "units": "metric"
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Извлечение данных
        temperature = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        pressure_in_mmHg = pressure * 0.750063755419211  # Перевод в мм рт. ст.
        wind_speed = data["wind"]["speed"]
        wind_direction_degrees = data["wind"]["deg"]
        wind_direction = degrees_to_wind_direction(wind_direction_degrees)
        precipitation_type = "Rain" if "rain" in data else "None"
        precipitation_amount = data.get("rain", {}).get("1h", 0)

        # Сохранение данных в базу
        new_record = WeatherData(
            temperature=temperature,
            wind_speed=wind_speed,
            wind_direction=wind_direction,  # Направление ветра текстом
            pressure=pressure_in_mmHg,
            precipitation_type=precipitation_type,
            precipitation_amount=precipitation_amount
        )
        session.add(new_record)
        session.commit()
    else:
        print(f"Ошибка при получении данных: {response.status_code}, {response.text}")
