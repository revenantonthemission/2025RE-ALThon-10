from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    year: Optional[str] = None
    semester: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    course_code: Optional[str] = None
    division: Optional[str] = None
    course_name: Optional[str] = None
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

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

# Lightweight DTO with only id and name
class CourseSummary(BaseModel):
    id: int
    course_name: str
    
    class Config:
        from_attributes = True
