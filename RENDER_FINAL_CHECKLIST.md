# ✅ Render 배포 최종 점검 체크리스트

## 현재 상태
- ✅ 환경 변수 설정 완료
- ⏳ 배포 및 연동 확인 필요

---

## 1단계: 배포 상태 확인

### 1.1 배포 완료 확인
1. Render 대시보드에서 **"Events"** 탭 클릭
2. 최신 배포 상태 확인:
   - ✅ **"Live"** 상태여야 함
   - ❌ "Building" 또는 "Failed"면 대기 또는 오류 확인

### 1.2 로그 확인
1. **"Logs"** 탭 클릭
2. 다음 메시지가 보이면 정상:
   ```
   * Running on http://0.0.0.0:5000
   ```
   또는
   ```
   * Running on all addresses (0.0.0.0)
   ```

### 1.3 서버 상태 테스트
브라우저에서 다음 URL 접속:
```
https://cardnews-slack.onrender.com/health
```
- ✅ 정상: `{"status":"ok","service":"slack_app"}` 응답
- ❌ 오류: 로그 확인 필요

---

## 2단계: 환경 변수 최종 확인

### 2.1 필수 환경 변수 확인 (8개)
**"Environment"** 탭에서 다음 변수들이 모두 있는지 확인:

- [ ] `SLACK_SIGNING_SECRET` - 실제 값 입력됨
- [ ] `SLACK_BOT_TOKEN` - `xoxb-`로 시작하는 실제 토큰
- [ ] `SLACK_WEBHOOK_URL` - 실제 웹훅 URL
- [ ] `NAVER_CLIENT_ID` - 실제 네이버 API ID
- [ ] `NAVER_CLIENT_SECRET` - 실제 네이버 API Secret
- [ ] `GEMINI_API_KEY` - 실제 Gemini API Key
- [ ] `STREAMLIT_APP_URL` - Streamlit 앱 URL
- [ ] `SLACK_APP_URL` - Render 도메인 URL (`https://cardnews-slack.onrender.com`)

### 2.2 값 형식 확인
- 모든 값이 실제 값으로 입력되어 있는지 확인
- 예시 값(`복사한_...`, `기존_...` 등)이 남아있지 않은지 확인

---

## 3단계: Slack App Request URL 설정

### 3.1 Interactivity Request URL 설정
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. 생성한 App 선택
3. 왼쪽 메뉴에서 **"Interactivity & Shortcuts"** 또는 **"Interactivity"** 클릭
4. **"Interactivity"** 섹션에서:
   - **Request URL** 입력란 확인:
     ```
     https://cardnews-slack.onrender.com/slack/interactive
     ```
   - ✅ **초록색 체크 표시**가 나타나면 성공
   - ❌ 실패하면:
     - Render 로그 확인
     - 몇 분 후 다시 시도
   - **"Save Changes"** 클릭

### 3.2 Slash Command Request URL 설정
1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. `/cardnews` 명령어 클릭
3. **Request URL** 입력란 확인:
   ```
   https://cardnews-slack.onrender.com/slack/command
   ```
4. **"Save"** 클릭

---

## 4단계: 기능 테스트

### 4.1 Slash Command 테스트
1. Slack 워크스페이스에서 아무 채널이나 열기
2. `/cardnews` 입력
3. ⏳ **첫 요청 시 슬립 모드에서 깨어나는데 약 30초-1분 소요될 수 있습니다**
4. ✅ **성공**: 기사 목록이 표시됨
5. ❌ **실패**: 
   - Render 로그 확인
   - 환경 변수 확인
   - Slack App Request URL 확인

### 4.2 버튼 클릭 테스트
1. 슬랙 알림 메시지에서 **"📝 카드뉴스 생성"** 버튼 클릭
2. ⏳ 첫 요청 시 깨어나는 시간 대기
3. ✅ **성공**: 카드뉴스가 생성되어 슬랙에 전송됨
4. ❌ **실패**: 
   - Render 로그 확인
   - 환경 변수 확인

### 4.3 요약 보기 테스트
1. 슬랙 알림 메시지에서 **"📄 요약 보기"** 버튼 클릭
2. ✅ **성공**: 요약이 표시됨
3. ❌ **실패**: 로그 확인

---

## 5단계: 오류 발생 시 확인 사항

### 5.1 Render 로그 확인
1. **"Logs"** 탭에서 오류 메시지 확인
2. 주요 오류:
   - `ModuleNotFoundError`: `requirements.txt` 확인
   - `KeyError`: 환경 변수 누락 확인
   - `ConnectionError`: Slack API 연결 문제

### 5.2 환경 변수 오류
- 값이 올바르게 입력되었는지 확인
- 따옴표나 공백이 포함되지 않았는지 확인
- 실제 값인지 확인 (예시 값 아님)

### 5.3 Slack API 오류
- `SLACK_BOT_TOKEN`이 올바른지 확인
- `SLACK_SIGNING_SECRET`이 올바른지 확인
- Slack App이 워크스페이스에 설치되어 있는지 확인

---

## 6단계: 추가 최적화 (선택사항)

### 6.1 슬립 모드 방지 (무료 플랜)
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

### 6.2 모니터링 설정
- **"Metrics"** 탭에서 서비스 상태 모니터링
- **"Logs"** 탭에서 실시간 로그 확인

---

## 📋 최종 체크리스트

### 배포 확인
- [ ] 배포 상태: "Live"
- [ ] 로그에 "Running on http://0.0.0.0:5000" 메시지 확인
- [ ] `/health` 엔드포인트 정상 응답

### 환경 변수
- [ ] 8개 변수 모두 실제 값으로 설정됨
- [ ] 중복 변수 없음
- [ ] `SLACK_APP_URL`이 실제 Render 도메인으로 설정됨

### Slack App 연동
- [ ] Interactivity Request URL 설정 및 검증 완료
- [ ] Slash Command Request URL 설정 완료

### 기능 테스트
- [ ] `/cardnews` 명령어 정상 작동
- [ ] 버튼 클릭으로 카드뉴스 생성 정상 작동
- [ ] 요약 보기 정상 작동

---

## 🎉 완료!

모든 체크리스트를 완료하면:
- ✅ 슬랙에서 `/cardnews` 명령어로 카드뉴스 생성
- ✅ 슬랙 메시지 버튼 클릭으로 카드뉴스 생성
- ✅ 카드뉴스가 슬랙에 자동 전송
- ✅ 요약 보기 기능 정상 작동

---

## 🆘 문제 발생 시

1. **Render 로그 확인** - 가장 먼저 확인
2. **환경 변수 확인** - 값이 올바른지 확인
3. **Slack App 설정 확인** - Request URL이 올바른지 확인
4. **슬립 모드 고려** - 첫 요청 시 시간 소요 가능

---

**다음 단계**: Slack App Request URL 설정 → 테스트

