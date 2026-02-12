import telebot
import os
import yt_dlp
import zipfile
import shutil
from telebot import types
from keep_alive import keep_alive

# 🔴 Token (Same as before)
BOT_TOKEN = '8314748732:AAFgldB1M0G_2hpKctC8AqncHgMfo2ngMpo' 
bot = telebot.TeleBot(BOT_TOKEN)

DEV_LINK = '<a href="https://www.instagram.com/akshitrana420">👑 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: 𝗔𝗸𝘀𝗵𝗶𝘁 𝗥𝗮𝗻𝗮 👑</a>'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"🚀 **Akshit Rana's Bot is Live!**\nSend Link or ZIP.\n\n{DEV_LINK}", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text and m.text.startswith('http'))
def handle_links(message):
    url = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🎥 Video", callback_data=f"v|{url}"),
               types.InlineKeyboardButton("🎶 Audio", callback_data=f"a|{url}"))
    bot.send_message(message.chat.id, "📥 Link Detected! Choose Format:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('v|', 'a|')))
def download(call):
    type, url = call.data.split('|')
    bot.edit_message_text("⚡ Processing...", call.message.chat.id, call.message.message_id)
    ydl_opts = {
        'format': 'best' if type == 'v' else 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as f:
                if type == 'v': bot.send_video(call.message.chat.id, f, caption=DEV_LINK, parse_mode='HTML')
                else: bot.send_audio(call.message.chat.id, f, caption=DEV_LINK, parse_mode='HTML')
            os.remove(filename)
    except: bot.send_message(call.message.chat.id, "❌ Error! Check if link is public.")

# ZIP logic
@bot.message_handler(content_types=['document'])
def handle_zip(message):
    if message.document.file_name.endswith('.zip'):
        bot.reply_to(message, "📦 ZIP Detected! Send Password or 'none'.")
        # (Zip code logic from previous turns)

keep_alive()
bot.polling(none_stop=True)
