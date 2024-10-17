import threading
import schedule
import time
import asyncio
from weather_api import fetch_weather_data_openweathermap  # Импорт функции для запроса данных о погоде
from export import export_to_excel  # Импорт асинхронной функции для экспорта данных в Excel

def console_input_listener():
    """
    Получает команды пользователя через консоль.
    При вводе команды 'export' запускается процесс экспорта данных в Excel.
    """
    while True:
        command = input("Введите команду 'export' для экспорта данных: ").strip()
        if command == "export":
            print("Начат экспорт данных в Excel...")
            # Запуск асинхронного экспорта данных в Excel
            asyncio.run(export_to_excel())
        else:
            print(f"Неизвестная команда: {command}")

if __name__ == "__main__":
    print("Запуск автоматического сбора данных о погоде...")

    # Создание отдельного потока для обработки команд из консоли
    console_thread = (threading.
                      Thread(target=console_input_listener, daemon=True))
    console_thread.start()

    schedule.every(3).minutes.do(fetch_weather_data_openweathermap)

    while True:
        schedule.run_pending()
        time.sleep(1)
