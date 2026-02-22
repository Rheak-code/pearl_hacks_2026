import streamlit as st

st.title("🏠 Home")
st.write("Welcome! Use the sidebar to go to Login/Signup, then explore your stats.")

col1, col2, col3 = st.columns(3)
col1.metric("Net Worth Δ", "$3,681.25")
col2.metric("Monthly Payment Δ", "$7.25")
col3.metric("Risk", "High")

st.divider()
st.subheader("Quick actions")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Go to General Stats"):
        st.switch_page("pages/04_GenStats.py")
with c2:
    if st.button("Go to Investing"):
        st.switch_page("pages/05_Invest.py")
with c3:
    if st.button("Update Personal Data"):
        st.switch_page("pages/07_PersonalData.py")