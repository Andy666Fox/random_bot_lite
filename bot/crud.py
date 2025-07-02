from sqlalchemy.sql.expression import func
from models import Channel
from database import get_session


async def get_random_channel():
    async with get_session()  as session:
        return (
            session.query(Channel).order_by(func.random()).limit(1).scalar().channelnick
        )

