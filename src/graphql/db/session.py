from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from src.apis.v1.core.project_settings import Settings
settings = Settings()
SQL_ALCHEMY_POSTGRES_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
engine = create_async_engine(
    SQL_ALCHEMY_POSTGRES_URL,
    future=True
)
async_session = async_scoped_session(
    sessionmaker(
        engine,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)

async def get_session_without_context_manager() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()

@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()