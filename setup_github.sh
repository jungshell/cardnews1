#!/bin/bash

# GitHub 저장소 연결 및 배포 준비 스크립트

echo "🚀 GitHub 저장소 연결 및 배포 준비"
echo ""

# 현재 디렉토리 확인
cd "$(dirname "$0")"
echo "📁 현재 디렉토리: $(pwd)"
echo ""

# Git 상태 확인
if [ ! -d ".git" ]; then
    echo "❌ Git 저장소가 아닙니다. 초기화합니다..."
    git init
    git branch -M main
fi

# 원격 저장소 확인
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ]; then
    echo "⚠️  원격 저장소가 연결되어 있지 않습니다."
    echo ""
    echo "다음 중 하나를 선택하세요:"
    echo ""
    echo "1️⃣  기존 저장소 연결 (예: cardnews, cardnews1 등)"
    echo "2️⃣  새 저장소 생성 후 연결"
    echo ""
    read -p "선택 (1 또는 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "기존 저장소 이름을 입력하세요 (예: cardnews, cardnews1):"
        read -p "저장소 이름: " repo_name
        REPO_URL="https://github.com/jungshell/${repo_name}.git"
        echo ""
        echo "연결할 저장소: $REPO_URL"
        read -p "계속하시겠습니까? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            git remote add origin "$REPO_URL"
            echo "✅ 원격 저장소 연결 완료!"
        else
            echo "❌ 취소되었습니다."
            exit 1
        fi
    elif [ "$choice" = "2" ]; then
        echo ""
        echo "새 저장소 이름을 입력하세요 (예: cardnews_3):"
        read -p "저장소 이름: " repo_name
        REPO_URL="https://github.com/jungshell/${repo_name}.git"
        echo ""
        echo "1. 먼저 GitHub에서 새 저장소를 생성하세요:"
        echo "   https://github.com/new"
        echo "   저장소 이름: $repo_name"
        echo "   Public 또는 Private 선택"
        echo "   'Initialize this repository with a README' 체크 해제"
        echo ""
        read -p "2. 저장소를 생성했나요? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            git remote add origin "$REPO_URL"
            echo "✅ 원격 저장소 연결 완료!"
        else
            echo "❌ 먼저 GitHub에서 저장소를 생성해주세요."
            exit 1
        fi
    else
        echo "❌ 잘못된 선택입니다."
        exit 1
    fi
else
    echo "✅ 원격 저장소가 이미 연결되어 있습니다:"
    echo "   $REMOTE_URL"
fi

echo ""
echo "📤 코드 푸시 준비..."
echo ""

# 변경사항 확인
if [ -n "$(git status --porcelain)" ]; then
    echo "변경된 파일이 있습니다. 커밋합니다..."
    git add .
    git commit -m "Update: 배포 준비"
else
    echo "변경사항이 없습니다."
fi

echo ""
echo "원격 저장소에 푸시하시겠습니까? (y/n)"
read -p "선택: " push_confirm

if [ "$push_confirm" = "y" ]; then
    echo ""
    echo "📤 푸시 중..."
    git push -u origin main
    echo ""
    echo "✅ 푸시 완료!"
    echo ""
    echo "🎉 다음 단계:"
    echo "   1. https://streamlit.io/cloud 접속"
    echo "   2. GitHub 계정으로 로그인"
    echo "   3. 'New app' 클릭"
    echo "   4. 저장소 선택: jungshell/$(basename $(git remote get-url origin) .git)"
    echo "   5. Main file: app.py"
    echo "   6. Secrets에 환경 변수 추가"
    echo "   7. Deploy!"
else
    echo "푸시를 건너뜁니다."
fi

