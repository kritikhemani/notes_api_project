from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import UserCreate, UserRead, Token
from app.models import User
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.security import hash_password, create_access_token, create_refresh_token, decode_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))

