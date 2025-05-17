import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import router
from defaults import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
