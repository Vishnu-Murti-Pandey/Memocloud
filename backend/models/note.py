from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional

def _uuid() -> str:
    return str(uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)

class Note(SQLModel, table=True):
    __tablename__ = "note"
    
    id: UUID = Field(default_factory=_uuid, primary_key=True)
    title: Optional[str] = Field(default="")
    content: Optional[str] = Field(default="")
    created_at: datetime = Field(default_factory=_now, nullable=False)
    updated_at: datetime = Field(default_factory=_now, nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)