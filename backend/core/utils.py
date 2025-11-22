"""
Utility functions for converting SQLAlchemy models to Pydantic schemas.
Uses Pydantic's from_attributes feature for seamless conversion.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.user import User as UserModel
from backend.models.course import Course as CourseModel
from backend.core.schema import UserProfile, CourseHistory, CourseInfo


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


def return_user_courses(user_ids: List[int]) -> List[str]:
    """
    Get all courses taken by a list of users.
    
    Args:
        user_ids: List of user IDs (integers, e.g. [1, 2, 3])
        
    Returns:
        List of course_codes taken by these users (flattened list, duplicates preserved)
    """
    from backend.db.database import SessionLocal
    db = SessionLocal()
    try:
        # Query users by integer ID
        users = db.query(UserModel).filter(UserModel.id.in_(user_ids)).all()
    
        all_courses = []
        for user in users:
            for course in user.courses:
                all_courses.append(course.course_code)
            
        return all_courses
    finally:
        db.close()


def return_course_info(courses: List[int]) -> List[CourseInfo]:
    """
    Get detailed information for a list of course IDs.
    
    Args:
        courses: List of course IDs (integers, e.g. [1, 2, 3])
        
    Returns:
        List of CourseInfo objects
    """
    from backend.db.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Query courses by integer ID
        course_models = db.query(CourseModel).filter(CourseModel.id.in_(courses)).all()
        
        # course_models을 CourseInfo로 변환
        course_infos = []
        for course in course_models:
            info = CourseInfo(
                id=course.id,
                year=course.year or "",
                semester=course.semester or "",
                department=course.department,
                major=course.major,
                course_code=course.course_code,
                division=course.division,
                course_name=course.course_name,
                credits=course.credits,
                class_time_room=course.class_time_room,
                hours=course.hours,
                professor=course.professor,
                capacity=course.capacity,
                english_lecture=course.english_lecture,
                chinese_lecture=course.chinese_lecture,
                approved_course=course.approved_course,
                cu_course=course.cu_course,
                odd_even=course.odd_even,
                international_student=course.international_student,
                honors_course=course.honors_course,
                engineering_certification=course.engineering_certification,
                exam_date=course.exam_date,
                target_students=course.target_students,
                recommended_year=course.recommended_year,
                remarks=course.remarks,
                description=course.description,
                note=course.note
            )
            course_infos.append(info)
            
        return course_infos
    finally:
        db.close()
