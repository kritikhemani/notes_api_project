from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import UserCreate, UserRead
from app.models import User
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(name=payload.name, email=payload.email, hashed_password=payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user