from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from common.log_handle import BotLoger
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
        logger.log_user_event(int(uid), "BMW", str(data["event_from_user"]))
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
        # if F.text != 'Найти канал':
        # return await handler(event, data)
        ####
        uid = str(data["event_from_user"]).split()[0][3:]
        logger.log_user_event(int(uid), "CDMW", str(data["event_from_user"]))
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
