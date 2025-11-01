from dispatcher import dp

from . import admin_handlers, user_commands, user_handlers

dp.include_router(admin_handlers.admin_router)
dp.include_router(user_commands.user_commands_router)
dp.include_router(user_handlers.user_router)
