import asyncio
import os

from aiogram import Bot, Dispatcher
from database.schemas import create_tables
from dotenv import load_dotenv
from handlers.handlers import basic_router, decline_router
from service.log_manager import bot_logger

# Load environment variables from .env file
load_dotenv()


async def main():
    """Main entry point. Initiate logging, api-keys, routers, history control, polling"""

    await create_tables()

    # bot instance
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    # main router (dispatcher) instance
    dp = Dispatcher()

    dp.include_routers(basic_router, decline_router)

    # ignore previos messages from users
    await bot.delete_webhook(drop_pending_updates=True)
    # initiate bot polling process
    bot_logger.log_system_event("Bot initialized")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
