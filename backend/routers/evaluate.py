from fastapi import APIRouter
from backend.schemas.student_form import StudentForm

router = APIRouter(tags=["evaluation"])

@router.post("/evaluate")
def evaluate_student(form: StudentForm):

    return {
        "message": "Form received successfully",
        "received": form
    }
