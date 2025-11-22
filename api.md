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

POST /courses/{id}/evaluate
data

```json
{
  "taken_courses":[
    {
      "id":"test",
      "grade":"A"
    }
  ],
  "eval_preference":3,
  "interests":[
    "asdf","asdfa"
  ],
  "team_preference":4,
  "attendence_type"[
    "online"
  ]
}
```
