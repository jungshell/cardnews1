# Railway 배포 가이드

## 사전 준비

1. Railway 계정 생성: https://railway.app/
2. GitHub 저장소 준비 (또는 Railway CLI 사용)

## 배포 단계

### 1. 프로젝트 연결

#### 방법 A: GitHub 연동
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 저장소 선택 및 연결

#### 방법 B: Railway CLI
```bash
railway login
railway init
railway up
```

### 2. 환경 변수 설정

Railway 대시보드의 "Variables" 탭에서 다음 환경 변수를 설정하세요:

```
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
GEMINI_API_KEY=your_gemini_api_key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. 서비스 설정

Railway는 `Procfile`을 자동으로 인식합니다:

- **web**: Streamlit 애플리케이션 (포트는 자동 할당)
- **worker**: 일일 크롤링 스케줄러

### 4. 배포 확인

1. 배포 완료 후 제공되는 URL로 접속
2. 애플리케이션이 정상 작동하는지 확인
3. 로그에서 에러가 없는지 확인

## 스케줄러 설정

`daily_fetch_scheduler.py`가 worker로 실행되면 자동으로 스케줄링됩니다:

- **크롤링**: 매일 23:55 UTC (한국 시간 08:55)
- **Slack 알림**: 매일 00:00 UTC (한국 시간 09:00)

## 문제 해결

### 포트 오류

Railway는 `$PORT` 환경 변수를 자동으로 제공합니다. `Procfile`에서 올바르게 사용하고 있는지 확인하세요.

### 스케줄러가 작동하지 않음

Railway 대시보드에서 worker 서비스가 실행 중인지 확인하세요. 로그를 확인하여 오류를 확인할 수 있습니다.

### 환경 변수 누락

모든 필수 환경 변수가 설정되었는지 확인하세요. `.env.example` 파일을 참고하세요.

## 무료 티어 제한

Railway 무료 티어는 다음과 같은 제한이 있습니다:

- 월 500시간 실행 시간
- 512MB RAM
- 1GB 디스크 공간

이 제한을 초과하면 유료 플랜으로 업그레이드해야 합니다.


