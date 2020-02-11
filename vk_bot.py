from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from dictconfig import LOGGING_CONFIG
import random
import os
import logging
import logging.config
from dotenv import load_dotenv
load_dotenv()


VK_TOKEN = os.getenv('VK_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SESSION_ID = 'current-user-id'


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('vk_bot')


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
    if response.query_result.intent.is_fallback == True:
        return None
    else:
        answer = response.query_result.fulfillment_text
        return answer


def reply_message(event, vk_api):
    try:
        answer = detect_intent_texts(
            PROJECT_ID, SESSION_ID, event.text, 'ru')
    except:
        logger.exception('detect intent not working')

    if answer == None:
        pass
        logger.info(f"message: {event.text}, not answered")
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
        logger.info(f"message: {event.text}, answered: {answer}")


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_message(event, vk_api)
