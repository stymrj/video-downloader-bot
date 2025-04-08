import telebot
import yt_dlp
import os

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 Welcome! Send any YouTube, Instagram, or Facebook video link to download!")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    if not url.startswith("http"):
        bot.reply_to(message, "⚠️ Please send a valid video URL.")
        return

    bot.send_message(message.chat.id, "📥 Downloading... Please wait ⏳")

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best[ext=mp4]/best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_path)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

bot.polling(non_stop=True)
