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


def return_user_courses(user_ids: List[str], db: Session) -> List[str]:
    """
    Get all courses taken by a list of users.
    
    Args:
        user_ids: List of student_ids (e.g. ["20211234", "20225678"])
        db: Database session
        
    Returns:
        List of course_codes taken by these users (flattened list, duplicates preserved)
    """
    # user_ids에 해당하는 user들을 가져옴
    users = db.query(UserModel).filter(UserModel.student_id.in_(user_ids)).all()
    
    all_courses = []
    for user in users:
        for course in user.courses:
            all_courses.append(course.course_code)
            
    return all_courses


def return_course_info(courses: List[str], db: Session) -> List[CourseInfo]:
    """
    Get detailed information for a list of course codes.
    
    Args:
        courses: List of course_codes (e.g. ["CSE2003", "CSE4001"])
        db: Database session
        
    Returns:
        List of CourseInfo objects
    """
    # course_codes에 해당하는 course들을 가져옴
    course_models = db.query(CourseModel).filter(CourseModel.course_code.in_(courses)).all()
    
    # course_models을 CourseInfo로 변환
    course_infos = []
    for course in course_models:
        # course_models의 정보를 CourseInfo로 변환
        syllabus_text = f"""
Course: {course.course_name} ({course.course_code})
Department: {course.department} - {course.major}
Professor: {course.professor}
Credits: {course.credits}
Class Time: {course.class_time_room}
Description: {course.description or 'N/A'}
Remarks: {course.remarks or 'N/A'}
Target Students: {course.target_students or 'N/A'}
Recommended Year: {course.recommended_year or 'N/A'}
        """.strip()
        
        info = CourseInfo(
            course_name=course.course_name,
            course_code=course.course_code,
            department=course.department or "",
            major=course.major or "",
            professor=course.professor or "",
            credits=course.credits or 0.0,
            class_time_room=course.class_time_room or "",
            description=course.description or "",
            remarks=course.remarks or "",
            target_students=course.target_students or "",
            recommended_year=course.recommended_year or "",
            syllabus_text=syllabus_text
        )
        course_infos.append(info)
        
    return course_infos
