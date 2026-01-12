import sys
import os
import telebot
from dotenv import load_dotenv
from cams import get_aerosol_forecast
from analyzer import format_report
import time

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n"
        "Это система раннего оповещения о высоких аэрозольных индексах.\n"
        "Отправь свою геолокацию 📍 для получения прогноза."
    )

@bot.message_handler(content_types=["location"])
def get_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(
        message.chat.id,
        f"✅ Геолокация получена:\nШирота: {lat}\nДолгота: {lon}\n"
        "Запрашиваем прогноз..."
    )

    try:
        data = get_aerosol_forecast(lat, lon)
        report = format_report(data)
        bot.send_message(message.chat.id, report)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении данных: {e}")

# автоперезапуск при падении
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 15 секунд...")
        time.sleep(15)


