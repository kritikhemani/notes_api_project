from app.schema import NoteCreate
from fastapi import Depends, APIRouter
from app.models import Note
from app.database import get_db
from sqlalchemy import select

router = APIRouter(prefix="/notes", tags=["notes"])