import streamlit as st
from lib.state import init_state
from lib.ui import app_header, sidebar_nav, require_auth

st.set_page_config(page_title="Finance App", page_icon="💸", layout="wide")

init_state()

app_header()
sidebar_nav()

# Optional: If you want to force auth globally, uncomment:
# require_auth()

st.write("Use the sidebar to navigate pages.")
st.info("Tip: Put your main app shell here. Pages live in frontend/pages/.")