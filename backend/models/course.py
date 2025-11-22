from sqlalchemy import Column, Integer, String, Float, Text
from backend.db.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String, index=True)
    semester = Column(String, index=True)
    department = Column(String, index=True)
    major = Column(String, index=True)
    course_code = Column(String, index=True)
    division = Column(String)
    course_name = Column(String, index=True)
    credits = Column(Float)
    class_time_room = Column(String)
    hours = Column(Float)
    professor = Column(String)
    capacity = Column(String)
    english_lecture = Column(String)
    chinese_lecture = Column(String)
    approved_course = Column(String)
    cu_course = Column(String)
    odd_even = Column(String)
    international_student = Column(String)
    honors_course = Column(String)
    engineering_certification = Column(String)
    exam_date = Column(String)
    target_students = Column(String)
    recommended_year = Column(String)
    remarks = Column(Text)
    description = Column(Text)
    note = Column(Text)
