from google import genai
from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv()

CONFIG_PATH = "./config.json"
SYSPROMPT = """
You are an expert academic advisor specializing in predicting student performance in university courses. 

You will be provided the following 
"""

client = genai.Client()

class GeminiResponse(BaseModel):
    risk: str
    risk_text: str
    grade_range: str

class UserData(BaseModel):
    pass

# Util function to open and load json file
def load_json(path: str):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)
    
def construct_user_prompt():
    pass

def call_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[SYSPROMPT, prompt],
        # Structured Response config
        config={
            "response_mime_type": "application/json",
            "response_schema": GeminiResponse,
        })

    return response.text

if __name__=="__main__":
    
    config = load_json(CONFIG_PATH)
    SYSPROMPT = config.get("sys_prompt")

    prompt = ""

    print(call_gemini(prompt))
