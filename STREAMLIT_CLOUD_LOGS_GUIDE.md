# 📋 Streamlit Cloud 로그 확인 가이드

## 1단계: Streamlit Cloud 대시보드 접속

1. [https://share.streamlit.io/](https://share.streamlit.io/) 접속
2. 로그인 (GitHub 계정으로 로그인)

## 2단계: 앱 선택

1. 대시보드에서 **"cardnews1"** 앱 찾기
2. **"cardnews1 • main • app.py"** 클릭
   - 또는 앱 이름 옆의 **⚙️ 아이콘** 클릭

## 3단계: "Manage app" 클릭

1. 앱을 클릭하면 앱 상세 페이지로 이동
2. 오른쪽 상단 또는 앱 제목 아래에 **"Manage app"** 버튼 클릭
   - 또는 앱 URL에서 직접: `https://share.streamlit.io/app/cardnews1/manage`

## 4단계: "Logs" 탭 클릭

1. "Manage app" 페이지에서 여러 탭이 보임:
   - **Settings** (설정)
   - **Secrets** (환경 변수)
   - **Logs** ← **여기 클릭!**
   - **Usage** (사용량)
   - **Deployments** (배포 기록)

2. **"Logs" 탭** 클릭

## 5단계: 로그 확인

로그 화면에서 다음을 확인:

### 배포 로그 확인
```
[XX:XX:XX] 🐙 Pulling code changes from Github...
[XX:XX:XX] 📦 Processing dependencies...
[XX:XX:XX] 🐍 Python dependencies were installed...
```

### 최신 커밋 확인
- 최근 배포 시간 확인
- 커밋 메시지 확인:
  - `로그 영역 전체 너비 강화 및 카드뉴스 생성 오류 메시지 상세화` ← 최신이어야 함

### 런타임 로그 확인
- 앱 실행 중 발생하는 오류
- `[Gemini]`로 시작하는 메시지
- `[네이버 API]`로 시작하는 메시지

## 6단계: 실시간 로그 확인

1. **로그 화면을 열어둔 상태**에서
2. **다른 탭에서 앱 사용** (크롤링 버튼 클릭 등)
3. **로그 화면으로 돌아와서** 새로고침 (F5)
4. 새로운 로그 메시지 확인

---

## 빠른 접근 방법

### 방법 1: URL로 직접 접근
```
https://share.streamlit.io/app/cardnews1/manage
```
→ "Logs" 탭 클릭

### 방법 2: 앱에서 직접
1. 앱 하단의 **"< Manage app"** 링크 클릭
2. "Logs" 탭 클릭

---

## 로그에서 확인할 사항

### ✅ 정상 배포 확인
```
[XX:XX:XX] 🐙 Pulling code changes from Github...
[XX:XX:XX] 📦 Processing dependencies...
[XX:XX:XX] ✅ Your app is live!
```

### ❌ 오류 확인
```
[XX:XX:XX] ❌ Error: ...
[XX:XX:XX] ⚠️ Warning: ...
```

### 🔍 크롤링 로그 확인
```
[네이버 API] HTTP 상태 코드: 200
[네이버 API] '충남콘텐츠진흥원' 검색 성공: XX개 기사 반환
```

### 🔍 카드뉴스 생성 로그 확인
```
[Gemini HTTP 오류] 401 ...
[Gemini 성공] XXX자 생성됨
```

---

## 문제 해결

### 로그가 안 보임
1. "Logs" 탭이 비활성화되어 있는지 확인
2. 브라우저 새로고침 (F5)
3. 다른 브라우저에서 시도

### 최신 커밋이 반영되지 않음
1. "Deployments" 탭에서 최신 배포 상태 확인
2. 배포가 실패했는지 확인
3. 수동으로 재배포 시도 (Settings → "Reboot app")

