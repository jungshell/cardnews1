#!/bin/bash

# macOS launchd 서비스로 등록하는 스크립트

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.ccon.streamlit.plist"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
LAUNCHD_FILE="$LAUNCHD_DIR/com.ccon.streamlit.plist"

echo "🚀 Streamlit 서비스 등록 중..."

# LaunchAgents 디렉토리 생성
mkdir -p "$LAUNCHD_DIR"

# plist 파일 복사 (경로 수정)
sed "s|/Volumes/Samsung USB/cardnews_3|$SCRIPT_DIR|g" "$PLIST_FILE" > "$LAUNCHD_FILE"

# 실행 권한 부여
chmod +x "$SCRIPT_DIR/start_streamlit.sh"
chmod +x "$SCRIPT_DIR/stop_streamlit.sh"

# 서비스 로드
launchctl load "$LAUNCHD_FILE" 2>/dev/null || launchctl unload "$LAUNCHD_FILE" 2>/dev/null && launchctl load "$LAUNCHD_FILE"

echo "✅ 서비스가 등록되었습니다!"
echo ""
echo "📋 관리 명령어:"
echo "  시작: launchctl start com.ccon.streamlit"
echo "  중지: launchctl stop com.ccon.streamlit"
echo "  상태 확인: launchctl list | grep com.ccon.streamlit"
echo "  제거: launchctl unload $LAUNCHD_FILE"
echo ""
echo "🌐 접속: http://localhost:8501"

