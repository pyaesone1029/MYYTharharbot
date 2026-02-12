import asyncio
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp


TOKEN =os.getenv('BOT_TOKEN')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ဗီဒီယိုကို စတင်ဒေါင်းလုဒ်ဆွဲနေပါပြီ... ခဏစောင့်ပါခင်ဗျာ။")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'myvideo.mp4',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('myvideo.mp4', 'rb') as video:
                await update.message.reply_video(video)
            os.remove('myvideo.mp4')
        except Exception as e:
            await update.message.reply_text(f"အမှားအယွင်းတစ်ခု ရှိသွားပါတယ်: {str(e)}")
    else:
        await update.message.reply_text("YouTube Link ပေးပို့ပေးပါဦး။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
