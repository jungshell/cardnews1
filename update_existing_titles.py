"""기존 daily_recommendations.json에 전체 제목 추가 스크립트"""
import json
import os
import re
from title_extractor import extract_full_title_from_url, _clean_title
from logger import logger

DATA_DIR = "data"
RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "daily_recommendations.json")


def update_existing_titles():
    """기존 추천 기사 데이터에 full_title 추가"""
    if not os.path.exists(RECOMMENDATIONS_FILE):
        logger.warning(f"{RECOMMENDATIONS_FILE} 파일이 없습니다.")
        return
    
    # 기존 데이터 로드
    with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data.get("articles", [])
    if not articles:
        logger.info("추가할 기사가 없습니다.")
        return
    
    logger.info(f"총 {len(articles)}개 기사의 전체 제목을 추출합니다...")
    
    updated_count = 0
    for idx, article in enumerate(articles, 1):
        # 기존 full_title이 있으면 정리만 수행
        if article.get("full_title"):
            original_full_title = article.get("full_title", "")
            cleaned_title = _clean_title(original_full_title)
            if cleaned_title != original_full_title:
                article["full_title"] = cleaned_title.strip()
                updated_count += 1
                logger.info(f"[{idx}/{len(articles)}] 제목 정리: {original_full_title[:50]}... → {cleaned_title[:50]}...")
            continue
        
        original_link = article.get("originallink") or article.get("link", "")
        if not original_link:
            logger.warning(f"[{idx}/{len(articles)}] 링크가 없습니다: {article.get('title', '')[:50]}...")
            continue
        
        logger.info(f"[{idx}/{len(articles)}] 전체 제목 추출 중: {original_link[:50]}...")
        full_title = extract_full_title_from_url(original_link)
        
        if full_title:
            # 제목 정리 (불필요한 접미사 제거)
            cleaned_title = _clean_title(full_title)
            article["full_title"] = cleaned_title.strip()
            updated_count += 1
            logger.info(f"  → 성공: {cleaned_title[:50]}...")
        else:
            logger.warning(f"  → 실패, 기존 제목 유지")
    
    # 업데이트된 데이터 저장
    with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"완료: {updated_count}개 기사의 전체 제목을 추가했습니다.")


if __name__ == "__main__":
    update_existing_titles()

