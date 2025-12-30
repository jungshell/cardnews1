"""일일 자동 크롤링 스크립트"""
import os
import sys
import time
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List

import requests
from dotenv import load_dotenv

from daily_recommendations import load_daily_recommendations, save_daily_recommendations
from history_manager import add_crawl_history
from logger import logger
from naver_api import search_naver_news
from title_extractor import extract_full_title_from_url


# 검색 키워드 목록
# ※ 사용자 요청으로 "충남콘텐츠", "충남 콘텐츠"는 제외
SEARCH_KEYWORDS = [
    "충남콘텐츠진흥원",
    "충콘진",
    "천안그린스타트업타운",
    "김곡미",
    "충남콘텐츠코리아랩",
    "충남콘텐츠기업지원센터",
    "충남글로벌게임센터",
    "충남음악창작소",
    "충남 e스포츠",
]


def _normalize_title(title: str) -> str:
    """
    제목을 정규화하여 비교하기 쉽게 만듭니다.
    
    Args:
        title: 원본 제목
        
    Returns:
        정규화된 제목
    """
    import re
    # 소문자 변환
    normalized = title.lower()
    # 공백, 특수문자 제거
    normalized = re.sub(r'[·\s\-·,，]', '', normalized)
    # 유사한 표현 통일
    normalized = normalized.replace('성료', '완료').replace('마무리', '완료')
    normalized = normalized.replace('성공적', '').replace('성공', '')
    normalized = normalized.replace('한국청소년육성회', '청소년육성회')
    normalized = normalized.replace('지역인프라연계', '').replace('인프라연계', '')
    # 추가 정규화: 유사 표현 통일
    normalized = normalized.replace('융복합', '융합').replace('융·복합', '융합')
    normalized = normalized.replace('콘텐츠', '콘텐츠')
    return normalized


def remove_duplicate_articles(articles: List[Dict], similarity_threshold: float = 0.85) -> List[Dict]:
    """
    중복 기사를 제거합니다.
    
    Args:
        articles: 기사 리스트
        similarity_threshold: 제목 유사도 임계값 (기본 0.85)
        
    Returns:
        중복이 제거된 기사 리스트
    """
    if not articles:
        return []
    
    seen_links = set()
    seen_originallinks = set()
    unique_articles = []
    
    for article in articles:
        link = article.get("link", "")
        originallink = article.get("originallink", "")
        title = article.get("title", "").strip()
        
        # 1. 링크 중복 체크 (link와 originallink 모두 체크) - 가장 확실한 중복 체크
        if link in seen_links:
            continue
        if originallink and originallink in seen_originallinks:
            continue
        
        # 2. 제목이 너무 짧으면 스킵 (유효하지 않은 기사)
        if len(title) < 10:
            continue
        
        # 3. 정규화된 제목으로 중복 체크
        normalized_title = _normalize_title(title)
        is_duplicate = False
        
        for existing in unique_articles:
            existing_title = existing.get("title", "").strip()
            if not existing_title:
                continue
            
            # 정확히 같은 제목이면 중복
            if title == existing_title:
                logger.debug(f"중복 제거: 정확히 같은 제목 - '{title}'")
                is_duplicate = True
                break
            
            # 정규화된 제목 비교
            existing_normalized = _normalize_title(existing_title)
            if normalized_title == existing_normalized:
                logger.info(f"중복 제거: 정규화 후 동일 - '{title}' vs '{existing_title}'")
                is_duplicate = True
                break
            
            # 유사도 체크 (정규화된 제목으로)
            similarity = SequenceMatcher(None, normalized_title, existing_normalized).ratio()
            if similarity >= similarity_threshold:
                logger.info(f"중복 제거: 유사도 {similarity:.2f} - '{title}' vs '{existing_title}'")
                is_duplicate = True
                break
        
        if is_duplicate:
            continue
        
        # 4. originallink가 같으면 중복 (가장 확실한 중복 체크)
        if originallink:
            for existing in unique_articles:
                existing_originallink = existing.get("originallink", "")
                if existing_originallink and originallink == existing_originallink:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            seen_links.add(link)
            if originallink:
                seen_originallinks.add(originallink)
            unique_articles.append(article)
    
    return unique_articles


def calculate_relevance_score(article: Dict, keywords: List[str]) -> float:
    """
    기사의 관련도 점수를 계산합니다. (10점 만점)
    
    Args:
        article: 기사 정보
        keywords: 검색 키워드 리스트
        
    Returns:
        관련도 점수 (0.0 ~ 10.0, 높을수록 관련도 높음)
    """
    score = 0.0
    title = article.get("title", "").lower()
    description = article.get("description", "").lower()
    
    # 주요 키워드 (회사명) - 높은 가중치
    main_keywords = ["충남콘텐츠진흥원", "충콘진"]
    other_keywords = [k for k in keywords if k not in main_keywords]
    
    # 1. 제목 매칭 점수 (최대 5점)
    title_score = 0.0
    for keyword in main_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in title:
            title_score += 2.5  # 주요 키워드: 각 2.5점
    
    for keyword in other_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in title:
            title_score += 0.3  # 기타 키워드: 각 0.3점
    
    title_score = min(title_score, 5.0)  # 최대 5점
    score += title_score
    
    # 2. 설명 매칭 점수 (최대 3점)
    desc_score = 0.0
    for keyword in main_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in description:
            desc_score += 1.5  # 주요 키워드: 각 1.5점
    
    for keyword in other_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in description:
            desc_score += 0.2  # 기타 키워드: 각 0.2점
    
    desc_score = min(desc_score, 3.0)  # 최대 3점
    score += desc_score
    
    # 3. 최근 기사 보너스 점수 (최대 2점)
    pub_date = article.get("pubDate", "")
    if pub_date:
        try:
            # ISO 형식 파싱 (예: "2024-12-24T09:00:00+09:00")
            date_str = pub_date.split("T")[0]
            article_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            days_diff = (today - article_date).days
            
            # 최근 4일 이내면 보너스 점수 (4일 전: 0.5점, 당일: 2점)
            if days_diff <= 4:
                bonus = 2.0 - (days_diff * 0.375)  # 0일: 2점, 1일: 1.625점, 2일: 1.25점, 3일: 0.875점, 4일: 0.5점
                score += bonus
        except Exception:
            pass
    
    # 최대 10점으로 제한
    return min(score, 10.0)


def fetch_daily_recommendations() -> List[Dict]:
    """
    여러 키워드로 뉴스를 검색하고, 중복 제거 및 관련도 점수 계산 후 추천 기사를 반환합니다.
    
    Returns:
        추천 기사 리스트 (관련도 점수 내림차순 정렬)
    """
    all_articles = []
    
    logger.info(f"크롤링 시작: {len(SEARCH_KEYWORDS)}개 키워드로 검색")
    
    # 관련도순과 날짜순 모두 검색하여 더 많은 기사 수집
    for keyword in SEARCH_KEYWORDS:
        logger.info(f"키워드 검색 중: {keyword}")
        # 날짜순 검색 (최신 기사)
        articles_date = search_naver_news(keyword, display=100, sort="date")
        all_articles.extend(articles_date)
        logger.info(f"키워드 '{keyword}' (날짜순): {len(articles_date)}개 기사 발견")
        
        # 관련도순 검색 (관련도 높은 기사) - 중복이지만 다른 기사도 포함될 수 있음
        articles_sim = search_naver_news(keyword, display=100, sort="sim")
        all_articles.extend(articles_sim)
        logger.info(f"키워드 '{keyword}' (관련도순): {len(articles_sim)}개 기사 발견")
        
        # API 호출 제한을 고려하여 짧은 대기
        time.sleep(0.1)
    
    logger.info(f"중복 제거 전: {len(all_articles)}개 기사")
    unique_articles = remove_duplicate_articles(all_articles)
    logger.info(f"중복 제거 후: {len(unique_articles)}개 기사 (제거: {len(all_articles) - len(unique_articles)}개)")
    
    # 관련도 점수 계산 (전체 제목 추출 전에 먼저 점수 계산)
    logger.info("관련도 점수 계산 중...")
    scored_articles = []
    for idx, article in enumerate(unique_articles, 1):
        score = calculate_relevance_score(article, SEARCH_KEYWORDS)
        # 10점 만점으로 제한 (혹시 모를 오버플로우 방지)
        score = min(score, 10.0)
        article["relevance_score"] = score
        scored_articles.append(article)
    
    # 관련도 점수 내림차순 정렬
    scored_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    # 상위 기사만 선정 (최대 50개)
    top_articles = scored_articles[:50]
    
    # 상위 기사에만 전체 제목 추출 (크롤링 시간 단축)
    # 상위 20개만 전체 제목 추출 (나머지는 기존 제목 사용)
    logger.info(f"상위 {min(20, len(top_articles))}개 기사의 전체 제목 추출 중...")
    for idx, article in enumerate(top_articles[:20], 1):
        original_link = article.get("originallink") or article.get("link", "")
        if original_link:
            logger.info(f"[{idx}/{min(20, len(top_articles))}] 전체 제목 추출 중: {original_link[:50]}...")
            full_title = extract_full_title_from_url(original_link)
            if full_title:
                article["full_title"] = full_title.strip()
                logger.info(f"  → 전체 제목 추출 성공: {full_title[:50]}...")
            else:
                logger.warning(f"  → 전체 제목 추출 실패, 기존 제목 사용")
    
    logger.info(f"완료: 상위 {len(top_articles)}개 기사 선정")
    
    return top_articles


def _clean_html_tags(text: str) -> str:
    """HTML 태그를 제거하고 텍스트만 반환합니다."""
    import re
    if not text:
        return ""
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # HTML 엔티티 디코딩
    text = text.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ').replace('&#39;', "'").replace('&apos;', "'")
    # 연속된 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _format_date(pub_date: str) -> str:
    """날짜를 한국어 형식으로 변환합니다."""
    if not pub_date:
        return "날짜 정보 없음"
    
    try:
        # ISO 형식 파싱 (예: "2025-12-30T10:30:00+09:00")
        if 'T' in pub_date:
            date_str = pub_date.split('T')[0]
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            dt = datetime.strptime(pub_date, "%Y-%m-%d")
        
        # 한국어 형식: "2025.12.30 (화)"
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        weekday = weekdays[dt.weekday()]
        return f"{dt.strftime('%Y.%m.%d')} ({weekday})"
    except Exception:
        return pub_date


def send_slack_notification(articles: List[Dict]) -> bool:
    """
    Slack으로 일일 추천 기사를 전송합니다.
    
    Args:
        articles: 기사 리스트 (상위 5개만 전송)
        
    Returns:
        전송 성공 여부
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL이 설정되지 않아 Slack 알림을 건너뜁니다.")
        return False
    
    # 상위 5개만 전송
    top_5 = articles[:5]
    
    # Block Kit 형식으로 메시지 구성
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📰 오늘의 추천 기사",
            },
        },
        {
            "type": "divider",
        },
    ]
    
    for idx, article in enumerate(top_5, 1):
        # 기사 정보 추출 및 HTML 태그 제거
        title = _clean_html_tags(article.get("title", ""))
        description = _clean_html_tags(article.get("description", ""))
        link = article.get("link", "")
        score = article.get("relevance_score", 0)
        pub_date = article.get("pubDate", "")
        
        # 날짜 포맷팅
        formatted_date = _format_date(pub_date)
        
        # 요약 정보 가져오기 (캐시에서)
        article_id = link or title
        try:
            from cache_manager import get_cached_summary
            summary = get_cached_summary(article_id)
        except Exception:
            summary = None
        
        # 기사 제목 (제목만 강조)
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{idx}. {title}*",
            },
        })
        
        # 메타 정보 (날짜, 관련도 점수)
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"📅 {formatted_date}  |  📊 관련도: {score:.1f}/10점",
                },
            ],
        })
        
        # 기사 설명 (간략)
        if description:
            desc_short = description[:150] + "..." if len(description) > 150 else description
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": desc_short,
                },
            })
        
        # 요약이 있으면 표시
        if summary:
            # 요약 요약 (너무 길면 잘라내기)
            summary_short = summary[:200] + "..." if len(summary) > 200 else summary
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📄 요약:*\n{summary_short}",
                },
            })
        
        # 버튼들
        buttons = []
        if link:
            buttons.append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "🔗 기사 보기",
                },
                "url": link,
                "action_id": f"view_article_{idx}",
            })
        
        # 카드뉴스 생성 버튼
        slack_app_url = os.getenv("SLACK_APP_URL")
        if slack_app_url:
            # Interactive 버튼 (Slack App 서버로 요청)
            buttons.append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "📄 요약 보기",
                },
                "action_id": f"view_summary_{idx}",
                "value": str(idx),
            })
            
            buttons.append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "📝 카드뉴스 생성",
                },
                "action_id": f"create_cardnews_{idx}",
                "value": str(idx),
            })
        else:
            # 일반 URL 버튼 (Streamlit 앱 링크)
            streamlit_base_url = os.getenv("STREAMLIT_APP_URL", "https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app")
            import urllib.parse
            streamlit_url = f"{streamlit_base_url}?article_url={urllib.parse.quote(link)}" if link else streamlit_base_url
            buttons.append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "📝 카드뉴스 생성",
                },
                "url": streamlit_url,
                "action_id": f"create_cardnews_{idx}",
            })
        
        if buttons:
            blocks.append({
                "type": "actions",
                "elements": buttons,
            })
        
        # 구분선
        if idx < len(top_5):
            blocks.append({"type": "divider"})
    
    payload = {"blocks": blocks}
    
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Slack 알림 전송 완료: {len(top_5)}개 기사")
        return True
    except Exception as e:
        logger.error(f"Slack 알림 전송 실패: {e}")
        return False


def main():
    """메인 실행 함수"""
    # 환경 변수 로드
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    # stdout에도 출력 (Streamlit에서 subprocess 로그를 보기 위해)
    import sys
    def log_and_print(message, level="info"):
        """logger와 stdout 모두에 출력"""
        if level == "info":
            logger.info(message)
            print(message, flush=True)
        elif level == "warning":
            logger.warning(message)
            print(f"[경고] {message}", flush=True)
        elif level == "error":
            logger.error(message)
            print(f"[오류] {message}", flush=True)
        else:
            logger.info(message)
            print(message, flush=True)
    
    # 명령줄 인자 확인
    slack_only = len(sys.argv) > 1 and sys.argv[1] == "slack-only"
    
    if slack_only:
        # Slack 알림만 전송
        log_and_print("Slack 알림만 전송 모드")
        articles = load_daily_recommendations()
        if articles:
            send_slack_notification(articles)
        else:
            log_and_print("daily_recommendations.json 파일이 없습니다.", "error")
    else:
        # 크롤링 실행
        log_and_print("=" * 60)
        log_and_print("일일 자동 크롤링 시작")
        log_and_print("=" * 60)
        
        articles = fetch_daily_recommendations()
        
        if articles:
            # daily_recommendations.json에 저장
            save_daily_recommendations(articles)
            log_and_print(f"저장 완료: {len(articles)}개 기사를 daily_recommendations.json에 저장")
            
            # 크롤링 기록 저장
            add_crawl_history("일일 자동 크롤링", len(articles))
            
            # Slack 알림 전송
            send_slack_notification(articles)
        else:
            log_and_print("추천 기사를 찾을 수 없습니다.", "warning")
    
    log_and_print("=" * 60)
    log_and_print("완료")
    log_and_print("=" * 60)


if __name__ == "__main__":
    main()

