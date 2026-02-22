import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import httpx
from lib.theme import apply_theme, topbar

apply_theme()
topbar()

API_BASE = "http://127.0.0.1:8000"  # FastAPI base URL

def call_simulation(assets: dict, liabilities: dict, shock_bps: float):
    payload = {"assets": assets, "liabilities": liabilities, "rateShockBps": shock_bps}
    try:
        r = httpx.post(f"{API_BASE}/simulate_rate_shock", json=payload, timeout=30.0)
        r.raise_for_status()
        return r.json()
    except httpx.ConnectError:
        st.error(f"Cannot connect to API at {API_BASE}. Is FastAPI running on port 8000?")
        return None
    except httpx.HTTPStatusError as e:
        st.error(f"API returned an error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

st.title("📈 Invest")
st.caption("Stress-test your portfolio against a rate shock (uses the same backend as the simulator).")

p = st.session_state.get("profile", {})
risk = p.get("risk_tolerance", "Medium")
st.write(f"Risk tolerance (from profile): **{risk}**")

st.subheader("Portfolio (Assets)")
a1, a2, a3 = st.columns(3)
cash = a1.number_input("Cash ($)", min_value=0.0, value=float(p.get("cash", 50_000.0)), step=1000.0)
bonds = a2.number_input("Bonds ($)", min_value=0.0, value=float(p.get("bonds", 100_000.0)), step=1000.0)
equities = a3.number_input("Equities ($)", min_value=0.0, value=float(p.get("equities", 150_000.0)), step=1000.0)

st.subheader("Debt (Liabilities)")
l1, l2 = st.columns(2)
fixed_mortgage = l1.number_input("Fixed Mortgage ($)", min_value=0.0, value=float(p.get("fixed_mortgage", 200_000.0)), step=1000.0)
variable_debt = l2.number_input("Variable Debt ($)", min_value=0.0, value=float(p.get("variable_debt", 50_000.0)), step=1000.0)

l3, l4, l5 = st.columns(3)
remaining_years = l3.number_input("Remaining Years", min_value=1, value=int(p.get("remaining_years", 25)), step=1)
mortgage_rate = (l4.number_input("Mortgage Rate %", min_value=0.0, value=float(p.get("mortgage_rate_pct", 6.5)), step=0.1) / 100.0)
variable_rate = (l5.number_input("Variable Rate %", min_value=0.0, value=float(p.get("variable_rate_pct", 8.0)), step=0.1) / 100.0)

shock_bps = st.slider("Rate Shock (bps)", -200, 200, 100, step=25)

if st.button("Run Invest Stress Test", use_container_width=True):
    with st.spinner("Calling API..."):
        result = call_simulation(
            assets={"cash": cash, "bonds": bonds, "equities": equities},
            liabilities={
                "fixed_mortgage": fixed_mortgage,
                "variable_debt": variable_debt,
                "remaining_years": int(remaining_years),
                "mortgage_rate": float(mortgage_rate),
                "variable_rate": float(variable_rate),
            },
            shock_bps=float(shock_bps),
        )

    if result:
        st.success("Simulation complete!")

        c1, c2 = st.columns(2)
        c1.metric("Net Worth Impact", f"${result['netWorthDelta']:,.2f}")
        c2.metric("Monthly Payment Increase", f"${result['newMonthlyPaymentIncrease']:,.2f}")

        c3, c4 = st.columns(2)
        c3.metric("Duration Gap", f"{result['durationGap']}")
        c4.metric("Risk Level", f"{result['riskClassification']}")

        st.divider()
        if result["netWorthDelta"] < 0:
            st.warning("This scenario hurts net worth. Consider shifting exposure (e.g., duration, equities) or reducing variable-rate debt.")
        else:
            st.info("This scenario is resilient. Try increasing the shock or changing the mix to test sensitivity.")