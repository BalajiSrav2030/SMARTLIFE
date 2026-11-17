"""Dashboard: net worth, monthly summary, health score, upcoming dues, goals, learning."""
from datetime import date
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import auth
import budget_logic
import db
import finance
import theme
import ui
from i18n import t
from lessons import LESSONS
from sample_data import load_sample
from utils import inr

user = auth.current_user()
uid = user["id"]
P = theme.P()
ui.header(f"{t('hello')}, {user['name'].split()[0]} 👋", t("tagline"))

txns = db.get_transactions(uid)
hold = db.get_holdings(uid)
if not txns and not hold:
    st.info(t("no_data"))
    if st.button(t("load_sample"), type="primary"):
        load_sample(uid)
        st.rerun()
    st.stop()

df = pd.DataFrame(txns, columns=["id", "txn_type", "category", "amount", "txn_date", "note"])
df["txn_date"] = pd.to_datetime(df["txn_date"])
df["ym"] = df["txn_date"].dt.to_period("M")
this_m = df["ym"].max() if not df.empty else pd.Period(date.today(), "M")
cur = df[df["ym"] == this_m]
inc = cur.loc[cur.txn_type == "income", "amount"].sum()
exp = cur.loc[cur.txn_type == "expense", "amount"].sum()
sr = (inc - exp) / inc * 100 if inc else 0
val = lambda k: sum(h["current_value"] for h in hold if h["kind"] == k)
assets_total = val("investment") + val("asset")
net = assets_total - val("loan")
avg_exp = df[df.txn_type == "expense"].groupby("ym")["amount"].sum().mean() if not df.empty else 0
liquid = sum(h["current_value"] for h in hold if h["category"] in ("Cash / Bank", "FD / RD"))
em = liquid / avg_exp if avg_exp else 0
score = finance.health_score(sr, em, val("loan"), assets_total)
tag = "Strong" if score >= 80 else "Good" if score >= 60 else "Needs work"

ui.kpis([
    {"l": t("net_worth"), "v": inr(net), "s": f"{t('assets')} {inr(assets_total)} · {t('loans')} {inr(val('loan'))}", "hero": True},
    {"l": t("monthly_income"), "v": inr(inc), "cls": "good"},
    {"l": t("monthly_expenses"), "v": inr(exp), "cls": "bad"},
    {"l": t("savings_rate"), "v": f"{sr:.0f}%", "s": "Target 20%+", "cls": "good" if sr >= 20 else "bad"},
    {"l": t("health_score"), "v": f"{score}/100", "s": f"{tag} · {t('emergency_months')}: {em:.1f}"},
])

al = budget_logic.alerts(uid)
if al:
    msgs = " · ".join(f"{'🔴' if a['level'] == 'over' else '⚠️'} {a['category']} {a['pct']:.0f}%" for a in al)
    (st.error if any(a["level"] == "over" for a in al) else st.warning)(
        f"**{t('budget_alerts')}:** {msgs} of this month's budget. See {t('budget_daily')}.")

c1, c2 = st.columns([1.35, 1])
with c1:
    monthly = (df.pivot_table(index="ym", columns="txn_type", values="amount", aggfunc="sum")
                 .reindex(columns=["income", "expense"]).fillna(0).tail(6)) if not df.empty else pd.DataFrame()
    fig = go.Figure([
        go.Bar(name=t("income"), x=[p.strftime("%b") for p in monthly.index], y=monthly.get("income", []),
               marker_color=P["chart"][0], marker_line_width=0),
        go.Bar(name=t("expense"), x=[p.strftime("%b") for p in monthly.index], y=monthly.get("expense", []),
               marker_color=P["chart"][3], marker_line_width=0),
    ])
    fig.update_layout(**theme.plotly_layout(barmode="group", height=300, bargap=0.35, yaxis_tickprefix="₹"))
    st.markdown(f"#### {t('income_vs_exp')}")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with c2:
    by_cat = cur[cur.txn_type == "expense"].groupby("category")["amount"].sum().sort_values(ascending=False)
    st.markdown(f"#### {t('exp_by_cat')}")
    if by_cat.empty:
        st.caption("—")
    else:
        fig = go.Figure(go.Pie(labels=by_cat.index, values=by_cat.values, hole=0.62, sort=False,
                               marker=dict(colors=P["chart"], line=dict(color=P["surface"], width=2)),
                               textinfo="percent", textfont_size=11))
        fig.update_layout(**theme.plotly_layout(height=300, showlegend=True,
                                                legend=dict(orientation="v", x=1, y=0.5, font=dict(color=P["muted"]))),
                          annotations=[dict(text=f"<b>{inr(exp)}</b>", showarrow=False, font=dict(size=15, color=P["ink"]))])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---- upcoming dues from holdings + insurance renewals ----
today = date.today()
dues = []
for h in hold:
    if h["due_date"]:
        dues.append((h["due_date"], h["name"], h["category"]))
for p in db.list_rows("policies", uid):
    if p["renewal"]:
        dues.append((p["renewal"], f"{p['ptype']} · {p['insurer']}", "Insurance renewal"))
dues = sorted((d, n, c, (date.fromisoformat(d) - today).days) for d, n, c in dues)
dues = [x for x in dues if 0 <= x[3] <= 30]

c3, c4 = st.columns(2)
with c3:
    body = ui.rows([(f"{escape(n)}<div class='m'>{escape(c)} · {d}</div>",
                     ui.pill("today" if k == 0 else f"in {k} day{'s' if k != 1 else ''}",
                             "red" if k <= 3 else "amber" if k <= 15 else "grey"))
                    for d, n, c, k in dues[:6]]) or f"<p class='m'>{t('nothing_due')}</p>"
    ui.card("🔔 " + t("upcoming"), body)
with c4:
    goals = db.list_rows("goals", uid)
    body = "".join(
        f"<div style='display:flex;justify-content:space-between;gap:8px;font-size:14px'><span>{escape(g['name'])}</span>"
        f"<span class='m'>{inr(g['saved'])} / {inr(g['target'])} · <b>{g['saved'] / g['target'] * 100:.0f}%</b></span></div>"
        + ui.bar(g["saved"] / g["target"] * 100, P["chart"][i % len(P["chart"])])
        for i, g in enumerate(goals[:5]) if g["target"]) or "<p class='m'>—</p>"
    ui.card("🎯 " + t("goals"), body)

prog = db.get_progress(uid)
done = len(prog)
ui.card("📚 " + t("learn"),
        f"<div style='display:flex;justify-content:space-between'><span>{done} / {len(LESSONS)} {t('lessons').lower()} · "
        f"{t('completed').lower()}</span><b>{done / len(LESSONS) * 100:.0f}%</b></div>" + ui.bar(done / len(LESSONS) * 100))
