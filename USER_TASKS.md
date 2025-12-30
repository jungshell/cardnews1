# ✅ 사용자가 직접 해야 할 작업 (체크리스트)

## 현재 상태
- ✅ 코드 작성 완료
- ✅ GitHub 푸시 완료
- ⏳ 서버 배포 및 Slack App 설정 필요

---

## 🎯 필수 작업 (순서대로 진행)

### 1단계: Slack App 생성 (약 10분)

#### 1.1 Slack App 생성
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. **"Create New App"** → **"From scratch"**
3. **App 이름**: `카드뉴스 자동화`
4. **워크스페이스 선택**: 카드뉴스를 받을 워크스페이스
5. **"Create App"** 클릭

#### 1.2 Interactive Components 활성화
1. 왼쪽 메뉴: **"Interactivity"** 클릭
2. **"Interactivity"** 토글을 **ON**
3. **Request URL**: 나중에 설정 (서버 배포 후)
4. **"Save Changes"** 클릭

#### 1.3 Slash Commands 추가
1. 왼쪽 메뉴: **"Slash Commands"** 클릭
2. **"Create New Command"** 클릭
3. 설정:
   - **Command**: `/cardnews`
   - **Request URL**: 나중에 설정 (서버 배포 후)
   - **Short Description**: `카드뉴스 생성`
   - **Usage Hint**: `[기사 번호]` (선택사항)
4. **"Save"** 클릭

#### 1.4 OAuth & Permissions 설정
1. 왼쪽 메뉴: **"OAuth & Permissions"** 클릭
2. **Bot Token Scopes**에 추가:
   - `chat:write` (메시지 전송)
   - `commands` (Slash Commands)
   - `users:read` (사용자 정보)
3. 페이지 상단: **"Install to Workspace"** 클릭
4. 권한 확인 후 **"Allow"** 클릭

#### 1.5 토큰 및 Secret 복사
1. **OAuth & Permissions** 페이지에서:
   - **Bot User OAuth Token** 복사
     - `xoxb-`로 시작하는 긴 문자열
     - 📋 **복사해서 저장해두세요!**

2. **Basic Information** → **"App Credentials"**:
   - **Signing Secret** 옆 **"Show"** 클릭
   - Secret 복사
     - 📋 **복사해서 저장해두세요!**

---

### 2단계: 서버 배포 (Railway 권장, 약 15분)

#### 2.1 Railway 계정 생성
1. [https://railway.app/](https://railway.app/) 접속
2. **"Login"** → **"GitHub"** 선택
3. GitHub 계정으로 로그인

#### 2.2 새 프로젝트 생성
1. **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. `jungshell/cardnews1` 저장소 선택
4. **"Deploy"** 클릭

#### 2.3 환경 변수 설정
**Variables** 탭에서 다음 추가:

```
SLACK_SIGNING_SECRET=복사한_Signing_Secret
SLACK_BOT_TOKEN=복사한_Bot_User_OAuth_Token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
NAVER_CLIENT_ID=네이버_API_Client_ID
NAVER_CLIENT_SECRET=네이버_API_Client_Secret
GEMINI_API_KEY=Gemini_API_Key
STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
SLACK_APP_URL=https://your-railway-url.railway.app
PORT=5000
```

**주의**: `SLACK_APP_URL`은 배포 후 도메인을 확인한 후 업데이트하세요.

#### 2.4 시작 명령어 설정
1. **Settings** 탭 클릭
2. **Deploy** 섹션에서:
   - **Start Command**: `python slack_app.py`
3. 저장

#### 2.5 배포 완료 대기
- 배포가 완료될 때까지 대기 (약 2-3분)
- **Settings** → **Domains**에서 URL 확인
  - 예: `https://cardnews-slack-production.up.railway.app`
- 📋 **이 URL을 복사해두세요!**

---

### 3단계: Slack App Request URL 설정 (약 5분)

#### 3.1 Interactivity Request URL 설정
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. 생성한 App 선택
3. **"Interactivity"** 클릭
4. **Request URL** 입력:
   ```
   https://your-railway-url.railway.app/slack/interactive
   ```
   - Railway에서 복사한 URL 사용
5. Slack이 자동으로 검증 (✅ 표시)
6. **"Save Changes"** 클릭

#### 3.2 Slash Command Request URL 설정
1. **"Slash Commands"** 클릭
2. `/cardnews` 명령어 클릭
3. **Request URL** 입력:
   ```
   https://your-railway-url.railway.app/slack/command
   ```
4. **"Save"** 클릭

---

### 4단계: Railway 환경 변수 업데이트 (선택)

Railway의 `SLACK_APP_URL` 환경 변수를 배포된 URL로 업데이트:
```
SLACK_APP_URL=https://your-railway-url.railway.app
```

---

### 5단계: 테스트 (약 5분)

#### 5.1 Slash Command 테스트
1. 슬랙 채널에서 `/cardnews` 입력
2. 기사 목록이 표시되는지 확인

#### 5.2 버튼 클릭 테스트
1. 슬랙 알림 메시지에서 **"📝 카드뉴스 생성"** 버튼 클릭
2. 카드뉴스가 생성되어 슬랙에 전송되는지 확인

---

## 📋 체크리스트

### Slack App 설정
- [ ] Slack App 생성 완료
- [ ] Interactive Components 활성화
- [ ] Slash Commands 추가 (`/cardnews`)
- [ ] OAuth & Permissions 설정
- [ ] Bot Token 복사 완료
- [ ] Signing Secret 복사 완료

### 서버 배포
- [ ] Railway 계정 생성
- [ ] 프로젝트 생성 및 배포
- [ ] 환경 변수 설정 (8개)
- [ ] Start Command 설정
- [ ] 배포 완료 및 URL 확인

### Slack App 연동
- [ ] Interactivity Request URL 설정
- [ ] Slash Command Request URL 설정
- [ ] URL 검증 완료 (✅ 표시)

### 테스트
- [ ] `/cardnews` 명령어 테스트
- [ ] 버튼 클릭 테스트
- [ ] 카드뉴스 생성 확인

---

## ⚠️ 중요 사항

### 환경 변수 값
다음 값들을 준비해두세요:
1. **SLACK_SIGNING_SECRET** - Slack App의 Signing Secret
2. **SLACK_BOT_TOKEN** - Slack App의 Bot User OAuth Token
3. **SLACK_WEBHOOK_URL** - 기존 웹훅 URL (이미 있음)
4. **NAVER_CLIENT_ID** - 네이버 API 키
5. **NAVER_CLIENT_SECRET** - 네이버 API Secret
6. **GEMINI_API_KEY** - Gemini API 키

### URL 확인
- Railway 배포 후 **반드시** 도메인 URL 확인
- Slack App의 Request URL에 정확히 입력

---

## 🆘 문제 해결

### Request URL 검증 실패
- 서버가 정상 실행 중인지 확인
- HTTPS 사용 필수 (HTTP 불가)
- Railway 로그 확인

### 버튼 클릭 시 오류
- 환경 변수가 올바르게 설정되었는지 확인
- Railway 로그 확인

---

## 완료 후

모든 설정이 완료되면:
- ✅ 슬랙에서 `/cardnews` 명령어로 카드뉴스 생성
- ✅ 슬랙 메시지 버튼 클릭으로 카드뉴스 생성
- ✅ 카드뉴스가 슬랙에 자동 전송

---

**총 예상 시간: 약 30-40분**

