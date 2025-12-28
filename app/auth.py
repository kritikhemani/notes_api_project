from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import UserCreate, UserRead
from app.models import User
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth", tags=["auth"])

