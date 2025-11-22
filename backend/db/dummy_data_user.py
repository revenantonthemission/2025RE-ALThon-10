from typing import List
from backend.core.schema import UserProfile  # 타입 힌팅용
from backend.db.dummy_data_list import FULL_DUMMY_DATA  # 옆 파일에서 데이터 가져옴

def get_dummy_users() -> List[UserProfile]:
    """
    dummy_data_list.py에 있는 데이터를 가져와 반환합니다.
    """
    return FULL_DUMMY_DATA