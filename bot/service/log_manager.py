import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime, timezone
from typing import Dict, Any


# basic logger class
class BotLoger:
    def __init__(self, log_file="./bot/logs/bot.log"):
        self.logger = logging.getLogger("TGRandombot")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _log(self, log_type: str, data: Dict[str, Any]):
        log_entry = {
            'timestamp': str(datetime.now(timezone.utc)),
            'type': log_type,
            **data
        }

        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def _get_traceback(self, error: Exception):
        import traceback
        return traceback.format_exc()

    def log_user_event(self, user_id: int, event_type: str, data: Dict[str, Any] = None):
        self._log("user_event", {
            "user_id": user_id,
            "event_type": event_type,
            "data": data,
        })

    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        self._log("error", {
            "error": str(error),
            "context": context,
            "traceback": self._get_traceback(error),
        })

    def log_system_event(self, event_type: str, data: Dict[str, Any] = None):
        self._log("system_event", {
            'event_type': event_type,
            'data': data
        })

bot_logger = BotLoger()
