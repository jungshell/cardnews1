"""기사 원문에서 전체 제목 추출 모듈"""
import re
from typing import Optional
import requests
from bs4 import BeautifulSoup
from logger import logger


def _clean_title(title: str) -> str:
    """
    제목에서 불필요한 부분을 제거합니다.
    
    Args:
        title: 원본 제목
        
    Returns:
        정리된 제목
    """
    # "< 문화 < 충남 < 전국 < 기사본문" 같은 패턴 제거
    title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*<\s*기사본문.*$", "", title)
    title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*$", "", title)  # "< 문화 < 충남 < 전국" 같은 패턴
    title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*$", "", title)  # "< 대전·충청 < 지역" 같은 패턴
    title = re.sub(r"\s*<\s*[^<]*$", "", title)  # "< 문화" 같은 패턴
    # " | 언론사명" 같은 패턴 제거
    title = re.sub(r"\s*\|\s*.*$", "", title)
    title = re.sub(r"\s*-\s*.*$", "", title)
    return title.strip()


def extract_full_title_from_url(url: str) -> Optional[str]:
    """
    기사 원문 URL에서 전체 제목을 추출합니다.
    
    Args:
        url: 기사 원문 URL
        
    Returns:
        전체 제목. 실패 시 None.
    """
    if not url:
        return None
    
    try:
        # User-Agent 설정 (일부 사이트에서 차단 방지)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        resp = requests.get(url, headers=headers, timeout=5)  # 타임아웃 5초로 단축
        resp.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 1. <title> 태그에서 추출 시도
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text().strip()
            # 불필요한 부분 제거 (예: " | 언론사명", "< 문화 < 충남 < 전국 < 기사본문")
            title = re.sub(r"\s*\|\s*.*$", "", title)
            title = re.sub(r"\s*-\s*.*$", "", title)
            title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*<\s*기사본문.*$", "", title)
            title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*$", "", title)  # "< 문화 < 충남 < 전국" 같은 패턴
            title = re.sub(r"\s*<\s*[^<]*<\s*[^<]*$", "", title)  # "< 대전·충청 < 지역" 같은 패턴
            title = re.sub(r"\s*<\s*[^<]*$", "", title)  # "< 문화" 같은 패턴
            if title and len(title) > 10:  # 너무 짧으면 다른 방법 시도
                return _clean_title(title)
        
        # 2. Open Graph 태그에서 추출 시도
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title.get("content").strip()
            if title:
                return _clean_title(title)
        
        # 3. 기사 제목 클래스/ID로 추출 시도 (주요 언론사 패턴)
        title_selectors = [
            "h1.article-title",
            "h1.title",
            ".article-title",
            ".title",
            "#articleTitle",
            ".article_headline",
            ".headline",
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title and len(title) > 10:
                    return _clean_title(title)
        
        # 4. <h1> 태그에서 추출 시도
        h1_tag = soup.find("h1")
        if h1_tag:
            title = h1_tag.get_text().strip()
            if title and len(title) > 10:
                return _clean_title(title)
        
        return None
        
    except Exception as e:
        logger.warning(f"[제목 추출 오류] {url}: {e}")
        return None

