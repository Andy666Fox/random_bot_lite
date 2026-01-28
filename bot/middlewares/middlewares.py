import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.log_manager import log_manager
from utils.message_manager import message_manager
from utils.defaults import defaults

class CooldownMW(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = defaults.cooldown_seconds):
        super().__init__()
        self.user_last_action: dict[int, float] = {}
        self.cooldown = cooldown_seconds

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        # Safely get handler name with better exception handling
        handler_name = "unknown_handler"
        try:
            if hasattr(handler, "__name__"):
                handler_name = handler.__name__
            elif hasattr(handler, "func"):
                handler_name = getattr(handler.func, "__name__", "unknown_handler")
            elif hasattr(handler, "__func__"):
                handler_name = getattr(handler.__func__, "__name__", "unknown_handler")
        except Exception:
            # If we can't determine the handler name, continue without it
            pass

        last_action = self.user_last_action.get(user_id)

        if last_action and (current_time - last_action) < self.cooldown:
            await event.answer(message_manager.ANSWER_TO_FLOOD)
            log_manager.log_user_event(
                user_id,
                "spamming",
                data={"time_window": current_time - last_action, "in handler": handler_name},
            )
            return

        self.user_last_action[user_id] = current_time
        return await handler(event, data)
