import sys
import os

# 👇 ГОВОРИМ PYTHON, ЧТО ТЕКУЩАЯ ПАПКА — РАБОЧАЯ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import telebot
from dotenv import load_dotenv

from cams import get_aerosol_forecast
from analyzer import format_report

# ====== ЗАГРУЗКА ПЕРЕМЕННЫХ ======
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# ====== /start ======
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n"
        "Это система раннего оповещения о высоких аэрозольных индексах.\n"
        "Отправь свою геолокацию 📍 для получения прогноза."
    )

# ====== ПОЛУЧЕНИЕ ГЕОЛОКАЦИИ ======
@bot.message_handler(content_types=["location"])
def get_location(message):
    lat = message.location.latitude
    lon = message.location.longitude

    bot.send_message(
        message.chat.id,
        f"📍 Геолокация получена:\n"
        f"Широта: {lat}\n"
        f"Долгота: {lon}\n\n"
        "🔄 Запрашиваю прогноз аэрозольного индекса..."
    )

    try:
        data = get_aerosol_forecast(lat, lon)
        report = format_report(data)
        bot.send_message(message.chat.id, report)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка при получении данных:\n{e}"
        )

# ====== ЗАПУСК 24/7 С АВТОПЕРЕЗАПУСКОМ ======
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 15 секунд...")
        time.sleep(15)
