from pydantic import BaseModel, Field, EmailStr
from typing import Optional

    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    
    class Config:
        from_attributes = True

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
    
    class config:
        from_attributes = True