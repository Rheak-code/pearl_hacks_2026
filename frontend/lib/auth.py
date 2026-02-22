import streamlit as st

def signup(email: str, password: str) -> tuple[bool, str]:
    users = st.session_state["users"]
    if not email or "@" not in email:
        return False, "Enter a valid email."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if email in users:
        return False, "User already exists."
    users[email] = {"password": password}
    return True, "Account created. Please log in."

def login(email: str, password: str) -> tuple[bool, str]:
    users = st.session_state["users"]
    if email not in users:
        return False, "No account found. Please sign up."
    if users[email]["password"] != password:
        return False, "Incorrect password."
    st.session_state["is_authed"] = True
    st.session_state["user_email"] = email
    return True, "Logged in!"

def logout():
    st.session_state["is_authed"] = False
    st.session_state["user_email"] = None