from sqlalchemy.sql.expression import func
from sqlalchemy import select
from schemas import Channel
from session_gen import get_session
from log_manager import bot_logger
import random


async def get_random_channel():
    try:
        async with get_session() as session:
            count_stmt = select(func.count(Channel.id)).where(
                Channel.channel_status == 1
            )
            count_result = await session.execute(count_stmt)
            total_count = count_result.scalar()

            if total_count == 0:
                return None

            random_offset = random.randint(0, total_count - 1)

            stmt = (
                select(Channel.channelnick)
                .where(Channel.channel_status == 1)
                .offset(random_offset)
                .limit(1)
            )
            result = await session.execute(stmt)
            channel_nick = result.scalar_one_or_none()
            return channel_nick

    except Exception as e:
        print(f"Processing failed: {e}")
        bot_logger.log_error(e, context={'get_random_channel_func_error': None})
        return None
