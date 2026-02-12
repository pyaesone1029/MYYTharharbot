import os, threading, http.server, requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 1. Render Port Fix (Service မပိတ်အောင်လုပ်ပေးခြင်း)
class PortHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube Downloader Pro is Online!")

threading.Thread(target=lambda: http.server.HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), PortHandler).serve_forever(), daemon=True).start()

# 2. Cobalt API Downloader (YouTube ရဲ့ ကန့်သတ်ချက်ကို ကျော်လွှားရန်)
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if any(site in url for site in ["youtube.com", "youtu.be", "facebook.com", "tiktok.com"]):
        await update.message.reply_text("ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        try:
            # API သုံးပြီး YouTube ကန့်သတ်ချက်ကို ကျော်ဖြတ်ခြင်း
            api_url = "https://api.cobalt.tools/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {"url": url, "vQuality": "720"}
            
            response = requests.post(api_url, json=payload, headers=headers).json()
            
            if "url" in response:
                await update.message.reply_video(video=response["url"], caption="ဒေါင်းလုပ် အောင်မြင်ပါပြီ! ✅")
            else:
                await update.message.reply_text("ဆောရီးပါ၊ ဒီဗီဒီယိုကို ဒေါင်းလို့မရသေးပါ။")
        except Exception as e:
            await update.message.reply_text("စနစ် အမှားအယွင်းရှိနေလို့ ခဏနေမှ ပြန်စမ်းပေးပါ။")
    else:
        await update.message.reply_text("YouTube/FB/TikTok Link တွေ ပို့ပေးနိုင်ပါတယ်။")

def main():
    token = os.environ.get('BOT_TOKEN')
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot is starting...")
    # drop_pending_updates က Conflict Error ကို ရှင်းပေးပါလိမ့်မယ်
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
