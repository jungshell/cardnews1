"""일일 추천 기사 관리 모듈"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DAILY_RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "daily_recommendations.json")

os.makedirs(DATA_DIR, exist_ok=True)


def load_daily_recommendations() -> List[Dict]:
    """
    daily_recommendations.json 파일에서 기사 목록을 로드합니다.
    
    Returns:
        기사 리스트. 파일이 없거나 형식이 잘못된 경우 빈 리스트 반환.
    """
    if not os.path.exists(DAILY_RECOMMENDATIONS_FILE):
        return []
    
    try:
        with open(DAILY_RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("articles", [])
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"[daily_recommendations 로드 오류] {e}")
        return []


def save_daily_recommendations(articles: List[Dict], meta: Optional[Dict] = None) -> None:
    """
    daily_recommendations.json 파일에 기사 목록을 저장합니다.
    
    Args:
        articles: 기사 리스트
    """
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "articles": articles,
        "meta": meta or {},
    }
    
    try:
        with open(DAILY_RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[daily_recommendations 저장 오류] {e}")


def get_daily_recommendations_date() -> Optional[str]:
    """
    daily_recommendations.json 파일의 날짜를 반환합니다.
    
    Returns:
        날짜 문자열 (YYYY-MM-DD). 파일이 없으면 None.
    """
    if not os.path.exists(DAILY_RECOMMENDATIONS_FILE):
        return None
    
    try:
        with open(DAILY_RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("date")
    except Exception:
        return None


def load_daily_recommendations_meta() -> Dict:
    """
    daily_recommendations.json 파일의 메타 정보를 반환합니다.
    
    Returns:
        메타 정보 딕셔너리. 없으면 빈 딕셔너리 반환.
    """
    if not os.path.exists(DAILY_RECOMMENDATIONS_FILE):
        return {}
    
    try:
        with open(DAILY_RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("meta", {}) or {}
    except Exception:
        return {}

