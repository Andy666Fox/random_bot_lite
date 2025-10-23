import os

from service.log_manager import bot_logger
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True)
    channelnick = Column(String, unique=True, nullable=False, index=True)
    status = Column(Integer, default=1)
    avg_score = Column(Float, default=5.0)

    ratings = relationship("Rating", back_populates="channel", cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    likes = Column(Integer, default=5)
    dislikes = Column(Integer, default=5)

    channel = relationship("Channel", back_populates="ratings")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    nickname = Column(String, default=None)
    last_online = Column(DateTime)
    last_channel_id = Column(Integer, ForeignKey("channels.id"), default=1)

    last_channel = relationship("Channel", foreign_keys=[last_channel_id])


engine = create_async_engine(os.getenv("BOT_DB_URL"), echo=False, future=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        bot_logger.log_system_event("DB tables created")
