import html
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import pytz

import streamlit as st
from dotenv import load_dotenv

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')

def get_kst_now() -> datetime:
    """한국 시간(서울) 기준 현재 시간을 반환합니다."""
    return datetime.now(KST)

from cache_manager import (
    get_cached_summary,
    save_cached_summary,
    get_cached_script,
    save_cached_script,
)
from card_parser import parse_card_script
from daily_recommendations import (
    load_daily_recommendations,
    get_daily_recommendations_date,
)
from gemini_api import summarize_with_gemini, generate_cardnews_with_gemini
from history_manager import add_crawl_history, get_crawl_history
from image_prep import prepare_card_images, create_images_zip
from naver_api import search_naver_news
from setup_checker import check_environment
from logger import logger


def load_env() -> None:
    """
    환경 변수를 .env에서 로드합니다.
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.info("환경 변수 로드 완료")
    else:
        logger.warning(".env 파일을 찾을 수 없습니다.")


def clean_html_tags(text: str) -> str:
    """HTML 태그를 제거합니다."""
    if not text:
        return ""
    # <b>, </b>, <strong>, </strong> 등 제거
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def clean_title_suffix(text: str) -> str:
    """제목에서 불필요한 접미사(예: '< 문화 < 충남 < 전국 < 기사본문')를 제거합니다."""
    if not text:
        return ""
    # "< 문화 < 충남 < 전국 < 기사본문" 같은 패턴 제거
    text = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*<\s*기사본문.*$", "", text)
    text = re.sub(r"\s*<\s*[^<]*<\s*[^<]*<\s*[^<]*$", "", text)  # "< 문화 < 충남 < 전국" 같은 패턴
    text = re.sub(r"\s*<\s*[^<]*<\s*[^<]*$", "", text)  # "< 대전·충청 < 지역" 같은 패턴
    text = re.sub(r"\s*<\s*[^<]*$", "", text)  # "< 문화" 같은 패턴
    return text.strip()


def _render_article_details(article: Dict, title: str, description: str, link: str, pub_date: str, score: float, idx: int) -> None:
    """
    기사 상세 정보를 렌더링합니다.
    
    Args:
        article: 기사 정보 딕셔너리
        title: 기사 제목
        description: 기사 설명
        link: 기사 링크
        pub_date: 발행일
        score: 관련도 점수
        idx: 기사 인덱스
    """
    
    # 관련도 분석 결과 (컴팩트화)
    title_lower = title.lower()
    desc_lower = description.lower() if description else ""
    
    # 주요 키워드와 기타 키워드 구분
    main_keywords = ["충남콘텐츠진흥원", "충콘진"]
    other_keywords = [
        "천안그린스타트업타운",
        "김곡미",
        "충남콘텐츠코리아랩",
        "충남콘텐츠기업지원센터",
        "충남글로벌게임센터",
        "충남음악창작소",
        "충남 e스포츠",
    ]
    
    title_score = 0.0
    desc_score = 0.0
    bonus_score = 0.0
    
    keyword_matches_title_main = []
    keyword_matches_title_other = []
    keyword_matches_desc_main = []
    keyword_matches_desc_other = []
    
    # 제목 매칭 점수 계산 (최대 5점)
    for keyword in main_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in title_lower:
            keyword_matches_title_main.append(keyword)
            title_score += 2.5
    
    for keyword in other_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in title_lower:
            keyword_matches_title_other.append(keyword)
            title_score += 0.3
    
    title_score = min(title_score, 5.0)
    
    # 설명 매칭 점수 계산 (최대 3점)
    for keyword in main_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in desc_lower:
            keyword_matches_desc_main.append(keyword)
            desc_score += 1.5
    
    for keyword in other_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in desc_lower:
            keyword_matches_desc_other.append(keyword)
            desc_score += 0.2
    
    desc_score = min(desc_score, 3.0)
    
    # 최근 기사 보너스 점수 계산 (최대 2점)
    if pub_date:
        try:
            from datetime import datetime
            if "T" in pub_date:
                date_str = pub_date.split("T")[0]
                article_date = datetime.strptime(date_str, "%Y-%m-%d")
                today = get_kst_now()
                days_diff = (today - article_date).days
                if days_diff <= 4:
                    bonus_score = 2.0 - (days_diff * 0.375)
        except:
            pass
    
    # 관련도 점수 색상 결정
    if score >= 8.0:
        score_color = "#4CAF50"  # 녹색
    elif score >= 6.0:
        score_color = "#FFC107"  # 노란색
    elif score >= 4.0:
        score_color = "#FF9800"  # 주황색
    else:
        score_color = "#9E9E9E"  # 회색
    
    # 관련도 한 줄 표시 + 배분 사유는 expander로 숨김
    relevance_col1, relevance_col2 = st.columns([3, 1])
    with relevance_col1:
        st.markdown(
            f"""
            <div style="padding: 6px 12px; margin: 4px 0; background-color: #2e2e2e; border-radius: 4px; display: inline-block;">
                <span style="font-size: 0.9em;">📊 관련도: </span>
                <span style="font-size: 1em; font-weight: bold; color: {score_color};">{score:.1f}/10점</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with relevance_col2:
        if link:
            st.markdown(f"🔗 [원문 보기]({link})", help="원문 링크")
    
    # 배분 사유는 expander로 숨김
    with st.expander("📈 배분 사유 보기", expanded=False):
        if title_score > 0:
            matches = []
            if keyword_matches_title_main:
                matches.extend(keyword_matches_title_main)
            if keyword_matches_title_other:
                matches.extend(keyword_matches_title_other[:3])
            st.write(f"  - 제목에 키워드 포함 ({', '.join(matches[:3])}): +{title_score:.1f}점 (최대 5점)")
        
        if desc_score > 0:
            matches = []
            if keyword_matches_desc_main:
                matches.extend(keyword_matches_desc_main)
            if keyword_matches_desc_other:
                matches.extend(keyword_matches_desc_other[:3])
            st.write(f"  - 설명에 키워드 포함 ({', '.join(matches[:3])}): +{desc_score:.1f}점 (최대 3점)")
        
        if bonus_score > 0:
            st.write(f"  - 최근 기사 보너스: +{bonus_score:.1f}점 (최대 2점)")
    
    # 기사 정보
    content = description or article.get("article_overview", "")
    article_id = link or title
    
    # 원문 요약 자동 생성 및 표시
    summary_key = f"daily_summary_{article_id}"
    
    # 자동으로 요약 생성 시도 (캐시 또는 새로 생성)
    if summary_key not in st.session_state:
        cached = get_cached_summary(article_id)
        if cached:
            st.session_state[summary_key] = cached
        else:
            # 자동 생성
            with st.spinner("원문 요약을 생성 중입니다..."):
                summary = summarize_with_gemini(content, title)
                if summary:
                    save_cached_summary(article_id, summary)
                    st.session_state[summary_key] = summary
    
    # 요약 표시 (접기 가능)
    if summary_key in st.session_state and st.session_state[summary_key]:
        summary_text = st.session_state[summary_key]
        # 요약 미리보기 (첫 2줄만)
        preview_lines = summary_text.split('\n')[:2]
        preview = '\n'.join(preview_lines)
        if len(summary_text.split('\n')) > 2:
            preview += "..."
        
        with st.expander(f"📄 원문 요약 ({preview[:50]}...)", expanded=False):
            st.markdown(summary_text)
    
    # 카드뉴스 문구 생성 버튼 (그룹화 및 컴팩트화)
    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])
    
    with btn_col1:
        if st.button("📝 카드뉴스 문구 생성", key=f"daily_cardnews_{idx}", use_container_width=True):
            cached_script = get_cached_script(article_id)
            if cached_script:
                st.session_state[f"card_script_{article_id}"] = cached_script
                st.success("✅ 캐시된 문구를 불러왔습니다.")
            else:
                with st.spinner("생성 중... (약 30초 소요)"):
                    try:
                        script = generate_cardnews_with_gemini(content, title)
                        if script:
                            # 파싱 테스트
                            cards = parse_card_script(script)
                            if not cards:
                                st.warning("⚠️ 생성된 문구를 파싱할 수 없습니다. 형식을 확인해주세요.")
                                st.code(script[:500] + "..." if len(script) > 500 else script, language="text")
                            else:
                                save_cached_script(article_id, script)
                                st.session_state[f"card_script_{article_id}"] = script
                                st.success(f"✅ 생성 완료! ({len(cards)}개 카드)")
                        else:
                            st.error("❌ 생성 실패: Gemini API 호출 실패 또는 응답 없음")
                            st.info("💡 Streamlit Cloud의 Secrets에서 GEMINI_API_KEY를 확인해주세요.")
                    except Exception as e:
                        st.error(f"❌ 생성 실패: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc(), language="text")
    
    with btn_col2:
        if st.button("🔄 새로 생성", key=f"daily_cardnews_new_{idx}", use_container_width=True, help="캐시 무시하고 새로 생성"):
            with st.spinner("생성 중... (약 30초 소요)"):
                try:
                    script = generate_cardnews_with_gemini(content, title)
                    if script:
                        # 파싱 테스트
                        cards = parse_card_script(script)
                        if not cards:
                            st.warning("⚠️ 생성된 문구를 파싱할 수 없습니다. 형식을 확인해주세요.")
                            st.code(script[:500] + "..." if len(script) > 500 else script, language="text")
                        else:
                            save_cached_script(article_id, script)
                            st.session_state[f"card_script_{article_id}"] = script
                            st.success(f"✅ 새로 생성 완료! ({len(cards)}개 카드)")
                    else:
                        st.error("❌ 생성 실패: Gemini API 호출 실패 또는 응답 없음")
                        st.warning("⚠️ 가능한 원인:")
                        st.markdown("""
                        - **GEMINI_API_KEY가 설정되지 않았거나 잘못됨**
                        - **Gemini API 쿼터 초과 (429 오류)**
                        - **네트워크 오류 또는 타임아웃**
                        """)
                        st.info("💡 **해결 방법:** Streamlit Cloud의 Secrets에서 `GEMINI_API_KEY`를 확인하고, 올바른 형식으로 설정했는지 확인해주세요.")
                        st.markdown("---")
                        st.caption("💡 **디버깅:** Streamlit Cloud의 'Manage app' → 'Logs'에서 '[Gemini]'로 시작하는 메시지를 확인하세요.")
                except Exception as e:
                    st.error(f"❌ 생성 실패: {str(e)}")
                    st.warning("⚠️ 예외 발생 - 상세 오류:")
                    import traceback
                    st.code(traceback.format_exc(), language="text")
    
    with btn_col3:
        st.write("")  # 공간 확보
    
    # 카드뉴스 문구 표시 (전체 너비, HEAD/BODY 분리, 클릭 시 복사)
    card_script_display = st.session_state.get(f"card_script_{article_id}", "")
    if not card_script_display:
        card_script_display = get_cached_script(article_id)
        if card_script_display:
            st.session_state[f"card_script_{article_id}"] = card_script_display
    
    if card_script_display:
        # 카드 파싱
        cards = parse_card_script(card_script_display)
        
        if cards:
            st.markdown("**📝 카드뉴스 문구**")
            
            # 카드 타입별 색상 정의
            card_type_colors = {
                "cover": "#6750A4",  # 보라색
                "intro": "#2196F3",  # 파란색
                "program": "#4CAF50",  # 초록색
                "impact": "#FF9800",  # 주황색
                "result": "#FF9800",  # 주황색
                "closing": "#FF5722",  # 주황-빨강
            }
            
            # 그리드 레이아웃 (2열 또는 3열)
            num_cards = len(cards)
            cols_per_row = 2 if num_cards <= 4 else 3
            
            for row_start in range(0, num_cards, cols_per_row):
                cols = st.columns(cols_per_row)
                for col_idx, col in enumerate(cols):
                    card_idx = row_start + col_idx
                    if card_idx < num_cards:
                        card = cards[card_idx]
                        card_type = card.get("type", "")
                        head = card.get("head", "")
                        body = card.get("body", "")
                        image_key = card.get("image_key", "")
                        
                        # 카드 타입별 색상
                        card_color = card_type_colors.get(card_type, "#625B71")
                        
                        with col:
                            # 카드형 디자인
                            st.markdown(
                                f"""
                                <div style="padding: 10px; margin: 4px 0; background-color: #2e2e2e; border-left: 4px solid {card_color}; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                    <div style="font-size: 0.85em; color: {card_color}; margin-bottom: 6px; font-weight: bold;">
                                        카드 {card_idx + 1}{f" ({card_type})" if card_type else ""}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # HEAD 표시
                            if head:
                                head_id = f"head_{article_id}_{idx}_{card_idx}"
                                head_col1, head_col2 = st.columns([9, 1])
                                with head_col1:
                                    st.text_input(
                                        "HEAD",
                                        head,
                                        key=f"head_input_{head_id}",
                                        disabled=True,
                                        label_visibility="collapsed"
                                    )
                                with head_col2:
                                    copy_clicked = st.button("📋", key=f"copy_head_btn_{head_id}", use_container_width=True, help="HEAD 복사")
                                    if copy_clicked:
                                        import streamlit.components.v1 as components
                                        copy_html = f"""
                                        <html>
                                        <head>
                                            <script>
                                            (function() {{
                                                const text = {json.dumps(head)};
                                                if (navigator.clipboard && navigator.clipboard.writeText) {{
                                                    navigator.clipboard.writeText(text).then(function() {{
                                                        const msg = document.createElement('div');
                                                        msg.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #4CAF50; color: white; padding: 12px 20px; border-radius: 5px; z-index: 999999; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);';
                                                        msg.textContent = '✅ 복사되었습니다!';
                                                        document.body.appendChild(msg);
                                                        setTimeout(function() {{
                                                            if (msg.parentNode) document.body.removeChild(msg);
                                                        }}, 2000);
                                                    }}).catch(function(err) {{
                                                        const textArea = document.createElement('textarea');
                                                        textArea.value = text;
                                                        textArea.style.position = 'fixed';
                                                        textArea.style.opacity = '0';
                                                        textArea.style.zIndex = '999999';
                                                        document.body.appendChild(textArea);
                                                        textArea.select();
                                                        document.execCommand('copy');
                                                        document.body.removeChild(textArea);
                                                    }});
                                                }} else {{
                                                    const textArea = document.createElement('textarea');
                                                    textArea.value = text;
                                                    textArea.style.position = 'fixed';
                                                    textArea.style.opacity = '0';
                                                    textArea.style.zIndex = '999999';
                                                    document.body.appendChild(textArea);
                                                    textArea.select();
                                                    document.execCommand('copy');
                                                    document.body.removeChild(textArea);
                                                }}
                                            }})();
                                            </script>
                                        </head>
                                        <body></body>
                                        </html>
                                        """
                                        components.html(copy_html, height=0)
                            
                            # BODY 표시
                            if body:
                                body_id = f"body_{article_id}_{idx}_{card_idx}"
                                body_col1, body_col2 = st.columns([9, 1])
                                with body_col1:
                                    st.text_area(
                                        "BODY",
                                        body,
                                        key=f"body_input_{body_id}",
                                        height=50,
                                        disabled=True,
                                        label_visibility="collapsed"
                                    )
                                with body_col2:
                                    copy_clicked = st.button("📋", key=f"copy_body_btn_{body_id}", use_container_width=True, help="BODY 복사")
                                    if copy_clicked:
                                        import streamlit.components.v1 as components
                                        copy_html = f"""
                                        <html>
                                        <head>
                                            <script>
                                            (function() {{
                                                const text = {json.dumps(body)};
                                                if (navigator.clipboard && navigator.clipboard.writeText) {{
                                                    navigator.clipboard.writeText(text).then(function() {{
                                                        const msg = document.createElement('div');
                                                        msg.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #4CAF50; color: white; padding: 12px 20px; border-radius: 5px; z-index: 999999; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);';
                                                        msg.textContent = '✅ 복사되었습니다!';
                                                        document.body.appendChild(msg);
                                                        setTimeout(function() {{
                                                            if (msg.parentNode) document.body.removeChild(msg);
                                                        }}, 2000);
                                                    }}).catch(function(err) {{
                                                        const textArea = document.createElement('textarea');
                                                        textArea.value = text;
                                                        textArea.style.position = 'fixed';
                                                        textArea.style.opacity = '0';
                                                        textArea.style.zIndex = '999999';
                                                        document.body.appendChild(textArea);
                                                        textArea.select();
                                                        document.execCommand('copy');
                                                        document.body.removeChild(textArea);
                                                    }});
                                                }} else {{
                                                    const textArea = document.createElement('textarea');
                                                    textArea.value = text;
                                                    textArea.style.position = 'fixed';
                                                    textArea.style.opacity = '0';
                                                    textArea.style.zIndex = '999999';
                                                    document.body.appendChild(textArea);
                                                    textArea.select();
                                                    document.execCommand('copy');
                                                    document.body.removeChild(textArea);
                                                }}
                                            }})();
                                            </script>
                                        </head>
                                        <body></body>
                                        </html>
                                        """
                                        components.html(copy_html, height=0)
                            
                            # IMAGE_KEY 표시 (있는 경우)
                            if image_key:
                                st.caption(f"🔑 {image_key}")
        else:
            # 파싱 실패 시 원본 텍스트 표시
            st.text_area("카드뉴스 문구", card_script_display, height=400, key=f"daily_script_{article_id}_{idx}")
    
    # 카드뉴스 문구가 있으면 이미지 자료 준비 버튼 표시
    card_script = st.session_state.get(f"card_script_{article_id}", "")
    if not card_script:
        card_script = get_cached_script(article_id)
        if card_script:
            st.session_state[f"card_script_{article_id}"] = card_script
    
    if card_script:
        # 이미지 자료 준비 버튼 (컴팩트하게)
        if st.button("🖼️ 이미지 자료 준비", key=f"daily_image_prep_{idx}", use_container_width=True):
            st.write("카드뉴스 파싱 및 이미지 자료 준비 중...")
            
            cards = parse_card_script(card_script)
            if not cards:
                st.error("카드뉴스 문구를 파싱할 수 없습니다. 형식을 확인해주세요.")
            else:
                st.success(f"{len(cards)}개의 카드를 파싱했습니다.")
                
                all_iconify_downloaded = []
                all_material_downloaded = []
                
                for card_idx, card in enumerate(cards, 1):
                    with st.expander(f"📋 카드 {card_idx}: {card.get('head', '')[:30]}..."):
                        st.write(f"**타입**: {card.get('type', '')}")
                        st.write(f"**제목**: {card.get('head', '')}")
                        if card.get('body'):
                            st.write(f"**본문**: {card.get('body', '')}")
                        
                        img_data = prepare_card_images(card)

                        # 플랫폼별 프롬프트 선택
                        prompts = img_data.get("prompts") or {
                            "copilot": img_data.get("prompt", ""),
                        }
                        prompt_options = [
                            "Copilot / Bing (DALL·E)",
                            "Google Gemini",
                            "로컬 / Stable Diffusion 계열",
                        ]
                        prompt_key_map = {
                            "Copilot / Bing (DALL·E)": "copilot",
                            "Google Gemini": "gemini",
                            "로컬 / Stable Diffusion 계열": "local",
                        }
                        default_option = "Copilot / Bing (DALL·E)"

                        selected_option = st.selectbox(
                            "프롬프트 버전 선택",
                            prompt_options,
                            index=prompt_options.index(default_option),
                            key=f"daily_prompt_mode_{article_id}_{idx}_{card_idx}",
                            help="Copilot/Bing, Gemini, 로컬(Stable Diffusion) 중에서 사용할 프롬프트 버전을 선택하세요.",
                        )

                        selected_key = prompt_key_map.get(selected_option, "copilot")
                        selected_prompt = prompts.get(selected_key) or img_data.get("prompt", "")

                        st.text_area(
                            "AI 이미지 생성 프롬프트",
                            selected_prompt,
                            height=180,
                            key=f"daily_prompt_{article_id}_{idx}_{card_idx}",
                        )
                        
                        if img_data["iconify_icons"]:
                            st.write("**Iconify 아이콘:**")
                            for icon in img_data["iconify_icons"]:
                                st.markdown(f"- [{icon['name']}]({icon['url']})")
                        
                        if img_data["material_icons"]:
                            st.write("**Material Icons:**")
                            for icon in img_data["material_icons"]:
                                st.markdown(f"- [{icon['name']}]({icon['url']})")
                        
                        all_iconify_downloaded.extend(img_data["iconify_downloaded"])
                        all_material_downloaded.extend(img_data["material_downloaded"])
                
                if all_iconify_downloaded or all_material_downloaded:
                    zip_data = create_images_zip(
                        all_iconify_downloaded,
                        all_material_downloaded,
                        f"cardnews_images_{article_id[:20]}.zip",
                    )
                    st.download_button(
                        label="📦 모든 이미지 ZIP 다운로드",
                        data=zip_data,
                        file_name=f"cardnews_images_{article_id[:20]}.zip",
                        mime="application/zip",
                    )
                    st.info(f"총 {len(all_iconify_downloaded) + len(all_material_downloaded)}개의 SVG 파일이 ZIP에 포함되었습니다.")
                    
                    # 카드뉴스 이미지 생성 가이드 표시
                    with st.expander("📖 카드뉴스 이미지 생성 가이드", expanded=False):
                        st.markdown("""
                        ### 🎯 추천 방법: Canva 사용 (무료 + 초보자 친화)
                        
                        **1단계: Canva 접속**
                        - [Canva.com](https://www.canva.com) 접속 (무료 회원가입)
                        - "카드뉴스" 또는 "Instagram Post" 템플릿 검색
                        
                        **2단계: 카드 제작**
                        - 템플릿 선택 후 편집
                        - **제목**: 각 카드의 HEAD 내용 입력
                        - **본문**: 각 카드의 BODY 내용 입력
                        - **배경색**: 
                          - Cover: #6750A4 (진한 파란색/보라색)
                          - Program/Impact/Result: 밝은 회색/흰색
                          - Closing: 연한 파란색/초록색
                        - **아이콘**: ZIP 파일의 SVG 아이콘 업로드 또는 Canva 내장 아이콘 사용
                        - **이미지**: IMAGE_KEY 키워드로 Canva 내장 무료 이미지 검색
                        
                        **3단계: 다운로드**
                        - PNG 또는 JPG 형식 (1080x1080px 권장)
                        
                        **💡 팁:**
                        - 첫 번째 카드를 완성한 후 복제하여 나머지 카드 제작
                        - 브랜드 컬러(#6750A4, #625B71)를 Canva에 저장해두면 재사용 편리
                        
                        **📚 상세 가이드:** `CARDNEWS_IMAGE_GUIDE.md` 파일 참고
                        """)


def get_crawl_time_display() -> Optional[str]:
    """
    크롤링 시간을 표시 형식으로 반환합니다.
    한국 시간(서울)으로 변환하여 표시합니다.
    
    Returns:
        "25.12.26.(금) 11:05" 형식의 문자열. 없으면 None.
    """
    import os
    from history_manager import get_crawl_history
    
    # 1. history.json에서 최근 크롤링 시간 확인
    history = get_crawl_history(limit=1)
    if history:
        timestamp_str = history[0].get("timestamp", "")
        if timestamp_str:
            try:
                # ISO 형식 파싱 (예: "2025-12-24T00:22:14" 또는 "2025-12-24T00:22:14+09:00")
                dt_kst = None
                if "T" in timestamp_str:
                    # 타임존 정보가 있는 경우
                    if "+" in timestamp_str or "Z" in timestamp_str:
                        dt_kst = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        if dt_kst.tzinfo is None:
                            # 타임존 정보가 없으면 KST로 간주
                            dt_kst = KST.localize(dt_kst)
                        else:
                            # 타임존 정보가 있으면 KST로 변환
                            dt_kst = dt_kst.astimezone(KST)
                    else:
                        # 타임존 정보가 없는 경우 (기존 데이터 호환성)
                        # "2025-12-24T00:22:14" 형식 -> KST로 간주
                        dt_str = timestamp_str.split("T")[0] + " " + timestamp_str.split("T")[1]
                        dt_naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                        dt_kst = KST.localize(dt_naive)
                else:
                    # 타임존 정보가 없는 경우 KST로 간주
                    dt_naive = datetime.fromisoformat(timestamp_str)
                    dt_kst = KST.localize(dt_naive)
                
                # 한국어 요일
                weekdays = ["월", "화", "수", "목", "금", "토", "일"]
                weekday = weekdays[dt_kst.weekday()]
                
                # "25.12.26.(금) 11:05" 형식
                return f"{dt_kst.strftime('%y.%m.%d')}.({weekday}) {dt_kst.strftime('%H:%M')}"
            except Exception:
                pass
    
    # 2. daily_recommendations.json 파일의 수정 시간 사용
    data_file = os.path.join("data", "daily_recommendations.json")
    if os.path.exists(data_file):
        try:
            mtime = os.path.getmtime(data_file)
            # 파일 mtime은 로컬 시간이므로, 시스템 타임존을 고려해 KST로 변환
            dt_local = datetime.fromtimestamp(mtime)
            # naive datetime을 시스템 타임존으로 간주하고 KST로 변환
            if dt_local.tzinfo is None:
                # 시스템이 UTC인 경우를 대비해 UTC로 간주 후 KST로 변환
                dt_utc = pytz.utc.localize(dt_local)
                dt_kst = dt_utc.astimezone(KST)
            else:
                dt_kst = dt_local.astimezone(KST)
            
            # 한국어 요일
            weekdays = ["월", "화", "수", "목", "금", "토", "일"]
            weekday = weekdays[dt_kst.weekday()]
            
            # "25.12.26.(금) 11:05" 형식
            return f"{dt_kst.strftime('%y.%m.%d')}.({weekday}) {dt_kst.strftime('%H:%M')}"
        except Exception:
            pass
    
    return None


def render_setup_warnings() -> None:
    """
    환경 변수/폴더 누락을 화면 상단에 표시합니다.
    """
    status = check_environment()
    missing_env = status["missing_env"]
    missing_dirs = status["missing_dirs"]

    if not missing_env and not missing_dirs:
        return

    messages: List[str] = []
    if missing_env:
        messages.append(
            "환경 변수 누락: " + ", ".join(missing_env) + " (.env 파일을 확인해주세요)"
        )
        logger.warning(f"환경 변수 누락: {', '.join(missing_env)}")
    if missing_dirs:
        messages.append("필요한 폴더가 없습니다: " + ", ".join(missing_dirs))
        logger.warning(f"필요한 폴더 누락: {', '.join(missing_dirs)}")

    st.warning(" / ".join(messages))


def main() -> None:
    """
    Streamlit 메인 진입점 - 탭 구조와 기본 플로우를 구성합니다.
    """
    load_env()
    logger.info("애플리케이션 시작")
    
    st.set_page_config(page_title="충남콘텐츠진흥원 카드뉴스 자동화", layout="wide")
    
    # 제목 중략 방지를 위한 전역 CSS
    st.markdown(
        """
        <style>
        /* 모든 텍스트 중략 방지 */
        * {
            text-overflow: clip !important;
        }
        /* 컬럼 내 텍스트 중략 방지 */
        div[data-testid="column"] {
            min-width: 0 !important;
        }
        div[data-testid="column"] > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        /* 마크다운 텍스트 중략 방지 */
        .stMarkdown {
            word-wrap: break-word !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }
        /* 컬럼 내부 요소 중략 방지 */
        div[data-testid="column"] .stMarkdown {
            word-wrap: break-word !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }
        /* div 요소 중략 방지 */
        div {
            text-overflow: clip !important;
        }
        /* flexbox 내부 요소 중략 방지 */
        div[style*="display: flex"] {
            min-width: 0 !important;
        }
        div[style*="display: flex"] > div {
            min-width: 0 !important;
            word-wrap: break-word !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }
        /* table-cell 내부 요소 중략 방지 */
        div[style*="display: table-cell"] {
            max-width: none !important;
            word-wrap: break-word !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }
        /* 모든 마크다운 내부 텍스트 중략 방지 */
        .stMarkdown p,
        .stMarkdown div,
        .stMarkdown span {
            text-overflow: clip !important;
            white-space: normal !important;
            overflow: visible !important;
        }
        /* Expander 제목 폰트 크기 줄이기 및 테두리 제거 */
        .streamlit-expanderHeader {
            font-size: 0.95em !important;
            border: none !important;
            background-color: transparent !important;
        }
        /* Expander 전체 테두리 제거 */
        .streamlit-expander {
            border: none !important;
            background-color: transparent !important;
        }
        /* Expander 헤더 호버 효과 제거 */
        .streamlit-expanderHeader:hover {
            background-color: transparent !important;
        }
        /* Expander 내용 전체 너비 사용 */
        .streamlit-expanderContent {
            width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        .streamlit-expanderContent > div {
            width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        /* Expander가 포함된 컬럼도 전체 너비 사용 */
        div[data-testid="column"] .streamlit-expanderContent {
            width: 100vw !important;
            max-width: 100vw !important;
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
        }
        /* 메인 컨테이너 내 expander 내용 전체 너비 */
        .main .streamlit-expanderContent,
        [data-testid="stAppViewContainer"] .streamlit-expanderContent {
            width: 100% !important;
            max-width: 100% !important;
        }
        /* Expander 내부 모든 요소 전체 너비 */
        .streamlit-expanderContent * {
            max-width: 100% !important;
        }
        /* 코드 블록(로그) 전체 너비 사용 */
        .stCodeBlock {
            width: 100% !important;
            max-width: 100% !important;
            font-size: 0.9em !important;
        }
        pre {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            font-size: 0.9em !important;
        }
        /* 로그 컨테이너 전체 너비 */
        div[data-testid="stVerticalBlock"] > div:has(.stCodeBlock) {
            width: 100% !important;
            max-width: 100% !important;
        }
        /* 컴팩트한 디자인 - 여백 최소화 */
        .stMarkdown {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        /* 버튼 그룹 간격 최소화 */
        div[data-testid="column"] {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        /* 텍스트 입력 필드 컴팩트 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            padding: 6px 10px !important;
            font-size: 0.9em !important;
        }
        /* Expander 간격 최소화 */
        .streamlit-expander {
            margin-bottom: 0.5rem !important;
        }
        /* 섹션 간 간격 최소화 */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        </style>
        <script>
        function copyToClipboard(elementId) {
            try {
                // 이벤트가 전달된 경우 방지
                if (window.event) {
                    window.event.preventDefault();
                    window.event.stopPropagation();
                }
                
                // data 속성에서 복사할 텍스트 가져오기
                const element = document.getElementById(elementId);
                if (!element) {
                    console.error('요소를 찾을 수 없습니다:', elementId);
                    return false;
                }
                
                let copyText = element.getAttribute('data-copy-text');
                if (!copyText) {
                    console.error('복사할 텍스트가 없습니다:', elementId);
                    return false;
                }
                
                // HTML 엔티티 디코딩
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = copyText;
                copyText = tempDiv.textContent || tempDiv.innerText || copyText;
                
                // 클립보드 API 사용 시도 (HTTPS 또는 localhost에서만 작동)
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(copyText).then(function() {
                        showCopyFeedback(elementId);
                        return true;
                    }).catch(function(err) {
                        console.error('클립보드 API 실패:', err);
                        return fallbackCopy(elementId, copyText);
                    });
                } else {
                    // 대체 방법 사용
                    return fallbackCopy(elementId, copyText);
                }
            } catch (err) {
                console.error('복사 함수 오류:', err);
                return false;
            }
        }
        
        function fallbackCopy(elementId, text) {
            try {
                // 대체 방법: 텍스트 영역 사용
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.top = '0';
                textArea.style.left = '0';
                textArea.style.width = '2em';
                textArea.style.height = '2em';
                textArea.style.padding = '0';
                textArea.style.border = 'none';
                textArea.style.outline = 'none';
                textArea.style.boxShadow = 'none';
                textArea.style.background = 'transparent';
                textArea.style.opacity = '0';
                textArea.style.zIndex = '9999';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                let success = false;
                try {
                    success = document.execCommand('copy');
                    if (success) {
                        showCopyFeedback(elementId);
                    } else {
                        console.error('복사 명령 실패');
                        alert('복사에 실패했습니다. 텍스트를 직접 선택하여 복사해주세요.');
                    }
                } catch (err) {
                    console.error('execCommand 실패:', err);
                    alert('복사에 실패했습니다. 텍스트를 직접 선택하여 복사해주세요.');
                }
                
                document.body.removeChild(textArea);
                return success;
            } catch (err) {
                console.error('대체 복사 방법 실패:', err);
                return false;
            }
        }
        
        function showCopyFeedback(elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                const originalBg = element.style.backgroundColor;
                const span = element.querySelector('span');
                if (span) {
                    element.style.backgroundColor = '#4a4a4a';
                    span.textContent = '✓ 복사됨!';
                    setTimeout(function() {
                        element.style.backgroundColor = originalBg;
                        span.textContent = '클릭하여 복사';
                    }, 2000);
                }
            }
        }
        
        // 전역 함수로 등록 (onclick에서 직접 호출 가능하도록)
        window.copyToClipboard = copyToClipboard;
        
        // 페이지 로드 후 이벤트 리스너 추가
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initCopyListeners);
        } else {
            initCopyListeners();
        }
        
        function initCopyListeners() {
            // 모든 copyable-text 클래스 요소에 이벤트 리스너 추가
            document.querySelectorAll('.copyable-text').forEach(function(el) {
                if (!el.hasAttribute('data-listener-added')) {
                    el.setAttribute('data-listener-added', 'true');
                    el.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        const elementId = el.getAttribute('id');
                        if (elementId) {
                            copyToClipboard(elementId);
                        }
                        return false;
                    });
                }
            });
        }
        
        // Streamlit의 동적 콘텐츠를 위해 MutationObserver 사용
        if (typeof MutationObserver !== 'undefined') {
            const observer = new MutationObserver(function(mutations) {
                initCopyListeners();
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    render_setup_warnings()

    st.title("충남콘텐츠진흥원 카드뉴스 자동화 시스템")

    tabs = st.tabs(
        [
            "오늘의 자동 추천 기사",
            "기록 보기",
        ]
    )

    with tabs[0]:
        st.subheader("오늘의 자동 추천 기사")
        
        # daily_recommendations.json 로드
        articles = load_daily_recommendations()
        date_str = get_daily_recommendations_date()
        
        # 오늘 크롤링 여부 확인 및 자동 새로고침
        from datetime import timedelta
        import os
        
        data_file = os.path.join("data", "daily_recommendations.json")
        today_kst = get_kst_now()
        today_9am_kst = today_kst.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # 오늘 9시 이후인지 확인
        should_have_crawled = today_kst >= today_9am_kst
        
        if should_have_crawled and os.path.exists(data_file):
            # 파일 수정 시간 확인
            file_mtime = os.path.getmtime(data_file)
            # 타임스탬프를 UTC로 간주하고 KST로 변환 (Python 버전 호환성)
            # datetime.utcfromtimestamp()를 사용하여 naive datetime 생성 후 UTC로 localize
            from datetime import datetime as dt
            file_mtime_dt_naive = dt.utcfromtimestamp(file_mtime)
            file_mtime_dt_utc = pytz.utc.localize(file_mtime_dt_naive)
            file_mtime_dt = file_mtime_dt_utc.astimezone(KST)
            
            # 오늘 9시 이후에 업데이트되었는지 확인
            if file_mtime_dt < today_9am_kst:
                # 오늘 크롤링이 아직 안 됨
                hours_since_9am = (today_kst - today_9am_kst).total_seconds() / 3600
                if hours_since_9am < 2:  # 9시~11시 사이
                    st.info(f"⏰ 오늘 아침 9시 자동 크롤링이 아직 실행되지 않았습니다. (예상 시간: 오전 9시, 현재: {today_kst.strftime('%H:%M')})")
                else:
                    st.warning(f"⚠️ 오늘 아침 9시 자동 크롤링이 실행되지 않았습니다. (마지막 크롤링: {file_mtime_dt.strftime('%Y-%m-%d %H:%M')})")
            else:
                # 오늘 크롤링 완료
                if file_mtime_dt.date() == today_kst.date():
                    st.success(f"✅ 오늘 아침 9시 자동 크롤링 완료! (크롤링 시간: {file_mtime_dt.strftime('%H:%M')})")
        
        # 세션 상태에 마지막 체크 시간 저장 (너무 자주 체크하지 않도록)
        last_check_key = "last_data_check_time"
        auto_refresh_key = "auto_refresh_enabled"
        
        # 자동 새로고침 설정 (기본값: 켜짐)
        if auto_refresh_key not in st.session_state:
            st.session_state[auto_refresh_key] = True
        
        # 자동 새로고침 토글
        col_toggle, col_info = st.columns([1, 4])
        with col_toggle:
            auto_refresh = st.checkbox(
                "🔄 자동 새로고침",
                value=st.session_state[auto_refresh_key],
                key="auto_refresh_checkbox",
                help="매 30초마다 최신 크롤링 결과를 자동으로 확인합니다."
            )
            st.session_state[auto_refresh_key] = auto_refresh
        
        with col_info:
            if auto_refresh:
                st.caption("💡 자동 새로고침이 켜져 있습니다. 오늘 9시 크롤링 결과가 자동으로 표시됩니다.")
        
        # 자동 새로고침 로직 (30초마다 체크)
        if auto_refresh:
            last_check = st.session_state.get(last_check_key, None)
            current_time = today_kst.timestamp()
            
            if last_check is None or (current_time - last_check) >= 30:
                # 파일 수정 시간 다시 확인
                if os.path.exists(data_file):
                    file_mtime = os.path.getmtime(data_file)
                    # 타임스탬프를 UTC로 간주하고 KST로 변환 (Python 버전 호환성)
                    # datetime.utcfromtimestamp()를 사용하여 naive datetime 생성 후 UTC로 localize
                    from datetime import datetime as dt
                    file_mtime_dt_naive = dt.utcfromtimestamp(file_mtime)
                    file_mtime_dt_utc = pytz.utc.localize(file_mtime_dt_naive)
                    file_mtime_dt = file_mtime_dt_utc.astimezone(KST)
                    
                    # 오늘 9시 이후에 업데이트되었고, 이전에 확인한 시간보다 최신이면 새로고침
                    if file_mtime_dt >= today_9am_kst and file_mtime_dt.date() == today_kst.date():
                        # 이전에 로드한 데이터와 비교
                        prev_file_mtime = st.session_state.get("prev_file_mtime", 0)
                        if file_mtime > prev_file_mtime:
                            st.session_state["prev_file_mtime"] = file_mtime
                            # 데이터 다시 로드
                            articles = load_daily_recommendations()
                            date_str = get_daily_recommendations_date()
                            st.rerun()
                
                st.session_state[last_check_key] = current_time
            
            # 30초 후 자동 새로고침을 위한 JavaScript
            st.markdown(
                """
                <script>
                setTimeout(function() {
                    window.location.reload();
                }, 30000);
                </script>
                """,
                unsafe_allow_html=True
            )
        
        # URL 파라미터로 기사 자동 선택 (슬랙에서 온 경우)
        article_url = st.query_params.get("article_url")
        auto_expand_idx = None
        if article_url and articles:
            for idx, article in enumerate(articles):
                if article.get("link") == article_url:
                    auto_expand_idx = idx
                    st.info(f"📌 슬랙에서 선택한 기사: {article.get('title', '')[:50]}...")
                    break
        
        # 크롤링 버튼 (항상 표시) - 전체 너비 사용
        if st.button("🔄 지금 다시 크롤링하기", key="daily_crawl_button", use_container_width=True):
                import subprocess
                import sys
                
                # 진행 상황 표시 영역 (전체 너비 사용)
                status_placeholder = st.empty()
                # 로그 영역을 전체 너비로 표시
                log_placeholder = st.empty()
                
                try:
                    # 현재 파일의 디렉토리 경로 가져오기
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    script_path = os.path.join(current_dir, "daily_fetch.py")
                    
                    if not os.path.exists(script_path):
                        st.error(f"크롤링 스크립트를 찾을 수 없습니다: {script_path}")
                    else:
                        # 환경 변수 전달 (Streamlit Cloud Secrets 포함)
                        env = os.environ.copy()
                        
                        # Streamlit Cloud Secrets는 자동으로 os.environ에 로드되지만,
                        # 명시적으로 확인하여 subprocess에 전달
                        required_vars = ["NAVER_CLIENT_ID", "NAVER_CLIENT_SECRET", "GEMINI_API_KEY"]
                        missing_vars = [var for var in required_vars if not env.get(var)]
                        
                        if missing_vars:
                            status_placeholder.error(f"❌ 환경 변수 누락: {', '.join(missing_vars)}")
                            log_placeholder.warning("Streamlit Cloud의 Secrets에 환경 변수를 설정해주세요.")
                        else:
                            status_placeholder.info("⏳ 크롤링 시작 중...")
                            
                            # subprocess 실행 (버퍼링 없이 실시간 출력)
                            process = subprocess.Popen(
                                [sys.executable, script_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True,
                                bufsize=1,  # 라인 버퍼링
                                universal_newlines=True,
                                cwd=current_dir,
                                env=env
                            )
                        
                        # 실시간 로그 수집
                        log_lines = []
                        from datetime import datetime as dt
                        start_time = dt.now()
                        last_update = start_time
                        
                        # 출력을 실시간으로 읽기
                        while True:
                            output = process.stdout.readline()
                            if output == '' and process.poll() is not None:
                                break
                            
                            if output:
                                log_lines.append(output.strip())
                                # 최근 20줄만 유지
                                if len(log_lines) > 20:
                                    log_lines.pop(0)
                                
                                # 1초마다 UI 업데이트 (너무 자주 업데이트하지 않음)
                                now = dt.now()
                                if (now - last_update).total_seconds() >= 1.0:
                                    elapsed = (now - start_time).total_seconds()
                                    status_placeholder.info(f"⏳ 크롤링 중... ({elapsed:.0f}초 경과)")
                                    # 로그를 텍스트 영역으로 표시 (전체 너비) - 고유 key 사용
                                    import html
                                    log_text = '\n'.join(log_lines[-20:])
                                    log_text_escaped = html.escape(log_text)
                                    log_placeholder.markdown(
                                        f"""
                                        <div style="width: 100vw; max-width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%); padding: 0;">
                                        <textarea readonly style="width: 100%; height: 500px; font-family: monospace; font-size: 0.85em; padding: 12px; background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #3e3e3e; border-radius: 4px; resize: both; overflow-y: auto; line-height: 1.4; box-sizing: border-box;">{log_text_escaped}</textarea>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                    last_update = now
                        
                        # 최종 결과 확인
                        return_code = process.poll()
                        elapsed = (dt.now() - start_time).total_seconds()
                        
                        if return_code == 0:
                            status_placeholder.success(f"✅ 크롤링 완료! ({elapsed:.1f}초 소요)")
                            
                            # GitHub에 자동 동기화 시도
                            sync_status = st.empty()
                            sync_status.info("🔄 GitHub에 동기화 중...")
                            
                            try:
                                # git 명령어 실행
                                git_commands = [
                                    ["git", "add", "data/daily_recommendations.json", "data/history.json"],
                                    ["git", "-c", "user.name=Streamlit App", "-c", "user.email=streamlit@cardnews.app", "commit", "-m", f"크롤링 결과 업데이트: {get_kst_now().strftime('%Y-%m-%d %H:%M:%S KST')}"],
                                    ["git", "push", "origin", "main"]
                                ]
                                
                                sync_success = True
                                for cmd in git_commands:
                                    result = subprocess.run(
                                        cmd,
                                        cwd=current_dir,
                                        capture_output=True,
                                        text=True,
                                        timeout=30
                                    )
                                    if result.returncode != 0:
                                        # git add는 파일이 없어도 실패할 수 있으므로 무시
                                        if cmd[0] == "git" and cmd[1] == "add":
                                            continue
                                        # commit은 변경사항이 없으면 실패할 수 있으므로 무시
                                        if cmd[0] == "git" and cmd[1] == "commit" and "nothing to commit" in result.stdout.lower():
                                            sync_status.warning("ℹ️ 변경사항이 없어 커밋을 건너뜁니다.")
                                            sync_success = None  # 실패도 성공도 아님
                                            break
                                        sync_success = False
                                        sync_status.error(f"❌ Git 동기화 실패: {result.stderr}")
                                        break
                                
                                if sync_success:
                                    sync_status.success("✅ GitHub 동기화 완료!")
                                elif sync_success is None:
                                    pass  # 이미 메시지 표시됨
                                else:
                                    sync_status.warning("⚠️ GitHub 동기화 실패 (로컬에는 저장됨)")
                                    
                            except subprocess.TimeoutExpired:
                                sync_status.warning("⏱️ GitHub 동기화 시간 초과 (로컬에는 저장됨)")
                            except Exception as e:
                                sync_status.warning(f"⚠️ GitHub 동기화 오류: {str(e)} (로컬에는 저장됨)")
                            
                            # 로그를 텍스트 영역으로 표시 (전체 너비)
                            import html
                            log_text = '\n'.join(log_lines[-30:])
                            log_text_escaped = html.escape(log_text)
                            log_placeholder.markdown(
                                f"""
                                <div style="position: relative; width: 100vw !important; max-width: 100vw !important; left: 50% !important; right: 50% !important; margin-left: -50vw !important; margin-right: -50vw !important; padding: 0 !important; box-sizing: border-box !important;">
                                <textarea readonly style="width: 100% !important; height: 600px !important; font-family: monospace !important; font-size: 0.85em !important; padding: 12px !important; background-color: #1e1e1e !important; color: #d4d4d4 !important; border: 1px solid #3e3e3e !important; border-radius: 4px !important; resize: both !important; overflow-y: auto !important; line-height: 1.4 !important; box-sizing: border-box !important; display: block !important;">{log_text_escaped}</textarea>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            # 2초 후 자동 새로고침
                            import time
                            time.sleep(2)
                            st.rerun()
                        else:
                            status_placeholder.error(f"❌ 크롤링 실패 (종료 코드: {return_code})")
                            # 로그를 텍스트 영역으로 표시 (전체 너비)
                            import html
                            log_text = '\n'.join(log_lines)
                            log_text_escaped = html.escape(log_text)
                            log_placeholder.markdown(
                                f"""
                                <div style="position: relative; width: 100vw !important; max-width: 100vw !important; left: 50% !important; right: 50% !important; margin-left: -50vw !important; margin-right: -50vw !important; padding: 0 !important; box-sizing: border-box !important;">
                                <textarea readonly style="width: 100% !important; height: 700px !important; font-family: monospace !important; font-size: 0.85em !important; padding: 12px !important; background-color: #1e1e1e !important; color: #d4d4d4 !important; border: 1px solid #3e3e3e !important; border-radius: 4px !important; resize: both !important; overflow-y: auto !important; line-height: 1.4 !important; box-sizing: border-box !important; display: block !important;">{log_text_escaped}</textarea>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                except subprocess.TimeoutExpired:
                    status_placeholder.error("⏱️ 크롤링이 시간 초과되었습니다. (10분)")
                except Exception as e:
                    status_placeholder.error(f"❌ 오류: {e}")
                    import traceback
                    log_placeholder.code(traceback.format_exc(), language="text")
        
        if not articles:
            st.info("아직 추천 기사가 없습니다. 위의 '🔄 지금 다시 크롤링하기' 버튼을 눌러 오늘의 기사를 불러오세요.")
        else:
            # 정렬 옵션
            col1, col2 = st.columns(2)
            with col1:
                sort_by = st.selectbox(
                    "정렬 기준",
                    options=["관련도 점수 (내림차순)", "날짜 (최신순)", "날짜 (오래된순)"],
                    key="daily_sort_by",
                )
            with col2:
                if date_str:
                    st.caption(f"📅 추천 기사 날짜: {date_str}")
                    
                    # 크롤링 시간 표시
                    crawl_time_str = get_crawl_time_display()
                    if crawl_time_str:
                        st.caption(f"🕐 크롤링 시간: {crawl_time_str}")
            
            # 정렬 적용
            # daily_fetch.py에서 이미 4일 이내 기사만 필터링하여 저장했으므로,
            # 여기서는 필터링하지 않고 그대로 표시합니다.
            sorted_articles = articles.copy()
            if sort_by == "관련도 점수 (내림차순)":
                sorted_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            elif sort_by == "날짜 (최신순)":
                sorted_articles.sort(key=lambda x: x.get("pubDate", ""), reverse=True)
            elif sort_by == "날짜 (오래된순)":
                sorted_articles.sort(key=lambda x: x.get("pubDate", ""))
            
            st.write(f"총 {len(sorted_articles)}개의 추천 기사가 있습니다. (오늘 기준 4일 내)")
            
            # 기사 목록을 테이블 형식으로 표시 (각 열 왼쪽 정렬)
            for idx, article in enumerate(sorted_articles):
                # 전체 제목이 있으면 사용, 없으면 기존 제목 사용
                title = clean_html_tags(article.get("full_title") or article.get("title", ""))
                # 제목에서 불필요한 접미사 제거
                title = clean_title_suffix(title)
                description = clean_html_tags(article.get("description", ""))
                link = article.get("link", "")
                pub_date = article.get("pubDate", "")
                score = article.get("relevance_score", 0)
                
                # 기존 데이터가 이전 점수 체계(100점 만점)로 저장되어 있을 수 있으므로 10점으로 제한
                if score > 10.0:
                    score = 10.0
                
                # 날짜 포맷팅 (예: 25.12.24.(수))
                date_display = ""
                if pub_date:
                    try:
                        # 여러 날짜 형식 처리
                        from datetime import datetime
                        dt = None
                        
                        # ISO 형식 (예: "2024-12-24T09:00:00+09:00")
                        if "T" in pub_date:
                            date_part = pub_date.split("T")[0]
                            year, month, day = date_part.split("-")
                            dt = datetime(int(year), int(month), int(day))
                        # "Thu, 27 No" 또는 "Sun, 30 Nov 2024" 같은 형식 처리
                        elif re.match(r"^[A-Za-z]{3},\s*\d{1,2}\s+[A-Za-z]{2,3}", pub_date):
                            # 월 이름 매핑
                            month_map = {
                                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                                "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
                                "No": 11, "De": 12  # 잘린 형식도 처리
                            }
                            
                            # "Thu, 27 No" 또는 "Sun, 30 Nov 2024" 파싱
                            parts = pub_date.split()
                            if len(parts) >= 3:
                                day = int(parts[1].rstrip(","))
                                month_name = parts[2]
                                month = month_map.get(month_name, 11)
                                
                                # 년도가 있으면 사용, 없으면 현재 년도
                                if len(parts) >= 4:
                                    year = int(parts[3])
                                else:
                                    year = get_kst_now().year
                                
                                dt = datetime(year, month, day)
                        # "2024-12-24" 형식
                        elif re.match(r"^\d{4}-\d{2}-\d{2}", pub_date):
                            dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                        
                        if dt:
                            weekdays = ["월", "화", "수", "목", "금", "토", "일"]
                            weekday = weekdays[dt.weekday()]
                            year_str = str(dt.year)[2:]  # 2자리 년도
                            month_str = f"{dt.month:02d}"  # 2자리 월
                            day_str = f"{dt.day:02d}"  # 2자리 일
                            date_display = f"{year_str}.{month_str}.{day_str}.({weekday})"
                    except Exception as e:
                        # 파싱 실패 시 빈 문자열 (영어 날짜는 표시하지 않음)
                        date_display = ""
                
                date_text = date_display if date_display else "-"
                score_display = f"{score:.1f}/10점" if score > 0 else "-"
                
                # 3열 레이아웃으로 표시 (각 열 왼쪽 정렬, 고정 너비)
                # 제목 공간 최대화, 날짜와 관련도는 최소 공간만 사용하고 5mm 간격 유지
                # 비율: 제목(최대한 넓게), 날짜(최소, 한 줄 유지), 관련도(최소, 오른쪽 정렬)
                # 날짜와 관련도 간 간격은 5mm 정도로 유지 (columns 비율로 조정)
                col_title, col_date, col_score = st.columns([8, 0.85, 0.6])
                
                with col_title:
                    # 제목을 expander 헤더로 사용 (제목 클릭 시 확장)
                    expander_key = f"article_expander_{idx}"
                    # URL 파라미터로 온 기사는 자동으로 확장
                    is_expanded = (auto_expand_idx == idx) if auto_expand_idx is not None else False
                    with st.expander(title, expanded=is_expanded):
                        # 상세 정보는 expander 내부에 표시 (전체 너비 사용)
                        _render_article_details(article, title, description, link, pub_date, score, idx)
                
                with col_date:
                    # 날짜 표시 (expander 헤더와 수직 정렬)
                    st.markdown(f"<div style='text-align: right; margin-top: 0.5rem; margin-right: 2mm; white-space: nowrap; font-size: 0.9em;'>{date_text}</div>", unsafe_allow_html=True)
                
                with col_score:
                    # 관련도 표시 (expander 헤더와 수직 정렬)
                    st.markdown(f"<div style='text-align: right; margin-top: 0.5rem; white-space: nowrap; font-size: 0.9em;'>{score_display}</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("기록 보기")
        history = get_crawl_history()
        if not history:
            st.info("아직 크롤링 기록이 없습니다.")
        else:
            st.table(history)


if __name__ == "__main__":
    main()



