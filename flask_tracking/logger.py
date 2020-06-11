from logging import Filter
from logging.config import dictConfig

from flask import request
from flask_login import current_user



class ContextualFilter(Filter):
    def filter(self, log_record):
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        log_record.user_id = -1 if\
            current_user.is_anonymous() else\
            current_user.get_id()
        return True



def setup_logger(app, level=10):
    error_log_path = app.config.get('ERROR_LOG_PATH') if\
        app.config.get("ERROR_LOG_PATH") else ""

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'contextual': {
                '()': 'flask_tracking.logger.ContextualFilter'
            }
        },
        'formatters': { 
            'standard': { 
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'debug_format': {
                'format':   "%(asctime)s\t%(levelname)s\tUser <%(user_id)-5s> "
                            "from %(ip)-16s\t%(method)-5s\t%(url)s\t%(message)s\n"
                            "\t\"%(filename)s\" on line: [%(lineno)i] "
                            "from function: <%(funcName)s>\n\t%(pathname)s"
            },
            'info_format': {
                'format':   "%(asctime)s\t%(levelname)s\tUser <%(user_id)-5s> "
                            "from %(ip)-16s\t%(method)-5s\t%(url)s\t%(message)s\n"
            },
            'file_format': {
                'format':   "-----------------------------------------------"
                            "-------------------------------------\n"
                            "%(asctime)-20s::%(levelname)-8s::%(method)-5s::"
                            "%(ip)-16s::%(user_id)-5s::%(url)s\n"
                            "\tMessage: %(message)s\n"
                            "\tException: %(exc_info)s\n\n"
            }
        },
        'handlers': {
            'default': { 
                'level': level,
                'formatter': 'info_format',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'filters': ['contextual']
            },
            'debug': {
                'level': 'DEBUG',
                'formatter': 'debug_format',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'filters': ['contextual']
            },
            'filer': {
                'level': level,
                'formatter': 'file_format',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': error_log_path,
                'when': 'D', 
                'backupCount': 7,
                'filters': ['contextual'],
                "encoding": "utf-8"
            }
        },
        'loggers': {
            app.name: {
                'handlers': ['debug', 'default', 'filer'],
                'level': level,
                'propagate': False
            }
        }
    }

    dictConfig(LOGGING_CONFIG)


def init_app(app, level):
    setup_logger(app, level)
