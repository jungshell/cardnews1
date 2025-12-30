# 🚂 Railway 배포 완벽 가이드

## 현재 상태
- ✅ Slack App 생성 완료
- ✅ Bot Token, Signing Secret 복사 완료
- ⏳ Railway 배포 진행 중

---

## 1단계: Railway 계정 생성 및 로그인

### 1.1 Railway 접속
1. [https://railway.app/](https://railway.app/) 접속
2. **"Login"** 또는 **"Start a New Project"** 버튼 클릭

### 1.2 GitHub로 로그인
1. **"Login with GitHub"** 선택
2. GitHub 계정으로 로그인
3. Railway가 GitHub 저장소에 접근할 수 있도록 권한 승인
   - ✅ **"Authorize Railway"** 클릭

---

## 2단계: 새 프로젝트 생성

### 2.1 프로젝트 시작
1. Railway 대시보드에서 **"New Project"** 버튼 클릭
2. **"Deploy from GitHub repo"** 선택
   - (또는 **"Deploy from GitHub"**)

### 2.2 저장소 선택
1. GitHub 저장소 목록이 표시됩니다
2. `jungshell/cardnews1` 저장소 찾기
3. 저장소 클릭하여 선택

### 2.3 배포 시작
1. **"Deploy Now"** 또는 **"Add"** 버튼 클릭
2. Railway가 자동으로 저장소를 클론하고 배포를 시작합니다
   - ⏳ 약 2-3분 소요

---

## 3단계: 서비스 설정

### 3.1 서비스 확인
배포가 시작되면:
1. 왼쪽에 서비스가 생성됩니다 (예: `cardnews1`)
2. 서비스 클릭하여 상세 페이지로 이동

### 3.2 Start Command 설정
1. 서비스 페이지에서 **"Settings"** 탭 클릭
2. **"Deploy"** 섹션으로 스크롤
3. **"Start Command"** 입력란 찾기
4. 다음 명령어 입력:
   ```
   python slack_app.py
   ```
5. **"Save"** 버튼 클릭

### 3.3 포트 설정 (자동)
- Railway는 자동으로 `PORT` 환경 변수를 설정합니다
- `slack_app.py`가 이미 `PORT` 환경 변수를 사용하도록 설정되어 있음
- 추가 설정 불필요

---

## 4단계: 환경 변수 설정 (중요!)

### 4.1 Variables 탭 열기
1. 서비스 페이지에서 **"Variables"** 탭 클릭
2. 또는 상단의 **"Variables"** 버튼 클릭

### 4.2 환경 변수 추가
**"New Variable"** 버튼을 클릭하여 다음 변수들을 하나씩 추가:

#### 필수 환경 변수 (8개)

1. **SLACK_SIGNING_SECRET**
   ```
   SLACK_SIGNING_SECRET=복사한_Signing_Secret_값
   ```
   - Slack App의 Signing Secret (이전에 복사한 값)

2. **SLACK_BOT_TOKEN**
   ```
   SLACK_BOT_TOKEN=xoxb-복사한_Bot_Token_값
   ```
   - Slack App의 Bot User OAuth Token (xoxb-로 시작)

3. **SLACK_WEBHOOK_URL**
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```
   - 기존 Slack 웹훅 URL (`.env` 파일에 있던 값)

4. **NAVER_CLIENT_ID**
   ```
   NAVER_CLIENT_ID=네이버_API_Client_ID
   ```
   - 네이버 검색 API Client ID

5. **NAVER_CLIENT_SECRET**
   ```
   NAVER_CLIENT_SECRET=네이버_API_Client_Secret
   ```
   - 네이버 검색 API Client Secret

6. **GEMINI_API_KEY**
   ```
   GEMINI_API_KEY=Gemini_API_Key_값
   ```
   - Google Gemini API Key

7. **STREAMLIT_APP_URL**
   ```
   STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
   ```
   - Streamlit Cloud 앱 URL (이미 배포된 URL)

8. **SLACK_APP_URL**
   ```
   SLACK_APP_URL=https://your-railway-url.railway.app
   ```
   - ⚠️ **나중에 업데이트 필요** (배포 완료 후 도메인 확인 후)

### 4.3 환경 변수 입력 방법
각 변수마다:
1. **"New Variable"** 클릭
2. **Key** 입력란에 변수 이름 입력 (예: `SLACK_BOT_TOKEN`)
3. **Value** 입력란에 값 입력 (예: `xoxb-1234567890-...`)
4. **"Add"** 또는 **"Save"** 클릭
5. 다음 변수 추가를 위해 반복

### 4.4 환경 변수 확인
- Variables 탭에서 모든 변수가 표시되는지 확인
- 값이 올바르게 입력되었는지 확인

---

## 5단계: 배포 완료 대기 및 URL 확인

### 5.1 배포 상태 확인
1. **"Deployments"** 탭 클릭
2. 배포 진행 상황 확인
   - ✅ **"Active"** 상태가 되면 배포 완료

### 5.2 도메인 URL 확인
1. **"Settings"** 탭 클릭
2. **"Domains"** 섹션으로 스크롤
3. **"Generate Domain"** 버튼 클릭 (아직 없다면)
4. 생성된 도메인 확인
   - 예: `cardnews-slack-production.up.railway.app`
   - 또는 `cardnews1-production.up.railway.app`
5. 📋 **이 URL을 복사해두세요!**

### 5.3 SLACK_APP_URL 업데이트
1. **"Variables"** 탭으로 돌아가기
2. `SLACK_APP_URL` 변수 찾기
3. **"Edit"** 클릭
4. Value를 실제 Railway 도메인으로 업데이트:
   ```
   https://cardnews-slack-production.up.railway.app
   ```
   - (실제 생성된 도메인으로 변경)
5. **"Save"** 클릭

---

## 6단계: 배포 확인 및 테스트

### 6.1 로그 확인
1. **"Deployments"** 탭에서 최신 배포 클릭
2. **"View Logs"** 클릭
3. 다음 메시지가 보이면 정상:
   ```
   * Running on http://0.0.0.0:5000
   ```

### 6.2 서버 상태 확인
1. 브라우저에서 Railway 도메인 접속:
   ```
   https://your-railway-url.railway.app
   ```
2. **"Not Found"** 또는 **"404"** 에러가 나오면 정상
   - (루트 경로는 없고 `/slack/interactive`, `/slack/command`만 있음)

### 6.3 Health Check (선택사항)
브라우저에서 다음 URL 접속:
```
https://your-railway-url.railway.app/health
```
- 정상이면 간단한 응답이 표시됩니다

---

## 7단계: Slack App Request URL 설정

### 7.1 Interactivity Request URL 설정
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. 생성한 App 선택
3. 왼쪽 메뉴에서 **"Interactivity & Shortcuts"** 또는 **"Interactivity"** 클릭
4. **"Interactivity"** 섹션에서:
   - **Request URL** 입력란에 다음 입력:
     ```
     https://your-railway-url.railway.app/slack/interactive
     ```
     - (실제 Railway 도메인으로 변경)
5. Slack이 자동으로 URL 검증 시도
   - ✅ **초록색 체크 표시**가 나타나면 성공
   - ❌ 실패하면 Railway 로그 확인
6. **"Save Changes"** 클릭

### 7.2 Slash Command Request URL 설정
1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. `/cardnews` 명령어 클릭
3. **Request URL** 입력란에 다음 입력:
   ```
   https://your-railway-url.railway.app/slack/command
   ```
   - (실제 Railway 도메인으로 변경)
4. **"Save"** 클릭

---

## 8단계: 최종 테스트

### 8.1 Slash Command 테스트
1. Slack 워크스페이스에서 아무 채널이나 열기
2. `/cardnews` 입력
3. 기사 목록이 표시되면 성공! ✅

### 8.2 버튼 클릭 테스트
1. 슬랙 알림 메시지에서 **"📝 카드뉴스 생성"** 버튼 클릭
2. 카드뉴스가 생성되어 슬랙에 전송되면 성공! ✅

---

## 📋 체크리스트

### Railway 설정
- [ ] Railway 계정 생성 (GitHub 연동)
- [ ] 프로젝트 생성 및 저장소 연결
- [ ] Start Command 설정 (`python slack_app.py`)
- [ ] 환경 변수 8개 모두 추가
- [ ] 배포 완료 확인 (Active 상태)
- [ ] 도메인 URL 확인 및 복사
- [ ] SLACK_APP_URL 업데이트

### Slack App 연동
- [ ] Interactivity Request URL 설정
- [ ] URL 검증 완료 (✅ 표시)
- [ ] Slash Command Request URL 설정

### 테스트
- [ ] `/cardnews` 명령어 테스트
- [ ] 버튼 클릭 테스트
- [ ] 카드뉴스 생성 확인

---

## ⚠️ 중요 사항

### 환경 변수 값 준비
다음 값들을 미리 준비해두세요:
1. **SLACK_SIGNING_SECRET** - Slack App의 Signing Secret
2. **SLACK_BOT_TOKEN** - Slack App의 Bot User OAuth Token (xoxb-로 시작)
3. **SLACK_WEBHOOK_URL** - 기존 웹훅 URL
4. **NAVER_CLIENT_ID** - 네이버 API 키
5. **NAVER_CLIENT_SECRET** - 네이버 API Secret
6. **GEMINI_API_KEY** - Gemini API 키

### URL 형식
- Railway 도메인은 항상 `https://`로 시작
- 마지막에 `/` 없이 입력
- 예: `https://cardnews-slack-production.up.railway.app`

### Request URL 검증
- Slack이 자동으로 URL을 검증합니다
- 검증 실패 시:
  1. Railway 서버가 실행 중인지 확인
  2. 로그에서 오류 확인
  3. URL이 정확한지 확인 (오타 없이)

---

## 🆘 문제 해결

### 배포가 실패해요
1. **"Deployments"** 탭에서 로그 확인
2. 환경 변수가 모두 설정되었는지 확인
3. Start Command가 올바른지 확인

### Request URL 검증 실패
1. Railway 로그 확인:
   - **"Deployments"** → 최신 배포 → **"View Logs"**
2. 서버가 정상 실행 중인지 확인:
   - `* Running on http://0.0.0.0:5000` 메시지 확인
3. HTTPS URL인지 확인 (HTTP 불가)
4. URL에 오타가 없는지 확인

### 환경 변수가 적용 안 돼요
1. 변수 추가 후 **"Redeploy"** 클릭
2. 또는 **"Deployments"** → **"Redeploy"** 클릭

### 슬랙에서 응답이 없어요
1. Railway 로그 확인
2. 환경 변수 (특히 `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`) 확인
3. Slack App의 Request URL이 올바른지 확인

---

## 💡 팁

### 무료 플랜 제한
- Railway 무료 플랜은 월 500시간 제공
- 사용량 모니터링: **"Usage"** 탭에서 확인

### 자동 배포
- GitHub에 푸시하면 자동으로 재배포됩니다
- 수동 재배포: **"Deployments"** → **"Redeploy"**

### 로그 확인
- 실시간 로그: **"Deployments"** → 최신 배포 → **"View Logs"**
- 오류 발생 시 로그를 먼저 확인하세요

---

**예상 소요 시간: 약 15-20분**

**다음 단계**: Slack App Request URL 설정 → 테스트

