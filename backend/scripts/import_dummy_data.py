#!/usr/bin/env python3
"""
Script to import dummy student data from JSON file to database.
Can be run from any directory: python backend/scripts/import_dummy_data.py
"""

import sys
import os
import json
import argparse
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get the backend directory (parent of scripts directory)
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Add both backend and project root to sys.path to allow imports
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import models and database configuration
try:
    # Try importing as if run from project root
    from backend.models.user import User, UserCourse
    from backend.db.database import Base, engine, SessionLocal
except ImportError:
    # If that fails, try importing as if run from backend directory
    from models.user import User, UserCourse
    from db.database import Base, engine, SessionLocal

def find_json_file(file_path=None):
    """Find the JSON file in common locations."""
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
    
    # Default: look in db directory, scripts directory, then backend directory
    default_name = 'dummy_data.json'
    locations = [
        BACKEND_DIR / 'db' / default_name,
        SCRIPT_DIR / default_name,
        BACKEND_DIR / default_name,
        Path.cwd() / default_name,
    ]
    
    for location in locations:
        if location.exists():
            return str(location)
    
    return None

def clear_existing_data(db):
    """Clear existing user and course data."""
    print("Clearing existing data...")
    try:
        # Delete in correct order due to foreign key constraints
        deleted_courses = db.query(UserCourse).delete()
        deleted_users = db.query(User).delete()
        db.commit()
        print(f"  ✓ Deleted {deleted_users} users and {deleted_courses} courses")
        return True
    except Exception as e:
        print(f"  ✗ Error clearing data: {e}")
        db.rollback()
        return False

def import_dummy_data(file_path=None, clear_first=False):
    """Import student data from JSON file to database."""
    # Find the JSON file
    json_file = find_json_file(file_path)
    
    if not json_file:
        print("Error: JSON file not found.")
        print(f"Looked in: {BACKEND_DIR}/db, {SCRIPT_DIR}, {BACKEND_DIR}, {Path.cwd()}")
        print("Please provide the file path as an argument or place 'dummy_data.json' in one of the above locations.")
        return 1
    
    if not os.path.exists(json_file):
        print(f"Error: JSON file not found at {json_file}")
        return 1
    
    print(f"Reading file from: {json_file}")
    
    # Read JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            students_data = json.load(f)
        print(f"Loaded {len(students_data)} students from JSON")
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return 1
    
    # Connect to database
    print(f"\nConnecting to database...")
    
    try:
        # Test connection
        with engine.connect() as conn:
            print("  ✓ Database connection successful")
        
        # Create tables if they don't exist
        print("  Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("  ✓ Tables ready")
    except Exception as e:
        print(f"  ✗ Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    db = SessionLocal()
    
    try:
        # Clear existing data if requested
        if clear_first:
            if not clear_existing_data(db):
                return 1
        
        # Import students
        print(f"\nImporting {len(students_data)} students...")
        imported_users = 0
        imported_courses = 0
        skipped_count = 0
        
        for student_data in students_data:
            try:
                # Check if user already exists
                existing_user = db.query(User).filter(
                    User.student_id == student_data['student_id']
                ).first()
                
                if existing_user:
                    print(f"  ⚠ Skipping existing student: {student_data['student_id']} ({student_data['name']})")
                    skipped_count += 1
                    continue
                
                # Create user
                user = User(
                    student_id=student_data['student_id'],
                    name=student_data['name'],
                    major=student_data['major'],
                    grade_level=student_data['grade_level'],
                    # embedding will be generated separately by the embedding service
                )
                db.add(user)
                db.flush()  # Get the user.id
                
                # Create user courses
                for course_data in student_data.get('courses', []):
                    user_course = UserCourse(
                        user_id=user.id,
                        course_code=course_data['course_code'],
                        course_name=course_data['course_name'],
                        grade_point=course_data['grade_point'],
                        semester=course_data['semester']
                    )
                    db.add(user_course)
                    imported_courses += 1
                
                imported_users += 1
                
                if imported_users % 10 == 0:
                    print(f"  Processed {imported_users} students...")
                    
            except Exception as e:
                print(f"  ⚠ Error processing student {student_data.get('student_id', 'unknown')}: {e}")
                skipped_count += 1
                continue
        
        db.commit()
        print(f"\n✓ Import completed successfully!")
        print(f"  - Imported: {imported_users} students")
        print(f"  - Imported: {imported_courses} courses")
        print(f"  - Skipped: {skipped_count} students")
        
        # Show summary
        total_users = db.query(User).count()
        total_courses = db.query(UserCourse).count()
        print(f"\nDatabase summary:")
        print(f"  - Total users: {total_users}")
        print(f"  - Total courses: {total_courses}")
        
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
    parser = argparse.ArgumentParser(
        description='Import dummy student data from JSON file to database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python import_dummy_data.py
  python import_dummy_data.py /path/to/dummy_data.json
  python import_dummy_data.py --clear
  python backend/scripts/import_dummy_data.py --clear
        """
    )
    parser.add_argument(
        'file_path',
        nargs='?',
        help='Path to the JSON file (default: searches in common locations)'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing data before importing'
    )
    
    args = parser.parse_args()
    
    exit_code = import_dummy_data(args.file_path, clear_first=args.clear)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
