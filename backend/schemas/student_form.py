from typing import List, Optional
from pydantic import BaseModel, Field


class CompletedSubject(BaseModel):
    id: str
    grade: str


class PreRequisiteKnowledge(BaseModel):
    completed_subjects: List[CompletedSubject]


class EvaluationPreference(BaseModel):
    exam_vs_assignment: int  # 0=시험 / 1=중간 / 2=과제


class Aptitude(BaseModel):
    preferred_fields: List[str]
    additional_interest: Optional[str] = None


class CollaborationPreference(BaseModel):
    team_project_tolerance: int  # 0~2 scale etc.


class ClassAndAttendanceStyle(BaseModel):
    attendance_method_preference: List[str]


class StudentForm(BaseModel):
    # 1. 사전지식
    pre_knowledge: PreRequisiteKnowledge = Field(..., alias="사전지식")

    # 2. 평가방식
    evaluation_preference: EvaluationPreference = Field(..., alias="평가방식")

    # 3. 적성
    aptitude: Aptitude = Field(..., alias="적성")

    # 4. 협력 정도
    collaboration_preference: CollaborationPreference = Field(..., alias="협력 정도")

    # 5. 수업 출석 방식
    class_and_attendance_style: ClassAndAttendanceStyle = Field(
        ..., alias="수업 출석 방식"
    )

    # 6. 선택한 과목들 (YOUR MISSING PART)
    selected_subject_ids: List[int] = Field(..., alias="선택한 과목")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
