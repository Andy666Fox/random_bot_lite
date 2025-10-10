from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from log_manager import bot_logger
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelnick = Column(String(100), unique=True, nullable=False)
    channel_status = Column(Integer, nullable=False)


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tg_id = Column(String(100), unique=True, nullable=False)
#     username = Column(String(100), unique=True, nullable=False)


engine = create_async_engine(os.getenv("BOT_DB_URL"), echo=False, future=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        bot_logger.log_system_event('DB tables created')