from google import genai
from google.genai import types
from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv
from schema import GeminiResponse, AnalysisRequest, UserProfile
from typing import List
import time
import json

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
    
    # GeminiResponse의 List로 반환
    return total_results

if __name__=="__main__":
    pass
