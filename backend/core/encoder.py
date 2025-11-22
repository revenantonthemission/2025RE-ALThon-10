from sentence_transformers import SentenceTransformer
from typing import List, Optional
from loguru import logger
import time
import numpy as np

# --- 모델 설정 및 로드 ---
EMBEDDING_MODEL_NAME = "jhgan/ko-sroberta-multitask"
EMBEDDER: Optional[SentenceTransformer] = None

try:
    start_time = time.perf_counter()
    EMBEDDER = SentenceTransformer(EMBEDDING_MODEL_NAME)
    load_duration_ms = (time.perf_counter() - start_time) * 1000
    logger.info(f"임베딩 모델 로드 성공: {EMBEDDING_MODEL_NAME}, 소요={load_duration_ms:.1f}ms")
except Exception as e:
    logger.error(f"임베딩 모델 로드 실패: {e}")
    EMBEDDER = None

def generate_embeddings(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    주어진 텍스트 리스트를 batch_size 단위로 청크 처리하며 임베딩 벡터 리스트를 생성
    (배치 처리 중 오류 발생 시, 최대 2회 재시도 후 성공한 배치까지의 결과를 반환함)
    
    :param texts: 임베딩을 생성할 입력 텍스트 리스트
    :param batch_size: 배치 처리 크기 (기본값: 32)
    :return: 성공적으로 처리된 임베딩 벡터 리스트 (List[List[float]])
    :raises RuntimeError: 임베딩 모델이 로드되지 않았을 경우
    """
    if EMBEDDER is None:
        logger.error("임베딩 모델(EMBEDDER)이 로드되지 않아 임베딩을 생성할 수 없습니다.")
        raise RuntimeError("Embedding model not initialized.")

    if not texts:
        logger.warning("빈 텍스트 리스트 입력.")
        return []

    # 성공적으로 생성된 모든 임베딩을 누적할 리스트
    all_embeddings: List[List[float]] = []
    MAX_RETRIES = 2  # 1번 시도 후 최대 2번 재시도 = 총 3번 시도
    
    i = 0
    while i < len(texts):
        chunk = texts[i:i + batch_size]
        chunk_index = i // batch_size
        
        attempt = 0
        batch_success = False
        
        # --- 내부 루프: 배치별 재시도 로직 ---
        while attempt <= MAX_RETRIES:
            try:
                logger.debug(f"배치 #{chunk_index} 시도 #{attempt + 1}/{MAX_RETRIES + 1} 처리 시작 (크기: {len(chunk)})")
                
                start_time = time.perf_counter()
                
                # 텍스트 임베딩 생성 호출
                embeddings_np = EMBEDDER.encode(
                    chunk, 
                    batch_size=len(chunk),
                    convert_to_tensor=False
                )
                
                duration_ms = (time.perf_counter() - start_time) * 1000
                logger.debug(f"배치 #{chunk_index} 성공, 소요={duration_ms:.1f}ms")
                
                # 성공 시 결과 저장 및 루프 탈출
                all_embeddings.extend(embeddings_np.tolist())
                batch_success = True
                break  # 성공했으므로 재시도 루프 탈출
                
            except Exception as e:
                attempt += 1
                if attempt <= MAX_RETRIES:
                    logger.warning(f"배치 #{chunk_index} 처리 중 오류 발생 (시도 {attempt}/{MAX_RETRIES}): {e}. 3초 후 재시도.")
                    time.sleep(3)  # 재시도 전 3초 대기
                else:
                    logger.error(f"배치 #{chunk_index} 최종 실패. 누적 결과 {len(all_embeddings)}건만 반환합니다.")
                    break  # 최종 실패했으므로 재시도 루프 탈출

        # --- 외부 루프: 배치 성공/실패 확인 ---
        if not batch_success:
            # 최종 실패했으므로, 바깥 루프를 종료하고 지금까지의 성공 결과를 반환
            logger.error(f"배치 #{chunk_index}가 {MAX_RETRIES + 1}번의 시도 후에도 실패하여 전체 임베딩 작업을 중단합니다.")
            return all_embeddings
        
        # 성공했으므로 다음 배치로 이동
        i += batch_size

    logger.info(f"전체 {len(texts)}건의 임베딩 성공적으로 생성 완료.")
    return all_embeddings