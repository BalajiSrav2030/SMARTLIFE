"""Markets & News: index snapshot, personal watchlist with live prices, and latest headlines."""
from html import escape

import streamlit as st

import auth
import db
import market
import ui
from i18n import t
from utils import inr

user = auth.current_user()
uid = user["id"]
ui.header(t("markets"), "Live prices for what you follow and the day's money news. Information only, not a recommendation to buy or sell.")

if st.button("🔄 Refresh prices"):
    market.stock.clear()
    market.crypto.clear()
    market.forex.clear()
    market.news.clear()

# ---- snapshot ----
SNAP = [("Nifty 50", market.stock, "NIFTY", "₹"), ("Sensex", market.stock, "SENSEX", "₹"),
        ("Bank Nifty", market.stock, "BANKNIFTY", "₹"), ("USD/INR", market.forex, "USDINR", "₹"),
        ("Bitcoin", market.crypto, "BTC", "$"), ("Gold ETF (GOLDBEES)", market.stock, "GOLDBEES", "₹")]
items = []
offline = 0
for label, fn, sym, cur in SNAP:
    q = fn(sym)
    if q:
        chg = q.get("change")
        items.append({"l": label, "v": f"{cur}{q['price']:,.2f}",
                      "s": f"{chg:+.2f}%" if chg is not None else "", "cls": "good" if (chg or 0) >= 0 else "bad"})
    else:
        offline += 1
        items.append({"l": label, "v": "—", "s": "not available"})
ui.kpis(items)
if offline == len(SNAP):
    st.warning("Live prices could not be loaded. Check your internet connection and press Refresh.")
st.caption("Indian prices from Yahoo Finance can be delayed by about 15 minutes. Crypto from CoinGecko.")

tab_w, tab_n = st.tabs(["⭐ " + t("watchlist"), "📰 " + t("news")])

with tab_w:
    with st.form("add_watch", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        sym = c1.text_input("Symbol", placeholder="RELIANCE, TCS, NIFTY, BTC, ETH…", max_chars=20)
        kind = c2.selectbox(t("type"), ["stock", "crypto"], format_func=lambda k: "Indian stock / index" if k == "stock" else "Crypto")
        c3.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if c3.form_submit_button("➕ Add", type="primary", use_container_width=True) and sym.strip():
            db.add_watch(uid, sym, kind)
            st.rerun()
    wl = db.get_watchlist(uid)
    if not wl:
        st.info("Add stocks or coins you want to follow.")
    else:
        rows = []
        for w in wl:
            q = market.stock(w["symbol"]) if w["kind"] == "stock" else market.crypto(w["symbol"])
            if q:
                chg = q.get("change")
                cur = "$" if w["kind"] == "crypto" else "₹"
                rows.append([f"<b>{escape(w['symbol'])}</b>", "Crypto" if w["kind"] == "crypto" else "NSE",
                             f"{cur}{q['price']:,.2f}",
                             f"<span class='{'good' if (chg or 0) >= 0 else 'bad'}'>{chg:+.2f}%</span>" if chg is not None else "—",
                             inr(q["price_inr"]) if q.get("price_inr") else "", escape(q["source"].split(" (")[0])])
            else:
                rows.append([f"<b>{escape(w['symbol'])}</b>", "Crypto" if w["kind"] == "crypto" else "NSE", "—", "—", "",
                             "not available"])
        ui.table(["Symbol", "Market", t("ltp"), "Change", "≈ in ₹", "Source"], rows, numeric=(2, 3, 4))
        with st.expander("🗑️ Remove"):
            opts = {f"{w['symbol']} ({w['kind']})": w for w in wl}
            pick = st.selectbox("Remove", list(opts), label_visibility="collapsed")
            if st.button(t("delete"), key="del_w"):
                db.remove_watch(uid, opts[pick]["symbol"], opts[pick]["kind"])
                st.rerun()
        st.caption("Use the Futures Risk Calculator before taking any trade on these.")

with tab_n:
    topic = st.radio("Topic", list(market.NEWS_FEEDS), horizontal=True, label_visibility="collapsed")
    news = market.news(topic)
    if news is None:
        st.warning("News could not be loaded. Check your internet connection and press Refresh.")
    elif not news:
        st.info("No headlines right now.")
    else:
        body = ui.rows([(f"<a href='{escape(n['link'])}' target='_blank' style='color:var(--ink);text-decoration:none'>"
                         f"<b>{escape(n['title'])}</b></a><div class='m'>{escape(n['source'])}</div>",
                         f"<span class='m'>{escape(n['time'])}</span>") for n in news])
        ui.card(f"📰 {topic}", body)
        st.caption("Headlines from Google News. Read the full article before acting; news is not advice.")
