from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import json

with open("yield_params.json") as f:
    yield_data = json.load(f)

app = FastAPI()

# ---------- DATA MODELS ----------

class AssetData(BaseModel):
    cash: float
    bonds: float
    equities: float

class LiabilityData(BaseModel):
    fixed_mortgage: float
    variable_debt: float
    mortgage_rate: float
    variable_rate: float
    remaining_years: int

class SimulationInput(BaseModel):
    assets: AssetData
    liabilities: LiabilityData
    rateShockBps: float  # basis points

# ---------- FINANCIAL ENGINE ----------

def bond_price_change(duration, convexity, rate_change):
    return -duration * rate_change + 0.5 * convexity * (rate_change ** 2)

def mortgage_payment(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

@app.post("/simulate_rate_shock")
def simulate(data: SimulationInput):

    rate_change = data.rateShockBps / 10000  # convert bps to decimal

    # ---- ASSET DURATIONS ----
    bond_duration = 6
    bond_convexity = 30
    equity_beta = 5

    bond_pct_change = bond_price_change(bond_duration, bond_convexity, rate_change)
    equity_pct_change = -equity_beta * rate_change

    bond_delta = data.assets.bonds * bond_pct_change
    equity_delta = data.assets.equities * equity_pct_change

    total_assets = data.assets.cash + data.assets.bonds + data.assets.equities
    asset_delta = bond_delta + equity_delta

    # ---- LIABILITY SHOCK ----
    new_variable_rate = data.liabilities.variable_rate + rate_change
    new_variable_payment = mortgage_payment(
        data.liabilities.variable_debt,
        new_variable_rate,
        data.liabilities.remaining_years
    )

    old_variable_payment = mortgage_payment(
        data.liabilities.variable_debt,
        data.liabilities.variable_rate,
        data.liabilities.remaining_years
    )

    payment_delta = new_variable_payment - old_variable_payment

    # ---- DURATION GAP ----
    asset_duration = (
        (data.assets.bonds * bond_duration +
         data.assets.equities * equity_beta) / total_assets
        if total_assets > 0 else 0
    )

    total_liabilities = (
        data.liabilities.fixed_mortgage +
        data.liabilities.variable_debt
    )

    liability_duration = 8  # average mortgage duration

    duration_gap = asset_duration - (
        (total_liabilities / total_assets) * liability_duration
        if total_assets > 0 else 0
    )

    # ---- NET WORTH IMPACT ----
    net_worth_delta = asset_delta - (payment_delta * 12)

    # ---- RISK CLASSIFICATION ----
    if abs(duration_gap) < 1:
        risk = "Low"
    elif abs(duration_gap) < 3:
        risk = "Moderate"
    else:
        risk = "High"

    return {
        "netWorthDelta": round(net_worth_delta, 2),
        "newMonthlyPaymentIncrease": round(payment_delta, 2),
        "durationGap": round(duration_gap, 2),
        "riskClassification": risk
    }