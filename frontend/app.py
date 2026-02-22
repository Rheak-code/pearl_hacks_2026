import streamlit as st
from lib.state import init_state
from lib.theme import apply_theme, topbar

st.set_page_config(page_title="Momentum", page_icon="💸", layout="wide")

init_state()
apply_theme()
topbar()

st.write("")  # landing shell if needed