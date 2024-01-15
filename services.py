from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from models import City


async def is_city_table_empty(db_session: AsyncSession):
    query = select(City.id.isnot(None))
    query = select(exists(query))
    result = await db_session.execute(query)
    table_exists = result.scalars().one()
    return not (table_exists)
