"""SmartLife – entry point.  Run with:  streamlit run app.py"""
from datetime import datetime, timedelta

import streamlit as st

import auth
import db
import theme
import ui
import vault_crypto
from i18n import LANGS, t

st.set_page_config(page_title="SmartLife", page_icon="💚", layout="wide")
db.init_db()


@st.cache_resource
def ensure_demo_user():
    """On a fresh server (e.g. Streamlit Cloud) create the demo account with sample data once."""
    if db.get_user_by_email("demo@smartlife.app") is None:
        from sample_data import load_sample
        load_sample(db.create_user("Demo User", "demo@smartlife.app", auth.hash_password("demo1234")))
    return True


ensure_demo_user()
st.session_state.setdefault("lang", "en")
st.session_state.setdefault("dark", False)
theme.apply()


def prefs(container):
    """Language + dark mode controls (sidebar when logged in, top of page on login)."""
    c1, c2 = container.columns([3, 2]) if container is st else (container, container)
    keys = list(LANGS)
    c1.selectbox(t("language"), keys, format_func=LANGS.get, key="lang")
    c2.toggle(t("dark_mode"), key="dark")


def nominee_portal():
    st.caption("If you are a nominee, enter the owner's email, your email and the access code the owner gave you.")
    with st.form("nominee"):
        owner = st.text_input("Owner's email")
        mine = st.text_input("Your email (as saved by the owner)")
        code = st.text_input(t("access_code"), type="password", placeholder="XXXX-XXXX")
        go = st.form_submit_button("Open vault", use_container_width=True)
    if not go:
        return
    tries = st.session_state.get("nominee_tries", 0)
    if tries >= 5:
        st.error("Too many attempts. Close the browser and try again later.")
        return
    rec = db.find_nominee(owner, mine)
    if not rec or not vault_crypto.check_code(code, rec["code_hash"]):
        st.session_state.nominee_tries = tries + 1
        st.error("Details don't match. Check the emails and the access code.")
        return
    settings = db.get_vault_settings(rec["owner_id"])
    last = datetime.fromisoformat(rec["last_login"]) if rec["last_login"] else None
    inactive = last is None or datetime.utcnow() - last > timedelta(days=settings["inactivity_days"])
    if not (settings["released"] or inactive):
        st.info(f"Verified ✅ {rec['owner_name']}'s vault is still locked. It opens if the owner releases it, "
                f"or after {settings['inactivity_days']} days without the owner logging in.")
        return
    st.success(f"Verified ✅ Records shared with you by {rec['owner_name']}")
    for it in db.list_rows("vault_items", rec["owner_id"]):
        if not it["visible"]:
            continue
        notes = vault_crypto.decrypt(it["notes_enc"])
        with st.expander(f"{it['title']} · {it['itype']}"):
            st.write(f"**{t('institution')}:** {it['institution'] or '—'}  ·  **Ref:** XXXX{it['last4'] or ''}")
            if notes:
                st.write(notes.decode())
            if it["file_enc"]:
                st.download_button(f"⬇ {it['file_name']}", vault_crypto.decrypt(it["file_enc"]),
                                   file_name=it["file_name"], key=f"nd{it['id']}")


def login_page():
    top = st.columns([3, 2])
    with top[1]:
        prefs(st)
    st.markdown(f"""<div style="text-align:center;margin:10px 0 18px">
      <div style="font-family:var(--display);font-weight:700;font-size:44px;letter-spacing:-.03em;color:var(--ink)">Smart<span style="color:var(--accent)">Life</span></div>
      <div style="color:var(--muted);font-size:16px">{t('tagline')}</div></div>""", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        tab_login, tab_signup, tab_nom = st.tabs([t("login"), t("signup"), "🔐 " + t("nominee_access")])
        with tab_login:
            with st.form("login"):
                email = st.text_input(t("email"))
                password = st.text_input(t("password"), type="password")
                if st.form_submit_button(t("login"), use_container_width=True, type="primary"):
                    if auth.login(email, password):
                        db.touch_login(st.session_state.user["id"])
                        st.rerun()
                    else:
                        st.error(t("login_error"))
            st.caption(t("demo_hint"))
        with tab_signup:
            with st.form("signup", clear_on_submit=True):
                name = st.text_input(t("full_name"))
                email = st.text_input(t("email") + " ")
                password = st.text_input(t("password") + " (min 8)", type="password")
                if st.form_submit_button(t("create_account"), use_container_width=True):
                    ok, msg = auth.register(name, email, password)
                    (st.success if ok else st.error)(msg)
        with tab_nom:
            nominee_portal()


user = auth.current_user()

if user is None:
    pg = st.navigation([st.Page(login_page, title="Login", icon="🔑")], position="hidden")
else:
    pages = {
        t("grp_money"): [
            st.Page("views/dashboard.py", title=t("dashboard"), icon="🏠", default=True),
            st.Page("views/income_expenses.py", title=t("income_expenses"), icon="💸"),
            st.Page("views/budget.py", title=t("budget_daily"), icon="📅"),
            st.Page("views/holdings.py", title=t("investments_assets"), icon="📊"),
            st.Page("views/goals.py", title=t("goals"), icon="🎯"),
        ],
        t("grp_tools"): [
            st.Page("views/calculators.py", title=t("calculators"), icon="🧮"),
            st.Page("views/futures.py", title=t("futures"), icon="⚡"),
            st.Page("views/markets.py", title=t("markets"), icon="📰"),
            st.Page("views/toolkit.py", title=t("toolkit"), icon="🧰"),
        ],
        t("grp_protect"): [
            st.Page("views/insurance.py", title=t("insurance"), icon="🩺"),
            st.Page("views/family.py", title=t("family"), icon="👨‍👩‍👧"),
            st.Page("views/vault.py", title=t("vault"), icon="🔐"),
        ],
        t("grp_learn"): [
            st.Page("views/learn.py", title=t("learn"), icon="📚"),
        ],
    }
    with st.sidebar:
        st.caption(t("tagline"))
        prefs(st.sidebar)
        st.caption(f"{t('signed_in_as')} **{user['name']}**")
        if st.button(t("logout"), use_container_width=True):
            auth.logout()
            st.rerun()
    st.logo("assets/logo.svg", size="large")
    pg = st.navigation(pages, expanded=True)

pg.run()
