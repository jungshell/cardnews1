# 🔍 Slack Command 오류 디버깅 가이드

## 현재 상태
- ❌ `/cardnews` 명령어 실행 시 오류 발생
- 오류 메시지: "{reason} 오류가 발생해 */cardnews*에 실패했습니다."

---

## 즉시 확인할 사항

### 1. Render 로그 확인 (가장 중요!)

1. Render 대시보드 접속
2. **"cardnews-slack"** 서비스 선택
3. **"Logs"** 탭 클릭
4. `/cardnews` 명령어 실행 시점의 로그 확인

#### 확인할 로그 메시지:

**요청 검증 실패 시:**
```
[Slack Command] 요청 검증 실패
```

**기사 데이터 로드 실패 시:**
```
[Slack Command] 기사 로드 오류: ...
```

**기타 오류:**
```
[Slack Command] 처리 오류: ...
```

---

## 가능한 원인 및 해결 방법

### 원인 1: 요청 검증 실패

**증상:**
- 로그에 `[Slack Command] 요청 검증 실패` 메시지

**해결 방법:**
1. Render → **"Environment"** 탭
2. `SLACK_SIGNING_SECRET` 확인:
   - 값이 올바른지 확인
   - Slack App의 Signing Secret과 일치하는지 확인
3. Slack App에서 Signing Secret 재확인:
   - [https://api.slack.com/apps](https://api.slack.com/apps)
   - App 선택 → **"Basic Information"** → **"App Credentials"**
   - Signing Secret 복사 후 Render에 업데이트

---

### 원인 2: 기사 데이터 로드 실패

**증상:**
- 로그에 `[Slack Command] 기사 로드 오류` 메시지
- 또는 `data/daily_recommendations.json` 파일이 없음

**해결 방법:**

#### 방법 1: GitHub Actions로 크롤링 실행
1. GitHub 저장소 → **"Actions"** 탭
2. **"Daily Crawl and Slack Notification"** 워크플로우 선택
3. **"Run workflow"** 버튼 클릭
4. 크롤링 완료 대기 (약 1-2분)

#### 방법 2: Streamlit 앱에서 크롤링 실행
1. Streamlit 앱 접속
2. **"오늘의 자동 추천 기사"** 탭
3. **"🔄 지금 다시 크롤링하기"** 버튼 클릭

#### 방법 3: 파일 확인
1. GitHub 저장소 → **"Code"** 탭
2. `data/daily_recommendations.json` 파일 확인
3. 파일이 비어있거나 형식이 잘못되었을 수 있음

---

### 원인 3: Render 서버 문제

**증상:**
- 로그에 연결 오류 또는 타임아웃

**해결 방법:**
1. Render → **"Events"** 탭
2. 최신 배포 상태 확인
3. **"Redeploy"** 클릭하여 재배포

---

### 원인 4: 슬립 모드

**증상:**
- 첫 요청 시 응답 없음
- 약 30초-1분 후 응답

**해결 방법:**
- Free 플랜의 정상 동작입니다
- 몇 분 후 다시 시도하세요

---

## 단계별 디버깅

### Step 1: Render 로그 확인
1. Render 대시보드 → **"Logs"** 탭
2. `/cardnews` 명령어 실행
3. 로그에서 오류 메시지 확인
4. 오류 메시지를 복사하여 저장

### Step 2: 환경 변수 확인
1. Render → **"Environment"** 탭
2. 다음 변수 확인:
   - `SLACK_SIGNING_SECRET` ✅
   - `SLACK_BOT_TOKEN` ✅
   - `SLACK_WEBHOOK_URL` ✅
   - 기타 필수 변수 ✅

### Step 3: 기사 데이터 확인
1. GitHub 저장소 → `data/daily_recommendations.json` 확인
2. 파일이 존재하는지 확인
3. 파일 내용이 올바른지 확인

### Step 4: 크롤링 실행
1. GitHub Actions 또는 Streamlit 앱에서 크롤링 실행
2. 크롤링 완료 후 `/cardnews` 명령어 다시 시도

---

## 체크리스트

### 즉시 확인
- [ ] Render 로그 확인 (가장 중요!)
- [ ] 오류 메시지 복사 및 저장
- [ ] 환경 변수 확인

### 문제 해결
- [ ] 요청 검증 실패 → Signing Secret 확인
- [ ] 기사 데이터 없음 → 크롤링 실행
- [ ] 서버 문제 → 재배포

---

## 로그 확인 방법

### Render 로그 접근
1. [https://dashboard.render.com](https://dashboard.render.com) 접속
2. **"cardnews-slack"** 서비스 클릭
3. **"Logs"** 탭 클릭
4. 실시간 로그 확인

### 로그 필터링
- **"Q Search"** 입력란에 `Slack Command` 입력
- 관련 로그만 필터링하여 확인

---

## 다음 단계

1. **Render 로그 확인** - 오류 메시지 확인
2. **오류 메시지 공유** - 정확한 원인 파악
3. **문제 해결** - 원인에 따른 해결 방법 적용

---

**가장 중요한 것**: Render 로그를 확인하여 정확한 오류 메시지를 찾아주세요!

