"""Loads 6 months of DUMMY transactions + sample holdings for one user.
Used by seed_demo.py (website) and the /demo command (Telegram bot)."""
import random
from datetime import date, timedelta

import db


def load_sample(uid: int, seed: int = 42) -> None:
    rnd = random.Random(seed)
    with db.get_conn() as conn:
        conn.execute("DELETE FROM transactions WHERE user_id = ?", (uid,))
        for tbl in ("holdings", "goals", "policies", "nominations", "family", "vault_items", "vault_settings",
                    "vault_codes", "health_profile", "budgets", "fitness_log", "watchlist"):
            conn.execute(f"DELETE FROM {tbl} WHERE user_id = ?", (uid,))

    today = date.today()
    for back in range(5, -1, -1):
        m = (today.month - back - 1) % 12 + 1
        y = today.year + (today.month - back - 1) // 12
        first = date(y, m, 1)
        last_day = today.day if back == 0 else 28

        def d(day):
            return first + timedelta(days=(day if back == 0 else min(day, last_day)) - 1)

        def add(kind, cat, amt, when, note=""):
            # in the current month, skip entries dated after today instead of piling them on today
            if back == 0 and when > today:
                return
            db.add_transaction(uid, kind, cat, amt, when, note)

        add("income", "Salary", 85000, d(1), "Monthly salary")
        if rnd.random() < 0.4:
            add("income", "Freelance", rnd.choice([5000, 8000, 12000]), d(15))
        add("expense", "Rent", 15000, d(2))
        add("expense", "EMI", 18500, d(5), "Home loan EMI")
        add("expense", "Bills & Utilities", rnd.randint(2500, 4000), d(8))
        for _ in range(4):
            add("expense", "Groceries", rnd.randint(1200, 2500), d(rnd.randint(1, 28)))
        for _ in range(6):
            add("expense", "Food", rnd.randint(300, 1200), d(rnd.randint(1, 28)))
        add("expense", "Transport", rnd.randint(1500, 3000), d(20))
        if rnd.random() < 0.5:
            add("expense", "Shopping", rnd.randint(2000, 7000), d(rnd.randint(1, 28)))
        if rnd.random() < 0.3:
            add("expense", "Health", rnd.randint(800, 3000), d(rnd.randint(1, 28)))
        add("expense", "Entertainment", rnd.randint(500, 2000), d(rnd.randint(1, 28)))

    nxt = lambda days: today + timedelta(days=days)
    holdings = [
        ("investment", "Mutual Funds", "Nifty 50 Index Fund (SIP)", 360000, 452000, nxt(6)),
        ("investment", "Stocks", "Stock portfolio", 250000, 287000, None),
        ("investment", "Gold", "Gold ETF / SGB", 150000, 196000, None),
        ("investment", "Crypto", "BTC + ETH", 80000, 94000, None),
        ("investment", "FD / RD", "Bank FD", 110000, 118000, None),
        ("asset", "Property", "2BHK flat", 3200000, 3800000, nxt(120)),
        ("asset", "Vehicle", "Car", 900000, 620000, nxt(29)),
        ("asset", "Cash / Bank", "Savings account", 0, 140000, None),
        ("loan", "Home Loan", "Home loan", 2500000, 1850000, nxt(1)),
        ("loan", "Car Loan", "Car loan", 600000, 210000, nxt(10)),
    ]
    for k, c, n, inv, cur, due in holdings:
        db.add_holding(uid, k, c, n, inv, cur, due)

    # fitness log (dummy) for the last 3 weeks
    db.set_height(uid, 172)
    for k in range(21, -1, -3):
        day = today - timedelta(days=k)
        db.add_row("fitness_log", uid, log_date=str(day), weight=round(78.4 - (21 - k) * 0.12, 1),
                   steps=rnd.randint(5000, 11000), workout_min=rnd.choice([0, 30, 45, 60]), note=rnd.choice(["walk", "gym", "yoga", ""]))
    for sym, kind in [("NIFTY", "stock"), ("RELIANCE", "stock"), ("HDFCBANK", "stock"), ("TCS", "stock"),
                      ("BTC", "crypto"), ("ETH", "crypto")]:
        db.add_watch(uid, sym, kind)

    # monthly budgets (Food set tight so the demo shows an alert)
    for cat, lim in [("Food", 3000), ("Groceries", 8000), ("Shopping", 5000), ("Transport", 3000),
                     ("Entertainment", 2000), ("Bills & Utilities", 4000)]:
        db.set_budget(uid, cat, lim)

    # goals
    for name, target, saved, years in [("House down payment", 2000000, 900000, 3), ("Emergency fund", 340000, 258000, 1),
                                       ("Child education", 1500000, 150000, 12), ("Retirement", 15000000, 1800000, 30)]:
        db.add_row("goals", uid, name=name, target=target, saved=saved,
                   target_date=str(date(today.year + years, today.month, 1)), expected_return=12)

    # insurance
    db.save_health(uid, blood_group="B+", conditions="None", allergies="Penicillin", doctor="Dr. Sample Clinic",
                   emergency_contact="Spouse")
    pols = [("Health", "Sample Health Insurer", "4321", 1000000, 18500, nxt(18), "Self, spouse, child"),
            ("Term life", "Sample Life Insurer", "8765", 10000000, 14200, nxt(140), "Self"),
            ("Vehicle", "Sample General Insurer", "1122", 620000, 9800, nxt(29), "Car")]
    for ptype, ins, l4, cover, prem, ren, cov in pols:
        db.add_row("policies", uid, ptype=ptype, insurer=ins, policy_last4=l4, cover=cover, premium=prem,
                   renewal=str(ren), covers=cov)

    # family & nominees
    spouse = db.add_row("family", uid, name="Priya", relation="Spouse", dob="1996-04-12",
                        email="priya@example.com", is_nominee=1)
    child = db.add_row("family", uid, name="Arjun", relation="Son", dob="2021-09-03", email=None, is_nominee=1)
    db.add_row("family", uid, name="Lakshmi", relation="Mother", dob="1968-01-20", email=None, is_nominee=0)
    for item, who, share in [("Mutual Funds · Nifty 50 Index Fund (SIP)", spouse, 50),
                             ("Mutual Funds · Nifty 50 Index Fund (SIP)", child, 50),
                             ("Property · 2BHK flat", spouse, 100), ("Insurance · Term life · Sample Life Insurer", spouse, 100),
                             ("Stocks · Stock portfolio", spouse, 100)]:
        db.add_row("nominations", uid, member_id=who, item=item, share=share)

    # vault (dummy records) + demo nominee code DEMO-2026
    import vault_crypto
    for title, itype, inst, l4, note in [
            ("Salary savings account", "Bank account", "Sample Bank", "4455",
             "Branch: Anna Nagar. Debit card and cheque book in the blue file, top shelf."),
            ("Demat account", "Demat / trading", "Sample Broker", "7788", "Holdings statement is emailed monthly."),
            ("House papers", "Property document", "Sub-registrar office", "", "Original sale deed in the bank locker.")]:
        db.add_row("vault_items", uid, title=title, itype=itype, institution=inst, last4=l4,
                   notes_enc=vault_crypto.encrypt(note), file_name=None, file_enc=None, visible=1)
    db.save_vault_settings(uid, 180, 1)
    db.set_vault_code(uid, spouse, vault_crypto.hash_code("DEMO-2026"))
