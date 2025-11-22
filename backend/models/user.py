from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector
from backend.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    major = Column(String)
    grade_level = Column(Integer)
    embedding = Column(Vector(1024))  # 1024-dimensional vector for Gemini embeddings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courses = relationship("UserCourse", back_populates="user")

class UserCourse(Base):
    __tablename__ = "user_courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_code = Column(String, index=True)
    course_name = Column(String)
    grade_point = Column(Float)
    semester = Column(String)
    
    user = relationship("User", back_populates="courses")
