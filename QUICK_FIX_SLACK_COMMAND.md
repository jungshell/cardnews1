# ⚡ Slack Command 빠른 해결

## 현재 상태 분석

### 로그 분석
- ✅ 서버 정상 작동: HTTP 200 응답
- ✅ 요청 수신: `/slack/command` POST 요청 처리됨
- ⚠️ 기사 데이터 없음 가능성 높음

### 문제 원인
로그에 `[Slack Command]` 메시지가 보이지 않는 것은:
1. **기사 데이터가 없어서** "추천 기사가 없습니다" 메시지 반환
2. 또는 로그가 더 아래에 있을 수 있음

---

## 즉시 해결 방법

### 방법 1: 크롤링 실행 (가장 중요!)

#### GitHub Actions로 실행
1. GitHub 저장소 → **"Actions"** 탭
2. **"Daily Crawl and Slack Notification"** 워크플로우 선택
3. **"Run workflow"** 버튼 클릭
4. 크롤링 완료 대기 (약 1-2분)
5. `/cardnews` 명령어 다시 시도

#### Streamlit 앱에서 실행
1. Streamlit 앱 접속
2. **"오늘의 자동 추천 기사"** 탭
3. **"🔄 지금 다시 크롤링하기"** 버튼 클릭
4. 크롤링 완료 후 `/cardnews` 명령어 다시 시도

---

### 방법 2: 로그 더 자세히 확인

Render 로그에서:
1. **"Search"** 입력란에 `Slack Command` 입력
2. 관련 로그만 필터링
3. 다음 메시지 확인:
   - `[Slack Command] 기사 로드 완료: X개` → 기사 개수 확인
   - `[Slack Command] 기사 데이터 없음` → 크롤링 필요
   - `[Slack Command] 기사 로드 오류` → 파일 문제

---

## 확인 사항

### GitHub 저장소 확인
1. GitHub 저장소 → **"Code"** 탭
2. `data/daily_recommendations.json` 파일 확인
3. 파일이 존재하는지 확인
4. 파일 내용 확인 (기사 데이터가 있는지)

### Render 환경 확인
1. Render → **"Environment"** 탭
2. 모든 환경 변수가 올바르게 설정되었는지 확인

---

## 예상 결과

### 크롤링 실행 후
1. `data/daily_recommendations.json` 파일에 기사 데이터 생성
2. Render 로그에 `[Slack Command] 기사 로드 완료: X개` 메시지
3. `/cardnews` 명령어 정상 작동
4. 기사 목록 표시

---

## 체크리스트

- [ ] 크롤링 실행 (GitHub Actions 또는 Streamlit 앱)
- [ ] 크롤링 완료 대기
- [ ] GitHub 저장소에 `data/daily_recommendations.json` 파일 확인
- [ ] `/cardnews` 명령어 다시 시도
- [ ] Render 로그에서 `[Slack Command] 기사 로드 완료` 메시지 확인

---

## 다음 단계

1. **크롤링 실행** - 가장 중요!
2. **크롤링 완료 후 `/cardnews` 명령어 다시 시도**
3. **여전히 오류가 나면 Render 로그에서 `[Slack Command]` 메시지 확인**

---

**가장 중요한 것**: 크롤링을 실행하여 기사 데이터를 생성하세요!

