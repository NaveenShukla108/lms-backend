from sqlalchemy.orm import Session
from models.course import Course
from schemas.course import CourseCreate, CourseUpdate
from uuid import UUID


def get_course(db: Session, course_id: UUID):
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(db: Session):
    return db.query(Course).all()

def create_course(db: Session, course: CourseCreate, trainer_id: UUID):
    new_course_data = course.model_dump()
    new_course_data["trainer_id"] = trainer_id
    new_course = Course(**new_course_data)  # Create actual model instance
    db.add(new_course)
    db.commit()
    db.refresh(new_course)  # Refresh the model instance
    return new_course

def update_course(db: Session, course_id: UUID, course: CourseUpdate):

    course_by_id = db.query(Course).filter(Course.id == course_id).first()
    if course_by_id:
        for field, value in course.model_dump_json().items():
            setattr(course_by_id, field, value)
        
        db.commit()
        db.refresh(course_by_id)
        return course_by_id 
    return None

def delete_course(db: Session, course_id: UUID):
    existing = get_course(db, course_id)
    if existing:
        db.delete(existing)
        db.commit()
        return existing
    return None