import streamlit as st
from lib.ui import require_auth

require_auth()

st.title("👤 Personal Data")

p = st.session_state["profile"]

with st.form("profile_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=int(p["age"]))
    income = st.number_input("Annual income ($)", min_value=0, value=int(p["income"]), step=1000)
    expenses = st.number_input("Monthly expenses ($)", min_value=0, value=int(p["expenses"]), step=100)
    current_savings = st.number_input("Current savings ($)", min_value=0, value=int(p["current_savings"]), step=500)
    retirement_age = st.number_input("Target retirement age", min_value=0, max_value=120, value=int(p["retirement_age"]))
    risk = st.selectbox("Risk tolerance", ["Low", "Medium", "High"], index=["Low","Medium","High"].index(p["risk_tolerance"]))

    submitted = st.form_submit_button("Save")
    if submitted:
        st.session_state["profile"] = {
            "age": int(age),
            "income": int(income),
            "expenses": int(expenses),
            "current_savings": int(current_savings),
            "retirement_age": int(retirement_age),
            "risk_tolerance": risk,
        }
        st.success("Saved!")