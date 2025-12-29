"""크롤링 기록 관리 모듈"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

os.makedirs(DATA_DIR, exist_ok=True)


def _load_history() -> Dict[str, Any]:
    """
    크롤링 기록 파일을 로드합니다.
    
    Returns:
        크롤링 기록 딕셔너리. 파일이 없으면 빈 구조 반환.
    """
    if not os.path.exists(HISTORY_FILE):
        return {"crawls": [], "deployments": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[기록 로드 오류] {e}")
        return {"crawls": [], "deployments": []}


def _save_history(data: Dict[str, Any]) -> None:
    """
    크롤링 기록을 파일에 저장합니다.
    
    Args:
        data: 저장할 기록 딕셔너리
    """
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[기록 저장 오류] {e}")


def add_crawl_history(keyword: str, article_count: int) -> None:
    """
    크롤링 기록을 추가합니다.
    
    Args:
        keyword: 검색 키워드
        article_count: 발견된 기사 개수
    """
    data = _load_history()
    data.setdefault("crawls", [])
    data["crawls"].append(
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "keyword": keyword,
            "article_count": article_count,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )
    _save_history(data)


def get_crawl_history(limit: int = 50) -> List[Dict[str, Any]]:
    """
    크롤링 기록을 조회합니다.
    
    Args:
        limit: 최대 반환 개수 (기본 50)
        
    Returns:
        크롤링 기록 리스트 (최신순)
    """
    data = _load_history()
    return list(reversed(data.get("crawls", [])))[:limit]


