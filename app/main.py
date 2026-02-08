from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router
from app.notes import router as notes_router
import uvicorn
from app.middleware import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(title="Notes API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def home():
    return {"message": "Welcome to the Notes API!"}

app.include_router(auth_router)
app.include_router(notes_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

