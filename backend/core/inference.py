from google import genai
from google.genai import types
from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv
from schema import GeminiResponse, AnalysisRequest
import json

load_dotenv()

CONFIG_PATH = "./config.json"
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

# Util function to open and load json file
def load_json(path: str):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)
    
def call_gemini(user_prompt: AnalysisRequest):

    # Define config
    config = types.GenerateContentConfig(
        system_instruction=SYSPROMPT,
        response_mime_type="application/json",
        response_schema=GeminiResponse
    )

    # Get user prompt
    user_prompt = AnalysisRequest

    # Make request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        # Structured Response config
        config=config)

    return response.text

if __name__=="__main__":
    
    config = load_json(CONFIG_PATH)
    SYSPROMPT = config.get("sys_prompt")

    prompt = ""

    print(call_gemini(prompt))
