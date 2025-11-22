from pydantic import BaseModel, Field
from typing import List

# 척도별 점수 및 이유
class AnalysisDetail(BaseModel):
    criteria: str = Field(description="분석 항목")
    score: int = Field(description="1~5 사이의 적합도 점수")
    reason: str = Field(description="근거")

# Gemini한테 반환받을 형식
class GeminiResponse(BaseModel):
    course_id: str
    details: List[AnalysisDetail]
    summary: str

# 각 과목별 유저 성적
class CourseHistory(BaseModel):
    course_id: str
    grade: str
    
    class Config:
        from_attributes = True

# 유저 정보 종합
class UserProfile(BaseModel):
    taken_courses: List[CourseHistory] = Field(description="이미 수강한 과목 리스트")
    eval_preference: int = Field(default=3, description="평가 방식 선호도 (1:시험선호 ~ 5:과제선호)")
    interests: List[str] = Field(default_factory=list, description="관심있는 적성 분야")
    team_preference: int = Field(default=3, description="조별과제 선호도 (1:매우싫음 ~ 5:매우좋음)")
    attendence_type: List[str] = Field(default_factory=list, description="선호하는 출석 방식")
    
    class Config:
        from_attributes = True

# 과목별 정보
class CourseInfo(BaseModel):
    course_name: str = Field(description="강의명")
    syllabus_text: str = Field(description="강의계획서 전체 텍스트")

# User prompt 합체
class AnalysisRequest(BaseModel):
    user_profile: UserProfile
    course_info: CourseInfo