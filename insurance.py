"""Health profile + insurance policies with renewal tracking and a simple cover check."""
from datetime import date
from html import escape

import streamlit as st

import auth
import db
import ui
from i18n import t
from utils import inr
import pandas as pd
import plotly.graph_objects as go
import theme

user = auth.current_user()
uid = user["id"]
ui.header(t("insurance"), "Keep health details and every policy in one place. Renewals show up on your dashboard.")

POLICY_TYPES = ["Health", "Term life", "Life (endowment / ULIP)", "Vehicle", "Home", "Personal accident", "Travel", "Other"]
BLOOD = ["", "A+", "A−", "B+", "B−", "AB+", "AB−", "O+", "O−"]

pol = db.list_rows("policies", uid, order="renewal")
today = date.today()
health_cover = sum(p["cover"] for p in pol if p["ptype"] == "Health")
life_cover = sum(p["cover"] for p in pol if p["ptype"] == "Term life")
premiums = sum(p["premium"] for p in pol)
due30 = [p for p in pol if p["renewal"] and 0 <= (date.fromisoformat(p["renewal"]) - today).days <= 30]

# yearly income from last 12 months of transactions (for a rough term-cover check)
yearly_income = sum(x["amount"] for x in db.get_transactions(uid)
                    if x["txn_type"] == "income" and (today - date.fromisoformat(x["txn_date"])).days <= 365)

ui.kpis([{"l": "Health cover", "v": inr(health_cover)}, {"l": "Life (term) cover", "v": inr(life_cover)},
         {"l": "Yearly premiums", "v": inr(premiums)}, {"l": "Renewals in 30 days", "v": len(due30), "cls": "bad" if due30 else "good"}])

tab_p, tab_h, tab_f = st.tabs(["🛡️ " + t("policies"), "🩺 " + t("health_profile"), "💪 " + t("fitness")])

with tab_p:
    with st.expander("➕ " + t("add_new"), expanded=not pol):
        with st.form("pol", clear_on_submit=True, border=False):
            c1, c2, c3 = st.columns(3)
            ptype = c1.selectbox(t("policy_type"), POLICY_TYPES)
            insurer = c2.text_input(t("insurer"), max_chars=60)
            last4 = c3.text_input("Policy no. – " + t("last4"), max_chars=4)
            c4, c5, c6 = st.columns(3)
            cover = c4.number_input(t("sum_assured"), 0.0, step=100000.0)
            premium = c5.number_input(t("premium"), 0.0, step=1000.0)
            renewal = c6.date_input(t("renewal"), value=None, min_value=today)
            covers = st.text_input("Who is covered", placeholder="Self, spouse, kids", max_chars=100)
            if st.form_submit_button(t("save"), type="primary"):
                if not insurer.strip():
                    st.error(t("insurer"))
                elif last4 and not (last4.isdigit() and len(last4) == 4):
                    st.error("Enter only the last 4 digits. Never store full policy or account numbers.")
                else:
                    db.add_row("policies", uid, ptype=ptype, insurer=insurer.strip(), policy_last4=last4, cover=cover,
                               premium=premium, renewal=str(renewal) if renewal else None, covers=covers.strip())
                    st.rerun()

    if pol:
        rows = []
        for p in pol:
            k = (date.fromisoformat(p["renewal"]) - today).days if p["renewal"] else None
            badge = ui.pill("—") if k is None else ui.pill("expired" if k < 0 else f"in {k} days",
                                                         "red" if k < 15 else "amber" if k <= 30 else "grey")
            rows.append([escape(p["ptype"]), escape(p["insurer"]), f"XXXX{escape(p['policy_last4'] or '')}",
                         inr(p["cover"]), inr(p["premium"]), (p["renewal"] or "—") + " " + badge, escape(p["covers"] or "")])
        ui.table([t("policy_type"), t("insurer"), "Policy", t("sum_assured"), t("premium"), t("renewal"), "Covers"], rows, numeric=(3, 4))
        with st.expander("🗑️ " + t("delete")):
            opts = {f"{p['ptype']} · {p['insurer']}": p["id"] for p in pol}
            pick = st.selectbox(t("delete"), list(opts), label_visibility="collapsed")
            if st.button(t("delete"), key="del_pol"):
                db.delete_row("policies", uid, opts[pick])
                st.rerun()

    tips = []
    if not health_cover:
        tips.append(("❌ No health insurance added", ui.pill("Add one", "red")))
    else:
        tips.append(("✅ Health insurance in place", ui.pill(inr(health_cover), "green")))
    if yearly_income:
        target = yearly_income * 10
        ok = life_cover >= target
        tips.append((f"{'✅' if ok else '⚠️'} Term cover vs 10× yearly income ({inr(target)})",
                     ui.pill("OK" if ok else "Low", "green" if ok else "amber")))
    ui.card("Cover check (rule of thumb)", ui.rows(tips) +
            "<p class='m' style='margin-top:8px'>A common rule of thumb is term cover of about 10–15× yearly income. "
            "This is general information, not advice; speak to a licensed advisor for your situation.</p>")

with tab_h:
    h = db.get_health(uid)
    with st.form("health"):
        c1, c2 = st.columns(2)
        bg = c1.selectbox(t("blood_group"), BLOOD, index=BLOOD.index(h.get("blood_group") or ""))
        doctor = c2.text_input(t("doctor"), h.get("doctor") or "", max_chars=80)
        cond = st.text_area(t("conditions"), h.get("conditions") or "", max_chars=300, height=80)
        allg = st.text_area(t("allergies"), h.get("allergies") or "", max_chars=300, height=80)
        emc = st.text_input("Emergency contact (name & relation)", h.get("emergency_contact") or "", max_chars=80)
        if st.form_submit_button(t("save"), type="primary"):
            db.save_health(uid, blood_group=bg, conditions=cond.strip(), allergies=allg.strip(), doctor=doctor.strip(),
                           emergency_contact=emc.strip())
            st.toast(t("saved") + " ✅")
    st.caption("Health details are personal data. Share them only with people you trust.")


with tab_f:
    P = theme.P()
    h = db.get_health(uid)
    logs = db.list_rows("fitness_log", uid, order="log_date")
    c1, c2 = st.columns([1, 2])
    with c1:
        height = st.number_input("Height (cm)", 100.0, 230.0, float(h.get("height_cm") or 170.0), step=1.0)
        if st.button("Save height"):
            db.set_height(uid, height)
            st.rerun()
    with c2:
        with st.form("fit_log", clear_on_submit=True):
            a, b, c, d = st.columns(4)
            ld = a.date_input(t("date"), value=date.today(), max_value=date.today())
            w = b.number_input("Weight (kg)", 0.0, 300.0, 0.0, step=0.1, help="0 = skip")
            stp = c.number_input("Steps", 0, 100000, 0, step=500)
            wk = d.number_input("Workout (min)", 0, 600, 0, step=5)
            nt = st.text_input("Activity", placeholder="walk, yoga, gym, cricket…", max_chars=60)
            if st.form_submit_button("➕ " + t("save"), type="primary"):
                if not (w or stp or wk):
                    st.error("Enter weight, steps or workout minutes.")
                else:
                    db.add_row("fitness_log", uid, log_date=str(ld), weight=w or None, steps=stp or None,
                               workout_min=wk or None, note=nt.strip())
                    st.rerun()
    if not logs:
        st.info("Log your weight, steps or workout to see your progress here.")
    else:
        df = pd.DataFrame(logs)
        df["log_date"] = pd.to_datetime(df["log_date"])
        wts = df.dropna(subset=["weight"])
        last_w = float(wts["weight"].iloc[-1]) if not wts.empty else None
        hcm = float(h.get("height_cm") or height)
        bmi = last_w / (hcm / 100) ** 2 if last_w else None
        band = (None if bmi is None else "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese")
        wk7 = df[df["log_date"] > pd.Timestamp(date.today()) - pd.Timedelta(days=7)]
        ui.kpis([{"l": "Latest weight", "v": f"{last_w:.1f} kg" if last_w else "—",
                  "s": (f"{last_w - float(wts['weight'].iloc[0]):+.1f} kg since first log" if len(wts) > 1 else "")},
                 {"l": "BMI", "v": f"{bmi:.1f}" if bmi else "—", "s": band or "Add weight and height",
                  "cls": "good" if band == "Normal" else "bad" if band else ""},
                 {"l": "Average steps (7 days)", "v": f"{wk7['steps'].dropna().mean():,.0f}" if wk7["steps"].notna().any() else "—",
                  "s": "Many people aim for 7,000–10,000"},
                 {"l": "Workout this week", "v": f"{wk7['workout_min'].fillna(0).sum():.0f} min",
                  "s": "WHO suggests 150+ min of moderate activity a week",
                  "cls": "good" if wk7["workout_min"].fillna(0).sum() >= 150 else ""}])
        if len(wts) > 1:
            fig = go.Figure(go.Scatter(x=wts["log_date"], y=wts["weight"], mode="lines+markers",
                                       line=dict(color=P["chart"][1], width=3)))
            fig.update_layout(**theme.plotly_layout(height=260, yaxis_title="kg", showlegend=False))
            st.markdown("#### Weight trend")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        ui.table([t("date"), "Weight", "Steps", "Workout", "Activity"],
                 [[r.log_date.strftime("%d %b %Y"), f"{r.weight:.1f} kg" if pd.notna(r.weight) else "—",
                   f"{int(r.steps):,}" if pd.notna(r.steps) else "—", f"{int(r.workout_min)} min" if pd.notna(r.workout_min) else "—",
                   escape(r.note or "")] for r in df.iloc[::-1].head(14).itertuples()])
        st.caption("BMI uses WHO adult bands. For many Asian adults, health risks start at lower BMI values; ask your doctor.")
