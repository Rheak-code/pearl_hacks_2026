import streamlit as st
from lib.auth import logout

def app_header():
    cols = st.columns([1, 3, 1])
    with cols[0]:
        st.markdown("## 💸")
    with cols[1]:
        st.markdown("## Finance Coach")
        st.caption("Budget • Investing • Retirement • Insights")
    with cols[2]:
        if st.session_state.get("is_authed"):
            st.caption(f"Signed in as **{st.session_state.get('user_email')}**")
            if st.button("Log out", use_container_width=True):
                logout()
                st.switch_page("pages/02_Login.py")

def sidebar_nav():
    st.sidebar.title("Navigation")
    if st.session_state.get("is_authed"):
        st.sidebar.success("Authenticated ✅")
    else:
        st.sidebar.warning("Not logged in")

    st.sidebar.caption("Use Streamlit's page list below (built-in).")

def require_auth():
    if not st.session_state.get("is_authed"):
        st.warning("Please log in to continue.")
        st.button("Go to Login", on_click=lambda: st.switch_page("pages/02_Login.py"), use_container_width=True)    
        st.stop()