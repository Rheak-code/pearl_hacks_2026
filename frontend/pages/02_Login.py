import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from lib.theme import apply_theme, topbar
from lib.auth import login

apply_theme()
topbar()

st.title("🔐 Login")

email = st.text_input("Email", placeholder="you@example.com")
password = st.text_input("Password", type="password")

if st.button("Continue", use_container_width=True):
    ok, msg = login(email, password)
    if ok:
        st.success(msg)
        st.switch_page("pages/05_Invest.py")  # or 06_Retire.py / 04_GenStats.py
    else:
        st.error(msg)

st.caption("No account yet? Go to Signup.")
if st.button("Go to Signup", use_container_width=True):
    st.switch_page("pages/03_Signup.py")