# 충남콘텐츠진흥원 카드뉴스 자동화 시스템 - 완전 명세서

## 📋 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택 및 아키텍처](#2-기술-스택-및-아키텍처)
3. [핵심 기능 및 워크플로우](#3-핵심-기능-및-워크플로우)
4. [API 통합 및 쿼터 관리](#4-api-통합-및-쿼터-관리)
5. [이미지 생성 워크플로우](#5-이미지-생성-워크플로우)
6. [데이터 구조](#6-데이터-구조)
7. [UI/UX 디자인](#7-uiux-디자인)
8. [스케줄링 시스템](#8-스케줄링-시스템)
9. [테스트 모드](#9-테스트-모드)
10. [배포 및 운영](#10-배포-및-운영)
11. [에러 처리 및 주의사항](#11-에러-처리-및-주의사항)

---

## 1. 프로젝트 개요

### 1.1 목적
충남콘텐츠진흥원 관련 뉴스 기사를 자동으로 수집하고, AI를 활용해 카드뉴스 형식으로 변환하여 이미지 생성을 위한 자료를 제공하는 Streamlit 웹 애플리케이션

### 1.2 주요 기능
- **자동 뉴스 수집**: 네이버 뉴스 Open API를 통한 실시간 뉴스 검색
- **AI 기반 요약**: Google Gemini API를 활용한 기사 요약 생성 (350-450자)
- **카드뉴스 문구 생성**: Google Gemini API를 활용한 8장 카드뉴스 문구 생성
- **이미지 자료 준비**: Iconify 및 Material Icons 벡터 이미지 다운로드 + AI 이미지 생성 프롬프트 제공
- **쿼터 관리**: 여러 Gemini API 키를 순환 사용하며 일일 쿼터 자동 관리
- **기록 관리**: 크롤링 및 배포 기록 저장 및 조회
- **Slack 알림**: 일일 추천 기사를 Slack으로 자동 전송

---

## 2. 기술 스택 및 아키텍처

### 2.1 기술 스택
```
Python 3.13
├── Streamlit (웹 UI 프레임워크)
├── Google Gemini API (AI 텍스트 생성)
├── Naver News Open API (뉴스 검색)
├── Iconify API (벡터 아이콘 검색/다운로드)
├── Material Icons (Google Fonts, 벡터 아이콘)
├── Pillow (이미지 처리, 현재는 사용 안 함)
├── python-dotenv (환경 변수 관리)
├── requests (HTTP 요청)
├── schedule (스케줄링, Railway용)
└── gspread (Google Sheets 연동, 선택사항)
```

### 2.2 프로젝트 구조
```
cardnews_2/
├── app.py                      # 메인 Streamlit 앱 (핵심 파일)
├── daily_fetch.py              # 일일 자동 크롤링 스크립트
├── daily_fetch_scheduler.py    # Railway 스케줄러
├── history_manager.py          # 기록 관리 모듈
├── google_sheets_manager.py    # 구글 시트 연동 모듈 (선택사항)
├── requirements.txt            # Python 의존성
├── .env                        # 환경 변수 (Git에 커밋 금지)
├── Procfile                    # Railway 배포 설정
├── data/
│   ├── daily_recommendations.json  # 자동 추천 기사
│   ├── gemini_quota.json           # Gemini API 쿼터 관리
│   └── history.json                # 기록 데이터
├── fonts/                      # 한글 폰트 파일들
└── outputs/                    # 생성된 파일 저장 (선택사항)
```

### 2.3 아키텍처 흐름
```
[사용자] 
  ↓
[Streamlit UI (app.py)]
  ├─→ [뉴스 검색] → Naver News API
  ├─→ [요약 생성] → Gemini API (summarize_with_gemini)
  ├─→ [카드뉴스 문구] → Gemini API (generate_cardnews_with_gemini)
  └─→ [이미지 자료] → Iconify API + Material Icons
  ↓
[결과 표시 및 다운로드]
```

---

## 3. 핵심 기능 및 워크플로우

### 3.1 메인 워크플로우

#### 3.1.1 "오늘의 자동 추천 기사" 탭
```
1. 사용자가 "🔄 지금 크롤링" 버튼 클릭
   ↓
2. daily_recommendations.json 파일에서 기사 목록 로드
   (또는 daily_fetch.py가 이미 실행되어 저장된 기사 사용)
   ↓
3. 기사 목록 표시 (제목, 설명, 링크)
   ↓
4. 사용자가 기사 선택
   ↓
5. "원문 요약 생성" 버튼 클릭
   → summarize_with_gemini() 호출
   → Gemini API로 350-450자 요약 생성
   → 요약 결과 표시
   ↓
6. "카드뉴스 문구 생성" 버튼 클릭
   → generate_cardnews_with_gemini() 호출
   → Gemini API로 8장 카드뉴스 문구 생성
   → 문구 결과 표시 (TEST_MODE일 때 편집 가능)
   ↓
7. "카드뉴스 이미지 자료 준비" 버튼 클릭
   → parse_card_script()로 카드 파싱
   → 각 카드의 IMAGE_KEY로 Iconify/Material Icons 검색
   → SVG 파일 다운로드
   → build_card_image_prompt()로 AI 이미지 생성 프롬프트 생성
   → ZIP 파일 생성
   → 결과 표시 및 다운로드 제공
```

#### 3.1.2 "실시간 뉴스 검색" 탭
```
1. 사용자가 검색어 입력 및 "뉴스 검색" 버튼 클릭
   ↓
2. search_naver_news() 호출
   → Naver News Open API로 검색
   → 결과 반환
   ↓
3. 기사 목록 표시
   ↓
4. 이후는 "오늘의 자동 추천 기사"와 동일 (5-7단계)
```

### 3.2 주요 함수 및 역할

#### 3.2.1 뉴스 검색
- **`search_naver_news(keyword, display=50)`**
  - Naver News Open API 호출
  - 반환: `List[Dict]` (title, description, link, pubDate 등)

#### 3.2.2 요약 생성
- **`summarize_with_gemini(news_content, news_title, max_retries=2)`**
  - Gemini API로 기사 요약 생성
  - 목표: 350-450자
  - 여러 API 키 순환 사용
  - 쿼터 관리 포함
  - 반환: `str | None` (요약 텍스트)

#### 3.2.3 카드뉴스 문구 생성
- **`generate_cardnews_with_gemini(news_content, news_title)`**
  - Gemini API로 8장 카드뉴스 문구 생성
  - 형식: `TYPE=cover|HEAD=...|IMAGE_KEY=...`
  - 반환: `str | None` (카드뉴스 스크립트)

#### 3.2.4 카드 파싱
- **`parse_card_script(script: str)`**
  - 카드뉴스 문구를 파싱하여 카드 리스트로 변환
  - 반환: `List[Dict]` (각 카드의 type, head, body, image_key)

#### 3.2.5 이미지 자료 준비
- **`search_iconify_icons(query, limit=3)`**
  - Iconify API로 벡터 아이콘 검색
  - 반환: `List[str]` (아이콘 이름 리스트)

- **`search_material_icons(query, limit=3)`**
  - Material Icons 검색 (Iconify의 material-symbols 사용)
  - 반환: `List[Dict]` (name, svg_url 등)

- **`download_svg(url, filename)`**
  - SVG 파일 다운로드
  - 반환: `Optional[bytes]` (SVG 바이너리)

- **`build_card_image_prompt(card)`**
  - 카드 정보를 바탕으로 AI 이미지 생성 프롬프트 생성
  - Bing Copilot, 나노바나나, ChatGPT 등에 붙여넣기 가능한 형식
  - 반환: `str` (프롬프트 텍스트)

- **`create_images_zip(images, zip_filename)`**
  - 다운로드한 이미지들을 ZIP 파일로 압축
  - 반환: `bytes` (ZIP 바이너리)

---

## 4. API 통합 및 쿼터 관리

### 4.1 Gemini API 쿼터 관리 시스템

#### 4.1.1 다중 API 키 관리
```python
# .env 파일에서 여러 키 로드
GEMINI_API_KEY=키1
GEMINI_API_KEY_2=키2
GEMINI_API_KEY_3=키3
GEMINI_API_KEY_4=키4

# 리스트로 관리 (비어있는 값 제외)
GEMINI_API_KEYS = [key1, key2, key3, key4]  # 비어있지 않은 것만
```

#### 4.1.2 쿼터 관리 파일
- **파일 경로**: `data/gemini_quota.json`
- **구조**:
```json
{
  "key_1": {
    "date": "2024-12-21",
    "count": 15,
    "limit": 20,
    "is_warning": true,
    "is_exceeded": false
  },
  "key_2": {
    "date": "2024-12-21",
    "count": 20,
    "limit": 20,
    "is_warning": true,
    "is_exceeded": true
  }
}
```

#### 4.1.3 쿼터 관리 함수
- **`load_gemini_quota()`**: 쿼터 데이터 로드
- **`save_gemini_quota(quota_data)`**: 쿼터 데이터 저장
- **`reset_daily_quota_if_needed(quota_data)`**: 날짜 변경 시 자동 리셋
- **`check_gemini_quota(key_index)`**: 쿼터 체크 (사용량 증가 없이)
  - 반환: `(current_count, is_warning, is_exceeded)`
- **`increment_gemini_usage(key_index)`**: 사용량 증가
  - 반환: `(current_count, is_warning)`
- **`sync_quota_to_exceeded(key_index)`**: API에서 429 에러 발생 시 쿼터를 초과 상태로 동기화
- **`get_gemini_quota_status()`**: 모든 키의 쿼터 상태 조회
  - 반환: `Dict[str, Dict]` (각 키별 상태)

#### 4.1.4 쿼터 설정
```python
GEMINI_DAILY_LIMIT = 20  # 하루 20회 제한
GEMINI_WARNING_THRESHOLD = 15  # 15회 사용 시 경고
```

#### 4.1.5 키 순환 로직
```python
# 요약 생성 시
for attempt in range(key_count * max_retries):
    key_index = (start_key_index + (attempt // max_retries)) % key_count
    retry_count = attempt % max_retries
    
    try:
        current_key = GEMINI_API_KEYS[key_index]
        genai.configure(api_key=current_key)
        
        # 쿼터 체크
        current_count, is_warning, is_exceeded = check_gemini_quota(key_index)
        
        if is_exceeded:
            continue  # 다음 키로
        
        # API 호출
        response = model.generate_content(...)
        
        # 성공 시 사용량 증가
        increment_gemini_usage(key_index)
        
    except Exception as e:
        # 429 에러 감지
        if "429" in str(e) or "quota" in str(e).lower():
            sync_quota_to_exceeded(key_index)
            start_key_index = (key_index + 1) % key_count
            continue
```

### 4.2 Naver News Open API
- **엔드포인트**: `https://openapi.naver.com/v1/search/news.json`
- **필수 헤더**:
  - `X-Naver-Client-Id`: NAVER_CLIENT_ID
  - `X-Naver-Client-Secret`: NAVER_CLIENT_SECRET
- **파라미터**:
  - `query`: 검색어
  - `display`: 결과 개수 (기본 50, TEST_MODE일 때 1)
  - `sort`: 정렬 방식 (sim: 정확도순, date: 날짜순)

### 4.3 Iconify API
- **엔드포인트**: `https://api.iconify.design/search`
- **파라미터**:
  - `query`: 검색어
  - `limit`: 결과 개수
- **SVG 다운로드**: `https://api.iconify.design/{icon_name}.svg`
- **특징**: API 키 불필요, 무료 사용 가능

### 4.4 Material Icons
- **검색 방법**: Iconify의 `material-symbols:` 프리픽스 사용
- **SVG URL**: `https://api.iconify.design/material-symbols:{icon_name}.svg`
- **특징**: API 키 불필요, 무료 사용 가능

---

## 5. 이미지 생성 워크플로우

### 5.1 현재 구현 방식 (하이브리드)
**직접 이미지 생성이 아닌, 이미지 생성에 필요한 자료를 제공하는 방식**

#### 5.1.1 워크플로우
```
1. 사용자가 "카드뉴스 이미지 자료 준비" 버튼 클릭
   ↓
2. parse_card_script()로 카드 파싱
   ↓
3. 각 카드별로:
   a. IMAGE_KEY 추출
   b. Iconify 아이콘 검색 (최대 3개)
   c. Material Icons 검색 (최대 3개)
   d. SVG 파일 다운로드
   e. build_card_image_prompt()로 AI 이미지 생성 프롬프트 생성
   ↓
4. 모든 다운로드한 이미지를 ZIP 파일로 압축
   ↓
5. UI에 표시:
   - 각 카드별 프롬프트 (복사 가능)
   - 각 카드별 Iconify 아이콘 링크
   - 각 카드별 Material Icons 링크
   - ZIP 다운로드 버튼
   - Canva 작업 가이드
```

### 5.2 카드뉴스 문구 형식
```
1. TYPE=cover | HEAD=충남콘텐츠진흥원, 지역 콘텐츠 산업의 새로운 도약 | IMAGE_KEY=innovation growth success
2. TYPE=program | HEAD=지원 프로그램 운영 | BODY=다양한 콘텐츠 기업을 위한 맞춤형 지원 프로그램을 운영하고 있습니다 | IMAGE_KEY=program support business
3. TYPE=impact | HEAD=성과 및 임팩트 | BODY=지역 콘텐츠 산업의 지속적인 성장을 이끌고 있습니다 | IMAGE_KEY=impact achievement result
4. TYPE=result | HEAD=구체적 성과 | BODY=다양한 프로젝트를 통해 지역 경제 활성화에 기여하고 있습니다 | IMAGE_KEY=result success outcome
5. TYPE=program | HEAD=추가 프로그램 | BODY=음악, 게임, e스포츠 등 다양한 분야를 지원합니다 | IMAGE_KEY=music game esports
6. TYPE=impact | HEAD=지역 파급효과 | BODY=충남 지역 콘텐츠 생태계 조성에 핵심적인 역할을 하고 있습니다 | IMAGE_KEY=ecosystem community region
7. TYPE=closing | HEAD=앞으로의 기대 | BODY=지속적인 지원을 통해 더 큰 성과를 만들어가겠습니다 | IMAGE_KEY=future expectation growth
8. TYPE=closing | HEAD=더 자세한 정보 | BODY=더 자세한 내용은 충남콘텐츠진흥원 홈페이지(www.ccon.kr)를 확인해주세요 | IMAGE_KEY=website homepage visit
```

### 5.3 카드 타입별 디자인 가이드

#### 5.3.1 Cover 카드
- **배경**: 진한 파란색/보라색 계열
- **텍스트 색상**: 흰색
- **레이아웃**: HEAD만 표시 (큰 글씨, 중앙 정렬)

#### 5.3.2 Program/Impact/Result 카드
- **배경**: 밝은 회색/흰색 계열
- **텍스트 색상**: 진한 회색/검정
- **레이아웃**: HEAD (상단, 큰 글씨) + BODY (아래, 중간 글씨)

#### 5.3.3 Closing 카드
- **배경**: 연한 파란색/초록색 계열
- **텍스트 색상**: 진한 회색/검정
- **레이아웃**: HEAD + BODY

### 5.4 AI 이미지 생성 프롬프트 구조
```python
def build_card_image_prompt(card: Dict[str, str]) -> str:
    """
    카드 타입별로 다른 프롬프트 생성
    - 공통: 충남콘텐츠진흥원 브랜드 컬러, 정사각형 비율, SNS 스타일
    - 카드별: TYPE, HEAD, BODY, IMAGE_KEY를 반영한 설명
    """
    # 예시 (Cover 카드)
    return """충남콘텐츠진흥원(충콘진) 브랜드 카드뉴스용 일러스트 한 장을 만든다.
정사각형(1:1) 비율, SNS용 카드뉴스 스타일.

디자인 스타일:
- 브랜드 컬러: #6750A4 (Primary), #625B71 (Secondary)
- 일러스트 스타일: 현대적이고 깔끔한 플랫 디자인
- 여백: 충분한 여백으로 가독성 확보

[커버 카드]
주제: "충남콘텐츠진흥원, 지역 콘텐츠 산업의 새로운 도약"을 한눈에 보여주는 장면.
충남콘텐츠진흥원이 지역 콘텐츠·음악·프로그램을 지원해서 큰 성과를 낸 이미지를 상징적으로 표현한다.
IMAGE_KEY 키워드: innovation growth success"""
```

### 5.5 Canva 작업 가이드
```
#### 1단계: 템플릿 준비
- Canva에서 **1080x1080** 정사각형 템플릿 생성
- 또는 "Instagram Post" 템플릿 사용

#### 2단계: 배경 설정
- 카드 타입에 따라 배경색 선택:
  - **Cover 카드**: 진한 파란색/보라색 계열
  - **Program/Impact/Result 카드**: 밝은 회색/흰색 계열
  - **Closing 카드**: 연한 파란색/초록색 계열

#### 3단계: 텍스트 배치
- **HEAD 텍스트**: 상단 중앙, 큰 글씨 (48pt), 볼드
- **BODY 텍스트**: HEAD 아래, 중간 글씨 (32pt), 일반체
- 텍스트 색상은 배경과 대비되게 선택

#### 4단계: 벡터 이미지 삽입
- 위에서 다운로드한 SVG 파일을 Canva에 업로드
- 적절한 크기로 조정 (카드의 20-30% 정도)
- 텍스트와 겹치지 않게 배치

#### 5단계: 로고 추가
- 충남콘텐츠진흥원 로고를 좌측 상단에 배치
- 크기: 약 200x60px

#### 6단계: 카드 번호 (Cover 제외)
- 원형 배경에 카드 번호 표시 (01, 02, ...)
- 좌측 상단, 로고 아래 배치
```

---

## 6. 데이터 구조

### 6.1 daily_recommendations.json
```json
{
  "date": "2024-12-21",
  "articles": [
    {
      "title": "기사 제목",
      "description": "기사 설명",
      "link": "https://...",
      "pubDate": "2024-12-21T09:00:00+09:00",
      "article_overview": "요약 텍스트 (선택사항)"
    }
  ]
}
```

### 6.2 gemini_quota.json
```json
{
  "key_1": {
    "date": "2024-12-21",
    "count": 15,
    "limit": 20,
    "is_warning": true,
    "is_exceeded": false
  }
}
```

### 6.3 history.json
```json
{
  "crawls": [
    {
      "date": "2024-12-21",
      "keyword": "충남콘텐츠진흥원",
      "article_count": 10,
      "timestamp": "2024-12-21T09:00:00"
    }
  ],
  "deployments": [
    {
      "date": "2024-12-21",
      "article_title": "기사 제목",
      "timestamp": "2024-12-21T10:00:00"
    }
  ]
}
```

### 6.4 카드 객체 구조
```python
{
    "type": "cover",  # cover, program, impact, result, closing
    "head": "카드 제목",
    "body": "카드 본문 (cover 타입은 없음)",
    "image_key": "innovation growth success"  # 영어 키워드 3-5단어
}
```

---

## 7. UI/UX 디자인

### 7.1 Streamlit 페이지 구조
```
app.py
├── 사이드바
│   ├── 쿼터 현황 표시
│   └── 설정 (선택사항)
│
└── 메인 영역
    ├── 탭 1: "오늘의 자동 추천 기사"
    │   ├── 크롤링 버튼
    │   ├── 기사 목록
    │   ├── 원문 요약 생성
    │   ├── 카드뉴스 문구 생성
    │   └── 카드뉴스 이미지 자료 준비
    │
    ├── 탭 2: "실시간 뉴스 검색"
    │   ├── 검색어 입력
    │   ├── 검색 버튼
    │   ├── 기사 목록
    │   └── (이후는 탭 1과 동일)
    │
    └── 탭 3: "기록 보기"
        ├── 크롤링 기록
        └── 배포 기록
```

### 7.2 주요 UI 컴포넌트

#### 7.2.1 쿼터 현황 표시
```python
# 사이드바에 표시
st.sidebar.markdown("### 📊 Gemini API 쿼터 현황")
for key_name, status in quota_status.items():
    remaining = status["remaining"]
    count = status["count"]
    limit = status["limit"]
    is_exceeded = status["is_exceeded"]
    
    if is_exceeded:
        st.sidebar.error(f"**{key_name}**: {count}/{limit}회 사용 (쿼터 초과)")
    elif is_warning:
        st.sidebar.warning(f"**{key_name}**: {count}/{limit}회 사용 (남은 횟수: {remaining}회)")
    else:
        st.sidebar.success(f"**{key_name}**: {count}/{limit}회 사용 (남은 횟수: {remaining}회)")
```

#### 7.2.2 테스트 모드 배너
```python
if TEST_MODE:
    st.info("🧪 **테스트 모드 활성화**: 크롤링 1개만, 원문요약/카드뉴스 문구는 한번만 생성됩니다.")
```

#### 7.2.3 카드뉴스 문구 편집 영역
```python
# TEST_MODE일 때만 편집 가능
edited_script = st.text_area(
    "카드뉴스 문구", 
    card_script, 
    height=400, 
    key=f"script_area_{article_key}",
    disabled=not TEST_MODE  # 테스트 모드일 때만 편집 가능
)
```

#### 7.2.4 이미지 자료 표시
```python
# 각 카드별로 Expander로 표시
with st.expander(f"📋 카드 {card_num}: {card.get('head', '')[:30]}..."):
    # 프롬프트 표시
    st.text_area("프롬프트", card_res["prompt"], height=150)
    
    # Iconify 아이콘
    for icon in card_res["iconify_icons"]:
        st.markdown(f"**{icon['name']}**")
        st.markdown(f"[SVG 다운로드]({icon['url']})")
    
    # Material Icons
    for icon in card_res["material_icons"]:
        st.markdown(f"**{icon['name']}**")
        st.markdown(f"[SVG 다운로드]({icon['url']})")
```

### 7.3 색상 팔레트 (Material Design 3)
- **Primary**: #6750A4
- **Secondary**: #625B71
- **Tertiary**: #7D5260
- **Surface**: #FFFBFE
- **Error**: #BA1A1A

---

## 8. 스케줄링 시스템

### 8.1 일일 자동 크롤링 (daily_fetch.py)

#### 8.1.1 실행 시간
- **크롤링**: 매일 오전 8시 55분 (한국 시간)
- **Slack 알림**: 매일 오전 9시 00분 (한국 시간)

#### 8.1.2 검색 키워드
```python
SEARCH_KEYWORDS = [
    "충남콘텐츠진흥원",
    "충콘진",
    "천안그린스타트업타운",
    "김곡미",
    "충남콘텐츠코리아랩",
    "충남콘텐츠기업지원센터",
    "충남글로벌게임센터",
    "충남음악창작소",
    "충남 e스포츠"
]
```

#### 8.1.3 중복 제거 로직
```python
def remove_duplicate_articles(articles, similarity_threshold=0.90):
    """
    1. 링크 중복 체크
    2. 제목 유사도 체크 (SequenceMatcher 사용)
    3. 본문 키워드 오버랩 체크
    """
    # 유사도 90% 이상이면 중복으로 간주
```

#### 8.1.4 관련도 점수 계산
```python
def calculate_relevance_score(article):
    """
    키워드 매칭 점수 계산
    - 제목에 키워드 포함: +10점
    - 설명에 키워드 포함: +5점
    - 최근 기사일수록 높은 점수
    """
```

#### 8.1.5 Slack 알림 형식
```python
def send_daily_slack_notification():
    """
    daily_recommendations.json을 읽어서
    Slack Block Kit 형식으로 메시지 전송
    """
    # 상위 5개 기사만 전송
    # 각 기사마다:
    # - 제목
    # - 설명
    # - 링크
    # - 요약 (있는 경우)
```

### 8.2 Railway 스케줄러 (daily_fetch_scheduler.py)

#### 8.2.1 Procfile 설정
```
web: streamlit run app.py --server.port $PORT --server.enableCORS false --server.enableXsrfProtection false
worker: python daily_fetch_scheduler.py
```

#### 8.2.2 스케줄 설정
```python
# UTC 시간 기준 (한국 시간 = UTC+9)
schedule.every().day.at("23:55").do(run_daily_fetch)  # 한국 08:55
schedule.every().day.at("00:00").do(run_slack_notification)  # 한국 09:00
```

---

## 9. 테스트 모드

### 9.1 TEST_MODE 활성화
```env
# .env 파일
TEST_MODE=True
```

### 9.2 TEST_MODE 동작

#### 9.2.1 크롤링 제한
```python
if TEST_MODE:
    articles = search_naver_news(keyword, display=1)  # 1개만
else:
    articles = search_naver_news(keyword, display=50)  # 50개
```

#### 9.2.2 요약 생성 제한
```python
if TEST_MODE:
    # 이미 요약이 있고 길이가 충분하면 재생성 안 함
    if article_key in st.session_state:
        existing_summary = st.session_state.get(f"{article_key}_overview")
        if existing_summary and len(existing_summary) > 200:
            # 재생성 안 함
            pass
```

#### 9.2.3 카드뉴스 문구 생성 제한
```python
if TEST_MODE:
    # 이미 문구가 있고 길이가 충분하면 재생성 안 함
    script_key = f"{article_key}_script"
    if script_key in st.session_state:
        existing_script = st.session_state[script_key]
        if existing_script and len(existing_script) > 300:
            # 재생성 안 함
            pass
```

#### 9.2.4 문구 편집 가능
```python
# TEST_MODE일 때만 편집 가능
edited_script = st.text_area(
    "카드뉴스 문구",
    card_script,
    disabled=not TEST_MODE
)

# 수정된 문구 저장
if TEST_MODE and edited_script != card_script:
    st.session_state[script_key] = edited_script
    card_script = edited_script  # 수정된 문구로 업데이트
```

---

## 10. 배포 및 운영

### 10.1 로컬 실행
```bash
# 가상 환경 활성화
source venv/bin/activate

# Streamlit 앱 실행
streamlit run app.py

# 일일 크롤링 실행
python daily_fetch.py

# Slack 알림만 실행
python daily_fetch.py slack-only
```

### 10.2 Railway 배포

#### 10.2.1 필수 파일
- `Procfile`: 프로세스 정의
- `requirements.txt`: Python 의존성
- `.env`: 환경 변수 (Railway 대시보드에서 설정)

#### 10.2.2 환경 변수 설정 (Railway)
```
NAVER_CLIENT_ID=...
NAVER_CLIENT_SECRET=...
GEMINI_API_KEY=...
GEMINI_API_KEY_2=...
GEMINI_API_KEY_3=...
GEMINI_API_KEY_4=...
SLACK_WEBHOOK_URL=...
TEST_MODE=False
```

#### 10.2.3 배포 프로세스
1. GitHub에 코드 푸시
2. Railway에서 GitHub 연동
3. 환경 변수 설정
4. 자동 배포 완료

### 10.3 스케줄링 옵션 비교

#### 10.3.1 PythonAnywhere
- **장점**: 무료 티어, 간단한 설정
- **단점**: 제한적 기능
- **적합도**: ⭐⭐⭐

#### 10.3.2 Railway
- **장점**: 무료 티어, 자동 배포, 스케줄러 지원
- **단점**: 타임존 설정 주의
- **적합도**: ⭐⭐⭐⭐⭐

#### 10.3.3 Cron (로컬)
- **장점**: 완전 무료, 완전한 제어
- **단점**: 시스템이 켜져 있어야 함
- **적합도**: ⭐⭐⭐⭐

---

## 11. 에러 처리 및 주의사항

### 11.1 주요 에러 처리

#### 11.1.1 Gemini API 에러
```python
try:
    response = model.generate_content(...)
except Exception as e:
    error_str = str(e)
    
    # 429 쿼터 초과
    if "429" in error_str or "quota" in error_str.lower():
        sync_quota_to_exceeded(key_index)
        # 다음 키로 전환
        continue
    
    # 기타 에러
    else:
        # 재시도 또는 다음 키로
        if retry_count < max_retries - 1:
            continue
        else:
            # 다음 키로 이동
            continue
```

#### 11.1.2 Naver API 에러
```python
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("items", [])
except requests.exceptions.RequestException as e:
    print(f"Naver API 오류: {e}")
    return []
```

#### 11.1.3 Iconify API 에러
```python
try:
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    return [item["name"] for item in data.get("icons", [])]
except Exception as e:
    print(f"Iconify 아이콘 검색 오류: {e}")
    return []
```

### 11.2 주의사항

#### 11.2.1 들여쓰기 규칙
- **Python 표준**: 4칸 공백 사용
- **중첩 블록**: 각 블록마다 4칸씩 추가
- **주의**: 탭과 공백 혼용 금지

#### 11.2.2 try-except 블록 구조
```python
# 올바른 구조
try:
    # 코드 블록 (들여쓰기 필수)
    response = model.generate_content(...)
    # ...
except Exception as e:
    # 에러 처리 (들여쓰기 필수)
    print(f"에러: {e}")
```

#### 11.2.3 세션 상태 관리
```python
# Streamlit 세션 상태 사용
if article_key not in st.session_state:
    st.session_state[article_key] = {}

# 값 저장
st.session_state[f"{article_key}_script"] = card_script

# 값 불러오기
card_script = st.session_state.get(f"{article_key}_script", "")
```

#### 11.2.4 파일 경로 처리
```python
# 절대 경로 사용 권장
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
QUOTA_FILE = os.path.join(DATA_DIR, "gemini_quota.json")

# 디렉토리 생성
os.makedirs(DATA_DIR, exist_ok=True)
```

### 11.3 코드 품질 관리

#### 11.3.1 포맷팅 도구
- **black**: 코드 포맷팅 (권장)
- **autopep8**: PEP 8 준수 자동 수정

#### 11.3.2 사용 방법
```bash
# black 사용 (문법 오류 없을 때만)
black app.py --line-length 120

# autopep8 사용 (문법 오류 있을 때도 시도)
autopep8 --in-place --aggressive --aggressive app.py
```

#### 11.3.3 문법 검사
```bash
python3 -m py_compile app.py
```

---

## 12. 핵심 구현 체크리스트

### 12.1 필수 구현 사항
- [ ] 환경 변수 로드 (.env)
- [ ] Gemini API 다중 키 관리
- [ ] 쿼터 관리 시스템 (JSON 파일 기반)
- [ ] Naver News API 연동
- [ ] 요약 생성 함수 (350-450자)
- [ ] 카드뉴스 문구 생성 함수 (8장 형식)
- [ ] 카드 파싱 함수
- [ ] Iconify 아이콘 검색/다운로드
- [ ] Material Icons 검색/다운로드
- [ ] AI 이미지 생성 프롬프트 생성
- [ ] ZIP 파일 생성
- [ ] Streamlit UI 구성
- [ ] TEST_MODE 구현
- [ ] 일일 크롤링 스크립트
- [ ] Slack 알림 기능

### 12.2 권장 구현 사항
- [ ] 에러 로깅 시스템
- [ ] 재시도 로직 (exponential backoff)
- [ ] 캐싱 시스템 (API 호출 최소화)
- [ ] 사용자 피드백 수집
- [ ] 성능 모니터링

---

## 13. 새로 만들 때 주의할 점

### 13.1 코드 구조 권장사항
1. **함수 분리**: 각 기능을 독립적인 함수로 분리
2. **에러 처리**: 모든 API 호출에 try-except 추가
3. **타입 힌트**: 함수 시그니처에 타입 명시
4. **주석**: 복잡한 로직에 주석 추가
5. **일관된 들여쓰기**: 4칸 공백 사용, 탭 금지

### 13.2 테스트 전략
1. **단위 테스트**: 각 함수별 테스트
2. **통합 테스트**: 전체 워크플로우 테스트
3. **에러 시나리오 테스트**: API 실패, 쿼터 초과 등

### 13.3 성능 최적화
1. **API 호출 최소화**: 캐싱 활용
2. **비동기 처리**: 가능한 경우 async/await 사용
3. **배치 처리**: 여러 작업을 한 번에 처리

---

## 14. 환경 변수 전체 목록

```env
# 네이버 뉴스 API
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# Google Gemini API (최대 4개)
GEMINI_API_KEY=your_gemini_api_key_1
GEMINI_API_KEY_2=your_gemini_api_key_2
GEMINI_API_KEY_3=your_gemini_api_key_3
GEMINI_API_KEY_4=your_gemini_api_key_4

# Slack Webhook (선택사항)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# 테스트 모드
TEST_MODE=False  # True로 설정 시 테스트 모드 활성화

# Google Sheets API (선택사항)
GOOGLE_SHEETS_CREDENTIALS_JSON='{"type":"service_account",...}'
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
```

---

## 15. 완성된 시스템의 최종 목표

1. **자동화**: 매일 자동으로 뉴스 수집 및 추천
2. **효율성**: API 쿼터를 효율적으로 관리하여 최대한 활용
3. **사용자 친화적**: 간단한 UI로 누구나 사용 가능
4. **확장성**: 새로운 기능 추가가 쉬운 구조
5. **안정성**: 에러 발생 시에도 시스템이 계속 동작

---

## 16. 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Naver News Open API 문서](https://developers.naver.com/docs/serviceapi/search/news/news.md)
- [Iconify API 문서](https://iconify.design/docs/api/)
- [Material Icons](https://fonts.google.com/icons)
- [Railway 문서](https://docs.railway.app/)

---

**이 명세서를 기반으로 Cursor AI를 사용하여 깔끔하고 안정적인 새 버전을 만들 수 있습니다.**

