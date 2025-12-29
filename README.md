# 충남콘텐츠진흥원 카드뉴스 자동화 시스템

충남콘텐츠진흥원 관련 뉴스를 자동으로 수집하고, AI를 활용하여 카드뉴스 문구와 이미지 자료를 생성하는 웹 애플리케이션입니다.

## 주요 기능

- **실시간 뉴스 검색**: 네이버 뉴스 API를 통한 실시간 기사 검색
- **오늘의 자동 추천 기사**: 일일 자동 크롤링으로 추천 기사 제공
- **AI 기사 요약**: Google Gemini API를 활용한 350~450자 요약 생성
- **카드뉴스 문구 생성**: 8장 형식의 카드뉴스 문구 자동 생성
- **이미지 자료 준비**: Iconify/Material Icons 검색 및 SVG 다운로드
- **Slack 알림**: 일일 추천 기사 자동 알림 (선택사항)

## 기술 스택

- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **뉴스 API**: 네이버 뉴스 Open API
- **아이콘**: Iconify API, Material Icons
- **배포**: Railway (무료 티어)

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd cardnews_3
```

### 2. 가상 환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`env.example` 파일을 복사하여 `.env` 파일을 생성하고, 필요한 값들을 입력하세요:

```bash
cp env.example .env
```

`.env` 파일 내용:

```env
# 네이버 뉴스 Open API 설정
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# Google Gemini API 설정
GEMINI_API_KEY=your_gemini_api_key

# Slack 알림 설정 (선택사항)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 5. API 키 발급

#### 네이버 뉴스 Open API
1. [네이버 개발자 센터](https://developers.naver.com/) 접속
2. 애플리케이션 등록
3. Client ID와 Client Secret 발급

#### Google Gemini API
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. API 키 생성
3. 생성된 키를 `.env` 파일에 입력

#### Slack Webhook (선택사항)
1. Slack 워크스페이스에서 "Incoming Webhooks" 앱 추가
2. Webhook URL 복사
3. `.env` 파일에 입력

### 6. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8502`로 접속하세요.

## 일일 자동 크롤링 실행

### 수동 실행

```bash
python daily_fetch.py
```

### Slack 알림만 전송

```bash
python daily_fetch.py slack-only
```

### 자동 스케줄링 (Railway)

Railway에서 `daily_fetch_scheduler.py`를 worker로 실행하면 자동으로 스케줄링됩니다.

- **크롤링**: 매일 오전 8시 55분 (한국 시간)
- **Slack 알림**: 매일 오전 9시 (한국 시간)

## 프로젝트 구조

```
cardnews_3/
├── app.py                      # Streamlit 메인 애플리케이션
├── daily_fetch.py              # 일일 자동 크롤링 스크립트
├── daily_fetch_scheduler.py    # Railway 스케줄러
├── cache_manager.py            # 캐시 관리 모듈
├── gemini_api.py               # Gemini API 모듈
├── naver_api.py                # 네이버 뉴스 API 모듈
├── card_parser.py              # 카드뉴스 파싱 모듈
├── image_prep.py               # 이미지 자료 준비 모듈
├── daily_recommendations.py    # 일일 추천 기사 관리 모듈
├── history_manager.py          # 크롤링 기록 관리 모듈
├── setup_checker.py            # 환경 설정 점검 모듈
├── logger.py                   # 로깅 시스템 모듈
├── requirements.txt             # Python 의존성
├── Procfile                     # Railway 배포 설정
├── runtime.txt                  # Python 버전 명시
├── .env.example                 # 환경 변수 예시 파일
├── data/                        # 데이터 저장 디렉터리
│   ├── history.json
│   └── daily_recommendations.json
├── cache/                       # 캐시 디렉터리
│   ├── summary_*.txt
│   └── card_script_*.txt
└── logs/                        # 로그 디렉터리
    ├── app_YYYYMMDD.log
    └── error_YYYYMMDD.log
```

## 사용 방법

### 1. 실시간 뉴스 검색

1. "실시간 뉴스 검색" 탭 선택
2. 검색어 입력 (예: "충남콘텐츠진흥원")
3. "뉴스 검색" 버튼 클릭
4. 기사 선택 후 "원문 요약 생성" 또는 "카드뉴스 문구 생성" 버튼 클릭

### 2. 오늘의 자동 추천 기사

1. "오늘의 자동 추천 기사" 탭 선택
2. 정렬 기준 선택 (관련도 점수, 날짜)
3. 기사 제목 클릭하여 상세 정보 확인
4. "원문 요약 생성", "카드뉴스 문구 생성", "카드뉴스 이미지 자료 준비" 버튼 사용

### 3. 기록 보기

"기록 보기" 탭에서 최근 크롤링 기록을 확인할 수 있습니다.

## Railway 배포

### 1. Railway 계정 생성 및 프로젝트 연결

1. [Railway](https://railway.app/) 접속 및 계정 생성
2. "New Project" → "Deploy from GitHub repo" 선택
3. 저장소 연결

### 2. 환경 변수 설정

Railway 대시보드에서 환경 변수를 설정하세요:

- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `GEMINI_API_KEY`
- `SLACK_WEBHOOK_URL` (선택사항)

### 3. 배포 설정

Railway는 `Procfile`을 자동으로 인식합니다:

```
web: streamlit run app.py --server.port $PORT --server.enableCORS false --server.enableXsrfProtection false
worker: python daily_fetch_scheduler.py
```

### 4. 배포 확인

배포 완료 후 제공되는 URL로 접속하여 애플리케이션이 정상 작동하는지 확인하세요.

## 문제 해결

### 환경 변수 오류

`.env` 파일이 올바르게 설정되었는지 확인하세요. `setup_checker.py`가 자동으로 점검합니다.

### API 쿼터 초과

- Gemini API: 무료 티어는 일일 요청 수 제한이 있습니다. 필요시 여러 API 키를 순환 사용하도록 확장 가능합니다.
- 네이버 API: 일일 요청 수 제한이 있습니다. `daily_fetch.py`의 `display` 파라미터를 조정하세요.

### 캐시 문제

캐시 파일은 `cache/` 디렉터리에 저장됩니다. 문제가 발생하면 해당 디렉터리를 삭제하고 다시 시도하세요.

## 라이선스

이 프로젝트는 충남콘텐츠진흥원을 위한 내부 프로젝트입니다.

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

