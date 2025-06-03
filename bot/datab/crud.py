from aiogram import types
from sqlalchemy.sql.expression import func
from datab.models import Channel, Session


async def get_random_channel():
    """main handler
    """
    with Session() as session:
        return (
            session.query(Channel).order_by(func.random()).limit(1).scalar().channelnick
        )


async def add_channel(message: types.Message):
    channel_nick = message.text.split()[-1]
    with Session() as session:
        exists = session.query(Channel).filter_by(channelnick=channel_nick).first()
        if not exists:
            new_channel = Channel(channelnick=channel_nick, score=0)
            session.add(new_channel)
            session.commit()
            ## todo: log the db interactions
            return True
        return False


async def increment_score(channel_nick: str):
    with Session() as session:
        channel = session.query(Channel).filter_by(channelnick=channel_nick).first()
        if channel:
            channel.score += 1
            session.commit()
            return True
        return False
