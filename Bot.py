import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 1. Render Port Fix
class PortHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_port_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), PortHandler)
    server.serve_forever()

threading.Thread(target=run_port_server, daemon=True).start()

# 2. Telegram Bot Code (Using python-telegram-bot)
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update, context):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က Render ပေါ်မှာ အောင်မြင်စွာ အလုပ်လုပ်နေပါပြီ။")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
