import os, threading, http.server, requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 1. Port Fix
class PortHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

threading.Thread(target=lambda: http.server.HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), PortHandler).serve_forever(), daemon=True).start()

# 2. Downloader Logic
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if any(site in url for site in ["youtube.com", "youtu.be", "facebook.com", "tiktok.com", "instagram.com"]):
        await update.message.reply_text("ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        try:
            # ပိုမိုတည်ငြိမ်သော API Server ကို ပြောင်းလဲအသုံးပြုထားပါသည်
            api_url = "https://api.cobalt.tools/api/json" # သို့မဟုတ် "https://cobalt.mizunodev.xyz/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {"url": url, "vQuality": "720"}
            
            response = requests.post(api_url, json=payload, headers=headers).json()
            
            if "url" in response:
                await update.message.reply_video(video=response["url"], caption="ဒေါင်းလုပ် အောင်မြင်ပါပြီ! ✅")
            elif "text" in response:
                await update.message.reply_text(f"API Error: {response['text']}")
            else:
                await update.message.reply_text("ဆောရီးပါ၊ အခုလောလောဆယ် Server ဒေါင်းနေလို့ တခြား Link နဲ့ စမ်းကြည့်ပေးပါ။")
        except Exception as e:
            await update.message.reply_text("ခဏနားပြီးမှ ပြန်စမ်းပေးပါခင်ဗျာ။")
    else:
        await update.message.reply_text("YouTube/FB/TikTok/IG Link တွေ ပို့ပေးနိုင်ပါတယ်။")

def main():
    app = Application.builder().token(os.environ.get('BOT_TOKEN')).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
