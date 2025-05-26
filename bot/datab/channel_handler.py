import json
import random
from aiogram import types 
from models import Channel, Session
from sqlalchemy.sql.expression import func


async def get_efficient_random(session):
    return session.query(Channel).order_by(func.random()).limit(1).sclar()


async def get_db_random_channel():
    with Session() as session:
        random_channel = Channel.get_random(session)

        if random_channel:
            return random_channel.channelnick
        else:
            return 'not found'
        
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
    
async def get_top_channels(limit=10):
    with Session() as session:
        channels = session.query(Channel).order_by(Channel.score.desc()).limit(limit).all()
        return [(ch.channelnick, ch.score) for ch in channels]



# Deprecated
def get_random_channel():
    with open("bot\\datab\\val_channels.json", "r") as file:
        data = json.load(file)

    return random.choice(list(data.keys()))
