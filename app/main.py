# main.py
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.database import async_session_maker, init_db
from app.routers import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
