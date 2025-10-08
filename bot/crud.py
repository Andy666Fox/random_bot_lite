from sqlalchemy.sql.expression import func
from sqlalchemy import select
from schemas import Channel
from session_gen import get_session
from monitoring.metrics_server import metrics
import random


async def get_random_channel():
    """
    Retrieve a random active channel nickname from the database.

    This function uses a two-step approach:
    1. Count total active channels (channel_status = 1)
    2. Use random offset to select one channel

    Returns:
        Optional[str]: Channel nickname if found, None if no active channels exist

    Raises:
        Exception: Database connection or query errors are caught and logged
    """
    try:
        async with get_session() as session:
            count_stmt = select(func.count(Channel.id)).where(
                Channel.channel_status == 1
            )
            metrics.record_db_query()
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
        return None
