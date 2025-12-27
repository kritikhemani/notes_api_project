from pydantic import BaseModel
from typing import Optional

    
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None