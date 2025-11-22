#!/usr/bin/env python3
"""
Independent script to import course data from Excel file to database.
Can be run from any directory: python backend/scripts/import_courses.py [file_path]
"""

import sys
import os
import argparse
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get the backend directory (parent of scripts directory)
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent

# Add backend directory to sys.path to allow imports
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Database connection configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "user"
DB_PASSWORD = "password"
DB_NAME = "course_db"  # Default database name, can be overridden

# Initialize these as None, will be created when needed
engine = None
SessionLocal = None
Base = declarative_base()

def get_database_connection(db_name=None):
    """Create and return database engine and session factory."""
    global engine, SessionLocal, DB_NAME
    
    # Use provided db_name or default
    current_db_name = db_name if db_name else DB_NAME
    
    # Check if we need to recreate the connection (new db_name or engine is None)
    if engine is None or (db_name and db_name != DB_NAME):
        # Check if psycopg2 is available
        try:
            import psycopg2
        except ImportError:
            try:
                import psycopg2_binary
            except ImportError:
                print("Error: psycopg2 or psycopg2-binary is required to connect to PostgreSQL.")
                print("Please install it using: pip install psycopg2-binary")
                sys.exit(1)
        
        # Create database connection
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{current_db_name}"
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        if db_name:
            DB_NAME = current_db_name
    
    return engine, SessionLocal

# Define Course model locally using our Base
from sqlalchemy import Column, Integer, String, Float, Text

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

def find_excel_file(file_path=None):
    """Find the Excel file in common locations."""
    if file_path:
        if os.path.isabs(file_path):
            return file_path
        # If relative path provided, try relative to script directory
        candidate = SCRIPT_DIR / file_path
        if candidate.exists():
            return str(candidate)
        # Try relative to current working directory
        candidate = Path.cwd() / file_path
        if candidate.exists():
            return str(candidate)
        return file_path
    
    # Default: look in scripts directory first, then backend directory
    default_name = '개설교과목정보.xls'
    locations = [
        SCRIPT_DIR / default_name,
        BACKEND_DIR / default_name,
        Path.cwd() / default_name,
    ]
    
    for location in locations:
        if location.exists():
            return str(location)
    
    return None

def import_courses(file_path=None):
    """Import courses from Excel file to database."""
    # Find the Excel file
    excel_file = find_excel_file(file_path)
    
    if not excel_file:
        print("Error: Excel file not found.")
        print(f"Looked in: {SCRIPT_DIR}, {BACKEND_DIR}, {Path.cwd()}")
        print("Please provide the file path as an argument or place '개설교과목정보.xls' in one of the above locations.")
        return 1
    
    if not os.path.exists(excel_file):
        print(f"Error: Excel file not found at {excel_file}")
        return 1
    
    print(f"Reading file from: {excel_file}")
    
    # Get database connection (will check for psycopg2 and create engine)
    print(f"\nConnecting to database...")
    print(f"  Host: {DB_HOST}:{DB_PORT}")
    print(f"  Database: {DB_NAME}")
    print(f"  User: {DB_USER}")
    print(f"  URL: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    try:
        # Initialize database connection
        engine, SessionLocal = get_database_connection()
        
        # Test connection
        with engine.connect() as conn:
            print("  ✓ Database connection successful")
        
        # Create tables if they don't exist
        print("  Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("  ✓ Tables ready")
    except SystemExit:
        # Re-raise SystemExit from get_database_connection if psycopg2 is missing
        raise
    except Exception as e:
        print(f"  ✗ Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    db = SessionLocal()
    
    try:
        # The file is actually HTML disguised as XLS
        print("Reading HTML table from file...")
        dfs = pd.read_html(excel_file, header=0)
        if not dfs:
            print("Error: No tables found in file")
            return 1
        
        df = dfs[0]
        print(f"Found {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        
        # Map columns
        # The file has these columns based on inspection:
        # 학년도, 학기, 소속, 학과, 과목번호, 분반, 과목명, 학점, 수업시간/강의실, 시간, 교수진, 수강생수, 
        # 영어강의, 중국어강의, 승인과목, CU과목, 홀짝구분, 국제학생, Honors과목, 공학인증, 시험일자, 
        # 수강대상, 권장학년, 수강신청 참조사항, 과목 설명, 비고
        
        imported_count = 0
        skipped_count = 0
        
        for idx, row in df.iterrows():
            # Skip header row if it's repeated or invalid
            try:
                if str(row.get('학년도', '')).strip() == '학년도':
                    skipped_count += 1
                    continue
                
                course = Course(
                    year=str(row['학년도']) if pd.notna(row['학년도']) else '',
                    semester=str(row['학기']) if pd.notna(row['학기']) else '',
                    department=str(row['소속']) if pd.notna(row['소속']) else '',
                    major=str(row['학과']) if pd.notna(row['학과']) else '',
                    course_code=str(row['과목번호']) if pd.notna(row['과목번호']) else '',
                    division=str(row['분반']) if pd.notna(row['분반']) else '',
                    course_name=str(row['과목명']) if pd.notna(row['과목명']) else '',
                    credits=float(row['학점']) if pd.notna(row['학점']) else 0.0,
                    class_time_room=str(row['수업시간/강의실']) if pd.notna(row['수업시간/강의실']) else '',
                    hours=float(row['시간']) if pd.notna(row['시간']) else 0.0,
                    professor=str(row['교수진']) if pd.notna(row['교수진']) else '',
                    capacity=str(row['수강생수']) if pd.notna(row['수강생수']) else '',
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
                imported_count += 1
                
                if (imported_count + skipped_count) % 100 == 0:
                    print(f"Processed {imported_count + skipped_count} rows...")
                    
            except Exception as e:
                print(f"Warning: Error processing row {idx}: {e}")
                skipped_count += 1
                continue
        
        db.commit()
        print(f"\nImport completed successfully!")
        print(f"  - Imported: {imported_count} courses")
        print(f"  - Skipped: {skipped_count} rows")
        return 0
        
    except Exception as e:
        print(f"Error importing data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return 1
    finally:
        db.close()

def main():
    """Main entry point with command-line argument support."""
    global DB_NAME
    
    parser = argparse.ArgumentParser(
        description='Import course data from Excel file to database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python import_courses.py
  python import_courses.py /path/to/개설교과목정보.xls
  python import_courses.py --db-name my_database
  python backend/scripts/import_courses.py
        """
    )
    parser.add_argument(
        'file_path',
        nargs='?',
        help='Path to the Excel file (default: searches in common locations)'
    )
    parser.add_argument(
        '--db-name',
        default=None,
        help=f'Database name (default: {DB_NAME})'
    )
    
    args = parser.parse_args()
    
    # Update database name if provided
    if args.db_name:
        DB_NAME = args.db_name
    
    exit_code = import_courses(args.file_path)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
