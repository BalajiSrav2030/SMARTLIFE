"""Budget & Daily: quick daily expenses, monthly budget alerts, and spending / savings averages."""
import calendar
from datetime import date
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import auth
import budget_logic as B
import db
import theme
import ui
from i18n import t
from utils import inr

user = auth.current_user()
uid = user["id"]
P = theme.P()
today = date.today()
days_in = calendar.monthrange(today.year, today.month)[1]
ui.header(t("budget_daily"), "Add today's spending in seconds, stay inside your budgets, and see how your saving compares.")

LEVEL_PILL = {"ok": ("On track", "green"), "near": ("Near limit", "amber"), "over": ("Over budget", "red")}

# flash message from the previous run (after a save)
flash = st.session_state.pop("budget_flash", None)
if flash:
    (st.error if flash[0] == "over" else st.warning if flash[0] == "near" else st.success)(flash[1])

tab_today, tab_budget, tab_avg = st.tabs(["📅 " + t("today"), "🎯 " + t("budgets"), "📊 " + t("averages")])

txns = db.get_transactions(uid)
today_rows = [x for x in txns if x["txn_type"] == "expense" and x["txn_date"] == str(today)]
spent_today = sum(x["amount"] for x in today_rows)
budgeted = set(db.get_budgets(uid))
spent_today_b = sum(x["amount"] for x in today_rows if x["category"] in budgeted)
month_rows = [x for x in txns if x["txn_type"] == "expense" and x["txn_date"][:7] == B.this_month()]
spent_month = sum(x["amount"] for x in month_rows)
allow = B.daily_allowance(uid)

# =============== TODAY ===============
with tab_today:
    ui.kpis([
        {"l": t("spent_today"), "v": inr(spent_today), "hero": True,
         "s": f"{len(today_rows)} entr{'y' if len(today_rows) == 1 else 'ies'}"},
        {"l": t("daily_allowance"), "v": inr(allow) if allow is not None else "—",
         "s": "Within your budgets, for each day left" if allow is not None else "Set budgets to see this",
         "cls": "bad" if allow is not None and spent_today_b > allow else "good"},
        {"l": "Spent this month", "v": inr(spent_month), "s": f"Day {today.day} of {days_in}"},
    ])
    if allow is not None and spent_today_b > allow:
        st.warning(f"Today's spending in budgeted categories is {inr(spent_today_b - allow)} above your daily allowance.")

    with st.form("quick_exp", clear_on_submit=True):
        c1, c2, c3 = st.columns([1.3, 1, 1.6])
        cat = c1.selectbox(t("category"), db.EXPENSE_CATEGORIES, index=db.EXPENSE_CATEGORIES.index("Food"))
        amt = c2.number_input(t("amount"), min_value=0.0, step=50.0, format="%.0f")
        note = c3.text_input(t("note"), max_chars=100, placeholder="e.g. lunch, auto, groceries")
        d = st.date_input(t("date"), value=today, max_value=today)
        if st.form_submit_button("➕ " + t("save"), type="primary"):
            if amt <= 0:
                st.error("Enter an amount above 0.")
            else:
                db.add_transaction(uid, "expense", cat, amt, d, note.strip())
                level, row = B.check_category(uid, cat)
                if level == "over":
                    msg = f"🔴 {cat}: {inr(row['spent'])} spent of {inr(row['limit'])} – over budget by {inr(-row['left'])}."
                elif level == "near":
                    msg = f"⚠️ {cat}: {row['pct']:.0f}% of the monthly budget used. {inr(row['left'])} left."
                else:
                    msg = f"✅ Saved {inr(amt)} · {cat}" + (f" · {inr(row['left'])} left in this budget" if row else "")
                st.session_state.budget_flash = (level or "ok", msg)
                st.rerun()

    st.markdown(f"#### {t('today')} · {today.strftime('%d %b %Y')}")
    if today_rows:
        ui.table([t("category"), t("note"), t("amount")],
                 [[escape(x["category"]), escape(x["note"] or ""), inr(x["amount"])] for x in today_rows], numeric=(2,))
        with st.expander("🗑️ " + t("delete")):
            opts = {f"{x['category']} · {inr(x['amount'])} · {x['note'] or ''}": x["id"] for x in today_rows}
            pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed")
            if st.button(t("delete"), key="del_today"):
                db.delete_transaction(uid, opts[pick])
                st.rerun()
    else:
        st.caption("No expenses added today yet.")

    # daily spend this month vs average daily budget
    per_day = {}
    for x in month_rows:
        per_day[int(x["txn_date"][8:10])] = per_day.get(int(x["txn_date"][8:10]), 0) + x["amount"]
    days = list(range(1, today.day + 1))
    fig = go.Figure(go.Bar(x=days, y=[per_day.get(dd, 0) for dd in days], name="Spent",
                           marker_color=[P["chart"][3] if allow and per_day.get(dd, 0) > sum(r["limit"] for r in B.status(uid)) / days_in
                                         else P["chart"][0] for dd in days]))
    budgets_total = sum(r["limit"] for r in B.status(uid))
    if budgets_total:
        fig.add_hline(y=budgets_total / days_in, line_dash="dash", line_color=P["muted"],
                      annotation_text=f"Average daily budget {inr(budgets_total / days_in)}",
                      annotation_font_color=P["muted"])
    fig.update_layout(**theme.plotly_layout(height=280, yaxis_tickprefix="₹", xaxis_title=f"Day of {today.strftime('%B')}",
                                            showlegend=False, bargap=0.25))
    st.markdown("#### Daily spending this month")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# =============== BUDGETS ===============
with tab_budget:
    rows = B.status(uid)
    if rows:
        tot_l = sum(r["limit"] for r in rows)
        tot_s = sum(r["spent"] for r in rows)
        alerts = [r for r in rows if r["level"] != "ok"]
        ui.kpis([{"l": "Total monthly budget", "v": inr(tot_l)},
                 {"l": "Spent so far", "v": inr(tot_s), "s": f"{tot_s / tot_l * 100:.0f}% used", "cls": "bad" if tot_s > tot_l else ""},
                 {"l": "Left this month", "v": inr(tot_l - tot_s), "cls": "good" if tot_l >= tot_s else "bad"},
                 {"l": t("budget_alerts"), "v": len(alerts), "cls": "bad" if alerts else "good"}])
        body = ""
        for i, r in enumerate(rows):
            label, color = LEVEL_PILL[r["level"]]
            bar_color = {"ok": P["good"], "near": P["warn"], "over": P["bad"]}[r["level"]]
            proj = (f"<span class='m'> · on pace for {inr(r['projected'])} by month end</span>"
                    if r["projected"] > r["limit"] and r["level"] == "ok" else "")
            body += (f"<div style='display:flex;justify-content:space-between;gap:8px;font-size:14.5px;margin-top:6px'>"
                     f"<span><b>{escape(r['category'])}</b>{proj}</span>"
                     f"<span>{inr(r['spent'])} / {inr(r['limit'])} &nbsp;{ui.pill(label, color)}</span></div>"
                     + ui.bar(r["pct"], bar_color))
        ui.card("🎯 " + t("budgets") + f" · {today.strftime('%B %Y')}", body)
    else:
        st.info("No budgets yet. Set a monthly limit for the categories you want to control.")

    c1, c2 = st.columns(2)
    with c1:
        with st.form("set_budget", clear_on_submit=True):
            st.markdown("**Set or change a budget**")
            cat = st.selectbox(t("category"), db.EXPENSE_CATEGORIES, key="b_cat")
            lim = st.number_input(t("monthly_limit"), min_value=0.0, step=500.0, format="%.0f")
            if st.form_submit_button(t("save"), type="primary"):
                if lim <= 0:
                    st.error("Enter a limit above 0.")
                else:
                    db.set_budget(uid, cat, lim)
                    st.rerun()
    with c2:
        if rows:
            with st.form("del_budget"):
                st.markdown("**Remove a budget**")
                cat = st.selectbox(t("category"), [r["category"] for r in rows], key="b_del")
                if st.form_submit_button(t("delete")):
                    db.delete_budget(uid, cat)
                    st.rerun()
    st.caption("Alerts: amber at 80% of a budget, red at 100%. They also show on the Dashboard and when you add an expense.")

# =============== AVERAGES ===============
with tab_avg:
    if not txns:
        st.info(t("no_data"))
    else:
        df = pd.DataFrame(txns)
        df["d"] = pd.to_datetime(df["txn_date"])
        df["ym"] = df["d"].dt.to_period("M")
        m = (df.pivot_table(index="ym", columns="txn_type", values="amount", aggfunc="sum")
               .reindex(columns=["income", "expense"]).fillna(0).tail(6))
        m["savings"] = m["income"] - m["expense"]
        m["rate"] = (m["savings"] / m["income"].where(m["income"] > 0) * 100).fillna(0)
        exp = df[df.txn_type == "expense"]
        last30 = exp[exp["d"] > pd.Timestamp(today) - pd.Timedelta(days=30)]["amount"].sum() / 30
        avg_rate = m["savings"].sum() / m["income"].sum() * 100 if m["income"].sum() else 0
        ui.kpis([
            {"l": t("avg_daily_spend") + " (this month)", "v": inr(spent_month / today.day)},
            {"l": t("avg_daily_spend") + " (last 30 days)", "v": inr(last30)},
            {"l": t("avg_monthly_savings"), "v": inr(m["savings"].mean()), "hero": True,
             "s": f"over the last {len(m)} months"},
            {"l": "Average savings rate", "v": f"{avg_rate:.0f}%", "cls": "good" if avg_rate >= 20 else "bad",
             "s": "Recommended: 20% or more (50/30/20 rule)"},
        ])
        if avg_rate >= 20:
            st.success(f"You save {avg_rate:.0f}% of your income on average, above the 20% guideline of the 50/30/20 rule.")
        else:
            st.warning(f"You save {avg_rate:.0f}% of your income on average. The 50/30/20 rule suggests at least 20%: "
                       f"about {inr(m['income'].mean() * 0.2 - m['savings'].mean())} more each month.")

        c1, c2 = st.columns([1.3, 1])
        with c1:
            labels = [p.strftime("%b %Y") for p in m.index]
            fig = go.Figure(go.Bar(x=labels, y=m["savings"], name=t("savings"),
                                   marker_color=[P["good"] if r >= 20 else P["warn"] for r in m["rate"]]))
            fig.add_trace(go.Scatter(x=labels, y=m["income"] * 0.2, mode="lines+markers", name="20% of income",
                                     line=dict(color=P["muted"], dash="dash")))
            fig.update_layout(**theme.plotly_layout(height=300, yaxis_tickprefix="₹", bargap=0.35))
            st.markdown("#### Monthly savings vs 20% target")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            wd = exp.groupby(exp["d"].dt.day_name())["amount"].sum()
            n_weeks = max(1, (exp["d"].max() - exp["d"].min()).days / 7)
            order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            vals = [wd.get(dname, 0) / n_weeks for dname in order]
            top = order[vals.index(max(vals))]
            fig = go.Figure(go.Bar(x=[o[:3] for o in order], y=vals,
                                   marker_color=[P["chart"][3] if o == top else P["chart"][0] for o in order]))
            fig.update_layout(**theme.plotly_layout(height=300, yaxis_tickprefix="₹", showlegend=False, bargap=0.3))
            st.markdown(f"#### Average spend by weekday · most on {top}")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        best, worst = m["rate"].idxmax(), m["rate"].idxmin()
        ui.table(["Month", t("income"), t("expense"), t("savings"), "Savings rate", ""],
                 [[p.strftime("%B %Y"), inr(r.income), inr(r.expense), inr(r.savings), f"{r.rate:.0f}%",
                   ui.pill("Best", "green") if p == best else ui.pill("Lowest", "red") if p == worst else ""]
                  for p, r in m.iloc[::-1].iterrows()], numeric=(1, 2, 3, 4))
