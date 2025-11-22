"""
Repository layer for database operations.
Separates data access logic from route handlers.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.course import Course as CourseModel
from backend.models.user import User as UserModel, UserCourse as UserCourseModel
from backend.schemas.course import CourseSummary
from backend.schemas.user import UserCreate, UserResponse, UserCourseCreate, UserCourseResponse


class CourseRepository:
    """Repository for Course-related database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Model -> DTO
    def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[CourseSummary]:
        """
        Get all courses with pagination (id, course_name, and course_code only).
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of CourseSummary DTOs (id, course_name, and course_code)
        """
        courses = self.db.query(CourseModel).offset(skip).limit(limit).all()
        return [CourseSummary.from_model(course) for course in courses]