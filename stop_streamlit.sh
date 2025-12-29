#!/bin/bash

# Streamlit 앱을 종료하는 스크립트

cd "$(dirname "$0")"

# PID 파일이 있으면 해당 프로세스 종료
if [ -f "streamlit.pid" ]; then
    PID=$(cat streamlit.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ Streamlit 프로세스 종료됨 (PID: $PID)"
    else
        echo "⚠️ PID 파일은 있지만 프로세스가 실행 중이 아닙니다."
    fi
    rm streamlit.pid
fi

# 포트 8501을 사용하는 모든 프로세스 종료
lsof -ti:8501 | xargs kill -9 2>/dev/null && echo "✅ 포트 8501의 모든 프로세스 종료됨" || echo "ℹ️ 포트 8501을 사용하는 프로세스가 없습니다."

