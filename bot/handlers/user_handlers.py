from aiogram import F, Router, types
from keyboards.builder import get_channel_rating_inline_keyboard
from middlewares.middlewares import CooldownMW
from utils.cache_manager import cache_manager
from utils.globals import BLOCKED_CONTENT_TYPES
from utils.log_manager import log_manager
from utils.message_manager import message_manager

user_router = Router()
user_router.message.middleware(CooldownMW())


@user_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    user_id = message.from_user.id
    channel, summary = await cache_manager.get_channel_with_summary_from_cache(user_id)
    text = f"@{channel}\n{summary}"

    log_manager.log_user_event(
        user_id, "search channel", data={f"Bot response to {message.from_user.username}": channel}
    )

    await message.answer(text, reply_markup=get_channel_rating_inline_keyboard(channel))


@user_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    log_manager.log_user_event(message.from_user.id, "wrong media type")
    await message.answer(message_manager.ANSWER_TO_MEDIA)


# Invalid text command handler
@user_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(message_manager.ANSWER_TO_WRONG_TEXT)
    log_manager.log_user_event(message.from_user.id, f"User entry: {str(message.text)}")
    await message.delete()
