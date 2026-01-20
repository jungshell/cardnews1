# 🔧 data 폴더 문제 해결

## 문제
- GitHub 저장소에 `data` 폴더와 `daily_recommendations.json` 파일이 없음
- `/cardnews` 명령어가 작동하지 않음

## 원인
`.gitignore` 파일에 `data/`가 포함되어 있어서 `data` 폴더 전체가 Git에 커밋되지 않았습니다.

## 해결 방법

### 1. .gitignore 수정 완료 ✅
`.gitignore`를 수정하여:
- `data/` 폴더는 기본적으로 무시
- 하지만 `data/daily_recommendations.json`과 `data/history.json`은 포함

### 2. 파일 커밋 완료 ✅
로컬에 있는 `data` 폴더의 파일들을 Git에 추가했습니다.

### 3. 다음 단계

#### GitHub Actions로 크롤링 실행
1. GitHub 저장소 → **"Actions"** 탭
2. **"Daily Crawl and Slack Notification"** 워크플로우 선택
3. **"Run workflow"** 버튼 클릭
4. 크롤링 완료 후 `data/daily_recommendations.json` 파일이 업데이트됨

#### 수동으로 크롤링 실행 (로컬)
로컬에서 실행하려면:
```bash
python daily_fetch.py
```

#### Streamlit 앱에서 크롤링 실행
1. Streamlit 앱 접속
2. **"오늘의 자동 추천 기사"** 탭
3. **"🔄 지금 다시 크롤링하기"** 버튼 클릭

---

## 확인 사항

### GitHub 저장소 확인
1. GitHub 저장소 → **"Code"** 탭
2. `data` 폴더가 보이는지 확인
3. `data/daily_recommendations.json` 파일이 있는지 확인

### Render에서 확인
1. Render는 GitHub 저장소를 클론하므로
2. `data/daily_recommendations.json` 파일이 있으면
3. `/cardnews` 명령어가 정상 작동해야 함

---

## 예상 결과

### 크롤링 실행 후
- ✅ `data/daily_recommendations.json` 파일 생성/업데이트
- ✅ GitHub에 자동 커밋 (GitHub Actions 실행 시)
- ✅ `/cardnews` 명령어 정상 작동
- ✅ 기사 목록 표시

---

## 체크리스트

- [x] `.gitignore` 수정 완료
- [x] `data` 폴더 파일 커밋 완료
- [ ] GitHub 저장소에 `data` 폴더 확인
- [ ] 크롤링 실행 (GitHub Actions 또는 수동)
- [ ] `/cardnews` 명령어 테스트

---

**다음 단계**: GitHub Actions로 크롤링을 실행하거나, Streamlit 앱에서 수동으로 크롤링을 실행하세요.

