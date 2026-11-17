"""Pure calculation functions (no UI) – easy to test and explain in viva."""
import math


# ---------- SIP / Lumpsum / EMI / Goal ----------
def sip_future_value(monthly, annual_rate, years, step_up_pct=0.0):
    """Month-by-month simulation. Investment made at start of each month.
    Returns (total_invested, future_value, yearly_rows)."""
    i = annual_rate / 12 / 100
    value = invested = 0.0
    amount = monthly
    rows = []
    for m in range(1, int(years * 12) + 1):
        value = (value + amount) * (1 + i)
        invested += amount
        if m % 12 == 0:
            rows.append({"Year": m // 12, "Invested": invested, "Value": value})
            amount *= 1 + step_up_pct / 100
    return invested, value, rows


def lumpsum_future_value(principal, annual_rate, years):
    return principal * (1 + annual_rate / 100) ** years


def emi(principal, annual_rate, years):
    """EMI = P·i·(1+i)^n / ((1+i)^n − 1)"""
    n = int(years * 12)
    i = annual_rate / 12 / 100
    if i == 0:
        return principal / n
    f = (1 + i) ** n
    return principal * i * f / (f - 1)


def goal_monthly_sip(cost_today, years, inflation_pct, annual_rate):
    """Returns (future_cost, monthly_sip_needed)."""
    future_cost = cost_today * (1 + inflation_pct / 100) ** years
    n = int(years * 12)
    i = annual_rate / 12 / 100
    factor = n if i == 0 else ((1 + i) ** n - 1) / i * (1 + i)
    return future_cost, future_cost / factor


def health_score(savings_rate, emergency_months, loans, assets_total):
    """0–100: savings rate (40) + emergency fund ≥ 6 months (30) + loans ≤ 50% of assets (30)."""
    score = (min(max(savings_rate, 0), 30) / 30 * 40
             + min(emergency_months, 6) / 6 * 30
             + (30 if loans <= assets_total * 0.5 else 10))
    return round(score)


# ---------- Futures risk ----------
def crypto_futures(capital, risk_pct, entry, stop, target, leverage, side="long", mmr_pct=0.5):
    """Position sizing by risk + approx isolated-margin liquidation price.
    Fees and funding are ignored. Returns a dict."""
    risk_amt = capital * risk_pct / 100
    sl_dist = abs(entry - stop) / entry
    notional = risk_amt / sl_dist
    qty = notional / entry
    margin = notional / leverage
    mmr = mmr_pct / 100
    if side == "long":
        liq = entry * (1 - 1 / leverage + mmr)
        sl_safe = stop > liq
    else:
        liq = entry * (1 + 1 / leverage - mmr)
        sl_safe = stop < liq
    reward = abs(target - entry) * qty
    return {
        "risk_amt": risk_amt, "notional": notional, "qty": qty, "margin": margin,
        "liq": liq, "sl_safe": sl_safe, "reward": reward,
        "rr": abs(target - entry) / abs(entry - stop),
        "margin_ok": margin <= capital,
    }


def fno_futures(capital, risk_pct, entry, stop, target, lot_size, margin_per_lot):
    """Indian F&O futures: how many lots fit the risk budget and the capital."""
    risk_amt = capital * risk_pct / 100
    loss_per_lot = abs(entry - stop) * lot_size
    lots_by_risk = math.floor(risk_amt / loss_per_lot)
    lots_by_margin = math.floor(capital / margin_per_lot)
    lots = max(0, min(lots_by_risk, lots_by_margin))
    return {
        "risk_amt": risk_amt, "loss_per_lot": loss_per_lot,
        "lots_by_risk": lots_by_risk, "lots_by_margin": lots_by_margin, "lots": lots,
        "margin": lots * margin_per_lot, "max_loss": lots * loss_per_lot,
        "profit": lots * abs(target - entry) * lot_size,
        "rr": abs(target - entry) / abs(entry - stop),
    }
