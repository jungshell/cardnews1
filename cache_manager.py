"""캐시 관리 모듈 - 요약 및 카드뉴스 문구 캐싱"""
import hashlib
import os
from typing import Optional


BASE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(BASE_DIR, "cache")

os.makedirs(CACHE_DIR, exist_ok=True)


def _make_hash_key(text: str) -> str:
    """
    텍스트를 해시 키로 변환합니다.
    
    Args:
        text: 해시할 텍스트
        
    Returns:
        32자리 16진수 해시 문자열
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:32]


def get_cached_summary(article_id: str) -> Optional[str]:
    """
    기사 ID(또는 URL)을 기반으로 저장된 요약을 반환합니다.
    
    Args:
        article_id: 기사 ID 또는 URL
        
    Returns:
        캐시된 요약 텍스트. 없으면 None.
    """
    key = _make_hash_key(article_id)
    path = os.path.join(CACHE_DIR, f"summary_{key}.txt")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[캐시 읽기 오류] {path}: {e}")
        return None


def save_cached_summary(article_id: str, summary: str) -> None:
    """
    기사 요약을 캐시에 저장합니다.
    
    Args:
        article_id: 기사 ID 또는 URL
        summary: 저장할 요약 텍스트
    """
    key = _make_hash_key(article_id)
    path = os.path.join(CACHE_DIR, f"summary_{key}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(summary)
    except Exception as e:
        print(f"[캐시 저장 오류] {path}: {e}")


def get_cached_script(article_id: str) -> Optional[str]:
    """
    기사 ID(또는 URL)을 기반으로 저장된 카드뉴스 문구를 반환합니다.
    
    Args:
        article_id: 기사 ID 또는 URL
        
    Returns:
        캐시된 카드뉴스 문구 텍스트. 없으면 None.
    """
    key = _make_hash_key(article_id)
    path = os.path.join(CACHE_DIR, f"card_script_{key}.txt")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[캐시 읽기 오류] {path}: {e}")
        return None


def save_cached_script(article_id: str, script: str) -> None:
    """
    카드뉴스 문구를 캐시에 저장합니다.
    
    Args:
        article_id: 기사 ID 또는 URL
        script: 저장할 카드뉴스 문구 텍스트
    """
    key = _make_hash_key(article_id)
    path = os.path.join(CACHE_DIR, f"card_script_{key}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
    except Exception as e:
        print(f"[캐시 저장 오류] {path}: {e}")


