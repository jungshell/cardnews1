# 🚀 배포 단계별 가이드 (GitHub 계정 있음)

## 현재 상태
- ✅ GitHub 계정: `jungshell`
- ✅ Git 저장소: 초기화됨
- ⚠️  원격 저장소: 연결 필요

---

## 1단계: GitHub 저장소 선택/생성

### 옵션 A: 기존 저장소 사용 (예: cardnews, cardnews1)
```bash
cd "/Volumes/Samsung USB/cardnews_3"
git remote add origin https://github.com/jungshell/cardnews.git
# 또는
git remote add origin https://github.com/jungshell/cardnews1.git
```

### 옵션 B: 새 저장소 생성
1. [https://github.com/new](https://github.com/new) 접속
2. 저장소 이름 입력 (예: `cardnews_3`)
3. Public 또는 Private 선택
4. **"Initialize this repository with a README" 체크 해제** ⚠️
5. "Create repository" 클릭

---

## 2단계: 코드 푸시

```bash
cd "/Volumes/Samsung USB/cardnews_3"

# 원격 저장소 연결 (위에서 선택한 저장소)
git remote add origin https://github.com/jungshell/저장소이름.git

# 코드 푸시
git add .
git commit -m "Deploy to Streamlit Cloud"
git branch -M main
git push -u origin main
```

**또는 자동 스크립트 사용:**
```bash
./setup_github.sh
```

---

## 3단계: Streamlit Cloud 배포

### 3-1. Streamlit Cloud 접속
- [https://streamlit.io/cloud](https://streamlit.io/cloud) 접속
- "Sign up" 또는 "Log in" 클릭
- GitHub 계정으로 로그인

### 3-2. 새 앱 생성
1. "New app" 버튼 클릭
2. 설정:
   - **Repository**: `jungshell/저장소이름` 선택
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. "Advanced settings" 클릭
4. "Secrets" 섹션에서 다음 추가:

```toml
NAVER_CLIENT_ID = "your_naver_client_id"
NAVER_CLIENT_SECRET = "your_naver_client_secret"
GEMINI_API_KEY = "your_gemini_api_key"
SLACK_WEBHOOK_URL = "your_slack_webhook_url"
```

5. "Deploy!" 클릭

### 3-3. 배포 완료
- 몇 분 후 자동으로 배포됩니다
- URL 예시: `https://저장소이름.streamlit.app`
- 이제 어디서든 접속 가능합니다! 🎉

---

## 빠른 명령어 (한 번에 실행)

```bash
cd "/Volumes/Samsung USB/cardnews_3"

# 1. 원격 저장소 연결 (저장소 이름만 변경)
git remote add origin https://github.com/jungshell/cardnews_3.git

# 2. 코드 푸시
git add .
git commit -m "Deploy to Streamlit Cloud"
git branch -M main
git push -u origin main

# 3. Streamlit Cloud에서 배포 (위 3단계 참고)
```

---

## ⚠️ 주의사항

1. **`.env` 파일은 절대 푸시하지 마세요!**
   - 이미 `.gitignore`에 포함되어 있습니다
   - 환경 변수는 Streamlit Cloud의 "Secrets"에서 설정하세요

2. **기존 저장소를 사용하는 경우**
   - 기존 코드와 충돌할 수 있습니다
   - 필요시 `git pull origin main` 먼저 실행

3. **새 저장소를 만드는 경우**
   - "Initialize with README" 체크 해제 필수!

---

## 🆘 문제 해결

### "remote origin already exists" 오류
```bash
git remote remove origin
git remote add origin https://github.com/jungshell/저장소이름.git
```

### 푸시 실패
```bash
# 원격 저장소 확인
git remote -v

# 강제 푸시 (주의: 기존 코드 덮어씀)
git push -u origin main --force
```

### 배포 실패
- Streamlit Cloud 대시보드에서 로그 확인
- 환경 변수가 모두 설정되었는지 확인
- `requirements.txt`에 모든 패키지가 포함되어 있는지 확인

