from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import dialogflow
import os


GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TG_TOKEN = os.getenv('TG_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')
SESSION_ID = 'current-user-id'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


REQUEST_KWARGS = {
    'proxy_url': 'socks5://95.216.145.100:1080',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'karadorum',
        'password': '13162007',
    }
}


def detect_intent_texts(project_id, session_id, text, language_code):
    import dialogflow_v2 as dialogflow
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


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте! Пишите сюда что попало')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    answer = detect_intent_texts(
        PROJECT_ID, SESSION_ID, update.message.text, 'ru')
    update.message.reply_text(answer)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(
        TG_TOKEN, request_kwargs=REQUEST_KWARGS, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
