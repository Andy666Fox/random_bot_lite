from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelnick = Column(String(100), unique=True, nullable=False)
    score = Column(Integer, default=0)

engine = create_engine('sqlite:///channels.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)