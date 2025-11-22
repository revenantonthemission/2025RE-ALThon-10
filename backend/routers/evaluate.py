from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.schemas.student_form import StudentForm
from backend.schemas.course import CourseResponse
from backend.core.schema import UserProfile, CourseInfo
from backend.core.inference import return_total_result
from backend.repositories.repository import CourseRepository

router = APIRouter(tags=["evaluation"])

@router.post("/courses/{course_id}/evaluate")
def evaluate_course(course_id: int, form: StudentForm, db: Session = Depends(get_db)):
    """
    Evaluate a course using Gemini based on the user's StudentForm.
    """

    # 1) Load course from DB
    repo = CourseRepository(db)
    course = repo.get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    # Convert to CourseInfo (Gemini format)
    course_info = CourseInfo(
        course_name=course.course_name,
        syllabus_text=course.description or ""
    )

    # 2) Convert StudentForm → UserProfile (Gemini format)
    taken_courses = [
        {"course_id": s.id, "grade": s.grade}
        for s in form.pre_knowledge.completed_subjects
    ]

    user_profile = UserProfile(
        taken_courses=taken_courses,
        eval_preference=form.evaluation_preference.exam_vs_assignment,
        interests=form.aptitude.preferred_fields,
        team_preference=form.collaboration_preference.team_project_tolerance,
        attendence_type=form.class_and_attendance_style.attendance_method_preference,
    )

    # 3) Call Gemini logic
    results = return_total_result(
        count=1,
        user_profile=user_profile,
        target_courses=[course_info]
    )

    # 4) Response format
    return {
        "course_id": course_id,
        "evaluation": results
    }