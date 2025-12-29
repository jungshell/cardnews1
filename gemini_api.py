"""Google Gemini API 모듈 - 요약 및 카드뉴스 문구 생성"""
import os
import time
from typing import Optional, List

import requests


GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1"
MAX_RETRIES = 2
RETRY_DELAY = 2  # 초


def _get_available_models() -> List[str]:
    """사용 가능한 모델 목록을 조회합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return []
    
    try:
        resp = requests.get(
            f"{GEMINI_API_BASE}/models",
            params={"key": api_key},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"[모델 목록 조회 실패] {resp.status_code} {resp.text}")
            return []
        
        data = resp.json()
        models = data.get("models", [])
        # generateContent를 지원하는 모델만 필터링
        available = []
        for model in models:
            name = model.get("name", "")
            supported_methods = model.get("supportedGenerationMethods", [])
            if "generateContent" in supported_methods:
                # "models/gemini-1.5-flash" 형식으로 변환
                if name.startswith("models/"):
                    available.append(name)
        
        return available
    except Exception as e:
        print(f"[모델 목록 조회 오류] {e}")
        return []


def _find_working_model() -> Optional[str]:
    """사용 가능한 모델 중 하나를 찾아 반환합니다."""
    available = _get_available_models()
    if not available:
        print("[경고] 사용 가능한 모델을 찾을 수 없습니다.")
        return None
    
    # 우선순위: flash 계열 > pro 계열 > 기타
    for model in available:
        if "flash" in model.lower():
            print(f"[모델 선택] {model}")
            return model
    
    for model in available:
        if "pro" in model.lower():
            print(f"[모델 선택] {model}")
            return model
    
    # 첫 번째 모델 사용
    print(f"[모델 선택] {available[0]}")
    return available[0]


def summarize_with_gemini(news_content: str, news_title: str) -> Optional[str]:
    """기사 내용을 350~450자 한글 요약으로 생성합니다. (직접 REST 호출, v1 엔드포인트 사용)"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return None

    # 사용 가능한 모델 찾기
    model_name = _find_working_model()
    if not model_name:
        print("[오류] 사용 가능한 Gemini 모델을 찾을 수 없습니다.")
        return None

    api_url = f"{GEMINI_API_BASE}/{model_name}:generateContent"

    prompt = (
        "다음 뉴스 기사를 한국어로 자연스럽게 350~450자 사이로 요약해 주세요.\n\n"
        "요약 형식:\n"
        "1. 핵심 키워드(충남콘텐츠진흥원, 충콘진, 충남콘텐츠코리아랩, 충남콘텐츠기업지원센터, 충남글로벌게임센터, 충남음악창작소, 김곡미 등)를 **굵게** 표시하세요.\n"
        "2. 핵심 키워드와 관련된 내용을 중심으로 요약하세요.\n"
        "3. 마지막에 '충남콘텐츠진흥원의 관여도' 섹션을 별도로 추가하여, 진흥원이 이 기사에서 어떤 역할을 했는지, 어떤 사업/프로그램과 관련이 있는지 명확히 설명하세요.\n"
        "4. 중복 표현은 줄이고, 핵심 내용 위주로 정리하세요.\n\n"
        f"[제목]\n{news_title}\n\n[본문]\n{news_content}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    # 재시도 로직
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                api_url,
                params={"key": api_key},
                json=payload,
                timeout=30,
            )
            if resp.status_code == 429:  # Rate limit
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"[Gemini Rate Limit] {wait_time}초 대기 후 재시도...")
                    time.sleep(wait_time)
                    continue
            if resp.status_code != 200:
                print(f"[Gemini HTTP 오류] {resp.status_code} {resp.text}")
                return None

            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                print("[Gemini 응답 경고] candidates가 비어 있습니다.")
                return None

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                print("[Gemini 응답 경고] parts가 비어 있습니다.")
                return None

            return parts[0].get("text", "")
        except requests.exceptions.Timeout:
            print(f"[Gemini 타임아웃] (시도 {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            print(f"[Gemini 호출 오류] {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    
    return None


def generate_cardnews_with_gemini(news_content: str, news_title: str) -> Optional[str]:
    """기사 내용을 바탕으로 8장 카드뉴스 문구를 생성합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return None

    # 사용 가능한 모델 찾기
    model_name = _find_working_model()
    if not model_name:
        print("[오류] 사용 가능한 Gemini 모델을 찾을 수 없습니다.")
        return None

    api_url = f"{GEMINI_API_BASE}/{model_name}:generateContent"

    prompt = (
        "당신은 충남콘텐츠진흥원의 젊고 센스 있는 SNS 홍보 담당자입니다. 아래 뉴스 기사를 읽고, 진흥원의 역할과 성과를 사실에 기반해 카드뉴스 형식으로 정리해 주세요. 독자가 끝까지 읽을 수 있도록 흥미로운 후크와 친근한 말투를 사용하는 것이 핵심입니다.\n\n"
        "⚠️ 절대 규칙:\n"
        "- 반드시 **이 기사 내용만** 사용하세요. 기사에 없는 예산, 인원수, 성과, 기관명 등은 절대 만들어내지 마세요.\n"
        "- '주도했다' 대신 **'지원했다', '참여했다', '협력했다', '추진했다'** 등 사실 기반 동사만 사용하세요.\n"
        "- **불필요한 설명 제거:** (이하 진흥원), 원장 이름, 기사 출처 등은 제외하고 핵심만 전달하세요.\n\n"
        "🎯 톤 & 타겟:\n"
        "- 타겟: 충남콘텐츠진흥원이 무엇을 하는 곳인지 잘 모르는 일반 시민.\n"
        "- 말투: **친구에게 카톡 하듯 매우 친근하고 캐주얼한 구어체.** (\"~했어요!\", \"~이랍니다.\", \"~는요?\", \"~할 거예요.\")\n"
        "- 후크(Hook): 초반 카드(1~3번)에 궁금증을 유발하는 질문이나 감탄사를 넣어 시선을 사로잡으세요.\n\n"
        "--- 1단계) 카드 분할 전략 (분량 엄수)\n"
        "- 기사의 흐름과 맥락에 따라 **최소 6장, 표준 8장, 최대 10장**으로 구성하세요.\n"
        "- 기사 내용이 짧더라도 내용을 세밀하게 쪼개어 가독성을 높이고, 정보를 충분히 풀어서 설명하세요.\n"
        "- **절대로 5장 이하로 끝내지 마세요.**\n\n"
        "- 구성 가이드:\n"
        "  - 1번(Cover): 가장 강력한 후크와 핵심 주제\n"
        "  - 2번(Intro): 기사 배경이나 궁금증 유발 질문\n"
        "  - 중간(Program/Impact/Result): 사업 내용, 지원 과정, 구체적 변화, 성과의 의미를 단계별로 상세히 나열\n"
        "  - 마지막(Closing): 홈페이지 방문 유도 및 친절한 마무리\n\n"
        "--- 2단계) 카드별 문구 작성 규칙\n"
        "- TYPE: cover / program / impact / result / closing 중 선택\n"
        "- HEAD: 12~20자 내외. **질문형, 감탄사 등 후크를 반드시 활용하세요.**\n"
        "- BODY (TYPE=cover 제외):\n"
        "  - **20~40자 내외의 완결된 문장.** (너무 짧거나 길지 않게 유지)\n"
        "  - **절대 \"...\"(줄임표)를 사용하지 마세요.** 문장을 명확하게 끝맺으세요.\n"
        "  - HEAD와 내용이 겹치지 않게 정보를 나누어 담으세요.\n"
        "- IMAGE_KEY: 영어 키워드 2~4단어. (예: \"business meeting\", \"award ceremony\")\n\n"
        "--- 3단계) 형식\n"
        f"기사 원문:\n[제목]\n{news_title}\n\n[본문]\n{news_content}\n\n"
        "위 내용을 바탕으로 아래 형식에 맞춰 한 줄씩 출력하세요. (번호는 1번부터 시작)\n\n"
        "출력 형식:\n"
        "1. TYPE=cover | HEAD=... | IMAGE_KEY=...\n"
        "2. TYPE=program | HEAD=... | BODY=... | IMAGE_KEY=...\n"
        "...\n"
        "N. TYPE=closing | HEAD=더 자세한 내용이 궁금하다면? | BODY=진흥원 홈페이지(https://ccon.kr/)에서 더 많은 정보를 확인해보세요! | IMAGE_KEY=website visit\n\n"
        "**중요:** 반드시 최소 6장 이상 생성하고, 마지막 카드는 항상 closing 타입으로 홈페이지를 유도하세요."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    # 재시도 로직
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                api_url,
                params={"key": api_key},
                json=payload,
                timeout=60,  # 카드뉴스 생성은 시간이 더 걸릴 수 있음
            )
            if resp.status_code == 429:  # Rate limit
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"[Gemini Rate Limit] {wait_time}초 대기 후 재시도...")
                    time.sleep(wait_time)
                    continue
            if resp.status_code != 200:
                print(f"[Gemini HTTP 오류] {resp.status_code} {resp.text}")
                return None

            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                print("[Gemini 응답 경고] candidates가 비어 있습니다.")
                return None

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                print("[Gemini 응답 경고] parts가 비어 있습니다.")
                return None

            return parts[0].get("text", "")
        except requests.exceptions.Timeout:
            print(f"[Gemini 타임아웃] (시도 {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            print(f"[Gemini 호출 오류] {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    
    return None


