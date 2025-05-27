from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class CourseBase(BaseModel):

    title: str
    description: Optional[str] = None
    # trainer_id: UUID
    duration: Optional[str] = None
    is_paid: bool = False
    price: Optional[int] = None
    certificate_template: Optional[str] = None
    is_active: bool = True

class CourseCreate(CourseBase):
    pass 

class CourseUpdate(CourseBase):
    pass 

class CourseOut(CourseBase):
    id: UUID
    trainer_id: UUID
    created_at: datetime

    class config:
        orm_mode = True