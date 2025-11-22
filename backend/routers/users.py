from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.database import get_db
from backend.models.user import User as UserModel, UserCourse as UserCourseModel
from backend.schemas.user import UserCreate, UserResponse, UserCourseCreate, UserCourseResponse

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.student_id == user.student_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    new_user = UserModel(
        student_id=user.student_id,
        name=user.name,
        major=user.major,
        grade_level=user.grade_level,
        embedding=user.embedding
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{student_id}", response_model=UserResponse)
def read_user(student_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.student_id == student_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/{student_id}/history", response_model=UserCourseResponse)
def add_course_history(student_id: str, course: UserCourseCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.student_id == student_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_course = UserCourseModel(
        user_id=db_user.id,
        course_code=course.course_code,
        course_name=course.course_name,
        grade_point=course.grade_point,
        semester=course.semester
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/users/{student_id}/history", response_model=List[UserCourseResponse])
def read_course_history(student_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.student_id == student_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.courses
