from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.database import get_db
from backend.repositories.repository import CourseRepository
from backend.schemas.course import CourseSummary, CourseResponse, CourseListResponse
from backend.core.schema import UserProfile, CourseInfo, AnalysisRequest, GeminiResponse

router = APIRouter()

@router.get("/courses", response_model=CourseListResponse)
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all courses with pagination.
    Uses CourseRepository for data access.
    """
    repo = CourseRepository(db)
    models = repo.get_all_courses(skip=skip, limit=limit)

    summaries = [CourseSummary.from_model(m) for m in models]
    return CourseListResponse(courses=summaries)


@router.get("/courses/{course_id}", response_model=CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    """
    Get a single course by ID.
    Uses CourseRepository for data access.
    """
    repo = CourseRepository(db)
    course = repo.get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

from backend.core.inference import return_total_result
