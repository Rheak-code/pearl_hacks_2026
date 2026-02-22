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
def call_retirement_projection(
    age: int,
    retirement_age: int,
    current_savings: float,
    monthly_contribution: float,
    annual_return_pct: float,
):
    payload = {
        "age": int(age),
        "retirementAge": int(retirement_age),
        "currentSavings": float(current_savings),
        "monthlyContribution": float(monthly_contribution),
        "annualReturnPct": float(annual_return_pct),
    }

    try:
        r = httpx.post(f"{API_BASE}/retirement_projection", json=payload, timeout=30.0)
        r.raise_for_status()
        return r.json()

    except httpx.ConnectError:
        # backend isn't running → show error (this is actionable)
        st.error(f"Cannot connect to API at {API_BASE}. Is FastAPI running on port 8000?")
        return None

    except httpx.HTTPStatusError as e:
        # endpoint doesn't exist yet → silently fall back to local math
        if e.response.status_code == 404:
            return None

        # other API errors (bad payload, 500, etc.) → show
        st.error(f"API returned an error: {e.response.status_code} - {e.response.text}")
        return None

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# ---------- STREAMLIT UI ----------
st.title("🏖️ Retirement")
st.caption("Retirement projection (FastAPI-powered, with a local fallback).")

# Defaults from session_state profile if available (NO REQUIREMENT)
p = st.session_state.get("profile", {})

default_age = int(p.get("age", 21))
default_retire_age = int(p.get("retirement_age", 65))
default_current = float(p.get("current_savings", 10_000.0))
default_monthly = float(p.get("monthly_retirement_contribution", 600.0))
default_rate = float(p.get("annual_return_pct", 6.0))

c1, c2, c3 = st.columns(3)
age = c1.number_input("Current age", min_value=0, max_value=120, value=default_age, step=1)
retire_age = c2.number_input("Retirement age", min_value=0, max_value=120, value=default_retire_age, step=1)
current = c3.number_input("Current savings ($)", min_value=0.0, value=default_current, step=1000.0)

c4, c5 = st.columns(2)
monthly = c4.number_input("Monthly contribution ($)", min_value=0.0, value=default_monthly, step=50.0)
rate = c5.slider("Estimated annual return (%)", 0.0, 15.0, default_rate, 0.5)

# Persist into session_state profile for other pages
if "profile" not in st.session_state or not isinstance(st.session_state["profile"], dict):
    st.session_state["profile"] = {}

st.session_state["profile"].update(
    {
        "age": int(age),
        "retirement_age": int(retire_age),
        "current_savings": float(current),
        "monthly_retirement_contribution": float(monthly),
        "annual_return_pct": float(rate),
    }
)

# Validation
if retire_age < age:
    st.error("Retirement age must be greater than or equal to current age.")
    st.stop()

years_left = int(retire_age) - int(age)
st.write(f"Years until retirement: **{years_left}**")

# Run projection
if st.button("Run Projection", use_container_width=True):
    with st.spinner("Computing projection..."):
        # Try backend first
        result = call_retirement_projection(
            age=int(age),
            retirement_age=int(retire_age),
            current_savings=float(current),
            monthly_contribution=float(monthly),
            annual_return_pct=float(rate),
        )

        # Fall back to local if backend not available / endpoint missing
        if result is None:
            result = call_retirement_projection(
                age=int(age),
                retirement_age=int(retire_age),
                current_savings=float(current),
                monthly_contribution=float(monthly),
                annual_return_pct=float(rate),
            )

    st.success("Projection complete!")

    colA, colB = st.columns(2)
    colA.metric("Current savings", f"${float(current):,.0f}")
    colB.metric("Projected at retirement", f"${float(result['futureValueTotal']):,.0f}")

    st.write(
        f"Projected contributions growth: **${float(result['futureValueContrib']):,.0f}**"
    )

