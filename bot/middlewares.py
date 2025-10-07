from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from log_handle import BotLoger
from defaults import ANSWER_TO_FLOOD
import time

logger = BotLoger()

class CooldownMW(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = 1):
        self.user_last_action = {}
        self.cooldown = cooldown_seconds

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        logger.log_user_event(user_id, handler.__name__, event.from_user.username)

        last_action = self.user_last_action.get(user_id)
        if last_action and (current_time - last_action) < self.cooldown:
            await event.answer(ANSWER_TO_FLOOD)
            return
        
        self.user_last_action[user_id] = current_time
        return await handler(event, data)