from openpyxl import Workbook
from database import WeatherData, session
async def export_to_excel():
    """
    Экспортирует последние 10 записей данных о погоде из базы данных в Excel файл.
    """

    records = (session.query(WeatherData).
               order_by(WeatherData.timestamp.desc()).limit(10).all())

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Weather Data"

    sheet.column_dimensions['B'].width = 20  # Увеличить ширину для столбца с датами

    # Добавляем заголовки для столбцов
    headers = ['ID', 'Timestamp', 'Temperature (C)', 'Wind Speed (m/s)',
               'Wind Direction', 'Pressure (mmHg)', 'Precipitation Type',
               'Precipitation Amount (mm)']
    sheet.append(headers)

    # Заполняем таблицу данными из базы
    for record in records:
        sheet.append([
            record.id,
            record.timestamp,
            record.temperature,
            record.wind_speed,
            record.wind_direction,
            record.pressure,
            record.precipitation_type,
            record.precipitation_amount
        ])

    workbook.save("weather_data_last_10.xlsx")
    print("Экспорт данных завершен!")
