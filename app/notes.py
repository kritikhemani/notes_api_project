from app.schema import NoteCreate, NoteRead, NoteUpdate
from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models import Note
from app.database import get_db
from sqlalchemy import select
from app.deps import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/create/")
def create_note(payload: NoteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_note = Note(title=payload.title, content=payload.content, owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/read/")
def read_notes(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    notes = db.query(Note).filter(Note.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notes

@router.put("/update/{note_id}/")
def update_notes(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    pass