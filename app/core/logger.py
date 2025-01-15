import logging.config

STDOUT_FORMAT = '%(log_color)s[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
FILE_FORMAT = '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', 'file']
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
            'format': STDOUT_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'file': {
            'format': FILE_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'formatter': 'verbose',
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'formatter': 'file',
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'app_error.log',
        },
        'access': {
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
        'uvicorn.error': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'uvicorn.access': {
            'level': 'INFO'
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
