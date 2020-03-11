from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import logging.config
from google_response import detect_intent_texts
from dotenv import load_dotenv
load_dotenv()


TG_TOKEN = os.getenv('TG_TOKEN')



logger = logging.getLogger('tg_bot')


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте! Пишите сюда что попало')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Help! It's real help for helping you by our help!")


def reply_message(update, context):

    try:
        answer = detect_intent_texts(
            update.message.chat_id, update.message.text)
        logger.info(
            f"message:{update.message.text}, answered: {answer}")
        update.message.reply_text(answer)
    except:
        logger.exception('detect intent not working')


def start_tg_bot():
    """Start the bot."""
    updater = Updater(
        TG_TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_tg_bot()
