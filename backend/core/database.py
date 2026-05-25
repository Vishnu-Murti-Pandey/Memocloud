from sqlmodel import SQLModel, Session, create_engine
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_tables():
    SQLModel.metadata.create_all(engine)