from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram import F

from keyboards import get_main_keyboard
from defaults import (
    START_MESSAGE,
    ANSWERS,
    BLOCKED_CONTENT_TYPES,
    MESSAGE_ANSWER,
    DEFAULT_RESPONSE,
)
from middlewares import BasicMW, CooldownMW
from crud import get_random_channel

import random

# bot have two types of routers
# DECLINE routers react for invalid messages (message types)
# GET_Channel normal work router. Control message sending from bot

decline_router = Router()
get_channel_router = Router()
decline_router.message.middleware(BasicMW())
get_channel_router.message.middleware(CooldownMW())


# Initial button handler
@get_channel_router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=get_main_keyboard())


# Main button handler
@get_channel_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    channel = await get_random_channel()
    text = f"{random.choice(ANSWERS)}\n@{channel}"  # get_random_channel()
    await message.answer(text)


# Invalid content type reaction handler
@decline_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    await message.answer(MESSAGE_ANSWER)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(DEFAULT_RESPONSE)
    await message.delete()
