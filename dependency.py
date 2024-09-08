from database import async_session_maker


# Dependency
async def get_db():
    async with async_session_maker() as session:
        yield session