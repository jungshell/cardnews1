# 🚀 Slack App 생성 단계별 가이드

## 현재 상태
- Slack API 페이지에 접속했지만 아직 로그인하지 않은 상태입니다.

---

## 1단계: Slack 계정으로 로그인

1. 페이지에서 **"sign in to your Slack account"** 링크 클릭
   - 또는 상단 오른쪽의 **"Go to Slack"** 버튼 클릭
2. Slack 워크스페이스 계정으로 로그인
3. 로그인 후 다시 [https://api.slack.com/apps](https://api.slack.com/apps) 접속

---

## 2단계: 새 App 생성

1. 로그인 후 페이지 상단에 **"Create New App"** 버튼이 보입니다
2. **"Create New App"** 클릭
3. **"From scratch"** 선택
4. 설정 입력:
   - **App Name**: `카드뉴스 자동화` (원하는 이름)
   - **Pick a workspace**: 카드뉴스를 받을 슬랙 워크스페이스 선택
5. **"Create App"** 버튼 클릭

---

## 3단계: Interactive Components 활성화

App을 생성하면 왼쪽에 메뉴가 나타납니다:

### 왼쪽 메뉴에서 찾기:
1. **"Interactivity & Shortcuts"** 또는 **"Interactivity"** 클릭
   - (메뉴 이름이 버전에 따라 다를 수 있음)
2. 페이지 상단의 **"Interactivity"** 토글을 **ON**으로 변경
3. **Request URL** 입력란:
   - 일단 비워두세요 (나중에 Railway 배포 후 입력)
   - 또는 임시로 `https://example.com` 입력 후 저장
4. **"Save Changes"** 버튼 클릭

---

## 4단계: Slash Commands 추가

1. 왼쪽 메뉴에서 **"Slash Commands"** 클릭
2. **"Create New Command"** 버튼 클릭
3. 설정 입력:
   - **Command**: `/cardnews`
   - **Request URL**: 일단 비워두거나 `https://example.com` 입력
   - **Short Description**: `카드뉴스 생성`
   - **Usage Hint**: `[기사 번호]` (선택사항)
4. **"Save"** 버튼 클릭

---

## 5단계: OAuth & Permissions 설정

1. 왼쪽 메뉴에서 **"OAuth & Permissions"** 클릭
2. **"Bot Token Scopes"** 섹션에서 **"Add an OAuth Scope"** 클릭
3. 다음 스코프들을 하나씩 추가:
   - `chat:write` (메시지 전송)
   - `commands` (Slash Commands)
   - `users:read` (사용자 정보)
4. 페이지 상단으로 스크롤
5. **"Install to Workspace"** 버튼 클릭
6. 권한 확인 후 **"Allow"** 클릭

---

## 6단계: 토큰 및 Secret 복사

### Bot User OAuth Token 복사
1. **"OAuth & Permissions"** 페이지에서
2. **"Bot User OAuth Token"** 섹션 찾기
3. `xoxb-`로 시작하는 긴 문자열 복사
   - 📋 **이 값을 Railway 환경 변수 `SLACK_BOT_TOKEN`에 사용합니다**

### Signing Secret 복사
1. 왼쪽 메뉴에서 **"Basic Information"** 클릭
2. **"App Credentials"** 섹션으로 스크롤
3. **"Signing Secret"** 옆의 **"Show"** 버튼 클릭
4. 표시된 Secret 복사
   - 📋 **이 값을 Railway 환경 변수 `SLACK_SIGNING_SECRET`에 사용합니다**

---

## 7단계: Request URL 설정 (Railway 배포 후)

Railway 배포가 완료되면:

1. **Interactivity** 페이지로 돌아가기
2. **Request URL** 입력:
   ```
   https://your-railway-url.railway.app/slack/interactive
   ```
3. Slack이 자동으로 검증 (✅ 표시)
4. **"Save Changes"** 클릭

5. **Slash Commands** 페이지로 이동
6. `/cardnews` 명령어 클릭
7. **Request URL** 입력:
   ```
   https://your-railway-url.railway.app/slack/command
   ```
8. **"Save"** 클릭

---

## 📋 체크리스트

- [ ] Slack 계정 로그인 완료
- [ ] App 생성 완료
- [ ] Interactive Components 활성화
- [ ] Slash Commands 추가 (`/cardnews`)
- [ ] OAuth & Permissions 설정
- [ ] Bot Token 복사 완료
- [ ] Signing Secret 복사 완료
- [ ] Railway 배포 완료 후 Request URL 설정

---

## ⚠️ 주의사항

- **Request URL은 HTTPS여야 합니다** (HTTP 불가)
- Railway 배포 전에는 임시 URL을 입력하거나 비워둘 수 있습니다
- 배포 후 반드시 실제 URL로 업데이트해야 합니다

---

## 🆘 문제 해결

### "Interactivity" 메뉴가 안 보여요
- App을 먼저 생성했는지 확인
- 왼쪽 메뉴를 스크롤해서 찾아보세요
- 메뉴 이름이 **"Interactivity & Shortcuts"**일 수도 있습니다

### Request URL 검증 실패
- 서버가 정상 실행 중인지 확인
- HTTPS URL인지 확인
- Railway 로그 확인

---

**다음 단계**: Railway 배포 → `USER_TASKS.md` 참고

