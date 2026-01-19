from aiogram import types
from aiogram.filters.command import Command, CommandObject
from database.methods import get_db_stats, insert_suggested_channel, insert_user
from keyboards.builder import get_main_keyboard
from utils.validation_manager import Validation
from utils.bot_answers import bot_answers
from utils.log_manager import bot_logger

from handlers import basic_router


@basic_router.message(Command("start"))
async def send_welcome(message: types.Message):
    uid = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = " " + message.from_user.last_name if message.from_user.last_name else ""
    nickname = first_name + " " + last_name
    status = await insert_user(uid, nickname)
    if status:
        msg = bot_answers.NEW_USER_HELLO.format(nickname) + bot_answers.START_INFO
    else:
        msg = bot_answers.OLD_USER_HELLO.format(nickname) + bot_answers.START_INFO
    bot_logger.log_user_event(uid, "start", data={"Bot started by user": nickname})
    await message.answer(msg, reply_markup=get_main_keyboard())


@basic_router.message(Command("extra"))
async def send_extra_commands(message: types.Message):
    bot_logger.log_user_event(
        message.from_user.id,
        "extra",
        data={"Looked for extra commands": message.from_user.id},
    )
    await message.answer(bot_answers.EXTRA_COMMANDS_DESCRIPTION)


@basic_router.message(Command("suggest"))
async def suggest_channel(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer(bot_answers.EMPTY_SUGGEST_ARGS)
        return

    channelnick = command.args.strip()
    if "t.me" in channelnick:
        channelnick = channelnick.split("/")[-1]
    elif channelnick.startswith("@"):
        channelnick = channelnick[1:]

    if await Validation.validate_channel(channelnick):
        status = await insert_suggested_channel(channelnick)
        match status[1]:
            case "created":
                await message.answer(bot_answers.SUGGEST_SUCCESS)
            case "exists":
                await message.answer(bot_answers.SUGGEST_EXISTS)
            case "error":
                await message.answer(bot_answers.SUGGEST_FAIL)
    else:
        status = "failed"
        await message.answer(bot_answers.SUGGEST_FAIL)

    bot_logger.log_user_event(
        message.from_user.id,
        "suggest",
        data={"User suggested channel": channelnick, "insert_status": status},
    )


@basic_router.message(Command("stats"))
async def show_stats(message: types.Message):
    if not Validation.is_admin(message.from_user.id):
        await message.answer(bot_answers.ADMIN_VALIDATION_FAILED_MESSAGE)
        bot_logger.log_user_event(
            message.from_user.id, "db stats requested", data={"is_admin": False}
        )
        return
    else:
        stats = await get_db_stats()
        msg = bot_answers.ADMIN_STATS_GATHER_TEMPLATE.format(stats[0], stats[1], stats[2], stats[3])
        await message.answer(msg)

    bot_logger.log_user_event(message.from_user.id, "db stats requested", data={"is_admin": True})
