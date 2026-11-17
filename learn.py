"""Learn: stock market, mutual funds, F&O, crypto, forex, TA, risk, personal finance + quizzes."""
from html import escape

import streamlit as st

import auth
import db
import ui
from i18n import t
from lessons import LESSONS

user = auth.current_user()
uid = user["id"]
ui.header(t("learn"), "Short lessons with a quiz at the end. General education, not investment advice.")
st.caption(t("lesson_lang_note"))

prog = db.get_progress(uid)
done = len(prog)
ui.kpis([{"l": t("lessons"), "v": len(LESSONS)}, {"l": t("completed"), "v": done, "cls": "good"},
         {"l": t("progress"), "v": f"{done / len(LESSONS) * 100:.0f}%", "hero": True}])

ids = [l["id"] for l in LESSONS]
sel = st.session_state.get("lesson") or ids[0]
cols = st.columns(4)
for i, l in enumerate(LESSONS):
    p = prog.get(l["id"])
    badge = f" ✅ {p['score']}/{p['total']}" if p else ""
    if cols[i % 4].button(f"{l['icon']} {l['title']}{badge}", key=f"ls_{l['id']}", use_container_width=True,
                          type="primary" if l["id"] == sel else "secondary"):
        st.session_state.lesson = l["id"]
        st.rerun()

L = next(l for l in LESSONS if l["id"] == sel)
body = "".join(f"<h4>{escape(h)}</h4><p>{txt}</p>" if not txt.startswith("<ul") else f"<h4>{escape(h)}</h4>{txt}"
               for h, txt in L["sections"])
terms = "".join(f"<span class='sl-term'>{escape(x)}</span>" for x in L["terms"])
st.markdown(f"<div class='sl-card sl-lesson'><div class='m'>{L['level']} · {L['minutes']} min</div>"
            f"<h3 style='font-size:22px;margin:4px 0 0'>{L['icon']} {escape(L['title'])}</h3>{body}"
            f"<h4>Key terms</h4>{terms}</div>", unsafe_allow_html=True)

st.markdown(f"#### 📝 {t('quiz')}")
with st.form(f"quiz_{sel}"):
    answers = [st.radio(f"{n}. {q}", opts, index=None, key=f"q_{sel}_{n}") for n, (q, opts, _, _) in enumerate(L["quiz"], 1)]
    submitted = st.form_submit_button(t("check"), type="primary")
if submitted:
    if None in answers:
        st.warning("Answer all questions first.")
    else:
        score = 0
        for n, ((q, opts, ans, why), a) in enumerate(zip(L["quiz"], answers), 1):
            ok = opts.index(a) == ans
            score += ok
            (st.success if ok else st.error)(f"{n}. {'Correct' if ok else 'Answer: ' + opts[ans]} · {why}")
        db.save_progress(uid, sel, score, len(L["quiz"]))
        if score == len(L["quiz"]):
            st.balloons()
        st.info(f"Score: {score}/{len(L['quiz'])}")
        nxt = ids[(ids.index(sel) + 1) % len(ids)]
        st.button(f"Next lesson → {next(l['title'] for l in LESSONS if l['id'] == nxt)}",
                  on_click=lambda: st.session_state.update(lesson=nxt))
