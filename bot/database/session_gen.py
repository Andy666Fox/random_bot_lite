"""
Database session management module.

Provides utilities for creating and managing async SQLAlchemy database sessions
with proper transaction handling and cleanup.
"""
from database.schemas import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


def async_session_generator():
    """
    Create and configure an async SQLAlchemy session factory.
    
    Returns:
        sessionmaker: Configured async session factory that creates AsyncSession instances
                     with automatic commit disabled (expire_on_commit=False) to allow
                     accessing model attributes after commit.
    
    Note:
        expire_on_commit=False prevents SQLAlchemy from expiring all instances
        after each commit, which is useful when you need to access model
        attributes outside of the session context.
    """
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    """
    Async context manager for database session handling with automatic transaction management.
    
    Provides a database session with automatic commit/rollback and cleanup.
    The session will automatically commit on successful completion or rollback on exceptions.
    
    Yields:
        AsyncSession: Active database session for executing queries
        
    Raises:
        Exception: Re-raises any exception that occurred during session operations
                  after performing rollback
    """
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
            await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
