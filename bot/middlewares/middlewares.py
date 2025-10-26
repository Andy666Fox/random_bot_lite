import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from service.default_answers import ANSWER_TO_FLOOD
from service.log_manager import bot_logger


class CooldownMW(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = 1):
        self.user_last_action = {}
        self.cooldown = cooldown_seconds

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        try:
            handler_name = getattr(handler, "__name__", "unknown_handler")
            if handler_name == "unknown_handler" and hasattr(handler, "func"):
                handler_name = getattr(handler.func, "__name__", "unknown_handler")
        except Exception:
            handler_name = "unknown_handler"

        last_action = self.user_last_action.get(user_id)

        if last_action and (current_time - last_action) < self.cooldown:
            await event.answer(ANSWER_TO_FLOOD)
            bot_logger.log_user_event(
                user_id, "spaming", data={"time_window": current_time - last_action}
            )
            return

        self.user_last_action[user_id] = current_time
        return await handler(event, data)
