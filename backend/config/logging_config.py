import logging, logging.config


LOGGING = {
    'version': 1,
    'formatters': {
        'default_formatter': {
            'format': '%(asctime).19s - %(name)s - [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter'
        },
        'main_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'filename': 'logs/api_chat.log',
            'maxBytes': 1048576,
            'backupCount': 5
        }
    },
    'loggers': {
        'main_logger': {
            'level': 'DEBUG',
            'handlers': ['console_handler', 'main_file_handler']
        }
    }
}


logger = logging.getLogger('main_logger')


def _setup_logger():
    logging.config.dictConfig(LOGGING)
