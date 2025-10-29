import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from database.schemas import create_tables
from dotenv import load_dotenv
from handlers.handlers import basic_router, decline_router
from utils.log_manager import bot_logger

load_dotenv()


async def main():
    """Main entry point. Initiate logging, api-keys, routers, history control, polling"""

    await create_tables()

    bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()

    dp.include_routers(basic_router, decline_router)

    await bot.delete_webhook(drop_pending_updates=True)
    bot_logger.log_system_event("Bot initialized")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_logger.log_system_event("Bot stopping")
