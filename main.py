import os
import logging.config
from tg_bot import start_tg_bot as tgbot
from vk_bot import start_vk_bot as vkbot
import argparse
from dotenv import load_dotenv


parser = argparse.ArgumentParser()
parser.add_argument("-start", help="starts VK or TG bot",
                    choices=['vkbot', 'tgbot'])

load_dotenv()
LOG_TOKEN = os.getenv('LOG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


if __name__ == "__main__":
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'telegram': {
                'class': 'telegram_handler.TelegramHandler',
                'level': 'WARNING',
                'formatter': 'standard',
                'token': LOG_TOKEN,
                'chat_id': TG_CHAT_ID,
            },
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'WARNING',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'fileHandler': {
                'class': 'logging.FileHandler',
                'level': 'WARNING',
                'formatter': 'standard',
                'filename': 'myapp.log',
                'mode': 'a',
            }
        },
        'loggers': {
            'tg_bot': {
                'handlers': ['telegram', 'consoleHandler', 'fileHandler'],
                'level': 'DEBUG'
            },
            'vk_bot': {
                'handlers': ['telegram', 'consoleHandler', 'fileHandler'],
                'level': 'DEBUG'
            }
        }
    }
    
    logging.config.dictConfig(LOGGING_CONFIG)
    args = parser.parse_args()

    if args.start == 'tgbot':
        tgbot()

    if args.start == 'vkbot':
        vkbot()
