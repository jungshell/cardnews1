# 🔧 GitHub Actions Workflow 수동 설정 가이드

## 문제
Personal Access Token에 `workflow` 권한이 없어서 푸시가 실패했습니다.

## 해결 방법: GitHub 웹사이트에서 직접 추가

### 1단계: GitHub 저장소 접속
1. [https://github.com/jungshell/cardnews1](https://github.com/jungshell/cardnews1) 접속

### 2단계: Workflow 파일 생성
1. **"Add file" → "Create new file" 클릭**
2. **파일 경로 입력:**
   ```
   .github/workflows/daily_crawl.yml
   ```
   - `.github` 폴더가 없으면 자동으로 생성됩니다

3. **아래 내용을 복사하여 붙여넣기:**

```yaml
name: Daily Crawl and Slack Notification

on:
  schedule:
    # 매일 오전 9시 (한국 시간) = UTC 0시
    - cron: '0 0 * * *'
  workflow_dispatch:  # 수동 실행도 가능하도록

jobs:
  crawl:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run daily crawl
      env:
        NAVER_CLIENT_ID: ${{ secrets.NAVER_CLIENT_ID }}
        NAVER_CLIENT_SECRET: ${{ secrets.NAVER_CLIENT_SECRET }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      run: |
        python daily_fetch.py
    
    - name: Commit and push results (if any)
      if: success()
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add data/daily_recommendations.json data/history.json || true
        git commit -m "Auto: Daily crawl results $(date +'%Y-%m-%d')" || exit 0
        git push || exit 0
```

4. **"Commit new file" 클릭**
   - 커밋 메시지: `GitHub Actions 자동 크롤링 설정 추가`

---

## 3단계: GitHub Secrets 설정 (필수!)

### Secrets 설정 위치
1. **Settings** 탭 클릭
2. **Secrets and variables** → **Actions** 클릭
3. **New repository secret** 클릭

### 추가할 4개의 Secret:

#### 1. NAVER_CLIENT_ID
- Name: `NAVER_CLIENT_ID`
- Secret: 네이버 API Client ID (따옴표 없이)
- 예: `CWSU/BOA4EDMPJ50/0ugraxmV/SDUKFIBZ00INIUK`

#### 2. NAVER_CLIENT_SECRET
- Name: `NAVER_CLIENT_SECRET`
- Secret: 네이버 API Client Secret (따옴표 없이)
- 예: `QlvJ13ux21jmi`

#### 3. GEMINI_API_KEY
- Name: `GEMINI_API_KEY`
- Secret: Gemini API Key (따옴표 없이)
- 예: `AIzaSyCWuk1pr0m2IwJRbENHfo0422DDYUabziY`

#### 4. SLACK_WEBHOOK_URL
- Name: `SLACK_WEBHOOK_URL`
- Secret: Slack Webhook URL (따옴표 없이)
- 예: `https://hooks.slack.com/services/REDACTED/REDACTED/REDACTED`

---

## 4단계: Workflow 활성화 확인

1. **Actions 탭 클릭**
2. **"Daily Crawl and Slack Notification" workflow 확인**
3. Workflow가 활성화되어 있는지 확인

---

## 5단계: 수동 테스트 (선택)

1. **Actions 탭** → **"Daily Crawl and Slack Notification"** 클릭
2. **"Run workflow"** 버튼 클릭 (오른쪽 상단)
3. **"Run workflow"** 확인
4. 실행이 시작되면 각 단계가 성공하는지 확인
5. 슬랙에 알림이 도착하는지 확인

---

## 실행 시간

- **매일 오전 9시 (한국 시간)**
- UTC 기준: 매일 0시 (자정)

---

## 체크리스트

- [ ] GitHub 웹사이트에서 workflow 파일 생성 완료
- [ ] GitHub Secrets에 4개 모두 설정 완료
- [ ] Actions 탭에서 workflow 활성화 확인
- [ ] 수동 테스트 성공
- [ ] 슬랙 알림 도착 확인

---

## 문제 해결

### Workflow가 실행되지 않음
1. Actions 탭에서 workflow 활성화 확인
2. Secrets가 모두 설정되었는지 확인
3. 로그에서 오류 메시지 확인

### 슬랙 알림이 오지 않음
1. SLACK_WEBHOOK_URL이 올바른지 확인
2. Workflow 로그에서 오류 확인

### 크롤링이 실패함
1. NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 확인
2. GEMINI_API_KEY 확인
3. Workflow 로그에서 상세 오류 확인

---

모든 설정이 완료되면 내일 오전 9시부터 자동으로 크롤링이 실행됩니다! 🎉

