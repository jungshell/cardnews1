# 🔧 GitHub Actions 권한 문제 해결 가이드

## 문제 상황

GitHub Actions 로그에서:
```
remote: Permission to jungshell/cardnews1.git denied to github-actions [bot].
fatal: unable to access 'https://github.com/jungshell/cardnews1/': The requested URL returned error: 403
```

**의미**: GitHub Actions가 저장소에 푸시할 권한이 없습니다.

## 해결 방법

### 워크플로우 파일에 권한 추가

`.github/workflows/daily_crawl.yml` 파일에 다음을 추가:

```yaml
jobs:
  crawl:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # 저장소에 쓰기 권한 부여 (git push를 위해 필요)
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    # ... 나머지 단계들
```

## 수정 방법

### 방법 1: GitHub 웹에서 직접 수정 (권장)

1. **워크플로우 파일 접속**
   - https://github.com/jungshell/cardnews1/blob/main/.github/workflows/daily_crawl.yml

2. **"✏️ Edit" 버튼 클릭**

3. **`jobs:` 섹션 수정**
   - `crawl:` 아래에 `permissions:` 추가:

```yaml
jobs:
  crawl:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # 저장소에 쓰기 권한 부여
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      # with: token 부분은 제거 (GITHUB_TOKEN이 자동으로 사용됨)
```

4. **"Commit changes" 클릭**

### 방법 2: 로컬에서 수정 후 푸시

워크플로우 파일은 이미 수정되었지만, 로컬에서 푸시할 때 권한 문제가 발생할 수 있습니다.

**대안**: GitHub 웹에서 직접 수정하는 것을 권장합니다.

## 확인 방법

1. **워크플로우 파일 수정 후**
2. **GitHub Actions → "Run workflow" 클릭**
3. **"Commit and push results" 단계 로그 확인**
   - `✅ 변경사항을 커밋하고 푸시합니다.` 메시지 확인
   - `Permission denied` 오류가 사라졌는지 확인

## 왜 "오늘 크롤링 완료"라고 나오는가?

`app.py`의 로직:
- 파일의 수정 시간을 확인해서 오늘 날짜이고 9시 이후면 "완료" 메시지 표시
- 하지만 실제로는 GitHub Actions가 크롤링을 실행했지만, git push가 실패해서 Streamlit Cloud가 받은 파일은 오래된 파일
- Streamlit Cloud는 GitHub 저장소의 파일을 사용하므로, GitHub에 푸시가 안 되면 오래된 파일을 계속 보여줌

**해결**: 권한을 추가하면 git push가 성공하고, Streamlit Cloud가 최신 데이터를 가져올 수 있습니다.

## 참고

- `permissions: contents: write`는 GitHub Actions가 저장소에 커밋/푸시할 수 있게 해줍니다
- 기본적으로 GitHub Actions는 읽기 전용 권한만 있습니다
- `GITHUB_TOKEN`은 자동으로 제공되므로 별도로 설정할 필요 없습니다
