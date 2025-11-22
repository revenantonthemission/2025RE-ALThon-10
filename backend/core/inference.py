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
from neighbor import get_similar_users

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

try:
    client = genai.Client()
    logger.info("Gemini 클라이언트 초기화 완료")
except Exception as e:
    logger.error(f"Gemini 클라이언트 초기화 실패: {e}")
    client = None
    
def find_recommended_course(
    current_user,
    senior_ids: List[str],
    db: Session
) -> Optional[str]:
    logger.info("추천 과목 산출 시작")

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
    logger.debug(f"기수강 과목 수: {len(taken_course_ids)}")

    # 2) senior_ids를 정수로 변환 후 DB에서 선배 조회
    try:
        ids_int = [int(sid) for sid in senior_ids]
    except ValueError:
        logger.warning("senior_ids 정수 변환 실패")
        return None

    seniors: List[User] = db.query(User).filter(User.id.in_(ids_int)).all()
    logger.debug(f"선배 수: {len(seniors)}")

    # 3) 선배들의 courses에서 현재 사용자가 듣지 않은 과목만 카운트
    counter = Counter()
    for senior in seniors:
        for uc in getattr(senior, "courses", []) or []:
            cid = getattr(uc, "course_id", None) or getattr(uc, "course_code", None)
            if cid is None:
                continue
            cid_str = str(cid)
            if cid_str in taken_course_ids:
                continue
            counter[cid_str] += 1
    logger.debug(f"카운트된 과목 수: {len(counter)}")

    # 4) 가장 많이 겹치는 과목 반환
    if not counter:
        logger.info("겹치는 과목 없음")
        return None

    most_common_course_id, _ = counter.most_common(1)[0]
    logger.info(f"추천 과목: {most_common_course_id}")
    return most_common_course_id

# 개별 요청 함수
def call_gemini(user_prompt: AnalysisRequest):
    if client is None:
        logger.error("Gemini 클라이언트가 초기화되지 않았습니다.")
        raise RuntimeError("Gemini client not initialized")

    logger.info("Gemini 요청 시작")

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
    logger.info(f"Gemini 응답 수신: 길이={len(response.text) if hasattr(response, 'text') and response.text else 0}")

    return response.text

# BE에서 호출할 함수
def return_total_result(count: int, user_profile: UserProfile) -> List[GeminiResponse]:
    logger.info(f"총 결과 생성 시작: count={count}")

    total_results: List[GeminiResponse] = []
    
    # 일단은 async 아니고 무식하게
    for i in range(1, count + 1):
        logger.debug(f"{i}번째 요청 처리")
        if i > 1:
            logger.debug("대기 0.3초")
            time.sleep(0.3) 
            
        # 개별 요청 Argument 구성, 과목 정보는 지금은 생략
        request_data = AnalysisRequest(user_profile=user_profile, course_info="")
        
        # Gemini 호출 및 결과 취합
        result = call_gemini(request_data)
        total_results.append(result)
        logger.debug(f"Gemini 결과 추가 (len={len(result) if result else 0})")

        # 선배들로부터 추천 과목 찾기
        # TODO: STR로 변환시켜줘야함!!
        logger.info("유사 사용자 검색 시작")
        senior_profiles: List[UserProfile] = get_similar_users(user_profile, k=5)
        logger.info("유사 사용자 검색 완료")

        most_common_course = find_recommended_course(user_profile, senior_profiles)
        logger.info(f"추천 과목: {most_common_course}")

        total_results.append(most_common_course)
        
    return total_results

if __name__=="__main__":
    pass
