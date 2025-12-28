from app.schema import NoteCreate
from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models import Note
from app.database import get_db
from sqlalchemy import select

router = APIRouter(prefix="/notes", tags=["notes"])