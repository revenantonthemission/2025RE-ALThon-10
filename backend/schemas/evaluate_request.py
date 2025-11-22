from typing import List
from pydantic import BaseModel, Field


class TakenCourse(BaseModel):
    course_id: str = Field(description="Course code (e.g., 'CSE2003')")
    grade: str = Field(description="Grade received (e.g., 'A', 'B+')")


class EvaluateRequest(BaseModel):
    taken_courses: List[TakenCourse] = Field(default_factory=list, description="List of previously taken courses")
    eval_preference: int = Field(default=3, description="Evaluation preference (1: exam preference ~ 5: assignment preference)")
    interests: List[str] = Field(default_factory=list, description="List of interest areas/topics")
    team_preference: int = Field(default=3, description="Team project preference (1: strongly dislike ~ 5: strongly like)")
    attendence_type: List[str] = Field(default_factory=list, description="Preferred attendance methods (e.g., ['online', 'offline', 'hybrid'])")

