from routers import basic_router
from aiogram import types, F
from keyboards.builder import get_channel_rating_inline_keyboard
from utils.cache_manager import cache_manager
from utils.log_manager import log_manager

@basic_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    user_id = message.from_user.id
    channel, summary = await cache_manager.get_channel_with_summary_from_cache(user_id)
    text = f"@{channel}\n{summary}"

    log_manager.log_user_event(
        message.from_user.id, "search channel", data={f"Bot response to {message.from_user.username}": channel}
    )

    await message.answer(text, reply_markup=get_channel_rating_inline_keyboard(channel))