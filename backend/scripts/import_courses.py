import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, engine, Base
from models.course import Course
from core.config import settings

def import_courses():
    # Create tables
    print(f"Connecting to database: {settings.DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '개설교과목정보.xls')
    print(f"Reading file from: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Excel file not found at {file_path}. Skipping import.")
        return
    
    try:
        # The file is actually HTML disguised as XLS
        dfs = pd.read_html(file_path, header=0)
        if not dfs:
            print("No tables found in file")
            return
        
        df = dfs[0]
        print(f"Found {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        
        # Map columns
        # The file has these columns based on inspection:
        # 학년도, 학기, 소속, 학과, 과목번호, 분반, 과목명, 학점, 수업시간/강의실, 시간, 교수진, 수강생수, 
        # 영어강의, 중국어강의, 승인과목, CU과목, 홀짝구분, 국제학생, Honors과목, 공학인증, 시험일자, 
        # 수강대상, 권장학년, 수강신청 참조사항, 과목 설명, 비고
        
        for _, row in df.iterrows():
            # Skip header row if it's repeated or invalid
            if row['학년도'] == '학년도':
                continue
                
            course = Course(
                year=str(row['학년도']),
                semester=str(row['학기']),
                department=str(row['소속']),
                major=str(row['학과']),
                course_code=str(row['과목번호']),
                division=str(row['분반']),
                course_name=str(row['과목명']),
                credits=float(row['학점']) if pd.notna(row['학점']) else 0.0,
                class_time_room=str(row['수업시간/강의실']),
                hours=float(row['시간']) if pd.notna(row['시간']) else 0.0,
                professor=str(row['교수진']),
                capacity=str(row['수강생수']),
                english_lecture=str(row['영어강의']) if pd.notna(row['영어강의']) else None,
                chinese_lecture=str(row['중국어강의']) if pd.notna(row['중국어강의']) else None,
                approved_course=str(row['승인과목']) if pd.notna(row['승인과목']) else None,
                cu_course=str(row['CU과목']) if pd.notna(row['CU과목']) else None,
                odd_even=str(row['홀짝구분']) if pd.notna(row['홀짝구분']) else None,
                international_student=str(row['국제학생']) if pd.notna(row['국제학생']) else None,
                honors_course=str(row['Honors과목']) if pd.notna(row['Honors과목']) else None,
                engineering_certification=str(row['공학인증']) if pd.notna(row['공학인증']) else None,
                exam_date=str(row['시험일자']) if pd.notna(row['시험일자']) else None,
                target_students=str(row['수강대상']) if pd.notna(row['수강대상']) else None,
                recommended_year=str(row['권장학년']) if pd.notna(row['권장학년']) else None,
                remarks=str(row['수강신청 참조사항']) if pd.notna(row['수강신청 참조사항']) else None,
                description=str(row['과목 설명']) if pd.notna(row['과목 설명']) else None,
                note=str(row['비고']) if pd.notna(row['비고']) else None
            )
            db.add(course)
        
        db.commit()
        print("Import completed successfully")
        
    except Exception as e:
        print(f"Error importing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_courses()
