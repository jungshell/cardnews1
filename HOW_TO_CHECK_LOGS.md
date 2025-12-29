# 📋 Streamlit Cloud 로그 확인 방법 (단계별 가이드)

## 방법 1: 앱에서 직접 접근 (가장 쉬움)

### 1단계: 앱 하단 링크 클릭
1. 앱 화면 하단 오른쪽에 **"< Manage app"** 링크 클릭
   - 또는 앱 URL 끝에 `/manage` 추가:
   ```
   https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app/manage
   ```

### 2단계: "Logs" 탭 클릭
1. "Manage app" 페이지 상단에 여러 탭이 보임:
   - **Settings** (설정)
   - **Secrets** (환경 변수)
   - **Logs** ← **여기 클릭!**
   - **Usage** (사용량)
   - **Deployments** (배포 기록)

2. **"Logs" 탭** 클릭

### 3단계: 로그 확인
- 실시간 로그가 표시됨
- 스크롤하여 과거 로그 확인 가능

---

## 방법 2: Streamlit Cloud 대시보드에서 접근

### 1단계: 대시보드 접속
1. [https://share.streamlit.io/](https://share.streamlit.io/) 접속
2. 로그인 (GitHub 계정)

### 2단계: 앱 선택
1. 대시보드에서 **"cardnews1"** 앱 찾기
2. **"cardnews1 • main • app.py"** 클릭
   - 또는 앱 이름 옆의 **⚙️ 아이콘** 클릭

### 3단계: "Manage app" 클릭
1. 앱 상세 페이지에서 **"Manage app"** 버튼 클릭
   - 오른쪽 상단 또는 앱 제목 아래

### 4단계: "Logs" 탭 클릭
1. "Logs" 탭 클릭

---

## 로그에서 확인할 사항

### ✅ 최신 배포 확인
```
[XX:XX:XX] 🐙 Pulling code changes from Github...
[XX:XX:XX] 📦 Processing dependencies...
[XX:XX:XX] ✅ Your app is live!
```

**최신 커밋 메시지 확인:**
- `로그 영역 전체 너비 강화 및 카드뉴스 생성 오류 메시지 상세화` ← 최신이어야 함

### 🔍 크롤링 로그 확인
```
[네이버 API] HTTP 상태 코드: 200
[네이버 API] '충남콘텐츠진흥원' 검색 성공: XX개 기사 반환 (전체: XX개)
```

### 🔍 카드뉴스 생성 로그 확인
```
[Gemini HTTP 오류] 401 ...
[Gemini 성공] XXX자 생성됨
```

### ❌ 오류 확인
```
[XX:XX:XX] ❌ Error: ...
[XX:XX:XX] ⚠️ Warning: ...
```

---

## 실시간 로그 확인 방법

1. **로그 화면을 열어둔 상태**에서
2. **다른 탭에서 앱 사용** (크롤링 버튼 클릭 등)
3. **로그 화면으로 돌아와서** 새로고침 (F5)
4. 새로운 로그 메시지 확인

---

## 빠른 접근 URL

직접 URL로 접근:
```
https://share.streamlit.io/app/cardnews1/manage
```
→ "Logs" 탭 클릭

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

