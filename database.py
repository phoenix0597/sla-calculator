from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

engine = create_async_engine(settings.DB_URL, echo=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
