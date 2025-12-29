"""카드뉴스 문구 파싱 모듈 - JSON 형식 지원"""
from typing import Dict, List
import json
import re


def parse_card_script(script: str) -> List[Dict[str, str]]:
    """
    카드뉴스 문구를 파싱하여 카드 리스트로 변환합니다.
    
    지원 형식:
    1. JSON 배열 형식 (새 형식):
       [{"slide_number": 1, "headline": "...", "description": "...", "image_keyword": "..."}]
    
    2. 기존 텍스트 형식 (하위 호환):
       1. TYPE=cover | HEAD=제목 | IMAGE_KEY=keyword1 keyword2 keyword3
    
    Args:
        script: 카드뉴스 문구 텍스트 (JSON 또는 텍스트 형식)
        
    Returns:
        카드 리스트. 각 카드는 {"type", "head", "body", "image_key"} 키를 가집니다.
        (JSON 형식의 경우 slide_number, headline, description, image_keyword를 변환)
    """
    script = script.strip()
    
    # JSON 형식인지 확인
    if script.startswith("[") or script.startswith("{"):
        try:
            # JSON 파싱 시도
            json_data = json.loads(script)
            if isinstance(json_data, list):
                cards = []
                for item in json_data:
                    card: Dict[str, str] = {
                        "type": "",  # JSON 형식에는 type이 없으므로 빈 문자열
                        "head": item.get("headline", ""),
                        "body": item.get("description", ""),
                        "image_key": item.get("image_keyword", ""),
                    }
                    if card["head"]:  # headline이 있으면 유효한 카드로 간주
                        cards.append(card)
                return cards
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 기존 텍스트 형식으로 처리
            pass
    
    # 기존 텍스트 형식 파싱 (하위 호환)
    cards = []
    lines = script.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line or not re.match(r"^\d+\.", line):
            continue
        
        # 번호 제거 (예: "1. " 제거)
        line = re.sub(r"^\d+\.\s*", "", line)
        
        # TYPE, HEAD, BODY, IMAGE_KEY 추출
        card: Dict[str, str] = {
            "type": "",
            "head": "",
            "body": "",
            "image_key": "",
        }
        
        # 파이프(|)로 구분된 부분들 파싱
        parts = [p.strip() for p in line.split("|")]
        
        for part in parts:
            if part.startswith("TYPE="):
                card["type"] = part.replace("TYPE=", "").strip()
            elif part.startswith("HEAD="):
                card["head"] = part.replace("HEAD=", "").strip()
            elif part.startswith("BODY="):
                card["body"] = part.replace("BODY=", "").strip()
            elif part.startswith("IMAGE_KEY="):
                card["image_key"] = part.replace("IMAGE_KEY=", "").strip()
        
        # 최소한 type과 head는 있어야 유효한 카드로 간주
        if card["type"] and card["head"]:
            cards.append(card)
    
    return cards

