from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from dependencies import get_current_user_id
from db.database import get_db
from schemas.course import CourseCreate, CourseUpdate, CourseOut
from crud.course import get_course, get_courses, create_course, update_course, delete_course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseOut])
def get_all_courses(db: Session = Depends(get_db)):
    return get_courses(db)

@router.get("/{course_id}", response_model=CourseOut)
def get_course_by_id(course_id: UUID, db: Session = Depends(get_db)):
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course Not found (GET)")
    return course

@router.post("/", response_model=CourseOut)
def post_course(
    course: CourseCreate, 
    db: Session = Depends(get_db), 
    user_id: UUID = Depends(get_current_user_id)
    ):
    return create_course(db=db, course=course, trainer_id=user_id)

@router.put("/{course_id}", response_model=CourseOut)
def put_course(course_id: UUID, course: CourseUpdate, db: Session = Depends(get_db)):
    course_by_id = update_course(db=db, course_id=course_id, course=course)
    if not course_by_id:
        raise HTTPException(status_code=404, detail="Course Not Found (PUT)")
    return course_by_id

@router.delete("/{course_id}", response_model=CourseOut)
def delete_course(course_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found (DELETE)")
    return deleted



