from fastapi import FastAPI

app = FastAPI(title="Notes API")


@app.get("/")
def home():
    return {"message": "Welcome to the Notes API!"}