from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base
from .config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии базы данных"""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(f"❌ Ошибка сессии базы: {e}")
            raise

async def get_db():
    async with SessionLocal() as session:
        yield session 
