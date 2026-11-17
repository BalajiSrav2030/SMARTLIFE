"""Database layer: SQLite connection, schema and queries.

All queries use parameter placeholders (?) to prevent SQL injection,
and every data query is scoped to a user_id.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "smartlife.db"

INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Interest", "Dividend", "Rent", "Other"]
HOLDING_CATEGORIES = {
    "investment": ["Stocks", "Mutual Funds", "SIP", "Gold", "Silver", "Crypto", "FD / RD", "PPF / EPF", "Other"],
    "asset": ["Property", "Land", "Vehicle", "Jewellery", "Cash / Bank", "Other"],
    "loan": ["Home Loan", "Car Loan", "Personal Loan", "Education Loan", "Credit Card", "Other"],
}
EXPENSE_CATEGORIES = [
    "Rent", "Food", "Groceries", "Transport", "Shopping", "Bills & Utilities",
    "EMI", "Health", "Education", "Entertainment", "Travel", "Other",
]


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                txn_type  TEXT NOT NULL CHECK (txn_type IN ('income', 'expense')),
                category  TEXT NOT NULL,
                amount    REAL NOT NULL CHECK (amount > 0),
                txn_date  TEXT NOT NULL,
                note      TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_txn_user_date
                ON transactions (user_id, txn_date);

            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name TEXT NOT NULL, target REAL NOT NULL, saved REAL NOT NULL DEFAULT 0,
                target_date TEXT NOT NULL, expected_return REAL NOT NULL DEFAULT 12
            );
            CREATE TABLE IF NOT EXISTS health_profile (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                blood_group TEXT, conditions TEXT, allergies TEXT, doctor TEXT, emergency_contact TEXT
            );
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                ptype TEXT NOT NULL, insurer TEXT NOT NULL, policy_last4 TEXT,
                cover REAL NOT NULL DEFAULT 0, premium REAL NOT NULL DEFAULT 0, renewal TEXT, covers TEXT
            );
            CREATE TABLE IF NOT EXISTS family (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name TEXT NOT NULL, relation TEXT NOT NULL, dob TEXT, email TEXT, is_nominee INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS nominations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                member_id INTEGER NOT NULL REFERENCES family(id) ON DELETE CASCADE,
                item TEXT NOT NULL, share REAL NOT NULL DEFAULT 100
            );
            CREATE TABLE IF NOT EXISTS vault_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL, itype TEXT NOT NULL, institution TEXT, last4 TEXT,
                notes_enc BLOB, file_name TEXT, file_enc BLOB, visible INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS vault_settings (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                inactivity_days INTEGER NOT NULL DEFAULT 180, released INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS vault_codes (
                member_id INTEGER PRIMARY KEY REFERENCES family(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                code_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS fitness_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                log_date TEXT NOT NULL, weight REAL, steps INTEGER, workout_min INTEGER, note TEXT
            );
            CREATE TABLE IF NOT EXISTS watchlist (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                symbol TEXT NOT NULL, kind TEXT NOT NULL CHECK (kind IN ('stock', 'crypto')),
                PRIMARY KEY (user_id, symbol, kind)
            );
            CREATE TABLE IF NOT EXISTS budgets (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                category TEXT NOT NULL, monthly_limit REAL NOT NULL CHECK (monthly_limit > 0),
                PRIMARY KEY (user_id, category)
            );
            CREATE TABLE IF NOT EXISTS learn_progress (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                lesson_id TEXT NOT NULL, score INTEGER NOT NULL, total INTEGER NOT NULL,
                PRIMARY KEY (user_id, lesson_id)
            );

            -- Telegram account -> SmartLife user
            CREATE TABLE IF NOT EXISTS telegram_links (
                tg_user_id INTEGER PRIMARY KEY,
                chat_id    INTEGER NOT NULL,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
            );

            -- Investments, assets and loans (liabilities) in one table
            CREATE TABLE IF NOT EXISTS holdings (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                kind          TEXT NOT NULL CHECK (kind IN ('investment', 'asset', 'loan')),
                category      TEXT NOT NULL,
                name          TEXT NOT NULL,
                invested      REAL NOT NULL DEFAULT 0 CHECK (invested >= 0),
                current_value REAL NOT NULL CHECK (current_value >= 0),
                due_date      TEXT,
                note          TEXT
            );
            """
        )


    # migration for databases created by older versions
    with get_conn() as conn:
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(users)")}
        if "last_login" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
        hcols = {r["name"] for r in conn.execute("PRAGMA table_info(health_profile)")}
        if "height_cm" not in hcols:
            conn.execute("ALTER TABLE health_profile ADD COLUMN height_cm REAL")


# ---------- generic per-user CRUD (table + column names are whitelisted) ----------
_TABLES = {
    "goals": ["name", "target", "saved", "target_date", "expected_return"],
    "policies": ["ptype", "insurer", "policy_last4", "cover", "premium", "renewal", "covers"],
    "family": ["name", "relation", "dob", "email", "is_nominee"],
    "nominations": ["member_id", "item", "share"],
    "fitness_log": ["log_date", "weight", "steps", "workout_min", "note"],
    "vault_items": ["title", "itype", "institution", "last4", "notes_enc", "file_name", "file_enc", "visible"],
}


def add_row(table, user_id, **fields):
    cols = _TABLES[table]
    bad = set(fields) - set(cols)
    if bad:
        raise ValueError(f"unknown columns {bad}")
    names = ", ".join(["user_id", *fields])
    marks = ", ".join("?" * (len(fields) + 1))
    with get_conn() as conn:
        cur = conn.execute(f"INSERT INTO {table} ({names}) VALUES ({marks})", (user_id, *fields.values()))
        return cur.lastrowid


def list_rows(table, user_id, order="id"):
    if table not in _TABLES or order not in ("id", *_TABLES[table]):
        raise ValueError("bad table/order")
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            f"SELECT * FROM {table} WHERE user_id = ? ORDER BY {order}", (user_id,)).fetchall()]


def update_row(table, user_id, row_id, **fields):
    cols = _TABLES[table]
    if set(fields) - set(cols):
        raise ValueError("unknown columns")
    sets = ", ".join(f"{k} = ?" for k in fields)
    with get_conn() as conn:
        conn.execute(f"UPDATE {table} SET {sets} WHERE id = ? AND user_id = ?", (*fields.values(), row_id, user_id))


def delete_row(table, user_id, row_id):
    if table not in _TABLES:
        raise ValueError("bad table")
    with get_conn() as conn:
        conn.execute(f"DELETE FROM {table} WHERE id = ? AND user_id = ?", (row_id, user_id))


def get_health(user_id):
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM health_profile WHERE user_id = ?", (user_id,)).fetchone()
    return dict(r) if r else {}


def save_health(user_id, **f):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO health_profile (user_id, blood_group, conditions, allergies, doctor, emergency_contact)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET blood_group=excluded.blood_group, conditions=excluded.conditions,
               allergies=excluded.allergies, doctor=excluded.doctor, emergency_contact=excluded.emergency_contact""",
            (user_id, f.get("blood_group"), f.get("conditions"), f.get("allergies"), f.get("doctor"),
             f.get("emergency_contact")))


def get_vault_settings(user_id):
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM vault_settings WHERE user_id = ?", (user_id,)).fetchone()
    return dict(r) if r else {"user_id": user_id, "inactivity_days": 180, "released": 0}


def save_vault_settings(user_id, inactivity_days, released):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO vault_settings (user_id, inactivity_days, released) VALUES (?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET inactivity_days=excluded.inactivity_days, released=excluded.released""",
            (user_id, int(inactivity_days), int(released)))


def set_vault_code(user_id, member_id, code_hash):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO vault_codes (member_id, user_id, code_hash) VALUES (?, ?, ?)
               ON CONFLICT(member_id) DO UPDATE SET code_hash=excluded.code_hash, created_at=CURRENT_TIMESTAMP""",
            (member_id, user_id, code_hash))


def vault_codes(user_id):
    with get_conn() as conn:
        return {r["member_id"]: dict(r) for r in conn.execute(
            "SELECT * FROM vault_codes WHERE user_id = ?", (user_id,)).fetchall()}


def find_nominee(owner_email, nominee_email):
    """Returns (owner_row, member_row, code_hash) or None."""
    with get_conn() as conn:
        r = conn.execute(
            """SELECT u.id AS owner_id, u.name AS owner_name, u.last_login, f.id AS member_id, f.name AS member_name,
                      c.code_hash
               FROM users u JOIN family f ON f.user_id = u.id
               JOIN vault_codes c ON c.member_id = f.id
               WHERE lower(u.email) = lower(?) AND lower(f.email) = lower(?) AND f.is_nominee = 1""",
            (owner_email.strip(), nominee_email.strip())).fetchone()
    return dict(r) if r else None


def touch_login(user_id):
    with get_conn() as conn:
        conn.execute("UPDATE users SET last_login = datetime('now') WHERE id = ?", (user_id,))


def save_progress(user_id, lesson_id, score, total):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO learn_progress (user_id, lesson_id, score, total) VALUES (?, ?, ?, ?)
               ON CONFLICT(user_id, lesson_id) DO UPDATE SET score=MAX(score, excluded.score), total=excluded.total""",
            (user_id, lesson_id, score, total))


def get_progress(user_id):
    with get_conn() as conn:
        return {r["lesson_id"]: dict(r) for r in conn.execute(
            "SELECT * FROM learn_progress WHERE user_id = ?", (user_id,)).fetchall()}


def set_height(user_id, height_cm):
    with get_conn() as conn:
        conn.execute("INSERT INTO health_profile (user_id, height_cm) VALUES (?, ?) "
                     "ON CONFLICT(user_id) DO UPDATE SET height_cm = excluded.height_cm", (user_id, float(height_cm)))


def get_watchlist(user_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT symbol, kind FROM watchlist WHERE user_id = ? ORDER BY kind, symbol", (user_id,)).fetchall()]


def add_watch(user_id, symbol, kind):
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO watchlist (user_id, symbol, kind) VALUES (?, ?, ?)",
                     (user_id, symbol.strip().upper()[:20], kind))


def remove_watch(user_id, symbol, kind):
    with get_conn() as conn:
        conn.execute("DELETE FROM watchlist WHERE user_id = ? AND symbol = ? AND kind = ?", (user_id, symbol, kind))


def get_budgets(user_id):
    with get_conn() as conn:
        return {r["category"]: r["monthly_limit"] for r in conn.execute(
            "SELECT category, monthly_limit FROM budgets WHERE user_id = ?", (user_id,)).fetchall()}


def set_budget(user_id, category, monthly_limit):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO budgets (user_id, category, monthly_limit) VALUES (?, ?, ?)
               ON CONFLICT(user_id, category) DO UPDATE SET monthly_limit = excluded.monthly_limit""",
            (user_id, category, float(monthly_limit)))


def delete_budget(user_id, category):
    with get_conn() as conn:
        conn.execute("DELETE FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))


# ---------- users ----------
def create_user(name, email, password_hash):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        return cur.lastrowid


def get_user_by_email(email):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


# ---------- telegram ----------
def get_or_create_tg_user(tg_user_id, chat_id, name, password_hash):
    """Each Telegram account gets its own SmartLife user (no password ever sent over chat)."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT user_id FROM telegram_links WHERE tg_user_id = ?", (tg_user_id,)
        ).fetchone()
        if row:
            conn.execute("UPDATE telegram_links SET chat_id = ? WHERE tg_user_id = ?", (chat_id, tg_user_id))
            return row["user_id"]
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name or "Telegram user", f"tg{tg_user_id}@telegram.smartlife", password_hash),
        )
        uid = cur.lastrowid
        conn.execute(
            "INSERT INTO telegram_links (tg_user_id, chat_id, user_id) VALUES (?, ?, ?)",
            (tg_user_id, chat_id, uid),
        )
        return uid


def get_all_tg_links():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT chat_id, user_id FROM telegram_links").fetchall()]


# ---------- transactions ----------
def add_transaction(user_id, txn_type, category, amount, txn_date, note=""):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO transactions (user_id, txn_type, category, amount, txn_date, note)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, txn_type, category, float(amount), str(txn_date), note),
        )


def delete_transaction(user_id, txn_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM transactions WHERE id = ? AND user_id = ?", (txn_id, user_id)
        )


def add_holding(user_id, kind, category, name, invested, current_value, due_date=None, note=""):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO holdings (user_id, kind, category, name, invested, current_value, due_date, note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, kind, category, name, float(invested), float(current_value),
             str(due_date) if due_date else None, note),
        )


def delete_holding(user_id, holding_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM holdings WHERE id = ? AND user_id = ?", (holding_id, user_id))


def get_holdings(user_id):
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT id, kind, category, name, invested, current_value, due_date, note
               FROM holdings WHERE user_id = ? ORDER BY kind, current_value DESC""",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_transactions(user_id):
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT id, txn_type, category, amount, txn_date, note
               FROM transactions WHERE user_id = ?
               ORDER BY txn_date DESC, id DESC""",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]
