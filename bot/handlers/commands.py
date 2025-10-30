from routers import basic_router
from aiogram.filters.command import Command, CommandObject
from aiogram import types
from database.methods import (
    insert_suggested_channel,
    insert_user
)
from utils.message_manager import message_manager
from utils.log_manager import log_manager
from keyboards.builder import get_main_keyboard
from utils.validation_manager import validation_manager


@basic_router.message(Command("start"))
async def send_welcome(message: types.Message):
    uid = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = " " + message.from_user.last_name if message.from_user.last_name else ""
    nickname = first_name + last_name
    status = await insert_user(uid, nickname)
    if status:
        msg = message_manager.NEW_USER_HELLO.format(nickname) + message_manager.START_INFO
    else:
        msg = message_manager.OLD_USER_HELLO.format(nickname) + message_manager.START_INFO
    log_manager.log_user_event(uid, "start", data={"Bot started by user": nickname})
    await message.answer(msg, reply_markup=get_main_keyboard())


@basic_router.message(Command("extra"))
async def send_extra_commands(message: types.Message):
    log_manager.log_user_event(
        message.from_user.id,
        "extra",
        data={"Looked for extra commands": message.from_user.id},
    )
    await message.answer(message_manager.EXTRA_COMMANDS_DESCRIPTION)


@basic_router.message(Command("suggest"))
async def suggest_channel(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer(message_manager.EMPTY_SUGGEST_ARGS)
        return

    channelnick = command.args.strip()
    if "t.me" in channelnick:
        channelnick = channelnick.split("/")[-1]
    elif channelnick.startswith("@"):
        channelnick = channelnick[1:]

    if await validation_manager.validate_channel(channelnick):
        status = await insert_suggested_channel(channelnick)
        match status[1]:
            case "created":
                await message.answer(message_manager.SUGGEST_SUCCESS)
            case "exists":
                await message.answer(message_manager.SUGGEST_EXISTS)
            case "error":
                await message.answer(message_manager.SUGGEST_FAIL)
    else:
        status = "failed"
        await message.answer(message_manager.SUGGEST_FAIL)

    log_manager.log_user_event(
        message.from_user.id,
        "suggest",
        data={"User suggested channel": channelnick, "insert_status": status},
    )