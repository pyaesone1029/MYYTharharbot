import os
import threading
import http.server
import telegram
from telegram.ext import Application, MessageHandler, filters
import yt_dlp

# 1. Render Port Fix (Bot Live ဖြစ်နေစေရန်)
class PortHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube Downloader is Online!")

def run_port_server():
    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(('0.0.0.0', port), PortHandler)
    server.serve_forever()

threading.Thread(target=run_port_server, daemon=True).start()

# 2. YouTube Bypass & Download Section
async def download_video(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            # YouTube security ကို ကျော်လွှားရန် setting များ
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # ဗီဒီယိုအရွယ်အစား 50MB ထက်ကြီးရင် Telegram ပို့မရလို့ စစ်ပါမယ်
                filesize = os.path.getsize('video.mp4')
                if filesize > 50 * 1024 * 1024:
                    await update.message.reply_text("ဗီဒီယိုက အရမ်းကြီးနေပါတယ် (50MB ထက်ကျော်သည်)။")
                    os.remove('video.mp4')
                    return

            with open('video.mp4', 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="ဒေါင်းလို့ အောင်မြင်ပါပြီ!")
            
            os.remove('video.mp4')
            
        except Exception as e:
            await update.message.reply_text("YouTube က ကန့်သတ်ထားလို့ ဒီဗီဒီယိုကို ဒေါင်းမရဖြစ်နေပါတယ်။ အခြားတစ်ခုနဲ့ ထပ်စမ်းကြည့်ပေးပါ။")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ YouTube Link ကိုပဲ ပို့ပေးပါခင်ဗျာ။")

def main():
    TOKEN = os.environ.get('BOT_TOKEN')
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot is starting with Bypass mode...")
    application.run_polling()

if __name__ == "__main__":
    main()
