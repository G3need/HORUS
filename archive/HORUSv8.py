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
from typing import List, Tuple, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from google import genai 
from dataclasses import dataclass
from enum import Enum

# ==============================================================================
# 🏛️ HORUS KEY: STRATEGIC CONFIGURATION
# ==============================================================================

class HorusConfig:
    APP_NAME = "HORUS KEY | Egypt Smart Travel Ecosystem"
    VERSION = "8.0.0-SOTA (Military-Grade)"
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
    
    # 💰 PRICING MATRIX (EGP)
    PRICING = {
        "foreigner_adult_base": 1000,
        "foreigner_student_discount": 0.5,  # 50% of base
        "arab_egyptian_fixed": 100,
        "visa_fee": 1250  # $25 USD * 50 EGP conversion rate
    }

# ==============================================================================
# 📝 DOCUMENTATION ENGINE (AUTO-README)
# ==============================================================================

class ReadmeGenerator:
    """Automatically generates the project documentation file."""
    
    @staticmethod
    def generate():
        content = f"""# Horus Key – Egypt's Smart Digital Travel Ecosystem 👁️

**Revolutionizing Border Management & Tourism Services**

> **Submitted by:** Mohamed Sayed Hassan Sayed Ahmed
> **Version:** {HorusConfig.VERSION}

---

## 📋 Executive Summary
**Horus Key** is a comprehensive digital platform that modernizes border entry, enhances the traveler experience, and boosts Egypt's tourism economy. It integrates arrival cards, visas, payments, transportation, and tourism services into one unified system.

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
*"HORUS KEY - Opening the Gateway to Smart Tourism."*
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
# 🧠 LEVEL 2: LOGIC ENGINES (SOTA ARCHITECTURE)
# ==============================================================================

class NationalityGroup(Enum):
    FOREIGN = "FOREIGN"
    ARAB = "ARAB"
    EGYPTIAN = "EGYPTIAN"

class VisitorType(Enum):
    ADULT = "ADULT"
    STUDENT = "STUDENT"
    KID = "KID"

class VisaPolicy:
    """
    LOGIC ENGINE 1: VISA POLICY ENFORCEMENT
    Implements strict 2026 Visa on Arrival rules with hardcoded eligibility.
    """
    
    # 🛂 VISA ON ARRIVAL ELIGIBLE COUNTRIES (74+ COUNTRIES)
    VOA_ELIGIBLE_COUNTRIES = {
        # North America
        "USA", "CANADA",
        # Europe (EU + UK + Schengen)
        "UK", "GERMANY", "FRANCE", "ITALY", "SPAIN", "NETHERLANDS", "BELGIUM", 
        "AUSTRIA", "SWEDEN", "DENMARK", "NORWAY", "FINLAND", "POLAND", 
        "CZECH REPUBLIC", "HUNGARY", "PORTUGAL", "GREECE", "IRELAND", 
        "SWITZERLAND", "LUXEMBOURG", "SLOVAKIA", "SLOVENIA", "ESTONIA", 
        "LATVIA", "LITHUANIA", "MALTA", "CYPRUS", "BULGARIA", "ROMANIA", 
        "CROATIA", "ICELAND", "LIECHTENSTEIN",
        # Asia Pacific
        "JAPAN", "AUSTRALIA", "NEW ZEALAND", "SOUTH KOREA", "SINGAPORE", 
        "MALAYSIA", "HONG KONG", "TAIWAN",
        # Middle East (Selected)
        "UAE", "SAUDI ARABIA", "QATAR", "KUWAIT", "BAHRAIN", "OMAN",
        # Others
        "RUSSIA", "TURKEY", "ISRAEL"
    }
    
    # 🚫 RESTRICTED NATIONALITIES (BLOCKED FROM VISA & PAYMENT)
    RESTRICTED_COUNTRIES = {
        "IRAN", "AFGHANISTAN", "SYRIA", "YEMEN", "LIBYA", "SOMALIA", 
        "NORTH KOREA", "SUDAN", "LEBANON", "IRAQ", "PALESTINE"
    }
    
    @classmethod
    def check_eligibility(cls, nationality: str) -> bool:
        """
        Check if nationality is eligible for Visa on Arrival.
        
        Args:
            nationality: Country name (string)
            
        Returns:
            bool: True if eligible, False if restricted or not in eligible list
        """
        if nationality.upper() in cls.RESTRICTED_COUNTRIES:
            return False
        return nationality.upper() in cls.VOA_ELIGIBLE_COUNTRIES
    
    @classmethod
    def get_nationality_group(cls, nationality: str) -> NationalityGroup:
        """
        Determine nationality group for pricing purposes.
        
        Args:
            nationality: Country name (string)
            
        Returns:
            NationalityGroup: FOREIGN, ARAB, or EGYPTIAN
        """
        arab_countries = {
            "UAE", "SAUDI ARABIA", "QATAR", "KUWAIT", "BAHRAIN", "OMAN",
            "JORDAN", "LEBANON", "IRAQ", "SYRIA", "YEMEN", "LIBYA", 
            "TUNISIA", "ALGERIA", "MOROCCO", "SUDAN", "PALESTINE"
        }
        
        if nationality.upper() == "EGYPT":
            return NationalityGroup.EGYPTIAN
        elif nationality.upper() in arab_countries:
            return NationalityGroup.ARAB
        else:
            return NationalityGroup.FOREIGN

class PriceCalculator:
    """
    LOGIC ENGINE 2: DYNAMIC PRICING & TICKETING
    Implements 2026 pricing matrix with nationality-based calculations.
    """
    
    @staticmethod
    def calculate_ticket_price(
        base_price: float, 
        nationality_group: NationalityGroup, 
        visitor_type: VisitorType,
        quantity: int = 1
    ) -> float:
        """
        Calculate ticket price based on nationality group and visitor type.
        
        Args:
            base_price: Base price for foreigner adult
            nationality_group: FOREIGN, ARAB, or EGYPTIAN
            visitor_type: ADULT, STUDENT, or KID
            quantity: Number of tickets
            
        Returns:
            float: Total price in EGP
        """
        if nationality_group == NationalityGroup.EGYPTIAN:
            unit_price = HorusConfig.PRICING["arab_egyptian_fixed"]
        elif nationality_group == NationalityGroup.ARAB:
            unit_price = HorusConfig.PRICING["arab_egyptian_fixed"]
        else:  # FOREIGN
            if visitor_type == VisitorType.STUDENT:
                unit_price = base_price * HorusConfig.PRICING["foreigner_student_discount"]
            elif visitor_type == VisitorType.KID:
                unit_price = base_price * 0.3  # 30% of base for kids
            else:  # ADULT
                unit_price = base_price
        
        return unit_price * quantity
    
    @staticmethod
    def get_visa_fee() -> float:
        """Get Visa on Arrival fee in EGP."""
        return HorusConfig.PRICING["visa_fee"]

class EcoEngine:
    """
    LOGIC ENGINE 3: ECO-GAMIFICATION (2026 TRANSPORT MODES)
    Updated with real Egyptian transport options and point system.
    """
    
    @staticmethod
    def calculate_impact(mode: str) -> tuple:
        """
        Calculate green points and impact level for transport mode.
        
        Args:
            mode: Transport mode name
            
        Returns:
            tuple: (points, impact_label)
        """
        # High Reward (+20 pts): Cairo Monorail, LRT (Electric Train), Electric Bus
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
            f"FULL NAME: {traveler_info['full_name']}",
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
# 💾 LEVEL 4: THE MONOLITH (DATABASE) - SOTA SCHEMA
# ==============================================================================

class HorusDB:
    def __init__(self):
        self.conn = sqlite3.connect(HorusConfig.DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_schema()
        self._seed_monolith()

    def _init_schema(self):
        # Drop existing tables for clean migration
        self.cursor.execute("DROP TABLE IF EXISTS travelers")
        self.cursor.execute("DROP TABLE IF EXISTS tickets")
        self.cursor.execute("DROP TABLE IF EXISTS visas")
        self.cursor.execute("DROP TABLE IF EXISTS monuments")
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute("DROP TABLE IF EXISTS marketplace_orders")
        
        # Updated schema with new columns
        tables = [
            # Updated travelers table with new columns
            '''CREATE TABLE travelers (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                full_name TEXT,
                passport_number TEXT UNIQUE, 
                nationality TEXT,
                nationality_group TEXT,
                passport_expiry TEXT,
                biometric_hash TEXT, 
                wallet_balance REAL DEFAULT 0, 
                wallet_status TEXT DEFAULT 'LOCKED',
                bank_linked BOOLEAN DEFAULT 0,
                green_points INTEGER DEFAULT 0, 
                has_claimed_gift BOOLEAN DEFAULT 0,
                created_at TEXT
            )''',
            
            # New tickets table for proper ticketing system
            '''CREATE TABLE tickets (
                id INTEGER PRIMARY KEY,
                traveler_id INT,
                attraction_name TEXT,
                visitor_type TEXT,
                quantity INT,
                total_price REAL,
                qr_hash TEXT,
                status TEXT DEFAULT 'ACTIVE',
                created_at TEXT,
                FOREIGN KEY (traveler_id) REFERENCES travelers (id)
            )''',
            
            # Updated monuments table with base pricing
            '''CREATE TABLE monuments (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                location TEXT, 
                base_price_foreigner REAL,
                description TEXT, 
                image_emoji TEXT
            )''',
            
            # Existing tables remain
            '''CREATE TABLE visas (
                id INTEGER PRIMARY KEY, 
                traveler_id INT, 
                visa_type TEXT, 
                digital_stamp TEXT, 
                status TEXT, 
                issued_at TEXT
            )''',
            
            '''CREATE TABLE transactions (
                id INTEGER PRIMARY KEY, 
                traveler_id INT, 
                service_type TEXT, 
                amount REAL, 
                details TEXT, 
                timestamp TEXT
            )''',
            
            '''CREATE TABLE marketplace_orders (
                id INTEGER PRIMARY KEY, 
                traveler_id INT, 
                item_name TEXT, 
                category TEXT, 
                price REAL, 
                status TEXT
            )'''
        ]
        
        for t in tables:
            self.cursor.execute(t)
        self.conn.commit()

    def _seed_monolith(self):
        # Seed monuments with base pricing for foreigners
        if self.cursor.execute("SELECT count(*) FROM monuments").fetchone()[0] == 0:
            monuments = [
                ("Great Pyramid", "Giza", 1000, "Ancient Wonder", "🔺"), 
                ("Karnak Temple", "Luxor", 800, "Temple Complex", "⛩️"), 
                ("GEM Museum", "Giza", 1200, "Grand Museum", "🏛️"),
                ("Valley of Kings", "Luxor", 900, "Royal Tombs", "⚰️"),
                ("Abu Simbel", "Aswan", 1100, "Ramesses II", "🗿")
            ]
            self.cursor.executemany(
                "INSERT INTO monuments (name, location, base_price_foreigner, description, image_emoji) VALUES (?, ?, ?, ?, ?)", 
                monuments
            )
        self.conn.commit()

    # --- CRUD Operations ---
    def register_traveler(self, name, full_name, passport, nationality, nationality_group, passport_expiry, bio_hash):
        try:
            self.cursor.execute(
                """INSERT INTO travelers 
                   (name, full_name, passport_number, nationality, nationality_group, passport_expiry, biometric_hash, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                (name, full_name, passport, nationality, nationality_group.value, passport_expiry, bio_hash, datetime.datetime.now().isoformat())
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Traveler already exists, return existing ID
            self.cursor.execute("SELECT id FROM travelers WHERE passport_number=?", (passport,))
            return self.cursor.fetchone()[0]

    def get_traveler(self, tid):
        return self.cursor.execute("SELECT * FROM travelers WHERE id=?", (tid,)).fetchone()

    def purchase(self, tid, item, cost, cat):
        bal = self.get_traveler(tid)[8]  # wallet_balance is at index 8
        wallet_status = self.get_traveler(tid)[9]  # wallet_status is at index 9
        if wallet_status != 'ACTIVE':
            return False  # Block purchases for locked accounts
        if bal >= cost:
            self.cursor.execute("UPDATE travelers SET wallet_balance = wallet_balance - ? WHERE id=?", (cost, tid))
            self.cursor.execute(
                "INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", 
                (tid, cat, -cost, item, datetime.datetime.now().isoformat())
            )
            self.conn.commit()
            return True
        return False

    def add_green_points(self, tid, points):
        self.cursor.execute("UPDATE travelers SET green_points = green_points + ? WHERE id=?", (points, tid))
        self.conn.commit()

    def add_visa(self, tid, stamp):
        self.cursor.execute(
            "INSERT INTO visas (traveler_id, visa_type, digital_stamp, status, issued_at) VALUES (?, ?, ?, ?, ?)", 
            (tid, "TOURIST", stamp, "ACTIVE", datetime.datetime.now().isoformat())
        )
        self.conn.commit()

    def create_ticket(self, traveler_id, attraction_name, visitor_type, quantity, total_price):
        qr_hash = hashlib.sha256(f"{traveler_id}{attraction_name}{datetime.datetime.now()}".encode()).hexdigest()[:16]
        self.cursor.execute(
            """INSERT INTO tickets 
               (traveler_id, attraction_name, visitor_type, quantity, total_price, qr_hash, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (traveler_id, attraction_name, visitor_type.value, quantity, total_price, qr_hash, datetime.datetime.now().isoformat())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_data(self, table):
        return self.cursor.execute(f"SELECT * FROM {table}").fetchall()
        
    def top_up(self, tid, amt):
        self.cursor.execute("UPDATE travelers SET wallet_balance = wallet_balance + ? WHERE id=?", (amt, tid))
        self.cursor.execute(
            "INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", 
            (tid, "TOPUP", amt, "Load", datetime.datetime.now().isoformat())
        )
        self.conn.commit()

    def activate_wallet(self, tid, card_number):
        """Activate wallet with $200 USD deposit (10000 EGP)"""
        activation_amount = 10000  # $200 USD * 50 EGP conversion
        self.cursor.execute(
            "UPDATE travelers SET wallet_balance = wallet_balance + ?, wallet_status = 'ACTIVE' WHERE id=?", 
            (activation_amount, tid)
        )
        self.cursor.execute(
            "INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", 
            (tid, "ACTIVATION", activation_amount, f"Initial Deposit - Card: {card_number[-4:]}", datetime.datetime.now().isoformat())
        )
        self.conn.commit()
        return True

    def link_bank(self, tid, bank_name):
        """Link bank account to traveler"""
        self.cursor.execute("UPDATE travelers SET bank_linked = 1 WHERE id=?", (tid,))
        self.cursor.execute(
            "INSERT INTO transactions (traveler_id, service_type, amount, details, timestamp) VALUES (?, ?, ?, ?, ?)", 
            (tid, "BANK_LINK", 0, f"Bank Linked: {bank_name}", datetime.datetime.now().isoformat())
        )
        self.conn.commit()
        return True

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
        files_to_sync = ["HORUSv8.py", "horus_core.db", "README.md"]
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
# 📱 UI (PLATINUM DASHBOARD) - INTEGRATED WITH LOGIC ENGINES
# ==============================================================================

current_user = None

def ui_login(image, passport, nationality, full_name, passport_expiry):
    global current_user
    # FIX: Handle None image for testing or weak connection
    if image is None: 
        # For Demo Purposes allow entry if fields are filled, else return error
        if not passport: return "❌ Scan or Data Required", gr.update(), gr.update(), "", "", ""
        bio_hash = "BIO-MANUAL-ENTRY"
    else:
        bio_hash = HorusSecurity.scan_face(image)

    # Determine nationality group using Logic Engine
    nationality_group = VisaPolicy.get_nationality_group(nationality)
    
    # Generate display name
    name = f"Traveler-{nationality[:3].upper()}-{passport[-4:]}"
    
    uid = db.register_traveler(name, full_name, passport, nationality, nationality_group, passport_expiry, bio_hash)
    current_user = db.get_traveler(uid)
    
    # Check wallet status for activation gate
    wallet_status = current_user[9]  # wallet_status is at index 9
    wallet_balance = current_user[8]  # wallet_balance is at index 8
    green_points = current_user[11]  # green_points is at index 11
    
    if wallet_status == 'LOCKED':
        # Show activation panel, hide main app
        return (
            f"✅ Verified: {name} - WALLET LOCKED",
            gr.Group(visible=False),  # Hide main app
            gr.Group(visible=True),   # Show activation panel
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "🔒 ACCOUNT LOCKED - Deposit $200 USD to activate"
        )
    else:
        # Show main app, hide activation panel
        return (
            f"✅ Verified: {name} - ACCOUNT ACTIVE",
            gr.Group(visible=True),   # Show main app
            gr.Group(visible=False),  # Hide activation panel
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "✅ ACCOUNT ACTIVE - All features available"
        )

def ui_activate_wallet(card_number):
    """Activate wallet with $200 USD deposit"""
    if not current_user: return "❌ Login required", gr.update(), gr.update()
    
    # Basic card validation (mock)
    if not card_number or len(card_number) < 16:
        return "❌ Invalid card number", gr.update(), gr.update()
    
    # Process activation
    if db.activate_wallet(current_user[0], card_number):
        # Refresh user data
        global current_user
        current_user = db.get_traveler(current_user[0])
        
        return (
            f"✅ Wallet Activated! 10,000 EGP deposited. Welcome to HORUS!",
            gr.Group(visible=True),   # Show main app
            gr.Group(visible=False)   # Hide activation panel
        )
    else:
        return "❌ Activation failed", gr.update(), gr.update()

def ui_link_bank(bank_name):
    """Link bank account to wallet"""
    if not current_user: return "❌ Login required"
    
    if db.link_bank(current_user[0], bank_name):
        return f"✅ Bank linked: {bank_name}"
    else:
        return "❌ Bank linking failed"

def process_qr_payment(qr_string):
    """
    Process QR payment in format: PAY:VENDOR_ID:AMOUNT:CURRENCY
    Example: PAY:CAIRO_METRO:50:EGP or PAY:STARBUCKS_ZAMALEK:150:EGP
    """
    if not current_user:
        return "❌ Login required to make payments"
    
    # Check if wallet is active
    wallet_status = current_user[9]  # wallet_status is at index 9
    if wallet_status != 'ACTIVE':
        return "❌ Wallet locked. Please activate your account to make payments."
    
    if not qr_string:
        return "❌ No QR data provided"
    
    try:
        # Parse QR string
        parts = qr_string.strip().split(':')
        
        # Validate format
        if len(parts) != 4 or parts[0] != 'PAY':
            return "❌ Invalid QR Format. Expected: PAY:VENDOR_ID:AMOUNT:CURRENCY"
        
        vendor_id = parts[1]
        amount_str = parts[2]
        currency = parts[3]
        
        # Validate amount
        try:
            amount = float(amount_str)
        except ValueError:
            return "❌ Invalid amount in QR code"
        
        # Validate currency (currently only EGP supported)
        if currency.upper() != 'EGP':
            return f"❌ Currency {currency} not supported. Only EGP accepted."
        
        # Check wallet balance
        current_balance = current_user[8]  # wallet_balance is at index 8
        
        if amount > current_balance:
            return f"❌ Insufficient Funds. Balance: {current_balance} EGP, Required: {amount} EGP"
        
        # Process payment
        if db.purchase(current_user[0], f"QR Payment to {vendor_id}", amount, "QR_PAYMENT"):
            # Refresh user data to get updated balance
            global current_user
            current_user = db.get_traveler(current_user[0])
            new_balance = current_user[8]
            
            return f"✅ PAID {amount} EGP to {vendor_id}. Balance: {new_balance} EGP."
        else:
            return "❌ Payment processing failed"
            
    except Exception as e:
        logger.error(f"QR Payment Error: {e}")
        return "❌ Error processing QR payment"

def ui_scan_qr(qr_input):
    """UI function for scanning QR codes"""
    return process_qr_payment(qr_input)

def ui_demo_login():
    """Bypasses security for presentation purposes."""
    global current_user
    name = "Diplomat-DEMO-001"
    full_name = "Demo User"
    uid = db.register_traveler(name, full_name, "D999999", "Egypt", NationalityGroup.EGYPTIAN, "2030-01-01", "BIO-DEMO-KEY")
    # Grant Demo Credits
    db.top_up(uid, 50000) 
    current_user = db.get_traveler(uid)
    return (
        f"✅ DEMO MODE ACTIVATED: {name}",
        gr.Group(visible=True),
        f"EGP {current_user[8]}",
        f"🌿 {current_user[9]}"
    )

def ui_book_transport(mode, dest):
    if not current_user: return "Login First"
    pts, lbl = EcoEngine.calculate_impact(mode)
    cost = 20
    if db.purchase(current_user[0], f"Ride: {mode}", cost, "TRANSPORT"):
        db.add_green_points(current_user[0], pts)
        return f"✅ Booked {mode}. +{pts} Points."
    return "❌ No Funds"

def ui_book_monument(monument_name, visitor_type, quantity):
    if not current_user: return "Login First"
    
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found"
    
    # Get nationality group from current user
    nationality_group_str = current_user[5]  # nationality_group column
    nationality_group = NationalityGroup(nationality_group_str)
    
    # Parse visitor type
    visitor_type_enum = VisitorType(visitor_type)
    
    # Calculate price using Logic Engine
    base_price = target[3]  # base_price_foreigner
    total_price = PriceCalculator.calculate_ticket_price(
        base_price, nationality_group, visitor_type_enum, quantity
    )
    
    if db.purchase(current_user[0], f"Ticket: {monument_name}", total_price, "MONUMENTS"):
        # Create ticket record
        db.create_ticket(current_user[0], monument_name, visitor_type_enum, quantity, total_price)
        return f"✅ Ticket Issued: {monument_name} ({quantity}x {visitor_type}) - {total_price} EGP"
    return "❌ Insufficient Funds"

def ui_issue_visa():
    if not current_user: return "Login First", None, None
    
    nationality = current_user[4]  # nationality column
    
    # ENFORCE VISA POLICY USING LOGIC ENGINE
    if not VisaPolicy.check_eligibility(nationality):
        return "❌ VISA ON ARRIVAL NOT AVAILABLE. Please visit nearest Consulate.", None, None
    
    # PROCESS VISA PAYMENT
    visa_fee = PriceCalculator.get_visa_fee()
    stamp, ts = HorusSecurity.generate_digital_stamp(current_user[3], current_user[4])
    
    if db.purchase(current_user[0], "Visa", visa_fee, "GOVT"):
        db.add_visa(current_user[0], stamp)
        data = json.dumps({"visa": stamp, "nationality": nationality})
        traveler_info = {
            "full_name": current_user[2],
            "passport": current_user[3], 
            "nationality": current_user[4]
        }
        pdf = DocumentIssuer.generate_visa_pdf(traveler_info, stamp, data)
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

with gr.Blocks(css=css, title="Horus Key Platinum v8") as demo:
    gr.Markdown(f"# 👁️ {HorusConfig.APP_NAME}")
    
    # STATUS BAR
    with gr.Row():
        status = gr.Textbox(label="Identity Status", value="Awaiting Biometrics")
        bal = gr.Textbox(label="Wallet Balance", value="---")
        score = gr.Textbox(label="Green Score", value="---")
        activation_status = gr.Textbox(label="Account Status", value="---")
        
    # ENTRY GATE
    with gr.Row():
        cam = gr.Image(sources=["webcam"], label="Biometric Scanner", type="numpy")
        with gr.Column():
            passport = gr.Textbox(label="Passport Number", value="A1234567")
            full_name = gr.Textbox(label="Full Name (as in Passport)", value="John Doe")
            passport_expiry = gr.Textbox(label="Passport Expiry (YYYY-MM-DD)", value="2028-12-31")
            nat = gr.Dropdown(["USA", "Egypt", "UK", "Germany", "Japan"], label="Nationality", value="USA")
            with gr.Row():
                btn = gr.Button("SCAN FACE & ENTER ECOSYSTEM", variant="primary")
                btn_demo = gr.Button("🔑 DEMO ACCESS (Bypass Bio)", variant="secondary")

    # ACTIVATION PANEL (Hidden initially)
    with gr.Group(visible=False) as activation_panel:
        gr.Markdown("# 🔒 ACCOUNT ACTIVATION REQUIRED")
        gr.Markdown("### Deposit $200 USD to unlock all HORUS features")
        with gr.Row():
            card_input = gr.Textbox(label="Credit Card Number", placeholder="1234-5678-9012-3456", type="password")
            btn_activate = gr.Button("DEPOSIT $200 & ACTIVATE", variant="primary")
        activation_msg = gr.Textbox(label="Activation Status", interactive=False)
        btn_activate.click(ui_activate_wallet, inputs=[card_input], outputs=[activation_msg, gr.Group(visible=True), activation_panel])

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
                    monument_name = gr.Dropdown([
                        "Great Pyramid", "Karnak Temple", "GEM Museum", 
                        "Valley of Kings", "Abu Simbel"
                    ], label="Select Monument")
                    visitor_type = gr.Dropdown(["ADULT", "STUDENT", "KID"], label="Visitor Type")
                    quantity = gr.Number(minimum=1, value=1, label="Quantity")
                    btn_mon = gr.Button("Purchase Ticket")
                out_mon = gr.Textbox(label="Ticket Status")
                btn_mon.click(ui_book_monument, inputs=[monument_name, visitor_type, quantity], outputs=[out_mon])

            # 4. WALLET & BANKING (NEW TAB)
            with gr.TabItem("💳 Wallet & Banking"):
                gr.Markdown("### Wallet Management & Banking Services")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Bank Linking**")
                        bank_dropdown = gr.Dropdown(["X-Bank", "InstaPay", "Bank of Egypt", "CIB"], label="Select Bank")
                        btn_bank = gr.Button("Link Bank Account")
                        out_bank = gr.Textbox(label="Bank Status")
                        btn_bank.click(ui_link_bank, inputs=[bank_dropdown], outputs=[out_bank])
                    with gr.Column():
                        gr.Markdown("**Wallet Info**")
                        wallet_info = gr.Textbox(label="Account Details", interactive=False)
                        refresh_btn = gr.Button("Refresh Balance")
                        refresh_btn.click(lambda: f"Status: {current_user[9] if current_user else 'N/A'}", outputs=[wallet_info])

            # 5. SCAN & PAY (NEW TAB)
            with gr.TabItem("📷 Scan & Pay"):
                gr.Markdown("### The Reverse QR - Scan to Pay")
                gr.Markdown("**Scan QR codes from Metro gates, merchants, or payment terminals**")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**QR Scanner Input**")
                        qr_input = gr.Textbox(
                            label="QR Code Data", 
                            placeholder="PAY:VENDOR_ID:AMOUNT:CURRENCY\nExample: PAY:CAIRO_METRO:50:EGP",
                            lines=3
                        )
                        btn_scan = gr.Button("📷 PROCESS PAYMENT", variant="primary")
                        scan_result = gr.Textbox(label="Payment Result", interactive=False)
                        btn_scan.click(ui_scan_qr, inputs=[qr_input], outputs=[scan_result])
                    
                    with gr.Column():
                        gr.Markdown("**Quick Examples**")
                        gr.Markdown("""
                        **Common QR Formats:**
                        - `PAY:CAIRO_METRO:50:EGP`
                        - `PAY:STARBUCKS_ZAMALEK:150:EGP`
                        - `PAY:UBER_RIDE:85:EGP`
                        - `PAY:PARKING_FEE:25:EGP`
                        
                        **Instructions:**
                        1. Scan QR code with your device
                        2. Copy the QR string here
                        3. Click "PROCESS PAYMENT"
                        4. Confirm payment from your wallet
                        """)
                        
                        gr.Markdown("**Current Balance**")
                        balance_display = gr.Textbox(label="Wallet Balance", interactive=False)
                        refresh_balance_btn = gr.Button("🔄 Refresh Balance")
                        refresh_balance_btn.click(
                            lambda: f"EGP {current_user[8] if current_user else '0'}", 
                            outputs=[balance_display]
                        )

            # 6. MARKETPLACE (4.H, 4.J)
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

            # 6. OFFERS (4.G)
            with gr.TabItem("🎁 Offers"):
                gr.Markdown("### 4.G Exclusive Deals")
                offers = [f"{o[0]} - {o[1]}" for o in MarketplaceEngine.get_exclusive_offers()]
                dd_offer = gr.Dropdown(offers, label="Select Offer")
                btn_offer = gr.Button("Claim Voucher")
                out_offer = gr.Textbox()
                btn_offer.click(ui_claim_offer, inputs=[dd_offer], outputs=[out_offer])
                
            # 7. AI
            with gr.TabItem("🤖 Horus AI"):
                gr.Markdown(f"Powered by **{HorusConfig.AI_MODEL}**")
                gr.ChatInterface(fn=ask_ai, type="messages")
                
            # 8. ADMIN
            with gr.TabItem("⚙️ Admin"):
                gr.Markdown("### System Sync (Force Push)")
                btn_s = gr.Button("Sync Code & Docs to GitHub", variant="stop")
                out_s = gr.TextArea(label="Diagnostic Logs")
                btn_s.click(GitAutopilot.sync_codebase, outputs=[out_s])

    # Event Wiring
    btn.click(ui_login, inputs=[cam, passport, nat, full_name, passport_expiry], outputs=[status, app, activation_panel, bal, score, activation_status])
    btn_demo.click(ui_demo_login, outputs=[status, app, activation_panel, bal, score, activation_status])

if __name__ == "__main__":
    demo.queue().launch(share=True)
