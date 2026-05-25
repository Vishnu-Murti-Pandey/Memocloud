from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

def _uuid() -> str:
    return str(uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: UUID = Field(default_factory=_uuid, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=_now, nullable=False)