from aiogram import Router
from middlewares.middlewares import CooldownMW

# bot have two types of routers
# DECLINE routers react for invalid messages (message types)
# BASIC work router. Control message sending from bot

decline_router = Router()
basic_router = Router()
decline_router.message.middleware(CooldownMW())
basic_router.message.middleware(CooldownMW())
