from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router
from app.notes import router as notes_router
from app.middleware import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(title="Notes API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home():
    return {"message": "Welcome to the Notes API!"}

app.include_router(auth_router)
app.include_router(notes_router)


