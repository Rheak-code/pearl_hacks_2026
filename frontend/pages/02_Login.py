import streamlit as st
from lib.auth import login

st.title("🔐 Login")

email = st.text_input("Email", placeholder="you@example.com")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)
with col1:
    if st.button("Login", use_container_width=True):
        ok, msg = login(email, password)
        if ok:
            st.success(msg)
            st.switch_page("pages/01_Home.py")
        else:
            st.error(msg)
with col2:
    if st.button("Go to Signup", use_container_width=True):
        st.switch_page("pages/03_Signup.py")