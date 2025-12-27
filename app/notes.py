from sqlalchemy.ext.asyncio import AsyncSession
from schema import NoteCreate
from fastapi import Depends, APIRouter
from models import Note
from db import get_db
from sqlalchemy import select

router = APIRouter(prefix="/notes", tags=["notes"])