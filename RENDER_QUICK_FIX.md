# ⚡ Render 설정 빠른 수정 가이드

## 현재 오류: "There's an error above. Please fix it to continue."

---

## 필수 수정 사항

### 1. Name 필드 입력 (필수!)
1. 페이지 상단으로 스크롤
2. **"Name"** 필드 찾기
3. 다음 입력:
   ```
   cardnews-slack
   ```
   - 소문자와 하이픈만 사용 가능

### 2. Start Command 수정 (중요!)
1. **"Start Command"** 필드 찾기
2. 현재 값: `$ gunicorn your_application.wsgi`
3. **전체 삭제** 후 다음으로 변경:
   ```
   python slack_app.py
   ```
   - `$` 기호 없이 입력

### 3. Build Command 확인
1. **"Build Command"** 필드 확인
2. 다음이 입력되어 있는지 확인:
   ```
   pip install -r requirements.txt
   ```
   - `$` 기호 없이 입력

### 4. 기타 설정 확인
- **Language**: `Python 3` ✅
- **Branch**: `main` ✅
- **Region**: `Singapore` ✅
- **Root Directory**: (비워두기) ✅

---

## 환경 변수는 나중에 추가 가능

⚠️ **중요**: 환경 변수는 지금 추가하지 않아도 배포는 시작할 수 있습니다.
- 배포 후 **"Environment"** 탭에서 추가할 수 있습니다
- 또는 지금 추가해도 됩니다 (8개 변수)

---

## 배포 시작

1. 모든 필드 수정 완료 후
2. 페이지 하단의 **"Deploy Web Service"** 버튼 클릭
3. 오류 메시지가 사라지고 배포가 시작됩니다

---

## 환경 변수 추가 (배포 후 또는 지금)

배포가 시작되면 **"Environment"** 탭에서 다음 변수들을 추가:

```
SLACK_SIGNING_SECRET=...
SLACK_BOT_TOKEN=...
SLACK_WEBHOOK_URL=...
NAVER_CLIENT_ID=...
NAVER_CLIENT_SECRET=...
GEMINI_API_KEY=...
STREAMLIT_APP_URL=https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app
SLACK_APP_URL=https://cardnews-slack.onrender.com
```

---

## 체크리스트

- [ ] Name: `cardnews-slack` 입력
- [ ] Start Command: `python slack_app.py` 입력
- [ ] Build Command: `pip install -r requirements.txt` 확인
- [ ] 오류 메시지 사라짐
- [ ] "Deploy Web Service" 버튼 클릭

---

**가장 중요한 것**: **Start Command**를 `python slack_app.py`로 변경하세요!

