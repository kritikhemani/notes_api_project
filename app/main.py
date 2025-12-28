from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router
from app.notes import router as notes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")


@app.get("/")
def home():
    return {"message": "Welcome to the Notes API!"}

