# https://gitlab.com/atronah/pythonista_extensions/tree/master

import logging
import console

class AlertHandler(logging.Handler):
    def emit(self, record):
        console.alert(record.levelname, record.msg, button1='Ok', hide_cancel_button=True)

def clear_handlers(logger_name=None):
    logger = logging.getLogger(logger_name)
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)
    return logger


def setup_alert_logging(logger_name=None, level=logging.INFO):
    logger = clear_handlers(logger_name) 
    logger.addHandler(AlertHandler(level))
    logger.setLevel(level)

