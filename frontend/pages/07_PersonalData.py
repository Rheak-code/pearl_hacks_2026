import streamlit as st
from lib.ui import require_auth
from lib.theme import apply_theme, topbar

apply_theme()
topbar()
require_auth()

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="mm-card">', unsafe_allow_html=True)
st.subheader("Link your bank account")
st.caption("Starter form — wire to Plaid later if you want.")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    addr1 = st.text_input("Address Line 1")
    addr2 = st.text_input("Address Line 2")
    zipc  = st.text_input("Zip Code")
    state = st.text_input("State")

with c2:
    age = st.number_input("Age", min_value=0, max_value=120, value=22)
    income = st.number_input("Average Annual Income", min_value=0, value=80000, step=1000)
    emp = st.text_input("Employment status")
    industry = st.text_input("Industry")

with c3:
    hh = st.number_input("Household Size", min_value=1, value=1)
    relationship = st.selectbox("Single/Married/Partnership", ["Single", "Married", "Partnership"])
    deps = st.number_input("Number of Dependents", min_value=0, value=0)

st.markdown("<br>", unsafe_allow_html=True)
_, center, _ = st.columns([1, 0.5, 1])
with center:
    if st.button("Next", use_container_width=True):
        # Save to session state or send to backend
        st.session_state["profile"].update({
            "age": int(age),
            "income": int(income),
        })
        st.switch_page("pages/04_GenStats.py")

st.markdown("</div>", unsafe_allow_html=True)