from aiogram import Router, types
from aiogram.filters.command import Command
from database.methods import get_db_stats
from middlewares.middlewares import CooldownMW
from utils.log_manager import log_manager
from utils.message_manager import message_manager
from utils.validation_manager import validation_manager

admin_router = Router()
admin_router.message.middleware(CooldownMW())


@admin_router.message(Command("stats"))
async def show_stats(message: types.Message):
    uid = message.from_user.id
    print(uid)
    if not await validation_manager.is_admin(uid):
        await message.answer(message_manager.ADMIN_VALIDATION_FAILED_MESSAGE)
        log_manager.log_user_event(uid, "db stats requested", data={"is_admin": False})
        return
    else:
        stats = await get_db_stats()
        msg = message_manager.ADMIN_STATS_GATHER_TEMPLATE.format(
            stats[0], stats[1], stats[2], stats[3]
        )
        await message.answer(msg)

    log_manager.log_user_event(message.from_user.id, "db stats requested", data={"is_admin": True})
