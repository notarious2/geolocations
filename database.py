from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = (
    f"postgresql+asyncpg://postgres:postgres@geolocations-postgres:5432/postgres"
)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
