from fastapi import FastAPI
from routers import course

app = FastAPI()

app.include_router(course.router, prefix="/api/courses")
