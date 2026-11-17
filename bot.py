"""SmartLife Telegram Bot.

Setup:
  1. Telegram la @BotFather → /newbot → token copy pannunga
  2. .env.example ah .env ah copy panni, TELEGRAM_BOT_TOKEN= la token podunga
  3. pip install -r requirements.txt
  4. python bot.py
"""
import logging
import os
import secrets
import warnings
from datetime import date, time
from html import escape
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

import bot_logic as L
import db
from sample_data import load_sample
from utils import inr

from telegram.warnings import PTBUserWarning

# Our conversation mixes buttons and typed answers on purpose; this warning does not apply.
warnings.filterwarnings("ignore", message=".*per_message=False.*", category=PTBUserWarning)

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("smartlife-bot")

IST = ZoneInfo("Asia/Kolkata")
HTML = ParseMode.HTML

MENU = ReplyKeyboardMarkup(
    [["📊 Dashboard", "➕ Add", "🧾 Recent"],
     ["💼 Holdings", "📈 Chart", "🔔 Reminders"],
     ["🧮 Calculators", "⚡ Futures", "❓ Help"]],
    resize_keyboard=True,
)


def uid_of(update: Update) -> int:
    u = update.effective_user
    return db.get_or_create_tg_user(u.id, update.effective_chat.id, u.first_name,
                                    "telegram$" + secrets.token_hex(16))


async def reply(update: Update, text: str, **kw):
    await update.effective_message.reply_text(text, parse_mode=HTML, disable_web_page_preview=True, **kw)


# ---------------- simple commands ----------------
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid_of(update)
    await reply(update, L.HELP, reply_markup=MENU)


async def help_cmd(update, ctx):
    await reply(update, L.HELP, reply_markup=MENU)


async def dashboard(update, ctx):
    await reply(update, L.dashboard_text(uid_of(update), update.effective_user.first_name or "friend"))


async def report(update, ctx):
    await reply(update, L.month_report_text(uid_of(update)))


async def chart(update, ctx):
    uid = uid_of(update)
    if not db.get_transactions(uid):
        return await reply(update, "Chart ku data illa. /demo try pannunga.")
    await update.effective_message.reply_photo(L.chart_png(uid), caption="📈 Income vs expenses + this month split")


async def holdings(update, ctx):
    uid = uid_of(update)
    rows = db.get_holdings(uid)
    kb = [[InlineKeyboardButton(f"🗑 {h['name'][:28]}", callback_data=f"delh:{h['id']}")] for h in rows[:12]]
    await reply(update, L.holdings_text(uid), reply_markup=InlineKeyboardMarkup(kb) if kb else None)


async def recent(update, ctx):
    uid = uid_of(update)
    txns = db.get_transactions(uid)[:10]
    kb = [[InlineKeyboardButton(f"🗑 Delete #{i}", callback_data=f"deltx:{t['id']}")
           for i, t in list(enumerate(txns, 1))[j:j + 5]] for j in range(0, len(txns), 5)]
    await reply(update, L.recent_text(txns), reply_markup=InlineKeyboardMarkup(kb) if kb else None)


async def reminders(update, ctx):
    up = L.upcoming(uid_of(update), 30)
    if not up:
        return await reply(update, "Next 30 days la payments illa. Holdings add pannumbodhu 'next due date' kudunga.")
    lines = ["<b>🔔 Next 30 days</b>"] + [f"• {d} · {escape(n)} ({L.days_label(k)})" for d, n, k in up]
    await reply(update, "\n".join(lines) + "\n\n<i>3 days munnaadi irundhu daily 9 AM ku reminder varum.</i>")


async def demo(update, ctx):
    load_sample(uid_of(update))
    await reply(update, "✅ Sample data load aachu (6 months dummy data). 📊 Dashboard click pannunga.")


async def delete_cb(update: Update, ctx):
    q = update.callback_query
    uid = uid_of(update)
    kind, _, raw = q.data.partition(":")
    if kind == "deltx":
        db.delete_transaction(uid, int(raw))
    elif kind == "delh":
        db.delete_holding(uid, int(raw))
    await q.answer("Deleted 🗑")
    await q.edit_message_reply_markup(None)
    await q.message.reply_text("Deleted ✅ Updated list ku button marubadi click pannunga.")


# ---------------- quick add: /expense 450 Food lunch ----------------
def _match_cat(word, cats):
    w = word.lower()
    for c in cats:
        if c.lower() == w or c.lower().startswith(w):
            return c
    return "Other"


async def quick_add(update, ctx, txn_type):
    args = ctx.args
    cats = db.EXPENSE_CATEGORIES if txn_type == "expense" else db.INCOME_CATEGORIES
    try:
        amount = L._num(args[0])
        if amount <= 0:
            raise ValueError
    except (IndexError, ValueError):
        return await reply(update, f"Example: <code>/{txn_type} 450 Food lunch</code>\nCategories: {', '.join(cats)}")
    cat = _match_cat(args[1], cats) if len(args) > 1 else "Other"
    note = " ".join(args[2:])[:100]
    db.add_transaction(uid_of(update), txn_type, cat, amount, date.today(), note)
    icon = "💸" if txn_type == "expense" else "💰"
    await reply(update, f"{icon} Saved: <b>{inr(amount)}</b> · {escape(cat)}" + (f" · {escape(note)}" if note else ""))


async def expense_cmd(update, ctx):
    await quick_add(update, ctx, "expense")


async def income_cmd(update, ctx):
    await quick_add(update, ctx, "income")


# ---------------- guided add (buttons) ----------------
KIND, CATEGORY, NAME, AMOUNT, INVESTED, NOTE, DUE = range(7)
KINDS = {"expense": "💸 Expense", "income": "💰 Income", "investment": "📊 Investment",
         "asset": "🏡 Asset", "loan": "💳 Loan"}


MENU_BTN = filters.Regex(r"^(📊 Dashboard|➕ Add|🧾 Recent|💼 Holdings|📈 Chart|🔔 Reminders|🧮 Calculators|⚡ Futures|❓ Help)$")
TEXT_IN = filters.TEXT & ~filters.COMMAND & ~MENU_BTN


def _cats(kind):
    if kind == "expense":
        return db.EXPENSE_CATEGORIES
    if kind == "income":
        return db.INCOME_CATEGORIES
    return db.HOLDING_CATEGORIES[kind]


async def add_start(update, ctx):
    ctx.user_data.clear()
    kb = [[InlineKeyboardButton(v, callback_data=f"kind:{k}")] for k, v in KINDS.items()]
    await reply(update, "Enna add pannanum?", reply_markup=InlineKeyboardMarkup(kb))
    return KIND


async def add_kind(update, ctx):
    q = update.callback_query
    await q.answer()
    kind = q.data.split(":", 1)[1]
    ctx.user_data["kind"] = kind
    cats = _cats(kind)
    kb = [[InlineKeyboardButton(c, callback_data=f"cat:{i}") for i, c in list(enumerate(cats))[j:j + 3]]
          for j in range(0, len(cats), 3)]
    await q.edit_message_text(f"{KINDS[kind]}: category select pannunga", reply_markup=InlineKeyboardMarkup(kb))
    return CATEGORY


async def add_cat(update, ctx):
    q = update.callback_query
    await q.answer()
    kind = ctx.user_data["kind"]
    ctx.user_data["cat"] = _cats(kind)[int(q.data.split(":", 1)[1])]
    await q.edit_message_text(f"{KINDS[kind]} · {ctx.user_data['cat']}")
    if kind in ("expense", "income"):
        await reply(update, "Amount evlo? (e.g. <code>450</code>, <code>1.5L</code>)")
        return AMOUNT
    await reply(update, "Name enna? (e.g. <i>Nifty 50 Index Fund</i>, <i>Home loan</i>)")
    return NAME


async def add_name(update, ctx):
    ctx.user_data["name"] = update.message.text.strip()[:80]
    first = "Original loan amount?" if ctx.user_data["kind"] == "loan" else "Evlo invest pannineenga / vaanguna vilai?"
    await reply(update, first + " (0 kooda podalaam)")
    return INVESTED


async def add_invested(update, ctx):
    try:
        ctx.user_data["invested"] = max(0.0, L._num(update.message.text))
    except ValueError:
        await reply(update, "Number mattum type pannunga (e.g. <code>3.6L</code>)")
        return INVESTED
    second = "Outstanding amount evlo?" if ctx.user_data["kind"] == "loan" else "Current value evlo?"
    await reply(update, second)
    return AMOUNT


async def add_amount(update, ctx):
    try:
        amt = L._num(update.message.text)
        if amt <= 0:
            raise ValueError
    except ValueError:
        await reply(update, "Valid amount type pannunga (e.g. <code>450</code>, <code>1.5L</code>)")
        return AMOUNT
    ctx.user_data["amount"] = amt
    if ctx.user_data["kind"] in ("expense", "income"):
        await reply(update, "Note? (illana /skip)")
        return NOTE
    await reply(update, "Next payment / EMI / renewal date? <code>YYYY-MM-DD</code> (illana /skip)")
    return DUE


async def add_note(update, ctx):
    note = "" if update.message.text == "/skip" else update.message.text.strip()[:100]
    d = ctx.user_data
    db.add_transaction(uid_of(update), d["kind"], d["cat"], d["amount"], date.today(), note)
    await reply(update, f"✅ Saved: {KINDS[d['kind']]} · {escape(d['cat'])} · <b>{inr(d['amount'])}</b>", reply_markup=MENU)
    return ConversationHandler.END


async def add_due(update, ctx):
    text = update.message.text.strip()
    due = None
    if text != "/skip":
        try:
            due = date.fromisoformat(text)
        except ValueError:
            await reply(update, "Date format <code>2026-12-05</code> maadhiri irukkanum (illana /skip)")
            return DUE
    d = ctx.user_data
    db.add_holding(uid_of(update), d["kind"], d["cat"], d["name"], d["invested"], d["amount"], due)
    await reply(update, f"✅ Saved: {KINDS[d['kind']]} · {escape(d['name'])} · <b>{inr(d['amount'])}</b>"
                + (f" · due {due}" if due else ""), reply_markup=MENU)
    return ConversationHandler.END


async def cancel(update, ctx):
    ctx.user_data.clear()
    await reply(update, "Cancelled.", reply_markup=MENU)
    return ConversationHandler.END


# ---------------- calculators & futures ----------------
def calc(fn):
    async def handler(update, ctx):
        if not ctx.args:
            return await reply(update, L.FUT_HELP if fn in (L.crypto_text, L.fno_text) else L.CALC_HELP)
        try:
            await reply(update, fn(ctx.args))
        except (ValueError, ZeroDivisionError) as e:
            msg = str(e) or "Values check pannunga"
            await reply(update, f"⚠️ {msg}\n\nExamples ku: " + ("⚡ Futures" if fn in (L.crypto_text, L.fno_text) else "🧮 Calculators"))
    return handler


async def calc_help(update, ctx):
    await reply(update, L.CALC_HELP)


async def fut_help(update, ctx):
    await reply(update, L.FUT_HELP)


# ---------------- daily reminder job ----------------
async def daily_reminders(ctx: ContextTypes.DEFAULT_TYPE):
    for link in db.get_all_tg_links():
        due = L.upcoming(link["user_id"], 3)
        if not due:
            continue
        lines = ["<b>🔔 SmartLife reminder</b>"] + [f"• {escape(n)} · {d} ({L.days_label(k)})" for d, n, k in due]
        try:
            await ctx.bot.send_message(link["chat_id"], "\n".join(lines), parse_mode=HTML)
        except Exception as e:  # user blocked the bot etc.
            log.warning("reminder failed for chat %s: %s", link["chat_id"], e)


async def on_error(update, ctx):
    log.exception("Unhandled error", exc_info=ctx.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Edho thappu aagiduchu. Marubadi try pannunga.")


def build_app(token: str) -> Application:
    db.init_db()
    app = Application.builder().token(token).build()

    add_conv = ConversationHandler(
        entry_points=[CommandHandler("add", add_start), MessageHandler(filters.Regex("^➕ Add$"), add_start)],
        states={
            KIND: [CallbackQueryHandler(add_kind, pattern=r"^kind:")],
            CATEGORY: [CallbackQueryHandler(add_cat, pattern=r"^cat:")],
            NAME: [MessageHandler(TEXT_IN, add_name)],
            INVESTED: [MessageHandler(TEXT_IN, add_invested)],
            AMOUNT: [MessageHandler(TEXT_IN, add_amount)],
            NOTE: [MessageHandler(TEXT_IN, add_note), CommandHandler("skip", add_note)],
            DUE: [MessageHandler(TEXT_IN, add_due), CommandHandler("skip", add_due)],
        },
        fallbacks=[CommandHandler("cancel", cancel), MessageHandler(MENU_BTN, cancel)],
    )
    app.add_handler(add_conv)

    for cmd, fn in {"start": start, "help": help_cmd, "dashboard": dashboard, "report": report,
                    "chart": chart, "holdings": holdings, "recent": recent, "reminders": reminders,
                    "demo": demo, "expense": expense_cmd, "income": income_cmd,
                    "calculators": calc_help, "futures": fut_help,
                    "sip": calc(L.sip_text), "lumpsum": calc(L.lumpsum_text), "emi": calc(L.emi_text),
                    "goal": calc(L.goal_text), "crypto": calc(L.crypto_text), "fno": calc(L.fno_text)}.items():
        app.add_handler(CommandHandler(cmd, fn))

    for label, fn in {"📊 Dashboard": dashboard, "🧾 Recent": recent, "💼 Holdings": holdings,
                      "📈 Chart": chart, "🔔 Reminders": reminders, "🧮 Calculators": calc_help,
                      "⚡ Futures": fut_help, "❓ Help": help_cmd}.items():
        app.add_handler(MessageHandler(filters.Regex(f"^{label}$"), fn))

    app.add_handler(CallbackQueryHandler(delete_cb, pattern=r"^del(tx|h):\d+$"))
    app.add_error_handler(on_error)
    app.job_queue.run_daily(daily_reminders, time=time(9, 0, tzinfo=IST), name="daily-reminders")
    return app


def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN illa. .env file la podunga (README paarunga).")
    log.info("SmartLife bot starting… Telegram la /start anuppunga.")
    build_app(token).run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
