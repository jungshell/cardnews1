"""Railway 스케줄러 - daily_fetch.py를 주기적으로 실행"""
import schedule
import time
import subprocess
import sys
import os

# 스케줄러는 로컬 타임존 기준으로 동작하므로 KST 고정
os.environ.setdefault("TZ", "Asia/Seoul")
if hasattr(time, "tzset"):
    time.tzset()


def run_daily_fetch():
    """daily_fetch.py를 실행합니다."""
    print(f"[스케줄러] 일일 크롤링 실행: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    script_path = os.path.join(os.path.dirname(__file__), "daily_fetch.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[에러] {result.stderr}")


def run_slack_notification():
    """Slack 알림만 전송합니다."""
    print(f"[스케줄러] Slack 알림 전송: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    script_path = os.path.join(os.path.dirname(__file__), "daily_fetch.py")
    result = subprocess.run([sys.executable, script_path, "slack-only"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[에러] {result.stderr}")


def main():
    """스케줄러 메인 루프 (KST 기준)"""
    # KST 기준으로 고정
    schedule.every().day.at("08:55").do(run_daily_fetch)
    schedule.every().day.at("09:00").do(run_slack_notification)

    print("[스케줄러 시작]")
    print("  - 크롤링: 매일 08:55 KST")
    print("  - Slack 알림: 매일 09:00 KST")
    print("  - 스케줄러 실행 중...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크


if __name__ == "__main__":
    main()


