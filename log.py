import logging.config
import logging.handlers
import os
import logging
from flask import request
from utils import work_dir
from datetime import datetime

def set_logging_handle(filepath, level, handle_type):

    class ResultFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            self.datefmt = "%Y%m%d%H%M%S"
            return super().format(record)
        
    result_formatter = ResultFormatter('[%(asctime)s] [%(name)s] %(remote_addr)s requested %(url)s %(levelname)s in %(module)s: %(message)s')

    if handle_type == "file":
        logging_handler = logging.handlers.TimedRotatingFileHandler(filepath, when="midnight", interval=1, encoding="utf-8", backupCount=3660)
    else:
        logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(result_formatter)
    logging_handler.setLevel(level)
    return logging_handler

def register_logging(app):
    # handle_type = "file" if not app.debug else "stdout"
    for handle_type in ["stdout", "stderr", "file"]:
        debug_logging_handle = set_logging_handle(app.config["LOG"]["DEBUG_LOG_FILEPATH"], logging.DEBUG, handle_type)
        info_logging_handle = set_logging_handle(app.config["LOG"]["INFO_LOG_FILEPATH"], logging.INFO, handle_type)
        warning_logging_handle = set_logging_handle(app.config["LOG"]["WARNING_LOG_FILEPATH"], logging.WARNING, handle_type)
        error_logging_handle = set_logging_handle(app.config["LOG"]["ERROR_LOG_FILEPATH"], logging.ERROR, handle_type)
        critical_logging_handle = set_logging_handle(app.config["LOG"]["CRITICAL_LOG_FILEPATH"], logging.CRITICAL, handle_type)

        app.logger.setLevel(logging.INFO) if not app.debug else app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(debug_logging_handle)
        app.logger.addHandler(info_logging_handle)
        app.logger.addHandler(warning_logging_handle)
        app.logger.addHandler(error_logging_handle)
        app.logger.addHandler(critical_logging_handle)

os.makedirs(os.path.join(work_dir, "logs", "note"), exist_ok=True)
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] [%(name)s] %(levelname)s in %(module)s: %(message)s",
            "datefmt": "%Y%m%d%H%M%S"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "simple",
            "stream": "ext://sys.stderr"
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": os.path.join(work_dir, "logs", "note", "demo.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 3660
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "stdout",
            "stderr",
            "file"
        ]
    }
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger("note")
