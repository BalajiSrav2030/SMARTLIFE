"""Learn module content. General education only – not investment advice.
Rules and tax treatment change: always check sebi.gov.in, rbi.org.in, amfiindia.com and incometax.gov.in."""

LESSONS = [
    {
        "id": "stocks", "icon": "📈", "title": "Stock market basics", "level": "Beginner", "minutes": 8,
        "sections": [
            ("What is a share?", "A share is a small piece of ownership in a company. If the company grows and earns more, "
             "the value of its shares can rise. Companies list on stock exchanges so that the public can buy and sell these shares."),
            ("Who runs the market in India?", "India's two main exchanges are the <b>NSE</b> and the <b>BSE</b>. "
             "<b>SEBI</b> (Securities and Exchange Board of India) is the regulator that protects investors and sets the rules. "
             "Your shares are held electronically in a <b>demat account</b> with a depository (NSDL or CDSL), and you place orders through a SEBI-registered broker."),
            ("Indices: Nifty 50 and Sensex", "An index tracks a basket of stocks to show how the market is doing. "
             "<b>Nifty 50</b> follows 50 large companies on NSE; <b>Sensex</b> follows 30 large companies on BSE."),
            ("Placing an order", "<ul><li><b>Market order</b>: buy/sell immediately at the best available price.</li>"
             "<li><b>Limit order</b>: buy/sell only at your price or better.</li>"
             "<li><b>Stop-loss order</b>: exits automatically if price moves against you to a set level.</li>"
             "<li><b>LTP</b> (last traded price) is the price of the most recent trade.</li></ul>"),
            ("Investing vs trading", "Investing means holding good businesses for years and letting compounding work. "
             "Trading means trying to profit from short-term price moves; it needs strict risk control and most beginners lose money doing it."),
        ],
        "terms": ["Share", "NSE / BSE", "SEBI", "Demat", "Nifty 50", "Sensex", "LTP", "Limit order", "Market cap", "Dividend"],
        "quiz": [
            ("Who regulates the securities market in India?", ["RBI", "SEBI", "NSE", "IRDAI"], 1,
             "SEBI regulates securities markets. RBI regulates banks and money; IRDAI regulates insurance."),
            ("A limit order will…", ["Execute instantly at any price", "Execute only at your price or better",
                                     "Always be cancelled", "Only work for mutual funds"], 1,
             "A limit order fills only at the price you set or a better one."),
            ("Nifty 50 tracks…", ["50 large NSE companies", "All companies in India", "Gold prices", "50 mutual funds"], 0,
             "Nifty 50 is an index of 50 large companies listed on NSE."),
        ],
    },
    {
        "id": "mf", "icon": "🧺", "title": "Mutual funds & SIP", "level": "Beginner", "minutes": 7,
        "sections": [
            ("What is a mutual fund?", "A mutual fund pools money from many investors and a professional fund manager invests it in stocks, bonds or both. "
             "You own <b>units</b>; the price of one unit is the <b>NAV</b> (net asset value), published every business day."),
            ("Types", "<ul><li><b>Equity funds</b>: mostly shares; higher risk, higher long-term growth potential.</li>"
             "<li><b>Debt funds</b>: bonds and money-market instruments; lower volatility.</li>"
             "<li><b>Hybrid funds</b>: a mix of both.</li>"
             "<li><b>Index funds / ETFs</b>: simply copy an index like Nifty 50, usually at low cost.</li></ul>"),
            ("Costs to check", "<b>Expense ratio</b> is the yearly fee taken from the fund. <b>Direct plans</b> have lower expense ratios than <b>regular plans</b> "
             "because no distributor commission is paid. Some funds charge an <b>exit load</b> if you redeem early."),
            ("SIP and rupee-cost averaging", "A <b>SIP</b> (systematic investment plan) invests a fixed amount every month. "
             "When prices are low you get more units, when high you get fewer, which averages your cost. "
             "The real power is <b>compounding</b>: returns earn further returns over long periods. Try the SIP calculator to see it."),
        ],
        "terms": ["NAV", "Units", "Expense ratio", "Direct plan", "Exit load", "Index fund", "ETF", "SIP", "Compounding"],
        "quiz": [
            ("NAV means…", ["New asset value", "Net asset value", "National average value", "Net annual volume"], 1,
             "NAV is the per-unit value of a mutual fund."),
            ("Which plan usually has a lower expense ratio?", ["Regular plan", "Direct plan", "Both are same", "Neither"], 1,
             "Direct plans skip distributor commission, so their expense ratio is lower."),
            ("A SIP helps mainly by…", ["Guaranteeing returns", "Investing regularly and averaging cost",
                                         "Avoiding all risk", "Doubling money every year"], 1,
             "SIPs build discipline and average the purchase cost; returns are not guaranteed."),
        ],
    },
    {
        "id": "fno", "icon": "⚡", "title": "Futures & options (F&O)", "level": "Intermediate", "minutes": 10,
        "sections": [
            ("Derivatives", "A derivative's value comes from something else (the <b>underlying</b>), like a stock or an index. "
             "Futures and options are the two main types traded on NSE and BSE."),
            ("Futures", "A futures contract is an agreement to buy or sell the underlying at a fixed price on a future <b>expiry</b> date. "
             "You trade in fixed <b>lot sizes</b> set by the exchange, and you only put up a <b>margin</b> (a fraction of the contract value). "
             "Profit and loss is settled daily (<b>mark-to-market</b>)."),
            ("Options", "A <b>call option</b> gives the right (not obligation) to buy at the strike price; a <b>put option</b> gives the right to sell. "
             "The buyer pays a <b>premium</b>. Option sellers (writers) receive the premium but can face large losses."),
            ("Leverage cuts both ways", "Because margin is small compared with contract value, a small price move creates a big gain or loss on your money. "
             "SEBI studies have reported that around 9 out of 10 individual F&O traders lost money. "
             "Use the Futures Risk Calculator to size positions so one bad trade cannot hurt your capital badly."),
            ("Before trading F&O", "<ul><li>Risk only 1–2% of capital per trade.</li><li>Always decide the stop-loss before entering.</li>"
             "<li>Check current lot sizes and margins on NSE / your broker; they change.</li>"
             "<li>Never use money meant for EMIs, emergencies or goals.</li></ul>"),
        ],
        "terms": ["Underlying", "Expiry", "Lot size", "Margin", "Mark-to-market", "Call", "Put", "Strike", "Premium", "Open interest"],
        "quiz": [
            ("A call option gives the buyer…", ["Obligation to buy", "Right to buy at strike", "Right to sell at strike", "A fixed dividend"], 1,
             "Call = right (not obligation) to buy at the strike price."),
            ("In futures you deposit…", ["The full contract value", "A margin", "Nothing", "Only brokerage"], 1,
             "You deposit margin; that is why futures are leveraged."),
            ("Per-trade risk most risk managers suggest:", ["1–2% of capital", "25% of capital", "50% of capital", "All of it"], 0,
             "Keeping risk at 1–2% per trade lets you survive a losing streak."),
        ],
    },
    {
        "id": "crypto", "icon": "🪙", "title": "Crypto basics", "level": "Beginner", "minutes": 8,
        "sections": [
            ("What is crypto?", "Cryptocurrencies like Bitcoin and Ethereum are digital assets recorded on a <b>blockchain</b>, "
             "a shared ledger maintained by many computers. Prices are set purely by supply and demand and can move 5–10% in a day."),
            ("Wallets and exchanges", "You can hold crypto on an <b>exchange</b> (custodial) or in your own <b>wallet</b> where you control the private keys. "
             "Whoever has the private key / seed phrase controls the coins, so never share it with anyone."),
            ("Spot vs futures", "<b>Spot</b> means you buy the actual coin. <b>Perpetual futures</b> let you trade price moves with leverage and no expiry; "
             "a periodic <b>funding rate</b> keeps the price close to spot. With leverage, if price moves against you enough, the position is "
             "<b>liquidated</b> and the margin is lost."),
            ("Rules in India (check current)", "Under rules introduced in 2022, gains on virtual digital assets are taxed at a flat rate and TDS applies on transfers above set limits; "
             "losses cannot be set off against other income. Exchanges serving Indians need to register with FIU-IND. "
             "Tax and regulatory rules change, so confirm on incometax.gov.in or with a tax professional."),
            ("Stay safe", "<ul><li>Use well-known, registered exchanges and turn on 2FA.</li>"
             "<li>Beware of 'guaranteed returns', Telegram tips and pump-and-dump groups.</li>"
             "<li>Keep crypto a small part of your portfolio.</li></ul>"),
        ],
        "terms": ["Blockchain", "Wallet", "Private key", "Seed phrase", "Spot", "Perpetual", "Funding rate", "Liquidation", "Stablecoin", "USDT"],
        "quiz": [
            ("Who controls coins in a self-custody wallet?", ["The exchange", "Whoever has the private key", "The government", "Nobody"], 1,
             "The private key / seed phrase controls the coins. Never share it."),
            ("Liquidation in crypto futures means…", ["You get a bonus", "Your position is force-closed and margin lost",
                                                       "Coins are converted to cash in your bank", "Funding rate becomes zero"], 1,
             "When losses eat the margin, the exchange closes the position."),
            ("A message promising 'guaranteed 5% daily returns' is most likely…", ["A great deal", "A scam", "Regulated", "Normal"], 1,
             "Guaranteed high returns are a classic scam signal."),
        ],
    },
    {
        "id": "forex", "icon": "💱", "title": "Forex basics", "level": "Intermediate", "minutes": 7,
        "sections": [
            ("Currency pairs", "Forex prices are quoted as pairs like <b>USD/INR</b>. The first currency is the <b>base</b>, the second the <b>quote</b>. "
             "USD/INR = 84 means 1 US dollar costs 84 rupees."),
            ("Pips and lots", "A <b>pip</b> is the standard small price step: 0.0001 for most pairs, 0.01 for JPY pairs. "
             "Internationally a <b>standard lot</b> is 100,000 units of the base currency. On Indian exchanges, currency futures like USD/INR have a contract size of 1,000 units."),
            ("Rules for Indian residents", "Indian residents may trade currency derivatives only on recognised Indian exchanges (NSE, BSE, MSE) in the pairs RBI permits. "
             "Trading forex on overseas online platforms is not permitted, and RBI publishes an <b>Alert List</b> of unauthorised platforms. "
             "Check rbi.org.in for the latest list and permitted pairs."),
            ("What moves currencies", "Interest rate decisions, inflation data, trade balances, oil prices for INR, and global risk sentiment. "
             "Central bank announcements can cause sudden large moves."),
        ],
        "terms": ["Base currency", "Quote currency", "Pip", "Lot", "Spread", "USD/INR", "RBI Alert List", "Currency futures"],
        "quiz": [
            ("In EUR/USD, the base currency is…", ["USD", "EUR", "INR", "Both"], 1, "The first currency in the pair is the base."),
            ("A pip on EUR/USD is usually…", ["0.01", "0.0001", "1", "0.1"], 1, "Most pairs: 0.0001. JPY pairs: 0.01."),
            ("Where can Indian residents legally trade currency derivatives?", ["Any overseas app", "Recognised Indian exchanges",
                                                                                "Telegram groups", "Nowhere"], 1,
             "Only on recognised Indian exchanges in RBI-permitted pairs."),
        ],
    },
    {
        "id": "ta", "icon": "🕯️", "title": "Technical analysis basics", "level": "Intermediate", "minutes": 7,
        "sections": [
            ("Candlesticks", "Each candle shows the <b>open, high, low and close</b> for a period. Green (or hollow) means close above open; red means close below open."),
            ("Support and resistance", "<b>Support</b> is a price zone where buying has stopped falls before; <b>resistance</b> is where selling has stopped rises. "
             "Traders often place stop-losses just beyond these zones."),
            ("Moving averages", "A moving average smooths price. When a short average (e.g. 20-day) crosses above a long one (e.g. 50-day), some traders read it as an uptrend signal."),
            ("RSI and volume", "<b>RSI</b> (0–100) measures momentum; above 70 is often called overbought, below 30 oversold. "
             "Rising <b>volume</b> on a breakout makes the move more convincing."),
            ("Limits", "Indicators describe the past; none predicts the future reliably. Always combine signals with risk management."),
        ],
        "terms": ["OHLC", "Candlestick", "Support", "Resistance", "Moving average", "RSI", "Volume", "Breakout", "Trend"],
        "quiz": [
            ("RSI above 70 is commonly called…", ["Oversold", "Overbought", "Neutral", "Liquidated"], 1, "Above 70 = overbought (not a sell guarantee)."),
            ("Support is a zone where…", ["Selling stopped rises", "Buying stopped falls", "Trading is banned", "Dividends are paid"], 1,
             "Support = buyers stepped in before."),
            ("Indicators can…", ["Predict the future exactly", "Describe past price behaviour", "Remove all risk", "Guarantee profit"], 1,
             "They summarise past data; use with risk control."),
        ],
    },
    {
        "id": "risk", "icon": "🛡️", "title": "Risk management", "level": "All levels", "minutes": 6,
        "sections": [
            ("The 1–2% rule", "Risk only 1–2% of your trading capital on any single trade. With ₹1,00,000 capital and 2% risk, the most you can lose on one trade is ₹2,000. "
             "Ten losses in a row would still leave you with about 82% of your capital."),
            ("Position sizing", "Position size = amount you are willing to lose ÷ distance to your stop-loss. The calculator in SmartLife does this for crypto, stocks, F&O and forex."),
            ("Risk : reward", "Aim for trades where the possible reward is at least twice the risk (1:2). Then even a 40% win rate can be profitable."),
            ("Diversify", "Spread money across asset types (equity, debt, gold) and across companies, so one bad event does not sink everything."),
            ("Foundation first", "Keep an emergency fund of 6 months' expenses, buy term and health insurance, and clear high-interest debt before taking trading risk."),
        ],
        "terms": ["Position size", "Stop-loss", "Risk:reward", "Drawdown", "Diversification", "Emergency fund", "Leverage"],
        "quiz": [
            ("Capital ₹1,00,000, risk 2%. Max loss per trade?", ["₹200", "₹2,000", "₹20,000", "₹50,000"], 1, "2% of 1,00,000 = 2,000."),
            ("With a 1:2 risk-reward, you can be profitable even when you win…", ["Only 90% of trades", "About 40% of trades", "Never", "100% of trades"], 1,
             "Winning 2 units vs losing 1 means ~34%+ win rate breaks even (before costs)."),
            ("What should come before trading?", ["Emergency fund & insurance", "Max leverage", "Borrowing money", "Tips from social media"], 0,
             "Protect the basics first."),
        ],
    },
    {
        "id": "pf", "icon": "🏠", "title": "Personal finance foundations", "level": "Beginner", "minutes": 6,
        "sections": [
            ("Budget: 50/30/20", "A simple starting point: about 50% of take-home pay on needs, 30% on wants, 20% on savings and investments. Track it on the Income & Expenses page."),
            ("Emergency fund", "Keep 6 months of expenses in a savings account, sweep FD or liquid fund so a job loss or hospital bill does not force you to sell investments or borrow."),
            ("Insurance", "<b>Term life insurance</b> protects your family if you die; <b>health insurance</b> protects savings from medical bills. "
             "Buy insurance for protection, not as an investment."),
            ("Debt and credit score", "Pay credit card bills in full every month; card interest is very high. Paying EMIs on time builds a good credit score, which lowers future loan rates."),
            ("Nominees and documents", "Add nominees to every bank account, demat account, mutual fund and policy, and keep your family informed. SmartLife's Family & Nominees and Legacy Vault help with this."),
        ],
        "terms": ["Budget", "50/30/20", "Emergency fund", "Term insurance", "Health insurance", "Credit score", "Nominee"],
        "quiz": [
            ("A common emergency fund target is…", ["1 week of expenses", "6 months of expenses", "10 years of income", "Zero"], 1,
             "About 6 months of expenses is a widely used target."),
            ("Term insurance is mainly for…", ["Investment returns", "Protecting family income", "Tax only", "Buying a car"], 1,
             "Term insurance replaces income for your family if you die."),
            ("Best way to use a credit card:", ["Pay minimum due", "Pay full bill every month", "Never pay", "Withdraw cash"], 1,
             "Paying in full avoids high interest."),
        ],
    },
]
