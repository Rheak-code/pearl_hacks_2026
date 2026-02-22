from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# ---------- CONFIGURATION ----------
FRED_API_KEY = "fea9fca02094f2ecc01efe7234532b08"  # <-- replace with your key

# ---------- DATA MODELS ----------
class AssetData(BaseModel):
    cash: float
    bonds: float
    equities: float

class LiabilityData(BaseModel):
    fixed_mortgage: float
    variable_debt: float
    remaining_years: int
    mortgage_rate: float
    variable_rate: float

class SimulationInput(BaseModel):
    assets: AssetData
    liabilities: LiabilityData
    rateShockBps: float

# ---------- ASYNC FRED FETCH ----------
async def fetch_fred_rate(series_id: str):
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
            print("FRED API failed:", response.text)
            raise HTTPException(status_code=502, detail=f"FRED API Error for {series_id}")

        data = response.json()
        print(f"Data for {series_id}:", data)  # debug output

        for obs in data.get("observations", []):
            val = obs.get("value")
            if val and val != ".":  # skip invalid/no-data points
                return {"rate": float(val)/100, "date": obs.get("date")}

    raise ValueError(f"No valid data found for {series_id}")

# ---------- CALCULATIONS ----------
def bond_price_change(duration, convexity, rate_change):
    # Taylor series approximation
    return -duration * rate_change + 0.5 * convexity * (rate_change ** 2)

def mortgage_payment(principal, annual_rate, years):
    if principal <= 0: return 0
    r = annual_rate / 12
    n = years * 12
    if r == 0: return principal / n
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

# ---------- ENDPOINT ----------
@app.post("/simulate_rate_shock")
async def simulate(data: SimulationInput):
    # 1. Fetch Real-Time Market Data
    try:
        ten_year = await fetch_fred_rate("DGS10")
        mortgage = await fetch_fred_rate("MORTGAGE30US")
        fed_funds = await fetch_fred_rate("FEDFUNDS")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Debug print
    print("10Y Treasury Rate:", ten_year)
    print("30Y Mortgage Rate:", mortgage)
    print("Fed Funds Rate:", fed_funds)

    # 2. Setup Shocks
    shock = data.rateShockBps / 10000
    market_bond_rate = ten_year["rate"]
    market_mtg_rate = mortgage["rate"]

    # 3. Asset Impact
    bond_impact = bond_price_change(6, 30, shock)
    equity_impact = -5 * shock
    asset_delta = (data.assets.bonds * bond_impact) + (data.assets.equities * equity_impact)
    total_assets = data.assets.cash + data.assets.bonds + data.assets.equities

    # 4. Liability Impact (Variable Debt Re-pricing)
    old_payment = mortgage_payment(data.liabilities.variable_debt, data.liabilities.variable_rate, data.liabilities.remaining_years)
    new_payment = mortgage_payment(data.liabilities.variable_debt, data.liabilities.variable_rate + shock, data.liabilities.remaining_years)
    payment_increase = new_payment - old_payment

    # 5. Risk Scoring (Duration Gap)
    a_dur = ((data.assets.bonds * 6) + (data.assets.equities * 5)) / total_assets if total_assets > 0 else 0
    l_dur = 8  # Assumption for long-term mortgage liabilities
    total_liab = data.liabilities.fixed_mortgage + data.liabilities.variable_debt
    dur_gap = a_dur - (l_dur * (total_liab / total_assets))

    return {
        "netWorthDelta": round(asset_delta - (payment_increase * 12), 2),
        "newMonthlyPaymentIncrease": round(payment_increase, 2),
        "durationGap": round(dur_gap, 2),
        "riskClassification": "High" if abs(dur_gap) > 3 else "Moderate" if abs(dur_gap) > 1 else "Low"
    }