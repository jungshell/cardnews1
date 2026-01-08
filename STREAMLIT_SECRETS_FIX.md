# 🔧 Streamlit Cloud Secrets 설정 가이드 (GEMINI_API_KEY 오류 해결)

## 문제 상황
- ❌ 카드뉴스 문구 생성 실패
- ❌ 에러 메시지: "생성 실패: Gemini API 호출 실패 또는 응답 없음"
- 💡 해결: Streamlit Cloud의 Secrets에서 `GEMINI_API_KEY` 확인 및 수정

---

## 해결 방법: Streamlit Cloud Secrets 설정

### 1단계: Streamlit Cloud 대시보드 접속

1. **Streamlit Cloud 접속**
   - https://share.streamlit.io 접속
   - 또는 https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

2. **앱 선택**
   - 대시보드에서 `cardnews1` 앱 클릭
   - 또는 앱 URL: https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app

---

### 2단계: Secrets 설정 페이지 이동

1. **앱 대시보드에서**
   - 오른쪽 상단 **"⋮" (더보기)** 메뉴 클릭
   - **"Settings"** 클릭

2. **또는 직접 접속**
   - https://share.streamlit.io/ 에서 앱 선택 후 Settings

3. **"Secrets" 섹션 찾기**
   - 왼쪽 메뉴 또는 페이지에서 **"Secrets"** 클릭

---

### 3단계: GEMINI_API_KEY 확인 및 수정

#### 현재 설정 확인

1. **Secrets 편집기 열기**
   - **"Edit secrets"** 또는 **"Secrets"** 버튼 클릭

2. **현재 설정 확인**
   - TOML 형식으로 표시됩니다:
   ```toml
   NAVER_CLIENT_ID = "your_naver_client_id"
   NAVER_CLIENT_SECRET = "your_naver_client_secret"
   GEMINI_API_KEY = "your_gemini_api_key"
   SLACK_WEBHOOK_URL = "your_slack_webhook_url"
   ```

#### GEMINI_API_KEY 수정

**문제가 있는 경우:**
- `GEMINI_API_KEY`가 없음 → 추가 필요
- `GEMINI_API_KEY` 값이 잘못됨 → 수정 필요
- 따옴표가 잘못됨 → 형식 확인 필요

**올바른 형식:**
```toml
GEMINI_API_KEY = "AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY"
```

**주의사항:**
- ✅ 따옴표(`"`)로 감싸야 합니다
- ✅ 등호(`=`) 앞뒤로 공백이 있어야 합니다
- ✅ 키 값에 공백이나 줄바꿈이 없어야 합니다
- ❌ 따옴표 없이 입력하면 안 됩니다
- ❌ `GEMINI_API_KEY=value` 형식은 안 됩니다 (공백 필요)

---

### 4단계: Gemini API 키 확인

**Gemini API 키가 없거나 잘못된 경우:**

1. **Google AI Studio 접속**
   - https://aistudio.google.com/app/apikey 접속
   - Google 계정으로 로그인

2. **API 키 생성 또는 확인**
   - 기존 키가 있으면 복사
   - 없으면 **"Create API Key"** 클릭하여 새로 생성

3. **API 키 형식 확인**
   - `AIzaSy`로 시작하는 긴 문자열
   - 예: `AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY`

---

### 5단계: Secrets 저장 및 재배포

1. **Secrets 저장**
   - Secrets 편집기에서 **"Save"** 버튼 클릭
   - 또는 **"Update"** 버튼 클릭

2. **자동 재배포**
   - Secrets 저장 시 자동으로 앱이 재배포됩니다
   - 약 1-2분 소요

3. **재배포 확인**
   - 앱 대시보드에서 **"Events"** 탭 확인
   - **"Deploy successful"** 메시지 확인

---

### 6단계: 테스트

1. **앱 접속**
   - https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app 접속

2. **카드뉴스 생성 테스트**
   - 기사 선택
   - **"📝 카드뉴스 문구 생성"** 버튼 클릭
   - 정상 작동하는지 확인

---

## 문제 해결 체크리스트

### Secrets 설정 확인
- [ ] `GEMINI_API_KEY`가 Secrets에 존재함
- [ ] `GEMINI_API_KEY` 값이 올바른 형식 (따옴표 포함)
- [ ] 등호(`=`) 앞뒤에 공백 있음
- [ ] 키 값에 공백이나 줄바꿈 없음

### API 키 확인
- [ ] Gemini API 키가 유효함 (Google AI Studio에서 확인)
- [ ] API 키가 `AIzaSy`로 시작함
- [ ] API 키가 만료되지 않음

### 재배포 확인
- [ ] Secrets 저장 후 재배포 완료됨
- [ ] 앱이 정상적으로 실행됨
- [ ] 로그에 오류 없음

---

## 추가 문제 해결

### 여전히 실패하는 경우

#### 1. Streamlit Cloud 로그 확인
1. 앱 대시보드 → **"Manage app"** → **"Logs"**
2. 카드뉴스 생성 시 오류 메시지 확인:
   - `[Gemini HTTP 오류]` → API 키 문제
   - `[Gemini Rate Limit]` → API 사용량 초과
   - `[Gemini 타임아웃]` → 네트워크 문제

#### 2. API 키 유효성 확인
1. **Google AI Studio에서 테스트**
   - https://aistudio.google.com/app/apikey
   - API 키가 활성화되어 있는지 확인
   - 사용량 제한에 걸리지 않았는지 확인

#### 3. Secrets 형식 재확인
```toml
# ✅ 올바른 형식
GEMINI_API_KEY = "AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY"

# ❌ 잘못된 형식들
GEMINI_API_KEY=AIzaSy...  # 공백 없음
GEMINI_API_KEY = AIzaSy...  # 따옴표 없음
GEMINI_API_KEY = "AIzaSy...
"  # 줄바꿈 있음
```

#### 4. 수동 재배포
1. 앱 대시보드 → **"⋮"** 메뉴 → **"Reboot app"** 클릭
2. 또는 **"Redeploy"** 클릭

---

## 참고 자료

- **Streamlit Cloud 문서**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Google AI Studio**: https://aistudio.google.com/app/apikey
- **Gemini API 문서**: https://ai.google.dev/docs

---

## 빠른 해결 요약

1. **Streamlit Cloud → 앱 선택 → Settings → Secrets**
2. **`GEMINI_API_KEY` 확인 및 수정** (따옴표 포함, 공백 확인)
3. **Save → 자동 재배포 대기 (1-2분)**
4. **앱에서 테스트**

이제 카드뉴스 문구 생성이 정상 작동할 것입니다! 🎉
