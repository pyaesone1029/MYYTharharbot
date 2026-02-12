import os
import threading
import http.server
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

# 1. Render Port Fix Section (Bot မပိတ်သွားအောင် ကူညီပေးမည့်အပိုင်း)
class PortHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube Downloader Bot is Running!")

def run_port_server():
    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(('0.0.0.0', port), PortHandler)
    server.serve_forever()

# Port server ကို background မှာ run ထားပါမယ်
threading.Thread(target=run_port_server, daemon=True).start()

# 2. YouTube Download Logic Section
async def download_video(update, context):
    url = update.message.text
    # YouTube Link ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'max_filesize': 50 * 1024 * 1024  # 50MB ထက်ကျော်ရင် ဒေါင်းမှာမဟုတ်ပါ (Free Plan RAM အတွက်)
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # ဒေါင်းပြီးသား ဗီဒီယိုကို Telegram ဆီ ပြန်ပို့ပေးခြင်း
            with open('video.mp4', 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="ဒေါင်းလို့ အောင်မြင်ပါပြီ!")
            
            # စက်ထဲမှာ နေရာမရှုပ်အောင် ဖျက်ပစ်ခြင်း
            os.remove('video.mp4')
            
        except Exception as e:
            await update.message.reply_text(f"အမှားအယွင်းရှိသွားပါတယ်- {str(e)}")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ YouTube Link ကိုပဲ ပို့ပေးပါခင်ဗျာ။")

# 3. Main Bot Process
def main():
    # Render Environment ထဲက BOT_TOKEN ကို ယူသုံးခြင်း
    TOKEN = os.environ.get('BOT_TOKEN')
    
    application = Application.builder().token(TOKEN).build()
    
    # စာသားဝင်လာတိုင်း ဒေါင်းမလားဆိုတာ စစ်ဆေးမယ့် handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("Bot is starting with YouTube Downloader logic...")
    application.run_polling()

if __name__ == "__main__":
    main()
