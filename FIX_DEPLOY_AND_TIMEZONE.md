# 🔧 Render 배포 실패 및 시간대 문제 해결

## 문제 1: Render 배포 실패

### 원인
- `requirements.txt`에 `pytz`와 `google-generativeai` 패키지가 누락됨
- `slack_app.py`에서 `pytz`를 사용하지만 `requirements.txt`에 없음

### 해결
✅ `requirements.txt`에 다음 패키지 추가:
- `pytz>=2025.1`
- `google-generativeai>=0.3.0`

---

## 문제 2: Render 로그 시간이 이상함

### 원인
- Render는 기본적으로 UTC 시간을 사용
- 코드에서 `print()`로 로그를 출력할 때 시간대 변환 없이 출력

### 해결
✅ `slack_app.py`에 KST 시간대 변환 함수 추가:
- `get_kst_now()`: 한국 시간(서울) 기준 현재 시간 반환
- `log_with_kst()`: KST 시간과 함께 로그 출력

모든 `print()` 문을 `log_with_kst()`로 변경하여 KST 시간으로 표시되도록 수정

---

## 수정 사항

### 1. `requirements.txt`
```txt
pytz>=2025.1
google-generativeai>=0.3.0
```

### 2. `slack_app.py`
- `pytz` 임포트 추가
- `get_kst_now()`, `log_with_kst()` 함수 추가
- 모든 로그 출력을 `log_with_kst()`로 변경

---

## 다음 단계

### 1. GitHub에 푸시
```bash
git add requirements.txt slack_app.py
git commit -m "Render 배포 실패 및 시간대 문제 수정"
git push origin main
```

### 2. Render 재배포
1. Render 대시보드 → **"Manual Deploy"** → **"Deploy latest commit"**
2. 배포 완료 대기 (약 2-3분)
3. 배포 성공 확인

### 3. 로그 확인
1. Render → **"Logs"** 탭
2. `/cardnews` 명령어 실행
3. 로그에서 KST 시간 확인:
   ```
   [2026-01-04 16:35:33 KST] [Slack Command] 명령어: /cardnews ...
   [2026-01-04 16:35:33 KST] [Slack Command] 기사 로드 완료: 40개
   ```

---

## 체크리스트

- [x] `requirements.txt`에 `pytz` 추가
- [x] `requirements.txt`에 `google-generativeai` 추가
- [x] `slack_app.py`에 KST 시간대 변환 함수 추가
- [x] 모든 로그 출력을 `log_with_kst()`로 변경
- [ ] GitHub에 푸시
- [ ] Render 재배포
- [ ] 로그에서 KST 시간 확인

---

## 예상 결과

### 배포 성공
- Render Events 탭에서 "Deploy live" 메시지 확인
- 서비스가 정상적으로 실행됨

### 로그 시간 표시
- 모든 로그가 KST 시간으로 표시됨
- 예: `[2026-01-04 16:35:33 KST] [Slack Command] ...`

### `/cardnews` 명령어 작동
- 기사 목록이 정상적으로 표시됨
- 카드뉴스 생성이 정상적으로 작동함

