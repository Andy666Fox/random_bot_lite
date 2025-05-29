import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime


class BotLoger:
    def __init__(self, log_file="bot.log"):
        self.logger = logging.getLogger("TGRandombot")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            json.dumps(
                {
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "message": "%(message)s",
                }
            )
        )

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_user_event(self, user_id: int, event_type: str, data):
        self.logger.info(
            {
                "user_id": user_id,
                "event_type": event_type,       
                "data": data,
            }
        )

    def log_db_interaction(self, user_id: int, event_type: str, data):
        pass    

    def log_error(self, error: Exception, context: dict = None):
        self.logger.error(
            {
                "error": str(error),
                "context": context,
                "traceback": self._get_traceback(error),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
