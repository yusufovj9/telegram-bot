import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token va guruh ID'larini muhit o'zgaruvchilaridan (Environment Variables) olamiz
BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
TARGET_GROUP_1 = os.getenv("TARGET_GROUP_1")
TARGET_GROUP_2 = os.getenv("TARGET_GROUP_2")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    groups = [TARGET_GROUP_1, TARGET_GROUP_2]
    success_count = 0

    # 1. Agar rasm (foto) yuborilgan bo'lsa
    if message.photo:
        # Eng yuqori sifatli rasmni olamiz (ro'yxatning oxirgi elementi)
        photo_file_id = message.photo[-1].file_id
        caption = message.caption or "" # Rasmdagi yozuv (matn) bo'lsa uni ham saqlaymiz
        
        logging.info("Rasm qabul qilindi, guruhlarga yuborilmoqda...")
        for group_id in groups:
            if group_id:
                try:
                    await context.bot.send_photo(chat_id=group_id, photo=photo_file_id, caption=caption)
                    logging.info(f"Rasm muvaffaqiyatli yuborildi: {group_id}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"Xatolik yuz berdi {group_id} ga rasm yuborishda: {e}")

    # 2. Agar audio yoki ovozli xabar yuborilgan bo'lsa
    elif message.audio or message.voice:
        file_id = message.audio.file_id if message.audio else message.voice.file_id
        logging.info("Audio/ovozli xabar qabul qilindi, guruhlarga yuborilmoqda...")
        
        for group_id in groups:
            if group_id:
                try:
                    if message.audio:
                        await context.bot.send_audio(chat_id=group_id, audio=file_id)
                    else:
                        await context.bot.send_voice(chat_id=group_id, voice=file_id)
                    logging.info(f"Audio muvaffaqiyatli yuborildi: {group_id}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"Xatolik yuz berdi {group_id} ga yuborishda: {e}")

    # Natija haqida xabar berish
    if success_count > 0:
        await message.reply_text("Xabar guruhlarga muvaffaqiyatli tarqatildi!")
    else:
        await message.reply_text("Xatolik: Xabarni guruhlarga yuborib bo'lmadi. Guruh ID'larini tekshiring.")

def main():
    if not BOT_TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN topilmadi!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Rasm, audio va ovozli xabarlarni birga ushlash uchun handler
    media_handler = MessageHandler(filters.PHOTO | filters.AUDIO | filters.VOICE, handle_media)
    app.add_handler(media_handler)

    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
