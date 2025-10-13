from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram import F

from keyboards.keyboards import get_main_keyboard
from defaults import (
    ANSWERS,
    START_MESSAGE,
    ANSWER_TO_MEDIA,
    ANSWER_TO_WRONG_TEXT,
    BLOCKED_CONTENT_TYPES
)
from middlewares.middlewares import CooldownMW
from bot.database.methods import get_random_channel
from log_manager import bot_logger

import random

# bot have two types of routers
# DECLINE routers react for invalid messages (message types)
# GET_Channel normal work router. Control message sending from bot

decline_router = Router()
get_channel_router = Router()
decline_router.message.middleware(CooldownMW())
get_channel_router.message.middleware(CooldownMW())

# Initial button handler
@get_channel_router.message(Command("start"))
async def send_welcome(message: types.Message):
    bot_logger.log_user_event(message.from_user.id, 'start', data={'Bot started by user': message.from_user.id})
    await message.answer(START_MESSAGE, reply_markup=get_main_keyboard())


# Main button handler
@get_channel_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    channel = await get_random_channel()
    text = f"{random.choice(ANSWERS)}\n@{channel}"
    bot_logger.log_user_event(message.from_user.id, 'search channel', data={'Bot send channel to': message.from_user.id})
    await message.answer(text)


# Invalid content type reaction handler
@decline_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    bot_logger.log_user_event(message.from_user.id, 'wrong media type')
    await message.answer(ANSWER_TO_MEDIA)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(ANSWER_TO_WRONG_TEXT)
    bot_logger.log_user_event(message.from_user.id, f'User entry: {str(message.text)}')
    await message.delete()
