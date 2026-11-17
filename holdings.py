"""Investments, Assets & Loans + Net Worth."""
from datetime import date
from html import escape

import plotly.graph_objects as go
import streamlit as st

import auth
import db
import theme
import ui
from i18n import t
from utils import inr

user = auth.current_user()
uid = user["id"]
P = theme.P()
ui.header(t("investments_assets"))

with st.expander("➕ " + t("add_new")):
    kind = st.radio(t("type"), ["investment", "asset", "loan"], horizontal=True, format_func=t, key="h_kind")
    with st.form("add_holding", clear_on_submit=True, border=False):
        c1, c2 = st.columns(2)
        category = c1.selectbox(t("category"), db.HOLDING_CATEGORIES[kind])
        name = c2.text_input(t("name"), max_chars=80)
        c3, c4, c5 = st.columns(3)
        invested = c3.number_input(t("loan_amount") if kind == "loan" else t("invested"), 0.0, step=1000.0)
        current = c4.number_input(t("outstanding") if kind == "loan" else t("current_value"), 0.0, step=1000.0)
        due = c5.date_input(t("next_due"), value=None, min_value=date.today())
        if st.form_submit_button(t("save"), type="primary"):
            if not name.strip() or current <= 0:
                st.error(f"{t('name')} + {t('current_value')}")
            else:
                db.add_holding(uid, kind, category, name.strip(), invested, current, due)
                st.rerun()

rows = db.get_holdings(uid)
if not rows:
    st.info(t("no_data"))
    st.stop()

inv = [r for r in rows if r["kind"] == "investment"]
val = lambda k: sum(r["current_value"] for r in rows if r["kind"] == k)
inv_in = sum(r["invested"] for r in inv)
ret = (val("investment") - inv_in) / inv_in * 100 if inv_in else 0
ui.kpis([
    {"l": t("net_worth"), "v": inr(val("investment") + val("asset") - val("loan")), "hero": True},
    {"l": t("investments"), "v": inr(val("investment")), "s": f"{ret:+.1f}% {t('returns')}", "cls": "good" if ret >= 0 else "bad"},
    {"l": t("assets"), "v": inr(val("asset"))},
    {"l": t("loans"), "v": inr(val("loan")), "cls": "bad"},
])

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"#### {t('allocation')}")
    alloc = {}
    for r in rows:
        if r["kind"] != "loan":
            alloc[r["category"]] = alloc.get(r["category"], 0) + r["current_value"]
    items = sorted(alloc.items(), key=lambda kv: -kv[1])
    fig = go.Figure(go.Pie(labels=[k for k, _ in items], values=[v for _, v in items], hole=0.62, sort=False,
                           marker=dict(colors=P["chart"], line=dict(color=P["surface"], width=2)), textinfo="percent"))
    fig.update_layout(**theme.plotly_layout(height=320, legend=dict(orientation="v", x=1, y=0.5, font=dict(color=P["muted"]))))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with c2:
    st.markdown(f"#### {t('investments')}: {t('invested').split(' (')[0]} vs {t('current_value').split(' (')[0]}")
    g = {}
    for r in inv:
        a = g.setdefault(r["category"], [0, 0])
        a[0] += r["invested"]
        a[1] += r["current_value"]
    fig = go.Figure([go.Bar(name=t("invested").split(" (")[0], x=list(g), y=[v[0] for v in g.values()], marker_color=P["chart"][7]),
                     go.Bar(name=t("current_value").split(" (")[0], x=list(g), y=[v[1] for v in g.values()], marker_color=P["chart"][0])])
    fig.update_layout(**theme.plotly_layout(barmode="group", height=320, yaxis_tickprefix="₹", bargap=0.35))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

for k in ("investment", "asset", "loan"):
    part = [r for r in rows if r["kind"] == k]
    if not part:
        continue
    st.markdown(f"#### {t(k + 's')}")
    data = []
    for r in part:
        gain = r["current_value"] - r["invested"]
        data.append([escape(r["category"]), escape(r["name"]), inr(r["invested"]), inr(r["current_value"]),
                     "" if k == "loan" else f"<span class='{'good' if gain >= 0 else 'bad'}'>{inr(gain)}</span>",
                     r["due_date"] or "—"])
    ui.table([t("category"), t("name"), t("loan_amount") if k == "loan" else t("invested"),
              t("outstanding") if k == "loan" else t("current_value"), "Gain", t("next_due")], data, numeric=(2, 3, 4))

with st.expander("🗑️ " + t("delete")):
    opts = {f"{t(r['kind'])} · {r['name']}": r["id"] for r in rows}
    pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed")
    if st.button(t("delete")):
        db.delete_holding(uid, opts[pick])
        st.rerun()
