import asyncio
from sqlalchemy import delete, select

from src.database import session_factory
from src.models import Tour, Place


async def delete_data():
    async with session_factory() as session:
        await session.execute(delete(Tour))
        await session.execute(delete(Place))


async def select_data():
    async with session_factory() as session:
        await session.execute(select(Tour))
        await session.execute(select(Place))


if __name__ == "__main__":
    asyncio.run(select_data())
