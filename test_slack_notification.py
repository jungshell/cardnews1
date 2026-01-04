"""Slack 알림 테스트 스크립트"""
import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# daily_fetch.py의 함수 사용
from daily_fetch import load_daily_recommendations, send_slack_notification

def main():
    """테스트 Slack 알림 전송"""
    print("=" * 60)
    print("Slack 알림 테스트 시작")
    print("=" * 60)
    
    # 기사 로드
    articles = load_daily_recommendations()
    
    if not articles:
        print("❌ 기사 데이터가 없습니다. 먼저 크롤링을 실행해주세요.")
        print("   Streamlit 앱에서 '지금 다시 크롤링하기' 버튼을 클릭하세요.")
        return
    
    print(f"✅ 기사 로드 완료: {len(articles)}개")
    print(f"📤 상위 5개 기사를 Slack으로 전송합니다...")
    
    # Slack 알림 전송
    success = send_slack_notification(articles)
    
    if success:
        print("✅ Slack 알림 전송 완료!")
        print("   Slack의 '#ai-news' 채널을 확인하세요.")
    else:
        print("❌ Slack 알림 전송 실패")
        print("   SLACK_WEBHOOK_URL 환경 변수를 확인하세요.")
    
    print("=" * 60)
    print("테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    main()

