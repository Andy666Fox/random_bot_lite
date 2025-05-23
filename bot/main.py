import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import decline_router, get_channel_router

async def main():
    """Main entry point. Initiate logging, api-keys, routers, history control, polling
    """
    # Standart cmd logging in worktime
    logging.basicConfig(level=logging.INFO)

    # bot instance
    bot = Bot(token=config.bot_token.get_secret_value())
    # main router (dispatcher) instance
    dp = Dispatcher()

    # second stage routers connecting
    dp.include_routers(get_channel_router, decline_router)

    # ignore previos messages from users
    await bot.delete_webhook(drop_pending_updates=True)
    # initiate bot polling process
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
