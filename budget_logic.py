"""Budget status and spending averages (no UI code)."""
import calendar
from datetime import date

import db


def this_month():
    return date.today().strftime("%Y-%m")


def month_spend(user_id, ym=None):
    """{category: amount spent} for one month (default: current)."""
    ym = ym or this_month()
    out = {}
    for t in db.get_transactions(user_id):
        if t["txn_type"] == "expense" and t["txn_date"][:7] == ym:
            out[t["category"]] = out.get(t["category"], 0) + t["amount"]
    return out


def status(user_id):
    """One row per budget: category, spent, limit, pct used, projected month-end spend, level."""
    today = date.today()
    days_in = calendar.monthrange(today.year, today.month)[1]
    spent = month_spend(user_id)
    rows = []
    for cat, limit in sorted(db.get_budgets(user_id).items()):
        s = spent.get(cat, 0)
        pct = s / limit * 100
        projected = s / today.day * days_in
        level = "over" if pct >= 100 else "near" if pct >= 80 else "ok"
        rows.append({"category": cat, "spent": s, "limit": limit, "pct": pct, "projected": projected,
                     "level": level, "left": limit - s})
    return rows


def alerts(user_id):
    return [r for r in status(user_id) if r["level"] != "ok"]


def check_category(user_id, category):
    """After adding an expense: returns (level, row) for that category, or (None, None) if no budget."""
    for r in status(user_id):
        if r["category"] == category:
            return r["level"], r
    return None, None


def daily_allowance(user_id):
    """How much can still be spent per day for the rest of this month within all budgets."""
    today = date.today()
    days_in = calendar.monthrange(today.year, today.month)[1]
    rows = status(user_id)
    if not rows:
        return None
    total_limit = sum(r["limit"] for r in rows)
    spent_before_today = sum(r["spent"] for r in rows) - sum(
        t["amount"] for t in db.get_transactions(user_id)
        if t["txn_type"] == "expense" and t["txn_date"] == str(today) and t["category"] in {r["category"] for r in rows})
    days_left = days_in - today.day + 1
    return max(0.0, (total_limit - spent_before_today) / days_left)
