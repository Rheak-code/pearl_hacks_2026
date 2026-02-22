import streamlit as st

def init_state():
    # Auth
    st.session_state.setdefault("is_authed", False)
    st.session_state.setdefault("user_email", None)

    # Simple “DB” placeholders
    st.session_state.setdefault("users", {})  # {email: {"password": "..."}}

    # Personal data / profile
    st.session_state.setdefault("profile", {
        "age": 22,
        "income": 80000,
        "expenses": 3500,
        "risk_tolerance": "Medium",
        "current_savings": 10000,
        "retirement_age": 65,
    })