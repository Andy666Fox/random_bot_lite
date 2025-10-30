from routers import decline_router
from aiogram import types, F
from utils.globals import BLOCKED_CONTENT_TYPES

from utils.message_manager import message_manager
from utils.log_manager import log_manager


@decline_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    log_manager.log_user_event(message.from_user.id, "wrong media type")
    await message.answer(message_manager.ANSWER_TO_MEDIA)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(message_manager.ANSWER_TO_WRONG_TEXT)
    log_manager.log_user_event(message.from_user.id, f"User entry: {str(message.text)}")
    await message.delete()