import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. 페이지 설정 (가로로 넓게 사용, 타이틀 설정)
st.set_page_config(page_title="우리 가족 지출 관리", layout="wide", initial_sidebar_state="collapsed")

# 2. 디자인 테마 변경 (스트림릿 기본 UI 숨기기 및 여백 제거)
st.markdown("""
    <style>
        /* 상단 헤더(햄버거 메뉴 등) 숨기기 */
        header {visibility: hidden;}
        /* 하단 워터마크 숨기기 */
        footer {visibility: hidden;}
        /* 전체 화면 상하좌우 여백 최소화 */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        /* iframe 테두리 제거 */
        iframe {
            border: none !important;
        }
        /* 로그인 박스 스타일링 */
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #2563eb;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# GAS 웹 앱 URL (1단계에서 복사한 주소 붙여넣기 - 반드시 큰따옴표 안에 넣으세요)
GAS_AUTH_URL = "https://script.google.com/macros/s/AKfycbw8aSdAa1SftZvt8tLhhD4haOmVZgBjP0yHyLs-f9HsZLdutjscf6jtP_NGYpgUKNTojg/exec"

# 세션 상태 초기화 (로그인 여부 저장)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""

# 로그인 함수
def login(user_id, user_pw):
    payload = {'id': user_id, 'pw': user_pw}
    try:
        response = requests.post(GAS_AUTH_URL, data=payload)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        st.error(f"인증 서버 오류: {e}")
        return False

# ----------------- 화면 렌더링 -----------------
if not st.session_state['logged_in']:
    # 로그인을 화면 가운데 정렬하기 위해 빈 컬럼 사용 (좌우 여백 생성)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # 위쪽 여백
        st.markdown("<h2 style='text-align: center; color: #1f2937;'>🏠 가족 지출 관리</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>로그인하여 대시보드에 접속하세요</p>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            user_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            user_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            submit_button = st.form_submit_button("로그인하기")
            
            if submit_button:
                if login(user_id, user_pw):
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = user_id
                    st.rerun()  # 화면 새로고침
                else:
                    st.error("아이디 또는 비밀번호가 틀렸습니다.")
else:
    # 로그인 성공 시 HTML 대시보드 렌더링
    
    # 우측 상단 로그아웃 버튼 배치
    col_empty, col_btn = st.columns([9, 1])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True) # 간격 조절
        if st.button("로그아웃 🚪"):
             st.session_state['logged_in'] = False
             st.session_state['current_user'] = ""
             st.rerun()
             
    # HTML 파일 읽기 및 Streamlit 화면에 삽입
    try:
        with open("budget_dashboard.html", "r", encoding="utf-8") as f:
            html_code = f.read()
        
        # Python에서 저장한 로그인 유저 ID를 HTML 코드에 자바스크립트 변수로 주입
        user_id = st.session_state['current_user']
        injection_script = f"<script>window.INJECTED_USER = '{user_id}';</script>"
        html_code = html_code.replace("</head>", injection_script + "\n</head>")
        
        # height를 대폭 늘려 스크롤 이중 발생 방지, width는 자동으로 꽉 참
        components.html(html_code, height=1800, scrolling=True)
    except FileNotFoundError:
        st.error("HTML 파일을 찾을 수 없습니다. 깃허브 저장소에 'team_budget_dashboard.html' 파일이 업로드 되어 있는지 확인해주세요.")
