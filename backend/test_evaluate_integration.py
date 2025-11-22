print("Starting test script...")

import sys
import os
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.routers.evaluate import evaluate_course
from backend.schemas.student_form import StudentForm

def test_evaluate_course_integration():
    # Mock Database Session
    mock_db = MagicMock(spec=Session)
    
    # Mock Course Model
    mock_course = MagicMock()
    mock_course.id = 1
    mock_course.year = "2025"
    mock_course.semester = "1"
    mock_course.course_name = "Test Course"
    mock_course.course_code = "TEST101"
    mock_course.department = "CS"
    mock_course.major = "CS"
    mock_course.division = "01"
    mock_course.credits = 3.0
    mock_course.class_time_room = "Mon 10:00"
    mock_course.hours = 3.0
    mock_course.professor = "Prof. Test"
    mock_course.capacity = "50"
    mock_course.english_lecture = "N"
    mock_course.chinese_lecture = "N"
    mock_course.approved_course = "N"
    mock_course.cu_course = "N"
    mock_course.odd_even = "N"
    mock_course.international_student = "Y"
    mock_course.honors_course = "N"
    mock_course.engineering_certification = "Y"
    mock_course.exam_date = "Midterm"
    mock_course.target_students = "All"
    mock_course.recommended_year = "3"
    mock_course.remarks = "None"
    mock_course.description = "Test Description"
    mock_course.note = "None"
    
    # Setup DB query result
    # CourseRepository uses db.query(CourseModel).filter(...).first()
    # We need to mock the chain: db.query().filter().first()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_course
    
    # Create a dummy StudentForm
    form_data = {
        "사전지식": {
            "completed_subjects": [{"id": "PRE101", "grade": "A"}]
        },
        "평가방식": {
            "exam_vs_assignment": 3
        },
        "적성": {
            "preferred_fields": ["AI"]
        },
        "협력 정도": {
            "team_project_tolerance": 4
        },
        "수업 출석 방식": {
            "attendance_method_preference": ["Online"]
        },
        "선택한 과목": [1]
    }
    form = StudentForm(**form_data)
    
    # Mock return_total_result response
    mock_results = ['{"course_id": "TEST101", "summary": "Good"}']
    
    # Patch return_total_result in backend.routers.evaluate
    with patch('backend.routers.evaluate.return_total_result') as mock_inference:
        mock_inference.return_value = mock_results
        
        # Call the function
        response = evaluate_course(course_id=1, form=form, db=mock_db)
        
        # Verify results
        print("Successfully called evaluate_course!")
        print(f"Response: {response}")
        
        assert response["course_id"] == 1
        assert response["evaluation"] == mock_results
        
        # Verify return_total_result was called with correct arguments
        args, kwargs = mock_inference.call_args
        # args[0] is count, args[1] is user_profile, args[2] is target_courses (or kwargs)
        # Check kwargs if used, or args position
        # return_total_result(count=1, user_profile=..., target_courses=...)
        
        call_kwargs = kwargs
        assert call_kwargs['count'] == 1
        assert len(call_kwargs['target_courses']) == 1
        assert call_kwargs['target_courses'][0].course_name == "Test Course"
        assert call_kwargs['user_profile'].interests == ["AI"]

if __name__ == "__main__":
    try:
        test_evaluate_course_integration()
        print("\n Test Passed!")
    except Exception as e:
        print(f"\n Test Failed: {e}")
        import traceback
        traceback.print_exc()
