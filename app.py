import streamlit as st
import json
import os
from pattern_filter import PatternFilter

# 패턴 파일 경로 (app.py와 동일 디렉토리에 위치)
PATTERN_FILE = "patterns.json"

def load_patterns():
    """
    패턴 JSON 파일을 로드합니다.
    파일이 없으면 빈 구조로 초기화합니다.
    """
    if os.path.exists(PATTERN_FILE):
        with open(PATTERN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"literals": {}, "regex": {}}
    return data

def save_patterns(data):
    """
    data 내용을 PATTERN_FILE에 저장합니다.
    """
    with open(PATTERN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.title("패턴 관리 및 텍스트 검출 UI")

# 사이드바 메뉴 구성
st.sidebar.title("메뉴")
menu_option = st.sidebar.selectbox("메뉴 선택", ["패턴 추가", "패턴 목록 확인", "텍스트 검출 테스트"])

if menu_option == "패턴 추가":
    st.header("패턴 추가")
    pattern_type = st.radio("패턴 유형 선택", ("literal", "regex"))
    
    pattern_input = st.text_input("패턴 입력", placeholder="예: 시발 또는 f[o0]o")
    category_input = st.text_input("카테고리 입력", placeholder="예: 욕설, 금지어 등")
    
    if st.button("패턴 추가하기"):
        if pattern_input and category_input:
            data = load_patterns()
            if pattern_type == "literal":
                data.setdefault("literals", {})[pattern_input] = category_input
            else:
                data.setdefault("regex", {})[pattern_input] = category_input
            save_patterns(data)
            st.success(f"{pattern_type} 패턴 '{pattern_input}' ({category_input}) 추가됨.")
        else:
            st.error("패턴과 카테고리를 모두 입력해주세요.")

elif menu_option == "패턴 목록 확인":
    st.header("현재 등록된 패턴 목록")
    data = load_patterns()
    
    st.subheader("Literal 패턴")
    if data.get("literals"):
        for pat, cat in data["literals"].items():
            st.write(f"패턴: `{pat}`  →  카테고리: **{cat}**")
    else:
        st.write("등록된 literal 패턴이 없습니다.")
    
    st.subheader("Regex 패턴")
    if data.get("regex"):
        for pat, cat in data["regex"].items():
            st.write(f"패턴: `{pat}`  →  카테고리: **{cat}**")
    else:
        st.write("등록된 regex 패턴이 없습니다.")

elif menu_option == "텍스트 검출 테스트":
    st.header("텍스트 검출 테스트")
    test_text = st.text_area("검사할 텍스트 입력", placeholder="검출할 텍스트를 입력하세요.")
    
    if st.button("검출 테스트"):
        if test_text:
            # 최신 패턴 파일을 기반으로 PatternFilter 인스턴스 생성
            pf = PatternFilter(PATTERN_FILE)
            detected, categories = pf.match(test_text)
            if detected:
                st.success("검출됨!")
                st.write("검출된 카테고리:")
                for cat in categories:
                    st.write(f"- {cat}")
            else:
                st.info("검출되지 않음.")
        else:
            st.error("검사할 텍스트를 입력해주세요.")
