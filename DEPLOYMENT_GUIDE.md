# 온라인 서버 배포 가이드

이 앱을 온라인 서버에 배포하는 방법을 안내합니다. 가장 간단한 방법부터 시작하세요.

## 🚀 방법 1: Streamlit Cloud (가장 간단, 무료)

### 장점
- ✅ 완전 무료
- ✅ GitHub만 연결하면 자동 배포
- ✅ 설정이 매우 간단
- ✅ 자동 HTTPS 지원

### 단계

1. **GitHub에 코드 업로드**
   ```bash
   # Git 저장소 초기화 (아직 안 했다면)
   git init
   git add .
   git commit -m "Initial commit"
   
   # GitHub에 새 저장소 생성 후
   git remote add origin https://github.com/yourusername/cardnews_3.git
   git push -u origin main
   ```

2. **Streamlit Cloud에 배포**
   - [Streamlit Cloud](https://streamlit.io/cloud) 접속
   - GitHub 계정으로 로그인
   - "New app" 클릭
   - 저장소 선택: `yourusername/cardnews_3`
   - Main file path: `app.py`
   - "Deploy!" 클릭

3. **환경 변수 설정**
   Streamlit Cloud 대시보드에서 "Settings" → "Secrets"에 다음을 추가:
   ```toml
   NAVER_CLIENT_ID = "your_naver_client_id"
   NAVER_CLIENT_SECRET = "your_naver_client_secret"
   GEMINI_API_KEY = "your_gemini_api_key"
   SLACK_WEBHOOK_URL = "your_slack_webhook_url"
   ```

4. **완료!**
   - 자동으로 배포되고 URL이 생성됩니다
   - 예: `https://your-app-name.streamlit.app`

---

## 🚂 방법 2: Railway (이미 설정됨)

### 장점
- ✅ 무료 티어 제공 (월 500시간)
- ✅ 자동 스케줄러 지원 (worker)
- ✅ GitHub 연동으로 자동 배포

### 단계

1. **Railway 계정 생성**
   - [Railway](https://railway.app/) 접속
   - GitHub 계정으로 로그인

2. **프로젝트 배포**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 저장소 선택: `yourusername/cardnews_3`
   - Railway가 자동으로 `Procfile`을 인식합니다

3. **환경 변수 설정**
   Railway 대시보드 → "Variables" 탭에서 추가:
   ```
   NAVER_CLIENT_ID=your_naver_client_id
   NAVER_CLIENT_SECRET=your_naver_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```

4. **서비스 확인**
   - `web` 서비스: Streamlit 앱 (자동으로 URL 생성)
   - `worker` 서비스: 일일 크롤링 스케줄러 (자동 실행)

5. **완료!**
   - 배포 완료 후 제공되는 URL로 접속
   - 예: `https://your-app-name.up.railway.app`

---

## 🎨 방법 3: Render (무료 티어 제공)

### 장점
- ✅ 무료 티어 제공
- ✅ 간단한 설정
- ✅ 자동 HTTPS

### 단계

1. **Render 계정 생성**
   - [Render](https://render.com/) 접속
   - GitHub 계정으로 로그인

2. **새 Web Service 생성**
   - "New" → "Web Service" 선택
   - GitHub 저장소 연결
   - 설정:
     - **Name**: `cardnews-app`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `streamlit run app.py --server.port $PORT --server.headless true`

3. **환경 변수 설정**
   Render 대시보드 → "Environment"에서 추가:
   ```
   NAVER_CLIENT_ID=your_naver_client_id
   NAVER_CLIENT_SECRET=your_naver_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   PORT=8501
   ```

4. **완료!**
   - 자동으로 배포되고 URL이 생성됩니다
   - 예: `https://cardnews-app.onrender.com`

---

## 📋 배포 전 체크리스트

### 필수 파일 확인
- ✅ `requirements.txt` - Python 패키지 목록
- ✅ `Procfile` - Railway용 (Railway 사용 시)
- ✅ `.env.example` - 환경 변수 예시
- ✅ `.gitignore` - `.env` 파일 제외 확인

### 환경 변수 확인
다음 변수들이 모두 설정되어야 합니다:
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `GEMINI_API_KEY`
- `SLACK_WEBHOOK_URL` (선택사항)

### Git 저장소 준비
```bash
# .env 파일은 Git에 포함하지 않도록 확인
echo ".env" >> .gitignore

# 필요한 파일만 커밋
git add .
git commit -m "Deploy to cloud"
git push
```

---

## 🔧 문제 해결

### 배포 실패
- 로그를 확인하여 오류 메시지 확인
- 환경 변수가 모두 설정되었는지 확인
- `requirements.txt`에 모든 패키지가 포함되어 있는지 확인

### 포트 오류
- Streamlit Cloud: 포트 설정 불필요 (자동)
- Railway: `$PORT` 환경 변수 사용 (이미 설정됨)
- Render: `$PORT` 환경 변수 사용

### 스케줄러가 작동하지 않음 (Railway)
- Railway 대시보드에서 `worker` 서비스가 실행 중인지 확인
- 로그에서 오류 메시지 확인

---

## 💡 추천

**처음 배포하는 경우**: **Streamlit Cloud**를 추천합니다.
- 가장 간단하고 빠름
- 무료
- 설정이 최소화됨

**스케줄러가 필요한 경우**: **Railway**를 추천합니다.
- `worker` 서비스로 자동 크롤링 가능
- 무료 티어 제공

