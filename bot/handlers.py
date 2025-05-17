from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram import F

from keyboards import get_main_keyboard
from defaults import *
from services import rw
from middlewares import BasicMW

import random

router = Router()
router.message.middleware(BasicMW())

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    await message.answer(f'{random.choice(ANSWERS)}\n@{rw.get_random_word()}'
            #reply_markup=types.ReplyKeyboardRemove()
        )
F  
@router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    await message.answer(MESSAGE_ANSWER)
    
@router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(DEFAULT_RESPONSE)
    await message.delete()