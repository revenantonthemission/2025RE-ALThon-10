from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from backend.db.database import get_db
from backend.schemas.evaluate_request import EvaluateRequest
from backend.core.schema import UserProfile, CourseInfo, CourseHistory, GeminiResponse
from backend.core.inference import return_total_result
from backend.repositories.repository import CourseRepository

router = APIRouter(tags=["evaluation"])

@router.post("/courses/{course_id}/evaluate")
def evaluate_course(course_id: int, request: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Evaluates a course for a specific user profile using Gemini AI.
    """

    # 1) Load course from DB
    repo = CourseRepository(db)
    course = repo.get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    # Convert to CourseInfo (Gemini format)
    course_info = CourseInfo.model_validate(course)

    # 2) Convert EvaluateRequest → UserProfile (Gemini format)
    taken_courses = [
        CourseHistory(course_id=tc.course_id, grade=tc.grade)
        for tc in request.taken_courses
    ]

    user_profile = UserProfile(
        taken_courses=taken_courses,
        eval_preference=request.eval_preference,
        interests=request.interests,
        team_preference=request.team_preference,
        attendence_type=request.attendence_type,
    )

    # 3) Call Gemini logic
    results = return_total_result(
        count=1,
        user_profile=user_profile,
        target_courses=[course_info]
    )

    # 4) Parse the JSON response (return_total_result returns List[str] with JSON strings)
    if not results or len(results) == 0:
        raise HTTPException(status_code=500, detail="Failed to get evaluation result")
    
    # Parse the first result (JSON string) into GeminiResponse
    result_json = json.loads(results[0])
    evaluation_result = GeminiResponse.model_validate(result_json)

    # 5) Return response in API spec format
    return {
        "course_id": course.course_code or str(course_id),
        "details": [
            {
                "criteria": detail.criteria,
                "score": detail.score,
                "reason": detail.reason
            }
            for detail in evaluation_result.details
        ],
        "summary": evaluation_result.summary
    }