import os
from dotenv import load_dotenv
load_dotenv()


LOG_TOKEN = os.getenv('LOG_TOKEN')

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
            'chat_id': '90419999',
        },
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
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
