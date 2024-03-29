"""Example from 
https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
"""

import csv
import datetime
import logging
import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

load_dotenv()  # take environment variables from .env.

LOGGER = logging.getLogger(__name__)

FILE_PATH = os.environ["FILE_PATH"]
BOT_NAME = os.environ["BOT_NAME"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

MADRID_TIMEZONE = ZoneInfo("Europe/Madrid")


def config_logging() -> None:
    # Enable logging
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def should_i_write(text: str) -> bool:
    """Should I write the text in the message?."""
    return f"@{BOT_NAME}" in text


async def to_excel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Write to csv."""
    # Open the CSV file in write mode
    with open(FILE_PATH, "a", encoding="utf-8") as csvfile:
        if not update.message or not update.message.text or not should_i_write(update.message.text):
            return
        username = update.message.from_user.username if update.message.from_user else None
        message = update.message.text
        # Create a CSV writer object
        writer = csv.writer(csvfile, dialect="excel", delimiter="|")

        # Write a message to the CSV file
        now = datetime.datetime.now()
        writer.writerow([now.astimezone(MADRID_TIMEZONE), username, message])


def main() -> None:
    """Start the bot."""
    config_logging()
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - save to excel the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, to_excel))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
