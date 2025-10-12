from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from log_manager import bot_logger
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    channelnick = Column(String, unique=True, nullable=False, index=True)
    status = Column(Integer, default=1)
    avg_score = Column(Float, default=5.0)

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    channel_nickname = Column(String, ForeignKey("channels.channelnick"))
    stars_counts = Column(String, default='{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    last_online = Column(DateTime)
    last_channel = Column(String)

engine = create_async_engine(os.getenv("BOT_DB_URL"), echo=False, future=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        bot_logger.log_system_event('DB tables created')