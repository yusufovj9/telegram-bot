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

# Render so'rovlarini (GET va HEAD) qabul qiluvchi HTTP server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is live")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Muhit o'zgaruvchilarini olish
BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
TARGET_GROUP_1 = (os.getenv("TARGET_GROUP_1") or "").strip()
TARGET_GROUP_2 = (os.getenv("TARGET_GROUP_2") or "").strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # Guruh ID-larini songa aylantirish
    raw_groups = [TARGET_GROUP_1, TARGET_GROUP_2]
    groups = []
    for g in raw_groups:
        if g:
            try:
                groups.append(int(g))
            except ValueError:
                logging.error(f"Guruh ID son emas: {g}")

    if not groups:
        logging.warning("Guruh ID'lari topilmadi!")
        return

    caption_text = message.caption if message.caption else ""

    for group_id in groups:
        try:
            # 1. Ovozli xabar (Voice)
            if message.voice:
                await context.bot.send_voice(chat_id=group_id, voice=message.voice.file_id, caption=caption_text)
            
            # 2. Audio / Musiqa (MP3)
            elif message.audio:
                await context.bot.send_audio(chat_id=group_id, audio=message.audio.file_id, caption=caption_text)
            
            # 3. Rasm (Photo)
            elif message.photo:
                await context.bot.send_photo(chat_id=group_id, photo=message.photo[-1].file_id, caption=caption_text)
            
            # 4. Video (Oddiy video)
            elif message.video:
                await context.bot.send_video(chat_id=group_id, video=message.video.file_id, caption=caption_text)
            
            # 5. Video note (Krugloshka video)
            elif message.video_note:
                await context.bot.send_video_note(chat_id=group_id, video_note=message.video_note.file_id)
            
            # 6. Hujjat / Fayl (Document)
            elif message.document:
                await context.bot.send_document(chat_id=group_id, document=message.document.file_id, caption=caption_text)
            
            # 7. Matnli xabar (Text)
            elif message.text:
                await context.bot.send_message(chat_id=group_id, text=message.text)
            
            logging.info(f"Xabar {group_id} guruhiga muvaffaqiyatli yuborildi.")
        except Exception as e:
            logging.error(f"Xatolik yuz berdi: {e}")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Barcha xabarlarni ushlash
    all_filters = filters.ALL & (~filters.COMMAND)
    app.add_handler(MessageHandler(all_filters, handle_message))

    logging.info("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
