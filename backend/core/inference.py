from google import genai
from google.genai import types
from os import getenv
from dotenv import load_dotenv
from backend.core.schema import GeminiResponse, AnalysisRequest, UserProfile, CourseInfo, CourseHistory
from typing import List, Optional
import time
from collections import Counter
from backend.core.utils import return_user_courses, return_course_info
import json
from loguru import logger
from backend.core.neighbor import get_similar_users

load_dotenv()

SYSPROMPT = """
You are an expert academic advisor specializing in predicting is a student is fit for certain university courses. 

You will be provided the student's following information:
- The student's prior taken classes (the information text will be long by nature, but the length doesn't necessarily mean importance. Refer to it with objectivity. Do consider the grade the user got in each class, as a reference point on assessing the user's strong/weak points.)
- Evaluation method preference, projects/assignments(1) vs. written tests(5) 
- Interested areas as keywords
- Emphasis on cooperative projects/assignments (Prefer team project: 5 - Hate team project: 1)
- Teaching/Attendence methods: Online vs. offline, Electronic vs. verbal(any item mentioned is what user prefers. If both are chosen, user is fine with both.)

On each axis, you are to return fitness score between 1 to 5 (integers), as well as approx. 2 sentences long explanation for each axis, in the given json format.

Candidate courses and the student's individual information will be provided below.

Write all text content in Korean.
"""

GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")

try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    logger.info("Gemini 클라이언트 초기화 완료")
except Exception as e:
    logger.error(f"Gemini 클라이언트 초기화 실패: {e}")
    client = None

# TODO: 직접 db 접근하지 않고 BE에서 제공하는 함수로 연결
def find_recommended_course(
    current_user: UserProfile,
    senior_ids: List[int],
    user_target_courses: List[str] = []
) -> Optional[str]:
    logger.info("추천 과목 산출 시작")

    # 1) 현재 사용자가 이미 수강한 과목 ID 집합 생성
    taken_course_ids = set()
    for c in getattr(current_user, "taken_courses", []) or []:
        if hasattr(c, "course_id"):
            cid = getattr(c, "course_id")
        elif isinstance(c, dict):
            cid = c.get("course_id") or c.get("id") or c.get("course_id")
        else:
            cid = c
        if cid is not None:
            taken_course_ids.add(str(cid))
    logger.debug(f"기수강 과목 수: {len(taken_course_ids)}")

    # 2) User가 수강 예정인 과목도 제외 집합에 추가
    excluded_course_ids = taken_course_ids.copy()
    for target_cid in user_target_courses:
        excluded_course_ids.add(str(target_cid))

    # 3) 선배 UserProfile 리스트 가져오기(return_course_info를 사용해)
    # TODO: senior를 UserProfile로 받은 상태에서, id 추출 해서 arg로 전달
    try:
        senior_course_infors = return_user_courses(senior_ids)
    except Exception as e:
        logger.error(f"선배 기수강 정보 획득 실패: {e}")
        return None

    # 4) 겹치는 횟수 cnt
    counter = Counter()
    for course_info in senior_course_infors:
        course_id_str = str(course_info.get("course_id") or course_info.get("id"))
        if course_id_str not in excluded_course_ids:
            counter[course_id_str] += 1

    # 5) 가장 많이 겹치는 과목 반환
    if not counter:
        logger.info("겹치는 과목 없음")
        return None

    most_common_course_id, _ = counter.most_common(1)[0]
    logger.info(f"추천 과목: {most_common_course_id}")
    return most_common_course_id

# Prompt 문자열로 변경
def create_gemini_prompt(request_data: AnalysisRequest) -> str:
    """
    Formats the user profile and course information into a single string prompt
    for the Gemini model to analyze.
    """
    
    taken_courses_history: List[CourseHistory] = request_data.user_profile.taken_courses

    taken_courses_id_list: List[int] = [history.course_id for history in taken_courses_history]

    taken_courses_detail: List[CourseInfo] = return_course_info(taken_courses_id_list)

    course_strings = []

    for course, history in zip(taken_courses_detail, taken_courses_history):
        # 각 CourseInfo 객체에서 분석에 필요한 핵심 정보 추출
        
        # CourseInfo 객체인지 확인 (course_code가 있는 경우)
        if hasattr(course, "course_code") and course.course_code:
            
            # 1. 기본 정보 섹션
            base_info = (
                f"[{course.course_code}] {course.course_name} (개설년도/학기: {course.year or '미상'}/{course.semester or '미상'} | "
                f"{course.credits or '미상'}학점 | {course.hours or '미상'}시수) "
                f"개설: {course.department or '미상'} ({course.major or '미상'}) | 담당교수: {course.professor or '미상'}. "
                f"강의 시간/장소: {course.class_time_room or '미상'} (정원: {course.capacity or '미상'}). "
            )
            
            # 2. 강의 특징 섹션
            feature_info = (
                f"특징: {course.target_students or course.recommended_year or '전학년'} 대상. "
                f"영어강의: {course.english_lecture or 'N'} | 중국어강의: {course.chinese_lecture or 'N'} | "
                f"인증교과목: {course.approved_course or 'N'} | 우등생과정: {course.honors_course or 'N'}. "
            )

            # 3. 시험 및 성적 섹션 (CourseHistory에서 성적 정보를 가져옴)
            # taken_courses_history의 성적 정보를 가져와 추가
            grade_info = f"성적: {history.grade or '미상'}."
            exam_info = f"시험일정: {course.exam_date or '미상'}."
            
            # 4. 상세 정보 섹션 (비고/개요 등)
            detail_info = f"상세설명(개요/비고): {course.description or course.remarks or '내용 없음'}."
            
            course_string = base_info + feature_info + grade_info + exam_info + detail_info
            
        else:
            # CourseHistory 객체 폴백 (CourseInfo가 아닌 경우)
            course_string = f"[ID: {course.course_id}] 성적: {course.grade}"
            
        course_strings.append(course_string)

    # 모든 과목 정보를 줄바꿈으로 구분하여 하나의 문자열로 결합
    taken_courses_detail_str = "\n".join(course_strings) or "없음"

    # 1. User Profile Details (similar to extract_profile_text but for the prompt)
    user_info = f"""
    --- 학생 정보 ---
    - 기수강 과목: {taken_courses_detail_str}
    - 평가 방식 선호 (1:시험, 5:과제): {request_data.user_profile.eval_preference}
    - 관심 분야: {', '.join(request_data.user_profile.interests)}
    - 팀 프로젝트 선호 (1:매우 싫음, 5:매우 좋음): {request_data.user_profile.team_preference}
    - 선호 출석/수업 방식: {', '.join(request_data.user_profile.attendence_type)}
    """

    # 2. Course Information
    course_info_parts = [
        f"--- 분석 대상 과목 정보 ---",
        f"- 과목 코드: {request_data.course_info.course_code or '정보 없음'}",
        f"- 과목명: {request_data.course_info.course_name or '정보 없음'}",
    ]
    
    # Add optional fields if they exist
    if request_data.course_info.department:
        course_info_parts.append(f"- 개설 학부: {request_data.course_info.department}")
    if request_data.course_info.major:
        course_info_parts.append(f"- 개설 학과: {request_data.course_info.major}")
    if request_data.course_info.professor:
        course_info_parts.append(f"- 담당 교수: {request_data.course_info.professor}")
    if request_data.course_info.credits:
        course_info_parts.append(f"- 학점: {request_data.course_info.credits}")
    if request_data.course_info.description:
        course_info_parts.append(f"- 강의 개요: {request_data.course_info.description}")
    if request_data.course_info.remarks:
        course_info_parts.append(f"- 비고: {request_data.course_info.remarks}")
    
    course_info = "\n    ".join(course_info_parts) + "\n    "
    
    # 3. Final instruction
    final_instruction = "\n\n위 학생 정보를 바탕으로 아래 과목에 대한 적합도를 분석하고 JSON 형식으로 결과를 반환하시오."
    
    return user_info + course_info + final_instruction

# 개별 요청 함수
def call_gemini(user_prompt: AnalysisRequest):
    if client is None:
        logger.error("Gemini 클라이언트가 초기화되지 않았습니다.")
        raise RuntimeError("Gemini client not initialized")

    logger.info("Gemini 요청 시작")

    prompt_str = create_gemini_prompt(user_prompt)

    # Define config
    config = types.GenerateContentConfig(
        system_instruction=SYSPROMPT,
        response_mime_type="application/json",
        response_schema=GeminiResponse
    )

    # Make request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_str,
        # Structured Response config
        config=config)
    logger.info(f"Gemini 응답 수신: 길이={len(response.text) if hasattr(response, 'text') and response.text else 0}")

    return response.text

def extract_profile_text(user_profile: UserProfile) -> str:
    """
    UserProfile 객체에서 'taken_courses'를 제외한 모든 필드를 추출하여
    임베딩 생성을 위한 단일 문자열로 결합합니다.
    """
    
    # taken_courses를 제외하고 모든 데이터를 딕셔너리로 추출합니다.
    user_data_dict = user_profile.model_dump(exclude={"taken_courses"}) 
    
    parts = []
    
    # 평가 방식 선호도 (eval_preference)
    if 'eval_preference' in user_data_dict:
        parts.append(f"평가 방식 선호도: {user_data_dict['eval_preference']} (1:시험선호, 5:과제선호)")
    
    # 관심 분야 (interests) - 리스트를 쉼표로 연결
    interests: List[str] = user_data_dict.get('interests', [])
    if interests:
        parts.append(f"관심 분야: {', '.join(interests)}")
        
    # 팀 프로젝트 선호도 (team_preference)
    if 'team_preference' in user_data_dict:
        parts.append(f"팀 프로젝트 선호도: {user_data_dict['team_preference']} (1:매우싫음, 5:매우좋음)")
    
    # 선호 출석 방식 (attendence_type) - 리스트를 쉼표로 연결
    attendance: List[str] = user_data_dict.get('attendence_type', [])
    if attendance:
        parts.append(f"선호 출석 방식: {', '.join(attendance)}")
    
    # 모든 정보를 쉼표와 공백으로 연결하여 최종 문자열 생성
    user_profile_str = ", ".join(parts)
    
    return user_profile_str

# BE에서 호출할 함수
def return_total_result(count: int, user_profile: UserProfile, target_courses: List[CourseInfo]):
    logger.info(f"총 결과 생성 시작: count={count}")

    total_results: List[GeminiResponse] = []
    
    # 일단은 async 아니고 무식하게
    for i in range(1, count + 1):
        logger.debug(f"{i}번째 요청 처리")
        if i > 1:
            logger.debug("대기 0.3초")
            time.sleep(0.3) 
            
        # 개별 요청 Argument 구성, 과목 정보는 지금은 생략
        request_data = AnalysisRequest(user_profile=user_profile, course_info=target_courses[i-1])
        
        # Gemini 호출 및 결과 취합
        result = call_gemini(request_data)
        # 선배들로부터 추천 과목 찾기
        user_profile_str = extract_profile_text(user_profile)

        logger.info("유사 사용자 검색 시작")
        senior_ids: List[int] = get_similar_users(user_profile_str, k=5)
        logger.info("유사 사용자 검색 완료")

        most_common_course = find_recommended_course(user_profile, senior_ids)
        logger.info(f"추천 과목: {most_common_course}")

        total_results.append({
            "evaluation": result,
            "recommendation": most_common_course
        })

    return total_results

if __name__=="__main__":
    pass
