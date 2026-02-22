import streamlit as st
from lib.ui import require_auth

require_auth()

st.title("🏖️ Retirement")

p = st.session_state["profile"]
age = p["age"]
retire_age = p["retirement_age"]
current = p["current_savings"]

years_left = max(0, retire_age - age)

st.write(f"Years until retirement: **{years_left}**")

monthly = st.number_input("Monthly retirement contribution ($)", min_value=0, value=600, step=50)
rate = st.slider("Estimated annual return (%)", 1.0, 10.0, 6.0, 0.5)

r = (rate / 100) / 12
n = years_left * 12

fv_contrib = monthly * (((1 + r) ** n - 1) / r) if (r > 0 and n > 0) else monthly * n
fv_total = current * ((1 + r) ** n) + fv_contrib if (r > 0 and n > 0) else current + fv_contrib

c1, c2 = st.columns(2)
c1.metric("Current savings", f"${current:,.0f}")
c2.metric("Projected at retirement", f"${fv_total:,.0f}")

st.caption("Starter projection only. Hook to your backend model later.")