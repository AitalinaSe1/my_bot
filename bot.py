import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n"
        "Это система раннего оповещения о высоких аэрозольных индексах.\n"
        "Отправь свою геолокацию 📍 для подписки."
    )

@bot.message_handler(content_types=["location"])
def get_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(
        message.chat.id,
        f"✅ Геолокация получена:\nШирота: {lat}\nДолгота: {lon}"
    )

bot.infinity_polling()