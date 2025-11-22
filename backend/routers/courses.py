from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.database import get_db
from backend.models.course import Course as CourseModel
from backend.schemas.course import Course as CourseSchema

router = APIRouter()

@router.get("/courses", response_model=List[CourseSchema])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(CourseModel).offset(skip).limit(limit).all()
    return courses

@router.get("/courses/{course_id}", response_model=CourseSchema)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
