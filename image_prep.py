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


def _get_card_base_info(card: Dict[str, str]) -> Dict[str, str]:
    """카드 공통 정보(타입/헤드/바디/이미지 키)를 정리합니다."""
    card_type = card.get("type", "").lower()
    head = card.get("head", "").strip()
    body = card.get("body", "").strip()
    image_key = card.get("image_key", "").strip()
    return {
        "type": card_type,
        "head": head,
        "body": body,
        "image_key": image_key,
    }


def _build_copilot_prompt(card: Dict[str, str]) -> str:
    """Copilot / Bing(DALL·E)에서 사용하기 좋은 설명형 프롬프트."""
    info = _get_card_base_info(card)
    card_type = info["type"]
    head = info["head"]
    body = info["body"]
    image_key = info["image_key"]

    type_comment = ""
    if card_type == "cover":
        type_comment = "커버 슬라이드답게 시선을 사로잡는 강렬한 구도와 감정적인 분위기로 표현해줘."
    elif card_type == "program":
        type_comment = "프로그램/현장 활동이 잘 보이도록 사람들의 활동 장면을 중심으로 표현해줘."
    elif card_type in {"impact", "result"}:
        type_comment = "성과와 변화를 느낄 수 있도록 상장, 그래프, 축하 분위기 등을 적절히 섞어줘."
    elif card_type == "closing":
        type_comment = "홈페이지 방문이나 정보 탐색을 떠올릴 수 있는 화면, 모바일, 웹 페이지 이미지를 포함해줘."

    prompt = f"""당신은 인스타그램 카드뉴스용 일러스트 이미지를 만드는 디자이너입니다.

조건:
- flat illustration, minimal, clean design
- brand colors #6750A4 and #625B71를 메인으로 사용
- 정사각형 1:1 비율 (instagram card news)
- 이미지 안에는 텍스트를 넣지 마세요 (no text on image)
- 사진 느낌보다는 일러스트/그래픽 느낌

장면 설명:
{image_key or "충남콘텐츠진흥원 관련 장면"},
충남콘텐츠진흥원과 관련된 장면,
{card_type or "card"} 슬라이드 내용에 맞게 상황을 그려줘.

슬라이드 정보:
- 슬라이드 유형(TYPE): {card_type or "-"}   (cover / program / impact / result / closing 중 하나)
- 제목(HEAD): {head or "-"}
- 내용(BODY): {body or "-"}

추가 지시:
{type_comment}"""

    return prompt.strip()


def _build_gemini_prompt(card: Dict[str, str]) -> str:
    """Google Gemini 이미지 생성에 맞춘 구조화 프롬프트."""
    info = _get_card_base_info(card)
    card_type = info["type"]
    head = info["head"]
    body = info["body"]
    image_key = info["image_key"]

    type_comment = ""
    if card_type == "cover":
        type_comment = "Type이 cover라서, 메시지를 직관적으로 상징하는 한 가지 강한 메타포를 사용해 주세요."
    elif card_type == "program":
        type_comment = "Type이 program이라서, 사람들의 활동과 현장을 중심으로 보여 주세요."
    elif card_type in {"impact", "result"}:
        type_comment = "Type이 impact/result라서, 성과와 변화를 시각적으로 드러내 주세요."
    elif card_type == "closing":
        type_comment = "Type이 closing이라서, 홈페이지 방문/정보 탐색을 연상시키는 구도로 구성해 주세요."

    prompt = f"""역할:
- 당신은 인스타그램 카드뉴스를 위한 일러스트 이미지를 설계하는 아트 디렉터입니다.

목표:
- 아래 카드뉴스 슬라이드 정보를 바탕으로, 시리즈 카드뉴스에 어울리는 단일 이미지를 만듭니다.

스타일:
- flat illustration, minimal, clean design
- brand colors #6750A4 and #625B71
- soft lighting, friendly mood
- square 1:1, high resolution
- no text inside the image, no logo, no watermark

슬라이드 정보:
- Type: {card_type or "-"} (cover / program / impact / result / closing)
- Head: {head or "-"}
- Body: {body or "-"}
- Image key: {image_key or "-"}

요청:
- 위 정보를 바탕으로, 카드뉴스 한 장에 사용할 이미지를 한 장 만들어 주세요.
- {type_comment or "슬라이드 타입에 맞게 장면의 구도와 분위기를 조정해 주세요."}"""

    return prompt.strip()


def _build_local_prompt(card: Dict[str, str]) -> str:
    """Stable Diffusion / 로컬 모델용 키워드 기반 프롬프트."""
    info = _get_card_base_info(card)
    card_type = info["type"] or "card"
    head = info["head"]
    image_key = info["image_key"] or "modern illustration"

    # TYPE을 영어 느낌으로 간단히 변환
    type_en = {
        "cover": "attention-grabbing cover",
        "program": "program scene",
        "impact": "impact scene",
        "result": "result scene",
        "closing": "closing scene with website or screen",
    }.get(card_type, f"{card_type} slide")

    prompt = (
        f"{image_key}, "
        f"chungnam content agency, korea, modern office, people collaborating, "
        f"{type_en} of instagram card news about \"{head}\", "
        "flat illustration, minimal, clean vector, soft lighting, "
        "brand colors #6750A4 and #625B71, high detail, smooth shapes, "
        "no text, no logo, no watermark, square 1:1"
    )

    return prompt


def build_card_image_prompt(card: Dict[str, str], mode: str = "copilot") -> str:
    """
    카드 정보를 바탕으로 AI 이미지 생성 프롬프트를 생성합니다.

    Args:
        card: 카드 정보 (type, head, body, image_key 포함)
        mode: 프롬프트 모드 ("copilot", "gemini", "local")

    Returns:
        프롬프트 텍스트
    """
    mode = (mode or "copilot").lower()
    if mode == "gemini":
        return _build_gemini_prompt(card)
    if mode in {"local", "stable", "stable_diffusion"}:
        return _build_local_prompt(card)
    # 기본값: Copilot/Bing용 프롬프트
    return _build_copilot_prompt(card)


def build_card_image_prompts(card: Dict[str, str]) -> Dict[str, str]:
    """
    카드에 대해 플랫폼별 프롬프트 세트를 생성합니다.

    Returns:
        {
            "copilot": ...,
            "gemini": ...,
            "local": ...,
        }
    """
    return {
        "copilot": build_card_image_prompt(card, mode="copilot"),
        "gemini": build_card_image_prompt(card, mode="gemini"),
        "local": build_card_image_prompt(card, mode="local"),
    }


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
            # 기본값은 Copilot/Bing용 프롬프트
            "prompt": build_card_image_prompt(card, mode="copilot"),
            "prompts": build_card_image_prompts(card),
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
            "prompt": build_card_image_prompt(card, mode="copilot"),
            "prompts": build_card_image_prompts(card),
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
        "prompt": build_card_image_prompt(card, mode="copilot"),
        "prompts": build_card_image_prompts(card),
        "iconify_icons": iconify_results,
        "material_icons": material_results,
        "iconify_downloaded": iconify_downloaded,
        "material_downloaded": material_downloaded,
    }

