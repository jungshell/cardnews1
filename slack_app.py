"""Slack App 서버 - 인터랙티브 기능 및 카드뉴스 생성"""
import os
import json
import hashlib
import hmac
import time
from flask import Flask, request, jsonify
from typing import Dict, Optional
import requests

from cache_manager import get_cached_summary, get_cached_script
from daily_recommendations import load_daily_recommendations
from gemini_api import generate_cardnews_with_gemini, summarize_with_gemini
from card_parser import parse_card_script
from image_prep import prepare_card_images, create_images_zip

app = Flask(__name__)

# 환경 변수
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def verify_slack_request(request):
    """Slack 요청 검증"""
    if not SLACK_SIGNING_SECRET:
        return True  # 개발 환경에서는 검증 건너뛰기
    
    timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    
    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    my_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    slack_signature = request.headers.get('X-Slack-Signature', '')
    return hmac.compare_digest(my_signature, slack_signature)


@app.route('/slack/interactive', methods=['POST'])
def handle_interactive():
    """Slack Interactive Components 처리"""
    if not verify_slack_request(request):
        return jsonify({"error": "Invalid request"}), 403
    
    payload = json.loads(request.form.get('payload'))
    
    if payload.get('type') == 'block_actions':
        actions = payload.get('actions', [])
        if not actions:
            return jsonify({"response_type": "ephemeral", "text": "액션이 없습니다."}), 200
        
        action = actions[0]
        action_id = action.get('action_id', '')
        
        # 카드뉴스 생성 버튼 클릭
        if action_id.startswith('create_cardnews_'):
            article_idx = int(action_id.split('_')[-1]) - 1
            articles = load_daily_recommendations()
            
            if article_idx < len(articles):
                article = articles[article_idx]
                return handle_create_cardnews(payload, article)
        
        # 요약 보기 버튼 클릭
        elif action_id.startswith('view_summary_'):
            article_idx = int(action_id.split('_')[-1]) - 1
            articles = load_daily_recommendations()
            
            if article_idx < len(articles):
                article = articles[article_idx]
                return handle_view_summary(payload, article)
    
    return jsonify({"response_type": "ephemeral", "text": "처리 완료"}), 200


def handle_create_cardnews(payload: Dict, article: Dict) -> Dict:
    """카드뉴스 생성 처리"""
    channel_id = payload.get('channel', {}).get('id')
    user_id = payload.get('user', {}).get('id')
    
    title = article.get('title', '')
    description = article.get('description', '')
    link = article.get('link', '')
    article_id = link or title
    
    # 즉시 응답 (사용자에게 진행 중 메시지)
    response_url = payload.get('response_url')
    if response_url:
        requests.post(response_url, json={
            "response_type": "ephemeral",
            "text": "카드뉴스 생성 중... 잠시만 기다려주세요.",
            "replace_original": False
        })
    
    # 카드뉴스 생성
    try:
        # 캐시 확인
        script = get_cached_script(article_id)
        if not script:
            script = generate_cardnews_with_gemini(description, title)
            if not script:
                return jsonify({
                    "response_type": "ephemeral",
                    "text": "❌ 카드뉴스 생성에 실패했습니다."
                }), 200
        
        # 파싱
        cards = parse_card_script(script)
        if not cards:
            return jsonify({
                "response_type": "ephemeral",
                "text": "❌ 카드뉴스 형식을 파싱할 수 없습니다."
            }), 200
        
        # 이미지 준비
        images_data = []
        for card in cards:
            img_data = prepare_card_images(card)
            images_data.append(img_data)
        
        # 결과를 슬랙에 전송 (Bot Token 사용)
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📝 카드뉴스 생성 완료: {title[:50]}",
                },
            },
            {
                "type": "divider",
            },
        ]
        
        # 각 카드 정보 표시 (최대 10개)
        for card_idx, card in enumerate(cards[:10], 1):
            card_type = card.get('type', '')
            head = card.get('head', '')
            body = card.get('body', '')
            image_key = card.get('image_key', '')
            
            card_text = f"*카드 {card_idx} ({card_type})*\n"
            if head:
                card_text += f"*HEAD:* {head}\n"
            if body:
                card_text += f"*BODY:* {body}\n"
            if image_key:
                card_text += f"*IMAGE_KEY:* {image_key}"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": card_text,
                },
            })
            
            if card_idx < min(len(cards), 10):
                blocks.append({"type": "divider"})
        
        if len(cards) > 10:
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*총 {len(cards)}개 카드 중 10개만 표시. 전체는 Streamlit 앱에서 확인하세요.*",
                    },
                ],
            })
        
        # Streamlit 앱 링크 버튼
        streamlit_url = os.getenv("STREAMLIT_APP_URL", "https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app")
        import urllib.parse
        streamlit_url_with_params = f"{streamlit_url}?article_url={urllib.parse.quote(link)}" if link else streamlit_url
        
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "🔗 Streamlit 앱에서 전체 보기",
                    },
                    "url": streamlit_url_with_params,
                },
            ],
        })
        
        # Bot Token으로 슬랙에 메시지 전송
        channel_id = payload.get('channel', {}).get('id')
        if SLACK_BOT_TOKEN and channel_id:
            try:
                requests.post(
                    "https://slack.com/api/chat.postMessage",
                    headers={
                        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "channel": channel_id,
                        "blocks": blocks,
                        "text": f"✅ 카드뉴스 생성 완료! ({len(cards)}개 카드)",
                    },
                    timeout=10
                )
            except Exception as e:
                print(f"[슬랙 메시지 전송 오류] {e}")
        
        return jsonify({
            "response_type": "in_channel",
            "text": f"✅ 카드뉴스 생성 완료! ({len(cards)}개 카드)",
            "blocks": blocks
        }), 200
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[카드뉴스 생성 오류] {error_msg}")
        print(traceback.format_exc())
        
        return jsonify({
            "response_type": "ephemeral",
            "text": f"❌ 오류 발생: {error_msg}"
        }), 200


def handle_view_summary(payload: Dict, article: Dict) -> Dict:
    """요약 보기 처리"""
    title = article.get('title', '')
    description = article.get('description', '')
    link = article.get('link', '')
    article_id = link or title
    
    # 즉시 응답
    response_url = payload.get('response_url')
    if response_url:
        requests.post(response_url, json={
            "response_type": "ephemeral",
            "text": "요약을 가져오는 중...",
            "replace_original": False
        })
    
    # 캐시에서 요약 가져오기
    summary = get_cached_summary(article_id)
    if not summary:
        # 요약 생성
        summary = summarize_with_gemini(description, title)
        if not summary:
            if response_url:
                requests.post(response_url, json={
                    "response_type": "ephemeral",
                    "text": "❌ 요약 생성에 실패했습니다.",
                    "replace_original": True
                })
            return jsonify({
                "response_type": "ephemeral",
                "text": "❌ 요약 생성에 실패했습니다."
            }), 200
    
    # HTML 태그 제거
    import re
    summary_clean = re.sub(r'<[^>]+>', '', summary)
    summary_clean = summary_clean.replace('**', '*')  # 마크다운 변환
    
    # 요약이 너무 길면 잘라내기
    if len(summary_clean) > 2000:
        summary_clean = summary_clean[:2000] + "..."
    
    # 결과 전송
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📄 요약: {title[:50]}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": summary_clean,
            },
        },
    ]
    
    if response_url:
        requests.post(response_url, json={
            "response_type": "ephemeral",
            "blocks": blocks,
            "replace_original": True
        })
    
    return jsonify({
        "response_type": "ephemeral",
        "blocks": blocks
    }), 200


@app.route('/slack/command', methods=['POST'])
def handle_command():
    """Slack Slash Command 처리"""
    if not verify_slack_request(request):
        return jsonify({"error": "Invalid request"}), 403
    
    command_text = request.form.get('text', '').strip()
    user_id = request.form.get('user_id')
    channel_id = request.form.get('channel_id')
    
    # /cardnews 1 → 첫 번째 기사
    # /cardnews → 전체 목록
    articles = load_daily_recommendations()
    
    if not articles:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❌ 추천 기사가 없습니다. 먼저 크롤링을 실행해주세요."
        }), 200
    
    if command_text.isdigit():
        # 특정 기사 선택
        idx = int(command_text) - 1
        if 0 <= idx < len(articles):
            article = articles[idx]
            return handle_create_cardnews({
                'channel': {'id': channel_id},
                'user': {'id': user_id},
                'response_url': None
            }, article)
        else:
            return jsonify({
                "response_type": "ephemeral",
                "text": f"❌ {idx + 1}번 기사가 없습니다. (총 {len(articles)}개)"
            }), 200
    else:
        # 전체 목록 표시
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📰 추천 기사 목록",
                },
            },
            {
                "type": "divider",
            },
        ]
        
        for idx, article in enumerate(articles[:10], 1):  # 최대 10개
            title = article.get('title', '')
            score = article.get('relevance_score', 0)
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{idx}. {title[:80]}*\n관련도: {score:.1f}/10점",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "생성",
                    },
                    "value": str(idx),
                    "action_id": f"create_cardnews_{idx}",
                },
            })
            
            if idx < min(len(articles), 10):
                blocks.append({"type": "divider"})
        
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"사용법: `/cardnews 1` (1번 기사 생성) 또는 버튼 클릭",
                },
            ],
        })
        
        return jsonify({
            "response_type": "ephemeral",
            "blocks": blocks
        }), 200


@app.route('/health', methods=['GET'])
def health():
    """헬스 체크"""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

