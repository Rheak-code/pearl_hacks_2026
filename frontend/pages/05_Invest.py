import streamlit as st
from lib.ui import require_auth

require_auth()

st.title("📈 Invest")

p = st.session_state["profile"]
risk = p["risk_tolerance"]

st.write(f"Your current risk tolerance: **{risk}**")

risk_to_alloc = {
    "Low": {"Stocks": 30, "Bonds": 60, "Cash": 10},
    "Medium": {"Stocks": 60, "Bonds": 30, "Cash": 10},
    "High": {"Stocks": 80, "Bonds": 15, "Cash": 5},
}

alloc = risk_to_alloc.get(risk, risk_to_alloc["Medium"])

st.subheader("Suggested allocation (starter)")
st.bar_chart(alloc)

st.divider()
st.subheader("What if I invest monthly?")
monthly = st.number_input("Monthly investment ($)", min_value=0, value=500, step=50)
years = st.slider("Years", 1, 40, 20)
rate = st.slider("Estimated annual return (%)", 1.0, 12.0, 7.0, 0.5)

# simple future value of monthly contributions (approx)
r = (rate / 100) / 12
n = years * 12
fv = monthly * (((1 + r) ** n - 1) / r) if r > 0 else monthly * n
st.metric("Estimated future value", f"${fv:,.0f}")
st.caption("This is a simplified estimate (not financial advice).")