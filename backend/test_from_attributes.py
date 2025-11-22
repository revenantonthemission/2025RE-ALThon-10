"""
Test Pydantic's from_attributes approach for SQLAlchemy to Pydantic conversion.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import SessionLocal
from backend.models.user import User as UserModel
from backend.core.utils import user_to_profile
from backend.core.schema import AnalysisRequest, CourseInfo
from backend.schemas.user import UserResponse


def test_from_attributes():
    """Test Pydantic's from_attributes conversion."""
    db = SessionLocal()
    
    try:
        # Test 1: UserResponse schema (already using from_attributes)
        print("=" * 60)
        print("Test 1: UserResponse with from_attributes")
        print("=" * 60)
        
        user = db.query(UserModel).first()
        if not user:
            print("No users found in database")
            return False
        
        # Direct conversion using Pydantic's from_attributes
        user_response = UserResponse.model_validate(user)
        
        print(f"Converted User model to UserResponse schema")
        print(f"   Student ID: {user_response.student_id}")
        print(f"   Name: {user_response.name}")
        print(f"   Courses: {len(user_response.courses)}")
        
        # Test 2: UserProfile conversion
        print("\n" + "=" * 60)
        print("Test 2: UserProfile with from_attributes + utils")
        print("=" * 60)
        
        user_profile = user_to_profile(
            user,
            eval_preference=4,
            interests=["AI", "Algorithms"],
            team_preference=2,
            attendence_type=["Hybrid"]
        )
        
        print(f"Converted User model to UserProfile schema")
        print(f"   Taken courses: {len(user_profile.taken_courses)}")
        print(f"   Eval preference: {user_profile.eval_preference}")
        print(f"   Interests: {user_profile.interests}")
        print(f"   Team preference: {user_profile.team_preference}")
        
        # Test 3: Full AnalysisRequest
        print("\n" + "=" * 60)
        print("Test 3: Complete AnalysisRequest for Gemini")
        print("=" * 60)
        
        course_info = CourseInfo(
            course_name="데이터구조",
            syllabus_text="Sample syllabus text"
        )
        
        analysis_request = AnalysisRequest(
            user_profile=user_profile,
            course_info=course_info
        )
        
        print(f"Created AnalysisRequest successfully")
        print(f"   User courses: {len(analysis_request.user_profile.taken_courses)}")
        print(f"   Target course: {analysis_request.course_info.course_name}")
        
        # Show course details
        if user_profile.taken_courses:
            print(f"\n📚 Course History:")
            for course in user_profile.taken_courses[:3]:
                print(f"   - {course.course_id}: {course.grade}")
        
        print("\n" + "=" * 60)
        print("All tests passed! Option 2 (from_attributes) works!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_from_attributes()
    sys.exit(0 if success else 1)
