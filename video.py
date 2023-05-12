import os
import logging

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application
import yt_dlp

TOKEN = '5852966669:AAGboRyd6rYfIuKlN27oaBKqE9Q-UXXqLqA'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! Send me a link to a video and I will download and send it back to you in MP4 format.')


async def url_handler(update: Update, context: CallbackContext) -> None:
    """Download the video from the URL and send it back to the user."""
    url = update.message.text
    try:
        with yt_dlp.YoutubeDL({'format': 'mp4'}) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, 'rb'))
        os.remove(video_path)
    except Exception as e:
        logger.exception("Error downloading video")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't download the video.")


def main():

    # Starting bot
    app = Application.builder().token(TOKEN).build()

    # Adding commands
    app.add_handler(CommandHandler('start', start))

    # Handling messages
    app.add_handler(MessageHandler(filters.TEXT, url_handler))

    # Checking for messages every 5 seconds
    app.run_polling(poll_interval=5)


if __name__ == '__main__':
    main()
