# 🔧 시간대 및 데이터 문제 해결

## 현재 문제

1. **시간 표시**: UTC 기준으로 표시됨 (2026-01-04 08:24:29)
2. **크롤링 실행**: 완료되었지만 `/cardnews` 명령어 여전히 오류

---

## 문제 1: 시간 표시를 한국 시간으로 변경

### 현재 상태
- 로그 시간이 UTC 기준으로 표시됨
- 한국 시간(UTC+9)으로 변경 필요

### 해결 방법
코드에서 시간대 처리를 추가해야 합니다. 하지만 먼저 더 중요한 문제를 해결하겠습니다.

---

## 문제 2: 크롤링 결과가 저장되지 않음

### 확인 사항

#### 1. GitHub 저장소 확인
1. GitHub 저장소 → **"Code"** 탭
2. `data/daily_recommendations.json` 파일 확인
3. 파일이 업데이트되었는지 확인
4. 파일 내용 확인 (기사 데이터가 있는지)

#### 2. 크롤링 로그 확인
Streamlit 앱의 크롤링 로그에서:
- "저장 완료: X개 기사를 daily_recommendations.json에 저장" 메시지 확인
- 오류 메시지 확인

#### 3. Render에서 파일 접근 확인
Render는 GitHub 저장소를 클론하므로:
- GitHub에 파일이 있어야 Render에서도 접근 가능
- 파일이 커밋되지 않았으면 Render에서도 없음

---

## 즉시 확인할 사항

### 1. GitHub 저장소에서 파일 확인
1. GitHub 저장소 → **"Code"** 탭
2. `data/daily_recommendations.json` 파일 클릭
3. 파일 내용 확인:
   - `"articles"` 배열이 있는지
   - 배열에 기사 데이터가 있는지
   - 파일이 비어있지 않은지

### 2. 크롤링이 실제로 완료되었는지 확인
Streamlit 앱의 크롤링 로그에서:
- "저장 완료" 메시지 확인
- "완료" 메시지 확인
- 오류 메시지 확인

### 3. Render 로그 확인
Render → **"Logs"** 탭에서:
- `/cardnews` 명령어 실행 시 로그 확인
- `[Slack Command] 기사 로드 완료: X개` 메시지 확인
- 또는 `[Slack Command] 기사 데이터 없음` 메시지 확인

---

## 가능한 원인

### 원인 1: 크롤링 결과가 GitHub에 커밋되지 않음
- Streamlit 앱에서 크롤링한 결과는 로컬에만 저장됨
- GitHub에 커밋되지 않으면 Render에서 접근 불가

### 원인 2: GitHub Actions 크롤링이 실패
- 크롤링은 실행되었지만 결과 저장 실패
- 또는 커밋/푸시 실패

### 원인 3: Render가 최신 코드를 가져오지 않음
- Render가 오래된 버전의 저장소를 사용 중
- 재배포 필요

---

## 해결 방법

### 방법 1: GitHub Actions 크롤링 결과 확인
1. GitHub 저장소 → **"Actions"** 탭
2. 최신 워크플로우 실행 확인
3. **"crawl"** 작업 클릭
4. 로그에서 다음 확인:
   - "저장 완료" 메시지
   - "Commit and push results" 단계 성공 여부

### 방법 2: 수동으로 파일 확인 및 커밋
1. 로컬에서 `data/daily_recommendations.json` 파일 확인
2. 파일이 있으면 GitHub에 커밋:
   ```bash
   git add data/daily_recommendations.json
   git commit -m "크롤링 결과 추가"
   git push origin main
   ```

### 방법 3: Render 재배포
1. Render → **"Manual Deploy"** → **"Deploy latest commit"**
2. 최신 코드로 재배포

---

## 다음 단계

1. **GitHub 저장소에서 `data/daily_recommendations.json` 파일 확인**
2. **파일 내용 확인 (기사 데이터가 있는지)**
3. **Render 로그에서 `/cardnews` 실행 시 메시지 확인**
4. **필요시 수동으로 파일 커밋**

---

**가장 중요한 것**: GitHub 저장소에 `data/daily_recommendations.json` 파일이 있고, 기사 데이터가 있는지 확인하세요!

