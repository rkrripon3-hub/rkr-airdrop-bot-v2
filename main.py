import telebot
import os
import config
from flask import Flask
import threading

bot = telebot.TeleBot(config.BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! RKR Airdrop Bot-এ আপনাকে স্বাগতম।")

if __name__ == '__main__':
    bot.infinity_polling()
  
