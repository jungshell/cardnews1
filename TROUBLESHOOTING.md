# 🔧 문제 해결 가이드

## 문제 1: `/cardnews` 명령어가 아무 반응이 없음

### 원인 분석
1. **요청 검증 실패**: `verify_slack_request`가 실패할 수 있음
2. **기사 데이터 로드 실패**: `load_daily_recommendations()` 오류
3. **에러 처리 부족**: 조용히 실패할 수 있음

### 해결 방법

#### 1. Render 로그 확인
1. Render 대시보드 → **"Logs"** 탭
2. `/cardnews` 명령어 실행 시 로그 확인
3. 오류 메시지 확인:
   - `[Slack Command] 요청 검증 실패` → Signing Secret 확인
   - `[Slack Command] 기사 로드 오류` → `daily_recommendations.json` 파일 확인
   - 기타 오류 메시지 확인

#### 2. 환경 변수 확인
Render의 **"Environment"** 탭에서:
- `SLACK_SIGNING_SECRET` - 올바른 값인지 확인
- `SLACK_BOT_TOKEN` - `xoxb-`로 시작하는지 확인

#### 3. 기사 데이터 확인
- `data/daily_recommendations.json` 파일이 있는지 확인
- 파일이 비어있거나 형식이 잘못되었을 수 있음

#### 4. 수정 사항 적용
코드에 에러 처리를 추가했습니다. 다음을 확인하세요:
- Render에 자동 재배포되었는지 확인
- 또는 수동으로 재배포

---

## 문제 2: 카드뉴스 문구 생성이 안 됨

### 원인 분석
1. **Gemini API 호출 실패**: API 키 문제 또는 Rate Limit
2. **환경 변수 문제**: `GEMINI_API_KEY`가 올바르지 않음
3. **응답 파싱 실패**: Gemini 응답 형식 문제

### 해결 방법

#### 1. Streamlit Cloud Secrets 확인
1. Streamlit Cloud → **"Settings"** → **"Secrets"**
2. `GEMINI_API_KEY` 확인:
   - 값이 올바른지 확인
   - TOML 형식이 올바른지 확인: `GEMINI_API_KEY = "your-key-here"`

#### 2. Gemini API 키 확인
1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. API 키가 유효한지 확인
3. Rate Limit에 걸리지 않았는지 확인

#### 3. Streamlit 앱 로그 확인
1. Streamlit Cloud → **"Manage app"** → **"Logs"**
2. 카드뉴스 생성 시 오류 메시지 확인:
   - `[Gemini HTTP 오류]` → API 키 문제
   - `[Gemini 응답 경고]` → 응답 형식 문제

#### 4. 수동 테스트
Streamlit 앱에서:
1. 기사 선택
2. **"카드뉴스 문구 생성"** 버튼 클릭
3. 오류 메시지 확인
4. 로그 확인

---

## 문제 3: GitHub Actions 확인

### 현재 상태
- ✅ GitHub Actions는 정상 작동 중 (6개 워크플로우 모두 성공)
- ✅ 매일 오전 9시(한국 시간) 자동 크롤링 실행
- ✅ 수동 실행도 가능 (`workflow_dispatch`)

### 확인 사항
1. **Secrets 설정 확인**:
   - GitHub 저장소 → **"Settings"** → **"Secrets and variables"** → **"Actions"**
   - 다음 Secrets가 설정되어 있는지 확인:
     - `NAVER_CLIENT_ID`
     - `NAVER_CLIENT_SECRET`
     - `GEMINI_API_KEY`
     - `SLACK_WEBHOOK_URL`

2. **크롤링 결과 확인**:
   - `data/daily_recommendations.json` 파일이 업데이트되었는지 확인
   - GitHub Actions 로그에서 크롤링 성공 여부 확인

---

## 종합 진단 체크리스트

### Render (Slack App 서버)
- [ ] 배포 상태: "Live"
- [ ] 로그에 오류 없음
- [ ] 환경 변수 모두 설정됨
- [ ] `/health` 엔드포인트 정상 응답

### Slack App 설정
- [ ] Interactivity Request URL 설정 및 검증 완료
- [ ] Slash Command Request URL 설정 완료
- [ ] Bot Token 및 Signing Secret 올바름

### 기사 데이터
- [ ] `data/daily_recommendations.json` 파일 존재
- [ ] 파일에 기사 데이터 있음
- [ ] 파일 형식 올바름

### Streamlit 앱
- [ ] 환경 변수 설정 완료
- [ ] Gemini API 키 유효
- [ ] 카드뉴스 생성 기능 정상

### GitHub Actions
- [ ] Secrets 설정 완료
- [ ] 워크플로우 정상 실행
- [ ] 크롤링 결과 저장됨

---

## 다음 단계

1. **Render 로그 확인** - `/cardnews` 명령어 실행 시 오류 확인
2. **기사 데이터 확인** - `data/daily_recommendations.json` 파일 확인
3. **Streamlit 앱 로그 확인** - 카드뉴스 생성 오류 확인
4. **환경 변수 재확인** - 모든 환경 변수가 올바른지 확인

---

## 빠른 해결 방법

### `/cardnews` 명령어 문제
1. Render 로그 확인
2. `data/daily_recommendations.json` 파일 확인
3. GitHub Actions로 수동 크롤링 실행

### 카드뉴스 문구 생성 문제
1. Streamlit Cloud Secrets 확인
2. Gemini API 키 유효성 확인
3. Streamlit 앱 로그 확인

---

**문제가 계속되면**: Render 로그와 Streamlit 로그를 확인하여 정확한 오류 메시지를 찾아주세요.

