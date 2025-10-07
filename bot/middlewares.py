from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from log_handle import BotLoger
from defaults import ANSWER_TO_FLOOD
import time

logger = BotLoger()


class BasicMW(BaseMiddleware):
    """parent middleware, contains basic mw functionality"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        ####
        uid = str(data["event_from_user"]).split()[0][3:]
        logger.log_user_event(
            int(uid), f"{handler.__name__}", str(data["event_from_user"]).split(" ")[4]
        )
        ####
        return await handler(event, data)


class CooldownMW(BaseMiddleware):
    """Middleware for antispam control"""

    def __init__(self):
        self.user_last_action = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        ####
        uid = str(data["event_from_user"]).split()[0][3:]
        logger.log_user_event(
            int(uid), f"{handler.__name__}", str(data["event_from_user"]).split(" ")[4]
        )
        ####

        # check the user last action time
        user_id = event.from_user.id
        current_time = time.time()
        last_action = self.user_last_action.get(user_id)

        # send warning message if duration less than 3 seconds
        if last_action and (current_time - last_action) < 2:
            await event.answer("Отставить спам, погоди пару секунд")
            return

        # user last action time update
        self.user_last_action[user_id] = current_time
        return await handler(event, data)



class CoolDownMW(BaseMiddleware):
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