# 🎯 Render 배포 다음 단계 가이드

## 현재 상태
- ✅ 배포 진행 중 (Building 상태)
- ✅ 패키지 설치 완료
- ⏳ 서비스 시작 대기 중

---

## 1단계: 배포 완료 대기 (약 2-3분)

### 확인 사항
1. **"Events"** 탭에서 배포 상태 확인
2. 다음 메시지들이 순서대로 나타납니다:
   - ✅ "Building" → "Starting service" → "Deploy successful"
3. 상태가 **"Live"**로 변경되면 완료!

### 로그 확인
- **"Logs"** 탭에서 실시간 로그 확인
- 다음 메시지가 보이면 정상:
   ```
   * Running on http://0.0.0.0:5000
   ```
   또는
   ```
   * Running on all addresses (0.0.0.0)
   ```

---

## 2단계: 환경 변수 설정 (배포 완료 후 또는 지금)

### 2.1 Environment 탭 이동
1. 왼쪽 메뉴에서 **"Environment"** 클릭
2. 또는 상단의 **"MANAGE"** 섹션에서 **"Environment"** 클릭

### 2.2 환경 변수 추가
**"Add Environment Variable"** 버튼을 클릭하여 다음 변수들을 하나씩 추가:

#### 필수 환경 변수 (8개)

1. **SLACK_SIGNING_SECRET**
   - **Key**: `SLACK_SIGNING_SECRET`
   - **Value**: Slack App의 Signing Secret (이전에 복사한 값)
   - **Add** 클릭

2. **SLACK_BOT_TOKEN**
   - **Key**: `SLACK_BOT_TOKEN`
   - **Value**: `xoxb-`로 시작하는 Bot User OAuth Token
   - **Add** 클릭

3. **SLACK_WEBHOOK_URL**
   - **Key**: `SLACK_WEBHOOK_URL`
   - **Value**: 기존 Slack 웹훅 URL
   - **Add** 클릭

4. **NAVER_CLIENT_ID**
   - **Key**: `NAVER_CLIENT_ID`
   - **Value**: 네이버 검색 API Client ID
   - **Add** 클릭

5. **NAVER_CLIENT_SECRET**
   - **Key**: `NAVER_CLIENT_SECRET`
   - **Value**: 네이버 검색 API Client Secret
   - **Add** 클릭

6. **GEMINI_API_KEY**
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Google Gemini API Key
   - **Add** 클릭

7. **STREAMLIT_APP_URL**
   - **Key**: `STREAMLIT_APP_URL`
   - **Value**: `https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app`
   - **Add** 클릭

8. **SLACK_APP_URL**
   - **Key**: `SLACK_APP_URL`
   - **Value**: `https://cardnews-slack.onrender.com`
   - ⚠️ **실제 도메인으로 확인 후 업데이트 필요**
   - **Add** 클릭

### 2.3 환경 변수 확인
- 모든 변수가 **"Environment Variables"** 섹션에 표시되는지 확인
- 값이 올바르게 입력되었는지 확인

### 2.4 재배포 (환경 변수 추가 후)
환경 변수를 추가하면 자동으로 재배포가 시작됩니다:
1. **"Events"** 탭으로 이동
2. 새로운 배포가 시작되는지 확인
3. 배포 완료 대기 (약 2-3분)

---

## 3단계: 도메인 확인 및 SLACK_APP_URL 업데이트

### 3.1 도메인 확인
1. 서비스 페이지 상단에서 도메인 확인
2. 형식: `https://cardnews-slack.onrender.com`
   - (또는 설정한 이름에 따라 다를 수 있음)
3. 📋 **이 URL을 복사해두세요!**

### 3.2 SLACK_APP_URL 업데이트
1. **"Environment"** 탭으로 이동
2. `SLACK_APP_URL` 변수 찾기
3. **"Edit"** 클릭 (또는 변수 옆의 연필 아이콘)
4. Value를 실제 Render 도메인으로 업데이트:
   ```
   https://cardnews-slack.onrender.com
   ```
   - (실제 생성된 도메인으로 변경)
5. **"Save Changes"** 클릭
6. 서비스가 자동으로 재배포됩니다 (약 2-3분)

---

## 4단계: 배포 확인 및 테스트

### 4.1 로그 확인
1. **"Logs"** 탭 클릭
2. 다음 메시지가 보이면 정상:
   ```
   * Running on http://0.0.0.0:5000
   ```

### 4.2 서버 상태 확인
1. 브라우저에서 Render 도메인 접속:
   ```
   https://cardnews-slack.onrender.com
   ```
2. **"Not Found"** 또는 **"404"** 에러가 나오면 정상
   - (루트 경로는 없고 `/slack/interactive`, `/slack/command`만 있음)

### 4.3 Health Check
브라우저에서 다음 URL 접속:
```
https://cardnews-slack.onrender.com/health
```
- 정상이면 `{"status":"ok","service":"slack_app"}` 응답이 표시됩니다

---

## 5단계: Slack App Request URL 설정

### 5.1 Interactivity Request URL 설정
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. 생성한 App 선택
3. 왼쪽 메뉴에서 **"Interactivity & Shortcuts"** 또는 **"Interactivity"** 클릭
4. **"Interactivity"** 섹션에서:
   - **Request URL** 입력란에 다음 입력:
     ```
     https://cardnews-slack.onrender.com/slack/interactive
     ```
     - (실제 Render 도메인으로 변경)
5. Slack이 자동으로 URL 검증 시도
   - ⚠️ **첫 요청 시 슬립 모드에서 깨어나는데 시간이 걸릴 수 있습니다** (약 30초-1분)
   - ✅ **초록색 체크 표시**가 나타나면 성공
   - ❌ 실패하면:
     - Render 로그 확인
     - 몇 분 후 다시 시도
6. **"Save Changes"** 클릭

### 5.2 Slash Command Request URL 설정
1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. `/cardnews` 명령어 클릭
3. **Request URL** 입력란에 다음 입력:
   ```
   https://cardnews-slack.onrender.com/slack/command
   ```
   - (실제 Render 도메인으로 변경)
4. **"Save"** 클릭

---

## 6단계: 최종 테스트

### 6.1 Slash Command 테스트
1. Slack 워크스페이스에서 아무 채널이나 열기
2. `/cardnews` 입력
3. ⏳ **첫 요청 시 슬립 모드에서 깨어나는데 약 30초-1분 소요될 수 있습니다**
4. 기사 목록이 표시되면 성공! ✅

### 6.2 버튼 클릭 테스트
1. 슬랙 알림 메시지에서 **"📝 카드뉴스 생성"** 버튼 클릭
2. ⏳ 첫 요청 시 깨어나는 시간 대기
3. 카드뉴스가 생성되어 슬랙에 전송되면 성공! ✅

---

## 📋 체크리스트

### 배포 완료
- [ ] 배포 상태가 "Live"로 변경됨
- [ ] 로그에 "Running on http://0.0.0.0:5000" 메시지 확인
- [ ] 도메인 URL 확인 및 복사

### 환경 변수 설정
- [ ] Environment 탭으로 이동
- [ ] 환경 변수 8개 모두 추가
- [ ] SLACK_APP_URL을 실제 도메인으로 업데이트
- [ ] 재배포 완료 대기

### Slack App 연동
- [ ] Interactivity Request URL 설정
- [ ] URL 검증 완료 (✅ 표시, 첫 요청 시 시간 소요 가능)
- [ ] Slash Command Request URL 설정

### 테스트
- [ ] `/cardnews` 명령어 테스트 (첫 요청 시 깨어나는 시간 고려)
- [ ] 버튼 클릭 테스트
- [ ] 카드뉴스 생성 확인

---

## ⚠️ 중요 사항

### 슬립 모드 (Free 플랜)
- **15분 동안 요청이 없으면 서비스가 슬립 모드로 전환됩니다**
- 첫 요청 시 깨어나는데 약 **30초-1분** 소요될 수 있습니다
- 이후 요청은 즉시 처리됩니다

### Request URL 검증
- Slack이 자동으로 URL을 검증합니다
- 첫 요청 시 슬립 모드에서 깨어나는 시간을 고려하세요
- 검증 실패 시:
  1. Render 로그 확인 (Logs 탭)
  2. 몇 분 후 다시 시도
  3. URL이 정확한지 확인 (오타 없이)

---

## 🎉 완료!

모든 설정이 완료되면:
- ✅ 슬랙에서 `/cardnews` 명령어로 카드뉴스 생성
- ✅ 슬랙 메시지 버튼 클릭으로 카드뉴스 생성
- ✅ 카드뉴스가 슬랙에 자동 전송

---

**현재**: 배포 완료 대기 중 → 환경 변수 설정 준비

