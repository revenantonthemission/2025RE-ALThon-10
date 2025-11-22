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

@router.post("/courses/{course_id}/evaluate", response_model=GeminiResponse)
def evaluate_course(
    course_id: int,
    user_profile: UserProfile,
    db: Session = Depends(get_db)
):
    """
    Evaluate a course for a specific user profile using Gemini AI.
    
    Request body example:
    {
      "taken_courses": [{"course_id": "CSE2003", "grade": "A"}],
      "eval_preference": 3,
      "interests": ["AI", "Web Development"],
      "team_preference": 4,
      "attendence_type": ["online"]
    }
    
    Args:
        course_id: The ID of the course to evaluate
        user_profile: User's profile including course history and preferences
        db: Database session
        
    Returns:
        GeminiResponse with evaluation details and summary
    """
    from backend.models.course import Course as CourseModel
    
    # Get the course from database
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Create CourseInfo from the course model
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
    
    course_info = CourseInfo(
        course_name=course.course_name,
        syllabus_text=syllabus_text
    )
    
    # Create analysis request
    analysis_request = AnalysisRequest(
        user_profile=user_profile,
        course_info=course_info
    )
    
    # TODO: Call Gemini API here with analysis_request
    # For now, return a mock response
    mock_response = GeminiResponse(
        course_id=course.course_code,
        details=[
            {
                "criteria": "학습 적합도",
                "score": 4,
                "reason": f"수강 이력: {len(user_profile.taken_courses)}개 과목 이수"
            },
            {
                "criteria": "평가 방식 적합도",
                "score": user_profile.eval_preference,
                "reason": f"평가 선호도 {user_profile.eval_preference}/5"
            },
            {
                "criteria": "팀 프로젝트 적합도",
                "score": user_profile.team_preference,
                "reason": f"팀 프로젝트 선호도 {user_profile.team_preference}/5"
            }
        ],
        summary=f"관심 분야: {', '.join(user_profile.interests)}. 선호 출석 방식: {', '.join(user_profile.attendence_type)}. 전반적으로 적합한 과목입니다."
    )
    
    return mock_response



"""
# user_id(의 리스트) 인풋, 해당 인물들의 기수강 내역 반환
return_user_courses(
	user_ids: List[str] # 유사한 선배의 user_id의 리스트
) -> List[str] # 입력된 모든 프로필의 기수강 과목 course_id를 1차원 리스트로 합쳐서 (중복되면 중복되는대로)

# course_id(의 리스트) 인풋, 해당 과목들의 정보 반환
return_course_info(
	courses: List[str] # 코스 ID string의 리스트
) -> List[CourseInfo] # Pydantic CourseInfo 오브젝트의 리스트
backend/core/schema.py의 CourseInfo 정의는 DB 모델에 대응할 수 있도록 수정 예정!
"""