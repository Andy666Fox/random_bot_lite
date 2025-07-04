from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()
db_url = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgres_tgrb:5432/{os.getenv("POSTGRES_DB")}'

class Channel(Base):
    # Basic db schema, conatain info about, id, channel nickname and channel score (in development)
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelnick = Column(String(100), unique=True, nullable=False)
    channel_status = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)

engine = create_async_engine(db_url,
                            echo=True, future=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
