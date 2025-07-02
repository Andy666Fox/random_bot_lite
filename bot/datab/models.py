from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Base = declarative_base()


class Channel(Base):
    # Basic db schema, conatain info about, id, channel nickname and channel score (in development)
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelnick = Column(String(100), unique=True, nullable=False)
    score = Column(Integer, default=0)


# TODO replace sqlite to Postgres
engine = create_engine("sqlite:///bot/datab/db/channels.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
