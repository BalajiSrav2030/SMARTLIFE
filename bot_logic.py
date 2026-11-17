"""Pure functions that build the bot's replies (HTML text).
No Telegram code here, so it is easy to test and explain."""
import io
from collections import defaultdict
from datetime import date, datetime
from html import escape

import db
import finance
from utils import inr

KIND_LABEL = {"investment": "Investment", "asset": "Asset", "loan": "Loan"}


def _month(d: str) -> str:
    return d[:7]


def _num(s: str) -> float:
    """'1,50,000' / '1.5L' / '2cr' / '15k' -> float"""
    s = s.strip().lower().replace(",", "").replace("₹", "").replace("$", "")
    mult = 1
    for suf, m in (("cr", 1e7), ("l", 1e5), ("k", 1e3)):
        if s.endswith(suf):
            s, mult = s[: -len(suf)], m
            break
    return float(s) * mult


def parse_numbers(args, count, names):
    """Parse the first `count` args as numbers; raise ValueError with a friendly message."""
    if len(args) < count:
        raise ValueError(f"{count} values venum: {', '.join(names)}")
    out = []
    for a, n in zip(args[:count], names):
        try:
            out.append(_num(a))
        except ValueError:
            raise ValueError(f"'{escape(a)}' number illa ({n})")
    return out


# ---------------- dashboard ----------------
def summary(uid):
    txns = db.get_transactions(uid)
    holds = db.get_holdings(uid)
    months = sorted({_month(t["txn_date"]) for t in txns})
    cur = months[-1] if months else date.today().strftime("%Y-%m")
    inc = sum(t["amount"] for t in txns if _month(t["txn_date"]) == cur and t["txn_type"] == "income")
    exp = sum(t["amount"] for t in txns if _month(t["txn_date"]) == cur and t["txn_type"] == "expense")
    val = lambda k: sum(h["current_value"] for h in holds if h["kind"] == k)
    exp_by_m = defaultdict(float)
    for t in txns:
        if t["txn_type"] == "expense":
            exp_by_m[_month(t["txn_date"])] += t["amount"]
    avg_exp = (sum(exp_by_m.values()) / len(exp_by_m)) if exp_by_m else 0
    liquid = sum(h["current_value"] for h in holds if h["category"] in ("Cash / Bank", "FD / RD"))
    sr = (inc - exp) / inc * 100 if inc else 0
    em = liquid / avg_exp if avg_exp else 0
    assets_total = val("investment") + val("asset")
    return {
        "txns": txns, "holds": holds, "months": months, "cur": cur, "inc": inc, "exp": exp,
        "sr": sr, "em": em, "inv": val("investment"), "ast": val("asset"), "loan": val("loan"),
        "net": assets_total - val("loan"),
        "score": finance.health_score(sr, em, val("loan"), assets_total),
    }


def dashboard_text(uid, name):
    s = summary(uid)
    if not s["txns"] and not s["holds"]:
        return ("Innum data illa.\n\n➕ <b>Add</b> button use pannunga, illa /demo type panni "
                "sample data load pannunga.")
    mname = datetime.strptime(s["cur"] + "-01", "%Y-%m-%d").strftime("%B %Y")
    tag = "Strong 💪" if s["score"] >= 80 else "Good 👍" if s["score"] >= 60 else "Needs work ⚠️"
    lines = [
        f"<b>Vanakkam, {escape(name)} 👋</b>",
        f"<i>{mname}</i>\n",
        f"🏦 <b>Net worth:</b> {inr(s['net'])}",
        f"💰 Income: {inr(s['inc'])}",
        f"💸 Expenses: {inr(s['exp'])}",
        f"📈 Savings rate: <b>{s['sr']:.0f}%</b> (target 20%+)",
        f"❤️ Health score: <b>{s['score']}/100</b> · {tag}",
        f"🛟 Emergency fund: {s['em']:.1f} months",
    ]
    up = upcoming(uid, 30)
    if up:
        lines.append("\n🔔 <b>Upcoming payments</b>")
        lines += [f"• {d} · {escape(n)} ({days_label(k)})" for d, n, k in up[:4]]
    return "\n".join(lines)


def days_label(k):
    return "today" if k <= 0 else "tomorrow" if k == 1 else f"in {k} days"


def upcoming(uid, within_days):
    today = date.today()
    out = []
    for h in db.get_holdings(uid):
        if h["due_date"]:
            k = (date.fromisoformat(h["due_date"]) - today).days
            if 0 <= k <= within_days:
                out.append((h["due_date"], h["name"], k))
    return sorted(out)


def month_report_text(uid):
    s = summary(uid)
    cur_exp = defaultdict(float)
    for t in s["txns"]:
        if _month(t["txn_date"]) == s["cur"] and t["txn_type"] == "expense":
            cur_exp[t["category"]] += t["amount"]
    if not cur_exp:
        return "Indha month expenses illa."
    total = sum(cur_exp.values())
    lines = [f"<b>🧾 {s['cur']} expenses: {inr(total)}</b>\n"]
    for cat, amt in sorted(cur_exp.items(), key=lambda x: -x[1]):
        pct = amt / total * 100
        bar = "▇" * max(1, round(pct / 5))
        lines.append(f"<code>{bar:<20}</code> {escape(cat)}: {inr(amt)} ({pct:.0f}%)")
    return "\n".join(lines)


def chart_png(uid):
    """Income vs expenses (last 6 months) + this month's expense split, as PNG bytes."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = summary(uid)
    months = s["months"][-6:]
    inc = [sum(t["amount"] for t in s["txns"] if _month(t["txn_date"]) == m and t["txn_type"] == "income") for m in months]
    exp = [sum(t["amount"] for t in s["txns"] if _month(t["txn_date"]) == m and t["txn_type"] == "expense") for m in months]
    labels = [datetime.strptime(m + "-01", "%Y-%m-%d").strftime("%b") for m in months]
    cat = defaultdict(float)
    for t in s["txns"]:
        if _month(t["txn_date"]) == s["cur"] and t["txn_type"] == "expense":
            cat[t["category"]] += t["amount"]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1.4, 1]})
    x = range(len(months))
    a1.bar([i - 0.2 for i in x], inc, 0.4, label="Income", color="#0d7a57")
    a1.bar([i + 0.2 for i in x], exp, 0.4, label="Expenses", color="#c2372b")
    a1.set_xticks(list(x), labels)
    a1.yaxis.set_major_formatter(lambda v, _: f"₹{v / 1000:.0f}k")
    a1.set_title("Income vs Expenses", loc="left", fontweight="bold")
    a1.spines[["top", "right"]].set_visible(False)
    a1.grid(axis="y", alpha=0.3)
    a1.legend(frameon=False)
    if cat:
        items = sorted(cat.items(), key=lambda kv: -kv[1])
        a2.pie([v for _, v in items], labels=[k for k, _ in items], autopct="%1.0f%%",
               pctdistance=0.78, wedgeprops={"width": 0.42}, textprops={"fontsize": 8})
    a2.set_title("This month's expenses", loc="left", fontweight="bold")
    fig.suptitle("SmartLife", x=0.01, ha="left", fontsize=10, color="#5b6f66")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf


# ---------------- holdings ----------------
def holdings_text(uid):
    s = summary(uid)
    if not s["holds"]:
        return "Investments / assets innum add pannala. ➕ <b>Add</b> button use pannunga."
    inv_in = sum(h["invested"] for h in s["holds"] if h["kind"] == "investment")
    ret = (s["inv"] - inv_in) / inv_in * 100 if inv_in else 0
    lines = [
        f"<b>🏦 Net worth: {inr(s['net'])}</b>",
        f"📊 Investments: {inr(s['inv'])} ({ret:+.1f}%)",
        f"🏡 Assets: {inr(s['ast'])}",
        f"💳 Loans: {inr(s['loan'])}",
    ]
    for k, icon in (("investment", "📊"), ("asset", "🏡"), ("loan", "💳")):
        rows = [h for h in s["holds"] if h["kind"] == k]
        if rows:
            lines.append(f"\n{icon} <b>{KIND_LABEL[k]}s</b>")
            for h in rows:
                extra = ""
                if k != "loan" and h["invested"]:
                    extra = f" ({(h['current_value'] - h['invested']) / h['invested'] * 100:+.0f}%)"
                due = f" · due {h['due_date']}" if h["due_date"] else ""
                lines.append(f"• {escape(h['name'])}: {inr(h['current_value'])}{extra}{due}")
    return "\n".join(lines)


def recent_text(txns):
    if not txns:
        return "Transactions illa."
    lines = ["<b>🧾 Recent transactions</b>"]
    for i, t in enumerate(txns, 1):
        sign = "+" if t["txn_type"] == "income" else "−"
        note = f" · {escape(t['note'])}" if t["note"] else ""
        lines.append(f"{i}. {t['txn_date']} · {escape(t['category'])} · <b>{sign}{inr(t['amount'])}</b>{note}")
    return "\n".join(lines)


# ---------------- calculators ----------------
CALC_HELP = """<b>🧮 Calculators</b>  (1.5L, 20k, 2cr maadhiri type pannalaam)

<b>SIP</b>: /sip monthly rate% years [step-up%]
<code>/sip 10000 12 10</code>
<code>/sip 10000 12 10 10</code>

<b>Lumpsum</b>: /lumpsum amount rate% years
<code>/lumpsum 1L 12 10</code>

<b>EMI</b>: /emi loan rate% years
<code>/emi 30L 8.5 20</code>

<b>Goal</b>: /goal cost-today years [inflation%] [return%]
<code>/goal 20L 5 6 12</code>

<i>Estimates mattum. Returns guaranteed illa.</i>"""


def sip_text(args):
    m, r, y = parse_numbers(args, 3, ["monthly", "rate", "years"])
    step = _num(args[3]) if len(args) > 3 else 0
    if not (0 < y <= 50):
        raise ValueError("Years 1–50 kulla irukkanum")
    inv, val, rows = finance.sip_future_value(m, r, y, step)
    lines = [f"<b>📈 SIP {inr(m)}/month · {r:g}% · {y:g} yrs" + (f" · step-up {step:g}%" if step else "") + "</b>\n",
             f"Invested: {inr(inv)}", f"Returns: {inr(val - inv)}", f"<b>Future value: {inr(val)}</b>\n"]
    pick = rows if len(rows) <= 6 else [rows[i] for i in sorted({0, len(rows) // 4, len(rows) // 2, 3 * len(rows) // 4, len(rows) - 1})]
    lines += [f"<code>Year {r_['Year']:>2}</code>  {inr(r_['Value'])}" for r_ in pick]
    return "\n".join(lines)


def lumpsum_text(args):
    p, r, y = parse_numbers(args, 3, ["amount", "rate", "years"])
    fv = finance.lumpsum_future_value(p, r, y)
    return (f"<b>💰 Lumpsum {inr(p)} · {r:g}% · {y:g} yrs</b>\n\n"
            f"<b>Future value: {inr(fv)}</b>\nGrowth: {fv / p:.2f}x")


def emi_text(args):
    p, r, y = parse_numbers(args, 3, ["loan", "rate", "years"])
    if not (0 < y <= 40):
        raise ValueError("Tenure 1–40 years kulla irukkanum")
    e = finance.emi(p, r, y)
    total = e * y * 12
    return (f"<b>🏠 Loan {inr(p)} · {r:g}% · {y:g} yrs</b>\n\n"
            f"<b>EMI: {inr(e)}/month</b>\nTotal interest: {inr(total - p)}\nTotal payment: {inr(total)}\n"
            f"Interest share: {(total - p) / total * 100:.0f}%")


def goal_text(args):
    cost, y = parse_numbers(args, 2, ["cost", "years"])
    infl = _num(args[2]) if len(args) > 2 else 6
    r = _num(args[3]) if len(args) > 3 else 12
    if not (0 < y <= 50):
        raise ValueError("Years 1–50 kulla irukkanum")
    fc, sip = finance.goal_monthly_sip(cost, y, infl, r)
    return (f"<b>🎯 Goal: {inr(cost)} (today) in {y:g} yrs</b>\n"
            f"Inflation {infl:g}% · Return {r:g}%\n\n"
            f"Future cost: {inr(fc)}\n<b>Monthly SIP venum: {inr(sip)}</b>")


# ---------------- futures ----------------
FUT_HELP = """<b>⚡ Futures Risk Calculator</b>
<i>Educational tool, financial advice illa.</i>

<b>Crypto</b>: /crypto long|short capital$ risk% entry stop target leverage [mmr%]
<code>/crypto long 1000 2 70000 68600 74200 10</code>
<code>/crypto short 1000 2 70000 71400 65800 5</code>

<b>Indian F&amp;O</b>: /fno long|short capital₹ risk% entry stop target lot-size margin-per-lot
<code>/fno long 5L 2 24000 23900 24300 75 150000</code>
<i>(Lot size and margin per lot adikadi maarum. NSE / broker la current value paathu podunga. Mela irukuradhu example numbers.)</i>"""


def _side(args):
    if not args or args[0].lower() not in ("long", "short"):
        raise ValueError("First word <b>long</b> or <b>short</b> irukkanum")
    return args[0].lower(), args[1:]


def _check_levels(side, e, sl, tp):
    ok = (sl < e < tp) if side == "long" else (tp < e < sl)
    if not ok:
        raise ValueError("LONG: stop &lt; entry &lt; target · SHORT: target &lt; entry &lt; stop")


def crypto_text(args):
    side, rest = _side(args)
    cap, rp, e, sl, tp, lev = parse_numbers(rest, 6, ["capital", "risk%", "entry", "stop", "target", "leverage"])
    mmr = _num(rest[6]) if len(rest) > 6 else 0.5
    if lev < 1:
        raise ValueError("Leverage 1x or adhigam irukkanum")
    _check_levels(side, e, sl, tp)
    r = finance.crypto_futures(cap, rp, e, sl, tp, lev, side, mmr)
    ck = lambda ok, t: f"{'✅' if ok else '❌'} {t}"
    return "\n".join([
        f"<b>⚡ Crypto {side.upper()} · {lev:g}x</b>\n",
        f"Position size: <b>${r['notional']:,.0f}</b> ({r['qty']:.4f} coins)",
        f"Margin needed: <b>${r['margin']:,.2f}</b> ({r['margin'] / cap * 100:.0f}% of capital)",
        f"Max loss (SL hit): <b>−${r['risk_amt']:,.2f}</b>",
        f"Profit (target hit): <b>+${r['reward']:,.2f}</b>",
        f"Risk : Reward = 1 : {r['rr']:.1f}",
        f"Liquidation ≈ <b>${r['liq']:,.2f}</b>\n",
        "<b>Risk check</b>",
        ck(rp <= 2, "Risk per trade ≤ 2%"),
        ck(r["rr"] >= 2, "Risk : Reward ≥ 1 : 2"),
        ck(r["sl_safe"], "Stop-loss liquidation ku munnaadi hit aagum"),
        ck(r["margin_ok"], "Margin capital kulla irukku"),
        ck(lev <= 10, f"Leverage {lev:g}x ≤ 10x"),
        "\n<i>Liquidation approx (isolated). Fees &amp; funding include pannala.</i>",
    ])


def fno_text(args):
    side, rest = _side(args)
    cap, rp, e, sl, tp, lot, mpl = parse_numbers(
        rest, 7, ["capital", "risk%", "entry", "stop", "target", "lot size", "margin per lot"])
    _check_levels(side, e, sl, tp)
    r = finance.fno_futures(cap, rp, e, sl, tp, int(lot), mpl)
    ck = lambda ok, t: f"{'✅' if ok else '❌'} {t}"
    lines = [
        f"<b>🇮🇳 F&amp;O Futures {side.upper()}</b>\n",
        f"<b>Lots edukkalaam: {r['lots']}</b>",
        f"Margin needed: {inr(r['margin'])}",
        f"Max loss (SL hit): −{inr(r['max_loss'])}",
        f"Profit (target hit): +{inr(r['profit'])}",
        f"Risk : Reward = 1 : {r['rr']:.1f}\n",
        f"Risk budget: {inr(r['risk_amt'])} · loss per lot: {inr(r['loss_per_lot'])}",
        f"Lots by risk: {r['lots_by_risk']} · lots by capital: {r['lots_by_margin']}\n",
        "<b>Risk check</b>",
        ck(rp <= 2, "Risk per trade ≤ 2%"),
        ck(r["rr"] >= 2, "Risk : Reward ≥ 1 : 2"),
        ck(r["margin"] <= cap * 0.5, "Margin usage ≤ 50% of capital"),
    ]
    if r["lots"] == 0:
        lines.append("\n❌ Indha risk budget la oru lot kooda edukka mudiyaadhu. SL tight pannunga, illa trade skip pannunga.")
    return "\n".join(lines)


HELP = """<b>SmartLife Bot 💚</b>
Unga full financial life, Telegram la.

<b>Quick add</b>
<code>/expense 450 Food lunch</code>
<code>/income 85000 Salary</code>

<b>Buttons</b>
📊 Dashboard · ➕ Add · 🧾 Recent · 💼 Holdings
📈 Chart · 🧮 Calculators · ⚡ Futures · 🔔 Reminders

<b>Other commands</b>
/report: indha month expense breakdown
/demo: sample data load (pazhaya data delete aagum)
/cancel: add flow ah stop panna

Daily 9 AM ku EMI / SIP / renewal reminders automatic ah varum.
<i>Real bank / card / account numbers inga podaadheenga.</i>"""
