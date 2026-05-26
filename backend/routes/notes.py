from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, desc
from schemas.note import CreateNoteRequest, CreateNoteResponse, GetAllNotesResponse, GetNoteByIdResponse, UpdateNoteRequest, UpdateNoteResponse, DeleteNoteResponse
from core.database import get_session
from models.note import Note
from models.user import User
from core.dependencies import get_current_user
from typing import List
from datetime import datetime, timezone
from core.redis import redis_client
import json

note_router = APIRouter(prefix='/api', tags=["Notes"])

@note_router.post('/notes', response_model=CreateNoteResponse)
def createNote(request: CreateNoteRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    title = request.title
    content = request.content
    
    note = Note(title=title, content=content, user_id=current_user.id)
    session.add(note)
    session.commit()
    session.refresh(note)
    
    redis_client.delete(f"all_notes:{current_user.id}")
    
    return CreateNoteResponse(note_id=str(note.id), message="New note created successfully.")
  
@note_router.get('/notes', response_model=List[GetAllNotesResponse])  
def getAllNotes(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    cache_key = f"all_notes:{user_id}"
    cached_notes = redis_client.get(cache_key)
    
    if cached_notes:
        print("CACHE HIT")
        return [
            GetAllNotesResponse(
                note_id=str(note['id']),
                user_id=str(note['user_id']),
                title=note['title'],
                content=note['content'],
                created_at=note['created_at'],
                updated_at=note['updated_at']
            ) 
            for note in json.loads(cached_notes)
        ]
    
    print("CACHE MISS → FETCHING FROM DB")
    all_notes = session.exec(select(Note).where(Note.user_id == user_id).order_by(desc(Note.updated_at))).all()
    
    notes_data = [note.model_dump(mode='json') for note in all_notes]
    redis_client.set(cache_key, json.dumps(notes_data), ex=120)
     
    return [
        GetAllNotesResponse(
            note_id=str(note.id),
            user_id=str(note.user_id),
            title=note.title,
            content=note.content,
            created_at=note.created_at,
            updated_at=note.updated_at
        )
        for note in all_notes
    ]
    
    
@note_router.get('/note', response_model=GetNoteByIdResponse)  
def getNoteByUserId(note_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    cache_key = f"note:{current_user.id}:{note_id}"
    cached_note = redis_client.get(cache_key)
    
    if cached_note:
        print("CACHE HIT")
        return json.loads(cached_note)
    
    print("CACHE MISS → FETCHING FROM DB")
    
    note = session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note_data = {
        "user_id": str(note.user_id),
        "note_id": str(note.id),
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat()
    }
    redis_client.set(cache_key, json.dumps(note_data), ex=60)
    
    return GetNoteByIdResponse(
        user_id=str(note.user_id), 
        note_id=str(note.id), 
        title=note.title, 
        content=note.content, 
        created_at=note.created_at,
        updated_at=note.updated_at
    )
   

@note_router.patch('/notes', response_model=UpdateNoteResponse)  
def updateNote(note_id: str, request: UpdateNoteRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    title = request.title
    content = request.content
    
    note = session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if title is not None:
        note.title = title
    if content is not None:
        note.content = content
    note.updated_at = datetime.now(timezone.utc)
    
    session.add(note)
    session.commit()
    session.refresh(note)
    
    redis_client.delete(f"note:{current_user.id}:{note_id}")
    redis_client.delete(f"all_notes:{current_user.id}")
    
    return UpdateNoteResponse(
        note_id=str(note.id),
        title=note.title,
        updated_at=note.updated_at,
        content=note.content,
        message="Note updated successfully."
    )
    
@note_router.delete('/notes', response_model=DeleteNoteResponse)
def deleteNote(note_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    note = session.get(Note, note_id)
    
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    
    session.delete(note)
    session.commit()
    
    redis_client.delete(f"note:{current_user.id}:{note_id}")
    redis_client.delete(f"all_notes:{current_user.id}")
    
    return DeleteNoteResponse(message="Note deleted successfully.")
    
    
    