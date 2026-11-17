"""Money Toolkit for middle-class families: salary planner, government schemes, monthly checklist."""
from html import escape

import plotly.graph_objects as go
import streamlit as st

import auth
import theme
import ui
from i18n import t
from utils import inr

user = auth.current_user()
P = theme.P()
ui.header(t("toolkit"), "Simple tools for a salaried family: split your salary, know the government schemes, and run a monthly money check.")

tab_s, tab_g, tab_c = st.tabs(["💵 Salary planner", "🏛️ Government schemes", "✅ Monthly checklist"])

# ================= SALARY PLANNER (50/30/20) =================
with tab_s:
    c1, c2 = st.columns([1, 1.4])
    with c1:
        sal = st.number_input("Monthly take-home salary (₹)", 5000, 10_00_000, 50_000, step=1000)
        emi = st.number_input("Current EMIs per month (₹)", 0, 10_00_000, 0, step=500)
        rent = st.number_input("Rent per month (₹)", 0, 10_00_000, 12_000, step=500)
        dependents = st.number_input("Dependents (spouse, kids, parents)", 0, 10, 2)
    needs, wants, save = sal * 0.5, sal * 0.3, sal * 0.2
    with c2:
        fig = go.Figure(go.Pie(labels=["Needs (50%)", "Wants (30%)", "Savings & investing (20%)"], values=[needs, wants, save],
                               hole=0.6, sort=False, marker=dict(colors=[P["chart"][1], P["chart"][2], P["chart"][0]],
                                                                 line=dict(color=P["surface"], width=2))))
        fig.update_layout(**theme.plotly_layout(height=300, legend=dict(orientation="v", x=1, y=0.5)),
                          annotations=[dict(text=f"<b>{inr(sal)}</b>", showarrow=False, font=dict(size=15, color=P["ink"]))])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    ui.kpis([{"l": "Needs: rent, food, bills, EMI", "v": inr(needs)}, {"l": "Wants: eating out, shopping, trips", "v": inr(wants)},
             {"l": "Savings & investing", "v": inr(save), "hero": True}])
    warn = []
    if emi > sal * 0.4:
        warn.append(f"⚠️ EMIs are {emi / sal * 100:.0f}% of take-home pay. Many lenders and planners treat about 40% as the upper limit.")
    if rent + emi > needs:
        warn.append(f"⚠️ Rent + EMI ({inr(rent + emi)}) already use more than the 50% needs share. Cut wants first to protect savings.")
    for w in warn:
        st.warning(w)
    emergency_target = (needs + wants) * 6
    split = [("Emergency fund (until you have 6 months of expenses)", save * 0.4, f"Target about {inr(emergency_target)}"),
             ("Term + health insurance premiums", save * 0.15, f"Term cover ~10–15× yearly income = {inr(sal * 12 * 10)}–{inr(sal * 12 * 15)}"),
             ("SIP in mutual funds (long-term goals)", save * 0.35, "Index or diversified equity funds for 7+ year goals"),
             ("Short-term goals (trip, gadget, festival)", save * 0.10, "Recurring deposit or liquid fund")]
    ui.card("Suggested split of your 20% savings",
            ui.rows([(escape(a), f"<b>{inr(b)}</b> / month<div class='m' style='text-align:right'>{escape(c)}</div>") for a, b, c in split])
            + f"<p class='m' style='margin-top:8px'>With {dependents} dependent(s), make term and health insurance a priority before investing for wants. "
              "Once the emergency fund is full, move that share to SIPs. A thumb rule, not advice.</p>")

# ================= GOVERNMENT SCHEMES =================
with tab_g:
    st.info("Interest rates, premiums and limits change. Always check the latest on indiapost.gov.in, npscra.nsdl.co.in, "
            "jansuraksha.gov.in or your bank before investing. General information, not advice.")
    SCHEMES = [
        ("Public Provident Fund (PPF)", "Anyone (one account per person)", "Long-term tax-free savings",
         "15-year lock-in, extendable in 5-year blocks · ₹500 to ₹1.5 lakh a year · government-backed · tax-free interest"),
        ("Sukanya Samriddhi Yojana (SSY)", "Parents of a girl child below 10 years", "Daughter's education / marriage",
         "Deposits for 15 years · matures 21 years from opening · ₹250 to ₹1.5 lakh a year · government-backed"),
        ("National Pension System (NPS)", "Indian citizens 18–70", "Retirement",
         "Market-linked, regulated by PFRDA · low cost · at retirement part is taken as lump sum and part buys an annuity"),
        ("Atal Pension Yojana (APY)", "Age 18–40, not an income-tax payer", "Guaranteed pension",
         "Fixed pension of ₹1,000 to ₹5,000 a month from age 60, based on the chosen amount and joining age"),
        ("PM Jeevan Jyoti Bima Yojana (PMJJBY)", "Age 18–50 with a bank account", "Low-cost life cover",
         "₹2 lakh life cover, renewed every year, premium auto-debited from the bank account"),
        ("PM Suraksha Bima Yojana (PMSBY)", "Age 18–70 with a bank account", "Low-cost accident cover",
         "₹2 lakh for accidental death or full disability, very small yearly premium, auto-debited"),
        ("Ayushman Bharat PM-JAY", "Eligible families as per government lists; senior citizens 70+", "Hospital cover",
         "Cashless hospital treatment up to ₹5 lakh per family per year at empanelled hospitals"),
        ("Senior Citizens Savings Scheme (SCSS)", "Age 60+ (some early retirees)", "Regular income for retirees",
         "5-year term, interest paid every quarter · government-backed · investment limit applies"),
    ]
    ui.table(["Scheme", "Who can join", "Best for", "Key features"],
             [[f"<b>{escape(a)}</b>", escape(b), escape(c), f"<span style='white-space:normal'>{escape(d)}</span>"] for a, b, c, d in SCHEMES])
    st.caption("Tip for families: PMJJBY + PMSBY give basic cover cheaply, but most earning members also need a proper term plan and health insurance.")

# ================= MONTHLY CHECKLIST =================
with tab_c:
    st.markdown("Tick these off once a month. Takes 15 minutes, saves a lot of stress.")
    CHECK = [
        ("Money in", ["Salary credited and checked against payslip", "Rent / other income received"]),
        ("Money out", ["All EMIs and credit card bills paid in full and on time", "Electricity, phone, internet, gas paid",
                       "Spending checked against budgets (Budget & Daily page)"]),
        ("Saving", ["SIPs ran successfully", "Emergency fund topped up", "Goal savings moved (trip, wedding, education)"]),
        ("Protection", ["Insurance renewals in the next 30 days checked", "Nominees correct on any new account or policy"]),
        ("Safety", ["No OTP, PIN or password shared with anyone", "Bank SMS / statement checked for unknown transactions",
                    "Family knows where the Legacy Vault records are"]),
    ]
    total = sum(len(v) for _, v in CHECK)
    done = 0
    cols = st.columns(len(CHECK))
    for col, (grp, items) in zip(cols, CHECK):
        with col:
            st.markdown(f"**{grp}**")
            for i, it in enumerate(items):
                done += st.checkbox(it, key=f"chk_{grp}_{i}")
    st.progress(done / total, text=f"{done} of {total} done this month")
    if done == total:
        st.success("All done for this month 🎉")
