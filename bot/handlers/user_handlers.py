from aiogram import F, Router, types
from aiogram.types import BufferedInputFile, LinkPreviewOptions

from keyboards.builder import get_channel_rating_inline_keyboard

from middlewares.middlewares import CooldownMW
from utils.globals import BLOCKED_CONTENT_TYPES
from utils.log_manager import log_manager
from utils.message_manager import message_manager
from utils.math_manager import math_manager
from database.methods import get_random_channel
from wc_manager.wordcloud_gen import _get_wordcloud_image

user_router = Router()
user_router.message.middleware(CooldownMW())

@user_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    user_id = message.from_user.id
    channel = await get_random_channel()
    log_manager.log_user_event(
         user_id, "search channel", data={f"Bot response to {message.from_user.username}": channel}
    )
    content = await math_manager._get_channel_content(channel)
    image_bytes = _get_wordcloud_image(content)

    photo = BufferedInputFile(image_bytes, filename="channel_tags.png")
    caption = f"https://t.me/{channel}"

    log_manager.log_user_event(
         user_id, "search channel", data={f"Bot response to {message.from_user.username}": channel}
    )

    await message.answer_photo(photo)
    await message.answer(f"https://t.me/{channel}",
                         link_preview_options=LinkPreviewOptions(is_disabled=False),
                         reply_markup=get_channel_rating_inline_keyboard(channel))





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
