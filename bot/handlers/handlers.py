from aiogram import types, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import CallbackQuery
from aiogram import F

from keyboards.keyboards import get_main_keyboard, get_channel_rating_inline_keyboard
from service.default_answers import *
from middlewares.middlewares import CooldownMW
from database.methods import *
from service.log_manager import bot_logger
from service.channel_validation import validate_channel
from service.admin_validation import is_admin

import random

# bot have two types of routers
# DECLINE routers react for invalid messages (message types)
# BASIC work router. Control message sending from bot

decline_router = Router()
basic_router = Router()
decline_router.message.middleware(CooldownMW())
basic_router.message.middleware(CooldownMW())

@basic_router.callback_query(F.data.startswith('rate:'))
async def handle_rating_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        _, action, channelnick = callback.data.split(':', 2)
        print()
        score = 1 if action == 'like' else -1
        success = await update_channel_rating(channelnick, score)
        if success:
            await callback.answer(RATING_CALLBACK_SUCCESS)
            bot_logger.log_user_event(callback.from_user.id, 'channel_rating', data={f'User {callback.from_user.username} rated': channelnick})
        else:
            await callback.answer(RATING_CALLBACK_FAIL)
            bot_logger.log_user_event(callback.from_user.id, 'channel_rating_fail', data={f'User {callback.from_user.username} rate failed': channelnick})
    except Exception as e:
        bot_logger.log_error(e, context={'handle_rating_callback_func_error': e})

# Initial button handler
@basic_router.message(Command("start"))
async def send_welcome(message: types.Message):
    uid = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else ''
    last_name = ' ' + message.from_user.last_name if message.from_user.last_name else ''
    nickname = first_name + ' ' + last_name
    status = await insert_user(uid, nickname)
    if status:
        msg = NEW_USER_HELLO.format(nickname) + START_INFO
    else:
        msg = OLD_USER_HELLO.format(nickname) + START_INFO
    bot_logger.log_user_event(uid, 'start', data={'Bot started by user': nickname})
    await message.answer(msg, reply_markup=get_main_keyboard())

@basic_router.message(Command("extra"))
async def send_extra_commands(message: types.Message):
    bot_logger.log_user_event(message.from_user.id, 'extra', data={'Looked for extra commands': message.from_user.id})
    await message.answer(EXTRA_COMMANDS_DESCRIPTION)


@basic_router.message(Command("suggest")) 
async def suggest_channel(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer(EMPTY_SUGGEST_ARGS)
        return
    
    channelnick = command.args.strip()
    if 't.me' in channelnick:
        channelnick = channelnick.split('/')[-1]
    elif channelnick.startswith('@'):
        channelnick = channelnick[1:]
 
    if await validate_channel(channelnick):
        status = await insert_suggested_channel(channelnick)
        match status[1]:
            case 'created':
                await message.answer(SUGGEST_SUCCESS)
            case 'exists':
                await message.answer(SUGGEST_EXISTS)
            case 'error':
                await message.answer(SUGGEST_FAIL)
    else:
        status = 'failed'
        await message.answer(SUGGEST_FAIL)

    bot_logger.log_user_event(message.from_user.id, 'suggest', data={'User suggested channel': channelnick, 'insert_status': status})

@basic_router.message(Command("stats"))
async def show_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(ADMIN_VALIDATION_FAILED_MESSAGE)
        bot_logger.log_user_event(message.from_user.id, 'db stats requested', data={'is_admin': False})
        return
    else:
        stats = await get_db_stats()
        msg = ADMIN_STATS_GATHER_TEMPLATE.format(stats[0], stats[1], stats[2], stats[3])
        await message.answer(msg)
    
    bot_logger.log_user_event(message.from_user.id, 'db stats requested', data={'is_admin': True})
        
@basic_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    channel = await get_random_channel()
    text = f"{random.choice(ANSWERS)}\n@{channel}"
    bot_logger.log_user_event(message.from_user.id, 'search channel', data={'Bot response': channel})

    await message.answer(
        text,
        reply_markup=get_channel_rating_inline_keyboard(channel)
    )

# Invalid content type reaction handler
@decline_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    bot_logger.log_user_event(message.from_user.id, 'wrong media type')
    await message.answer(ANSWER_TO_MEDIA)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(ANSWER_TO_WRONG_TEXT)
    bot_logger.log_user_event(message.from_user.id, f'User entry: {str(message.text)}')
    await message.delete()
