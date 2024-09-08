# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings
from models import Base

engine = create_async_engine(settings.DB_URL, echo=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
