from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateNoteRequest(BaseModel):
    title: str
    content: str
    
class UpdateNoteRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    
class CreateNoteResponse(BaseModel):
    note_id: str
    message: str
    
class GetNoteByIdResponse(BaseModel):
    user_id: str
    note_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
class GetAllNotesResponse(BaseModel):
    user_id: str
    note_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class UpdateNoteResponse(BaseModel):
    note_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    updated_at: datetime
    message: str

class DeleteNoteResponse(BaseModel):
    message: str