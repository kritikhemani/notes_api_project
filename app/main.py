from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.auth import router as auth_router
from app.notes import router as notes_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Notes API", lifespan=lifespan)


@app.get("/")
async def home():
    return {"message": "Welcome to the Notes API!"}

app.include_router(auth_router)
app.include_router(notes_router)

