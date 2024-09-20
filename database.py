from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./lms.db"

engine = create_engine(DATABASE_URL)

# Create a sessionmaker to create sessions for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for your SQLAlchemy models
Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# db_dependency = Annotated[Session, Depends(get_db)]