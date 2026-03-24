from datetime import datetime, timedelta
from jose import jwt 
from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_EXPIRES_DAYS = 7

def hash_password(password: str) -> str:
    raise Exception("New hash function running")
    #Convert to fixed length (always < 72 bytes)
    #print("New hash function running")
    #safe_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    #return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    safe_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(safe_password, hashed)

def create_token(user_id: int, token_type: str, expires: timedelta) -> str:
    now = datetime.utcnow()
    payload = {"sub": str(user_id), "type": token_type, "exp": now + expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int) -> str:
    return create_token(user_id, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: int) -> str:
    return create_token(user_id, "refresh", timedelta(days=REFRESH_EXPIRES_DAYS))

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])