from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

app = FastAPI()

# --- FRED API Key ---
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_API_KEY")  # Replace or set environment variable

# ---------- DATA MODELS ----------
class AssetData(BaseModel):
    cash: float
    bonds: float
    equities: float

class LiabilityData(BaseModel):
    fixed_mortgage: float
    variable_debt: float
    remaining_years: int
    mortgage_rate: Optional[float] = None
    variable_rate: Optional[float] = None

class SimulationInput(BaseModel):
    assets: AssetData
    liabilities: LiabilityData
    rateShockBps: float  # basis points

# ---------- UTILITY FUNCTIONS ----------
async def fetch_fred_rate(series_id: str):
    """Fetch most recent numeric observation for a FRED series"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 5
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"FRED API Error for {series_id}")
        
        data = response.json()
        for obs in data.get("observations", []):
            val = obs.get("value")
            if val and val != ".":  # Skip holidays / missing data
                return {"rate": float(val) / 100, "date": obs.get("date")}
    raise ValueError(f"No valid data found for {series_id}")

def bond_price_change(duration, convexity, rate_change):
    return -duration * rate_change + 0.5 * convexity * (rate_change ** 2)

def mortgage_payment(principal, annual_rate, years):
    if principal <= 0:
        return 0
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

# ---------- ENDPOINT ----------
@app.post("/simulate_rate_shock")
async def simulate(data: SimulationInput):
    # --- Debug prints to confirm optional rates ---
    print("Mortgage Rate Provided:", data.liabilities.mortgage_rate)
    print("Variable Rate Provided:", data.liabilities.variable_rate)
    
    # 1️⃣ Fetch real-time rates if not provided
    try:
        ten_year = await fetch_fred_rate("DGS10")
        mortgage = await fetch_fred_rate("MORTGAGE30US")
        fed_funds = await fetch_fred_rate("FEDFUNDS")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Use FRED rates if the user did not provide them
    market_bond_rate = ten_year["rate"]
    market_mtg_rate = data.liabilities.variable_rate or mortgage["rate"]

    # 2️⃣ Apply user-specified rate shock
    shock = data.rateShockBps / 10000  # convert bps to decimal

    # 3️⃣ Asset impact
    bond_impact = bond_price_change(6, 30, shock)
    equity_impact = -5 * shock
    asset_delta = (data.assets.bonds * bond_impact) + (data.assets.equities * equity_impact)
    total_assets = data.assets.cash + data.assets.bonds + data.assets.equities

    # 4️⃣ Liability impact (variable debt repricing)
    old_payment = mortgage_payment(data.liabilities.variable_debt, market_mtg_rate, data.liabilities.remaining_years)
    new_payment = mortgage_payment(data.liabilities.variable_debt, market_mtg_rate + shock, data.liabilities.remaining_years)
    payment_increase = new_payment - old_payment
    total_liabilities = data.liabilities.fixed_mortgage + data.liabilities.variable_debt

    # 5️⃣ Duration gap / risk
    a_dur = ((data.assets.bonds * 6) + (data.assets.equities * 5)) / total_assets if total_assets > 0 else 0
    l_dur = 8
    dur_gap = a_dur - (l_dur * (total_liabilities / total_assets))

    if abs(dur_gap) < 1:
        risk_level = "Low"
    elif abs(dur_gap) < 3:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    # 6️⃣ Return results
    return {
        "status": "success",
        "market_data_as_of": ten_year["date"],
        "metrics": {
            "netWorthDelta": round(asset_delta - (payment_increase * 12), 2),
            "monthlyPaymentIncrease": round(payment_increase, 2),
            "durationGap": round(dur_gap, 2),
            "riskLevel": risk_level
        },
        "rates_used": {
            "base_10y_treasury": f"{market_bond_rate:.2%}",
            "base_30y_mortgage": f"{market_mtg_rate:.2%}",
            "fed_funds_rate": f"{fed_funds['rate']:.2%}"
        }
    }
