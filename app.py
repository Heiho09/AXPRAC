import streamlit as st
import requests
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="우리 가족 지출 관리", layout="wide")

# GAS 웹 앱 URL (1단계에서 복사한 주소 붙여넣기)
GAS_AUTH_URL = "https://script.google.com/macros/s/AKfycbw8aSdAa1SftZvt8tLhhD4haOmVZgBjP0yHyLs-f9HsZLdutjscf6jtP_NGYpgUKNTojg/exec"

# 세션 상태 초기화 (로그인 여부 저장)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 로그인 함수
def login(user_id, user_pw):
    # GAS로 인증 요청 보내기
    payload = {'id': user_id, 'pw': user_pw}
    try:
        response = requests.post(GAS_AUTH_URL, data=payload)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        st.error(f"인증 서버 오류: {e}")
        return False

# 화면 렌더링
if not st.session_state['logged_in']:
    st.title("🔒 로그인")
    with st.form("login_form"):
        user_id = st.text_input("아이디")
        user_pw = st.text_input("비밀번호", type="password")
        submit_button = st.form_submit_button("로그인")
        
        if submit_button:
            if login(user_id, user_pw):
                st.session_state['logged_in'] = True
                st.success("로그인 성공!")
                st.rerun()  # 화면 새로고침
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")
else:
    # 로그인 성공 시 HTML 대시보드 렌더링
    st.title("🏠 가족 지출 관리 대시보드")
    if st.button("로그아웃"):
         st.session_state['logged_in'] = False
         st.rerun()
         
    # HTML 파일 읽기 및 Streamlit 화면에 삽입 (iframe 형태)
    with open("budget_dashboard.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # height를 충분히 주어 스크롤 없이 보이게 설정
    components.html(html_code, height=1200, scrolling=True)
