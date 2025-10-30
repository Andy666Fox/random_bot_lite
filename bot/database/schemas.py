import os

from utils.log_manager import log_manager
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channelnick = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Integer, default=1)
    avg_score = Column(Float, default=5.0)
    summary = Column(String(250), default=None)

    ratings = relationship("Rating", back_populates="channel", cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"))
    likes = Column(Integer, default=5)
    dislikes = Column(Integer, default=5)

    channel = relationship("Channel", back_populates="ratings")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    nickname = Column(String(50), default=None)
    last_online = Column(DateTime)
    last_channel_id = Column(Integer, ForeignKey("channels.id"), default=1)

    last_channel = relationship("Channel", foreign_keys=[last_channel_id])


engine = create_async_engine(
    os.getenv("DB_URL"), echo=False, future=True, pool_pre_ping=True, pool_size=10, max_overflow=20
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        log_manager.log_system_event("DB tables created")
