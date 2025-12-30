# 🎨 Render 배포 완벽 가이드

## 현재 상태
- ✅ Slack App 생성 완료
- ✅ Bot Token, Signing Secret 복사 완료
- ⏳ Render 배포 진행 중

---

## Render 장점
- ✅ **완전 무료** (프로젝트 제한 없음)
- ✅ 간단한 설정
- ✅ 자동 HTTPS
- ✅ GitHub 연동으로 자동 배포
- ⚠️ 15분 비활성 시 슬립 모드 (첫 요청 시 자동 깨어남)

---

## 1단계: Render 계정 생성

### 1.1 Render 접속
1. [https://render.com/](https://render.com/) 접속
2. **"Get Started for Free"** 버튼 클릭
   - 또는 상단 오른쪽의 **"Sign Up"** 클릭

### 1.2 GitHub로 로그인
1. **"Sign up with GitHub"** 선택
2. GitHub 계정으로 로그인
3. Render가 GitHub 저장소에 접근할 수 있도록 권한 승인
   - ✅ **"Authorize Render"** 클릭

### 1.3 이메일 확인 (선택사항)
- 이메일 인증을 요청할 수 있지만, 바로 진행 가능

---

## 2단계: 새 Web Service 생성

### 2.1 대시보드에서 시작
1. Render 대시보드 접속
2. 상단 오른쪽의 **"New +"** 버튼 클릭
3. **"Web Service"** 선택

### 2.2 GitHub 저장소 연결
1. **"Connect account"** 또는 **"Connect GitHub"** 클릭 (처음이라면)
2. GitHub 계정 권한 승인
3. 저장소 목록에서 `jungshell/cardnews1` 찾기
4. 저장소 클릭하여 선택

---

## 3단계: Web Service 설정

### 3.1 기본 설정
다음 정보를 입력:

- **Name**: `cardnews-slack` (원하는 이름, 소문자와 하이픈만 사용)
- **Region**: `Singapore` 선택 (한국과 가장 가까운 지역)
- **Branch**: `main` (기본값)
- **Root Directory**: (비워두기 - 루트에서 실행)
- **Runtime**: `Python 3` 선택
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  python slack_app.py
  ```

### 3.2 Plan 선택
- **Free** 플랜 선택 (기본값)
  - 512MB RAM
  - 0.1 CPU
  - 무료

### 3.3 고급 설정 (선택사항)
- **Auto-Deploy**: `Yes` (기본값) - GitHub 푸시 시 자동 배포
- **Health Check Path**: (비워두기)

---

## 4단계: 환경 변수 설정 (중요!)

### 4.1 환경 변수 추가
설정 페이지에서 **"Environment"** 섹션으로 스크롤

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
   - ⚠️ **나중에 업데이트 필요** (배포 완료 후 실제 도메인으로 변경)
   - **Add** 클릭

9. **PORT** (선택사항, 자동 설정됨)
   - Render는 자동으로 `PORT` 환경 변수를 설정합니다
   - `slack_app.py`가 이미 `PORT` 환경 변수를 사용하도록 설정되어 있음
   - 추가 설정 불필요

### 4.2 환경 변수 확인
- 모든 변수가 **"Environment Variables"** 섹션에 표시되는지 확인
- 값이 올바르게 입력되었는지 확인

---

## 5단계: 서비스 생성 및 배포

### 5.1 서비스 생성
1. 모든 설정이 완료되었는지 확인
2. 페이지 하단의 **"Create Web Service"** 버튼 클릭
3. 배포가 자동으로 시작됩니다

### 5.2 배포 진행 상황 확인
1. **"Events"** 탭에서 배포 로그 확인
2. 다음 단계들이 순서대로 진행됩니다:
   - **"Cloning repository"**
   - **"Building service"**
   - **"Starting service"**
   - **"Deploy successful"** ✅

### 5.3 배포 완료 대기
- ⏳ 약 5-10분 소요
- 배포가 완료되면 **"Live"** 상태로 변경됩니다

---

## 6단계: 도메인 확인 및 업데이트

### 6.1 도메인 확인
1. 서비스 페이지 상단에서 도메인 확인
2. 형식: `https://cardnews-slack.onrender.com`
   - (또는 설정한 이름에 따라 다를 수 있음)
3. 📋 **이 URL을 복사해두세요!**

### 6.2 SLACK_APP_URL 업데이트
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

## 7단계: 배포 확인 및 테스트

### 7.1 로그 확인
1. **"Logs"** 탭 클릭
2. 다음 메시지가 보이면 정상:
   ```
   * Running on http://0.0.0.0:5000
   ```
   또는
   ```
   * Running on all addresses (0.0.0.0)
   ```

### 7.2 서버 상태 확인
1. 브라우저에서 Render 도메인 접속:
   ```
   https://cardnews-slack.onrender.com
   ```
2. **"Not Found"** 또는 **"404"** 에러가 나오면 정상
   - (루트 경로는 없고 `/slack/interactive`, `/slack/command`만 있음)

### 7.3 Health Check (선택사항)
브라우저에서 다음 URL 접속:
```
https://cardnews-slack.onrender.com/health
```
- 정상이면 간단한 응답이 표시됩니다

---

## 8단계: Slack App Request URL 설정

### 8.1 Interactivity Request URL 설정
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

### 8.2 Slash Command Request URL 설정
1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. `/cardnews` 명령어 클릭
3. **Request URL** 입력란에 다음 입력:
   ```
   https://cardnews-slack.onrender.com/slack/command
   ```
   - (실제 Render 도메인으로 변경)
4. **"Save"** 클릭

---

## 9단계: 최종 테스트

### 9.1 Slash Command 테스트
1. Slack 워크스페이스에서 아무 채널이나 열기
2. `/cardnews` 입력
3. ⏳ **첫 요청 시 슬립 모드에서 깨어나는데 약 30초-1분 소요될 수 있습니다**
4. 기사 목록이 표시되면 성공! ✅

### 9.2 버튼 클릭 테스트
1. 슬랙 알림 메시지에서 **"📝 카드뉴스 생성"** 버튼 클릭
2. ⏳ 첫 요청 시 깨어나는 시간 대기
3. 카드뉴스가 생성되어 슬랙에 전송되면 성공! ✅

---

## 📋 체크리스트

### Render 설정
- [ ] Render 계정 생성 (GitHub 연동)
- [ ] Web Service 생성
- [ ] GitHub 저장소 연결
- [ ] Build Command 설정 (`pip install -r requirements.txt`)
- [ ] Start Command 설정 (`python slack_app.py`)
- [ ] 환경 변수 8개 모두 추가
- [ ] 서비스 생성 및 배포 완료
- [ ] 도메인 URL 확인 및 복사
- [ ] SLACK_APP_URL 업데이트

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

### 환경 변수 값 준비
다음 값들을 미리 준비해두세요:
1. **SLACK_SIGNING_SECRET** - Slack App의 Signing Secret
2. **SLACK_BOT_TOKEN** - Slack App의 Bot User OAuth Token (xoxb-로 시작)
3. **SLACK_WEBHOOK_URL** - 기존 웹훅 URL
4. **NAVER_CLIENT_ID** - 네이버 API 키
5. **NAVER_CLIENT_SECRET** - 네이버 API Secret
6. **GEMINI_API_KEY** - Gemini API 키

### URL 형식
- Render 도메인은 항상 `https://`로 시작
- 마지막에 `/` 없이 입력
- 예: `https://cardnews-slack.onrender.com`

### 슬립 모드 (Free 플랜)
- **15분 동안 요청이 없으면 서비스가 슬립 모드로 전환됩니다**
- 첫 요청 시 깨어나는데 약 **30초-1분** 소요될 수 있습니다
- 이후 요청은 즉시 처리됩니다
- **해결책**: 
  - 정기적으로 요청 보내기 (예: GitHub Actions로 주기적 ping)
  - 또는 Hobby 플랜 ($7/월)으로 업그레이드 (항상 활성 상태)

### Request URL 검증
- Slack이 자동으로 URL을 검증합니다
- 첫 요청 시 슬립 모드에서 깨어나는 시간을 고려하세요
- 검증 실패 시:
  1. Render 서버가 실행 중인지 확인 (Logs 탭)
  2. 몇 분 후 다시 시도
  3. URL이 정확한지 확인 (오타 없이)

---

## 🆘 문제 해결

### 배포가 실패해요
1. **"Events"** 탭에서 로그 확인
2. 환경 변수가 모두 설정되었는지 확인
3. Build Command와 Start Command가 올바른지 확인
4. `requirements.txt`에 `flask`가 포함되어 있는지 확인

### Request URL 검증 실패
1. Render 로그 확인:
   - **"Logs"** 탭에서 실시간 로그 확인
2. 서버가 정상 실행 중인지 확인:
   - `* Running on http://0.0.0.0:5000` 메시지 확인
3. 슬립 모드일 수 있으므로 몇 분 후 다시 시도
4. HTTPS URL인지 확인 (HTTP 불가)
5. URL에 오타가 없는지 확인

### 환경 변수가 적용 안 돼요
1. 변수 추가 후 **"Manual Deploy"** → **"Deploy latest commit"** 클릭
2. 또는 GitHub에 푸시하면 자동 재배포됩니다

### 슬랙에서 응답이 없어요
1. Render 로그 확인 (슬립 모드일 수 있음)
2. 첫 요청 후 30초-1분 대기
3. 환경 변수 (특히 `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`) 확인
4. Slack App의 Request URL이 올바른지 확인

### 슬립 모드가 너무 자주 발생해요
**해결책:**
1. **Hobby 플랜 ($7/월)**로 업그레이드 - 항상 활성 상태
2. **무료로 유지**: GitHub Actions로 주기적으로 ping 보내기
   - 예: 매 10분마다 `/health` 엔드포인트 호출

---

## 💡 팁

### 자동 배포
- GitHub에 푸시하면 자동으로 재배포됩니다
- 수동 재배포: **"Manual Deploy"** → **"Deploy latest commit"**

### 로그 확인
- 실시간 로그: **"Logs"** 탭
- 배포 로그: **"Events"** 탭
- 오류 발생 시 로그를 먼저 확인하세요

### 무료 플랜 제한
- 15분 비활성 시 슬립 모드
- 첫 요청 시 깨어나는 시간: 약 30초-1분
- 월 750시간 제공 (충분함)

### 슬립 모드 방지 (무료)
GitHub Actions로 주기적으로 ping 보내기:
```yaml
# .github/workflows/keep-alive.yml
name: Keep Render Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # 10분마다
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render
        run: |
          curl https://cardnews-slack.onrender.com/health
```

---

## 🎉 완료!

모든 설정이 완료되면:
- ✅ 슬랙에서 `/cardnews` 명령어로 카드뉴스 생성
- ✅ 슬랙 메시지 버튼 클릭으로 카드뉴스 생성
- ✅ 카드뉴스가 슬랙에 자동 전송

**예상 소요 시간: 약 20-30분**

---

**다음 단계**: Slack App Request URL 설정 → 테스트

