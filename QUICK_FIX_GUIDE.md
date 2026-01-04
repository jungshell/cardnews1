# 🚀 빠른 해결 가이드

## 문제별 해결 방법

### 1. #ai-news 채널 찾기

**Slack에서 채널 찾는 방법:**

1. **왼쪽 사이드바 확인**
   - Slack 왼쪽에서 "채널" (Channels) 섹션 찾기
   - "#ai-news"가 목록에 있는지 확인

2. **채널이 안 보이면**
   - 왼쪽 사이드바 맨 아래 **"+"** 버튼 클릭
   - **"채널 찾기"** 또는 **"Browse channels"** 클릭
   - 검색창에 **"ai-news"** 입력

3. **채널이 아예 없으면**
   - 새 채널 생성: **"+"** → **"채널 만들기"**
   - 채널 이름: `#ai-news`
   - **중요**: Slack Webhook URL이 이 채널을 가리키는지 확인

---

### 2. Slack 알림 받기

**✅ 네, 맞습니다!**

**방법 3 (Streamlit 앱에서 크롤링)**을 실행하면:
- 크롤링 완료 후 **자동으로 Slack 알림 전송**
- `#ai-news` 채널에 "📰 오늘의 추천 기사" 메시지 전송

**다른 방법들도 동일하게 작동:**
- 방법 1: `test_slack_notification.py` 실행 → Slack 알림
- 방법 2: GitHub Actions 실행 → 크롤링 → Slack 알림

---

### 3. 크롤링 로그에 09시로 나오는 이유

**원인:**
- Streamlit Cloud는 **UTC 시간대**를 사용
- 로그의 "09:14:30"은 실제로는 **UTC 09시** = **한국 시간 18시 (오후 6시)**
- 현재 시간이 오후 5시라면, UTC는 오전 8시 (한국 시간 -9시간)

**해결:**
- `logger.py`는 이미 KST로 설정되어 있지만
- Streamlit Cloud의 시스템 시간이 UTC이므로 로그 시간이 UTC로 표시될 수 있음
- 실제 크롤링 시간은 정확하지만, 표시만 UTC로 나올 수 있음

**확인 방법:**
- 로그의 "09:14:30"이 실제로는 한국 시간 오후 6시 14분일 수 있음
- 크롤링 시간 표시: "26.01.04.(일) 09:15"는 실제로는 오후 6시 15분일 수 있음

---

### 4. 크롤링된 기사와 /cardnews 기사가 다른 이유 ⚠️

**핵심 문제:**

**Streamlit 앱에서 크롤링하면:**
1. ✅ 로컬 `data/daily_recommendations.json`에 저장
2. ❌ **GitHub에 자동 푸시되지 않음**
3. ❌ Render의 `slack_app.py`는 **GitHub 저장소의 파일**을 읽음
4. ❌ 따라서 Render는 **오래된 파일**을 읽을 수 있음

**해결 방법:**

#### 즉시 해결: 크롤링 결과를 GitHub에 푸시

터미널에서 실행:
```bash
cd "/Volumes/Samsung USB/cardnews_3"
git add data/daily_recommendations.json data/history.json
git commit -m "크롤링 결과 업데이트: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
```

#### 권장 방법: GitHub Actions 사용

1. GitHub 저장소 → **"Actions"** 탭
2. **"Daily Crawl and Slack Notification"** 선택
3. 오른쪽 상단 **"Run workflow"** 클릭
4. 크롤링 완료 후 **자동으로 GitHub에 푸시됨**

---

### 5. HTML 태그가 여전히 보임

**원인:**
- `slack_app.py`에 HTML 태그 제거 코드 추가했지만
- **Render에 재배포되지 않음**

**해결:**
1. Render 대시보드 → **"Manual Deploy"** → **"Deploy latest commit"**
2. 배포 완료 대기 (약 2-3분)
3. `/cardnews` 명령어 다시 실행
4. HTML 태그가 제거되었는지 확인

---

## 즉시 해야 할 일 (우선순위)

### 1단계: 크롤링 결과를 GitHub에 푸시 (가장 중요!)

```bash
cd "/Volumes/Samsung USB/cardnews_3"
git add data/daily_recommendations.json data/history.json
git commit -m "크롤링 결과 업데이트"
git push origin main
```

### 2단계: Render 재배포

- Render 대시보드 → **"Manual Deploy"** → **"Deploy latest commit"**

### 3단계: 확인

- Slack에서 `/cardnews` 명령어 실행
- 기사 목록이 최신 크롤링 결과와 일치하는지 확인
- HTML 태그가 제거되었는지 확인

---

## 체크리스트

- [ ] #ai-news 채널 찾기
- [ ] 크롤링 결과를 GitHub에 푸시
- [ ] Render 재배포
- [ ] `/cardnews` 명령어로 기사 목록 확인
- [ ] HTML 태그 제거 확인

