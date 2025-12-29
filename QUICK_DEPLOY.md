# 🚀 빠른 배포 가이드 (5분 안에 완료!)

## 방법 1: Streamlit Cloud (가장 간단, 추천 ⭐)

### 1단계: GitHub에 코드 업로드

```bash
cd "/Volumes/Samsung USB/cardnews_3"

# Git 초기화
git init
git add .
git commit -m "Initial commit"

# GitHub에 새 저장소 생성 후 (github.com에서 먼저 생성)
git remote add origin https://github.com/yourusername/cardnews_3.git
git branch -M main
git push -u origin main
```

### 2단계: Streamlit Cloud 배포

1. [https://streamlit.io/cloud](https://streamlit.io/cloud) 접속
2. "Sign up" → GitHub 계정으로 로그인
3. "New app" 클릭
4. 설정:
   - **Repository**: `yourusername/cardnews_3` 선택
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Advanced settings" → "Secrets" 클릭
6. 다음 내용 추가:
   ```
   NAVER_CLIENT_ID = "your_naver_client_id"
   NAVER_CLIENT_SECRET = "your_naver_client_secret"
   GEMINI_API_KEY = "your_gemini_api_key"
   SLACK_WEBHOOK_URL = "your_slack_webhook_url"
   ```
7. "Deploy!" 클릭

### 3단계: 완료! 🎉
- 몇 분 후 자동으로 배포됩니다
- URL 예시: `https://your-app-name.streamlit.app`
- 이제 어디서든 접속 가능합니다!

---

## 방법 2: Railway (스케줄러 필요 시)

### 1단계: GitHub에 코드 업로드 (위와 동일)

### 2단계: Railway 배포

1. [https://railway.app/](https://railway.app/) 접속
2. GitHub 계정으로 로그인
3. "New Project" → "Deploy from GitHub repo"
4. 저장소 선택
5. "Variables" 탭에서 환경 변수 추가:
   ```
   NAVER_CLIENT_ID=your_naver_client_id
   NAVER_CLIENT_SECRET=your_naver_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```
6. 자동 배포 완료!

---

## ⚠️ 주의사항

1. **`.env` 파일은 절대 GitHub에 올리지 마세요!**
   - 이미 `.gitignore`에 포함되어 있습니다
   - 환경 변수는 각 플랫폼의 대시보드에서 설정하세요

2. **API 키 보안**
   - GitHub에 API 키를 직접 올리지 마세요
   - 각 플랫폼의 "Secrets" 또는 "Environment Variables" 기능을 사용하세요

3. **필수 파일 확인**
   - `requirements.txt` ✅
   - `Procfile` ✅ (Railway용)
   - `.gitignore` ✅

---

## 🆘 문제 해결

### 배포 실패
- 로그 확인: 각 플랫폼의 대시보드에서 로그 확인
- 환경 변수 확인: 모든 변수가 설정되었는지 확인
- `requirements.txt` 확인: 모든 패키지가 포함되어 있는지 확인

### 접속 불가
- 배포 완료까지 몇 분 기다리기
- 로그에서 오류 메시지 확인
- 포트 설정 확인 (Streamlit Cloud는 자동)

