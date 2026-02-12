import os
import threading
import telebot
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Render Port Fix Section
class PortHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_port_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), PortHandler)
    server.serve_forever()

# Start Port Server in Background
threading.Thread(target=run_port_server, daemon=True).start()

# 2. Telegram Bot Section
# Get Token from Render Environment Variable
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်တော်က Render ပေါ်မှာ အောင်မြင်စွာ အလုပ်လုပ်နေပါပြီ။")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# 3. Start the Bot
print("Bot is starting...")
bot.infinity_polling()
