"""Calculators hub: SIP, Lumpsum, EMI, Goal, FD, Retirement."""
import plotly.graph_objects as go
import streamlit as st

import finance
import theme
import ui
from i18n import t
from utils import inr

P = theme.P()
ui.header(t("calculators"), t("calc_note"))

tabs = st.tabs(["📈 SIP", "💰 Lumpsum", "🏠 EMI", "🎯 Goal", "🏦 FD", "🌴 Retirement"])


def growth(rows, inv_key="Invested", val_key="Value"):
    fig = go.Figure([
        go.Bar(name=t("total_invested"), x=[r["Year"] for r in rows], y=[r[inv_key] for r in rows], marker_color=P["chart"][7]),
        go.Bar(name=t("future_value"), x=[r["Year"] for r in rows], y=[r[val_key] for r in rows], marker_color=P["chart"][0]),
    ])
    fig.update_layout(**theme.plotly_layout(barmode="group", height=320, bargap=0.3, yaxis_tickprefix="₹", xaxis_title=t("years")))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


with tabs[0]:
    c = st.columns(4)
    m = c[0].number_input(t("monthly_sip"), 100, 10_00_000, 10_000, step=500)
    r = c[1].number_input(t("expected_return"), 1.0, 30.0, 12.0, step=0.5, key="sr")
    y = c[2].number_input(t("years"), 1, 40, 10, key="sy")
    s = c[3].number_input(t("step_up"), 0.0, 50.0, 0.0, step=5.0)
    inv, val, rows = finance.sip_future_value(m, r, y, s)
    ui.kpis([{"l": t("total_invested"), "v": inr(inv)}, {"l": t("est_returns"), "v": inr(val - inv), "cls": "good"},
             {"l": t("future_value"), "v": inr(val), "hero": True}])
    growth(rows)

with tabs[1]:
    c = st.columns(3)
    p = c[0].number_input(t("amount"), 1000, 10_00_00_000, 1_00_000, step=10_000)
    r = c[1].number_input(t("expected_return"), 1.0, 30.0, 12.0, step=0.5, key="lr")
    y = c[2].number_input(t("years"), 1, 40, 10, key="ly")
    fv = finance.lumpsum_future_value(p, r, y)
    ui.kpis([{"l": t("total_invested"), "v": inr(p)}, {"l": t("future_value"), "v": inr(fv), "hero": True},
             {"l": "Growth", "v": f"{fv / p:.2f}x"}])
    growth([{"Year": k, "Invested": p, "Value": finance.lumpsum_future_value(p, r, k)} for k in range(1, int(y) + 1)])

with tabs[2]:
    c = st.columns(3)
    loan = c[0].number_input(t("loan_amount"), 10_000, 10_00_00_000, 30_00_000, step=50_000)
    lr = c[1].number_input(t("interest_rate"), 0.0, 30.0, 8.5, step=0.1)
    ly = c[2].number_input(t("years"), 1, 30, 20, key="ey")
    e = finance.emi(loan, lr, ly)
    total = e * ly * 12
    ui.kpis([{"l": t("monthly_emi"), "v": inr(e), "hero": True}, {"l": t("total_interest"), "v": inr(total - loan), "cls": "bad"},
             {"l": t("total_payment"), "v": inr(total)}])
    # yearly balance
    bal, i, rows = loan, lr / 12 / 100, []
    for yr in range(1, int(ly) + 1):
        paid_i = 0
        for _ in range(12):
            it = bal * i
            paid_i += it
            bal = max(0, bal - (e - it))
        rows.append((yr, bal, paid_i))
    fig = go.Figure([go.Scatter(x=[r_[0] for r_ in rows], y=[r_[1] for r_ in rows], fill="tozeroy", name="Balance",
                                line=dict(color=P["chart"][1], width=3))])
    fig.update_layout(**theme.plotly_layout(height=300, yaxis_tickprefix="₹", xaxis_title=t("years")))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tabs[3]:
    c = st.columns(4)
    cost = c[0].number_input(t("cost_today"), 10_000, 50_00_00_000, 20_00_000, step=50_000)
    gy = c[1].number_input(t("years"), 1, 40, 5, key="gy")
    infl = c[2].number_input(t("inflation"), 0.0, 15.0, 6.0, step=0.5)
    gr = c[3].number_input(t("expected_return"), 1.0, 30.0, 12.0, step=0.5, key="gr")
    fc, sip = finance.goal_monthly_sip(cost, gy, infl, gr)
    ui.kpis([{"l": f"{t('future_value')} ({gy} {t('years').lower()})", "v": inr(fc)},
             {"l": t("monthly_needed"), "v": inr(sip), "hero": True}])

with tabs[4]:
    c = st.columns(3)
    fd = c[0].number_input(t("amount"), 1000, 10_00_00_000, 1_00_000, step=10_000, key="fd")
    fr = c[1].number_input(t("interest_rate"), 0.0, 15.0, 7.0, step=0.1, key="fr")
    fy = c[2].number_input(t("years"), 1, 10, 3, key="fy")
    mat = fd * (1 + fr / 400) ** (4 * fy)
    ui.kpis([{"l": "Maturity", "v": inr(mat), "hero": True}, {"l": "Interest", "v": inr(mat - fd), "cls": "good"}])
    st.markdown('<div class="sl-formula">Maturity = P × (1 + r/4)^(4 × years) · quarterly compounding, before tax</div>',
                unsafe_allow_html=True)

with tabs[5]:
    c = st.columns(4)
    age = c[0].number_input("Current age", 18, 70, 28)
    ret_age = c[1].number_input("Retirement age", 40, 75, 60)
    life = c[2].number_input("Plan till age", 60, 100, 85)
    mexp = c[3].number_input("Monthly expenses today (₹)", 5_000, 10_00_000, 40_000, step=5_000)
    c = st.columns(3)
    infl = c[0].number_input(t("inflation"), 0.0, 15.0, 6.0, step=0.5, key="ri")
    pre = c[1].number_input("Return before retirement (%)", 1.0, 20.0, 12.0, step=0.5)
    post = c[2].number_input("Return after retirement (%)", 1.0, 15.0, 7.0, step=0.5)
    if ret_age <= age or life <= ret_age:
        st.error("Ages: current < retirement < plan-till")
    else:
        yrs = ret_age - age
        exp_at_ret = mexp * (1 + infl / 100) ** yrs * 12
        real = (1 + post / 100) / (1 + infl / 100) - 1
        n = life - ret_age
        corpus = exp_at_ret * (n if abs(real) < 1e-9 else (1 - (1 + real) ** -n) / real * (1 + real))
        _, sip = finance.goal_monthly_sip(corpus, yrs, 0, pre)
        ui.kpis([{"l": "Yearly expenses at retirement", "v": inr(exp_at_ret)},
                 {"l": "Corpus needed", "v": inr(corpus), "hero": True}, {"l": t("monthly_needed"), "v": inr(sip)}])
        st.markdown('<div class="sl-formula">Corpus = yearly expense at retirement × annuity factor at the real return '
                    '((1+post)/(1+inflation) − 1), paid at the start of each year</div>', unsafe_allow_html=True)
