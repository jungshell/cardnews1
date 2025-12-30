# 🚂 Railway 대안 가이드

## 현재 상황
- Railway 무료 플랜에서 프로젝트 생성 제한 도달
- 이미 5개 프로젝트 존재

---

## 방법 1: 기존 프로젝트에 서비스 추가 (권장)

### 1.1 기존 프로젝트 선택
1. Railway 대시보드에서 기존 프로젝트 선택
   - 예: `gallant-acceptance` 또는 `perfect-enthusiasm`
2. 프로젝트 페이지로 이동

### 1.2 새 서비스 추가
1. 프로젝트 페이지에서 **"+ New"** 버튼 클릭
2. **"GitHub Repo"** 선택
3. `jungshell/cardnews1` 저장소 선택
4. **"Deploy"** 클릭

### 1.3 서비스 설정
- Start Command: `python slack_app.py`
- 환경 변수 8개 추가
- 나머지는 동일하게 진행

**장점**: 무료 플랜에서도 가능, 추가 비용 없음

---

## 방법 2: Render 사용 (완전 무료)

### 2.1 Render 계정 생성
1. [https://render.com/](https://render.com/) 접속
2. **"Get Started for Free"** 클릭
3. GitHub로 로그인

### 2.2 새 Web Service 생성
1. 대시보드에서 **"New +"** 클릭
2. **"Web Service"** 선택
3. `jungshell/cardnews1` 저장소 연결

### 2.3 설정
- **Name**: `cardnews-slack` (원하는 이름)
- **Region**: `Singapore` (한국과 가까운 지역)
- **Branch**: `main`
- **Root Directory**: (비워두기)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python slack_app.py`

### 2.4 환경 변수 설정
**"Environment"** 섹션에서 다음 추가:
```
SLACK_SIGNING_SECRET=...
SLACK_BOT_TOKEN=...
SLACK_WEBHOOK_URL=...
NAVER_CLIENT_ID=...
NAVER_CLIENT_SECRET=...
GEMINI_API_KEY=...
STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
SLACK_APP_URL=https://cardnews-slack.onrender.com
PORT=5000
```

### 2.5 배포
1. **"Create Web Service"** 클릭
2. 배포 완료 대기 (약 5분)
3. 도메인 확인: `https://cardnews-slack.onrender.com`

**장점**: 완전 무료, 프로젝트 제한 없음
**단점**: 15분 비활성 시 슬립 모드 (첫 요청 시 깨어남)

---

## 방법 3: Fly.io 사용 (무료 티어)

### 3.1 Fly.io 계정 생성
1. [https://fly.io/](https://fly.io/) 접속
2. **"Sign Up"** 클릭
3. GitHub로 로그인

### 3.2 앱 생성
터미널에서:
```bash
# Fly.io CLI 설치 (macOS)
curl -L https://fly.io/install.sh | sh

# 로그인
fly auth login

# 앱 생성
cd "/Volumes/Samsung USB/cardnews_3"
fly launch --name cardnews-slack
```

### 3.3 설정 파일 생성
`fly.toml` 파일이 자동 생성됩니다. 수정:
```toml
app = "cardnews-slack"
primary_region = "icn"  # 서울

[build]

[env]
  PORT = "5000"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[services]]
  protocol = "tcp"
  internal_port = 5000
```

### 3.4 환경 변수 설정
```bash
fly secrets set SLACK_SIGNING_SECRET=...
fly secrets set SLACK_BOT_TOKEN=...
fly secrets set SLACK_WEBHOOK_URL=...
fly secrets set NAVER_CLIENT_ID=...
fly secrets set NAVER_CLIENT_SECRET=...
fly secrets set GEMINI_API_KEY=...
fly secrets set STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
fly secrets set SLACK_APP_URL=https://cardnews-slack.fly.dev
```

### 3.5 배포
```bash
fly deploy
```

**장점**: 빠른 속도, 무료 티어 제공
**단점**: CLI 사용 필요

---

## 방법 4: Railway 유료 플랜 업그레이드

### 4.1 Hobby 플랜 ($5/월)
- 무제한 프로젝트
- 8GB RAM / 8 vCPU
- 7일 로그 히스토리
- 월 $5

### 4.2 업그레이드 방법
1. 모달에서 **"Upgrade to Hobby"** 클릭
2. 결제 정보 입력
3. 업그레이드 완료 후 프로젝트 생성

---

## 추천 순서

1. **기존 프로젝트에 서비스 추가** (가장 간단, 무료)
2. **Render 사용** (완전 무료, 프로젝트 제한 없음)
3. **Fly.io 사용** (빠른 속도, CLI 필요)
4. **Railway 업그레이드** (비용 발생)

---

## 각 방법 비교

| 방법 | 비용 | 난이도 | 속도 | 추천도 |
|------|------|--------|------|--------|
| 기존 프로젝트 추가 | 무료 | ⭐ 쉬움 | 빠름 | ⭐⭐⭐⭐⭐ |
| Render | 무료 | ⭐⭐ 보통 | 보통 | ⭐⭐⭐⭐ |
| Fly.io | 무료 | ⭐⭐⭐ 어려움 | 빠름 | ⭐⭐⭐ |
| Railway 업그레이드 | $5/월 | ⭐ 쉬움 | 빠름 | ⭐⭐ |

---

## 다음 단계

**방법 1 (기존 프로젝트 추가)을 권장합니다:**
1. 기존 프로젝트 선택
2. "+ New" → "GitHub Repo"
3. 저장소 연결 및 배포
4. 환경 변수 설정
5. Slack App Request URL 설정

어떤 방법으로 진행할까요?

