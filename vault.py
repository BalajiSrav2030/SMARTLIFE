"""Legacy Vault: encrypted records + verified nominee access."""
from html import escape

import streamlit as st

import auth
import db
import ui
import vault_crypto
from i18n import t

user = auth.current_user()
uid = user["id"]
ui.header(t("vault"), t("vault_sub"))

TYPES = ["Bank account", "Demat / trading", "Mutual fund folio", "Insurance policy", "Property document",
         "Loan", "Will / legal", "Digital account", "Other"]
items = db.list_rows("vault_items", uid)
fam = [f for f in db.list_rows("family", uid) if f["is_nominee"]]
codes = db.vault_codes(uid)
settings = db.get_vault_settings(uid)

ui.kpis([{"l": "Records", "v": len(items)}, {"l": "Shared with nominees", "v": sum(i["visible"] for i in items)},
         {"l": "Nominees with access code", "v": f"{sum(1 for f in fam if f['id'] in codes)} / {len(fam)}"},
         {"l": "Status", "v": "Released" if settings["released"] else "Locked", "cls": "bad" if settings["released"] else "good"}])

st.markdown("<div class='sl-card'><b>🔒 How your data is protected</b><ul class='m' style='margin:6px 0 0'>"
            "<li>Notes and documents are encrypted (Fernet / AES) before saving.</li>"
            "<li>Only the last 4 digits of any account number are stored; never store full numbers, PINs, OTPs or passwords.</li>"
            "<li>Nominees need your email, their own email and a one-time access code. Codes are stored only as salted hashes.</li>"
            "<li>The vault opens to nominees only after you release it, or after you have not logged in for the set number of days.</li>"
            "</ul></div>", unsafe_allow_html=True)

tab_r, tab_a = st.tabs(["🗂️ Records", "🔑 Nominee access"])

with tab_r:
    with st.expander("➕ " + t("add_new"), expanded=not items):
        with st.form("vault_add", clear_on_submit=True, border=False):
            c1, c2 = st.columns(2)
            title = c1.text_input("Title", placeholder="e.g. SBI savings account", max_chars=80)
            itype = c2.selectbox(t("type"), TYPES)
            c3, c4 = st.columns(2)
            inst = c3.text_input(t("institution"), max_chars=80)
            last4 = c4.text_input("Reference – " + t("last4"), max_chars=4)
            notes = st.text_area(t("private_notes"), placeholder="Branch, RM contact, where the papers are kept, instructions for family…",
                                 max_chars=2000, height=110)
            f = st.file_uploader(t("attach"), type=["pdf", "png", "jpg", "jpeg"])
            visible = st.checkbox(t("visible_to"), value=True)
            if st.form_submit_button(t("save"), type="primary"):
                if not title.strip():
                    st.error("Title")
                elif last4 and not (last4.isdigit() and len(last4) == 4):
                    st.error("Only the last 4 digits, please. Full numbers are not stored.")
                elif f is not None and f.size > 5 * 1024 * 1024:
                    st.error("File must be under 5 MB.")
                else:
                    db.add_row("vault_items", uid, title=title.strip(), itype=itype, institution=inst.strip(), last4=last4,
                               notes_enc=vault_crypto.encrypt(notes.strip()),
                               file_name=f.name if f else None, file_enc=vault_crypto.encrypt(f.getvalue()) if f else None,
                               visible=int(visible))
                    st.rerun()
    for it in items:
        with st.expander(f"{'👁️' if it['visible'] else '🙈'}  {it['title']} · {it['itype']}"):
            st.markdown(f"**{t('institution')}:** {escape(it['institution'] or '—')} &nbsp;·&nbsp; **Ref:** XXXX{escape(it['last4'] or '')}",
                        unsafe_allow_html=True)
            notes = vault_crypto.decrypt(it["notes_enc"])
            if notes:
                st.text(notes.decode())
            c1, c2, c3 = st.columns(3)
            if it["file_enc"]:
                c1.download_button(f"⬇ {it['file_name']}", vault_crypto.decrypt(it["file_enc"]), file_name=it["file_name"],
                                   key=f"dl{it['id']}")
            if c2.button("Hide from nominees" if it["visible"] else "Share with nominees", key=f"vis{it['id']}"):
                db.update_row("vault_items", uid, it["id"], visible=0 if it["visible"] else 1)
                st.rerun()
            if c3.button(t("delete"), key=f"vd{it['id']}"):
                db.delete_row("vault_items", uid, it["id"])
                st.rerun()

with tab_a:
    st.markdown(f"#### {t('release_rule')}")
    c1, c2 = st.columns(2)
    days = c1.number_input(t("inactivity"), 30, 3650, int(settings["inactivity_days"]), step=30)
    released = c2.toggle("Release vault to nominees now", value=bool(settings["released"]))
    if st.button(t("save"), type="primary", key="save_rule"):
        db.save_vault_settings(uid, days, released)
        st.toast(t("saved") + " ✅")
        st.rerun()

    st.markdown(f"#### {t('access_code')}")
    if not fam:
        st.info("Add nominees with an email on the Family & Nominees page first.")
    for f in fam:
        c1, c2 = st.columns([3, 1])
        has = f["id"] in codes
        when = codes[f["id"]]["created_at"][:10] if has else ""
        c1.markdown(f"**{escape(f['name'])}** ({escape(f['relation'])}) · {escape(f['email'] or 'no email')}  "
                    + (ui.pill(f"code set {when}", "green") if has else ui.pill("no code", "amber")), unsafe_allow_html=True)
        if c2.button("New code" if has else t("gen_code"), key=f"code{f['id']}", disabled=not f["email"]):
            code = vault_crypto.new_code()
            db.set_vault_code(uid, f["id"], vault_crypto.hash_code(code))
            st.session_state[f"shown_code_{f['id']}"] = code
            st.rerun()
        shown = st.session_state.pop(f"shown_code_{f['id']}", None)
        if shown:
            st.success(f"Access code for {f['name']}: **{shown}** · Write it down and give it to them privately. "
                       "It will not be shown again.")
    st.caption("Nominees open the vault from the login screen → 'Nominee access'.")
