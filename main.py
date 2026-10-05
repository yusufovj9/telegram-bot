import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render portini ushlab turish uchun HTTP server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is live")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Muhit o'zgaruvchilarini olish (.strip() ortiqcha \n va probellarni tozalaydi)
BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
TARGET_GROUP_1 = (os.getenv("TARGET_GROUP_1") or "").strip()
TARGET_GROUP_2 = (os.getenv("TARGET_GROUP_2") or "").strip()

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    groups = [g for g in [TARGET_GROUP_1, TARGET_GROUP_2] if g]
    
    if not groups:
        logging.warning("Guruh ID'lari topilmadi!")
        return

    for group_id in groups:
        try:
            # Media turiga qarab guruhlarga yuborish
            if message.voice:
                await context.bot.send_voice(chat_id=group_id, voice=message.voice.file_id)
            elif message.audio:
                await context.bot.send_audio(chat_id=group_id, audio=message.audio.file_id)
            elif message.photo:
                await context.bot.send_photo(chat_id=group_id, photo=message.photo[-1].file_id, caption=message.caption or "")
            elif message.document:
                await context.bot.send_document(chat_id=group_id, document=message.document.file_id, caption=message.caption or "")
            logging.info(f"Xabar {group_id} guruhiga yuborildi.")
        except Exception as e:
            logging.error(f"{group_id} guruhiga yuborishda xatolik: {e}")

def main():
    # Web serverni alohida oqimda (thread) ishga tushirish
    threading.Thread(target=run_http_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Ovozli xabar, audio, rasm va hujjatlarni ushlab qolish
    media_filter = filters.VOICE | filters.AUDIO | filters.PHOTO | filters.Document.ALL
    app.add_handler(MessageHandler(media_filter, handle_media))

    logging.info("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
