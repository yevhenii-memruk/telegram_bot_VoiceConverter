from typing import Final
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, Updater, filters

from audio_text import AudioConverter


TOKEN: Final = "6841833282:AAGCIyoHLTZmp9JElj1oEr1WZPGuTXE-jAI"
BOT_USERNAME: Final = "@memrik_bot"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Send me your record voice in \".ogg\" format\n\t OR\njust start recording your voice message🤩"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def downloader(update, context):
    # Downloading user's voice message
    file = await context.bot.get_file(update.message.voice)
    await file.download_to_drive("audio/user_voice.ogg")

    converter = AudioConverter(audio="audio/user_voice.ogg", file_name="result.wav")
    converter.converter_ogg_to_wav()
    converter.audio_recognizer()

    # Sending text from converted audio
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{converter.recognized_text}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Commands
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Message
    application.add_handler(MessageHandler(filters.VOICE, downloader))
    
    application.run_polling()