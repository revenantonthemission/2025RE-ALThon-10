from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from backend.models.course import Course as CourseModel

class CourseSummary(BaseModel):
    id: int
    course_name: str
    course_code: str

    @classmethod
    def from_model(cls, model: "CourseModel") -> "CourseSummary":
        return cls(
            id=model.id,
            course_name=model.course_name,
            course_code=model.course_code
        )

    class Config:
        from_attributes = True


class CourseResponse(CourseSummary):
    year: Optional[str] = None
    semester: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    division: Optional[str] = None
    credits: Optional[float] = None
    class_time_room: Optional[str] = None
    hours: Optional[float] = None
    professor: Optional[str] = None
    capacity: Optional[str] = None
    english_lecture: Optional[str] = None
    chinese_lecture: Optional[str] = None
    approved_course: Optional[str] = None
    cu_course: Optional[str] = None
    odd_even: Optional[str] = None
    international_student: Optional[str] = None
    honors_course: Optional[str] = None
    engineering_certification: Optional[str] = None
    exam_date: Optional[str] = None
    target_students: Optional[str] = None
    recommended_year: Optional[str] = None
    remarks: Optional[str] = None
    description: Optional[str] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    courses: List[CourseSummary]