import asyncio


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from sqlalchemy import text

from config import POSTGRES_URL
from database.models import Base

engine = create_async_engine(
    POSTGRES_URL, echo=True
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    


async def create_table():
    async with engine.begin () as conn:
        Base.metadata.bind=engine
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    
