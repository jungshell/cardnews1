# ✅ 다음 단계: GitHub Actions 설정 완료하기

## 현재 상태
✅ Workflow 파일 생성 완료 (`daily_crawl.yml`)

## 다음 단계

### 1단계: GitHub Secrets 설정 (필수!)

1. **GitHub 저장소 → Settings 탭 클릭**
   - [https://github.com/jungshell/cardnews1/settings](https://github.com/jungshell/cardnews1/settings)

2. **왼쪽 메뉴에서 "Secrets and variables" → "Actions" 클릭**

3. **"New repository secret" 버튼 클릭**

4. **다음 4개의 Secret을 추가:**

   #### Secret 1: NAVER_CLIENT_ID
   - Name: `NAVER_CLIENT_ID`
   - Secret: 네이버 API Client ID
   - 예: `CWSU/BOA4EDMPJ50/0ugraxmV/SDUKFIBZ00INIUK`

   #### Secret 2: NAVER_CLIENT_SECRET
   - Name: `NAVER_CLIENT_SECRET`
   - Secret: 네이버 API Client Secret
   - 예: `QlvJ13ux21jmi`

   #### Secret 3: GEMINI_API_KEY
   - Name: `GEMINI_API_KEY`
   - Secret: Gemini API Key
   - 예: `AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY`

   #### Secret 4: SLACK_WEBHOOK_URL
   - Name: `SLACK_WEBHOOK_URL`
   - Secret: Slack Webhook URL
   - 예: `https://hooks.slack.com/services/REDACTED/REDACTED/REDACTED`

5. **각 Secret 저장**
   - "Add secret" 버튼 클릭

---

### 2단계: Workflow 활성화 확인

1. **Actions 탭 클릭**
   - [https://github.com/jungshell/cardnews1/actions](https://github.com/jungshell/cardnews1/actions)

2. **"Daily Crawl and Slack Notification" workflow 확인**
   - 왼쪽 메뉴에서 확인 가능

3. **활성화 여부 확인**
   - Workflow가 보이면 활성화된 것입니다

---

### 3단계: 수동 테스트 (권장)

1. **Actions 탭 → "Daily Crawl and Slack Notification" 클릭**

2. **"Run workflow" 버튼 클릭** (오른쪽 상단)

3. **"Run workflow" 확인**

4. **실행 확인**
   - Workflow 실행이 시작됨
   - 각 단계가 성공적으로 완료되는지 확인:
     - ✅ Checkout repository
     - ✅ Set up Python
     - ✅ Install dependencies
     - ✅ Run daily crawl
     - ✅ Commit and push results

5. **슬랙 알림 확인**
   - 슬랙에 "📰 오늘의 추천 기사" 메시지가 도착하는지 확인

---

## 실행 시간

- **매일 오전 9시 (한국 시간)**
- UTC 기준: 매일 0시 (자정)

---

## 체크리스트

- [x] Workflow 파일 생성 완료
- [ ] GitHub Secrets에 4개 모두 설정 완료
- [ ] Actions 탭에서 workflow 활성화 확인
- [ ] 수동 테스트 성공
- [ ] 슬랙 알림 도착 확인

---

## 문제 해결

### Secrets 설정이 안 보임
- Settings → Secrets and variables → Actions 경로 확인
- 저장소에 대한 권한이 있는지 확인

### Workflow가 실행되지 않음
- Actions 탭에서 workflow 활성화 확인
- Secrets가 모두 설정되었는지 확인

### 슬랙 알림이 오지 않음
- SLACK_WEBHOOK_URL이 올바른지 확인
- Workflow 로그에서 오류 확인

---

모든 설정이 완료되면 내일 오전 9시부터 자동으로 크롤링이 실행됩니다! 🎉

