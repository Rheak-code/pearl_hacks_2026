import streamlit as st
from lib.auth import signup

st.title("🧾 Signup")

email = st.text_input("Email", placeholder="you@example.com")
password = st.text_input("Password (min 6 chars)", type="password")
confirm = st.text_input("Confirm password", type="password")

if st.button("Create account", use_container_width=True):
    if password != confirm:
        st.error("Passwords do not match.")
    else:
        ok, msg = signup(email, password)
        if ok:
            st.success(msg)
            st.switch_page("pages/02_Login.py")
        else:
            st.error(msg)