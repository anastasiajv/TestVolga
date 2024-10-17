from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Настройка базы данных
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow) # Время записи данных
    temperature = Column(Float) # Температура в градусах Цельсия
    wind_speed = Column(Float) # Скорость ветра в м/с
    wind_direction = Column(String) # Направление ветра в градусах
    pressure = Column(Float) # Давление в мм рт. ст.
    precipitation_type = Column(String) # Тип осадков (например, дождь)
    precipitation_amount = Column(Float) # Количество осадков (мм)

# Инициализация базы данных
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
