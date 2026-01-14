import asyncio
import os

from aiogram import Bot
from database.schemas import create_tables
import handlers # do not delete this import. Loads routers
from dispatcher import dp
from dotenv import load_dotenv
from utils.log_manager import log_manager

load_dotenv()

async def main():
    """Main entry point. Initiate logging, api-keys, routers, history control, polling"""

    await create_tables()

    bot = Bot(
        token=os.getenv("BOT_TOKEN")
    )  # , default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)

    await bot.delete_webhook(drop_pending_updates=True)
    log_manager.log_system_event("Bot initialized")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_manager.log_system_event("Bot stopping")
