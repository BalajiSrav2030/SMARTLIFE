"""SmartLife – entry point.  Run with:  streamlit run app.py"""
import streamlit as st

import auth
import db

st.set_page_config(page_title="SmartLife", page_icon="💚", layout="wide")
db.init_db()


def login_page():
    st.markdown("<h1 style='text-align:center'>Smart<span style='color:#22c55e'>Life</span></h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b'>Unga full financial life, oru idathula</p>",
                unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        tab_login, tab_signup = st.tabs(["Login", "Sign up"])

        with tab_login:
            with st.form("login"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True, type="primary"):
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Email or password thappu.")

        with tab_signup:
            with st.form("signup", clear_on_submit=True):
                name = st.text_input("Full name")
                email = st.text_input("Email ")
                password = st.text_input("Password (min 8 chars)", type="password")
                if st.form_submit_button("Create account", use_container_width=True):
                    ok, msg = auth.register(name, email, password)
                    (st.success if ok else st.error)(msg)


user = auth.current_user()

if user is None:
    pg = st.navigation([st.Page(login_page, title="Login", icon="🔑")], position="hidden")
else:
    pages = {
        "Main": [
            st.Page("views/dashboard.py", title="Dashboard", icon="🏠", default=True),
            st.Page("views/income_expenses.py", title="Income & Expenses", icon="💸"),
            st.Page("views/holdings.py", title="Investments & Assets", icon="📊"),
        ],
        "Tools": [
            st.Page("views/calculators.py", title="Calculators", icon="🧮"),
            st.Page("views/futures.py", title="Futures Risk Calc", icon="⚡"),
        ],
        "Future scope": [
            st.Page("views/coming_soon.py", title="Health & Insurance", icon="🩺", url_path="insurance"),
            st.Page("views/coming_soon.py", title="Family & Nominees", icon="👨‍👩‍👧", url_path="family"),
            st.Page("views/coming_soon.py", title="Legacy Vault", icon="🔐", url_path="vault"),
            st.Page("views/coming_soon.py", title="Learn", icon="📚", url_path="learn"),
        ],
    }
    with st.sidebar:
        st.markdown(f"### Smart<span style='color:#22c55e'>Life</span>", unsafe_allow_html=True)
        st.caption(f"Logged in as **{user['name']}**")
        if st.button("Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    pg = st.navigation(pages)

pg.run()
