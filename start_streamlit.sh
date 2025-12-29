#!/bin/bash

# Streamlit 앱을 백그라운드로 실행하는 스크립트
# 컴퓨터를 껐다 켜도 자동으로 실행되도록 launchd에 등록할 수 있습니다.

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 기존 Streamlit 프로세스 종료 (포트 8501)
lsof -ti:8501 | xargs kill -9 2>/dev/null || true

# Streamlit 실행 (백그라운드)
nohup streamlit run app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &

# 프로세스 ID 저장
echo $! > streamlit.pid

echo "✅ Streamlit이 백그라운드에서 실행 중입니다."
echo "📝 로그 확인: tail -f streamlit.log"
echo "🌐 접속: http://localhost:8501"
echo "🛑 종료: ./stop_streamlit.sh 또는 kill \$(cat streamlit.pid)"

