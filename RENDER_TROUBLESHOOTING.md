# 🔧 Render 저장소 연결 문제 해결

## 문제: `cardnews1` 저장소가 목록에 안 보여요

---

## 해결 방법 1: Public Git Repository 탭 사용 (가장 간단)

### 단계
1. Render의 "New Web Service" 페이지에서
2. 상단 탭 중 **"Public Git Repository"** 클릭
3. **"Repository URL"** 입력란에 다음 입력:
   ```
   https://github.com/jungshell/cardnews1
   ```
4. **"Continue"** 버튼 클릭
5. 나머지 설정 진행

**장점**: 저장소 목록이 안 보여도 바로 연결 가능

---

## 해결 방법 2: GitHub 권한 재설정

### 단계
1. Render의 "New Web Service" 페이지에서
2. **"Credentials"** 드롭다운 클릭
3. **"Configure in GitHub"** 클릭
4. GitHub에서 Render 앱 권한 확인:
   - 저장소 접근 권한이 있는지 확인
   - `cardnews1` 저장소가 포함되어 있는지 확인
5. 권한 업데이트 후 Render 페이지 새로고침
6. 저장소 목록에서 `cardnews1` 확인

---

## 해결 방법 3: GitHub에서 Render 앱 권한 확인

### 단계
1. GitHub 접속
2. 우측 상단 프로필 아이콘 클릭
3. **"Settings"** 클릭
4. 왼쪽 메뉴에서 **"Applications"** → **"Authorized OAuth Apps"** 클릭
5. **"Render"** 찾기
6. **"Configure"** 클릭
7. **"Repository access"** 섹션 확인:
   - **"All repositories"** 선택되어 있는지 확인
   - 또는 **"Only select repositories"**에서 `cardnews1`이 선택되어 있는지 확인
8. 필요시 권한 업데이트 후 저장
9. Render 페이지로 돌아가서 새로고침

---

## 해결 방법 4: Render 연결 해제 후 재연결

### 단계
1. Render의 "New Web Service" 페이지에서
2. **"Credentials"** 드롭다운 클릭
3. **"Disconnect credential"** 클릭
4. **"Connect GitHub"** 버튼 클릭
5. GitHub 권한 재승인
6. 저장소 목록 확인

---

## 추천 순서

1. **방법 1 (Public Git Repository 탭)** - 가장 빠르고 간단
2. **방법 3 (GitHub 권한 확인)** - 근본적인 해결
3. **방법 2 (Render에서 재설정)** - 빠른 해결
4. **방법 4 (재연결)** - 마지막 수단

---

## 확인 사항

### 저장소가 Public인지 확인
- `cardnews1` 저장소가 Public인지 확인
- Private 저장소라면 Render의 유료 플랜이 필요할 수 있습니다

### 저장소 이름 확인
- GitHub에서 정확한 저장소 이름 확인
- `jungshell/cardnews1`이 맞는지 확인

---

## 다음 단계

저장소 연결이 완료되면:
1. **"Continue"** 클릭
2. 서비스 설정 진행 (Name, Region, Build Command 등)
3. 환경 변수 설정
4. 배포 시작

---

**문제가 계속되면**: Public Git Repository 탭을 사용하는 것이 가장 확실합니다!

