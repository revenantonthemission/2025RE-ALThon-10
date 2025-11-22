from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# UserCourse Schemas
class UserCourseBase(BaseModel):
    course_code: str
    course_name: str
    grade_point: float
    semester: str

class UserCourseCreate(UserCourseBase):
    pass

class UserCourseResponse(UserCourseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    student_id: str
    name: str
    major: str
    grade_level: int

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    courses: List[UserCourseResponse] = []

    class Config:
        from_attributes = True
