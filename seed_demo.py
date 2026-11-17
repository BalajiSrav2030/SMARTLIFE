"""Creates the website demo user with DUMMY data.

Login:  demo@smartlife.app  /  demo1234
"""
import auth
import db
from sample_data import load_sample

db.init_db()

EMAIL, PASSWORD = "demo@smartlife.app", "demo1234"
user = db.get_user_by_email(EMAIL)
uid = user["id"] if user else db.create_user("Demo User", EMAIL, auth.hash_password(PASSWORD))
load_sample(uid)

print(f"Demo data ready ✅  Login: {EMAIL} / {PASSWORD}")
