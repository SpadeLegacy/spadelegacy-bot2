import telebot
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

video_storage = {}

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    unique_id = str(uuid.uuid4())[:10]
    video_storage[unique_id] = {
        'file_id': file_id,
        'caption': message.caption or "ویدیو از spadelegacy_bot"
    }
    
    link = f"https://t.me/spadelegacy_bot?start={unique_id}"
    
    bot.reply_to(message, f"✅ ویدیو دریافت شد!\n\n🔗 لینک:\n`{link}`\n\nاین لینک رو توی کانالت بذار.", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if len(message.text.split()) > 1:
        unique_id = message.text.split()[1]
        if unique_id in video_storage:
            data = video_storage[unique_id]
            bot.send_video(message.chat.id, data['file_id'], caption=data['caption'], supports_streaming=True)
        else:
            bot.reply_to(message, "❌ لینک نامعتبر یا منقضی شده.")
    else:
        bot.reply_to(message, "👋 سلام! ویدیو بفرست.")

print("ربات روشن شد...")
bot.infinity_polling()
