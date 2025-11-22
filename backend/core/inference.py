from google import genai
from google.genai import types
from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv
from schema import GeminiResponse, AnalysisRequest, UserProfile
from typing import List, Optional
import time
from collections import Counter
from sqlalchemy.orm import Session
from backend.models.user import User
import json
from loguru import logger

load_dotenv()

SYSPROMPT = """
You are an expert academic advisor specializing in predicting is a student is fit for certain university courses. 

You will be provided the student's following information:
- The student's prior taken classes
- Evaluation method preference, projects/assignments(1) vs. written tests(5) 
- Interested areas as keywords
- Emphasis on cooperative projects/assignments (Prefer team project: 5 - Hate team project: 1)
- Teaching/Attendence methods: Online vs. offline, Electronic vs. verbal(any item mentioned is what user prefers. If both are chosen, user is fine with both.)

On each axis, you are to return fitness score between 1 to 5 (integers), as well as approx. 2 sentences long explanation for each axis, in the given json format.

Candidate courses and the student's individual information will be provided below.

Write all text content in Korean.
"""

client = genai.Client()
def find_recommended_course(
    current_user,
    senior_ids: List[str],
    user_target_courses: List[str] = []
) -> Optional[str]:

    # 1) 현재 사용자가 이미 수강한 과목 ID 집합 생성
    taken_course_ids = set()
    for c in getattr(current_user, "taken_courses", []) or []:
        if hasattr(c, "course_id"):
            cid = getattr(c, "course_id")
        elif isinstance(c, dict):
            cid = c.get("course_id") or c.get("id") or c.get("course_code")
        else:
            cid = c
        if cid is not None:
            taken_course_ids.add(str(cid))

    # 2) User가 수강 예정인 과목도 제외 집합에 추가
    excluded_course_ids = taken_course_ids.copy()
    for target_cid in user_target_courses:
        excluded_course_ids.add(str(target_cid))


    # 3) 선배 UserProfile 리스트 가져오기(return_course_info를 사용해)
    try:
        senior_course_infors = return_course_info(senior_ids)
    except Exception as e:
        return None

    # 4) 겹치는 횟수 cnt
    counter = Counter()
    for course_info in senior_course_infors:
        course_id_str = str(course_info.get("course_id") or course_info.get("id"))
        if course_id_str not in excluded_course_ids:
            counter[course_id_str] += 1

    # 5) 가장 많이 겹치는 과목 반환
    if not counter:
        return None

    most_common_course_id, _ = counter.most_common(1)[0]
    return most_common_course_id

# 개별 요청 함수
def call_gemini(user_prompt: AnalysisRequest):

    # Define config
    config = types.GenerateContentConfig(
        system_instruction=SYSPROMPT,
        response_mime_type="application/json",
        response_schema=GeminiResponse
    )

    # Make request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        # Structured Response config
        config=config)

    return response.text

# BE에서 호출할 함수
def return_total_result(count: int, user_profile: UserProfile) -> List[GeminiResponse]:

    total_results: List[GeminiResponse] = []
    
    # 일단은 async 아니고 무식하게
    for i in range(1, count + 1):

        if i > 1:
            time.sleep(0.3) 
            
        # 개별 요청 Argument 구성, 과목 정보는 지금은 생략
        request_data = AnalysisRequest(user_profile=user_profile, course_info="")
        
        # Gemini 호출 및 결과 취합
        result = call_gemini(request_data)
        total_results.append(result)

        # 선배들로부터 추천 과목 찾기
        senior_profiles: List[UserProfile] = get_neighbor(user_profile, k=5)
        most_common_course = find_recommended_course(user_profile, senior_profiles)

        total_results.append(most_common_course)
    return total_results

if __name__=="__main__":
    pass
