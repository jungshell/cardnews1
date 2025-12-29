"""네이버 뉴스 Open API 모듈"""
import os
import time
from typing import Dict, List

import requests


NAVER_NEWS_URL = "https://openapi.naver.com/v1/search/news.json"
MAX_RETRIES = 3
RETRY_DELAY = 1  # 초


def search_naver_news(keyword: str, display: int = 10, sort: str = "date") -> List[Dict]:
    """
    네이버 뉴스 Open API로 기사 목록을 조회합니다.
    
    Args:
        keyword: 검색 키워드
        display: 반환할 기사 개수 (기본 10, 최대 100)
        sort: 정렬 기준 ("date": 날짜순, "sim": 관련도순)
        
    Returns:
        기사 리스트. 각 기사는 {"title", "link", "description", "pubDate"} 키를 가집니다.
        실패 시 빈 리스트 반환.
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("[네이버 API 오류] NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET이 설정되지 않았습니다.")
        return []

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": keyword,
        "display": min(display, 100),  # 최대 100개로 제한
        "sort": sort,
    }

    # 재시도 로직
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(NAVER_NEWS_URL, headers=headers, params=params, timeout=10)
            
            # HTTP 상태 코드 확인 (성공 여부와 상관없이 로그 출력)
            print(f"[네이버 API] HTTP 상태 코드: {resp.status_code}", flush=True)
            
            if resp.status_code != 200:
                error_text = resp.text[:200]  # 처음 200자만
                print(f"[네이버 API] HTTP 오류 {resp.status_code}: {error_text}", flush=True)
                return []
            
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", [])
            total = data.get("total", 0)  # 전체 검색 결과 수
            print(f"[네이버 API] '{keyword}' 검색 성공: {len(items)}개 기사 반환 (전체: {total}개)", flush=True)
            return items
        except requests.exceptions.Timeout:
            print(f"[네이버 API] 타임아웃 (시도 {attempt + 1}/{MAX_RETRIES})", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except requests.exceptions.HTTPError as e:
            error_text = str(e.response.text)[:200] if hasattr(e, 'response') and e.response else str(e)
            print(f"[네이버 API] HTTP 오류: {e.response.status_code if hasattr(e, 'response') else 'N/A'} {error_text}", flush=True)
            return []  # HTTP 오류는 재시도하지 않음
        except Exception as e:
            print(f"[네이버 API] 오류: {e}", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    
    print(f"[네이버 API] '{keyword}' 검색 실패 (최대 재시도 횟수 초과)", flush=True)
    return []


