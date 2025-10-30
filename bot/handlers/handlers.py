from aiogram import F, Router, types
from aiogram.filters.command import Command, CommandObject
from database.methods import (
    get_db_stats,
    insert_suggested_channel,
    insert_user,
    update_channel_rating
)
from keyboards.builder import get_channel_rating_inline_keyboard, get_main_keyboard
from middlewares.middlewares import CooldownMW
from utils.cache_manager import cache_manager
from utils.globals import BLOCKED_CONTENT_TYPES
from utils.log_manager import log_manager
from utils.message_manager import message_manager
from utils.validation_manager import validation_manager

decline_router = Router()
basic_router = Router()
decline_router.message.middleware(CooldownMW())
basic_router.message.middleware(CooldownMW())


@basic_router.callback_query(F.data.startswith("rate:"))
async def handle_rating_callback(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        _, action, channelnick = callback.data.split(":", 2)
        print()
        score = 1 if action == "like" else -1
        success = await update_channel_rating(channelnick, score)
        if success:
            await callback.answer(message_manager.RATING_CALLBACK_SUCCESS)
            log_manager.log_user_event(
                callback.from_user.id,
                "channel_rating",
                data={f"User {callback.from_user.username} rated": channelnick},
            )
        else:
            await callback.answer(message_manager.RATING_CALLBACK_FAIL)
            log_manager.log_user_event(
                callback.from_user.id,
                "channel_rating_fail",
                data={f"User {callback.from_user.username} rate failed": channelnick},
            )
    except Exception as e:
        log_manager.log_error(e, context={"handle_rating_callback_func_error": e})

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

@basic_router.message(Command("stats"))
async def show_stats(message: types.Message):
    uid = message.from_user.id
    print(uid)
    if not await validation_manager.is_admin(uid):
        await message.answer(message_manager.ADMIN_VALIDATION_FAILED_MESSAGE)
        log_manager.log_user_event(
            uid, "db stats requested", data={"is_admin": False}
        )
        return
    else:
        stats = await get_db_stats()
        msg = message_manager.ADMIN_STATS_GATHER_TEMPLATE.format(stats[0], stats[1], stats[2], stats[3])
        await message.answer(msg)

    log_manager.log_user_event(message.from_user.id, "db stats requested", data={"is_admin": True})


@basic_router.message(F.text == "Найти канал")
async def handle_start_button(message: types.Message):
    user_id = message.from_user.id
    channel, summary = await cache_manager.get_channel_with_summary_from_cache(user_id)
    text = f"@{channel}\n{summary}"

    log_manager.log_user_event(
        user_id, "search channel", data={f"Bot response to {message.from_user.username}": channel}
    )

    await message.answer(text, reply_markup=get_channel_rating_inline_keyboard(channel))

@decline_router.message(F.content_type.in_(BLOCKED_CONTENT_TYPES))
async def handle_blocked_content(message: types.Message):
    await message.delete()
    log_manager.log_user_event(message.from_user.id, "wrong media type")
    await message.answer(message_manager.ANSWER_TO_MEDIA)


# Invalid text command handler
@decline_router.message(F.text)
async def default_response(message: types.Message):
    await message.answer(message_manager.ANSWER_TO_WRONG_TEXT)
    log_manager.log_user_event(message.from_user.id, f"User entry: {str(message.text)}")
    await message.delete()
