"""Financial goals with progress and the monthly SIP needed to reach each one."""
from datetime import date
from html import escape

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
ui.header(t("goals"), "Wedding, trip, house, education, health, retirement: plan each one with a target and a date.")

# Typical middle-class goals: (icon, name, amount today in ₹, years away, expected return %)
# Amounts are starting suggestions only – edit them to your own plan. Safer (lower-return) choices for short goals.
TEMPLATES = [
    ("🛟", "Emergency fund", 300000, 1, 6.5), ("✈️", "Family trip", 150000, 1, 6.5),
    ("💪", "Fitness: gym and equipment", 50000, 1, 6.5), ("🏥", "Health and medical fund", 300000, 2, 7),
    ("💍", "Wedding", 1000000, 3, 9), ("🚗", "Car", 800000, 3, 9), ("🏍️", "Two-wheeler", 150000, 2, 7),
    ("🏡", "House down payment", 2000000, 5, 11), ("🎓", "Child education", 1500000, 12, 12),
    ("👧", "Child's wedding", 2000000, 20, 12), ("🌴", "Retirement", 15000000, 30, 12),
]

st.markdown(f"#### {t('quick_goal')}")
cols = st.columns(4)
for i, (icon, gname, amt, yrs, ret) in enumerate(TEMPLATES):
    if cols[i % 4].button(f"{icon} {gname}", key=f"tpl{i}", use_container_width=True):
        tdate_t = date(date.today().year + yrs, date.today().month, 1)
        db.add_row("goals", uid, name=f"{icon} {gname}", target=amt, saved=0, target_date=str(tdate_t),
                   expected_return=ret)
        st.toast(f"{gname} goal added: {inr(amt)} in {yrs} year{'s' if yrs > 1 else ''}. Edit it below.")
        st.rerun()
st.caption("One click adds the goal with a suggested amount and date. Use ✏️ Update on the goal to change what you have saved, "
           "or delete it and add your own figures with ➕.")

with st.expander("➕ " + t("add_new"), expanded=not db.list_rows("goals", uid)):
    with st.form("goal", clear_on_submit=True, border=False):
        c1, c2 = st.columns(2)
        name = c1.text_input(t("name"), placeholder="e.g. Child education", max_chars=60)
        target = c2.number_input(t("target_amount"), 0.0, step=50000.0)
        c3, c4, c5 = st.columns(3)
        saved = c3.number_input(t("saved_so_far"), 0.0, step=10000.0)
        tdate = c4.date_input(t("target_date"), value=date(date.today().year + 5, date.today().month, 1),
                              min_value=date.today())
        rate = c5.number_input(t("expected_return"), 0.0, 30.0, 12.0, step=0.5)
        if st.form_submit_button(t("save"), type="primary"):
            if not name.strip() or target <= 0:
                st.error(f"{t('name')} + {t('target_amount')}")
            else:
                db.add_row("goals", uid, name=name.strip(), target=target, saved=saved, target_date=str(tdate),
                           expected_return=rate)
                st.rerun()


def sip_needed(remaining, months, rate):
    """Monthly SIP so that SIP growth + nothing else covers `remaining`."""
    if remaining <= 0:
        return 0.0
    if months <= 0:
        return remaining
    i = rate / 12 / 100
    factor = months if i == 0 else ((1 + i) ** months - 1) / i * (1 + i)
    return remaining / factor


goals = db.list_rows("goals", uid, order="target_date")
if not goals:
    st.info(t("no_data"))
    st.stop()

today = date.today()
tot_t = sum(g["target"] for g in goals)
tot_s = sum(g["saved"] for g in goals)
plans = []
for g in goals:
    d = date.fromisoformat(g["target_date"])
    months = max(0, (d.year - today.year) * 12 + d.month - today.month)
    i = g["expected_return"] / 12 / 100
    grown_saved = g["saved"] * (1 + i) ** months
    plans.append((g, d, months, sip_needed(g["target"] - grown_saved, months, g["expected_return"])))

ui.kpis([{"l": t("target_amount"), "v": inr(tot_t)}, {"l": t("saved_so_far"), "v": inr(tot_s), "cls": "good"},
         {"l": t("progress"), "v": f"{tot_s / tot_t * 100:.0f}%" if tot_t else "0%"},
         {"l": t("monthly_needed"), "v": inr(sum(p[3] for p in plans)), "hero": True}])

cols = st.columns(2)
for idx, (g, d, months, sip) in enumerate(plans):
    pct = g["saved"] / g["target"] * 100 if g["target"] else 0
    color = P["chart"][idx % len(P["chart"])]
    status = ui.pill("Reached", "green") if pct >= 100 else ui.pill(f"{months} months left", "amber" if months < 12 else "grey")
    body = (f"<div style='display:flex;justify-content:space-between'><span class='m'>{inr(g['saved'])} / {inr(g['target'])}</span>"
            f"<b>{pct:.0f}%</b></div>{ui.bar(pct, color)}"
            + ui.rows([(t("target_date"), d.strftime("%b %Y")), (t("expected_return"), f"{g['expected_return']:g}%"),
                       (t("monthly_needed"), f"<b>{inr(sip)}</b>"), ("", status)]))
    with cols[idx % 2]:
        ui.card("🎯 " + g["name"], body)
        with st.popover("✏️ Update"):
            new_saved = st.number_input(t("saved_so_far"), 0.0, value=float(g["saved"]), step=5000.0, key=f"gs{g['id']}")
            new_target = st.number_input(t("target_amount"), 1.0, value=float(g["target"]), step=10000.0, key=f"gt{g['id']}")
            new_date = st.date_input(t("target_date"), value=date.fromisoformat(g["target_date"]), min_value=date.today(),
                                     key=f"gdt{g['id']}")
            b1, b2 = st.columns(2)
            if b1.button(t("save"), key=f"gu{g['id']}", type="primary"):
                db.update_row("goals", uid, g["id"], saved=new_saved, target=new_target, target_date=str(new_date))
                st.rerun()
            if b2.button(t("delete"), key=f"gd{g['id']}"):
                db.delete_row("goals", uid, g["id"])
                st.rerun()

st.caption("Monthly SIP needed assumes your current savings also keep growing at the expected return. " + t("calc_note"))
