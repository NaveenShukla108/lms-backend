from fastapi import FastAPI
from routers import course
from db.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(course.router, prefix="/api")
