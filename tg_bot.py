from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import logging.config
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv


load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TG_TOKEN = os.getenv('TG_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')

logger = logging.getLogger('tg_bot')


def detect_intent_texts(session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        return None

    answer = response.query_result.fulfillment_text

    return answer


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
            update.message.chat_id, update.message.text, 'ru')
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
