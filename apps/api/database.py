from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import config_settings

engine = create_engine(config_settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

async_engine = create_async_engine(config_settings.async_database_url, pool_pre_ping=True, pool_size=5, max_overflow=10)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    """
    Hands a database session.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session object.
    """
    async with AsyncSessionLocal() as session:
        yield session
