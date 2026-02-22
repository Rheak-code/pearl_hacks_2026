import streamlit as st
from lib.theme import apply_theme, topbar
from lib.auth import login

apply_theme()
topbar()

st.markdown("<br>", unsafe_allow_html=True)

# Centered beige card
left, mid, right = st.columns([1, 1.2, 1])
with mid:
    st.html('<div class="mm-card"><h1 style="text-align:center; color:#123; font-weight:800;">Log In</h1></div>')

    email = st.text_input("Username", placeholder="Username")
    password = st.text_input("Password", type="password", placeholder="Password")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue", use_container_width=True):
        ok, msg = login(email, password)
        if ok:
            st.success(msg)
            st.switch_page("pages/04_GenStats.py")
        else:
            st.error(msg)

    st.markdown(
        '<p style="text-align:center;margin-top:14px;">Don’t have an account? '
        '<a style="color:#0f0c4b;font-weight:600;" href="#">Click here to Sign Up</a></p>',
        unsafe_allow_html=True,
    )

    if st.button("Go to Signup", use_container_width=True):
        st.switch_page("pages/03_Signup.py")

    st.markdown("</div>", unsafe_allow_html=True)