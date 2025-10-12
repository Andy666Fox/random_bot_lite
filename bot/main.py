import asyncio
from aiogram import Bot, Dispatcher
import os

from handlers.handlers import decline_router, get_channel_router
from database.schemas import create_tables
from dotenv import load_dotenv
from log_manager import bot_logger

# Load environment variables from .env file
load_dotenv()


async def main():
    """Main entry point. Initiate logging, api-keys, routers, history control, polling"""
    # Setup standard logging for console output
    # INFO level allows seeing main bot operation events
    #logging.basicConfig(level=logging.INFO)

    # Create database tables (if they don't exist yet)
    await create_tables()

    # bot instance
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    # main router (dispatcher) instance
    dp = Dispatcher()

    # Connect second-level routers for handling different event types:
    # - get_channel_router: handles channel information requests
    # - decline_router: handles rejections or declines
    dp.include_routers(get_channel_router, decline_router)

    # ignore previos messages from users
    await bot.delete_webhook(drop_pending_updates=True)
    # initiate bot polling process
    bot_logger.log_system_event('Bot initialized')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
