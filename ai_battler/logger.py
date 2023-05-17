import logging
import json
import os


class JsonFormatter:
    def format(self, record):
        return json.dumps(vars(record))


def get_logger():
    logger = logging.getLogger(__name__)
    logger.basicConfig()
    logger.handlers[0].setFormatter(JsonFormatter())
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return logger
