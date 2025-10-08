from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from log_handle import BotLoger
from defaults import ANSWER_TO_FLOOD
import functools
from monitoring.metrics_server import metrics
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

        try:
            handler_name = getattr(handler, '__name__', 'unknown_handler')
            if handler_name == 'unknown_handler':
                if hasattr(handler, 'func'):
                    handler_name = getattr(handler.func, '__name__', 'unknown_handler')
        except:
            handler_name = 'unknown_handler'

        logger.log_user_event(user_id, handler_name, event.from_user.username)
        last_action = self.user_last_action.get(user_id)
        if last_action and (current_time - last_action) < self.cooldown:
            await event.answer(ANSWER_TO_FLOOD)
            return
        
        self.user_last_action[user_id] = current_time
        return await handler(event, data)
    
class MetricsMW(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            event: object,  # Message, CallbackQuery, etc.
            data: Dict[str, Any]
        ) -> Any:
            user_id = str(event.from_user.id) if hasattr(event, 'from_user') else 'unknown'
            metrics.record_request(user_id)

            return await handler(event, data)
