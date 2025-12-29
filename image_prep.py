"""카드뉴스 이미지 자료 준비 모듈"""
import io
import os
import zipfile
from typing import Dict, List, Optional
import requests


ICONIFY_API_BASE = "https://api.iconify.design"


def search_iconify_icons(query: str, limit: int = 3) -> List[Dict[str, str]]:
    """
    Iconify API로 벡터 아이콘을 검색합니다.
    
    Args:
        query: 검색어 (영어 키워드)
        limit: 최대 결과 개수
        
    Returns:
        아이콘 정보 리스트. 각 항목은 {"name", "url"} 키를 가집니다.
    """
    try:
        resp = requests.get(
            f"{ICONIFY_API_BASE}/search",
            params={"query": query, "limit": limit},
            timeout=5,
        )
        if resp.status_code != 200:
            print(f"[Iconify 검색 오류] {resp.status_code}")
            return []
        
        data = resp.json()
        icons = data.get("icons", [])
        
        results = []
        for icon_name in icons[:limit]:
            # SVG 다운로드 URL 생성
            svg_url = f"{ICONIFY_API_BASE}/{icon_name}.svg"
            results.append({"name": icon_name, "url": svg_url})
        
        return results
    except Exception as e:
        print(f"[Iconify 검색 오류] {e}")
        return []


def search_material_icons(query: str, limit: int = 3) -> List[Dict[str, str]]:
    """
    Material Icons를 Iconify API를 통해 검색합니다.
    
    Args:
        query: 검색어 (영어 키워드)
        limit: 최대 결과 개수
        
    Returns:
        아이콘 정보 리스트. 각 항목은 {"name", "url"} 키를 가집니다.
    """
    try:
        # material-symbols 프리픽스로 검색
        resp = requests.get(
            f"{ICONIFY_API_BASE}/search",
            params={"query": f"material-symbols:{query}", "limit": limit},
            timeout=5,
        )
        if resp.status_code != 200:
            print(f"[Material Icons 검색 오류] {resp.status_code}")
            return []
        
        data = resp.json()
        icons = data.get("icons", [])
        
        results = []
        for icon_name in icons[:limit]:
            # material-symbols 프리픽스가 포함된 경우 그대로 사용
            if icon_name.startswith("material-symbols:"):
                svg_url = f"{ICONIFY_API_BASE}/{icon_name}.svg"
                results.append({"name": icon_name, "url": svg_url})
        
        return results
    except Exception as e:
        print(f"[Material Icons 검색 오류] {e}")
        return []


def download_svg(url: str, max_retries: int = 2) -> Optional[bytes]:
    """
    SVG 파일을 다운로드합니다.
    
    Args:
        url: SVG 파일 URL
        max_retries: 최대 재시도 횟수
        
    Returns:
        SVG 바이너리 데이터. 실패 시 None.
    """
    import time
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 429 and attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
                continue
            return None
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
                continue
        except Exception as e:
            print(f"[SVG 다운로드 오류] {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return None


def build_card_image_prompt(card: Dict[str, str]) -> str:
    """
    카드 정보를 바탕으로 AI 이미지 생성 프롬프트를 생성합니다.
    
    Args:
        card: 카드 정보 (type, head, body, image_key 포함)
        
    Returns:
        프롬프트 텍스트
    """
    card_type = card.get("type", "").lower()
    head = card.get("head", "")
    body = card.get("body", "")
    image_key = card.get("image_key", "")
    
    # 카드 타입별 배경색 가이드
    bg_color_guide = {
        "cover": "진한 파란색/보라색 계열",
        "program": "밝은 회색/흰색 계열",
        "impact": "밝은 회색/흰색 계열",
        "result": "밝은 회색/흰색 계열",
        "closing": "연한 파란색/초록색 계열",
    }
    bg_color = bg_color_guide.get(card_type, "밝은 회색/흰색 계열")
    
    prompt = f"""충남콘텐츠진흥원(충콘진) 브랜드 카드뉴스용 일러스트 한 장을 만든다.
정사각형(1:1) 비율, SNS용 카드뉴스 스타일.

디자인 스타일:
- 브랜드 컬러: #6750A4 (Primary), #625B71 (Secondary)
- 일러스트 스타일: 현대적이고 깔끔한 플랫 디자인
- 여백: 충분한 여백으로 가독성 확보
- 배경: {bg_color}

[카드 타입: {card_type.upper()}]
제목: "{head}"
"""
    
    if body:
        prompt += f'본문: "{body}"\n'
    
    prompt += f"\nIMAGE_KEY 키워드: {image_key}"""
    
    return prompt


def create_images_zip(
    iconify_icons: List[Dict[str, bytes]],
    material_icons: List[Dict[str, bytes]],
    zip_filename: str = "cardnews_images.zip",
) -> bytes:
    """
    다운로드한 이미지들을 ZIP 파일로 압축합니다.
    
    Args:
        iconify_icons: Iconify 아이콘 리스트. 각 항목은 {"name": ..., "data": ...} 형식.
        material_icons: Material Icons 리스트. 각 항목은 {"name": ..., "data": ...} 형식.
        zip_filename: ZIP 파일명
        
    Returns:
        ZIP 파일 바이너리 데이터
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Iconify 아이콘 추가
        for icon in iconify_icons:
            name = icon.get("name", "unknown")
            data = icon.get("data")
            if data:
                zip_file.writestr(f"iconify/{name}.svg", data)
        
        # Material Icons 추가
        for icon in material_icons:
            name = icon.get("name", "unknown")
            data = icon.get("data")
            if data:
                # material-symbols:xxx 형식에서 파일명만 추출
                clean_name = name.replace("material-symbols:", "")
                zip_file.writestr(f"material-icons/{clean_name}.svg", data)
    
    zip_buffer.seek(0)
    return zip_buffer.read()


def prepare_card_images(card: Dict[str, str]) -> Dict:
    """
    카드의 이미지 자료를 준비합니다 (Iconify/Material Icons 검색 + 다운로드 + 프롬프트 생성).
    
    Args:
        card: 카드 정보
        
    Returns:
        {
            "prompt": str,
            "iconify_icons": List[Dict],
            "material_icons": List[Dict],
            "iconify_downloaded": List[Dict],  # 다운로드된 SVG 데이터 포함
            "material_downloaded": List[Dict],  # 다운로드된 SVG 데이터 포함
        }
    """
    image_key = card.get("image_key", "")
    if not image_key:
        return {
            "prompt": build_card_image_prompt(card),
            "iconify_icons": [],
            "material_icons": [],
            "iconify_downloaded": [],
            "material_downloaded": [],
        }
    
    # image_key에서 쉼표로 구분된 키워드 추출
    # 여러 키워드 중 첫 번째 단어만 사용 (Iconify는 단일 단어 검색에 최적화)
    keywords = [k.strip() for k in image_key.replace(",", " ").split() if k.strip()]
    search_query = keywords[0] if keywords else image_key.strip().split()[0] if image_key.strip() else ""
    
    if not search_query:
        return {
            "prompt": build_card_image_prompt(card),
            "iconify_icons": [],
            "material_icons": [],
            "iconify_downloaded": [],
            "material_downloaded": [],
        }
    
    # Iconify 아이콘 검색
    iconify_results = search_iconify_icons(search_query, limit=3)
    
    # Material Icons 검색
    material_results = search_material_icons(search_query, limit=3)
    
    # SVG 다운로드
    iconify_downloaded = []
    for icon in iconify_results:
        svg_data = download_svg(icon["url"])
        if svg_data:
            iconify_downloaded.append({"name": icon["name"], "data": svg_data})
    
    material_downloaded = []
    for icon in material_results:
        svg_data = download_svg(icon["url"])
        if svg_data:
            material_downloaded.append({"name": icon["name"], "data": svg_data})
    
    return {
        "prompt": build_card_image_prompt(card),
        "iconify_icons": iconify_results,
        "material_icons": material_results,
        "iconify_downloaded": iconify_downloaded,
        "material_downloaded": material_downloaded,
    }

