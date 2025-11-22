GET /courses
response

```json
{
  "courses": [
    {
      "id": "id",
      "course_code": "adf",
      "couse_name": "adsf"
    },
    {
      "id": "id",
      "course_code": "adf",
      "couse_name": "adsf"
    }
  ]
}
```

POST /courses/{course_id}/evaluate

Evaluates a course for a specific user profile using Gemini AI.

**Path Parameters:**

- `course_id` (integer, required): The ID of the course to evaluate

**Request Body:**

```json
{
  "taken_courses": [
    {
      "course_id": "CSE2003",
      "grade": "A"
    }
  ],
  "eval_preference": 3,
  "interests": ["AI", "Web Development"],
  "team_preference": 4,
  "attendence_type": ["online"]
}
```

**Request Body Schema:**

- `taken_courses` (array, required): List of previously taken courses
  - `course_id` (string): Course code (e.g., "CSE2003")
  - `grade` (string): Grade received (e.g., "A", "B+")
- `eval_preference` (integer, default: 3): Evaluation preference (1: exam preference ~ 5: assignment preference)
- `interests` (array, default: []): List of interest areas/topics
- `team_preference` (integer, default: 3): Team project preference (1: strongly dislike ~ 5: strongly like)
- `attendence_type` (array, default: []): Preferred attendance methods (e.g., ["online", "offline", "hybrid"])

**Response (200 OK):**

```json
{
  "course_id": "CSE2003",
  "details": [
    {
      "criteria": "학습 적합도",
      "score": 4,
      "reason": "수강 이력: 5개 과목 이수"
    },
    {
      "criteria": "평가 방식 적합도",
      "score": 3,
      "reason": "평가 선호도 3/5"
    },
    {
      "criteria": "팀 프로젝트 적합도",
      "score": 4,
      "reason": "팀 프로젝트 선호도 4/5"
    }
  ],
  "summary": "관심 분야: AI, Web Development. 선호 출석 방식: online. 전반적으로 적합한 과목입니다."
}
```

**Response Schema:**

- `course_id` (string): Course code
- `details` (array): List of analysis details
  - `criteria` (string): Analysis criteria name
  - `score` (integer): Suitability score (1-5)
  - `reason` (string): Reasoning for the score
- `summary` (string): Overall evaluation summary

**Error Responses:**

- `404 Not Found`: Course not found
  ```json
  {
    "detail": "Course not found"
  }
  ```
