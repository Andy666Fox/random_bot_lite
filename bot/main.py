import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command

from random_word import RandomWords
import random

from keyboards import get_main_keyboard
from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
router = Router()
rw = RandomWords()
dp.include_router(router)

answers = ['Вот например:', 'А как тебе этот:', 'Что насчет этого:', 'Ну вот собсна:']

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Добро пожаловать! Что умеет этот бот?\n" \
        "Подкидывать вам случайные каналы со всего Telegram! (если найдет конечно)" \
        "Попробуйте!",
        reply_markup=get_main_keyboard()
    )

@router.message(lambda message: message.text == "Найти канал")
async def handle_start_button(message: types.Message):
    print(message.chat.id, message.message_id)
    await message.answer(f'{random.choice(answers)}\n@{rw.get_random_word()}'
            #reply_markup=types.ReplyKeyboardRemove()
        )



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
