# 🔧 모든 문제 해결 가이드

## 문제 1: #ai-news 채널 찾기

### Slack에서 채널 찾는 방법

1. **왼쪽 사이드바에서 "채널" 섹션 확인**
   - Slack 왼쪽 사이드바에서 "채널" (Channels) 섹션 찾기
   - "#ai-news" 채널이 목록에 있는지 확인

2. **채널이 안 보이면**:
   - 왼쪽 사이드바 맨 아래 "+" 버튼 클릭
   - "채널 찾기" 또는 "Browse channels" 클릭
   - "ai-news" 검색

3. **채널이 아예 없으면**:
   - 새 채널 생성: "+" 버튼 → "채널 만들기"
   - 채널 이름: `#ai-news`
   - Slack Webhook URL이 이 채널을 가리키는지 확인

---

## 문제 2: Slack 알림 받기

### ✅ 네, 맞습니다!

**방법 3 (Streamlit 앱에서 크롤링)**을 실행하면:
1. 크롤링 실행
2. `daily_recommendations.json`에 저장
3. **자동으로 Slack 알림 전송** (`send_slack_notification()` 호출)

**다른 방법들**:
- **방법 1 (로컬 테스트)**: `test_slack_notification.py` 실행 → Slack 알림 전송
- **방법 2 (GitHub Actions)**: 워크플로우 실행 → 크롤링 → Slack 알림 전송

---

## 문제 3: 크롤링 로그에 09시로 나오는 이유

### 원인
- Streamlit Cloud는 **UTC 시간대**를 사용
- 크롤링 로그는 `logger.py`의 KST 포맷터를 사용하지만, 실제 시간은 UTC 기준
- 로그에 표시되는 시간이 UTC일 수 있음

### 확인 필요
- 로그의 "09:14:30"이 UTC인지 KST인지 확인
- 현재 시간이 오후 5시라면, UTC는 오전 8시 (한국 시간 -9시간)
- 로그의 "09:14:30"이 실제로는 한국 시간 오후 6시 14분일 수 있음

### 해결
- `logger.py`는 이미 KST로 설정되어 있음
- 하지만 Streamlit Cloud의 시스템 시간이 UTC일 수 있음
- 로그 시간을 명시적으로 KST로 변환하도록 수정 필요

---

## 문제 4: 크롤링된 기사와 /cardnews 기사가 다름

### 원인 분석

**Streamlit 앱에서 크롤링하면**:
1. 로컬 `data/daily_recommendations.json`에 저장
2. **GitHub에 자동 푸시되지 않음**
3. Render의 `slack_app.py`는 GitHub 저장소의 파일을 읽음
4. 따라서 Render는 **오래된 파일**을 읽을 수 있음

**해결 방법**:

#### 방법 1: 크롤링 후 수동으로 GitHub에 푸시 (임시)
```bash
cd "/Volumes/Samsung USB/cardnews_3"
git add data/daily_recommendations.json data/history.json
git commit -m "크롤링 결과 업데이트"
git push origin main
```

#### 방법 2: GitHub Actions 사용 (권장)
- GitHub Actions가 크롤링하면 자동으로 GitHub에 푸시됨
- "Actions" 탭 → "Run workflow" 클릭

#### 방법 3: Streamlit 앱에서 크롤링 후 자동 푸시 추가 (향후 개선)
- 크롤링 완료 후 자동으로 GitHub에 커밋/푸시하는 기능 추가

---

## 문제 5: HTML 태그가 여전히 보임

### 원인
- `slack_app.py`에 HTML 태그 제거 코드를 추가했지만
- **Render에 재배포되지 않음**

### 해결
1. Render 대시보드 → "Manual Deploy" → "Deploy latest commit"
2. 배포 완료 대기 (약 2-3분)
3. `/cardnews` 명령어 다시 실행
4. HTML 태그가 제거되었는지 확인

---

## 즉시 해야 할 일

### 1. 크롤링 결과를 GitHub에 푸시
```bash
cd "/Volumes/Samsung USB/cardnews_3"
git add data/daily_recommendations.json data/history.json
git commit -m "크롤링 결과 업데이트: $(date +'%Y-%m-%d')"
git push origin main
```

### 2. Render 재배포
- Render 대시보드 → "Manual Deploy" → "Deploy latest commit"

### 3. Slack에서 확인
- `/cardnews` 명령어 실행
- 기사 목록이 최신 크롤링 결과와 일치하는지 확인
- HTML 태그가 제거되었는지 확인

---

## 체크리스트

- [ ] #ai-news 채널 찾기
- [ ] 크롤링 결과를 GitHub에 푸시
- [ ] Render 재배포
- [ ] `/cardnews` 명령어로 기사 목록 확인
- [ ] HTML 태그 제거 확인
- [ ] 크롤링 로그 시간 확인

