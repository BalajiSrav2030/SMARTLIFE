"""Live prices.
Crypto: CoinGecko (free, no key) with Binance as fallback.
Indian stocks / indices / forex: Yahoo Finance via yfinance (NSE/BSE quotes can be delayed).
Every function returns a dict or None – the UI falls back to manual entry on None."""
from datetime import datetime

import requests
import streamlit as st

UA = {"User-Agent": "SmartLife-college-project/1.0"}

INDEX_ALIASES = {
    "NIFTY": "^NSEI", "NIFTY50": "^NSEI", "NIFTY 50": "^NSEI", "BANKNIFTY": "^NSEBANK", "NIFTY BANK": "^NSEBANK",
    "SENSEX": "^BSESN", "FINNIFTY": "NIFTY_FIN_SERVICE.NS", "MIDCPNIFTY": "^NSEMDCP50",
}


def _now():
    return datetime.now().strftime("%d %b %Y, %I:%M %p")


@st.cache_data(ttl=60, show_spinner=False)
def crypto(query: str):
    q = query.strip()
    if not q:
        return None
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search", params={"query": q}, headers=UA, timeout=6)
        coins = r.json().get("coins", []) if r.ok else []
        coin = next((c for c in coins if c["symbol"].lower() == q.lower()), coins[0] if coins else None)
        if coin:
            p = requests.get("https://api.coingecko.com/api/v3/simple/price",
                             params={"ids": coin["id"], "vs_currencies": "usd,inr", "include_24hr_change": "true"},
                             headers=UA, timeout=6).json().get(coin["id"], {})
            if "usd" in p:
                return {"name": coin["name"], "symbol": coin["symbol"].upper(), "price": p["usd"],
                        "price_inr": p.get("inr"), "change": p.get("usd_24h_change"),
                        "source": "CoinGecko", "time": _now()}
    except (requests.RequestException, ValueError, KeyError):
        pass
    try:  # fallback: Binance spot ticker
        sym = q.upper().replace("/", "").replace("-", "")
        sym = sym if sym.endswith("USDT") else sym + "USDT"
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", params={"symbol": sym}, headers=UA, timeout=6)
        if r.ok:
            d = r.json()
            return {"name": sym, "symbol": sym, "price": float(d["lastPrice"]), "price_inr": None,
                    "change": float(d["priceChangePercent"]), "source": "Binance", "time": _now()}
    except (requests.RequestException, ValueError, KeyError):
        pass
    return None


def _yahoo(symbol: str):
    import yfinance as yf
    t = yf.Ticker(symbol)
    hist = t.history(period="5d", interval="1d")
    if hist is None or hist.empty:
        return None
    last = float(hist["Close"].iloc[-1])
    prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else None
    return last, prev


@st.cache_data(ttl=60, show_spinner=False)
def stock(query: str):
    q = query.strip().upper()
    if not q:
        return None
    candidates = [INDEX_ALIASES[q]] if q in INDEX_ALIASES else (
        [q] if "." in q or q.startswith("^") else [f"{q}.NS", f"{q}.BO"])
    for sym in candidates:
        try:
            res = _yahoo(sym)
        except Exception:  # network / parsing issues inside yfinance
            res = None
        if res:
            last, prev = res
            return {"name": q, "symbol": sym, "price": last,
                    "change": (last - prev) / prev * 100 if prev else None,
                    "source": "Yahoo Finance (NSE/BSE may be delayed)", "time": _now()}
    return None


@st.cache_data(ttl=60, show_spinner=False)
def forex(pair: str):
    p = pair.strip().upper().replace("/", "").replace(" ", "")
    if len(p) != 6:
        return None
    try:
        res = _yahoo(f"{p}=X")
    except Exception:
        res = None
    if not res:
        return None
    last, prev = res
    return {"name": f"{p[:3]}/{p[3:]}", "symbol": p, "price": last,
            "change": (last - prev) / prev * 100 if prev else None, "source": "Yahoo Finance", "time": _now()}


NEWS_FEEDS = {
    "India markets": "https://news.google.com/rss/search?q=stock+market+india+sensex+nifty&hl=en-IN&gl=IN&ceid=IN:en",
    "Personal finance": "https://news.google.com/rss/search?q=personal+finance+india+mutual+funds+tax&hl=en-IN&gl=IN&ceid=IN:en",
    "Crypto": "https://news.google.com/rss/search?q=bitcoin+crypto+india&hl=en-IN&gl=IN&ceid=IN:en",
}


@st.cache_data(ttl=600, show_spinner=False)
def news(topic: str, limit: int = 12):
    """Latest headlines from Google News RSS. Returns a list of dicts or None when offline."""
    import xml.etree.ElementTree as ET
    from email.utils import parsedate_to_datetime
    url = NEWS_FEEDS.get(topic)
    if not url:
        return None
    try:
        r = requests.get(url, headers=UA, timeout=8)
        r.raise_for_status()
        root = ET.fromstring(r.content)
    except (requests.RequestException, ET.ParseError):
        return None
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        src = (it.findtext("source") or "").strip()
        try:
            when = parsedate_to_datetime(it.findtext("pubDate") or "").strftime("%d %b, %I:%M %p")
        except (TypeError, ValueError):
            when = ""
        if src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        if title and link.startswith("http"):
            items.append({"title": title, "link": link, "source": src, "time": when})
        if len(items) >= limit:
            break
    return items
