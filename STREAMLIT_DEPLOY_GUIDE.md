# 🚀 Streamlit Cloud 재배포 가이드

## 자동 재배포 (권장)

**Streamlit Cloud는 GitHub에 푸시하면 자동으로 재배포됩니다!**

### 방법
1. 코드 변경 후 GitHub에 푸시:
   ```bash
   git add .
   git commit -m "변경 사항"
   git push origin main
   ```

2. **자동 재배포 시작**
   - Streamlit Cloud가 자동으로 변경사항 감지
   - 약 1-2분 후 재배포 완료

3. **재배포 확인**
   - Streamlit 앱 URL 접속
   - 변경사항이 반영되었는지 확인

---

## 수동 재배포 (필요 시)

### Streamlit Cloud 대시보드에서
1. **Streamlit Cloud 접속**
   - https://share.streamlit.io 접속
   - 로그인

2. **앱 선택**
   - 대시보드에서 `cardnews1` 앱 클릭

3. **재배포**
   - 오른쪽 상단 **"⋮" (더보기)** 메뉴 클릭
   - **"Reboot app"** 또는 **"Redeploy"** 선택

---

## 재배포 확인 방법

1. **앱 URL 접속**
   - https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app

2. **변경사항 확인**
   - 새로고침 (F5 또는 Cmd+R)
   - 변경된 기능 테스트

---

## 문제 해결

### 재배포가 안 될 때
1. **GitHub 푸시 확인**
   - GitHub 저장소에서 최신 커밋 확인
   - 푸시가 완료되었는지 확인

2. **Streamlit Cloud 로그 확인**
   - 앱 대시보드 → **"Manage app"** → **"Logs"**
   - 오류 메시지 확인

3. **수동 재배포 시도**
   - 위의 "수동 재배포" 방법 사용

---

## 현재 상태

✅ **최신 코드가 GitHub에 푸시되었습니다**
- 크롤링 결과 자동 동기화
- 시간 표시 KST 통일
- 필터링 로직 개선 (30일로 확장)

⏳ **자동 재배포 대기 중**
- 약 1-2분 후 재배포 완료 예상

