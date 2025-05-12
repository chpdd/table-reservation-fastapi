from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from typing import Annotated

from src.config import settings

engine = create_async_engine(settings.db_url, echo=True)

session_factory = async_sessionmaker(engine)


async def get_db():
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    def __repr__(self):
        return f"{self.__name__}({self.__dict__})"


db_dep = Annotated[AsyncSession, Depends(get_db)]
