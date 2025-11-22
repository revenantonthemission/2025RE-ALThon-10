from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pgvector.sqlalchemy import Vector
from os import getenv
from dotenv import load_dotenv
from typing import List
import time
from backend.models.user import User
from loguru import logger
from backend.core.encoder import generate_embeddings

load_dotenv()

# --- DB 연결 ---
DATABASE_URL = getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL 환경 변수가 설정되지 않았습니다. 애플리케이션을 종료합니다.")
    raise EnvironmentError("DATABASE_URL 환경 변수를 설정해야 합니다.")

engine = create_engine(DATABASE_URL)
logger.info("데이터베이스 엔진 초기화 완료")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """DB 세션을 관리하는 제너레이터 함수"""
    db = SessionLocal()
    logger.debug("DB 세션 생성")
    try:
        yield db
    finally:
        try:
            db.close()
            logger.debug("DB 세션 종료")
        except Exception as e:
            logger.error(f"DB 세션 종료 중 오류: {e}")

# --- kNN 검색 ---
def find_similar_users(db: Session, query_vector: List[float], k: int = 5) -> List[int]:
    """
    User.feature_vector 컬럼을 사용하여 PostgreSQL에서 kNN 검색을 실행하고 
    유사 유저 목록 (User 객체 리스트)을 반환합니다.
    """
    if not query_vector:
        logger.warning("빈 query_vector가 전달되어 유사 사용자 검색을 건너뜁니다.")
        return []

    logger.debug(f"kNN 검색 준비: k={k}, 벡터차원={len(query_vector)}")
    start = time.perf_counter()
    try:
        # 코사인 거리 연산자 (<=>) 사용
        similar_users = (
            db.query(User)
            .order_by(User.embedding.cosine_distance(query_vector))
            .limit(k)
            .all()
        )
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(f"kNN 검색 완료: k={k}, 결과={len(similar_users)}건, 소요={duration_ms:.1f}ms")
        if similar_users:
            try:
                ids = [u.id for u in similar_users if hasattr(u, 'id')]
                logger.debug(f"유사 사용자 ID: {ids}")
            except Exception:
                logger.debug("유사 사용자 ID를 로깅하는 중 오류가 발생했지만 검색 결과에는 영향이 없습니다.")
        return ids
    except Exception as e:
        logger.error("kNN 검색 중 오류 발생 : {e}")
        raise

# --- 통합 메인 파이프라인 함수 (Top K User 반환) ---
def get_similar_users(user_profile_data: str, k: int = 5) -> List[int]:
    """
    유저 입력 데이터를 받아 임베딩을 생성하고 kNN 검색,
    Top K 유사 유저 객체 리스트를 반환
    
    :param user_profile_data: 현재 검색하는 유저 프로필
    :param k: 찾을 유사 유저의 수
    :return: Top K User 객체 리스트 (List[User])
    """
    logger.info(f"유사 사용자 검색 시작: k={k}, 입력길이={len(user_profile_data) if user_profile_data else 0}")
    # 유저 입력 임베딩 생성
    try:
        query_vector = generate_embeddings([user_profile_data])[0]
    except Exception:
        logger.error("임베딩 생성 중 오류 발생")
        raise

    # DB 세션 확보
    db_session_generator = get_db_session()
    db = next(db_session_generator)
    
    try:
        logger.info(f"kNN 검색 실행 (k={k})")
        similar_users: List[int] = find_similar_users(db, query_vector, k=k)
        logger.info(f"유사 사용자 검색 종료: 결과={len(similar_users)}건")
        return similar_users
    finally:
        # DB 세션 명시적으로 닫기
        try:
            db.close()
            logger.debug("get_similar_users: DB 세션 종료")
        except Exception as e:
            logger.error(f"get_similar_users: DB 세션 종료 중 오류: {e}")
