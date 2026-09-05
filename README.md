# 🌾 KRISHI KENDRA (कृषि केंद्र)
### Direct Farm-to-Buyer Digital Agricultural Trade & Fulfilment Platform
**Smart India Hackathon (SIH 2026) | Problem Statement SIH26033**  
**Sponsoring Ministry:** Ministry of Consumer Affairs, Food & Public Distribution  

---

## 📖 1. Project Overview & Problem Addressed

In traditional Indian agricultural trade, 5–7 layers of intermediaries (village collectors, commission agents / *arhtiyas*, APMC traders, secondary wholesalers, sub-wholesalers, retailers) capture **65%–80%** of the consumer rupee, leaving smallholder farmers with only 20%–35% of the final price while driving retail food inflation.

**Krishi Kendra** eliminates exploitative middlemen by providing:
1. **Direct Farmer-to-Buyer Connectivity:** Smallholder farmers and FPOs connect directly with bulk buyers, institutional kitchens, supermarkets, and consumer buying clubs.
2. **Unified Buyer Model:** Buyers enter their required quantity (from 50 kg to 50 tonnes) without artificial account splits.
3. **Automated Matching Engine:** Smart rule-based matching based on product, available inventory, quantity range preferences, and district proximity.
4. **Transparent Price Discovery:** Real-time APMC Mandi rates (Agmarknet benchmark) displayed directly alongside buyer offer inputs and crop listings.
5. **Smart Decision Support & Counter-Negotiation:** Built-in Deal Fairness Assistant evaluates offers against live market rates to protect farmers from lowball bids.
6. **Tracked Fulfilment & Escrow Payouts:** Milk-run logistics coordination, assigned vehicle tracking, driver contact, and smart escrow security.
7. **Farmer Ecosystem Modules:** Cold Storage preservation locator, Input Supplies Marketplace (Seeds, Fertilizers, Sprayers), and Central/State Government Schemes bulletin board.
8. **Digital Visiting Card & Strict Privacy:** Shareable professional business cards with system-generated IDs (`FK-2026-XXXX` / `BK-2026-XXXX`) and opt-in phone sharing consent.
9. **Multilingual & Voice Copilot:** Built-in Hindi, Marathi, Tamil, Telugu, and English localization + voice commands via Web Speech API.

---

## 🛠️ 2. Technology Stack

- **Backend:** Python 3.11+ / Flask / Flask-SQLAlchemy / Flask-JWT-Extended / Werkzeug / Jinja2
- **Database:** SQLite (with SQLAlchemy ORM for clean zero-rewrite migration to PostgreSQL)
- **Frontend:** HTML5 / CSS3 / Vanilla JavaScript / Bootstrap 5 / FontAwesome
- **Speech & Audio:** Browser Native Web Speech API (Speech Recognition & Speech Synthesis)
- **Architecture:** Modular Blueprint design with clean separation of Models, Routes, Services, and Templates.

---

## 🚀 3. Quick Start & Local Setup

### Step 1: Clone and Navigate to Directory
```powershell
cd c:\Users\grant\Desktop\SIH
```

### Step 2: Install Python Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Seed Sample Demonstration Data
```powershell
python seed/sample_data.py
```

### Step 4: Start the Web Server
```powershell
python run.py
```
Open your web browser and visit: **`http://127.0.0.1:5000`**

---

## 🔑 4. Pre-Configured Demo Accounts

| Role | Mobile Number / Krishi ID | Password | Verification Status | Features to Test |
| :--- | :--- | :--- | :--- | :--- |
| **Farmer** | `9876543210` (`FK-2026-1001`) | `farmer123` | **Verified 🌟** | Inventory CRUD, Review Buyer Offers, Counter-Offer, Mandi Rates, Visiting Card, Transport Request |
| **Buyer** | `9876543220` (`BK-2026-2001`) | `buyer123` | **Verified ⭐** | Browse Crops, Post Requirement (Qty), Compare Offers, Historical Spend, Order Tracking |
| **Admin / Officer** | `9876543230` (`ADM-2026-001`) | `admin123` | **Authorized 🛡️** | Approve ID Verifications, Add Categories/Crops, Register Cold Storages, Publish Schemes, Dispute Mediation, Audit Logs |

*Note: For new user registrations, enter any 10-digit mobile number and use the instant demo OTP `123456`.*

---

## 🧪 5. Running Automated Tests

Run the full pytest suite to verify authentication, inventory CRUD, buyer requirement posting, matching engine, and order state machines:
```powershell
python -m pytest -v
```

---

## 📂 6. Project Directory Structure

```
SIH/
├── app.py / run.py          # Main application launcher & CLI
├── config.py                # Environment and app configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables sample
├── README.md                # Project documentation
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── extensions.py        # SQLAlchemy, JWT, CORS
│   ├── models.py            # Complete relational database models
│   ├── routes/
│   │   ├── main.py          # Landing page, i18n, visiting card
│   │   ├── auth.py          # Auth, OTP verification, profiles, privacy
│   │   ├── farmer.py        # Farmer dashboard, inventory, offers
│   │   ├── buyer.py         # Buyer dashboard, browse, requirements
│   │   ├── admin.py         # Admin portal, verification, schemes, disputes
│   │   ├── chat.py          # Order-linked chat & phone sharing
│   │   ├── orders.py        # Fulfilment timeline, invoices, disputes
│   │   ├── cold_storage.py  # Cold storage discovery & booking
│   │   ├── marketplace.py   # Farm input supplies (seeds, fertilizers)
│   │   ├── schemes.py       # Govt schemes & subsidies directory
│   │   └── api.py           # Mandi rate lookup, voice query, deal analysis
│   ├── services/
│   │   ├── otp_service.py   # OTP generation & verification
│   │   ├── mandi_service.py # APMC mandi rates query service
│   │   ├── matching_service.py # Requirement-to-farmer matching
│   │   ├── deal_analysis_service.py # Smart deal fairness analyzer
│   │   ├── notification_service.py # In-app notifications
│   │   └── audit_service.py # Administrative audit logger
│   ├── templates/           # Jinja2 responsive templates
│   └── static/              # CSS stylesheets, JS scripts, uploads
├── seed/
│   └── sample_data.py       # Indian agriculture seed dataset
└── tests/                   # Automated pytest suite
```
