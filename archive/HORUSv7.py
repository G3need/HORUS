import os
import sys
import subprocess
import time
import warnings
import shutil
import logging
import threading

# Configure System-Level Logging for Military-Grade Traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("HORUS_SYSTEM")

# Suppress harmless warnings
warnings.filterwarnings("ignore")

# ------------------------------------------------------------------------------
# 🛠️ SYSTEM PREP: INFRASTRUCTURE DEPLOYMENT
# ------------------------------------------------------------------------------
def install_dependencies():
    system_packages = [
        "gradio", 
        "qrcode", 
        "reportlab", 
        "google-genai" 
    ]
    
    print("⚡ [SYSTEM] INITIATING TACTICAL DEPENDENCY DEPLOYMENT...")
    for package in system_packages:
        try:
            pkg_name = package.replace("-", ".") if "google" not in package else "google.genai"
            if package == "google-genai": 
                import google.genai
            else:
                __import__(pkg_name)
        except ImportError:
            print(f"⚙️ [INSTALL] Deploying {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("✅ [SYSTEM] INFRASTRUCTURE SECURED.\n")

install_dependencies()

# ------------------------------------------------------------------------------
# 📚 IMPORTS
# ------------------------------------------------------------------------------
import gradio as gr
import sqlite3
import hashlib
import datetime
import json
import random
import qrcode
import numpy as np
from typing import List, Tuple
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from google import genai 

# ==============================================================================
# 🏛️ HORUS KEY: STRATEGIC CONFIGURATION
# ==============================================================================

class HorusConfig:
    APP_NAME = "HORUS KEY | Egypt Smart Travel Ecosystem"
    VERSION = "7.0.0-GrandMaster (S-Tier)"
    DB_NAME = "horus_core.db"
    
    # 🐙 GITHUB IDENTITY
    GIT_USER_EMAIL = "ahmedgeneed@gmail.com"
    GIT_USER_NAME = "Horus Architect"
    REPO_OWNER = "G3need"
    REPO_NAME = "HORUS"
    
    # 💾 LOCAL WORKSPACE
    PROJECT_ROOT = "/content/HORUS_REPO"
    
    # 🧠 AI CONFIG (LOCKED)
    AI_MODEL = "gemini-3-flash-preview"
    
    # 🛂 VISA ON ARRIVAL ELIGIBILITY (2026 DOCTRINE)
    VOA_ELIGIBLE_COUNTRIES = {
        # North America
        "USA", "Canada",
        # Europe (EU + UK + Schengen)
        "UK", "Germany", "France", "Italy", "Spain", "Netherlands", "Belgium", 
        "Austria", "Sweden", "Denmark", "Norway", "Finland", "Poland", 
        "Czech Republic", "Hungary", "Portugal", "Greece", "Ireland", 
        "Switzerland", "Luxembourg", "Slovakia", "Slovenia", "Estonia", 
        "Latvia", "Lithuania", "Malta", "Cyprus", "Bulgaria", "Romania", 
        "Croatia", "Iceland", "Liechtenstein",
        # Asia Pacific
        "Japan", "Australia", "New Zealand", "South Korea", "Singapore", 
        "Malaysia", "Hong Kong", "Taiwan",
        # Middle East (Selected)
        "UAE", "Saudi Arabia", "Qatar", "Kuwait", "Bahrain", "Oman",
        # Others
        "Russia", "Turkey", "Israel"
    }
    
    # 🚫 RESTRICTED NATIONALITIES (BLOCKED FROM VISA & PAYMENT)
    RESTRICTED_COUNTRIES = {
        "Iran", "Afghanistan", "Syria", "Yemen", "Libya", "Somalia", 
        "North Korea", "Sudan", "Lebanon", "Iraq", "Palestine"
    }
    
    # 💰 PRICING MATRIX (EGP)
    PRICING = {
        "foreigner_adult": 1000,
        "foreigner_student": 500,
        "arab_egyptian": 100,
        "visa_fee": 1250  # $25 USD * 50 EGP conversion rate
    } 

# ==============================================================================
# 📝 DOCUMENTATION ENGINE (AUTO-README)
# ==============================================================================

class ReadmeGenerator:
    """Automatically generates the project documentation file."""
    
    @staticmethod
    def generate():
        content = f"""# Horus Key – Egypt’s Smart Digital Travel Ecosystem 👁️

**Revolutionizing Border Management & Tourism Services**

> **Submitted by:** Mohamed Sayed Hassan Sayed Ahmed
> **Version:** {HorusConfig.VERSION}

---

## 📋 Executive Summary
**Horus Key** is a comprehensive digital platform that modernizes border entry, enhances the traveler experience, and boosts Egypt’s tourism economy. It integrates arrival cards, visas, payments, transportation, and tourism services into one unified system.

## 🚀 Objectives
1. **Seamless Ecosystem:** Establish a unified digital travel platform.
2. **Paperless Borders:** Eliminate manual paperwork.
3. **Integration:** Combine 10+ core traveler services.
4. **Economic Growth:** Enhance tourism revenue and global image.
5. **Security:** Support government efficiency and data sovereignty.

## 🛠️ Integrated Services (The Ecosystem)

### 🛂 Identity & Border Control
* **4.A Digital Arrival Card:** Paperless entry requirements.
* **4.B Visa upon Arrival (Digital Stamp):** Pre-payment and instant digital issuance.
* **4.I QR Reader & Access:** Secure, contactless verification.

### 💳 Financial Infrastructure
* **4.C Mobile Wallet:** Multi-currency support and cashless payments.
* **4.G Discounts & Offers:** Exclusive deals for app users.

### 🚕 Mobility & Transport
* **4.D Online Booking:** Airport transfers and rides.
* **4.E Eco-Travel Integration:** Metro, Electric Bus, and Monorail with "Green Score" rewards.

### 🏛️ Tourism & Heritage
* **4.F Monument Ticketing:** Instant access to Pyramids, Museums, and Temples.
* **4.J Souvenir Marketplace:** Verified local artisans and authentic products.

### 📶 Connectivity
* **4.H eSIM & Mobile Data:** Instant local connectivity upon arrival.

---

## 🤖 Technology Stack
* **Core:** Python 3.10+
* **UI Framework:** Gradio (High-Performance Dashboard)
* **AI Engine:** Google Gemini ({HorusConfig.AI_MODEL})
* **Database:** SQLite (Relational Monolith)
* **Security:** SHA-512 Biometric Hashing & SHA-256 Digital Stamps
* **Docs:** ReportLab PDF Generation

## 📦 Installation & Usage
This system is designed for deployment in high-availability environments (Google Colab / Cloud Run).

1.  **Clone Repository:** `git clone https://github.com/G3need/HORUS.git`
2.  **Install Deps:** `pip install -r requirements.txt`
3.  **Run:** `python app.py`

---

## 🛡️ Risk Management
* **Technical:** Redundant backup servers and phased rollouts.
* **Data Security:** End-to-end encryption (GDPR/Egyptian Data Protection Law).
* **Adoption:** User-friendly biometric onboarding.

## ⚖️ Compliance
Operates within regulations of:
* Ministry of Tourism & Antiquities
* Ministry of Communications & IT
* Central Bank of Egypt (Digital Payments)

---
*“HORUS KEY - Opening the Gateway to Smart Tourism.”*
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("📄 README.md generated successfully.")

# ==============================================================================
# 🔐 LEVEL 1: SECURITY & IDENTITY
# ==============================================================================

class HorusSecurity:
    """
    Implements Section 4.A & 4.B: Biometric Identity & Digital Entry.
    """
    @staticmethod
    def scan_face(image: np.ndarray) -> str:
        if image is None: return None
        try:
            # Cryptographic hash of biometric data
            image_bytes = image.tobytes()
            bio_hash = hashlib.sha512(image_bytes).hexdigest().upper()[:32]
            logger.info(f"Biometric Scan Complete: {bio_hash}")
            return f"BIO-{bio_hash}"
        except Exception as e:
            logger.error(f"Biometric Failure: {e}")
            return f"BIO-MOCK-{random.randint(1000,9999)}"

    @staticmethod
    def generate_digital_stamp(passport_number: str, nationality: str) -> tuple:
        timestamp = datetime.datetime.now().isoformat()
        raw_string = f"{passport_number}:{nationality}:{timestamp}:HORUS_SECURE"
        digital_stamp = hashlib.sha256(raw_string.encode()).hexdigest().upper()[:24]
        return digital_stamp, timestamp

# ==============================================================================
# 🧠 LEVEL 2: ECO ENGINE & MARKETPLACE
# ==============================================================================

class EcoEngine:
    """Implements Section 4.D & 4.E: Sustainable Transport Logic."""
    @staticmethod
    def calculate_impact(mode: str) -> tuple:
        # High Reward (+20 pts): Cairo Monorail, LRT (Light Rail), Electric Bus
        if mode in ["Cairo Monorail", "LRT (Electric Train)", "Electric Bus"]:
            return 20, "High (Green) 🌿"
        # Medium Reward (+10 pts): Cairo Metro (Lines 1-3)
        elif mode in ["Metro Line 1", "Metro Line 2", "Metro Line 3"]:
            return 10, "Medium ⚠️"
        # No Reward (0 pts): Private Car, Taxi, Standard Uber
        elif mode in ["Gas-Powered Taxi", "Private Car", "Standard Uber"]:
            return 0, "Low 💨"
        # Fallback for legacy transport modes
        elif mode in ["Shared Shuttle", "Train"]:
            return 10, "Medium ⚠️"
        return 0, "Low 💨"

class MarketplaceEngine:
    """Implements Section 4.H (Connectivity) & 4.J (Souvenirs)."""
    @staticmethod
    def get_esims():
        return [
            ("Orange Tourist Line", "50GB Data + 200 Local Mins", 500),
            ("Vodafone Red Traveler", "40GB Data + Int'l Calls", 550),
            ("WE Data Pass", "Unlimited Social Media", 400),
            ("Etisalat Emerald", "VIP Connection", 600)
        ]
        
    @staticmethod
    def get_souvenirs():
        return [
            ("Papyrus Scroll (Auth)", "Hand-painted Giza Art", 250),
            ("Alabaster Vase", "Luxor Craftsman", 450),
            ("Silver Cartouche", "Custom Name (Hieroglyphs)", 1200),
            ("Organic Spice Box", "Aswan Market", 150),
            ("Cotton Galabeya", "Egyptian Cotton", 600)
        ]
    
    @staticmethod
    def get_exclusive_offers():
        """Section 4.G: Discounts & Offers"""
        return [
            ("Nile Ritz Carlton", "15% Off Spa", "Hotel"),
            ("Uber Egypt", "50 EGP Ride Voucher", "Transport"),
            ("Sound & Light Show", "Buy 1 Get 1 Free", "Entertainment")
        ]

# ==============================================================================
# 📄 LEVEL 3: OFFICIAL DOCUMENTATION
# ==============================================================================

class DocumentIssuer:
    @staticmethod
    def generate_visa_pdf(traveler_info: dict, stamp: str, qr_data: str) -> str:
        filename = f"EGYPT_VISA_{traveler_info['passport']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Design Elements
        c.setLineWidth(5)
        c.setStrokeColorRGB(0.6, 0.5, 0.1) # Gold border
        c.rect(0.5 * inch, 0.5 * inch, 7.5 * inch, 10 * inch)
        
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(4.25 * inch, 10 * inch, "ARAB REPUBLIC OF EGYPT")
        c.setFont("Helvetica", 16)
        c.drawCentredString(4.25 * inch, 9.6 * inch, "MINISTRY OF INTERIOR - E-VISA")
        
        y = 8.5
        details = [
            f"FULL NAME: {traveler_info['name']}",
            f"PASSPORT NO: {traveler_info['passport']}",
            f"NATIONALITY: {traveler_info['nationality']}",
            f"VISA CLASS: T-1 (TOURIST)",
            f"DIGITAL STAMP: {stamp}",
            f"ISSUED: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        ]
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0,0,0)
        for line in details:
            c.drawString(1 * inch, y * inch, line)
            y -= 0.5
            
        # QR Generation
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 1 * inch, 4 * inch, width=3*inch, height=3*inch)
        
        c.drawString(1 * inch, 3.5 * inch, "VALID FOR ENTRY AT ALL BORDERS")
        c.save()
        return filename

# ==============================================================================
# 💾 LEVEL 4: THE MONOLITH (DATABASE)
# ==============================================================================

class HorusDB:
    def __init__(self):
        self.conn = sqlite3.connect(HorusConfig.DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_schema()
        self._seed_monolith()

    def _init_schema(self):
        # Tables covering all 10 ecosystem services including Section 4.F (Monuments)
        tables = [
            'CREATE TABLE IF NOT EXISTS travelers (id INTEGER PRIMARY KEY, name TEXT, passport_number TEXT UNIQUE, nationality TEXT, biometric_hash TEXT, wallet_balance REAL DEFAULT 0, green_points INTEGER DEFAULT 0, created_at TEXT)',
            'CREATE TABLE IF NOT EXISTS visas (id INTEGER PRIMARY KEY, traveler_id INT, visa_type TEXT, digital_stamp TEXT, status TEXT, issued_at TEXT)',
            'CREATE TABLE IF NOT EXISTS monuments (id INTEGER PRIMARY KEY, name TEXT, location TEXT, price_egp REAL, description TEXT, image_emoji TEXT)',
            'CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, traveler_id INT, service_type TEXT, amount REAL, details TEXT, timestamp TEXT)',
            'CREATE TABLE IF NOT EXISTS marketplace_orders (id INTEGER PRIMARY KEY, traveler_id INT, item_name TEXT, category TEXT, price REAL, status TEXT)'
        ]
        for t in tables:
            self.cursor.execute(t)
        self.conn.commit()

    def _seed_monolith(self):
        # Implements 4.F: Monument & Museum Tickets
        if self.cursor.execute("SELECT count(*) FROM monuments").fetchone()[0] == 0:
            monuments = [
                ("Great Pyramid", "Giza", 540, "Ancient Wonder", "🔺"), 
                ("Karnak Temple", "Luxor", 450, "Temple Complex", "⛩️"), 
                ("GEM Museum", "Giza", 1200, "Grand Museum", "🏛️"),
                ("Valley of Kings", "Luxor", 600, "Royal Tombs", "⚰️"),
                ("Abu Simbel", "Aswan", 620, "Ramesses II", "🗿")
            ]
            self.cursor.executemany("INSERT INTO monuments (name, location, price_egp, description, image_emoji) VALUES (?, ?, ?, ?, ?)", monuments)
        self.conn.commit()

    # --- CRUD Operations ---
    def register_traveler(self, name, passport, nationality, bio_hash):
        try:
            self.cursor.execute("INSERT INTO travelers (name, passport_number, nationality, biometric_hash, created_at) VALUES (?, ?, ?, ?, ?)", (name, passport, nationality, bio_hash, datetime.datetime.now().isoformat()))
            self.conn.commit()
            return self.cursor.lastrowid
        except:
            self.cursor.execute("SELECT id FROM travelers WHERE passport_number=?", (passport,))
            return self.cursor.fetchone()[0]

    def get_traveler(self, tid):
        return self.cursor.execute("SELECT * FROM travelers WHERE id=?", (tid,)).fetchone()

    def purchase(self, tid, item, cost, cat):
        bal = self.get_traveler(tid)[5]
        if bal >= cost:
            self.cursor.execute("UPDATE travelers SET wallet_balance = wallet_balance - ? WHERE id=?", (cost, tid))
            self.cursor.execute("INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", (tid, cat, -cost, item, datetime.datetime.now().isoformat()))
            self.conn.commit()
            return True
        return False

    def add_green_points(self, tid, points):
        self.cursor.execute("UPDATE travelers SET green_points = green_points + ? WHERE id=?", (points, tid))
        self.conn.commit()

    def add_visa(self, tid, stamp):
        self.cursor.execute("INSERT INTO visas (traveler_id, visa_type, digital_stamp, status, issued_at) VALUES (?, ?, ?, ?, ?)", (tid, "TOURIST", stamp, "ACTIVE", datetime.datetime.now().isoformat()))
        self.conn.commit()

    def get_data(self, table):
        return self.cursor.execute(f"SELECT * FROM {table}").fetchall()
        
    def top_up(self, tid, amt):
        self.cursor.execute("UPDATE travelers SET wallet_balance = wallet_balance + ? WHERE id=?", (amt, tid))
        self.cursor.execute("INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", (tid, "TOPUP", amt, "Load", datetime.datetime.now().isoformat()))
        self.conn.commit()

db = HorusDB()

# ==============================================================================
# 🔄 LEVEL 5: GIT AUTOPILOT (VERBOSE DIAGNOSTICS)
# ==============================================================================

class GitAutopilot:
    @staticmethod
    def sync_codebase():
        logs = ["🚀 Starting DIAGNOSTIC Force Sync..."]
        try:
            from google.colab import userdata
            pat = userdata.get('GITHUB_PAT')
        except:
            return "❌ CRITICAL: 'GITHUB_PAT' Secret missing in Colab."
            
        if not pat: return "❌ CRITICAL: PAT is empty/null."

        # Auth URL construction
        repo_url = f"https://{pat}@github.com/{HorusConfig.REPO_OWNER}/{HorusConfig.REPO_NAME}.git"
        root = HorusConfig.PROJECT_ROOT
        
        def run(cmd, cwd=None):
            try:
                # Capture STDOUT and STDERR for debugging
                res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
                if res.returncode != 0:
                    logs.append(f"⚠️ FAIL: {cmd}")
                    logs.append(f"   └── STDERR: {res.stderr.strip()}")
                    return False
                logs.append(f"✅ OK: {cmd}")
                return True
            except Exception as e:
                logs.append(f"❌ EXCEPTION: {e}")
                return False

        # 0. GENERATE README
        ReadmeGenerator.generate()

        # 1. CLEAN & INIT
        if os.path.exists(root):
            shutil.rmtree(root)
        os.makedirs(root, exist_ok=True)
        logs.append(f"📂 Workspace: {root}")

        run("git init", cwd=root)
        run("git checkout -b main", cwd=root)

        # 2. STAGE FILES
        files_to_sync = ["app.py", "horus_core.db", "README.md"]
        for f in files_to_sync:
            if os.path.exists(f):
                shutil.copy(f, f"{root}/{f}")
                logs.append(f"📄 Staged: {f}")
            else:
                logs.append(f"⚠️ MISSING: {f} (Cannot sync)")

        # 3. IDENTITY
        run(f"git config user.email '{HorusConfig.GIT_USER_EMAIL}'", cwd=root)
        run(f"git config user.name '{HorusConfig.GIT_USER_NAME}'", cwd=root)

        # 4. COMMIT & PUSH
        run("git add .", cwd=root)
        run(f"git commit -m 'Horus Sovereign Sync {datetime.datetime.now()}'", cwd=root)
        
        # 5. REMOTE & FORCE PUSH
        run(f"git remote add origin {repo_url}", cwd=root)
        
        logs.append("📡 Attempting Push to GitHub...")
        if run("git push -u origin main --force", cwd=root):
            logs.append("✨ SUCCESS: Repository Updated.")
        else:
            logs.append("❌ PUSH FAILED. Verify PAT permissions/Repo existence.")
            
        return "\n".join(logs)

# ==============================================================================
# 🧠 AI & CHAT (ROBUST KEY ROTATION + CACHING)
# ==============================================================================

# GLOBAL CACHE TO FIX THE "WEB UI" PERMISSION BUG
_KEY_CACHE = []

def get_rotated_key():
    """
    Fetches a random key from the rotational pool.
    Uses caching to prevent 'Configuration Error' in Web UI modes.
    """
    global _KEY_CACHE
    
    # 1. Return cached keys if available (Bypass Colab Permission Prompt)
    if _KEY_CACHE:
        return random.choice(_KEY_CACHE)
    
    # 2. If not cached, try fetching from Secrets (Triggers Prompt in Colab)
    try:
        from google.colab import userdata
        keys_str = userdata.get('GEMINI_KEYS')
        if not keys_str:
            # Fallback: Try OS Environ
            keys_str = os.environ.get('GEMINI_KEYS')
        
        if keys_str:
            # Robust parsing
            _KEY_CACHE = [k.strip() for k in keys_str.split(',') if k.strip()]
            if _KEY_CACHE:
                logger.info(f"🔑 Gemini Keys Cached: {len(_KEY_CACHE)} keys loaded.")
                return random.choice(_KEY_CACHE)
    except Exception as e:
        logger.error(f"Secret Fetch Error: {e}")
        
    return None

def ask_ai(msg, history):
    key = get_rotated_key()
    if not key: return "⚠️ Configuration Error: Please grant access to 'GEMINI_KEYS' in the Colab tab, then try again."
    try:
        client = genai.Client(api_key=key)
        # FORCE SPECIFIC MODEL AS REQUESTED
        res = client.models.generate_content(
            model=HorusConfig.AI_MODEL, 
            contents=msg
        )
        return res.text
    except Exception as e: return f"AI Error: {str(e)}"

# ==============================================================================
# 📱 UI (PLATINUM DASHBOARD)
# ==============================================================================

current_user = None

def ui_login(image, passport, nationality):
    global current_user
    # FIX: Handle None image for testing or weak connection
    if image is None: 
        # For Demo Purposes allow entry if fields are filled, else return error
        if not passport: return "❌ Scan or Data Required", gr.update(), "", ""
        bio_hash = "BIO-MANUAL-ENTRY"
    else:
        bio_hash = HorusSecurity.scan_face(image)

    name = f"Traveler-{nationality[:3].upper()}-{passport[-4:]}"
    uid = db.register_traveler(name, passport, nationality, bio_hash)
    current_user = db.get_traveler(uid)
    
    return (
        f"✅ Verified: {name}",
        gr.Group(visible=True), 
        f"EGP {current_user[5]}",
        f"🌿 {current_user[6]}"
    )

def ui_demo_login():
    """Bypasses security for presentation purposes."""
    global current_user
    name = "Diplomat-DEMO-001"
    uid = db.register_traveler(name, "D999999", "Egypt", "BIO-DEMO-KEY")
    # Grant Demo Credits
    db.top_up(uid, 50000) 
    current_user = db.get_traveler(uid)
    return (
        f"✅ DEMO MODE ACTIVATED: {name}",
        gr.Group(visible=True),
        f"EGP {current_user[5]}",
        f"🌿 {current_user[6]}"
    )

def ui_book_transport(mode, dest):
    if not current_user: return "Login First"
    pts, lbl = EcoEngine.calculate_impact(mode)
    cost = 20
    if db.purchase(current_user[0], f"Ride: {mode}", cost, "TRANSPORT"):
        db.add_green_points(current_user[0], pts)
        return f"✅ Booked {mode}. +{pts} Points."
    return "❌ No Funds"

def ui_book_monument(monument_name):
    if not current_user: return "Login First"
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found"
    
    price = target[3]
    if db.purchase(current_user[0], f"Ticket: {monument_name}", price, "MONUMENTS"):
         return f"✅ Ticket Issued: {monument_name} ({price} EGP)"
    return "❌ Insufficient Funds"

def ui_issue_visa():
    if not current_user: return "Login First", None, None
    
    nationality = current_user[3]
    
    # BLOCK RESTRICTED NATIONALITIES
    if nationality in HorusConfig.RESTRICTED_COUNTRIES:
        return "❌ Visa on Arrival NOT available. Please apply at nearest Consulate.", None, None
    
    # CHECK VISA ELIGIBILITY
    if nationality not in HorusConfig.VOA_ELIGIBLE_COUNTRIES:
        return "❌ Visa on Arrival NOT available. Please apply at nearest Consulate.", None, None
    
    # PROCESS VISA PAYMENT
    visa_fee = HorusConfig.PRICING["visa_fee"]
    stamp, ts = HorusSecurity.generate_digital_stamp(current_user[2], current_user[3])
    
    if db.purchase(current_user[0], "Visa", visa_fee, "GOVT"):
        db.add_visa(current_user[0], stamp)
        data = json.dumps({"visa": stamp, "nationality": nationality})
        pdf = DocumentIssuer.generate_visa_pdf({"name": current_user[1], "passport": current_user[2], "nationality": current_user[3]}, stamp, data)
        qr = qrcode.make(data)
        qr.save("qr.png")
        return f"✅ Issued: {stamp} ({visa_fee} EGP)", "qr.png", pdf
    return "❌ Insufficient Funds", None, None

def ui_buy_esim(plan_name):
    if not current_user: return "Login First"
    # Parse mock data
    price = 500 if "Orange" in plan_name else 400
    if db.purchase(current_user[0], plan_name, price, "CONNECTIVITY"):
        return f"✅ Activated: {plan_name}. QR sent to email."
    return "❌ Insufficient Funds"

def ui_buy_souvenir(item_name):
    if not current_user: return "Login First"
    price = 250
    if db.purchase(current_user[0], item_name, price, "SOUVENIR"):
        return f"✅ Purchased: {item_name}. Pickup at Airport Zone B."
    return "❌ Insufficient Funds"

def ui_claim_offer(offer_name):
    if not current_user: return "Login First"
    return f"✅ VOUCHER CLAIMED: {offer_name}. Saved to Wallet."

# CLEAN CSS
css = """
body { background-color: #F5F5DC; }
.gradio-container { font-family: sans-serif; }
button.primary { background-color: #D4AF37 !important; color: white !important; font-weight: bold; }
button.secondary { background-color: #2F4F4F !important; color: white !important; }
"""

with gr.Blocks(css=css, title="Horus Key Platinum") as demo:
    gr.Markdown(f"# 👁️ {HorusConfig.APP_NAME}")
    
    # STATUS BAR
    with gr.Row():
        status = gr.Textbox(label="Identity Status", value="Awaiting Biometrics")
        bal = gr.Textbox(label="Wallet Balance", value="---")
        score = gr.Textbox(label="Green Score", value="---")
        
    # ENTRY GATE
    with gr.Row():
        cam = gr.Image(sources=["webcam"], label="Biometric Scanner", type="numpy")
        with gr.Column():
            passport = gr.Textbox(label="Passport Number", value="A1234567")
            nat = gr.Dropdown(["USA", "Egypt", "UK", "Germany", "Japan"], label="Nationality", value="USA")
            with gr.Row():
                btn = gr.Button("SCAN FACE & ENTER ECOSYSTEM", variant="primary")
                btn_demo = gr.Button("🔑 DEMO ACCESS (Bypass Bio)", variant="secondary")

    # MAIN APP GROUP (Hidden initially)
    with gr.Group(visible=False) as app:
        with gr.Tabs():
            # 1. VISA (4.A, 4.B, 4.I)
            with gr.TabItem("🛂 Visa & Identity"):
                gr.Markdown("### 4.B Visa upon Arrival & 4.I Digital Access")
                btn_visa = gr.Button(f"Pay {HorusConfig.PRICING['visa_fee']} EGP & Issue Visa")
                with gr.Row():
                    out_v = gr.Textbox(label="Status")
                    img_v = gr.Image(label="Digital QR Stamp")
                    file_v = gr.File(label="Download E-Visa PDF")
                btn_visa.click(ui_issue_visa, outputs=[out_v, img_v, file_v])
                
            # 2. TRANSPORT (4.D, 4.E)
            with gr.TabItem("🚕 Mobility"):
                gr.Markdown("### 4.D Booking & 4.E Eco-Travel")
                mode = gr.Dropdown([
                    "Cairo Monorail", "LRT (Electric Train)", "Electric Bus",
                    "Metro Line 1", "Metro Line 2", "Metro Line 3",
                    "Gas-Powered Taxi", "Private Car", "Standard Uber",
                    "Shared Shuttle", "Train"
                ], label="Mode")
                dest = gr.Textbox(label="Destination", placeholder="e.g. Pyramids")
                btn_tr = gr.Button("Book Ride")
                out_tr = gr.Textbox(label="Receipt")
                btn_tr.click(ui_book_transport, inputs=[mode, dest], outputs=[out_tr])
            
            # 3. MONUMENTS (4.F)
            with gr.TabItem("🏛️ Monuments"):
                gr.Markdown("### 4.F Heritage Tickets")
                with gr.Row():
                    btn_m1 = gr.Button("Great Pyramid (540 EGP)")
                    btn_m2 = gr.Button("Karnak Temple (450 EGP)")
                    btn_m3 = gr.Button("GEM Museum (1200 EGP)")
                out_mon = gr.Textbox(label="Ticket Status")
                btn_m1.click(lambda: ui_book_monument("Great Pyramid"), outputs=[out_mon])
                btn_m2.click(lambda: ui_book_monument("Karnak Temple"), outputs=[out_mon])
                btn_m3.click(lambda: ui_book_monument("GEM Museum"), outputs=[out_mon])

            # 4. MARKETPLACE (4.H, 4.J)
            with gr.TabItem("🛍️ Marketplace"):
                gr.Markdown("### 4.H Connectivity & 4.J Souvenirs")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**eSIMs**")
                        plans = [f"{p[0]} ({p[2]} EGP)" for p in MarketplaceEngine.get_esims()]
                        dd_sim = gr.Dropdown(plans, label="Data Plan")
                        btn_sim = gr.Button("Activate eSIM")
                        out_sim = gr.Textbox()
                        btn_sim.click(ui_buy_esim, inputs=[dd_sim], outputs=[out_sim])
                    with gr.Column():
                        gr.Markdown("**Souvenirs**")
                        items = [f"{i[0]} ({i[2]} EGP)" for i in MarketplaceEngine.get_souvenirs()]
                        dd_shop = gr.Dropdown(items, label="Authentic Items")
                        btn_shop = gr.Button("Purchase")
                        out_shop = gr.Textbox()
                        btn_shop.click(ui_buy_souvenir, inputs=[dd_shop], outputs=[out_shop])

            # 5. OFFERS (4.G)
            with gr.TabItem("🎁 Offers"):
                gr.Markdown("### 4.G Exclusive Deals")
                offers = [f"{o[0]} - {o[1]}" for o in MarketplaceEngine.get_exclusive_offers()]
                dd_offer = gr.Dropdown(offers, label="Select Offer")
                btn_offer = gr.Button("Claim Voucher")
                out_offer = gr.Textbox()
                btn_offer.click(ui_claim_offer, inputs=[dd_offer], outputs=[out_offer])
                
            # 6. AI
            with gr.TabItem("🤖 Horus AI"):
                gr.Markdown(f"Powered by **{HorusConfig.AI_MODEL}**")
                gr.ChatInterface(fn=ask_ai, type="messages")
                
            # 7. ADMIN
            with gr.TabItem("⚙️ Admin"):
                gr.Markdown("### System Sync (Force Push)")
                btn_s = gr.Button("Sync Code & Docs to GitHub", variant="stop")
                out_s = gr.TextArea(label="Diagnostic Logs")
                btn_s.click(GitAutopilot.sync_codebase, outputs=[out_s])

    # Event Wiring
    btn.click(ui_login, inputs=[cam, passport, nat], outputs=[status, app, bal, score])
    btn_demo.click(ui_demo_login, outputs=[status, app, bal, score])

if __name__ == "__main__":
    demo.queue().launch(share=True)