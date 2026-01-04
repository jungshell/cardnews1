# 🔍 Render에서 데이터 파일 접근 확인

## 현재 상태

### ✅ 확인 완료
- GitHub 저장소에 `data/daily_recommendations.json` 파일 존재
- 파일에 기사 데이터 있음 (약 40개)
- 파일 날짜: 2025-12-27 (오래됨, 하지만 데이터는 있음)

### ⏳ 확인 필요
- Render가 이 파일을 읽을 수 있는지
- `/cardnews` 명령어 실행 시 정확한 오류 메시지

---

## 즉시 확인할 사항

### 1. Render 로그 확인 (가장 중요!)

1. Render 대시보드 → **"Logs"** 탭
2. `/cardnews` 명령어 실행
3. 로그에서 다음 메시지 확인:

**정상 작동 시:**
```
[Slack Command] 명령어: /cardnews , 사용자: ..., 채널: ...
[Slack Command] 기사 로드 완료: 40개
```

**오류 발생 시:**
```
[Slack Command] 기사 로드 오류: ...
```
또는
```
[Slack Command] 기사 데이터 없음
```

---

### 2. Render 재배포 확인

1. Render 대시보드 → **"Events"** 탭
2. 최신 배포 확인:
   - GitHub 푸시 후 자동 재배포되었는지
   - 최신 커밋이 배포되었는지
3. 필요시 **"Manual Deploy"** → **"Deploy latest commit"** 클릭

---

### 3. 파일 경로 확인

Render에서 파일 경로는:
- `data/daily_recommendations.json` (상대 경로)
- 또는 `/mount/src/cardnews1/data/daily_recommendations.json` (절대 경로)

코드에서 `os.path.join(os.path.dirname(__file__), "data")`를 사용하므로:
- `slack_app.py`가 있는 디렉토리 기준으로 `data` 폴더를 찾음
- Render는 GitHub 저장소를 클론하므로 경로가 맞아야 함

---

## 가능한 원인

### 원인 1: Render가 오래된 코드 사용
- 최신 코드가 배포되지 않음
- **해결**: Render 재배포

### 원인 2: 파일 경로 문제
- Render에서 파일을 찾을 수 없음
- **해결**: 로그에서 정확한 오류 확인

### 원인 3: 파일 읽기 권한 문제
- 파일은 있지만 읽을 수 없음
- **해결**: 로그에서 정확한 오류 확인

---

## 해결 방법

### Step 1: Render 로그 확인
1. Render → **"Logs"** 탭
2. `/cardnews` 명령어 실행
3. 로그에서 `[Slack Command]` 메시지 확인
4. 오류 메시지 복사

### Step 2: Render 재배포
1. Render → **"Manual Deploy"** → **"Deploy latest commit"**
2. 배포 완료 대기 (약 2-3분)
3. `/cardnews` 명령어 다시 시도

### Step 3: 로그 메시지 공유
- 로그에서 확인한 정확한 메시지를 알려주시면 해결 방법 제시

---

## 예상 결과

### 정상 작동 시
1. Render 로그에 `[Slack Command] 기사 로드 완료: 40개` 메시지
2. Slack에서 기사 목록 표시
3. 버튼 클릭으로 카드뉴스 생성 가능

---

## 체크리스트

- [ ] Render 로그 확인 (`[Slack Command]` 메시지)
- [ ] Render 재배포 확인
- [ ] `/cardnews` 명령어 다시 시도
- [ ] 로그 메시지 공유 (오류가 계속되면)

---

**가장 중요한 것**: Render 로그에서 `/cardnews` 실행 시 정확한 메시지를 확인해주세요!

