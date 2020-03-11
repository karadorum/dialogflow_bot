from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import os
import logging
import logging.config
from google_response import detect_intent_texts
from dotenv import load_dotenv
load_dotenv()


VK_TOKEN = os.getenv('VK_TOKEN')

logger = logging.getLogger('vk_bot')


def reply_message(event, vk_api):
    try:
        answer = detect_intent_texts(event.user_id, event.text)
    except:
        logger.exception('detect intent not working')

    if not answer:
        pass
        logger.info(f"message: {event.text}, not answered")
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
        logger.info(f"message: {event.text}, answered: {answer}")


def start_vk_bot():
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_message(event, api)


if __name__ == "__main__":
    start_vk_bot()
