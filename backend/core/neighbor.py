from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pgvector.sqlalchemy import Vector
from os import getenv
from dotenv import load_dotenv
from typing import List
from sentence_transformers import SentenceTransformer
from backend.models.user import User
from loguru import logger

load_dotenv()

# --- DB 연결 ---
DATABASE_URL = getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL 환경 변수를 설정해야 합니다.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """DB 세션을 관리하는 제너레이터 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 임베딩 모델 설정 ---
EMBEDDING_MODEL_NAME = "jhgan/ko-sroberta-multitask"
try:
    EMBEDDER = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception as e:
    logger.error(f"임베딩 모델 로드 실패: {e}")
    EMBEDDER = None

# --- kNN 검색 ---
def find_similar_users(db: Session, query_vector: List[float], k: int = 5) -> List[User]:
    """
    User.feature_vector 컬럼을 사용하여 PostgreSQL에서 kNN 검색을 실행하고 
    유사 유저 목록 (User 객체 리스트)을 반환합니다.
    """
    if not query_vector:
        return []

    # 코사인 거리 연산자 (<=>) 사용
    similar_users = (
        db.query(User)
        .order_by(User.embedding.cosine_distance(query_vector)) 
        .limit(k)
        .all()
    )
    
    return similar_users

# --- 통합 메인 파이프라인 함수 (Top K User 반환) ---
def get_similar_users(user_profile_data: str, k: int = 5) -> List[User]:
    """
    유저 입력 데이터를 받아 임베딩을 생성하고 kNN 검색,
    Top K 유사 유저 객체 리스트를 반환
    
    :param user_profile_data: 현재 검색하는 유저 프로필
    :param k: 찾을 유사 유저의 수
    :return: Top K User 객체 리스트 (List[User])
    """
    
    if EMBEDDER is None:
        raise RuntimeError("Embedding model not loaded.")
    
    # 유저 입력 임베딩 생성 (768차원)
    query_vector = EMBEDDER.encode(user_profile_data, convert_to_tensor=False).tolist()

    # DB 세션 확보
    db_session_generator = get_db_session()
    db = next(db_session_generator)
    
    try:
        print(f"beginning kNN search. (k={k})")
        
        # 3. kNN 검색 실행 및 Top K User 객체 반환
        similar_users: List[User] = find_similar_users(db, query_vector, k=k)
        
        return similar_users
    
    finally:
        # DB 세션 명시적으로 닫기
        db.close()