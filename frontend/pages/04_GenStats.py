import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import httpx
from lib.theme import apply_theme, topbar

apply_theme()
topbar()

# ---------- API CONFIG ----------
API_BASE = "http://127.0.0.1:8000"

# ---------- API CALL ----------
def call_simulation(assets: dict, liabilities: dict, shock_bps: float):
    payload = {"assets": assets, "liabilities": liabilities, "rateShockBps": shock_bps}
    try:
        r = httpx.post(f"{API_BASE}/simulate_rate_shock", json=payload, timeout=30.0)
        r.raise_for_status()
        return r.json()
    except httpx.ConnectError:
        st.error(f"Cannot connect to API at {API_BASE}. Is FastAPI running?")
        return None
    except httpx.HTTPStatusError as e:
        st.error(f"API error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


# ---------- PAGE HEADER ----------
st.title("📊 General Stats")
st.caption("Rate Shock Simulator")

# ---------- DEFAULTS ----------
p = st.session_state.get("profile", {})

default_cash = float(p.get("cash", 50_000.0))
default_bonds = float(p.get("bonds", 100_000.0))
default_equities = float(p.get("equities", 150_000.0))
default_fixed_mortgage = float(p.get("fixed_mortgage", 200_000.0))
default_variable_debt = float(p.get("variable_debt", 50_000.0))
default_remaining_years = int(p.get("remaining_years", 25))
default_mortgage_rate_pct = float(p.get("mortgage_rate_pct", 6.5))
default_variable_rate_pct = float(p.get("variable_rate_pct", 8.0))


# ---------- INPUT CARD ----------
st.subheader("Assets")
st.button("Link Bank Account", disabled=True)  # placeholder for future credit card input UI

a1, a2, a3 = st.columns(3)
cash = a1.number_input("Cash ($)", min_value=0.0, value=default_cash, step=1000.0)
bonds = a2.number_input("Bonds ($)", min_value=0.0, value=default_bonds, step=1000.0)
equities = a3.number_input("Equities ($)", min_value=0.0, value=default_equities, step=1000.0)

st.subheader("Liabilities")
l1, l2 = st.columns(2)
fixed_mortgage = l1.number_input("Fixed Mortgage ($)", min_value=0.0, value=default_fixed_mortgage, step=1000.0)
variable_debt = l2.number_input("Variable Debt ($)", min_value=0.0, value=default_variable_debt, step=1000.0)

l3, l4, l5 = st.columns(3)
remaining_years = l3.number_input("Remaining Years", min_value=1, value=default_remaining_years, step=1)
mortgage_rate = (l4.number_input("Mortgage Rate %", min_value=0.0, value=default_mortgage_rate_pct, step=0.1) / 100.0)
variable_rate = (l5.number_input("Variable Rate %", min_value=0.0, value=default_variable_rate_pct, step=0.1) / 100.0)

shock_bps = st.slider("Rate Shock (bps)", -200, 200, 100, step=25)

run = st.button("Run Simulation", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ---------- RUN SIMULATION ----------
if run:
    with st.spinner("Running simulation..."):
        result = call_simulation(
            assets={"cash": float(cash), "bonds": float(bonds), "equities": float(equities)},
            liabilities={
                "fixed_mortgage": float(fixed_mortgage),
                "variable_debt": float(variable_debt),
                "remaining_years": int(remaining_years),
                "mortgage_rate": float(mortgage_rate),
                "variable_rate": float(variable_rate),
            },
            shock_bps=float(shock_bps),
        )

    if result:
        st.success("Simulation Complete")

        # ---------- METRICS CARD ----------

        c1, c2 = st.columns(2)
        c1.metric("Net Worth Impact", f"${result['netWorthDelta']:,.2f}")
        c2.metric("Monthly Payment Change", f"${result['newMonthlyPaymentIncrease']:,.2f}")

        c3, c4 = st.columns(2)
        c3.metric("Duration Gap", f"{result['durationGap']}")
        c4.metric("Risk Level", f"{result['riskClassification']}")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- CONTEXT SECTION ----------

        st.subheader("📘 What This Means For You")

        shock_direction = "increase" if shock_bps > 0 else "decrease"
        net_delta = result["netWorthDelta"]
        payment_delta = result["newMonthlyPaymentIncrease"]
        risk = result["riskClassification"]

        if net_delta < 0:
            net_msg = f"Your total net worth would decrease by approximately ${abs(net_delta):,.2f}."
        else:
            net_msg = f"Your total net worth would increase by approximately ${net_delta:,.2f}."

        if payment_delta > 0:
            pay_msg = f"Your monthly debt payments would rise by about ${payment_delta:,.2f}, reducing cash flow."
        elif payment_delta < 0:
            pay_msg = f"Your monthly debt payments would decrease by about ${abs(payment_delta):,.2f}, improving flexibility."
        else:
            pay_msg = "Your monthly payments would remain unchanged."

        if risk.lower() in ["high", "severe"]:
            risk_msg = "Your financial structure is highly sensitive to rate changes."
            st.error("⚠ High sensitivity to interest rate movement.")
        elif risk.lower() in ["moderate", "medium"]:
            risk_msg = "Your portfolio shows moderate exposure to interest rate shifts."
            st.warning("⚠ Moderate exposure detected.")
        else:
            risk_msg = "Your financial position appears resilient to this rate movement."
            st.success("✓ Low interest rate sensitivity.")

        st.html(
    f"""
    <div style="
        font-size:20px;
        line-height:1.7;
        color:#1a1a1a;
        margin-top:15px;
        ">
        <p style="font-size:22px; font-weight:600; margin-bottom:18px;">
            Based on a {abs(shock_bps)} basis point {shock_direction} in interest rates:
        </p>

        <p style="margin-bottom:12px;">
            • {net_msg}
        </p>

        <p style="margin-bottom:12px;">
            • {pay_msg}
        </p>

        <p style="margin-top:18px; font-weight:600;">
            Risk Insight:
        </p>

        <p>
            {risk_msg}
        </p>
        </div>
        """
)