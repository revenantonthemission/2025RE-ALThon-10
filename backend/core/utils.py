"""
Utility functions for converting SQLAlchemy models to Pydantic schemas.
Uses Pydantic's from_attributes feature for seamless conversion.
"""
from typing import Optional, List
from backend.models.user import User as UserModel
from backend.core.schema import UserProfile, CourseHistory


def grade_point_to_letter(grade_point: float) -> str:
    """Convert numeric grade point to letter grade."""
    if grade_point >= 4.5:
        return "A+"
    elif grade_point >= 4.0:
        return "A"
    elif grade_point >= 3.5:
        return "B+"
    elif grade_point >= 3.0:
        return "B"
    elif grade_point >= 2.5:
        return "C+"
    elif grade_point >= 2.0:
        return "C"
    elif grade_point >= 1.5:
        return "D+"
    elif grade_point >= 1.0:
        return "D"
    else:
        return "F"


def user_to_profile(
    user: UserModel,
    eval_preference: int = 3,
    interests: Optional[List[str]] = None,
    team_preference: int = 3,
    attendence_type: Optional[List[str]] = None
) -> UserProfile:
    """
    Convert SQLAlchemy User model to UserProfile Pydantic schema.
    
    Uses Pydantic's from_attributes feature for automatic conversion.
    
    Args:
        user: SQLAlchemy User model instance
        eval_preference: Evaluation preference (1-5), defaults to 3
        interests: List of interest areas
        team_preference: Team project preference (1-5), defaults to 3
        attendence_type: Preferred attendance types
    
    Returns:
        UserProfile schema instance
    
    Example:
        user = db.query(UserModel).filter_by(student_id="20211234").first()
        profile = user_to_profile(
            user,
            eval_preference=4,
            interests=["AI", "Web Development"],
            team_preference=2,
            attendence_type=["Online", "Hybrid"]
        )
    """
    # Convert UserCourse models to CourseHistory schemas
    taken_courses = [
        CourseHistory(
            course_id=course.course_code,
            grade=grade_point_to_letter(course.grade_point)
        )
        for course in user.courses
    ]
    
    # Create UserProfile using Pydantic's model_validate
    return UserProfile(
        taken_courses=taken_courses,
        eval_preference=eval_preference,
        interests=interests or [],
        team_preference=team_preference,
        attendence_type=attendence_type or []
    )
