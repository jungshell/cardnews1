# 🧪 Slack 알림 테스트 가이드

## 매일 오전 9시 자동 실행 확인

### ✅ 현재 설정
- **GitHub Actions**: 매일 UTC 0시 (한국 시간 오전 9시)에 자동 실행
- **크롤링**: 네이버 뉴스에서 기사 수집
- **Slack 알림**: 상위 5개 기사를 `#ai-news` 채널로 전송

### 📅 실행 시간
- **자동 실행**: 매일 오전 9시 (한국 시간)
- **수동 실행**: GitHub Actions에서 "Run workflow" 버튼 클릭

---

## 지금 테스트로 받아보기

### 방법 1: 로컬에서 테스트 (추천)

1. **터미널에서 실행**:
```bash
cd "/Volumes/Samsung USB/cardnews_3"
python test_slack_notification.py
```

2. **결과 확인**:
   - Slack의 `#ai-news` 채널 확인
   - "📰 오늘의 추천 기사" 메시지 확인
   - 상위 5개 기사가 표시되는지 확인

---

### 방법 2: GitHub Actions 수동 실행

1. **GitHub 저장소 접속**:
   - https://github.com/jungshell/cardnews1 접속

2. **Actions 탭 클릭**:
   - 상단 메뉴에서 "Actions" 클릭

3. **워크플로우 선택**:
   - 왼쪽 사이드바에서 "Daily Crawl and Slack Notification" 클릭

4. **수동 실행**:
   - 오른쪽 상단의 "Run workflow" 버튼 클릭
   - "Run workflow" 드롭다운에서 "Run workflow" 클릭

5. **실행 확인**:
   - 워크플로우 실행 상태 확인
   - 완료되면 Slack에서 알림 확인

---

### 방법 3: Streamlit 앱에서 크롤링 실행

1. **Streamlit 앱 접속**:
   - https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app

2. **크롤링 실행**:
   - "지금 다시 크롤링하기" 버튼 클릭
   - 크롤링 완료 대기

3. **Slack 알림 확인**:
   - 크롤링 완료 후 자동으로 Slack 알림 전송
   - `#ai-news` 채널 확인

---

## HTML 태그 제거 확인

### ✅ 수정 완료
- `slack_app.py`에 `clean_html_tags()` 함수 추가
- `/cardnews` 명령어에서 제목 표시 시 HTML 태그 제거
- `handle_create_cardnews()`에서 제목/설명 HTML 태그 제거
- `handle_view_summary()`에서 제목/설명 HTML 태그 제거

### 확인 방법
1. `/cardnews` 명령어 실행
2. 기사 제목에 `<b>`, `</b>` 같은 태그가 없는지 확인
3. 매일 오전 9시 알림에서도 HTML 태그가 없는지 확인

---

## 예상 결과

### Slack 알림 형식
```
📰 오늘의 추천 기사
─────────────────────

1. 충남콘텐츠진흥원, 충남콘텐츠코리아랩 육성기업 문체부장관상 등 전국적 성과 창출
📅 2025.11.27 (수)  |  📊 관련도: 4.7/10점

[기사 설명...]

📄 요약:
[요약 내용...]

[📄 요약 보기] [📝 카드뉴스 생성]
─────────────────────
```

---

## 문제 해결

### 문제 1: "기사 데이터가 없습니다"
**해결**: 먼저 크롤링을 실행하세요.
- Streamlit 앱에서 "지금 다시 크롤링하기" 버튼 클릭
- 또는 GitHub Actions 수동 실행

### 문제 2: "Slack 알림 전송 실패"
**해결**: 환경 변수 확인
- `SLACK_WEBHOOK_URL`이 올바르게 설정되었는지 확인
- GitHub Secrets에 `SLACK_WEBHOOK_URL`이 있는지 확인

### 문제 3: HTML 태그가 여전히 보임
**해결**: 코드가 업데이트되었는지 확인
- GitHub에 최신 코드가 푸시되었는지 확인
- Render에서 재배포되었는지 확인

---

## 체크리스트

- [x] HTML 태그 제거 함수 추가
- [x] `/cardnews` 명령어에서 HTML 태그 제거 적용
- [x] 테스트 스크립트 생성
- [ ] 로컬에서 테스트 실행
- [ ] Slack 알림 확인
- [ ] HTML 태그 제거 확인

