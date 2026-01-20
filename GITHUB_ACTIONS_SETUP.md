# 🤖 GitHub Actions 자동 크롤링 설정 가이드

## 개요
매일 오전 9시(한국 시간)에 자동으로 크롤링을 실행하고, 결과를 슬랙으로 알림을 보내도록 설정합니다.

## 설정 단계

### 1단계: GitHub Secrets 설정

1. **GitHub 저장소 접속**
   - [https://github.com/jungshell/cardnews1](https://github.com/jungshell/cardnews1)

2. **Settings 클릭**
   - 저장소 상단 메뉴에서 "Settings" 클릭

3. **Secrets and variables → Actions 클릭**
   - 왼쪽 메뉴에서 "Secrets and variables" → "Actions" 클릭

4. **New repository secret 클릭**

5. **다음 4개의 Secret 추가:**

   #### Secret 1: NAVER_CLIENT_ID
   - Name: `NAVER_CLIENT_ID`
   - Secret: 네이버 API Client ID (따옴표 없이)
   - 예: `CWSU/BOA4EDMPJ50/0ugraxmV/SDUKFIBZ00INIUK`

   #### Secret 2: NAVER_CLIENT_SECRET
   - Name: `NAVER_CLIENT_SECRET`
   - Secret: 네이버 API Client Secret (따옴표 없이)
   - 예: `QlvJ13ux21jmi`

   #### Secret 3: GEMINI_API_KEY
   - Name: `GEMINI_API_KEY`
   - Secret: Gemini API Key (따옴표 없이)
   - 예: `AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY`

   #### Secret 4: SLACK_WEBHOOK_URL
   - Name: `SLACK_WEBHOOK_URL`
   - Secret: Slack Webhook URL (따옴표 없이)
   - 예: `https://hooks.slack.com/services/REDACTED/REDACTED/REDACTED`

6. **각 Secret 저장**
   - "Add secret" 버튼 클릭

---

### 2단계: Workflow 파일 푸시

코드는 이미 생성되었습니다. 다음 명령어로 푸시하세요:

```bash
cd "/Volumes/Samsung USB/cardnews_3"
git add .github/workflows/daily_crawl.yml
git commit -m "GitHub Actions 자동 크롤링 설정 추가"
git push
```

---

### 3단계: Workflow 활성화 확인

1. **GitHub 저장소 접속**
   - [https://github.com/jungshell/cardnews1](https://github.com/jungshell/cardnews1)

2. **Actions 탭 클릭**
   - 저장소 상단 메뉴에서 "Actions" 클릭

3. **Workflow 확인**
   - 왼쪽 메뉴에서 "Daily Crawl and Slack Notification" 클릭
   - Workflow가 활성화되어 있는지 확인

---

### 4단계: 수동 테스트 (선택)

1. **Actions 탭 → "Daily Crawl and Slack Notification" 클릭**

2. **"Run workflow" 버튼 클릭**
   - 오른쪽 상단의 "Run workflow" 드롭다운 클릭
   - "Run workflow" 버튼 클릭

3. **실행 확인**
   - Workflow 실행이 시작됨
   - 각 단계가 성공적으로 완료되는지 확인
   - 슬랙에 알림이 도착하는지 확인

---

## 스케줄 확인

### 실행 시간
- **매일 오전 9시 (한국 시간)**
- UTC 기준: 매일 0시 (자정)

### 스케줄 형식
```yaml
cron: '0 0 * * *'
```
- `0 0` = 0시 0분 (UTC)
- `* * *` = 매일

---

## 문제 해결

### Workflow가 실행되지 않음
1. **Actions 탭 확인**
   - Workflow가 활성화되어 있는지 확인
   - "Enable workflow" 버튼이 있는지 확인

2. **Secrets 확인**
   - Settings → Secrets and variables → Actions
   - 4개의 Secret이 모두 설정되어 있는지 확인

3. **로그 확인**
   - Actions 탭 → 최신 실행 클릭
   - 오류 메시지 확인

### 슬랙 알림이 오지 않음
1. **SLACK_WEBHOOK_URL 확인**
   - GitHub Secrets에 올바르게 설정되었는지 확인
   - Slack Webhook URL이 유효한지 확인

2. **Workflow 로그 확인**
   - Actions 탭 → 최신 실행 → "Run daily crawl" 단계
   - 오류 메시지 확인

### 크롤링이 실패함
1. **환경 변수 확인**
   - NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 확인
   - GEMINI_API_KEY 확인

2. **로그 확인**
   - Actions 탭 → 최신 실행 → "Run daily crawl" 단계
   - 상세 로그 확인

---

## 수동 실행 방법

언제든지 수동으로 크롤링을 실행할 수 있습니다:

1. **GitHub 저장소 → Actions 탭**
2. **"Daily Crawl and Slack Notification" 클릭**
3. **"Run workflow" 버튼 클릭**
4. **"Run workflow" 확인**

---

## 확인 사항

- [ ] GitHub Secrets에 4개 모두 설정됨
- [ ] Workflow 파일이 푸시됨
- [ ] Actions 탭에서 Workflow 활성화 확인
- [ ] 수동 테스트 성공
- [ ] 슬랙 알림 도착 확인

---

## 다음 단계

모든 설정이 완료되면:
1. 내일 오전 9시에 자동으로 크롤링이 실행됩니다
2. 크롤링 완료 후 슬랙에 알림이 전송됩니다
3. 결과는 `data/daily_recommendations.json`에 저장됩니다

