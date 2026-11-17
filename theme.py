"""Light / dark theme for the whole app (custom CSS on top of Streamlit)."""
import streamlit as st

PALETTE = {
    "light": dict(bg="#f4f7f5", surface="#ffffff", sunk="#ecf1ee", line="#dbe4df", ink="#11231c", muted="#5d7068",
                  accent="#0e7a58", accent_ink="#ffffff", accent_soft="#dcf0e7", gold="#b07d12",
                  good="#12804e", bad="#c03a2b", warn="#a46a00", good_soft="#e0f3e8", bad_soft="#fbe5e1",
                  warn_soft="#fbf0d8", hero="#0f2a20", hero_ink="#ffffff", hero_muted="#a9d9c4",
                  side="#0f2a20", side_ink="#c3d8ce", side_on="#1c4434", field="#ffffff",
                  chart=["#0e7a58", "#2f6fd0", "#c48a16", "#c03a2b", "#7a5bd0", "#4f9a8f", "#d0732f", "#8a9a93"]),
    "dark": dict(bg="#0b1411", surface="#121f1a", sunk="#18271f", line="#253a30", ink="#e3eee8", muted="#93a99f",
                 accent="#34c592", accent_ink="#05261a", accent_soft="#143a2c", gold="#e2b24e",
                 good="#4dd08f", bad="#f27b6f", warn="#f0b54e", good_soft="#123323", bad_soft="#3a1c19",
                 warn_soft="#3a2c11", hero="#173b2e", hero_ink="#ffffff", hero_muted="#9fdcc2",
                 side="#070e0b", side_ink="#a7bdb2", side_on="#173027", field="#0f1a16",
                 chart=["#34c592", "#6aa1f0", "#e2b24e", "#f27b6f", "#a991f0", "#7fb3aa", "#f0a06a", "#7d8e87"]),
}


def mode() -> str:
    return "dark" if st.session_state.get("dark") else "light"


def P() -> dict:
    return PALETTE[mode()]


def plotly_layout(**extra):
    p = P()
    base = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=p["muted"], family="Manrope, -apple-system, sans-serif", size=12),
                colorway=p["chart"], margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor=p["line"], zerolinecolor=p["line"]),
                yaxis=dict(gridcolor=p["line"], zerolinecolor=p["line"]),
                legend=dict(orientation="h", y=-0.18, font=dict(color=p["muted"])),
                hoverlabel=dict(bgcolor=p["surface"], font_color=p["ink"]))
    base.update(extra)
    return base


def apply():
    p = P()
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@500;600;700&display=swap');
:root {{
  --bg:{p['bg']}; --surface:{p['surface']}; --sunk:{p['sunk']}; --line:{p['line']}; --ink:{p['ink']}; --muted:{p['muted']};
  --accent:{p['accent']}; --accent-ink:{p['accent_ink']}; --accent-soft:{p['accent_soft']}; --gold:{p['gold']};
  --good:{p['good']}; --bad:{p['bad']}; --warn:{p['warn']}; --good-soft:{p['good_soft']}; --bad-soft:{p['bad_soft']}; --warn-soft:{p['warn_soft']};
  --hero:{p['hero']}; --hero-ink:{p['hero_ink']}; --hero-muted:{p['hero_muted']};
  --side:{p['side']}; --side-ink:{p['side_ink']}; --side-on:{p['side_on']}; --field:{p['field']};
  --body: 'Manrope', -apple-system, 'Noto Sans Tamil', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Kannada', 'Noto Sans Malayalam', sans-serif;
  --display: 'Sora', 'Manrope', -apple-system, 'Noto Sans Tamil', 'Noto Sans Devanagari', sans-serif;
}}
html, body, .stApp, [data-testid="stAppViewContainer"] {{ background: var(--bg) !important; color: var(--ink); font-family: var(--body); }}
[data-testid="stHeader"] {{ background: transparent !important; }}
.stAppDeployButton, [data-testid="stStatusWidget"] {{ display: none !important; }}
[data-testid="stMainBlockContainer"], .block-container {{ padding-top: 2.2rem !important; max-width: 1180px; }}
.stApp p, .stApp li, .stApp label, .stMarkdown, [data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"] {{ color: var(--ink); font-family: var(--body); }}
[data-testid="stCaptionContainer"], .stApp small {{ color: var(--muted) !important; }}
.stApp h1, .stApp h2, .stApp h3 {{ font-family: var(--display); color: var(--ink); letter-spacing: -0.02em; }}

/* sidebar */
[data-testid="stSidebar"] {{ background: var(--side) !important; border-right: 0; }}
[data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{ color: var(--side-ink) !important; }}
[data-testid="stSidebarNav"] a span {{ color: var(--side-ink) !important; font-weight: 500; }}
[data-testid="stSidebarNav"] a {{ border-radius: 10px; padding: 6px 10px; }}
[data-testid="stSidebarNav"] a:hover {{ background: var(--side-on); }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{ background: var(--side-on); box-shadow: inset 3px 0 0 #34c592; }}
[data-testid="stSidebarNav"] a[aria-current="page"] span {{ color: #fff !important; font-weight: 700; }}
[data-testid="stSidebarNavSeparator"], [data-testid="stSidebar"] hr {{ border-color: var(--side-on) !important; }}
[data-testid="stNavSectionHeader"] {{ color: #7fa596 !important; text-transform: uppercase; letter-spacing: .08em; font-size: 11px !important; }}
[data-testid="stSidebar"] [data-baseweb="select"], [data-testid="stSidebar"] [data-baseweb="select"] * {{ background: var(--side-on) !important; border-color: var(--side-on) !important; color: #fff !important; -webkit-text-fill-color: #fff; }}
[data-testid="stSidebar"] .stButton button {{ background: transparent !important; border: 1px solid var(--side-on) !important; color: var(--side-ink) !important; }}

/* inputs (Streamlit 1.4x+ test ids, plus older baseweb fallbacks) */
[data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"], [data-testid="stDateInputField"],
[data-testid="stTextAreaRootElement"], [data-testid="stSelectbox"] [role="group"], [data-testid="stMultiSelect"] [role="group"],
[data-testid="stTimeInput"] [role="group"],
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {{
  background: var(--field) !important; border: 1px solid var(--line) !important; border-radius: 10px !important; }}
[data-testid="stNumberInputContainer"] [data-testid="stTextInputRootElement"], [data-baseweb="input"] [data-baseweb="base-input"] {{ border: 0 !important; }}
.stApp input, .stApp textarea {{ background: transparent !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink); caret-color: var(--ink); }}
.stApp input::placeholder, .stApp textarea::placeholder {{ color: var(--muted) !important; -webkit-text-fill-color: var(--muted); opacity: .8; }}
[data-testid="stSelectbox"] [role="group"] *, [data-baseweb="select"] div {{ color: var(--ink) !important; }}
[data-testid="stTextInputRootElement"]:focus-within, [data-testid="stNumberInputContainer"]:focus-within, [data-testid="stSelectbox"] [role="group"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within, [data-testid="stDateInputField"]:focus-within {{ border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft); }}
[data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] {{ background: var(--sunk) !important; color: var(--ink) !important; }}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="group"] {{ background: var(--side-on) !important; border-color: var(--side-on) !important; }}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="group"] * {{ color: #fff !important; -webkit-text-fill-color: #fff; }}
[role="listbox"], [role="listbox"] [role="option"], [data-testid="stSelectboxVirtualDropdown"] {{ background: var(--surface) !important; color: var(--ink) !important; }}
[role="listbox"] [role="option"]:hover, [role="listbox"] [role="option"][aria-selected="true"] {{ background: var(--accent-soft) !important; }}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"], [data-baseweb="calendar"], [data-baseweb="calendar"] * {{
  background-color: var(--surface) !important; color: var(--ink) !important; }}
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] {{ background-color: var(--accent-soft) !important; }}
[data-testid="stFileUploaderDropzone"] {{ background: var(--field) !important; border: 1px dashed var(--line) !important; }}
[data-testid="stFileUploaderDropzone"] * {{ color: var(--muted) !important; }}

/* buttons */
.stButton button, .stFormSubmitButton button, .stDownloadButton button {{
  border-radius: 10px !important; font-weight: 600 !important; border: 1px solid var(--line) !important;
  background: var(--surface) !important; color: var(--ink) !important; }}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primaryFormSubmit"], .stFormSubmitButton button {{
  background: var(--accent) !important; color: var(--accent-ink) !important; border-color: var(--accent) !important; }}
.stButton button p, .stFormSubmitButton button p {{ color: inherit !important; }}

/* tabs, expanders, forms */
[role="tablist"] {{ gap: 4px; background: var(--sunk); padding: 4px; border-radius: 12px; width: fit-content; max-width: 100%; flex-wrap: wrap; }}
[role="tab"] {{ border-radius: 9px !important; padding: 6px 14px !important; background: transparent !important; }}
[role="tab"] p {{ color: var(--muted) !important; font-weight: 600; }}
[role="tab"][aria-selected="true"] {{ background: var(--surface) !important; box-shadow: 0 1px 3px rgba(0,0,0,.12); }}
[role="tab"][aria-selected="true"] p {{ color: var(--ink) !important; }}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"], [role="tablist"] + div[aria-hidden], .stTabs [data-baseweb="tab-border"] {{ display: none !important; }}
.stTabs [role="tablist"] {{ border-bottom: 0 !important; }}
[data-testid="stExpander"] details, [data-testid="stForm"] {{ background: var(--surface); border: 1px solid var(--line) !important; border-radius: 14px !important; }}
[data-testid="stExpander"] summary {{ background: var(--surface) !important; border-radius: 14px; }}
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {{ font-weight: 700; color: var(--ink) !important; }}
[data-testid="stExpanderDetails"] {{ background: var(--surface) !important; }}
[data-testid="stPopoverBody"], [data-testid="stPopover"] button {{ background: var(--surface) !important; color: var(--ink) !important; }}
[data-testid="stAlert"] {{ border-radius: 12px; }}
.stRadio label p, .stCheckbox label p, .stToggle label p {{ color: var(--ink) !important; }}
[data-testid="stSidebar"] .stToggle label p, [data-testid="stSidebar"] label p, [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{ color: var(--side-ink) !important; }}
[data-testid="stDateInputField"] *, [data-testid="stDateInputField"] input {{ color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; }}
[data-testid="stSlider"] div[data-testid="stTickBarMin"], [data-testid="stSlider"] div[data-testid="stTickBarMax"] {{ color: var(--muted); }}

/* our components */
.sl-head h1 {{ font-size: 30px; margin: 0 0 4px; line-height: 1.2; }}
.sl-head p {{ color: var(--muted); margin: 0 0 6px; font-size: 15px; }}
.sl-kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 6px 0 14px; }}
.sl-kpi {{ background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 14px 16px; min-width: 0; }}
.sl-kpi.hero {{ background: var(--hero); border-color: var(--hero); }}
.sl-kpi .l {{ font-size: 11.5px; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); font-weight: 700; }}
.sl-kpi.hero .l {{ color: var(--hero-muted); }}
.sl-kpi .v {{ font-family: var(--display); font-size: 24px; font-weight: 600; margin-top: 4px; color: var(--ink); font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }}
.sl-kpi.hero .v {{ color: var(--hero-ink); }}
.sl-kpi .s {{ font-size: 12.5px; color: var(--muted); margin-top: 2px; }}
.sl-kpi.hero .s {{ color: var(--hero-muted); }}
.sl-kpi .v.good, .good {{ color: var(--good) !important; }} .sl-kpi .v.bad, .bad {{ color: var(--bad) !important; }}
.sl-card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; margin-bottom: 12px; }}
.sl-card h3 {{ font-size: 16px; margin: 0 0 10px; }}
.sl-row {{ display: flex; justify-content: space-between; gap: 12px; align-items: center; padding: 9px 0; border-bottom: 1px solid var(--line); font-size: 14.5px; color: var(--ink); }}
.sl-row:last-child {{ border-bottom: 0; }}
.sl-row .m {{ color: var(--muted); font-size: 12.5px; }}
.pill {{ font-size: 11.5px; font-weight: 700; padding: 2px 10px; border-radius: 99px; white-space: nowrap; }}
.pill.green {{ background: var(--good-soft); color: var(--good); }} .pill.red {{ background: var(--bad-soft); color: var(--bad); }}
.pill.amber {{ background: var(--warn-soft); color: var(--warn); }} .pill.grey {{ background: var(--sunk); color: var(--muted); }}
.sl-bar {{ height: 8px; background: var(--sunk); border-radius: 8px; overflow: hidden; margin: 6px 0 12px; }}
.sl-bar i {{ display: block; height: 100%; background: var(--accent); border-radius: 8px; }}
.sl-table {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; margin-bottom: 12px; }}
.sl-table table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.sl-table th {{ text-align: left; color: var(--muted); font-size: 11.5px; text-transform: uppercase; letter-spacing: .06em; padding: 10px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
.sl-table td {{ padding: 9px 12px; border-bottom: 1px solid var(--line); color: var(--ink); white-space: nowrap; }}
.sl-table tr:last-child td {{ border-bottom: 0; }}
.sl-table td.n, .sl-table th.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.sl-price {{ display: flex; gap: 14px; align-items: baseline; flex-wrap: wrap; background: var(--accent-soft); border-radius: 14px; padding: 12px 16px; margin: 6px 0 10px; }}
.sl-price b {{ font-family: var(--display); font-size: 26px; color: var(--ink); }}
.sl-price span {{ color: var(--muted); font-size: 13px; }}
.sl-formula {{ font-family: ui-monospace, Menlo, monospace; font-size: 12.5px; color: var(--muted); background: var(--sunk); border-radius: 10px; padding: 10px 12px; line-height: 1.6; }}
.sl-brand {{ font-family: var(--display); font-weight: 700; font-size: 24px; color: #fff !important; letter-spacing: -0.02em; }}
.sl-brand b {{ color: #34c592 !important; }}
.sl-lesson h4 {{ font-family: var(--display); margin: 14px 0 6px; color: var(--ink); }}
.sl-lesson p, .sl-lesson li {{ line-height: 1.65; color: var(--ink); }}
.sl-term {{ display: inline-block; background: var(--sunk); border-radius: 8px; padding: 2px 8px; margin: 2px 4px 2px 0; font-size: 13px; color: var(--ink); }}
</style>""", unsafe_allow_html=True)
