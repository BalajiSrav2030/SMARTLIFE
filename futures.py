"""Futures Risk Calculator with live prices: Crypto, Indian stocks/F&O, Forex."""
import math

import plotly.graph_objects as go
import streamlit as st

import finance
import market
import theme
import ui
from i18n import t
from utils import inr

P = theme.P()
ui.header(t("futures"), t("fut_sub"))


def live_price_box(prefix, fetch, placeholder, help_text):
    """Search box + Get price button. Fills the entry field via session_state."""
    c1, c2 = st.columns([3, 1])
    q = c1.text_input(t("search_symbol"), placeholder=placeholder, key=f"{prefix}_q", help=help_text)
    c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if c2.button(t("get_price"), key=f"{prefix}_go", type="primary", use_container_width=True) and q.strip():
        with st.spinner("…"):
            st.session_state[f"{prefix}_quote"] = fetch(q) or {"error": True}
    quote = st.session_state.get(f"{prefix}_quote")
    if quote and quote.get("error"):
        st.warning(t("price_fail"))
    elif quote:
        cur = "$" if prefix in ("cr",) else ("" if prefix == "fx" else "₹")
        chg = quote.get("change")
        chg_html = (f"<span class='{'good' if chg >= 0 else 'bad'}'>{chg:+.2f}% (24h)</span>" if chg is not None and prefix == "cr"
                    else f"<span class='{'good' if chg >= 0 else 'bad'}'>{chg:+.2f}%</span>" if chg is not None else "")
        inr_txt = f" · ≈ {inr(quote['price_inr'])}" if quote.get("price_inr") else ""
        st.markdown(f"<div class='sl-price'><span>{t('ltp')} · <b style='font-size:15px'>{quote['name']}</b></span>"
                    f"<b>{cur}{quote['price']:,.4f}".rstrip("0").rstrip(".") + f"</b>{chg_html}"
                    f"<span>{inr_txt} · {quote['source']} · {quote['time']}</span></div>", unsafe_allow_html=True)

        def use():
            price = float(quote["price"])
            st.session_state[f"{prefix}_entry"] = price
            for sd in ("long", "short"):
                seed_levels(prefix, sd, price, force=True)
        st.button("↳ " + t("use_as_entry"), key=f"{prefix}_use", on_click=use)


PCT = {"cr": (0.02, 0.06), "st": (0.01, 0.03)}


def seed_levels(prefix, side, entry, force=False):
    """Default stop-loss / target around the entry price."""
    if prefix == "fx":
        pair = st.session_state.get("fx_pair", "USDINR").upper()
        pip = 0.01 if "JPY" in pair else (0.0025 if pair.endswith("INR") else 0.0001)
        d_sl, d_tp = 40 * pip, 100 * pip
    else:
        d_sl, d_tp = entry * PCT[prefix][0], entry * PCT[prefix][1]
    sgn = 1 if side == "long" else -1
    for key, v in ((f"{prefix}_sl_{side}", entry - sgn * d_sl), (f"{prefix}_tp_{side}", entry + sgn * d_tp)):
        if force or key not in st.session_state:
            st.session_state[key] = round(v, 4)


def side_picker(prefix):
    return st.radio(" ", ["long", "short"], horizontal=True, format_func=t, key=f"{prefix}_side", label_visibility="collapsed")


def levels_chart(levels, prefix_sym):
    fig = go.Figure()
    for name, price, color in levels:
        fig.add_hline(y=price, line_color=color, line_width=2.5,
                      annotation=dict(text=f"<b>{name}</b> {prefix_sym}{price:,.2f}", font=dict(color=color, size=12)),
                      annotation_position="right")
    prices = [p for _, p, _ in levels]
    pad = (max(prices) - min(prices)) * 0.18 or 1
    fig.update_layout(**theme.plotly_layout(height=300, showlegend=False, margin=dict(t=10, b=10, l=10, r=190),
                                            yaxis=dict(range=[min(prices) - pad, max(prices) + pad], tickprefix=prefix_sym,
                                                       gridcolor=P["line"]),
                                            xaxis=dict(visible=False)))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def checks(items):
    ui.card(t("risk_check"), ui.rows([(f"{'✅' if ok else '❌'} {label}", ui.pill(good if ok else bad, "green" if ok else "red"))
                                      for ok, label, good, bad in items]))


def valid(side, e, sl, tp):
    return (sl < e < tp) if side == "long" else (tp < e < sl)


tab_c, tab_s, tab_f = st.tabs(["🪙 " + t("crypto"), "🇮🇳 " + t("stocks_fno"), "💱 " + t("forex")])

# ======================= CRYPTO =======================
with tab_c:
    live_price_box("cr", market.crypto, "BTC, ETH, SOL, bitcoin…", "CoinGecko (Binance fallback)")
    st.session_state.setdefault("cr_entry", 70000.0)
    left, right = st.columns([1, 2], gap="large")
    with left:
        side = side_picker("cr")
        cap = st.number_input(t("capital") + " ($)", 10.0, 1e9, 1000.0, step=100.0)
        rp = st.number_input(t("risk_pct"), 0.1, 100.0, 2.0, step=0.5, key="cr_rp")
        e = st.number_input(t("entry") + " ($)", 0.0, 1e9, step=10.0, format="%.4f", key="cr_entry")
        seed_levels("cr", side, e)
        sl = st.number_input(t("stop_loss") + " ($)", 0.0, 1e9, step=10.0, format="%.4f", key=f"cr_sl_{side}")
        tp = st.number_input(t("target") + " ($)", 0.0, 1e9, step=10.0, format="%.4f", key=f"cr_tp_{side}")
        lev = st.slider(t("leverage"), 1, 125, 10)
        mmr = st.number_input("Maintenance margin (%)", 0.0, 10.0, 0.5, step=0.1, help="Differs by exchange and position size.")
    with right:
        if not (e > 0 and valid(side, e, sl, tp)):
            st.error("LONG: stop-loss < entry < target · SHORT: target < entry < stop-loss")
        else:
            r = finance.crypto_futures(cap, rp, e, sl, tp, lev, side, mmr)
            ui.kpis([{"l": t("position_size"), "v": f"${r['notional']:,.0f}", "s": f"{r['qty']:.6f} coins"},
                     {"l": t("margin_needed"), "v": f"${r['margin']:,.2f}", "s": f"{r['margin'] / cap * 100:.0f}% of capital"},
                     {"l": t("max_loss"), "v": f"−${r['risk_amt']:,.2f}", "cls": "bad"},
                     {"l": t("profit_target"), "v": f"+${r['reward']:,.2f}", "s": f"R:R 1 : {r['rr']:.1f}", "cls": "good"}])
            levels_chart([(t("target"), tp, P["good"]), (t("entry"), e, P["ink"]), (t("stop_loss"), sl, P["bad"]),
                          (t("liquidation"), r["liq"], P["chart"][4])], "$")
            checks([(rp <= 2, "Risk ≤ 2%", "Safe", "Risky"), (r["rr"] >= 2, "Risk : Reward ≥ 1 : 2", "Good", "Weak"),
                    (r["sl_safe"], "Stop-loss before liquidation", "Safe", "Danger"),
                    (r["margin_ok"], "Margin within capital", "OK", "Too big"), (lev <= 10, f"Leverage {lev}x ≤ 10x", "OK", "High")])
            st.markdown(f"<div class='sl-formula'>{t('liquidation')} ≈ ${r['liq']:,.2f} = Entry × (1 {'−' if side == 'long' else '+'} 1/Leverage "
                        f"{'+' if side == 'long' else '−'} MMR) · isolated margin, fees & funding not included</div>", unsafe_allow_html=True)

# ======================= INDIAN STOCKS / F&O =======================
with tab_s:
    live_price_box("st", market.stock, "RELIANCE, TCS, HDFCBANK, NIFTY, BANKNIFTY…", "NSE symbol. Yahoo Finance, may be delayed.")
    st.session_state.setdefault("st_entry", 2500.0)
    mode = st.radio(" ", ["F&O futures (lots)", "Cash / intraday (shares)"], horizontal=True, label_visibility="collapsed")
    left, right = st.columns([1, 2], gap="large")
    with left:
        side = side_picker("st")
        cap = st.number_input(t("capital") + " (₹)", 1000.0, 1e11, 5_00_000.0, step=10_000.0)
        rp = st.number_input(t("risk_pct"), 0.1, 100.0, 2.0, step=0.5, key="st_rp")
        e = st.number_input(t("entry") + " (₹)", 0.0, 1e8, step=1.0, key="st_entry")
        seed_levels("st", side, e)
        sl = st.number_input(t("stop_loss") + " (₹)", 0.0, 1e8, key=f"st_sl_{side}")
        tp = st.number_input(t("target") + " (₹)", 0.0, 1e8, key=f"st_tp_{side}")
        if mode.startswith("F&O"):
            lot = st.number_input(t("lot_size"), 1, 1_000_000, value=None, placeholder="Check on NSE")
            mpl = st.number_input(t("margin_per_lot"), 1.0, 1e9, value=None, placeholder="Check with your broker")
            st.caption("Lot size and margin change often. Check NSE / your broker before trading.")
    with right:
        if not (e > 0 and valid(side, e, sl, tp)):
            st.error("LONG: stop-loss < entry < target · SHORT: target < entry < stop-loss")
        elif mode.startswith("F&O") and (lot is None or mpl is None):
            st.info(f"{t('lot_size')} + {t('margin_per_lot')} ←")
        elif mode.startswith("F&O"):
            r = finance.fno_futures(cap, rp, e, sl, tp, int(lot), mpl)
            ui.kpis([{"l": t("lots"), "v": r["lots"], "hero": True}, {"l": t("margin_needed"), "v": inr(r["margin"])},
                     {"l": t("max_loss"), "v": "−" + inr(r["max_loss"]), "cls": "bad"},
                     {"l": t("profit_target"), "v": "+" + inr(r["profit"]), "s": f"R:R 1 : {r['rr']:.1f}", "cls": "good"}])
            if r["lots"] == 0:
                st.error("Your risk budget cannot cover even one lot. Tighten the stop-loss or skip this trade.")
            levels_chart([(t("target"), tp, P["good"]), (t("entry"), e, P["ink"]), (t("stop_loss"), sl, P["bad"])], "₹")
            checks([(rp <= 2, "Risk ≤ 2%", "Safe", "Risky"), (r["rr"] >= 2, "Risk : Reward ≥ 1 : 2", "Good", "Weak"),
                    (r["margin"] <= cap * 0.5, "Margin ≤ 50% of capital", "OK", "High")])
            st.markdown(f"<div class='sl-formula'>Risk budget {inr(r['risk_amt'])} ÷ loss per lot {inr(r['loss_per_lot'])} = "
                        f"{r['lots_by_risk']} lots · capital allows {r['lots_by_margin']} · take the smaller</div>", unsafe_allow_html=True)
        else:
            risk_amt = cap * rp / 100
            per_share = abs(e - sl)
            qty = min(math.floor(risk_amt / per_share), math.floor(cap / e))
            ui.kpis([{"l": "Shares", "v": f"{qty:,}", "hero": True}, {"l": "Capital used", "v": inr(qty * e)},
                     {"l": t("max_loss"), "v": "−" + inr(qty * per_share), "cls": "bad"},
                     {"l": t("profit_target"), "v": "+" + inr(qty * abs(tp - e)), "s": f"R:R 1 : {abs(tp - e) / per_share:.1f}", "cls": "good"}])
            levels_chart([(t("target"), tp, P["good"]), (t("entry"), e, P["ink"]), (t("stop_loss"), sl, P["bad"])], "₹")
            checks([(rp <= 2, "Risk ≤ 2%", "Safe", "Risky"), (abs(tp - e) / per_share >= 2, "Risk : Reward ≥ 1 : 2", "Good", "Weak")])

# ======================= FOREX =======================
with tab_f:
    st.info("Indian residents may trade currency derivatives only on recognised Indian exchanges (NSE / BSE / MSE) in RBI-permitted pairs. "
            "Overseas online forex platforms are not permitted; check RBI's Alert List on rbi.org.in.")
    live_price_box("fx", market.forex, "USDINR, EURINR, EURUSD, GBPUSD…", "Yahoo Finance")
    st.session_state.setdefault("fx_entry", 84.0)
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.session_state.setdefault("fx_pair", "USDINR")
        pair = st.text_input("Pair", max_chars=7, key="fx_pair").upper().replace("/", "")
        side = side_picker("fx")
        inr_pair = pair.endswith("INR")
        contract = st.number_input("Contract size (units of base)", 1, 10_000_000, 1000 if inr_pair else 100_000,
                                   help="Indian exchange currency futures like USD/INR use 1,000 units. Check the exchange spec.")
        cap = st.number_input(t("capital") + (" (₹)" if inr_pair else f" ({pair[3:] or 'quote'})"), 100.0, 1e10, 2_00_000.0 if inr_pair else 10_000.0)
        rp = st.number_input(t("risk_pct"), 0.1, 100.0, 1.0, step=0.5, key="fx_rp")
        e = st.number_input(t("entry"), 0.0, 1e6, step=0.0025, format="%.4f", key="fx_entry")
        pip = 0.01 if "JPY" in pair else (0.0025 if inr_pair else 0.0001)
        seed_levels("fx", side, e)
        sl = st.number_input(t("stop_loss"), 0.0, 1e6, format="%.4f", key=f"fx_sl_{side}")
        tp = st.number_input(t("target"), 0.0, 1e6, format="%.4f", key=f"fx_tp_{side}")
        mpl = st.number_input("Margin per contract", 0.0, 1e9, 0.0, help="From your broker. Leave 0 to skip the margin check.")
    with right:
        if not (e > 0 and valid(side, e, sl, tp)):
            st.error("LONG: stop-loss < entry < target · SHORT: target < entry < stop-loss")
        else:
            risk_amt = cap * rp / 100
            loss_per_contract = abs(e - sl) * contract
            n = math.floor(risk_amt / loss_per_contract)
            if mpl > 0:
                n = min(n, math.floor(cap / mpl))
            ticks = abs(e - sl) / pip
            cur = "₹" if inr_pair else ""
            ui.kpis([{"l": "Contracts / lots", "v": n, "hero": True},
                     {"l": "Stop distance", "v": f"{ticks:.0f} {'ticks' if inr_pair else 'pips'}"},
                     {"l": t("max_loss"), "v": f"−{cur}{n * loss_per_contract:,.2f}", "cls": "bad"},
                     {"l": t("profit_target"), "v": f"+{cur}{n * abs(tp - e) * contract:,.2f}",
                      "s": f"R:R 1 : {abs(tp - e) / abs(e - sl):.1f}", "cls": "good"}])
            if n == 0:
                st.error("Risk budget cannot cover one contract. Widen the budget or tighten the stop.")
            levels_chart([(t("target"), tp, P["good"]), (t("entry"), e, P["ink"]), (t("stop_loss"), sl, P["bad"])], cur)
            checks([(rp <= 2, "Risk ≤ 2%", "Safe", "Risky"), (abs(tp - e) / abs(e - sl) >= 2, "Risk : Reward ≥ 1 : 2", "Good", "Weak"),
                    (inr_pair, "INR pair on an Indian exchange", "Permitted", "Check RBI rules")])
            if not inr_pair:
                st.caption(f"Amounts are in the quote currency ({pair[3:]}). Pip = {pip}.")
