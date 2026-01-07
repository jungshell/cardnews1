# 📢 Slack 채널 정보

## 현재 설정된 Slack 채널

### Webhook URL로 전송되는 채널
- **채널 이름**: `#경영혁신본부-카드뉴스` (이미지에서 확인)
- **설정 위치**: `SLACK_WEBHOOK_URL` 환경 변수

### 채널 확인 방법

#### 방법 1: Webhook URL에서 확인
1. **Streamlit Cloud Secrets** 또는 **로컬 `.env` 파일** 확인
2. `SLACK_WEBHOOK_URL` 값 확인
3. URL 형식: `https://hooks.slack.com/services/T.../B.../...`
4. Slack 워크스페이스에서 **"Incoming Webhooks"** 앱 설정 확인
5. 해당 Webhook이 연결된 채널 확인

#### 방법 2: Slack에서 확인
1. Slack 워크스페이스 접속
2. 왼쪽 사이드바에서 **"앱"** (Apps) 섹션 확인
3. **"Incoming Webhooks"** 앱 찾기
4. 앱 설정에서 연결된 채널 확인

---

## Slack 알림이 전송되는 시점

### 자동 전송
- **매일 오전 9시 (한국 시간)**: GitHub Actions가 크롤링 실행 후 자동 전송
- **크롤링 완료 시**: `daily_fetch.py` 실행 시 자동 전송

### 수동 전송
- **Streamlit 앱에서 크롤링**: 크롤링 완료 후 자동 전송
- **테스트 스크립트 실행**: `python test_slack_notification.py`

---

## Slack 메시지 형식

```
📰 오늘의 추천 기사
─────────────────────

1. [기사 제목]
📅 2025.11.27 (수)  |  📊 관련도: 4.7/10점

[기사 설명...]

📄 요약:
[요약 내용...]

[📄 요약 보기] [📝 카드뉴스 생성]
─────────────────────
```

---

## 채널 변경 방법

### Webhook URL 변경
1. **Slack 워크스페이스** 접속
2. **"Incoming Webhooks"** 앱 설정
3. 새 채널 선택 또는 새 Webhook 생성
4. 새 Webhook URL 복사
5. **Streamlit Cloud Secrets** 또는 **로컬 `.env`**에 업데이트
6. **GitHub Secrets**에도 업데이트 (GitHub Actions용)

---

## 현재 문제

### 슬랙에 2025년 기사가 나오는 이유
- **원인**: GitHub에 오래된 데이터가 있음
- **해결**: 최신 크롤링 실행 후 GitHub에 푸시 필요

### 해결 방법
1. Streamlit 앱에서 **"지금 다시 크롤링하기"** 버튼 클릭
2. 크롤링 완료 후 자동으로 GitHub에 푸시됨
3. Render에서 `/cardnews` 명령어로 최신 기사 확인

