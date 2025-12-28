from datetime import datetime, timedelta
from jose import jwt 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_EXPIRES_DAYS = 7

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(user_id: int, token_type: str, expires: timedelta) -> str:
    now = datetime.utcnow()
    payload = {"sub": str(user_id), "type": token_type, "exp": now + expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)