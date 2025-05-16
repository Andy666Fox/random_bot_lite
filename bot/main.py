import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties

from config_reader import config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Hello')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
