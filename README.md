# SmartLife: All-in-One Personal Finance & Life Management Platform

College project. Track income, expenses, investments, assets, goals and more in one place.

## Features
- 🌐 7 languages: English, தமிழ், Tanglish, हिन्दी, తెలుగు, ಕನ್ನಡ, മലയാളം (sidebar → Language)
- 🌗 Light / dark mode toggle
- 🏠 Dashboard: net worth, income, expenses, savings rate, financial health score, upcoming payments & renewals, goals, learning progress
- 💸 Income & Expenses · 📅 Budget & Daily (quick daily expenses, category budgets with 80%/100% alerts, average daily spend, average monthly savings vs 20% rule)
- 📊 Investments, Assets & Loans · 🎯 Goals with one-click templates: wedding, trip, health, fitness, house, car, education, retirement
- 📰 Markets & News: Nifty/Sensex/BTC snapshot, personal watchlist with live prices, Google News headlines
- 🧰 Money Toolkit: 50/30/20 salary planner, government schemes (PPF, SSY, NPS, APY, PMJJBY, PMSBY, PM-JAY, SCSS), monthly money checklist
- 🧮 Calculators: SIP (step-up), Lumpsum, EMI (with balance chart), Goal, FD, Retirement
- ⚡ Futures Risk Calculator with **live LTP**: type BTC / RELIANCE / NIFTY / USDINR → "Get live price" → "Use as entry price"
  - Crypto (CoinGecko, Binance fallback): position size, margin, liquidation price
  - Indian stocks & F&O (Yahoo Finance, may be delayed): lots by risk & capital, or shares for cash trades
  - Forex: INR pairs on Indian exchanges + international pairs, pips / ticks, contracts
- 🩺 Health & Insurance: health profile, policies, renewal alerts, cover check, fitness tracker (weight, BMI, steps, workouts)
- 👨‍👩‍👧 Family & Nominees: members, nominee share per account / policy, gaps
- 🔐 Legacy Vault: encrypted notes & documents, nominee access codes, release after inactivity or manual release
- 📚 Learn: stock market, mutual funds, F&O, crypto, forex, technical analysis, risk management, personal finance + quizzes

## Run it (Mac)
```bash
cd ~/Downloads/smartlife
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_demo.py
streamlit run app.py
```
Login: `demo@smartlife.app` / `demo1234`
Nominee demo (login screen → Nominee access): owner `demo@smartlife.app`, nominee `priya@example.com`, code `DEMO-2026`
Live prices need internet.

## Telegram Bot 🤖
Ellaa features um Telegram la: dashboard, add income/expense/investment/loan, holdings,
chart, SIP/EMI/goal calculators, crypto & F&O futures risk calculator, daily payment reminders.

### Setup (first time, ~10 min)
1. **Python install** (illana): https://www.python.org/downloads/ →
   Windows la install pannumbodhu **"Add Python to PATH"** tick pannunga.
2. Telegram la **@BotFather** open → `/newbot` → bot ku name + username kudunga → **token** copy pannunga.
3. Indha folder la `.env.example` ah copy panni `.env` nu rename pannunga, adhula:
   `TELEGRAM_BOT_TOKEN=<unga token>`
   ⚠️ Token yaarkittaiyum share pannaadheenga, screenshot la um kaattaadheenga.
4. Terminal (Windows: Command Prompt) la indha folder la:
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
5. Telegram la unga bot ah open panni `/start` → `/demo` (sample data) → 📊 Dashboard.

Terminal open la irukkura varaikkum dhaan bot work aagum (laptop off panna bot stop aagum).

### Bot commands
| Command / Button | Enna pannum |
|---|---|
| 📊 Dashboard | Net worth, income, expenses, savings rate, health score, upcoming dues |
| ➕ Add | Buttons vazhiya expense / income / investment / asset / loan add |
| `/expense 450 Food lunch` | Quick expense add |
| `/income 85000 Salary` | Quick income add |
| 🧾 Recent | Last 10 transactions + delete buttons |
| 💼 Holdings | Investments, assets, loans, net worth |
| 📈 Chart | Income vs expenses chart image |
| `/report` | Indha month category-wise expenses |
| 🔔 Reminders | Next 30 days payments (daily 9 AM IST auto reminder) |
| `/sip 10000 12 10` | SIP calculator (`/sip monthly rate years [step-up]`) |
| `/lumpsum 1L 12 10` | Lumpsum calculator |
| `/emi 30L 8.5 20` | EMI calculator |
| `/goal 20L 5 6 12` | Goal planner |
| `/crypto long 1000 2 70000 68600 74200 10` | Crypto futures risk |
| `/fno long 5L 2 24000 23900 24300 75 150000` | Indian F&O lots & risk (lot size/margin: NSE/broker la check pannunga) |
| `/demo` | Sample data load |

## Project structure
```
smartlife/
├── app.py               # entry point, login + navigation
├── auth.py              # password hashing, login/logout
├── db.py                # SQLite schema + queries
├── finance.py           # all financial formulas (SIP, EMI, futures risk)
├── utils.py             # Indian ₹ number format
├── seed_demo.py         # dummy demo data (website login)
├── sample_data.py       # shared dummy data loader
├── bot.py               # Telegram bot: handlers, buttons, daily reminders
├── bot_logic.py         # bot reply text, calculators, chart image (no Telegram code)
├── .env.example         # copy to .env, put bot token
├── requirements.txt
└── views/
    ├── dashboard.py
    ├── income_expenses.py
    ├── holdings.py      # investments, assets, loans
    ├── calculators.py
    ├── futures.py
    └── coming_soon.py   # future-scope placeholder
```

## Security notes
- Parameterized SQL queries (no SQL injection)
- Every query scoped to the logged-in user's id
- Only dummy data is used in this project; no real personal/financial data
- `smartlife.db`, `.env` (bot token) and `.vault.key` (vault encryption key) are in `.gitignore`; don't commit or share them
- Vault notes/files are encrypted with Fernet; nominee codes are stored only as salted PBKDF2 hashes
- Only last 4 digits of account / policy numbers are stored
- Each Telegram account gets its own SmartLife user; no passwords are sent over chat
- Bot never asks for bank, card or account numbers
