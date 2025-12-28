from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import User
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    pass
    