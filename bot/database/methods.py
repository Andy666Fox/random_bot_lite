from sqlalchemy.sql.expression import text
from sqlalchemy import select
from database.schemas import Channel
from database.session_gen import get_session
from log_manager import bot_logger
import random

async def get_random_channel():
    try:
        async with get_session() as session:
            max_rowid_result = await session.execute(text("SELECT MAX(ROWID) FROM channels"))
            max_rowid = max_rowid_result.scalar()

            if not max_rowid:
                return None

            while True:
                random_rowid = random.randint(1, max_rowid)
                stmt = select(Channel.channelnick).where(
                    Channel.id == random_rowid
                )
                result = await session.execute(stmt)
                channel = result.scalar_one_or_none()
                if channel:
                    return channel

    except Exception as e:
        print(f"Processing failed: {e}")
        bot_logger.log_error(e, context={'get_random_channel_func_error': e})
        return None


# async def get_random_channel():
#     try:
#         async with get_session() as session:
#             count_stmt = select(func.count(Channel.id)).where(
#                 Channel.status == 1
#             )
#             count_result = await session.execute(count_stmt)
#             total_count = count_result.scalar()

#             if total_count == 0:
#                 return None

#             random_offset = random.randint(0, total_count - 1)

#             stmt = (
#                 select(Channel.channelnick)
#                 .where(Channel.status == 1)
#                 .offset(random_offset)
#                 .limit(1)
#             )
#             result = await session.execute(stmt)
#             channel_nick = result.scalar_one_or_none()
#             return channel_nick

#     except Exception as e:
#         print(f"Processing failed: {e}")
#         bot_logger.log_error(e, context={'get_random_channel_func_error': None})
#         return None
