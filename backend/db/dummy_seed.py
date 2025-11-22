# backend/seed.py

import random
from sqlalchemy import delete
from dotenv import load_dotenv
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 경로 설정 (backend/ 폴더에서 실행한다고 가정)
from backend.db.database import engine, SessionLocal, Base
from backend.models.user import User, UserCourse
from backend.db.dummy_data_user import get_dummy_users
from backend.core.encoder import generate_embeddings

load_dotenv()

# [추가] 성적 문자열 -> 숫자 변환 맵
GRADE_TO_POINT = {
    "A+": 4.5, "A": 4.0, 
    "B+": 3.5, "B": 3.0, 
    "C+": 2.5, "C": 2.0, 
    "D+": 1.5, "D": 1.0, 
    "F": 0.0, "P": 0.0 # Pass는 0점 혹은 별도 처리 (일단 0)
}

def seed_data():
    print("DB 초기화 및 데이터 마이그레이션을 시작합니다...")
    
    # 테이블 생성 (없으면 생성)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # 1. 기존 데이터 삭제
        print("기존 데이터를 정리합니다...")
        session.query(UserCourse).delete()
        session.query(User).delete()
        session.commit()

        # 2. 더미 데이터 가져오기
        dummy_profiles = get_dummy_users()
        print(f"총 {len(dummy_profiles)}명의 프로필을 변환하여 DB에 저장합니다.")

        for i, p in enumerate(dummy_profiles):
            
            # --- A. 텍스트 임베딩 생성 ---
            summary_text = (
                f"관심분야: {', '.join(p.interests)}. "
                f"평가방식선호: {p.eval_preference}점 (1:시험~5:과제). "
                f"팀플선호: {p.team_preference}점 (1:싫음~5:좋음). "
                f"선호출석: {', '.join(p.attendence_type)}."
            )
            
            try:
                print(f"   [{i+1}/{len(dummy_profiles)}] User_{i+1} 벡터화 중...")
                vector = generate_embeddings([summary_text])[0]
            except Exception as e:
                print(f"임베딩 실패: {e}")
                continue

            # --- B. User 객체 생성 ---
            db_user = User(
                student_id=f"2024{1000+i}",
                name=f"Student_{i+1}",
                major="Computer Science",
                grade_level=random.choice([3, 4]),
                embedding=vector
            )

            # --- C. 수강 과목 연결 (스키마 매칭) ---
            for course in p.taken_courses:
                # [변환 로직] 문자열 성적 -> 실수형 점수
                g_point = GRADE_TO_POINT.get(course.grade, 0.0)
                
                # [가짜 데이터] course_code가 없으므로 임의로 생성 (예: CS101)
                fake_code = f"CS{random.randint(100, 400)}"

                user_course = UserCourse(
                    course_code=fake_code,
                    course_name=course.course_id,
                    grade_point=g_point,
                    semester=random.choice(["2023-1", "2023-2", "2024-1"])
                )
                
                db_user.courses.append(user_course)

            session.add(db_user)

        # 3. 최종 저장
        session.commit()
        print("모든 데이터가 성공적으로 변환되어 저장되었습니다!")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()