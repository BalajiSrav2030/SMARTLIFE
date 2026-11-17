"""Income & Expenses: add, filter, delete."""
from datetime import date
from html import escape

import pandas as pd
import streamlit as st

import auth
import budget_logic
import db
import ui
from i18n import t
from utils import inr

user = auth.current_user()
uid = user["id"]
ui.header(t("income_expenses"))
_f = st.session_state.pop("ie_flash", None)
if _f:
    (st.error if _f[0] == "over" else st.warning)(_f[1])

with st.expander("➕ " + t("add_new"), expanded=True):
    txn_type = st.radio(t("type"), ["expense", "income"], horizontal=True, format_func=t, key="ie_type")
    cats = db.EXPENSE_CATEGORIES if txn_type == "expense" else db.INCOME_CATEGORIES
    with st.form("add_txn", clear_on_submit=True, border=False):
        c1, c2, c3 = st.columns(3)
        category = c1.selectbox(t("category"), cats)
        amount = c2.number_input(t("amount"), min_value=0.0, step=100.0, format="%.2f")
        txn_date = c3.date_input(t("date"), value=date.today(), max_value=date.today())
        note = st.text_input(t("note"), max_chars=100)
        if st.form_submit_button(t("save"), type="primary"):
            if amount <= 0:
                st.error("Amount > 0")
            else:
                db.add_transaction(uid, txn_type, category, amount, txn_date, note.strip())
                st.toast(t("saved") + " ✅")
                if txn_type == "expense":
                    level, row = budget_logic.check_category(uid, category)
                    if level in ("near", "over"):
                        st.session_state.ie_flash = (level, f"{'🔴' if level == 'over' else '⚠️'} {category}: "
                                                     f"{row['pct']:.0f}% of the monthly budget used ({inr(row['spent'])} of {inr(row['limit'])}).")
                st.rerun()

txns = db.get_transactions(uid)
if not txns:
    st.info(t("no_data"))
    st.stop()

df = pd.DataFrame(txns)
df["txn_date"] = pd.to_datetime(df["txn_date"])
df["month"] = df["txn_date"].dt.strftime("%Y-%m")
months = sorted(df["month"].unique(), reverse=True)
f1, f2, _ = st.columns([1, 1, 2])
sel_m = f1.selectbox(t("month"), ["all", *months], format_func=lambda m: t("all") if m == "all" else
                     pd.Timestamp(m + "-01").strftime("%B %Y"))
sel_t = f2.selectbox(t("type"), ["all", "income", "expense"], format_func=t)
view = df[(df.month == sel_m) if sel_m != "all" else df.month.notna()]
if sel_t != "all":
    view = view[view.txn_type == sel_t]

inc = view.loc[view.txn_type == "income", "amount"].sum()
exp = view.loc[view.txn_type == "expense", "amount"].sum()
ui.kpis([{"l": t("income"), "v": inr(inc), "cls": "good"}, {"l": t("expense"), "v": inr(exp), "cls": "bad"},
         {"l": t("savings"), "v": inr(inc - exp)}])

rows = [[r.txn_date.strftime("%d %b %Y"), escape(t(r.txn_type)), escape(r.category), escape(r.note or ""),
         f"<span class='{'good' if r.txn_type == 'income' else ''}'>{'+' if r.txn_type == 'income' else '−'}{inr(r.amount)}</span>"]
        for r in view.head(100).itertuples()]
ui.table([t("date"), t("type"), t("category"), t("note"), t("amount")], rows, numeric=(4,))
if len(view) > 100:
    st.caption(f"Showing latest 100 of {len(view)}")

with st.expander("🗑️ " + t("delete")):
    opts = {f"{r.txn_date.date()} · {r.category} · {inr(r.amount)}": r.id for r in view.itertuples()}
    if opts:
        pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed")
        if st.button(t("delete")):
            db.delete_transaction(uid, opts[pick])
            st.rerun()
