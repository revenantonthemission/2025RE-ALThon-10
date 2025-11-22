"""
Repository layer for database operations.
Separates data access logic from route handlers.
"""
from typing import List
from sqlalchemy.orm import Session
from backend.models.course import Course as CourseModel
from backend.schemas.course import CourseSummary


class CourseRepository:
    """Repository for Course-related database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Model -> DTO
    def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[CourseSummary]:
        """
        Get all courses with pagination (id and name only).
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of CourseSummary DTOs (id and course_name only)
        """
        courses = self.db.query(CourseModel.id, CourseModel.course_name).offset(skip).limit(limit).all()
        return [CourseSummary(id=c.id, course_name=c.course_name) for c in courses]
