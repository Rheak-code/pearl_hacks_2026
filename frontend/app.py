import streamlit as st
from lib.state import init_state
from lib.theme import apply_theme, topbar

st.set_page_config(page_title="Momentum", page_icon="💸", layout="wide")

init_state()
apply_theme()
topbar()

st.header("Balance your Money. Own your Future.", anchor=None)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Login", use_container_width=True, key="login_btn"):
        st.switch_page("pages/02_Login.py")  # relative to app root

st.html(
    """
    <div style="text-align: center; color: white;">
        <h1 style="font-weight:500;">Balance your Money. Own your Future.</h1>

        <div style="width:300px;height:3px;background:#ffffff55;margin:20px auto;"></div>

        <p style="max-width:800px;margin:0 auto;font-size:18px;line-height:1.6;">
            Money is more complex than ever. Rates change, inflation rises, and markets shift—
            yet most people don’t see how it impacts their everyday finances.
        </p>
    </div>
    """)

st.write("")  # landing shell if needed