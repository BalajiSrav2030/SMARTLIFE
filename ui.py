"""Small HTML building blocks so every page looks consistent in light and dark mode."""
from html import escape

import streamlit as st


def header(title, sub=""):
    st.markdown(f'<div class="sl-head"><h1>{escape(title)}</h1>'
                + (f"<p>{escape(sub)}</p>" if sub else "") + "</div>", unsafe_allow_html=True)


def kpis(items):
    """items: list of dicts {l, v, s?, cls?, hero?}"""
    html = "".join(
        f'<div class="sl-kpi{" hero" if it.get("hero") else ""}"><div class="l">{escape(it["l"])}</div>'
        f'<div class="v {it.get("cls", "")}">{escape(str(it["v"]))}</div>'
        + (f'<div class="s">{escape(it["s"])}</div>' if it.get("s") else "") + "</div>"
        for it in items)
    st.markdown(f'<div class="sl-kpis">{html}</div>', unsafe_allow_html=True)


def card(title, body_html):
    st.markdown(f'<div class="sl-card"><h3>{escape(title)}</h3>{body_html}</div>', unsafe_allow_html=True)


def rows(items):
    """items: list of (left_html, right_html) – caller escapes user text."""
    return "".join(f'<div class="sl-row"><span>{l}</span><span>{r}</span></div>' for l, r in items)


def pill(text, color="grey"):
    return f'<span class="pill {color}">{escape(text)}</span>'


def bar(pct, color=None):
    pct = max(0, min(100, pct))
    style = f"width:{pct:.0f}%" + (f";background:{color}" if color else "")
    return f'<div class="sl-bar"><i style="{style}"></i></div>'


def table(headers, data, numeric=()):
    """headers: list[str]; data: list[list[str]] (already escaped/formatted); numeric: column indexes."""
    th = "".join(f'<th class="{"n" if i in numeric else ""}">{escape(h)}</th>' for i, h in enumerate(headers))
    tr = "".join("<tr>" + "".join(f'<td class="{"n" if i in numeric else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>"
                 for r in data)
    st.markdown(f'<div class="sl-table"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>',
                unsafe_allow_html=True)
