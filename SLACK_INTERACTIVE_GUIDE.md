# 🤖 슬랙 인터랙티브 기능 확장 가이드

## ✅ 현재 구현된 기능

### 기본 슬랙 알림 (개선 완료)
- ✅ HTML 태그 제거 (`</b>` 등)
- ✅ 기사 제목 표시
- ✅ 배포일시 표시 (한국어 형식: "2025.12.30 (화)")
- ✅ 관련도 점수 표시
- ✅ 기사 설명 (간략)
- ✅ 요약 정보 (캐시에서 자동 로드)
- ✅ 버튼: "🔗 기사 보기", "📝 카드뉴스 생성"

---

## 🚀 슬랙에서 카드뉴스 생성/이미지 생성 방법

### 방법 1: Streamlit 앱 연동 (현재 구현, 간단)

#### 현재 상태
- 슬랙 메시지에 "📝 카드뉴스 생성" 버튼
- 버튼 클릭 시 Streamlit 앱으로 이동
- Streamlit 앱에서 카드뉴스 생성 및 이미지 준비

#### 개선 방안: URL 파라미터로 기사 자동 선택

**1단계: Streamlit 앱에 URL 파라미터 처리 추가**

```python
# app.py에 추가
article_url = st.query_params.get("article_url")
if article_url:
    # 해당 기사 찾기
    articles = load_daily_recommendations()
    for idx, article in enumerate(articles):
        if article.get("link") == article_url:
            # 해당 기사 자동 선택 및 카드뉴스 생성 화면 표시
            _render_article_details(article, ...)
            break
```

**2단계: 슬랙 버튼 URL에 파라미터 추가**

```python
# daily_fetch.py에서
streamlit_url = f"{base_url}?article_url={link}"
```

---

### 방법 2: Slack App + Interactive Components (완전 자동화)

#### 장점
- 슬랙에서 직접 카드뉴스 생성 가능
- 버튼 클릭으로 즉시 작업 가능
- 모달 다이얼로그로 상세 정보 표시

#### 구현 단계

**1단계: Slack App 생성**
1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. "Create New App" → "From scratch"
3. App 이름: "카드뉴스 자동화"
4. 워크스페이스 선택

**2단계: Interactive Components 활성화**
1. Features → "Interactivity" 활성화
2. Request URL 설정:
   - 예: `https://your-server.com/slack/interactive`
   - 또는 Streamlit Cloud Functions 사용

**3단계: Slash Commands 추가**
1. Features → "Slash Commands"
2. `/cardnews` 명령어 추가
   - Command: `/cardnews`
   - Request URL: `https://your-server.com/slack/command`
   - Short Description: "카드뉴스 생성"

**4단계: 웹 서버 구축 (Flask 예시)**

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/slack/interactive', methods=['POST'])
def handle_interactive():
    payload = request.form.get('payload')
    data = json.loads(payload)
    
    if data['type'] == 'block_actions':
        action = data['actions'][0]
        if action['action_id'].startswith('create_cardnews_'):
            # 카드뉴스 생성 API 호출
            article_id = action['value']
            result = generate_cardnews(article_id)
            
            # 결과를 슬랙에 전송
            send_cardnews_result(data['channel']['id'], result)
    
    return '', 200

@app.route('/slack/command', methods=['POST'])
def handle_command():
    text = request.form.get('text', '')
    # /cardnews 1 → 첫 번째 기사
    # 카드뉴스 생성 및 결과 전송
    return jsonify({
        "response_type": "in_channel",
        "text": "카드뉴스 생성 중...",
    })
```

**5단계: 카드뉴스 생성 API 엔드포인트**

```python
def generate_cardnews(article_id: str):
    # 기사 정보 가져오기
    articles = load_daily_recommendations()
    article = next((a for a in articles if a.get("link") == article_id), None)
    
    if not article:
        return {"error": "기사를 찾을 수 없습니다."}
    
    # 카드뉴스 생성
    script = generate_cardnews_with_gemini(
        article.get("description", ""),
        article.get("title", "")
    )
    
    # 이미지 준비
    cards = parse_card_script(script)
    images_zip = create_images_zip(cards)
    
    return {
        "script": script,
        "cards": cards,
        "images_zip": images_zip,
    }
```

---

### 방법 3: Slack Workflow Builder (코드 없이)

#### 장점
- 코드 없이 설정 가능
- 빠른 구현

#### 단계
1. Slack → Workflow Builder
2. 웹훅 트리거 설정
3. 카드뉴스 생성 API 호출 (HTTP Request)
4. 결과를 슬랙에 전송

---

## 📋 추천 구현 순서

### 1단계: Streamlit URL 파라미터 연동 (가장 간단)
- 슬랙 버튼 클릭 시 Streamlit 앱으로 이동
- URL 파라미터로 기사 자동 선택
- **예상 시간: 30분**

### 2단계: Slack App 구축 (완전 자동화)
- 슬랙에서 직접 카드뉴스 생성
- 버튼 클릭으로 즉시 작업
- **예상 시간: 2-3시간**

### 3단계: 이미지 자동 생성 및 업로드
- 카드뉴스 생성 후 이미지 자동 생성
- 슬랙에 이미지 업로드
- **예상 시간: 1-2시간**

---

## 🔧 즉시 적용 가능한 개선사항

### 1. Streamlit URL 파라미터 처리

`app.py`에 추가:

```python
# URL 파라미터로 기사 자동 선택
article_url = st.query_params.get("article_url")
if article_url:
    articles = load_daily_recommendations()
    for idx, article in enumerate(articles):
        if article.get("link") == article_url:
            # 해당 기사 자동 선택
            st.session_state['selected_article_idx'] = idx
            break
```

### 2. 슬랙 버튼 URL에 파라미터 추가

`daily_fetch.py`에서:

```python
streamlit_url = f"https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app?article_url={link}"
```

---

## 📚 참고 자료

- [Slack Block Kit](https://api.slack.com/block-kit)
- [Slack Interactive Components](https://api.slack.com/interactivity)
- [Slack Slash Commands](https://api.slack.com/interactivity/slash-commands)
- [Slack Workflow Builder](https://slack.com/help/articles/360041352714-Create-workflows-in-Slack)

---

## 다음 단계

1. **즉시 적용**: Streamlit URL 파라미터 처리 추가
2. **향후 확장**: Slack App 구축 (선택)

어떤 방법으로 진행하시겠어요?
