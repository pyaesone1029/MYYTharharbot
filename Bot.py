import os, threading, http.server, requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 1. Render Port Fix (Service တည်ငြိမ်စေရန်)
class PortHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube Downloader v10 is Active!")

threading.Thread(target=lambda: http.server.HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), PortHandler).serve_forever(), daemon=True).start()

# 2. Cobalt v10 Logic (YouTube Bypass)
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if any(site in url for site in ["youtube.com", "youtu.be", "facebook.com", "tiktok.com", "instagram.com"]):
        await update.message.reply_text("ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        try:
            # Cobalt API v10 ကို အသုံးပြုခြင်း
            api_url = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": url,
                "videoQuality": "720", # v10 အတွက် videoQuality ဟု ပြောင်းလဲထားပါသည်
                "filenamePattern": "basic"
            }
            
            response = requests.post(api_url, json=payload, headers=headers).json()
            
            if response.get("status") == "stream" or response.get("url"):
                video_url = response.get("url")
                await update.message.reply_video(video=video_url, caption="ဒေါင်းလုပ် အောင်မြင်ပါပြီ! ✅")
            else:
                await update.message.reply_text(f"ဆောရီးပါ၊ API ကနေ ဗီဒီယို ရှာမတွေ့ပါ။")
        except Exception as e:
            await update.message.reply_text("စနစ် အနည်းငယ် အလုပ်မလုပ်ဖြစ်နေလို့ ခဏနေမှ ပြန်စမ်းပေးပါ။")
    else:
        await update.message.reply_text("YouTube/FB/TikTok/IG Link တွေ ပို့ပေးနိုင်ပါတယ်။")

def main():
    token = os.environ.get('BOT_TOKEN')
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot v10 is starting...")
    # drop_pending_updates က Conflict Error ကို ရှင်းပေးပါမည်
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
