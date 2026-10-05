import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
TARGET_GROUP_1 = (os.getenv("TARGET_GROUP_1") or "").strip()
TARGET_GROUP_2 = (os.getenv("TARGET_GROUP_2") or "").strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # Guruhda kelgan xabar bo'lsa, uni qayta yubormaymiz (cheksiz loop bo'lmasligi uchun)
    if message.chat.type in ['group', 'supergroup']:
        return

    logging.info(f"Yangi xabar keldi! Chat ID: {message.chat_id}")

    raw_groups = [TARGET_GROUP_1, TARGET_GROUP_2]
    groups = []
    for g in raw_groups:
        if g:
            try:
                groups.append(int(g))
            except ValueError:
                logging.error(f"Guruh ID noto'g'ri: '{g}'")

    if not groups:
        logging.error("Guruh ID'lari topilmadi!")
        return

    caption_text = message.caption if message.caption else ""

    for group_id in groups:
        try:
            if message.voice:
                await context.bot.send_voice(chat_id=group_id, voice=message.voice.file_id, caption=caption_text)
            elif message.audio:
                await context.bot.send_audio(chat_id=group_id, audio=message.audio.file_id, caption=caption_text)
            elif message.photo:
                await context.bot.send_photo(chat_id=group_id, photo=message.photo[-1].file_id, caption=caption_text)
            elif message.video:
                await context.bot.send_video(chat_id=group_id, video=message.video.file_id, caption=caption_text)
            elif message.video_note:
                await context.bot.send_video_note(chat_id=group_id, video_note=message.video_note.file_id)
            elif message.document:
                await context.bot.send_document(chat_id=group_id, document=message.document.file_id, caption=caption_text)
            elif message.text:
                await context.bot.send_message(chat_id=group_id, text=message.text)
            
            logging.info(f"Muvaffaqiyatli yuborildi: {group_id}")
        except Exception as e:
            logging.error(f"Guruhga yuborishda xatolik ({group_id}): {e}")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Har qanday xabar va mediamanbalarni tutib olish
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_message))
    
    logging.info("Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
