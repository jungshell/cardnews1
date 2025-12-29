"""Railway 스케줄러 - daily_fetch.py를 주기적으로 실행"""
import schedule
import time
import subprocess
import sys
import os


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
    """스케줄러 메인 루프"""
    # UTC 시간 기준 (한국 시간 = UTC+9)
    # 매일 23:55 UTC = 한국 시간 08:55
    schedule.every().day.at("23:55").do(run_daily_fetch)
    
    # 매일 00:00 UTC = 한국 시간 09:00
    schedule.every().day.at("00:00").do(run_slack_notification)
    
    print("[스케줄러 시작]")
    print("  - 크롤링: 매일 23:55 UTC (한국 시간 08:55)")
    print("  - Slack 알림: 매일 00:00 UTC (한국 시간 09:00)")
    print("  - 스케줄러 실행 중...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크


if __name__ == "__main__":
    main()


