from sqlalchemy.sql.expression import func
from sqlalchemy import select
from models import Channel
from database import get_session


async def get_random_channel():
    async with get_session()  as session:
        stmt = select(Channel).order_by(func.random()).limit(1)
        result = await session.execute(stmt)
        channel = result.scalar_one_or_none()

        if channel:
            return channel.channelnick
        return None

