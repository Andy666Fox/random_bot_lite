import random

from aiogram import F, Router, types
from database.methods import get_random_channel
from keyboards.keyboards import get_channel_rating_inline_keyboard
from middlewares.middlewares import CooldownMW
from service.log_manager import bot_logger

from bot.service.bot_answers import bot_answers

decline_router = Router()
basic_router = Router()
decline_router.message.middleware(CooldownMW())
basic_router.message.middleware(CooldownMW())


@basic_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    channel = await get_random_channel()
    text = f"{random.choice(bot_answers.ANSWERS)}\n@{channel}"
    bot_logger.log_user_event(
        message.from_user.id, "search channel", data={"Bot response": channel}
    )

    await message.answer(text, reply_markup=get_channel_rating_inline_keyboard(channel))


# Invalid content type reaction handler
@decline_router.message(F.content_type.in_(bot_answers.BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    bot_logger.log_user_event(message.from_user.id, "wrong media type")
    await message.answer(bot_answers.ANSWER_TO_MEDIA)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(bot_answers.ANSWER_TO_WRONG_TEXT)
    bot_logger.log_user_event(message.from_user.id, f"User entry: {str(message.text)}")
    await message.delete()
