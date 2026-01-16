from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    

class NoteCreate(BaseModel):
    title: str
    content: str
    
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    
