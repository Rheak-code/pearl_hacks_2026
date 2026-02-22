import streamlit as st
import httpx
from lib.theme import apply_theme, topbar

apply_theme()
topbar()

# ---------- API CONFIG ----------
API_BASE = "http://127.0.0.1:8000"  # <-- Make sure your FastAPI backend runs on this port

# ---------- API CALL ----------
def call_simulation(assets: dict, liabilities: dict, shock_bps: float):
    payload = {
        "assets": assets,
        "liabilities": liabilities,
        "rateShockBps": shock_bps
    }
    try:
        response = httpx.post(f"{API_BASE}/simulate_rate_shock", json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except httpx.ConnectError:
        st.error("Cannot connect to API. Is FastAPI running on port 8001?")
        return None
    except httpx.HTTPStatusError as e:
        st.error(f"API returned an error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# ---------- STREAMLIT UI ----------
st.title("Rate Shock Simulator")

# Assets
st.subheader("Assets")
col1, col2, col3 = st.columns(3)
cash = col1.number_input("Cash", value=50000.0)
bonds = col2.number_input("Bonds", value=100000.0)
equities = col3.number_input("Equities", value=150000.0)

# Liabilities
st.subheader("Liabilities")
col1, col2 = st.columns(2)
fixed_mortgage = col1.number_input("Fixed Mortgage", value=200000.0)
variable_debt = col2.number_input("Variable Debt", value=50000.0)

col1, col2, col3 = st.columns(3)
remaining_years = col1.number_input("Remaining Years", value=25)
mortgage_rate = col2.number_input("Mortgage Rate %", value=6.5) / 100
variable_rate = col3.number_input("Variable Rate %", value=8.0) / 100

# Shock input
shock_bps = st.slider("Rate Shock (bps)", -200, 200, 100, step=25)

# Run simulation
if st.button("Run Simulation"):
    with st.spinner("Calling API..."):
        result = call_simulation(
            assets={"cash": cash, "bonds": bonds, "equities": equities},
            liabilities={
                "fixed_mortgage": fixed_mortgage,
                "variable_debt": variable_debt,
                "remaining_years": remaining_years,
                "mortgage_rate": mortgage_rate,
                "variable_rate": variable_rate
            },
            shock_bps=shock_bps
        )

        if result:
            st.success("Simulation complete!")
            col1, col2 = st.columns(2)
            col1.metric("Net Worth Impact", f"${result['netWorthDelta']:,}")
            col2.metric("Monthly Payment Increase", f"${result['newMonthlyPaymentIncrease']:,.2f}")

            col1, col2 = st.columns(2)
            col1.metric("Duration Gap", result['durationGap'])
            col2.metric("Risk Level", result['riskClassification'])