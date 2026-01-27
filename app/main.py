from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router
from app.notes import router as notes_router
import uvicorn

app = FastAPI(title="Notes API")


@app.get("/")
async def home():
    return {"message": "Welcome to the Notes API!"}

app.include_router(auth_router)
app.include_router(notes_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

