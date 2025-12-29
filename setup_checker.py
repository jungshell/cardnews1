"""환경 설정 점검 모듈"""
import os
from typing import Dict, List


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
REQUIRED_ENV_VARS = [
    "NAVER_CLIENT_ID",
    "NAVER_CLIENT_SECRET",
    "GEMINI_API_KEY",
]


def check_environment() -> Dict[str, List[str]]:
    """
    필수 환경 변수와 디렉터리 존재 여부를 점검합니다.
    
    Returns:
        {
            "missing_env": 누락된 환경 변수 리스트,
            "missing_dirs": 누락된 디렉터리 리스트
        }
    """
    missing_env: List[str] = []
    for key in REQUIRED_ENV_VARS:
        if not os.getenv(key):
            missing_env.append(key)

    missing_dirs: List[str] = []
    for path in [DATA_DIR]:
        if not os.path.exists(path):
            missing_dirs.append(path)

    return {
        "missing_env": missing_env,
        "missing_dirs": missing_dirs,
    }


