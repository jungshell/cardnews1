# 🤖 Slack App 구축 가이드 (완전 자동화)

## 개요
슬랙에서 직접 카드뉴스 생성 및 이미지 준비까지 가능하도록 Slack App을 구축합니다.

---

## 1단계: Slack App 생성

### 1. Slack API 웹사이트 접속
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. 로그인 (슬랙 워크스페이스 계정)

### 2. 새 App 생성
1. **"Create New App"** 클릭
2. **"From scratch"** 선택
3. **App 이름**: `카드뉴스 자동화` (또는 원하는 이름)
4. **워크스페이스 선택**: 카드뉴스를 받을 워크스페이스 선택
5. **"Create App"** 클릭

---

## 2단계: Interactive Components 활성화

### 1. Features → Interactivity 활성화
1. 왼쪽 메뉴에서 **"Interactivity"** 클릭
2. **"Interactivity"** 토글을 **ON**으로 설정

### 2. Request URL 설정
- **Request URL**: `https://your-server.com/slack/interactive`
  - 예: `https://cardnews-slack.herokuapp.com/slack/interactive`
  - 또는 Railway/Render 등 사용
  - **나중에 설정 가능** (서버 배포 후)

### 3. 저장
- **"Save Changes"** 클릭

---

## 3단계: Slash Commands 추가

### 1. Features → Slash Commands
1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. **"Create New Command"** 클릭

### 2. 명령어 설정
- **Command**: `/cardnews`
- **Request URL**: `https://your-server.com/slack/command`
- **Short Description**: `카드뉴스 생성`
- **Usage Hint**: `[기사 번호]` (선택사항)

### 3. 저장
- **"Save"** 클릭

---

## 4단계: OAuth & Permissions 설정

### 1. Features → OAuth & Permissions
1. 왼쪽 메뉴에서 **"OAuth & Permissions"** 클릭

### 2. Scopes 추가
**Bot Token Scopes**에 다음 추가:
- `chat:write` - 메시지 전송
- `commands` - Slash Commands 사용
- `users:read` - 사용자 정보 읽기

### 3. 워크스페이스에 설치
1. 페이지 상단의 **"Install to Workspace"** 클릭
2. 권한 확인 후 **"Allow"** 클릭

### 4. 토큰 복사
- **Bot User OAuth Token** 복사
  - `xoxb-`로 시작하는 긴 문자열
- 이 토큰을 환경 변수에 저장 (나중에)

---

## 5단계: Signing Secret 복사

### 1. Basic Information → App Credentials
1. 왼쪽 메뉴에서 **"Basic Information"** 클릭
2. **"App Credentials"** 섹션 찾기
3. **"Signing Secret"** 옆의 **"Show"** 클릭
4. Secret 복사
   - 예: `1234567890abcdef1234567890abcdef`

---

## 6단계: 서버 배포

### 옵션 1: Railway (권장, 간단)

#### 1. Railway 계정 생성
1. [https://railway.app/](https://railway.app/) 접속
2. GitHub로 로그인

#### 2. 새 프로젝트 생성
1. **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. `cardnews1` 저장소 선택

#### 3. 환경 변수 설정
**Variables** 탭에서 다음 추가:
```
SLACK_SIGNING_SECRET=복사한_Signing_Secret
SLACK_BOT_TOKEN=복사한_Bot_User_OAuth_Token
SLACK_WEBHOOK_URL=기존_웹훅_URL
NAVER_CLIENT_ID=네이버_API_키
NAVER_CLIENT_SECRET=네이버_API_Secret
GEMINI_API_KEY=Gemini_API_키
STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
PORT=5000
```

#### 4. 시작 명령어 설정
**Settings** → **Deploy** → **Start Command**:
```
python slack_app.py
```

#### 5. 도메인 확인
배포 완료 후 **Settings** → **Domains**에서 URL 확인
- 예: `https://cardnews-slack-production.up.railway.app`

---

### 옵션 2: Render

#### 1. Render 계정 생성
1. [https://render.com/](https://render.com/) 접속
2. GitHub로 로그인

#### 2. 새 Web Service 생성
1. **"New +"** → **"Web Service"** 클릭
2. GitHub 저장소 연결
3. 설정:
   - **Name**: `cardnews-slack`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python slack_app.py`

#### 3. 환경 변수 설정
**Environment** 탭에서 위와 동일한 환경 변수 추가

---

## 7단계: Slack App 설정 업데이트

### 1. Request URL 업데이트
배포된 서버 URL을 Slack App에 설정:

1. **Interactivity** → **Request URL**
   - `https://your-server.com/slack/interactive` 입력
   - Slack이 자동으로 검증

2. **Slash Commands** → `/cardnews` → **Request URL**
   - `https://your-server.com/slack/command` 입력

---

## 8단계: 슬랙 알림에 버튼 추가

`daily_fetch.py`의 `send_slack_notification` 함수를 수정하여 Interactive 버튼 추가:

```python
# 요약 보기 버튼 추가
buttons.append({
    "type": "button",
    "text": {
        "type": "plain_text",
        "text": "📄 요약 보기",
    },
    "action_id": f"view_summary_{idx}",
    "value": str(idx),
})
```

---

## 사용 방법

### 1. 슬랙 메시지에서 버튼 클릭
- **"📝 카드뉴스 생성"** 버튼 클릭
- 카드뉴스가 자동으로 생성되어 슬랙에 전송됨

### 2. Slash Command 사용
- `/cardnews` - 전체 목록 보기
- `/cardnews 1` - 첫 번째 기사 카드뉴스 생성

---

## 문제 해결

### Request URL 검증 실패
- 서버가 정상적으로 실행 중인지 확인
- HTTPS 사용 필수 (HTTP 불가)
- `/slack/interactive` 엔드포인트가 정상 응답하는지 확인

### 버튼 클릭 시 오류
- 환경 변수가 올바르게 설정되었는지 확인
- Slack App의 Signing Secret이 올바른지 확인
- 서버 로그 확인

---

## 체크리스트

- [ ] Slack App 생성 완료
- [ ] Interactive Components 활성화
- [ ] Slash Commands 추가
- [ ] OAuth & Permissions 설정
- [ ] Bot Token 복사
- [ ] Signing Secret 복사
- [ ] 서버 배포 (Railway/Render)
- [ ] 환경 변수 설정
- [ ] Request URL 업데이트
- [ ] 테스트 완료

---

## 다음 단계

서버 배포가 완료되면:
1. Slack App의 Request URL 업데이트
2. 슬랙에서 `/cardnews` 명령어 테스트
3. 슬랙 메시지의 버튼 클릭 테스트

