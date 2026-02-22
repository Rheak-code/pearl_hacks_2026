import streamlit as st
from lib.ui import require_auth
import streamlit as st
from lib.theme import apply_theme, topbar

apply_theme()
topbar()
require_auth()

st.title("📊 General Stats")

p = st.session_state["profile"]
income = p["income"]
expenses_monthly = p["expenses"]
savings = p["current_savings"]

monthly_savings = (income / 12) - expenses_monthly

c1, c2, c3 = st.columns(3)
c1.metric("Annual Income", f"${income:,.0f}")
c2.metric("Monthly Expenses", f"${expenses_monthly:,.0f}")
c3.metric("Est. Monthly Savings", f"${monthly_savings:,.0f}")

st.divider()
st.subheader("Notes")
st.write("- These are simple derived numbers from your Personal Data page.")
st.write("- Later, you can replace with real backend calculations.")