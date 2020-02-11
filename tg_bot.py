from dictconfig import LOGGING_CONFIG
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
SESSION_ID = 'current-user-id'
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
PROXY_URL = os.getenv('PROXY_URL')


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('tg_bot')


REQUEST_KWARGS = {
    'proxy_url': PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': USERNAME,
        'password': PASSWORD,
    }
}


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

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
            PROJECT_ID, SESSION_ID, update.message.text, 'ru')
        logger.info(
            f"message:{update.message.text}, answered: {answer}")
        update.message.reply_text(answer)
    except:
        logger.exception('detect intent not working')


def main():
    """Start the bot."""
    updater = Updater(
        TG_TOKEN, request_kwargs=REQUEST_KWARGS, use_context=True)
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
    main()
