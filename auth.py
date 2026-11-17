"""Authentication: password hashing (PBKDF2-SHA256 with random salt) + login state."""
import hashlib
import hmac
import re
import secrets
import sqlite3

import streamlit as st

import db

ITERATIONS = 200_000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), ITERATIONS)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), ITERATIONS)
    return hmac.compare_digest(digest.hex(), digest_hex)


def register(name, email, password):
    """Returns (ok, message)."""
    email = email.strip().lower()
    if not name.strip():
        return False, "Name enter pannunga."
    if not EMAIL_RE.match(email):
        return False, "Valid email enter pannunga."
    if len(password) < 8:
        return False, "Password kuraindhadhu 8 characters irukkanum."
    try:
        db.create_user(name.strip(), email, hash_password(password))
    except sqlite3.IntegrityError:
        return False, "Indha email already register aagirukku."
    return True, "Account create aachu! Ippo login pannunga."


def login(email, password):
    user = db.get_user_by_email(email.strip().lower())
    # Same error message for wrong email / wrong password (don't leak which one)
    if user is None or not verify_password(password, user["password_hash"]):
        return False
    st.session_state.user = {"id": user["id"], "name": user["name"], "email": user["email"]}
    return True


def logout():
    st.session_state.pop("user", None)


def current_user():
    return st.session_state.get("user")
