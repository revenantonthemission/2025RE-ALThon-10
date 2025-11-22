from pydantic import BaseModel, Field
from typing import List, Optional

# 척도별 점수 및 이유
class AnalysisDetail(BaseModel):
    criteria: str = Field(description="분석 항목")
    score: int = Field(description="1~5 사이의 적합도 점수")
    reason: str = Field(description="근거")

# Gemini한테 반환받을 형식
class GeminiResponse(BaseModel):
    course_id: int
    details: List[AnalysisDetail]
    summary: str

# 각 과목별 유저 성적
class CourseHistory(BaseModel):
    course_id: int
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
    id: int = Field(description="과목 고유 번호 (PK)")
    year: str = Field(description="개설 학년도")
    semester: str = Field(description="개설 학기")
    
    # 학부/학과 정보
    department: Optional[str] = Field(description="개설 학부 (단과대학/소속)")
    major: Optional[str] = Field(description="개설 학과")
    
    # 과목 기본 정보
    course_code: Optional[str] = Field(description="과목 코드 (예: CS2001)")
    division: Optional[str] = Field(description="분반 정보")
    course_name: Optional[str] = Field(description="과목명")
    
    # 강의 시간/장소/학점 정보
    credits: Optional[float] = Field(description="학점")
    class_time_room: Optional[str] = Field(description="수업 시간 및 강의실 정보")
    hours: Optional[float] = Field(description="총 강의 시수 (시간)")
    professor: Optional[str] = Field(description="담당 교수")
    capacity: Optional[str] = Field(description="수강 정원")
    
    # 강의 특징 및 조건
    english_lecture: Optional[str] = Field(description="영어 강의 여부")
    chinese_lecture: Optional[str] = Field(description="중국어 강의 여부")
    approved_course: Optional[str] = Field(description="인증 교과목 여부")
    cu_course: Optional[str] = Field(description="C.U. 인증 교과목 여부")
    odd_even: Optional[str] = Field(description="홀짝 학기 교차 개설 여부")
    international_student: Optional[str] = Field(description="외국인 학생 수강 가능 여부")
    honors_course: Optional[str] = Field(description="우등생 과정 교과목 여부")
    engineering_certification: Optional[str] = Field(description="공학 인증 교과목 여부")
    
    # 시험 및 수강 대상 정보
    exam_date: Optional[str] = Field(description="시험 날짜 및 시간 정보")
    target_students: Optional[str] = Field(description="수강 대상 학년 및 학과 (예: 3학년 이상 컴퓨터공학)")
    recommended_year: Optional[str] = Field(description="권장 학년")
    
    # 상세 설명
    remarks: Optional[str] = Field(description="비고 또는 특이 사항")
    description: Optional[str] = Field(description="강의 개요 및 상세 설명")
    note: Optional[str] = Field(description="추가적인 참고 사항")

    class Config:
        from_attributes = True

# User prompt 합체
class AnalysisRequest(BaseModel):
    user_profile: UserProfile
    course_info: CourseInfo