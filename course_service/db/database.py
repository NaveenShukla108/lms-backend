from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = f"postgresql://postgres:Ankit%408296@localhost:5432/course_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base =  declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db  # gives the session to the route
    finally:
        db.close() 