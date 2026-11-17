"""Family members, nominee mapping for every account / policy, and gaps."""
from datetime import date
from html import escape

import streamlit as st

import auth
import db
import ui
from i18n import t

user = auth.current_user()
uid = user["id"]
ui.header(t("family"), "Make sure every account, investment and policy has a nominee, and your family knows.")

RELATIONS = ["Spouse", "Son", "Daughter", "Father", "Mother", "Brother", "Sister", "Other"]
fam = db.list_rows("family", uid)
noms = db.list_rows("nominations", uid)
items = ([f"{h['category']} · {h['name']}" for h in db.get_holdings(uid) if h["kind"] != "loan"]
         + [f"Insurance · {p['ptype']} · {p['insurer']}" for p in db.list_rows("policies", uid)])
covered = {}
for n in noms:
    covered[n["item"]] = covered.get(n["item"], 0) + n["share"]
gaps = [i for i in items if covered.get(i, 0) < 100]

ui.kpis([{"l": t("members"), "v": len(fam)}, {"l": t("nominees"), "v": sum(1 for f in fam if f["is_nominee"])},
         {"l": "Items covered", "v": f"{len(items) - len(gaps)} / {len(items)}"},
         {"l": t("coverage_gap"), "v": len(gaps), "cls": "bad" if gaps else "good"}])

tab_m, tab_n = st.tabs(["👨‍👩‍👧 " + t("members"), "📝 " + t("nominees")])

with tab_m:
    with st.expander("➕ " + t("add_new"), expanded=not fam):
        with st.form("mem", clear_on_submit=True, border=False):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input(t("name"), max_chars=60)
            rel = c2.selectbox(t("relation"), RELATIONS)
            dob = c3.date_input(t("dob"), value=None, min_value=date(1920, 1, 1), max_value=date.today())
            c4, c5 = st.columns([2, 1])
            email = c4.text_input(t("email") + " (for Legacy Vault access)", max_chars=80)
            is_nom = c5.checkbox("Is a nominee", value=True)
            if st.form_submit_button(t("save"), type="primary"):
                if not name.strip():
                    st.error(t("name"))
                else:
                    db.add_row("family", uid, name=name.strip(), relation=rel, dob=str(dob) if dob else None,
                               email=email.strip().lower() or None, is_nominee=int(is_nom))
                    st.rerun()
    if fam:
        def age(d):
            if not d:
                return "—"
            b = date.fromisoformat(d)
            return str(date.today().year - b.year - ((date.today().month, date.today().day) < (b.month, b.day)))
        ui.table([t("name"), t("relation"), "Age", t("email"), "Nominee"],
                 [[escape(f["name"]), escape(f["relation"]), age(f["dob"]), escape(f["email"] or "—"),
                   ui.pill("Yes", "green") if f["is_nominee"] else ui.pill("No")] for f in fam])
        with st.expander("🗑️ " + t("delete")):
            opts = {f"{f['name']} ({f['relation']})": f["id"] for f in fam}
            pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed")
            if st.button(t("delete"), key="del_mem"):
                db.delete_row("family", uid, opts[pick])
                st.rerun()

with tab_n:
    nominees = [f for f in fam if f["is_nominee"]]
    if not nominees:
        st.info("Add a family member and tick 'Is a nominee' first.")
    elif not items:
        st.info("Add investments, assets or policies first.")
    else:
        with st.form("nom", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 1.3, 0.8])
            item = c1.selectbox(t("nominee_for"), items)
            who = c2.selectbox(t("nominees"), nominees, format_func=lambda f: f"{f['name']} ({f['relation']})")
            share = c3.number_input(t("share_pct"), 1.0, 100.0, 100.0, step=5.0)
            if st.form_submit_button(t("save"), type="primary"):
                if covered.get(item, 0) + share > 100.0001:
                    st.error(f"Total share for this item would be over 100% (already {covered.get(item, 0):g}%).")
                else:
                    db.add_row("nominations", uid, member_id=who["id"], item=item, share=share)
                    st.rerun()

    names = {f["id"]: f["name"] for f in fam}
    rows = []
    for i in items:
        mine = [n for n in noms if n["item"] == i]
        who = ", ".join(f"{escape(names.get(n['member_id'], '?'))} {n['share']:g}%" for n in mine) or "—"
        tot = covered.get(i, 0)
        rows.append([escape(i), who, ui.pill("100%", "green") if tot >= 100 else ui.pill(f"{tot:g}%", "red" if tot == 0 else "amber")])
    if rows:
        ui.table([t("nominee_for"), t("nominees"), "Covered"], rows)
    if noms:
        with st.expander("🗑️ " + t("delete")):
            opts = {f"{n['item']} → {names.get(n['member_id'], '?')} ({n['share']:g}%)": n["id"] for n in noms}
            pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed", key="del_nom_sel")
            if st.button(t("delete"), key="del_nom"):
                db.delete_row("nominations", uid, opts[pick])
                st.rerun()
    st.caption("SmartLife only records your plan. Also register nominees officially with each bank, AMC, depository and insurer.")
