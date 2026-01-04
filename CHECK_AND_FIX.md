# 🔍 확인 및 수정 가이드

## 현재 상태

### ✅ 완료된 작업
1. `.gitignore` 수정 - `data` 폴더의 필수 파일 포함
2. 로컬 파일 GitHub에 커밋 완료
3. 로거 시간대 한국 시간으로 변경

### ⏳ 확인 필요
1. GitHub 저장소에 `data` 폴더가 있는지
2. 크롤링이 실행되어 최신 데이터가 있는지
3. Render가 최신 코드를 사용하는지

---

## 즉시 확인할 사항

### 1. GitHub 저장소 확인 (가장 중요!)

1. GitHub 저장소 → **"Code"** 탭
2. `data` 폴더가 보이는지 확인
3. `data/daily_recommendations.json` 파일 클릭
4. 파일 내용 확인:
   - `"date"` 필드 확인 (최신 날짜인지)
   - `"articles"` 배열에 기사 데이터가 있는지
   - 기사 개수 확인

**예상 결과:**
- 파일이 있고 기사 데이터가 있으면 → Render 재배포 후 테스트
- 파일이 없거나 비어있으면 → 크롤링 실행 필요

---

### 2. Render 재배포 확인

1. Render 대시보드 → **"Events"** 탭
2. 최신 배포 확인:
   - GitHub 푸시 후 자동 재배포되었는지
   - 또는 **"Manual Deploy"** → **"Deploy latest commit"** 클릭

---

### 3. 크롤링 실행 (데이터가 없거나 오래된 경우)

#### 방법 1: GitHub Actions (권장)
1. GitHub 저장소 → **"Actions"** 탭
2. **"Daily Crawl and Slack Notification"** 워크플로우 선택
3. **"Run workflow"** 버튼 클릭
4. 크롤링 완료 대기 (약 1-2분)
5. **"Commit and push results"** 단계 성공 확인
6. GitHub 저장소에서 `data/daily_recommendations.json` 파일 업데이트 확인

#### 방법 2: Streamlit 앱
1. Streamlit 앱 접속
2. **"오늘의 자동 추천 기사"** 탭
3. **"🔄 지금 다시 크롤링하기"** 버튼 클릭
4. 크롤링 완료 후:
   - 로컬에 파일 저장됨
   - **수동으로 GitHub에 커밋 필요**:
     ```bash
     git add data/daily_recommendations.json
     git commit -m "크롤링 결과 업데이트"
     git push origin main
     ```

---

### 4. `/cardnews` 명령어 테스트

1. Render 재배포 완료 대기 (약 2-3분)
2. 크롤링 완료 대기
3. Slack에서 `/cardnews` 명령어 실행
4. Render 로그 확인:
   - `[Slack Command] 기사 로드 완료: X개` 메시지 확인
   - 또는 오류 메시지 확인

---

## 문제 해결 체크리스트

### GitHub 저장소
- [ ] `data` 폴더 존재 확인
- [ ] `data/daily_recommendations.json` 파일 존재 확인
- [ ] 파일에 기사 데이터 있음 확인
- [ ] 파일 날짜가 최신인지 확인

### 크롤링
- [ ] 크롤링 실행 (GitHub Actions 또는 Streamlit 앱)
- [ ] 크롤링 완료 확인
- [ ] GitHub에 커밋됨 확인

### Render
- [ ] 최신 코드로 재배포 완료
- [ ] 환경 변수 모두 설정됨
- [ ] 로그 확인 가능

### 테스트
- [ ] `/cardnews` 명령어 실행
- [ ] Render 로그에서 `[Slack Command] 기사 로드 완료` 메시지 확인
- [ ] 기사 목록 표시 확인

---

## 예상 결과

### 모든 설정 완료 후
1. ✅ GitHub에 최신 기사 데이터 있음
2. ✅ Render에 최신 코드 배포됨
3. ✅ `/cardnews` 명령어 정상 작동
4. ✅ 기사 목록 표시
5. ✅ 버튼 클릭으로 카드뉴스 생성 가능

---

## 시간 표시 개선

로거 시간대를 한국 시간(서울, UTC+9)으로 변경했습니다.
- 다음 배포 후 로그 시간이 한국 시간으로 표시됩니다
- Streamlit 앱의 크롤링 로그도 한국 시간으로 표시됩니다

---

**다음 단계**: 
1. **GitHub 저장소에서 `data/daily_recommendations.json` 파일 확인**
2. **파일이 없거나 오래되었으면 크롤링 실행**
3. **Render 재배포 확인**
4. **`/cardnews` 명령어 테스트**

