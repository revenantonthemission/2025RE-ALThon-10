from google import genai
from os import getenv
from pydantic import BaseModel

# SYSPROMPT = 

client = genai.Client()

class GeminiResponse:
    risk: str
    risk_text: str
    grade_range: str

def call_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        # Structured Response config
        config={
            "response_mime_type": "application/json",
            "response_schema": GeminiResponse,
        })

    return response.text