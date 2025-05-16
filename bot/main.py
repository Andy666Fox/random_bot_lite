import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command

from random_word import RandomWords
import random

from keyboards import get_main_keyboard
from config_reader import config
from defaults import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
router = Router()
rw = RandomWords()
dp.include_router(router)

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=get_main_keyboard()
    )

@router.message(lambda message: message.text == "Найти канал")
async def handle_start_button(message: types.Message):
    print(message.chat.id, message.message_id)
    await message.answer(f'{random.choice(ANSWERS)}\n@{rw.get_random_word()}'
            #reply_markup=types.ReplyKeyboardRemove()
        )
    
@router.message(lambda message: message.content_type in BLOCKED_CONTENT_TYPES)
async def handle_blocked_content(message: types.Message):
    await message.delete()
    await message.answer(MESSAGE_ANSWER)
    
@router.message()
async def default_response(message: types.Message):
    await message.answer(DEFAULT_RESPONSE)
    await message.delete()



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
