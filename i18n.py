"""UI translations. Format per line: key | English | தமிழ் | Tanglish | हिन्दी | తెలుగు | ಕನ್ನಡ | മലയാളം
Lesson content in Learn is English; titles and UI are translated."""
import streamlit as st

LANGS = {"en": "English", "ta": "தமிழ்", "tg": "Tanglish", "hi": "हिन्दी", "te": "తెలుగు", "kn": "ಕನ್ನಡ", "ml": "മലയാളം"}
_ORDER = list(LANGS)

_RAW = """
tagline|Your whole financial life, in one place|உங்கள் முழு நிதி வாழ்க்கை, ஒரே இடத்தில்|Unga full financial life, oru idathula|आपकी पूरी वित्तीय ज़िंदगी, एक जगह|మీ పూర్తి ఆర్థిక జీవితం, ఒకే చోట|ನಿಮ್ಮ ಸಂಪೂರ್ಣ ಹಣಕಾಸು ಜೀವನ, ಒಂದೇ ಕಡೆ|നിങ്ങളുടെ മുഴുവൻ സാമ്പത്തിക ജീവിതം, ഒരിടത്ത്
grp_money|Money|பணம்|Panam|पैसा|డబ్బు|ಹಣ|പണം
grp_tools|Tools|கருவிகள்|Tools|टूल्स|టూల్స్|ಉಪಕರಣಗಳು|ടൂളുകൾ
grp_protect|Protect|பாதுகாப்பு|Protect|सुरक्षा|రక్షణ|ರಕ್ಷಣೆ|സംരക്ഷണം
grp_learn|Learn|கற்றல்|Learn|सीखें|నేర్చుకోండి|ಕಲಿಯಿರಿ|പഠിക്കുക
dashboard|Dashboard|டாஷ்போர்டு|Dashboard|डैशबोर्ड|డాష్‌బోర్డ్|ಡ್ಯಾಶ್‌ಬೋರ್ಡ್|ഡാഷ്ബോർഡ്
income_expenses|Income & Expenses|வருமானம் & செலவுகள்|Income & Expenses|आय और खर्च|ఆదాయం & ఖర్చులు|ಆದಾಯ & ಖರ್ಚು|വരുമാനം & ചെലവുകൾ
investments_assets|Investments & Assets|முதலீடுகள் & சொத்துகள்|Investments & Assets|निवेश और संपत्ति|పెట్టుబడులు & ఆస్తులు|ಹೂಡಿಕೆ & ಆಸ್ತಿ|നിക്ഷേപങ്ങൾ & ആസ്തികൾ
goals|Goals|இலக்குகள்|Goals|लक्ष्य|లక్ష్యాలు|ಗುರಿಗಳು|ലക്ഷ്യങ്ങൾ
calculators|Calculators|கணிப்பான்கள்|Calculators|कैलकुलेटर|కాలిక్యులేటర్లు|ಕ್ಯಾಲ್ಕುಲೇಟರ್‌ಗಳು|കാൽക്കുലേറ്ററുകൾ
futures|Futures Risk Calculator|ஃபியூச்சர்ஸ் ரிஸ்க் கணிப்பான்|Futures Risk Calculator|फ्यूचर्स रिस्क कैलकुलेटर|ఫ్యూచర్స్ రిస్క్ కాలిక్యులేటర్|ಫ್ಯೂಚರ್ಸ್ ರಿಸ್ಕ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್|ഫ്യൂച്ചേഴ്സ് റിസ്ക് കാൽക്കുലേറ്റർ
insurance|Health & Insurance|உடல்நலம் & காப்பீடு|Health & Insurance|स्वास्थ्य और बीमा|ఆరోగ్యం & బీమా|ಆರೋಗ್ಯ & ವಿಮೆ|ആരോഗ്യം & ഇൻഷുറൻസ്
family|Family & Nominees|குடும்பம் & நாமினிகள்|Family & Nominees|परिवार और नॉमिनी|కుటుంబం & నామినీలు|ಕುಟುಂಬ & ನಾಮಿನಿಗಳು|കുടുംബം & നോമിനികൾ
vault|Legacy Vault|லெகசி வால்ட்|Legacy Vault|लेगेसी वॉल्ट|లెగసీ వాల్ట్|ಲೆಗಸಿ ವಾಲ್ಟ್|ലെഗസി വോൾട്ട്
learn|Learn|கற்றல்|Learn|सीखें|నేర్చుకోండి|ಕಲಿಯಿರಿ|പഠിക്കുക
language|Language|மொழி|Language|भाषा|భాష|ಭಾಷೆ|ഭാഷ
dark_mode|Dark mode|இருண்ட பயன்முறை|Dark mode|डार्क मोड|డార్క్ మోడ్|ಡಾರ್ಕ್ ಮೋಡ್|ഡാർക്ക് മോഡ്
logout|Log out|வெளியேறு|Logout|लॉग आउट|లాగ్ అవుట్|ಲಾಗ್ ಔಟ್|ലോഗ് ഔട്ട്
signed_in_as|Signed in as|உள்நுழைந்தவர்|Logged in as|लॉग इन|లాగిన్ అయినవారు|ಲಾಗಿನ್ ಆದವರು|ലോഗിൻ ചെയ്തത്
login|Log in|உள்நுழை|Login|लॉग इन|లాగిన్|ಲಾಗಿನ್|ലോഗിൻ
signup|Sign up|பதிவு செய்|Sign up|साइन अप|సైన్ అప్|ಸೈನ್ ಅಪ್|സൈൻ അപ്പ്
email|Email|மின்னஞ்சல்|Email|ईमेल|ఈమెయిల్|ಇಮೇಲ್|ഇമെയിൽ
password|Password|கடவுச்சொல்|Password|पासवर्ड|పాస్‌వర్డ్|ಪಾಸ್‌ವರ್ಡ್|പാസ്‌വേഡ്
full_name|Full name|முழு பெயர்|Full name|पूरा नाम|పూర్తి పేరు|ಪೂರ್ಣ ಹೆಸರು|മുഴുവൻ പേര്
create_account|Create account|கணக்கை உருவாக்கு|Account create pannu|खाता बनाएं|ఖాతా సృష్టించండి|ಖಾತೆ ರಚಿಸಿ|അക്കൗണ്ട് സൃഷ്ടിക്കുക
login_error|Email or password is wrong.|மின்னஞ்சல் அல்லது கடவுச்சொல் தவறு.|Email or password thappu.|ईमेल या पासवर्ड गलत है।|ఈమెయిల్ లేదా పాస్‌వర్డ్ తప్పు.|ಇಮೇಲ್ ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ತಪ್ಪು.|ഇമെയിൽ അല്ലെങ്കിൽ പാസ്‌വേഡ് തെറ്റാണ്.
nominee_access|Nominee access|நாமினி அணுகல்|Nominee access|नॉमिनी एक्सेस|నామినీ యాక్సెస్|ನಾಮಿನಿ ಪ್ರವೇಶ|നോമിനി ആക്സസ്
demo_hint|Demo login: demo@smartlife.app / demo1234|டெமோ: demo@smartlife.app / demo1234|Demo login: demo@smartlife.app / demo1234|डेमो लॉगिन: demo@smartlife.app / demo1234|డెమో: demo@smartlife.app / demo1234|ಡೆಮೊ: demo@smartlife.app / demo1234|ഡെമോ: demo@smartlife.app / demo1234
hello|Hello|வணக்கம்|Vanakkam|नमस्ते|నమస్తే|ನಮಸ್ಕಾರ|നമസ്കാരം
net_worth|Net worth|நிகர மதிப்பு|Net worth|कुल संपत्ति|నికర విలువ|ನಿವ್ವಳ ಮೌಲ್ಯ|ആകെ മൂല്യം
monthly_income|Monthly income|மாத வருமானம்|Monthly income|मासिक आय|నెలవారీ ఆదాయం|ಮಾಸಿಕ ಆದಾಯ|പ്രതിമാസ വരുമാനം
monthly_expenses|Monthly expenses|மாத செலவுகள்|Monthly expenses|मासिक खर्च|నెలవారీ ఖర్చులు|ಮಾಸಿಕ ಖರ್ಚು|പ്രതിമാസ ചെലവ്
savings_rate|Savings rate|சேமிப்பு விகிதம்|Savings rate|बचत दर|పొదుపు రేటు|ಉಳಿತಾಯ ದರ|സമ്പാദ്യ നിരക്ക്
health_score|Financial health score|நிதி ஆரோக்கிய மதிப்பெண்|Financial health score|वित्तीय स्वास्थ्य स्कोर|ఆర్థిక ఆరోగ్య స్కోర్|ಹಣಕಾಸು ಆರೋಗ್ಯ ಅಂಕ|സാമ്പത്തിക ആരോഗ്യ സ്കോർ
emergency_months|Emergency fund (months)|அவசர நிதி (மாதங்கள்)|Emergency fund (months)|आपातकालीन फंड (महीने)|అత్యవసర నిధి (నెలలు)|ತುರ್ತು ನಿಧಿ (ತಿಂಗಳು)|അടിയന്തര ഫണ്ട് (മാസം)
upcoming|Upcoming payments & renewals|வரவிருக்கும் கட்டணங்கள்|Upcoming payments & renewals|आगामी भुगतान और नवीनीकरण|రాబోయే చెల్లింపులు|ಮುಂಬರುವ ಪಾವತಿಗಳು|വരാനിരിക്കുന്ന പേയ്‌മെന്റുകൾ
nothing_due|Nothing due in the next 30 days.|அடுத்த 30 நாட்களில் எதுவும் இல்லை.|Next 30 days la edhuvum illa.|अगले 30 दिनों में कुछ बकाया नहीं।|రాబోయే 30 రోజుల్లో ఏమీ లేదు.|ಮುಂದಿನ 30 ದಿನಗಳಲ್ಲಿ ಏನೂ ಇಲ್ಲ.|അടുത്ത 30 ദിവസം ഒന്നുമില്ല.
income_vs_exp|Income vs expenses|வருமானம் vs செலவு|Income vs expenses|आय बनाम खर्च|ఆదాయం vs ఖర్చు|ಆದಾಯ vs ಖರ್ಚು|വരുമാനം vs ചെലവ്
exp_by_cat|This month by category|இந்த மாதம் வகைவாரியாக|Indha month category wise|इस महीने श्रेणी अनुसार|ఈ నెల వర్గాల వారీగా|ಈ ತಿಂಗಳು ವರ್ಗವಾರು|ഈ മാസം വിഭാഗം തിരിച്ച്
recent|Recent transactions|சமீபத்திய பரிவர்த்தனைகள்|Recent transactions|हाल के लेन-देन|ఇటీవలి లావాదేవీలు|ಇತ್ತೀಚಿನ ವಹಿವಾಟುಗಳು|സമീപകാല ഇടപാടുകൾ
no_data|No data yet. Add your first entry or load sample data.|இன்னும் தரவு இல்லை. முதல் பதிவைச் சேர்க்கவும்.|Innum data illa. First entry add pannunga.|अभी कोई डेटा नहीं। पहली एंट्री जोड़ें।|ఇంకా డేటా లేదు. మొదటి ఎంట్రీ జోడించండి.|ಇನ್ನೂ ಡೇಟಾ ಇಲ್ಲ. ಮೊದಲ ಎಂಟ್ರಿ ಸೇರಿಸಿ.|ഇതുവരെ ഡാറ്റ ഇല്ല. ആദ്യ എൻട്രി ചേർക്കുക.
load_sample|Load sample data|மாதிரி தரவை ஏற்று|Sample data load pannu|सैंपल डेटा लोड करें|నమూనా డేటా లోడ్ చేయండి|ಮಾದರಿ ಡೇಟಾ ಲೋಡ್ ಮಾಡಿ|സാമ്പിൾ ഡാറ്റ ലോഡ് ചെയ്യുക
add_new|Add new|புதிதாகச் சேர்|Pudhusa add pannu|नया जोड़ें|కొత్తది జోడించండి|ಹೊಸದು ಸೇರಿಸಿ|പുതിയത് ചേർക്കുക
type|Type|வகை|Type|प्रकार|రకం|ವಿಧ|തരം
income|Income|வருமானம்|Income|आय|ఆదాయం|ಆದಾಯ|വരുമാനം
expense|Expense|செலவு|Expense|खर्च|ఖర్చు|ಖರ್ಚು|ചെലവ്
category|Category|பிரிவு|Category|श्रेणी|వర్గం|ವರ್ಗ|വിഭാഗം
amount|Amount (₹)|தொகை (₹)|Amount (₹)|राशि (₹)|మొత్తం (₹)|ಮೊತ್ತ (₹)|തുക (₹)
date|Date|தேதி|Date|तारीख|తేదీ|ದಿನಾಂಕ|തീയതി
note|Note|குறிப்பு|Note|नोट|గమనిక|ಟಿಪ್ಪಣಿ|കുറിപ്പ്
save|Save|சேமி|Save|सेव करें|సేవ్ చేయండి|ಉಳಿಸಿ|സേവ് ചെയ്യുക
saved|Saved|சேமிக்கப்பட்டது|Saved|सेव हो गया|సేవ్ అయింది|ಉಳಿಸಲಾಗಿದೆ|സേവ് ചെയ്തു
delete|Delete|நீக்கு|Delete|हटाएं|తొలగించండి|ಅಳಿಸಿ|ഇല്ലാതാക്കുക
month|Month|மாதம்|Month|महीना|నెల|ತಿಂಗಳು|മാസം
all|All|அனைத்தும்|All|सभी|అన్నీ|ಎಲ್ಲಾ|എല്ലാം
savings|Savings|சேமிப்பு|Savings|बचत|పొదుపు|ಉಳಿತಾಯ|സമ്പാദ്യം
investments|Investments|முதலீடுகள்|Investments|निवेश|పెట్టుబడులు|ಹೂಡಿಕೆಗಳು|നിക്ഷേപങ്ങൾ
assets|Assets|சொத்துகள்|Assets|संपत्ति|ఆస్తులు|ಆಸ್ತಿಗಳು|ആസ്തികൾ
loans|Loans|கடன்கள்|Loans|ऋण|రుణాలు|ಸಾಲಗಳು|വായ്പകൾ
investment|Investment|முதலீடு|Investment|निवेश|పెట్టుబడి|ಹೂಡಿಕೆ|നിക്ഷേപം
asset|Asset|சொத்து|Asset|संपत्ति|ఆస్తి|ಆಸ್ತಿ|ആസ്തി
loan|Loan|கடன்|Loan|ऋण|రుణం|ಸಾಲ|വായ്പ
name|Name|பெயர்|Name|नाम|పేరు|ಹೆಸರು|പേര്
invested|Invested (₹)|முதலீடு (₹)|Invested (₹)|निवेश (₹)|పెట్టుబడి (₹)|ಹೂಡಿಕೆ (₹)|നിക്ഷേപിച്ചത് (₹)
current_value|Current value (₹)|தற்போதைய மதிப்பு (₹)|Current value (₹)|वर्तमान मूल्य (₹)|ప్రస్తుత విలువ (₹)|ಪ್ರಸ್ತುತ ಮೌಲ್ಯ (₹)|നിലവിലെ മൂല്യം (₹)
outstanding|Outstanding (₹)|நிலுவை (₹)|Outstanding (₹)|बकाया (₹)|బకాయి (₹)|ಬಾಕಿ (₹)|ബാക്കി (₹)
next_due|Next due date|அடுத்த நிலுவை தேதி|Next due date|अगली देय तिथि|తదుపరి గడువు|ಮುಂದಿನ ಗಡುವು|അടുത്ത അവസാന തീയതി
returns|returns|வருமானம்|returns|रिटर्न|రాబడి|ಆದಾಯ|റിട്ടേൺ
allocation|Asset allocation|சொத்து ஒதுக்கீடு|Asset allocation|एसेट एलोकेशन|ఆస్తి కేటాయింపు|ಆಸ್ತಿ ಹಂಚಿಕೆ|ആസ്തി വിന്യാസം
target_amount|Target amount (₹)|இலக்கு தொகை (₹)|Target amount (₹)|लक्ष्य राशि (₹)|లక్ష్య మొత్తం (₹)|ಗುರಿ ಮೊತ್ತ (₹)|ലക്ഷ്യ തുക (₹)
saved_so_far|Saved so far (₹)|இதுவரை சேமித்தது (₹)|Ippo varaikkum saved (₹)|अब तक बचत (₹)|ఇప్పటివరకు పొదుపు (₹)|ಈವರೆಗೆ ಉಳಿತಾಯ (₹)|ഇതുവരെ സമ്പാദിച്ചത് (₹)
target_date|Target date|இலக்கு தேதி|Target date|लक्ष्य तिथि|లక్ష్య తేదీ|ಗುರಿ ದಿನಾಂಕ|ലക്ഷ്യ തീയതി
monthly_needed|Monthly SIP needed|தேவையான மாத SIP|Monthly SIP venum|ज़रूरी मासिक SIP|అవసరమైన నెలవారీ SIP|ಬೇಕಾದ ಮಾಸಿಕ SIP|ആവശ്യമായ പ്രതിമാസ SIP
calc_note|Estimates only. Returns are not guaranteed.|மதிப்பீடுகள் மட்டுமே. வருமானம் உத்தரவாதம் இல்லை.|Estimates mattum. Returns guaranteed illa.|केवल अनुमान। रिटर्न की गारंटी नहीं।|అంచనాలు మాత్రమే. రాబడి హామీ లేదు.|ಅಂದಾಜು ಮಾತ್ರ. ಆದಾಯ ಖಾತರಿಯಿಲ್ಲ.|കണക്കുകൂട്ടൽ മാത്രം. റിട്ടേൺ ഉറപ്പില്ല.
monthly_sip|Monthly SIP (₹)|மாத SIP (₹)|Monthly SIP (₹)|मासिक SIP (₹)|నెలవారీ SIP (₹)|ಮಾಸಿಕ SIP (₹)|പ്രതിമാസ SIP (₹)
expected_return|Expected return (% p.a.)|எதிர்பார்க்கும் வருமானம் (%)|Expected return (% p.a.)|अपेक्षित रिटर्न (% वार्षिक)|ఆశించిన రాబడి (%)|ನಿರೀಕ್ಷಿತ ಆದಾಯ (%)|പ്രതീക്ഷിക്കുന്ന റിട്ടേൺ (%)
years|Years|ஆண்டுகள்|Years|वर्ष|సంవత్సరాలు|ವರ್ಷಗಳು|വർഷം
step_up|Yearly step-up (%)|ஆண்டு அதிகரிப்பு (%)|Yearly step-up (%)|वार्षिक स्टेप-अप (%)|వార్షిక పెంపు (%)|ವಾರ್ಷಿಕ ಹೆಚ್ಚಳ (%)|വാർഷിക വർധന (%)
total_invested|Total invested|மொத்த முதலீடு|Total invested|कुल निवेश|మొత్తం పెట్టుబడి|ಒಟ್ಟು ಹೂಡಿಕೆ|ആകെ നിക്ഷേപം
est_returns|Estimated returns|மதிப்பிடப்பட்ட வருமானம்|Estimated returns|अनुमानित रिटर्न|అంచనా రాబడి|ಅಂದಾಜು ಆದಾಯ|കണക്കാക്കിയ റിട്ടേൺ
future_value|Future value|எதிர்கால மதிப்பு|Future value|भविष्य मूल्य|భవిష్యత్ విలువ|ಭವಿಷ್ಯದ ಮೌಲ್ಯ|ഭാവി മൂല്യം
loan_amount|Loan amount (₹)|கடன் தொகை (₹)|Loan amount (₹)|ऋण राशि (₹)|రుణ మొత్తం (₹)|ಸಾಲದ ಮೊತ್ತ (₹)|വായ്പ തുക (₹)
interest_rate|Interest rate (% p.a.)|வட்டி விகிதம் (%)|Interest rate (% p.a.)|ब्याज दर (% वार्षिक)|వడ్డీ రేటు (%)|ಬಡ್ಡಿ ದರ (%)|പലിശ നിരക്ക് (%)
monthly_emi|Monthly EMI|மாத EMI|Monthly EMI|मासिक EMI|నెలవారీ EMI|ಮಾಸಿಕ EMI|പ്രതിമാസ EMI
total_interest|Total interest|மொத்த வட்டி|Total interest|कुल ब्याज|మొత్తం వడ్డీ|ಒಟ್ಟು ಬಡ್ಡಿ|ആകെ പലിശ
total_payment|Total payment|மொத்த கட்டணம்|Total payment|कुल भुगतान|మొత్తం చెల్లింపు|ಒಟ್ಟು ಪಾವತಿ|ആകെ തിരിച്ചടവ്
cost_today|Cost today (₹)|இன்றைய செலவு (₹)|Inniku cost (₹)|आज की लागत (₹)|నేటి ఖర్చు (₹)|ಇಂದಿನ ವೆಚ್ಚ (₹)|ഇന്നത്തെ ചെലവ് (₹)
inflation|Inflation (% p.a.)|பணவீக்கம் (%)|Inflation (% p.a.)|महंगाई (% वार्षिक)|ద్రవ్యోల్బణం (%)|ಹಣದುಬ್ಬರ (%)|പണപ്പെരുപ്പം (%)
fut_sub|Know your risk before you take the trade. Educational tool, not financial advice.|வர்த்தகத்திற்கு முன் உங்கள் ரிஸ்க்கை அறியுங்கள். கல்வி நோக்கம் மட்டும், நிதி ஆலோசனை அல்ல.|Trade edukkuradhukku munnaadi risk therinjukonga. Educational tool mattum, financial advice illa.|ट्रेड से पहले अपना जोखिम जानें। शैक्षिक टूल, वित्तीय सलाह नहीं।|ట్రేడ్‌కు ముందు రిస్క్ తెలుసుకోండి. విద్యా సాధనం, ఆర్థిక సలహా కాదు.|ಟ್ರೇಡ್ ಮೊದಲು ರಿಸ್ಕ್ ತಿಳಿಯಿರಿ. ಶೈಕ್ಷಣಿಕ ಸಾಧನ, ಹಣಕಾಸು ಸಲಹೆ ಅಲ್ಲ.|ട്രേഡിന് മുമ്പ് റിസ്ക് അറിയുക. പഠന ഉപകരണം, സാമ്പത്തിക ഉപദേശമല്ല.
crypto|Crypto|கிரிப்டோ|Crypto|क्रिप्टो|క్రిప్టో|ಕ್ರಿಪ್ಟೋ|ക്രിപ്റ്റോ
stocks_fno|Indian stocks & F&O|இந்திய பங்குகள் & F&O|Indian stocks & F&O|भारतीय शेयर और F&O|భారత స్టాక్స్ & F&O|ಭಾರತೀಯ ಷೇರು & F&O|ഇന്ത്യൻ ഓഹരികൾ & F&O
forex|Forex|அந்நியச் செலாவணி|Forex|फॉरेक्स|ఫారెక్స్|ಫಾರೆಕ್ಸ್|ഫോറെക്സ്
search_symbol|Type coin / stock name|காயின் / பங்கு பெயரை தட்டச்சு செய்யவும்|Coin / stock name type pannunga|कॉइन / स्टॉक नाम लिखें|కాయిన్ / స్టాక్ పేరు టైప్ చేయండి|ಕಾಯಿನ್ / ಷೇರು ಹೆಸರು ಟೈಪ್ ಮಾಡಿ|കോയിൻ / ഓഹരി പേര് ടൈപ്പ് ചെയ്യുക
get_price|Get live price|நேரடி விலை|Live price edu|लाइव कीमत लें|లైవ్ ధర పొందండి|ಲೈವ್ ಬೆಲೆ ಪಡೆಯಿರಿ|ലൈവ് വില നേടുക
ltp|Last traded price|கடைசி வர்த்தக விலை|Last traded price (LTP)|अंतिम ट्रेड मूल्य|చివరి ట్రేడ్ ధర|ಕೊನೆಯ ವಹಿವಾಟು ಬೆಲೆ|അവസാന ട്രേഡ് വില
use_as_entry|Use as entry price|நுழைவு விலையாகப் பயன்படுத்து|Entry price ah use pannu|एंट्री प्राइस के रूप में उपयोग करें|ఎంట్రీ ధరగా వాడండి|ಎಂಟ್ರಿ ಬೆಲೆಯಾಗಿ ಬಳಸಿ|എൻട്രി വിലയായി ഉപയോഗിക്കുക
price_fail|Live price not available right now. Check the name or enter the price manually.|நேரடி விலை இப்போது கிடைக்கவில்லை. பெயரைச் சரிபார்க்கவும்.|Live price ippo kidaikkala. Name check pannunga, illa manual ah podunga.|लाइव कीमत अभी उपलब्ध नहीं। नाम जांचें या कीमत खुद डालें।|లైవ్ ధర ఇప్పుడు అందుబాటులో లేదు. పేరు తనిఖీ చేయండి.|ಲೈವ್ ಬೆಲೆ ಈಗ ಲಭ್ಯವಿಲ್ಲ. ಹೆಸರು ಪರಿಶೀಲಿಸಿ.|ലൈവ് വില ഇപ്പോൾ ലഭ്യമല്ല. പേര് പരിശോധിക്കുക.
long|Long (buy)|லாங் (வாங்கு)|Long (buy)|लॉन्ग (खरीद)|లాంగ్ (కొనుగోలు)|ಲಾಂಗ್ (ಖರೀದಿ)|ലോങ് (വാങ്ങൽ)
short|Short (sell)|ஷார்ட் (விற்பனை)|Short (sell)|शॉर्ट (बिक्री)|షార్ట్ (అమ్మకం)|ಶಾರ್ಟ್ (ಮಾರಾಟ)|ഷോർട്ട് (വിൽപ്പന)
capital|Trading capital|வர்த்தக மூலதனம்|Trading capital|ट्रेडिंग पूंजी|ట్రేడింగ్ మూలధనం|ಟ್ರೇಡಿಂಗ್ ಬಂಡವಾಳ|ട്രേഡിംഗ് മൂലധനം
risk_pct|Risk per trade (%)|ஒரு வர்த்தக ரிஸ்க் (%)|Risk per trade (%)|प्रति ट्रेड जोखिम (%)|ఒక్కో ట్రేడ్ రిస్క్ (%)|ಪ್ರತಿ ಟ್ರೇಡ್ ರಿಸ್ಕ್ (%)|ഓരോ ട്രേഡിലെ റിസ്ക് (%)
entry|Entry price|நுழைவு விலை|Entry price|एंट्री प्राइस|ఎంట్రీ ధర|ಎಂಟ್ರಿ ಬೆಲೆ|എൻട്രി വില
stop_loss|Stop-loss|ஸ்டாப்-லாஸ்|Stop-loss|स्टॉप-लॉस|స్టాప్-లాస్|ಸ್ಟಾಪ್-ಲಾಸ್|സ്റ്റോപ്പ്-ലോസ്
target|Target|இலக்கு|Target|टारगेट|టార్గెట్|ಟಾರ್ಗೆಟ್|ടാർഗറ്റ്
leverage|Leverage (x)|லீவரேஜ் (x)|Leverage (x)|लीवरेज (x)|లీవరేజ్ (x)|ಲೀವರೇಜ್ (x)|ലിവറേജ് (x)
position_size|Position size|நிலை அளவு|Position size|पोजीशन साइज़|పొజిషన్ సైజ్|ಪೊಸಿಷನ್ ಗಾತ್ರ|പൊസിഷൻ സൈസ്
margin_needed|Margin needed|தேவையான மார்ஜின்|Margin needed|ज़रूरी मार्जिन|అవసరమైన మార్జిన్|ಬೇಕಾದ ಮಾರ್ಜಿನ್|ആവശ്യമായ മാർജിൻ
max_loss|Max loss (stop-loss hit)|அதிகபட்ச இழப்பு|Max loss (SL hit)|अधिकतम नुकसान|గరిష్ట నష్టం|ಗರಿಷ್ಠ ನಷ್ಟ|പരമാവധി നഷ്ടം
profit_target|Profit (target hit)|லாபம் (இலக்கு)|Profit (target hit)|मुनाफ़ा (टारगेट)|లాభం (టార్గెట్)|ಲಾಭ (ಟಾರ್ಗೆಟ್)|ലാഭം (ടാർഗറ്റ്)
liquidation|Liquidation price|லிக்விடேஷன் விலை|Liquidation price|लिक्विडेशन प्राइस|లిక్విడేషన్ ధర|ಲಿಕ್ವಿಡೇಶನ್ ಬೆಲೆ|ലിക്വിഡേഷൻ വില
risk_check|Risk check|ரிஸ்க் சரிபார்ப்பு|Risk check|जोखिम जांच|రిస్క్ తనిఖీ|ರಿಸ್ಕ್ ಪರಿಶೀಲನೆ|റിസ്ക് പരിശോധന
lots|Lots you can take|எடுக்கக்கூடிய லாட்கள்|Lots edukkalaam|आप कितने लॉट ले सकते हैं|తీసుకోగల లాట్లు|ತೆಗೆದುಕೊಳ್ಳಬಹುದಾದ ಲಾಟ್‌ಗಳು|എടുക്കാവുന്ന ലോട്ടുകൾ
lot_size|Lot size|லாட் அளவு|Lot size|लॉट साइज़|లాట్ సైజ్|ಲಾಟ್ ಗಾತ್ರ|ലോട്ട് സൈസ്
margin_per_lot|Margin per lot (₹)|ஒரு லாட் மார்ஜின் (₹)|Margin per lot (₹)|प्रति लॉट मार्जिन (₹)|లాట్‌కు మార్జిన్ (₹)|ಪ್ರತಿ ಲಾಟ್ ಮಾರ್ಜಿನ್ (₹)|ലോട്ടിന് മാർജിൻ (₹)
health_profile|Health profile|உடல்நல விவரம்|Health profile|स्वास्थ्य प्रोफ़ाइल|ఆరోగ్య ప్రొఫైల్|ಆರೋಗ್ಯ ಪ್ರೊಫೈಲ್|ആരോഗ്യ പ്രൊഫൈൽ
blood_group|Blood group|இரத்த வகை|Blood group|ब्लड ग्रुप|బ్లడ్ గ్రూప్|ರಕ್ತದ ಗುಂಪು|രക്തഗ്രൂപ്പ്
conditions|Medical conditions|மருத்துவ நிலைகள்|Medical conditions|चिकित्सा स्थितियां|వైద్య పరిస్థితులు|ವೈದ್ಯಕೀಯ ಸ್ಥಿತಿಗಳು|രോഗാവസ്ഥകൾ
allergies|Allergies|ஒவ்வாமைகள்|Allergies|एलर्जी|అలెర్జీలు|ಅಲರ್ಜಿಗಳು|അലർജികൾ
doctor|Family doctor|குடும்ப மருத்துவர்|Family doctor|फैमिली डॉक्टर|ఫ్యామిలీ డాక్టర్|ಕುಟುಂಬ ವೈದ್ಯ|കുടുംബ ഡോക്ടർ
policies|Insurance policies|காப்பீட்டு பாலிசிகள்|Insurance policies|बीमा पॉलिसी|బీమా పాలసీలు|ವಿಮಾ ಪಾಲಿಸಿಗಳು|ഇൻഷുറൻസ് പോളിസികൾ
policy_type|Policy type|பாலிசி வகை|Policy type|पॉलिसी प्रकार|పాలసీ రకం|ಪಾಲಿಸಿ ವಿಧ|പോളിസി തരം
insurer|Insurer|காப்பீட்டாளர்|Insurer|बीमा कंपनी|బీమా సంస్థ|ವಿಮಾ ಕಂಪನಿ|ഇൻഷുറർ
last4|Last 4 digits only|கடைசி 4 இலக்கங்கள் மட்டும்|Last 4 digits mattum|केवल अंतिम 4 अंक|చివరి 4 అంకెలు మాత్రమే|ಕೊನೆಯ 4 ಅಂಕಿಗಳು ಮಾತ್ರ|അവസാന 4 അക്കം മാത്രം
sum_assured|Cover amount (₹)|காப்பீட்டுத் தொகை (₹)|Cover amount (₹)|कवर राशि (₹)|కవర్ మొత్తం (₹)|ಕವರ್ ಮೊತ್ತ (₹)|കവർ തുക (₹)
premium|Yearly premium (₹)|ஆண்டு பிரீமியம் (₹)|Yearly premium (₹)|वार्षिक प्रीमियम (₹)|వార్షిక ప్రీమియం (₹)|ವಾರ್ಷಿಕ ಪ್ರೀಮಿಯಂ (₹)|വാർഷിക പ്രീമിയം (₹)
renewal|Renewal date|புதுப்பிப்பு தேதி|Renewal date|नवीनीकरण तिथि|రెన్యూవల్ తేదీ|ನವೀಕರಣ ದಿನಾಂಕ|പുതുക്കൽ തീയതി
members|Family members|குடும்ப உறுப்பினர்கள்|Family members|परिवार के सदस्य|కుటుంబ సభ్యులు|ಕುಟುಂಬ ಸದಸ್ಯರು|കുടുംബാംഗങ്ങൾ
relation|Relation|உறவு|Relation|रिश्ता|సంబంధం|ಸಂಬಂಧ|ബന്ധം
dob|Date of birth|பிறந்த தேதி|Date of birth|जन्म तिथि|పుట్టిన తేదీ|ಹುಟ್ಟಿದ ದಿನಾಂಕ|ജനനത്തീയതി
nominees|Nominees|நாமினிகள்|Nominees|नॉमिनी|నామినీలు|ನಾಮಿನಿಗಳು|നോമിനികൾ
nominee_for|Nominee for|எதற்கான நாமினி|Nominee for|किसके लिए नॉमिनी|దేనికి నామినీ|ಯಾವುದಕ್ಕೆ ನಾಮಿನಿ|ഏതിനുള്ള നോമിനി
share_pct|Share (%)|பங்கு (%)|Share (%)|हिस्सा (%)|వాటా (%)|ಪಾಲು (%)|വിഹിതം (%)
coverage_gap|Items without a nominee|நாமினி இல்லாதவை|Nominee illadhavai|बिना नॉमिनी वाले आइटम|నామినీ లేనివి|ನಾಮಿನಿ ಇಲ್ಲದವು|നോമിനി ഇല്ലാത്തവ
vault_sub|Encrypted records your nominees can access through a verified process.|சரிபார்க்கப்பட்ட முறையில் நாமினிகள் அணுகக்கூடிய மறைகுறியாக்கப்பட்ட பதிவுகள்.|Encrypted records, verified process vazhiya nominees ku kidaikkum.|एन्क्रिप्टेड रिकॉर्ड, सत्यापित प्रक्रिया से नॉमिनी को मिलेंगे।|ఎన్‌క్రిప్ట్ చేసిన రికార్డులు, ధృవీకరణ ద్వారా నామినీలకు.|ಎನ್‌ಕ್ರಿಪ್ಟ್ ದಾಖಲೆಗಳು, ಪರಿಶೀಲಿತ ಪ್ರಕ್ರಿಯೆಯಿಂದ ನಾಮಿನಿಗಳಿಗೆ.|എൻക്രിപ്റ്റ് ചെയ്ത രേഖകൾ, സ്ഥിരീകരിച്ച പ്രക്രിയയിലൂടെ നോമിനികൾക്ക്.
institution|Bank / institution|வங்கி / நிறுவனம்|Bank / institution|बैंक / संस्था|బ్యాంక్ / సంస్థ|ಬ್ಯಾಂಕ್ / ಸಂಸ್ಥೆ|ബാങ്ക് / സ്ഥാപനം
private_notes|Private notes (encrypted)|தனிப்பட்ட குறிப்புகள் (மறைகுறியாக்கம்)|Private notes (encrypted)|निजी नोट्स (एन्क्रिप्टेड)|ప్రైవేట్ నోట్స్ (ఎన్‌క్రిప్ట్)|ಖಾಸಗಿ ಟಿಪ್ಪಣಿ (ಎನ್‌ಕ್ರಿಪ್ಟ್)|സ്വകാര്യ കുറിപ്പ് (എൻക്രിപ്റ്റ്)
attach|Attach document (encrypted)|ஆவணம் இணை (மறைகுறியாக்கம்)|Document attach (encrypted)|दस्तावेज़ संलग्न करें (एन्क्रिप्टेड)|డాక్యుమెంట్ జత చేయండి|ದಾಖಲೆ ಲಗತ್ತಿಸಿ|ഡോക്യുമെന്റ് ചേർക്കുക
visible_to|Visible to nominees|நாமினிகளுக்குத் தெரியும்|Nominees ku theriyum|नॉमिनी को दिखेगा|నామినీలకు కనిపిస్తుంది|ನಾಮಿನಿಗಳಿಗೆ ಕಾಣುತ್ತದೆ|നോമിനികൾക്ക് കാണാം
release_rule|Release rule|வெளியீட்டு விதி|Release rule|रिलीज़ नियम|విడుదల నియమం|ಬಿಡುಗಡೆ ನಿಯಮ|റിലീസ് നിയമം
inactivity|Release after inactivity (days)|செயலற்ற நிலைக்குப் பின் வெளியீடு (நாட்கள்)|Inactive aana apram release (days)|निष्क्रियता के बाद रिलीज़ (दिन)|నిష్క్రియత తర్వాత విడుదల (రోజులు)|ನಿಷ್ಕ್ರಿಯತೆಯ ನಂತರ ಬಿಡುಗಡೆ (ದಿನ)|നിഷ്ക്രിയതയ്ക്ക് ശേഷം റിലീസ് (ദിവസം)
access_code|Access code|அணுகல் குறியீடு|Access code|एक्सेस कोड|యాక్సెస్ కోడ్|ಪ್ರವೇಶ ಕೋಡ್|ആക്സസ് കോഡ്
gen_code|Generate access code|குறியீட்டை உருவாக்கு|Access code generate pannu|एक्सेस कोड बनाएं|కోడ్ సృష్టించండి|ಕೋಡ್ ರಚಿಸಿ|കോഡ് സൃഷ്ടിക്കുക
lessons|Lessons|பாடங்கள்|Lessons|पाठ|పాఠాలు|ಪಾಠಗಳು|പാഠങ്ങൾ
quiz|Quick quiz|சிறு வினாடி வினா|Quick quiz|क्विक क्विज़|క్విక్ క్విజ్|ಕ್ವಿಕ್ ಕ್ವಿಜ್|ക്വിക്ക് ക്വിസ്
check|Check answers|பதில்களைச் சரிபார்|Answers check pannu|उत्तर जांचें|సమాధానాలు చూడండి|ಉತ್ತರ ಪರಿಶೀಲಿಸಿ|ഉത്തരം പരിശോധിക്കുക
completed|Completed|முடிந்தது|Completed|पूरा|పూర్తయింది|ಪೂರ್ಣಗೊಂಡಿದೆ|പൂർത്തിയായി
progress|Progress|முன்னேற்றம்|Progress|प्रगति|పురోగతి|ಪ್ರಗತಿ|പുരോഗതി
lesson_lang_note|Lesson text is in English. Menus follow your language.|பாட உரை ஆங்கிலத்தில் உள்ளது.|Lesson text English la irukku.|पाठ अंग्रेज़ी में है।|పాఠం ఇంగ్లీష్‌లో ఉంది.|ಪಾಠ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿದೆ.|പാഠം ഇംഗ്ലീഷിലാണ്.
budget_daily|Budget & Daily|பட்ஜெட் & தினசரி|Budget & Daily|बजट और दैनिक|బడ్జెట్ & రోజువారీ|ಬಜೆಟ್ & ದೈನಂದಿನ|ബജറ്റ് & ദിവസേന
today|Today|இன்று|Inniku|आज|ఈరోజు|ಇಂದು|ഇന്ന്
budgets|Budgets|பட்ஜெட்கள்|Budgets|बजट|బడ్జెట్లు|ಬಜೆಟ್‌ಗಳು|ബജറ്റുകൾ
averages|Averages|சராசரிகள்|Averages|औसत|సగటులు|ಸರಾಸರಿಗಳು|ശരാശരികൾ
spent_today|Spent today|இன்றைய செலவு|Inniku selavu|आज का खर्च|ఈరోజు ఖర్చు|ಇಂದಿನ ಖರ್ಚು|ഇന്നത്തെ ചെലവ്
daily_allowance|Daily allowance|தினசரி வரம்பு|Daily allowance|दैनिक सीमा|రోజువారీ పరిమితి|ದೈನಂದಿನ ಮಿತಿ|ദൈനംദിന പരിധി
monthly_limit|Monthly limit (₹)|மாத வரம்பு (₹)|Monthly limit (₹)|मासिक सीमा (₹)|నెలవారీ పరిమితి (₹)|ಮಾಸಿಕ ಮಿತಿ (₹)|പ്രതിമാസ പരിധി (₹)
budget_alerts|Budget alerts|பட்ஜெட் எச்சரிக்கைகள்|Budget alerts|बजट अलर्ट|బడ్జెట్ హెచ్చరికలు|ಬಜೆಟ್ ಎಚ್ಚರಿಕೆಗಳು|ബജറ്റ് അലേർട്ടുകൾ
avg_daily_spend|Average daily spend|சராசரி தினசரி செலவு|Average daily spend|औसत दैनिक खर्च|సగటు రోజువారీ ఖర్చు|ಸರಾಸರಿ ದೈನಂದಿನ ಖರ್ಚು|ശരാശരി ദൈനംദിന ചെലവ്
avg_monthly_savings|Average monthly savings|சராசரி மாத சேமிப்பு|Average monthly savings|औसत मासिक बचत|సగటు నెలవారీ పొదుపు|ಸರಾಸರಿ ಮಾಸಿಕ ಉಳಿತಾಯ|ശരാശരി പ്രതിമാസ സമ്പാദ്യം
markets|Markets & News|சந்தை & செய்திகள்|Markets & News|बाज़ार और समाचार|మార్కెట్లు & వార్తలు|ಮಾರುಕಟ್ಟೆ & ಸುದ್ದಿ|വിപണി & വാർത്തകൾ
toolkit|Money Toolkit|பண கருவிப்பெட்டி|Money Toolkit|मनी टूलकिट|మనీ టూల్‌కిట్|ಹಣದ ಟೂಲ್‌ಕಿಟ್|മണി ടൂൾകിറ്റ്
fitness|Fitness|உடற்தகுதி|Fitness|फिटनेस|ఫిట్‌నెస్|ಫಿಟ್‌ನೆಸ್|ഫിറ്റ്നസ്
watchlist|Watchlist|கண்காணிப்பு பட்டியல்|Watchlist|वॉचलिस्ट|వాచ్‌లిస్ట్|ವಾಚ್‌ಲಿಸ್ಟ್|വാച്ച്‌ലിസ്റ്റ്
news|Market news|சந்தை செய்திகள்|Market news|बाज़ार समाचार|మార్కెట్ వార్తలు|ಮಾರುಕಟ್ಟೆ ಸುದ್ದಿ|വിപണി വാർത്തകൾ
quick_goal|Quick start a goal|இலக்கை விரைவாகத் தொடங்கு|Quick ah goal start pannu|जल्दी लक्ष्य शुरू करें|త్వరగా లక్ష్యం ప్రారంభించండి|ಬೇಗ ಗುರಿ ಪ್ರಾರಂಭಿಸಿ|വേഗത്തിൽ ലക്ഷ്യം തുടങ്ങുക
"""

T = {}
for line in _RAW.strip().splitlines():
    parts = line.split("|")
    T[parts[0]] = dict(zip(_ORDER, parts[1:]))


def lang() -> str:
    return st.session_state.get("lang", "en")


def t(key: str) -> str:
    row = T.get(key)
    if row is None:
        return key
    return row.get(lang()) or row["en"]
