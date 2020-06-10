from logging import NOTSET, DEBUG, ERROR, INFO, WARNING, Filter, Formatter, getLogger, StreamHandler
from logging.handlers import TimedRotatingFileHandler

from flask import request
from flask_login import current_user




class ContextualFilter(Filter):
    def filter(self, log_record):
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        log_record.user_id = -1 if current_user.is_anonymous() else current_user.get_id()

        return True



def setup_logger(app):
    app.logger.addFilter(ContextualFilter())

    if app.debug:
        # Add a formatter that makes use of our new contextual information
        debug_handler = StreamHandler()
        log_format = "---------------------------------------------------------------------------------------------\n"
        log_format += "%(asctime)s\t%(levelname)s\tUser <%(user_id)s> from %(ip)s\t%(method)s\t%(url)s\t%(message)s\n"
        log_format += "     Line: %(lineno)i from function: <%(funcName)s>\tin %(filename)s\n     %(pathname)s"
        formatter = Formatter(log_format)
        debug_handler.setLevel(DEBUG) # sets Handler level
        debug_handler.setFormatter(formatter)
        app.logger.addHandler(debug_handler)
        #app.logger.setLevel(DEBUG)
    else:
        info_handler = StreamHandler()
        log_format = "---------------------------------------------------------------------------------------------\n"
        log_format += "%(asctime)s\t%(levelname)s\tUser <%(user_id)s> from %(ip)s\t%(method)s\t%(url)s\t%(message)s\n"
        formatter = Formatter(log_format)
        info_handler.setLevel(INFO) # sets Handler level
        info_handler.setFormatter(formatter)
        app.logger.addHandler(info_handler)
        app.logger.setLevel(INFO) # sets Logger level
    
    print(app.logger)
    print(app.logger.handlers)

    # Only set up a file handler if we know where to put the logs
    if app.config.get("ERROR_LOG_PATH"):
        # Create one file for each day. Delete logs over 7 days old.
        file_handler = TimedRotatingFileHandler(app.config["ERROR_LOG_PATH"], when="D", backupCount=7)

        # Use a multi-line format for this logger, for easier scanning
        file_formatter = Formatter(
        "%(asctime)s::%(levelname)s::%(method)s::%(url)s::%(ip)s::%(user_id)s\n"
        "Message: %(message)s\n"
        "Exception: %(exc_info)s\n"
        "------------------------------------------")

        # Filter out all log messages that are lower than Error.
        file_handler.setLevel(WARNING)
        file_handler.setFormatter(file_formatter)
        app.logger.addHandler(file_handler)
        


def init_app(app):
    setup_logger(app)
