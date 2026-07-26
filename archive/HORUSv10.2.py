# ==============================================================================
# HORUS v10.2.py - Self-Healing Architecture & Enhanced QR
# ==============================================================================

# STANDARD LIBRARY IMPORTS (System Prep)
import os
import sys
import subprocess
import importlib.util
import platform
import logging
from pathlib import Path

# Configure logging for system operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==============================================================================
# 🛠️ SELF-HEALING DEPENDENCY INSTALLER
# ==============================================================================

def is_linux_colab():
    """Check if running on Linux (Google Colab) environment"""
    try:
        return platform.system() == "Linux" and "google.colab" in sys.modules
    except:
        return False

def check_package_installed(package_name):
    """Check if a package is installed using importlib.util"""
    try:
        # Handle special cases for package names vs import names
        import_name = {
            'pillow': 'PIL',
            'opencv-python': 'cv2',
            'reportlab': 'reportlab',
            'gradio': 'gradio',
            'pyzbar': 'pyzbar',
            'qrcode': 'qrcode',
            'numpy': 'numpy',
            'google-generativeai': 'google.generativeai'
        }.get(package_name.lower(), package_name.lower())
        
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False

def install_system_dependencies():
    """Install system-level dependencies (libzbar0 for QR scanning)"""
    if is_linux_colab():
        try:
            logger.info("🐧 Linux (Colab) detected - Installing system dependencies...")
            # Install libzbar0 BEFORE importing pyzbar
            subprocess.run(["apt-get", "install", "-y", "libzbar0"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            logger.info("✅ System dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install system dependencies: {e}")
            return False
    else:
        logger.info("ℹ️ Non-Linux environment detected - Skipping system dependencies")
        return True

def install_python_dependencies():
    """Install Python packages with robust error handling"""
    required_packages = [
        'gradio>=4.0.0',
        'pyzbar',
        'qrcode[pil]',
        'pillow',
        'opencv-python',
        'reportlab',
        'numpy',
        'google-generativeai'
    ]
    
    missing_packages = []
    for package in required_packages:
        package_name = package.split('>=')[0].split('[')[0]
        if not check_package_installed(package_name):
            missing_packages.append(package)
            logger.warning(f"📦 Missing package: {package}")
        else:
            logger.info(f"✅ Package already installed: {package}")
    
    if not missing_packages:
        logger.info("🎉 All Python packages are already installed!")
        return True
    
    logger.info(f"📦 Installing {len(missing_packages)} missing packages...")
    
    for package in missing_packages:
        try:
            logger.info(f"📦 Installing {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--upgrade', package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install {package}: {e}")
            return False
    
    logger.info("🎉 Python dependencies installation complete!")
    return True

def install_dependencies():
    """
    Self-healing dependency installer with system and Python package management
    """
    logger.info("🚀 Starting self-healing dependency installation...")
    
    # Step 1: Install system dependencies (libzbar0 for QR scanning)
    if not install_system_dependencies():
        logger.error("❌ System dependency installation failed")
        return False
    
    # Step 2: Install Python packages
    if not install_python_dependencies():
        logger.error("❌ Python dependency installation failed")
        return False
    
    logger.info("✅ All dependencies installed successfully!")
    return True

# ==============================================================================
# 📚 HEAVY IMPORTS (Safe Import Pattern)
# ==============================================================================

def safe_import_with_error_handling():
    """Perform heavy imports with comprehensive error handling"""
    import_status = {}
    
    try:
        import gradio as gr
        import_status['gradio'] = True
        logger.info("✅ Gradio imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Gradio: {e}")
        import_status['gradio'] = False
    
    try:
        import numpy as np
        import_status['numpy'] = True
        logger.info("✅ NumPy imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import NumPy: {e}")
        import_status['numpy'] = False
    
    try:
        from PIL import Image
        import_status['pillow'] = True
        logger.info("✅ Pillow imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Pillow: {e}")
        import_status['pillow'] = False
    
    try:
        import cv2
        import_status['opencv'] = True
        logger.info("✅ OpenCV imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import OpenCV: {e}")
        import_status['opencv'] = False
    
    try:
        from pyzbar import pyzbar
        import_status['pyzbar'] = True
        logger.info("✅ Pyzbar imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Pyzbar: {e}")
        import_status['pyzbar'] = False
    
    try:
        import qrcode
        import_status['qrcode'] = True
        logger.info("✅ QRCode imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import QRCode: {e}")
        import_status['qrcode'] = False
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import_status['reportlab'] = True
        logger.info("✅ ReportLab imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import ReportLab: {e}")
        import_status['reportlab'] = False
    
    try:
        from google import genai
        import_status['genai'] = True
        logger.info("✅ Google Generative AI imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Google Generative AI: {e}")
        import_status['genai'] = False
    
    try:
        import sqlite3
        import_status['sqlite3'] = True
        logger.info("✅ SQLite3 imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import SQLite3: {e}")
        import_status['sqlite3'] = False
    
    return import_status

# Run the self-healing installer
if not install_dependencies():
    logger.error("❌ CRITICAL: Dependency installation failed. Some features may not work.")
    sys.exit(1)

# Perform safe imports
import_status = safe_import_with_error_handling()

# Check critical imports
critical_imports = ['gradio', 'numpy', 'sqlite3']
failed_critical = [pkg for pkg in critical_imports if not import_status.get(pkg, False)]

if failed_critical:
    logger.error(f"❌ CRITICAL: Failed to import critical packages: {failed_critical}")
    sys.exit(1)

# Assign imported modules to global namespace
gr = globals().get('gr')
np = globals().get('np')
Image = globals().get('Image')
cv2 = globals().get('cv2')
pyzbar = globals().get('pyzbar')
qrcode = globals().get('qrcode')
canvas = globals().get('canvas')
letter = globals().get('letter')
ImageReader = globals().get('ImageReader')
pdfmetrics = globals().get('pdfmetrics')
TTFont = globals().get('TTFont')
genai = globals().get('genai')
sqlite3 = globals().get('sqlite3')

# Additional standard library imports
import json
import hashlib
import random
import threading
import datetime
import io
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple

# ==============================================================================
# 🏛️ CONFIGURATION & UTILITIES
# ==============================================================================

@dataclass
class HorusConfig:
    """Enhanced configuration for HORUS v10.2 with self-healing capabilities"""
    APP_NAME: str = "Horus Key Platinum v10.2"
    DB_NAME: str = "HorusDB.db"
    AI_MODEL: str = "gemini-1.5-flash"
    VERSION: str = "10.2.0-Gold (Self-Healing)"
    PRICING: dict = field(default_factory=lambda: {
        "visa_fee": 2000,
        "monument_foreign_adult": 600,
        "monument_foreign_student": 300,
        "monument_local_adult": 120,
        "monument_local_student": 60,
        "transport_base": 20,
        "esim_orange": 500,
        "esim_vodafone": 400,
        "souvenir_base": 250,
        "activation_deposit": 10000  # EGP equivalent of $200 USD
    })
    
    # Self-healing configuration
    AUTO_INSTALL_DEPS: bool = True
    QR_SCANNER_ENABLED: bool = import_status.get('pyzbar', False)
    CAMERA_ENABLED: bool = import_status.get('opencv', False)
    AI_ENABLED: bool = import_status.get('genai', False)
    
    @classmethod
    def get_system_status(cls):
        """Get comprehensive system status"""
        return {
            "version": cls.VERSION,
            "platform": platform.system(),
            "is_colab": is_linux_colab(),
            "dependencies": import_status,
            "qr_scanner": cls.QR_SCANNER_ENABLED,
            "camera": cls.CAMERA_ENABLED,
            "ai": cls.AI_ENABLED
        }

class ReadmeGenerator:
    """Enhanced README generator with system status and troubleshooting"""
    
    @staticmethod
    def generate_readme():
        """Generate comprehensive README with troubleshooting guide"""
        system_status = HorusConfig.get_system_status()
        
        readme_content = f"""
# {HorusConfig.APP_NAME}

## 🚀 Self-Healing Architecture

HORUS v10.2 features an intelligent dependency management system that automatically detects and installs missing packages.

## 📋 System Requirements

### Core Dependencies (Auto-Installed)
- **Python 3.8+**
- **Gradio 4.0+** - Web interface
- **SQLite3** - Database (built-in)
- **NumPy** - Numerical operations

### QR Scanner Dependencies
- **Pyzbar** - QR code decoding
- **OpenCV** - Image processing
- **Pillow** - Image handling

### System Dependencies (Linux/Colab)
- **libzbar0** - QR code library (auto-installed on Colab)

### Optional Dependencies
- **ReportLab** - PDF generation
- **Google Generative AI** - AI chat functionality

## 🔧 Installation

### Automatic Installation (Recommended)
```bash
python HORUSv10.2.py
```
The application will automatically detect and install missing dependencies.

### Manual Installation
```bash
# System dependencies (Linux/Colab only)
sudo apt-get update
sudo apt-get install -y libzbar0

# Python dependencies
pip install gradio>=4.0.0 pyzbar qrcode[pil] pillow opencv-python reportlab numpy google-generativeai
```

## 🛠️ Troubleshooting

### QR Scanner Not Working
**Issue**: "No QR code detected" or QR decoding errors
**Solution**:
1. Ensure good lighting and clear QR code
2. Check camera permissions
3. Verify pyzbar installation: `pip install --upgrade pyzbar`
4. On Linux: `sudo apt-get install -y libzbar0`

### Camera Not Working
**Issue**: "HARDWARE ERROR: WEBCAM DATA INVALID"
**Solution**:
1. Check browser camera permissions
2. Try different browser (Chrome/Firefox)
3. Ensure OpenCV is installed: `pip install --upgrade opencv-python`

### AI Chat Not Working
**Issue**: "Configuration Error: Please grant access to 'GEMINI_KEYS'"
**Solution**:
1. Set environment variable: `export GEMINI_KEYS="your-api-key"`
2. In Colab: Add GEMINI_KEYS to notebook secrets
3. Get API key from: https://makersuite.google.com/app/apikey

### PDF Generation Issues
**Issue**: Visa PDF not downloading
**Solution**:
1. Ensure ReportLab is installed: `pip install --upgrade reportlab`
2. Check browser download settings
3. Try different browser

## 📊 System Status

Current system status:
- **Platform**: {system_status['platform']}
- **Colab Environment**: {system_status['is_colab']}
- **QR Scanner**: {'✅ Available' if system_status['qr_scanner'] else '❌ Not Available'}
- **Camera**: {'✅ Available' if system_status['camera'] else '❌ Not Available'}
- **AI Chat**: {'✅ Available' if system_status['ai'] else '❌ Not Available'}

## 🎯 Features

### Core Features
- ✅ Biometric Security (SHA-512)
- ✅ Wallet & Banking Integration
- ✅ Family Mode Ticketing
- ✅ Green Score System
- ✅ Real Egypt Transport Options

### Enhanced Features
- ✅ Deep Data Collection (15 fields)
- ✅ Welcome Gift System
- ✅ QR Code Scanning (Camera + Manual)
- ✅ AI Chat Assistant
- ✅ PDF Document Generation
- ✅ Self-Healing Dependencies

### Security Features
- ✅ Activation Gate ($200 USD deposit)
- ✅ Visa Policy Enforcement
- ✅ Transaction Logging
- ✅ Bank Integration

## 🚀 Quick Start

1. Run the application: `python HORUSv10.2.py`
2. Click "🔑 DEMO ACCESS" for instant testing
3. Or use "SCAN FACE & ENTER ECOSYSTEM" for full registration
4. Activate wallet with $200 USD deposit (demo bypasses this)
5. Explore all features: Visa, Transport, Monuments, QR Payments

## 📞 Support

For issues and support:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Check system status in the application
4. Review logs for detailed error messages

---
*HORUS v10.2 - Self-Healing Smart Travel Platform*
"""
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        logger.info("✅ README.md generated successfully")
        return "README.md"

# ==============================================================================
# 🔐 SECURITY & BIOMETRICS
# ==============================================================================

class HorusSecurity:
    """Enhanced security class with robust biometric handling"""
    
    @staticmethod
    def hash_biometric(data: str) -> str:
        """Generate SHA-512 hash for biometric data"""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def generate_digital_stamp(passport: str, nationality: str) -> Tuple[str, str]:
        """Generate unique digital stamp for visa documents"""
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        stamp = f"VISA-{nationality[:2].upper()}-{passport[-4:]}-{ts}"
        return stamp, ts
    
    @staticmethod
    def scan_face(image) -> Optional[str]:
        """
        Enhanced biometric scanning with comprehensive None handling
        SECURITY FIX: Prevent "HARDWARE ERROR" with proper None input handling
        """
        # SECURITY FIX: Strict None input handling
        if image is None:
            logger.warning("Biometric scan received None input")
            return None
        
        # SECURITY FIX: Validate numpy array type and shape
        if not isinstance(image, np.ndarray):
            logger.warning(f"Biometric scan received invalid type: {type(image)}")
            return None
        
        # SECURITY FIX: Validate image dimensions
        if len(image.shape) < 2 or len(image.shape) > 3:
            logger.warning(f"Biometric scan received invalid image shape: {image.shape}")
            return None
        
        try:
            # Convert numpy array to PIL Image for processing
            if len(image.shape) == 3:
                # RGB image, convert to PIL
                pil_image = Image.fromarray(image.astype('uint8'))
            else:
                # Grayscale image, convert to PIL
                pil_image = Image.fromarray(image.astype('uint8'), mode='L')
            
            # Simulate biometric processing (in production, use actual face recognition)
            # For demo, we'll generate a consistent hash based on image properties
            img_bytes = pil_image.tobytes()
            bio_hash = hashlib.sha512(img_bytes).hexdigest()
            
            logger.info("Biometric scan successful")
            return bio_hash
            
        except Exception as e:
            logger.error(f"Biometric scan failed: {str(e)}")
            return None

# ==============================================================================
# 📱 QR DECODING ENHANCEMENT
# ==============================================================================

class QRDecoder:
    """
    Enhanced QR Code Decoding class using pyzbar for robust QR functionality
    Supports decoding from webcam images and various QR formats
    """
    
    @staticmethod
    def decode_from_image(image) -> List[str]:
        """
        Decode QR codes from numpy array image
        Returns list of decoded QR data strings
        """
        if image is None:
            logger.warning("QR decode received None image")
            return []
        
        try:
            # Convert numpy array to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(image.astype('uint8'))
            else:
                pil_image = Image.fromarray(image.astype('uint8'), mode='L')
            
            # Convert PIL to OpenCV format for pyzbar
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Decode QR codes
            decoded_objects = pyzbar.decode(opencv_image)
            
            # Extract data from decoded objects
            qr_data = []
            for obj in decoded_objects:
                qr_data.append(obj.data.decode('utf-8'))
            
            logger.info(f"Decoded {len(qr_data)} QR codes from image")
            return qr_data
            
        except Exception as e:
            logger.error(f"QR decoding failed: {str(e)}")
            return []
    
    @staticmethod
    def validate_payment_qr(qr_data: str) -> bool:
        """
        Validate if QR data follows payment format: PAY:VENDOR_ID:AMOUNT:CURRENCY
        """
        if not qr_data or not isinstance(qr_data, str):
            return False
        
        try:
            parts = qr_data.strip().split(':')
            return (
                len(parts) == 4 and 
                parts[0] == 'PAY' and
                parts[1].strip() and  # vendor_id not empty
                parts[2].replace('.', '').isdigit() and  # amount is numeric
                parts[3].strip()  # currency not empty
            )
        except Exception:
            return False
    
    @staticmethod
    def parse_payment_qr(qr_data: str) -> Optional[Dict[str, str]]:
        """
        Parse payment QR data into structured dictionary
        Returns: {'vendor_id': str, 'amount': str, 'currency': str}
        """
        if not QRDecoder.validate_payment_qr(qr_data):
            return None
        
        try:
            parts = qr_data.strip().split(':')
            return {
                'vendor_id': parts[1].strip(),
                'amount': parts[2].strip(),
                'currency': parts[3].strip()
            }
        except Exception:
            return None

# ==============================================================================
# 🧠 LOGIC ENGINES
# ==============================================================================

class VisaPolicy:
    """Military-grade visa policy enforcement with hardcoded eligibility"""
    
    ELIGIBLE_COUNTRIES = [
        "USA", "UK", "Germany", "France", "Italy", "Spain", "Netherlands", "Belgium",
        "Austria", "Switzerland", "Sweden", "Norway", "Denmark", "Finland", "Iceland",
        "Japan", "South Korea", "Singapore", "Malaysia", "Australia", "New Zealand",
        "Canada", "UAE", "Saudi Arabia", "Kuwait", "Bahrain", "Qatar", "Oman",
        "Russia", "China", "India", "Brazil", "Argentina", "Mexico", "South Africa",
        "Egypt", "Jordan", "Lebanon", "Morocco", "Tunisia", "Algeria", "Libya",
        "Sudan", "Ethiopia", "Kenya", "Tanzania", "Uganda", "Rwanda", "Ghana",
        "Nigeria", "Senegal", "Ivory Coast", "Cameroon", "DR Congo", "Zambia",
        "Zimbabwe", "Botswana", "Namibia", "Mozambique", "Angola", "Madagascar"
    ]
    
    RESTRICTED_COUNTRIES = [
        "Iran", "Afghanistan", "Syria", "Yemen", "Libya", "Somalia", 
        "North Korea", "Sudan", "Lebanon", "Iraq", "Palestine"
    ]
    
    @staticmethod
    def get_nationality_group(nationality: str) -> str:
        """Classify nationality for pricing and policy purposes"""
        if nationality == "Egypt":
            return "Egyptian"
        elif nationality in ["Jordan", "Lebanon", "Morocco", "Tunisia", "Algeria", "Libya", "Sudan"]:
            return "Arab"
        else:
            return "Foreign"
    
    @staticmethod
    def check_eligibility(nationality: str) -> bool:
        """Check if nationality is eligible for Visa on Arrival"""
        return nationality in VisaPolicy.ELIGIBLE_COUNTRIES
    
    @staticmethod
    def is_restricted(nationality: str) -> bool:
        """Check if nationality is restricted from all services"""
        return nationality in VisaPolicy.RESTRICTED_COUNTRIES

class PriceCalculator:
    """Dynamic pricing calculator with nationality and visitor type considerations"""
    
    @staticmethod
    def calculate_ticket_price(base_price: float, nationality_group: str, visitor_type: str, quantity: int = 1) -> float:
        """Calculate ticket price based on multiple factors"""
        multiplier = 1.0
        
        # Nationality pricing
        if nationality_group == "Egyptian":
            multiplier *= 0.2  # 20% of foreign price
        elif nationality_group == "Arab":
            multiplier *= 0.5  # 50% of foreign price
        
        # Visitor type pricing
        if visitor_type == "Student":
            multiplier *= 0.5  # 50% discount
        elif visitor_type == "Kid":
            multiplier *= 0.3  # 70% discount
        
        return base_price * multiplier * quantity
    
    @staticmethod
    def get_visa_fee() -> int:
        """Get standard visa fee"""
        return HorusConfig.PRICING["visa_fee"]
    
    @staticmethod
    def get_activation_deposit() -> int:
        """Get activation deposit amount"""
        return HorusConfig.PRICING["activation_deposit"]

class EcoEngine:
    """Environmental impact calculator for transportation choices"""
    
    @staticmethod
    def calculate_impact(mode: str) -> Tuple[int, str]:
        """Calculate green points and impact label for transport mode"""
        if mode in ["Cairo Monorail", "LRT (Electric Train)", "Electric Bus", "Metro Line 1", "Metro Line 2", "Metro Line 3"]:
            return 20, "🌿 Eco-Friendly"
        elif mode in ["Shared Shuttle", "Train"]:
            return 10, "🍃 Shared Transport"
        else:
            return 0, "🚗 Private Transport"

class MarketplaceEngine:
    """Marketplace engine for eSIMs, souvenirs, and exclusive offers"""
    
    @staticmethod
    def get_esims() -> List[Tuple[str, str, int]]:
        """Get available eSIM plans"""
        return [
            ("Orange Egypt", "30GB + Unlimited Calls", HorusConfig.PRICING["esim_orange"]),
            ("Vodafone", "20GB + Unlimited Calls", HorusConfig.PRICING["esim_vodafone"])
        ]
    
    @staticmethod
    def get_souvenirs() -> List[Tuple[str, str, int]]:
        """Get available souvenir items"""
        return [
            ("Pharaonic Amulet", "Authentic Egyptian Jewelry", HorusConfig.PRICING["souvenir_base"]),
            ("Papyrus Scroll", "Hand-painted Ancient Art", HorusConfig.PRICING["souvenir_base"]),
            ("Alabaster Statue", "Miniature Pyramid Replica", HorusConfig.PRICING["souvenir_base"])
        ]
    
    @staticmethod
    def get_exclusive_offers() -> List[Tuple[str, str]]:
        """Get exclusive offers for travelers"""
        return [
            ("Pyramids Sunset Tour", "30% off guided experience"),
            ("Nile Dinner Cruise", "Free upgrade to VIP deck"),
            ("Luxor Temple Access", "Skip-the-line priority entry")
        ]

class DocumentIssuer:
    """Document generation engine for visas and official documents"""
    
    @staticmethod
    def generate_visa_pdf(traveler_info: Dict[str, str], stamp: str, data: str) -> str:
        """Generate visa PDF with enhanced security features"""
        filename = f"visa_{traveler_info['passport']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Try to load fonts, fallback to default if not available
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Header
        c.setFont(font_name, 16)
        c.drawString(100, 750, "ARAB REPUBLIC OF EGYPT")
        c.drawString(100, 730, "MINISTRY OF FOREIGN AFFAIRS")
        
        # Visa details
        c.setFont(font_name, 12)
        c.drawString(100, 680, f"Visa Number: {stamp}")
        c.drawString(100, 660, f"Name: {traveler_info['full_name']}")
        c.drawString(100, 640, f"Passport: {traveler_info['passport']}")
        c.drawString(100, 620, f"Nationality: {traveler_info['nationality']}")
        c.drawString(100, 600, f"Type: Tourist Visa")
        c.drawString(100, 580, f"Valid Until: {datetime.datetime.now() + datetime.timedelta(days=180)}")
        
        # Security watermark
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 400, "EGYPT")
        
        c.save()
        return filename

# ==============================================================================
# 🗄️ DATABASE LAYER - DEEP DATA COMPLIANCE
# ==============================================================================

class HorusDB:
    """Thread-safe singleton database with deep data fields per Procedure Doc 1030"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.conn = sqlite3.connect(HorusConfig.DB_NAME, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self._init_schema()
            self.initialized = True
    
    def _init_schema(self):
        """Initialize database schema with deep data fields"""
        # Drop existing tables for clean migration
        self.cursor.execute("DROP TABLE IF EXISTS travelers")
        self.cursor.execute("DROP TABLE IF EXISTS tickets")
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute("DROP TABLE IF EXISTS monuments")
        self.cursor.execute("DROP TABLE IF EXISTS visas")
        
        # Updated travelers table with DEEP DATA fields (15 total)
        self.cursor.execute('''
            CREATE TABLE travelers (
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
                created_at TEXT,
                -- DEEP DATA FIELDS (Procedure Doc 1030)
                occupation TEXT,
                purpose_of_travel TEXT,
                accommodation_address TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE tickets (
                id INTEGER PRIMARY KEY,
                traveler_id INTEGER,
                monument_name TEXT,
                visitor_type TEXT,
                quantity INTEGER,
                price REAL,
                created_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY,
                traveler_id INTEGER,
                description TEXT,
                amount REAL,
                category TEXT,
                created_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE monuments (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                description TEXT,
                base_price_foreigner REAL,
                location TEXT,
                google_maps_link TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE visas (
                id INTEGER PRIMARY KEY,
                traveler_id INTEGER,
                stamp TEXT UNIQUE,
                created_at TEXT
            )
        ''')
        
        # Seed monuments with Google Maps links
        monuments_data = [
            ("Great Pyramid", "The last surviving Wonder of the Ancient World", 600, "Giza Plateau, Egypt", "https://maps.google.com/?q=Great+Pyramid+Giza"),
            ("Karnak Temple", "Largest ancient religious site in the world", 400, "Luxor, Egypt", "https://maps.google.com/?q=Karnak+Temple+Luxor"),
            ("GEM Museum", "Grand Egyptian Museum - Home to Tutankhamun treasures", 300, "Giza, Egypt", "https://maps.google.com/?q=Grand+Egyptian+Museum"),
            ("Valley of Kings", "Royal burial ground of pharaohs", 350, "Luxor, Egypt", "https://maps.google.com/?q=Valley+of+Kings+Luxor"),
            ("Abu Simbel", "Massive rock temples built by Ramesses II", 450, "Aswan, Egypt", "https://maps.google.com/?q=Abu+Simbel+Aswan")
        ]
        
        self.cursor.executemany('''
            INSERT INTO monuments (name, description, base_price_foreigner, location, google_maps_link)
            VALUES (?, ?, ?, ?, ?)
        ''', monuments_data)
        
        self.conn.commit()
        logger.info("Database schema initialized with deep data fields")
    
    def register_traveler(self, name, full_name, passport, nationality, nationality_group, expiry, bio_hash, occupation, purpose_of_travel, accommodation_address):
        """Register traveler with deep data fields"""
        self.cursor.execute('''
            INSERT INTO travelers 
            (name, full_name, passport_number, nationality, nationality_group, passport_expiry, biometric_hash, occupation, purpose_of_travel, accommodation_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, full_name, passport, nationality, nationality_group, expiry, bio_hash, occupation, purpose_of_travel, accommodation_address, datetime.datetime.now().isoformat()))
        self.conn.commit()
        logger.info(f"Traveler registered: {name} with deep data fields")
        return self.cursor.lastrowid
    
    def get_traveler(self, tid):
        """Get traveler information by ID"""
        self.cursor.execute("SELECT * FROM travelers WHERE id=?", (tid,))
        return self.cursor.fetchone()
    
    def activate_wallet(self, tid, card_number):
        """Activate wallet with $200 USD deposit"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_status='ACTIVE', wallet_balance=?, bank_linked=1 WHERE id=?", 
                              (HorusConfig.PRICING["activation_deposit"], tid))
            self.conn.commit()
            logger.info(f"Wallet activated for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Wallet activation failed: {e}")
            return False
    
    def top_up(self, tid, amount):
        """Add funds to wallet"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance+? WHERE id=?", (amount, tid))
            self.conn.commit()
            logger.info(f"Wallet topped up: {amount} EGP for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Wallet top-up failed: {e}")
            return False
    
    def purchase(self, tid, description, amount, category):
        """Process purchase transaction with comprehensive logging"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and traveler[8] >= amount:  # wallet_balance check
                self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance-? WHERE id=?", (amount, tid))
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, created_at) VALUES (?, ?, ?, ?, ?)",
                                  (tid, description, amount, category, datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Purchase processed: {description} - {amount} EGP for traveler {tid}")
                return True
            else:
                logger.warning(f"Insufficient funds for traveler {tid}: balance={traveler[8] if traveler else 0}, required={amount}")
                return False
        except Exception as e:
            logger.error(f"Purchase processing failed: {e}")
            return False
    
    def create_ticket(self, traveler_id, monument_name, visitor_type, quantity, price):
        """Create ticket record with detailed logging"""
        try:
            self.cursor.execute('''
                INSERT INTO tickets (traveler_id, monument_name, visitor_type, quantity, price, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (traveler_id, monument_name, visitor_type, quantity, price, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Ticket created: {monument_name} - {quantity} {visitor_type} for traveler {traveler_id}")
            return True
        except Exception as e:
            logger.error(f"Ticket creation failed: {e}")
            return False
    
    def add_green_points(self, tid, points):
        """Add green points to traveler with logging"""
        try:
            self.cursor.execute("UPDATE travelers SET green_points=green_points+? WHERE id=?", (points, tid))
            self.conn.commit()
            logger.info(f"Green points added: {points} points for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Green points addition failed: {e}")
            return False
    
    def claim_gift(self, tid):
        """Claim welcome gift - returns success status with logging"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and not traveler[12]:  # has_claimed_gift is at index 12
                self.cursor.execute("UPDATE travelers SET has_claimed_gift = 1 WHERE id=?", (tid,))
                # Log gift transaction
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, created_at) VALUES (?, ?, ?, ?, ?)",
                                  (tid, "Welcome Gift Claimed", 0, "GIFT", datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Welcome gift claimed for traveler {tid}")
                return True
            else:
                logger.warning(f"Gift claim failed for traveler {tid}: already claimed or not found")
                return False
        except Exception as e:
            logger.error(f"Gift claim failed: {e}")
            return False
    
    def link_bank(self, tid, bank_name):
        """Link bank account to traveler with logging"""
        try:
            self.cursor.execute("UPDATE travelers SET bank_linked=1 WHERE id=?", (tid,))
            self.conn.commit()
            logger.info(f"Bank linked: {bank_name} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Bank linking failed: {e}")
            return False
    
    def add_visa(self, tid, stamp):
        """Add visa record with logging"""
        try:
            self.cursor.execute("INSERT INTO visas (traveler_id, stamp, created_at) VALUES (?, ?, ?)",
                              (tid, stamp, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Visa added: {stamp} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Visa addition failed: {e}")
            return False
    
    def get_data(self, table):
        """Generic data retrieval with error handling"""
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Data retrieval failed for table {table}: {e}")
            return []
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        try:
            stats = {}
            stats['total_travelers'] = self.cursor.execute("SELECT COUNT(*) FROM travelers").fetchone()[0]
            stats['active_wallets'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE wallet_status='ACTIVE'").fetchone()[0]
            stats['total_transactions'] = self.cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            stats['total_visas'] = self.cursor.execute("SELECT COUNT(*) FROM visas").fetchone()[0]
            stats['gifts_claimed'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE has_claimed_gift=1").fetchone()[0]
            return stats
        except Exception as e:
            logger.error(f"System stats retrieval failed: {e}")
            return {}

# ==============================================================================
# 🤖 GIT AUTOPILOT & AI SERVICES
# ==============================================================================

class GitAutopilot:
    """Automated Git repository management with enhanced logging"""
    
    @staticmethod
    def sync_codebase():
        """Sync codebase to GitHub repository with comprehensive error handling"""
        try:
            # Initialize git repository if not exists
            if not os.path.exists(".git"):
                logger.info("Initializing Git repository...")
                os.system("git init")
                os.system("git branch -M main")
            
            # Add all files
            logger.info("Adding files to Git...")
            os.system("git add .")
            
            # Check if there are changes to commit
            result = os.system("git diff --cached --quiet")
            if result == 0:  # No changes to commit
                logger.info("No changes to commit")
                return "✅ No changes to commit - repository is up to date"
            
            # Commit with timestamp
            commit_msg = f"HORUS v{HorusConfig.VERSION} - Auto-sync {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            logger.info(f"Committing changes: {commit_msg}")
            os.system(f'git commit -m "{commit_msg}"')
            
            # Push to remote (if configured)
            # os.system("git push origin main")
            
            logger.info(f"Code synced successfully. Commit: {commit_msg}")
            return f"✅ Code synced successfully. Commit: {commit_msg}"
        except Exception as e:
            logger.error(f"Git sync failed: {str(e)}")
            return f"❌ Sync failed: {str(e)}"

def get_rotated_key():
    """Get API key with rotation logic and validation"""
    keys = os.getenv("GEMINI_KEYS", "").split(",")
    if not keys or not keys[0]:
        logger.warning("No GEMINI_KEYS environment variable found")
        return None
    key = keys[0].strip()
    if not key or len(key) < 10:
        logger.warning("Invalid API key format")
        return None
    return key

def ask_ai(msg, history):
    """Enhanced AI chat interface with comprehensive error handling"""
    if not HorusConfig.AI_ENABLED:
        return "⚠️ AI Chat is not available. Please install google-generativeai package."
    
    key = get_rotated_key()
    if not key: 
        return "⚠️ Configuration Error: Please set GEMINI_KEYS environment variable with your API key."
    
    try:
        client = genai.Client(api_key=key)
        res = client.models.generate_content(
            model=HorusConfig.AI_MODEL, 
            contents=msg
        )
        logger.info(f"AI response generated for message: {msg[:50]}...")
        return res.text
    except Exception as e: 
        logger.error(f"AI chat error: {str(e)}")
        return f"AI Error: {str(e)}"

# ==============================================================================
# 📱 UI (PLATINUM DASHBOARD) - ENHANCED WITH SELF-HEALING
# ==============================================================================

current_user = None

def ui_login(image, passport, nationality, full_name, passport_expiry, occupation, purpose_of_travel, accommodation_address):
    """Enhanced login with critical None fix and deep data capture"""
    global current_user
    
    # CRITICAL FIX: Check for None image first
    if image is None:
        return "⚠️ Waiting for biometric scan...", gr.update(), gr.update(), "", "", ""
    
    # Robust numpy check
    if not isinstance(image, np.ndarray):
        return "❌ HARDWARE ERROR: WEBCAM DATA INVALID", gr.update(), gr.update(), "", "", ""
    
    bio_hash = HorusSecurity.scan_face(image)
    if not bio_hash:
        return "❌ BIOMETRIC SCAN FAILED", gr.update(), gr.update(), "", "", ""

    nationality_group = VisaPolicy.get_nationality_group(nationality)
    name = f"Traveler-{nationality[:3].upper()}-{passport[-4:]}"
    
    # Register with DEEP DATA fields
    uid = db.register_traveler(name, full_name, passport, nationality, nationality_group, passport_expiry, bio_hash, occupation, purpose_of_travel, accommodation_address)
    current_user = db.get_traveler(uid)
    
    wallet_status = current_user[9]
    wallet_balance = current_user[8]
    green_points = current_user[11]
    
    if wallet_status == 'LOCKED':
        return (
            f"✅ Verified: {name} - WALLET LOCKED",
            gr.Group(visible=False),
            gr.Group(visible=True),
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "🔒 ACCOUNT LOCKED - Deposit $200 USD to activate"
        )
    else:
        return (
            f"✅ Verified: {name} - ACCOUNT ACTIVE",
            gr.Group(visible=True),
            gr.Group(visible=False),
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "✅ ACCOUNT ACTIVE - All features available"
        )

def ui_activate_wallet(card_number):
    """Activate wallet with enhanced validation and logging"""
    global current_user
    
    if not current_user: 
        return "❌ Login required", gr.update(), gr.update()
    
    if not card_number or len(card_number) < 16:
        return "❌ Invalid card number", gr.update(), gr.update()
    
    if db.activate_wallet(current_user[0], card_number):
        # Refresh user data from DB to get updated status
        current_user = db.get_traveler(current_user[0])
        return (
            f"✅ Wallet Activated! 10,000 EGP deposited. Welcome to HORUS!",
            gr.Group(visible=True),   # Show App
            gr.Group(visible=False)   # Hide Activation Panel
        )
    else:
        return "❌ Activation failed", gr.update(), gr.update()

def ui_link_bank(bank_name):
    """Link bank account to traveler with logging"""
    if not current_user: return "❌ Login required"
    if db.link_bank(current_user[0], bank_name):
        return f"✅ Bank linked: {bank_name}"
    else:
        return "❌ Bank linking failed"

def process_qr_payment(qr_string):
    """Process QR payment with enhanced validation and logging"""
    global current_user
    
    if not current_user:
        return "❌ Login required to make payments"
    
    wallet_status = current_user[9]
    if wallet_status != 'ACTIVE':
        return "❌ Wallet locked. Please activate your account to make payments."
    
    if not qr_string:
        return "❌ No QR data provided"
    
    try:
        parts = qr_string.strip().split(':')
        
        if len(parts) != 4 or parts[0] != 'PAY':
            return "❌ Invalid QR Format. Expected: PAY:VENDOR_ID:AMOUNT:CURRENCY"
        
        vendor_id = parts[1]
        amount_str = parts[2]
        currency = parts[3]
        
        try:
            amount = float(amount_str)
        except ValueError:
            return "❌ Invalid amount in QR code"
        
        if currency.upper() != 'EGP':
            return f"❌ Currency {currency} not supported. Only EGP accepted."
        
        current_balance = current_user[8]
        
        if amount > current_balance:
            return f"❌ Insufficient Funds. Balance: {current_balance} EGP, Required: {amount} EGP"
        
        if db.purchase(current_user[0], f"QR Payment to {vendor_id}", amount, "QR_PAYMENT"):
            # Refresh user data from DB to get updated balance
            current_user = db.get_traveler(current_user[0])
            new_balance = current_user[8]
            
            return f"✅ PAID {amount} EGP to {vendor_id}. Balance: {new_balance} EGP."
        else:
            return "❌ Payment processing failed"
            
    except Exception as e:
        logger.error(f"QR Payment Error: {e}")
        return "❌ Error processing QR payment"

def ui_scan_qr(qr_input):
    """Scan QR code from manual input"""
    return process_qr_payment(qr_input)

def ui_scan_qr_from_camera(image):
    """Enhanced QR scanning from webcam using QRDecoder"""
    if image is None:
        return "⚠️ Please position QR code in front of camera"
    
    try:
        # Convert PIL Image to numpy array for QRDecoder
        image_array = np.array(image)
        
        # Decode QR codes using enhanced QRDecoder
        qr_data_list = QRDecoder.decode_from_image(image_array)
        
        if not qr_data_list:
            return "❌ No QR code detected. Please try again."
        
        # Process first detected QR code
        qr_data = qr_data_list[0]
        
        # Validate payment QR format
        if not QRDecoder.validate_payment_qr(qr_data):
            return f"❌ Invalid QR format detected: {qr_data}\nExpected: PAY:VENDOR_ID:AMOUNT:CURRENCY"
        
        # Process the payment
        result = process_qr_payment(qr_data)
        return f"📷 QR Scanned: {qr_data}\n{result}"
        
    except Exception as e:
        logger.error(f"QR Camera Scan Error: {e}")
        return f"❌ QR scanning failed: {str(e)}"

def ui_simulate_metro_scan():
    """Simulate scanning a Cairo Metro QR code for demo purposes"""
    simulated_qr = "PAY:CAIRO_METRO:50:EGP"
    result = process_qr_payment(simulated_qr)
    # Add transaction ID for visibility
    transaction_id = f"TXN-{random.randint(100000, 999999)}"
    return f"{result}\n📋 Transaction ID: {transaction_id}"

def ui_book_transport(mode, dest):
    """Book transportation with green points calculation"""
    global current_user
    if not current_user: return "Login First"
    pts, lbl = EcoEngine.calculate_impact(mode)
    cost = 20
    if db.purchase(current_user[0], f"Ride: {mode}", cost, "TRANSPORT"):
        db.add_green_points(current_user[0], pts)
        return f"✅ Booked {mode}. +{pts} Points."
    return "❌ No Funds"

def ui_get_monument_info(monument_name):
    """Get monument information including Google Maps link"""
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found"
    
    return f"📍 {monument_name}\n🗺️ Location: {target[4]}\n📄 Description: {target[2]}"

def ui_book_monument_family(monument_name, adults, students, kids):
    """
    FAMILY MODE: Book monument tickets for multiple visitor types
    Calculate: (Adults * Price) + (Students * Price * 0.5) + (Kids * Price * 0.3)
    """
    global current_user
    if not current_user: return "Login First"
    
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found"
    
    nationality_group_str = current_user[5]
    nationality_group = VisaPolicy.get_nationality_group(nationality_group_str)
    base_price = target[3]  # base_price_foreigner
    
    # Calculate prices for each visitor type
    adult_price = PriceCalculator.calculate_ticket_price(base_price, nationality_group, "Adult", adults)
    student_price = PriceCalculator.calculate_ticket_price(base_price, nationality_group, "Student", students)
    kid_price = PriceCalculator.calculate_ticket_price(base_price, nationality_group, "Kid", kids)
    
    total_price = adult_price + student_price + kid_price
    total_visitors = adults + students + kids
    
    if total_visitors == 0:
        return "❌ Please select at least one visitor"
    
    if db.purchase(current_user[0], f"Family Ticket: {monument_name}", total_price, "MONUMENTS"):
        # Create ticket records for each visitor type
        if adults > 0:
            db.create_ticket(current_user[0], monument_name, "Adult", adults, adult_price)
        if students > 0:
            db.create_ticket(current_user[0], monument_name, "Student", students, student_price)
        if kids > 0:
            db.create_ticket(current_user[0], monument_name, "Kid", kids, kid_price)
        
        return f"✅ ISSUED: {adults} Adults, {students} Students, {kids} Kids for {monument_name}. Total: {total_price} EGP."
    return "❌ Insufficient Funds"

def ui_issue_visa():
    """Issue visa with digital stamp and PDF generation"""
    global current_user
    if not current_user: return "Login First", None, None
    
    nationality = current_user[4]
    
    if not VisaPolicy.check_eligibility(nationality):
        return "❌ VISA ON ARRIVAL NOT AVAILABLE. Please visit nearest Consulate.", None, None
    
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
    """Purchase eSIM connectivity plan"""
    global current_user
    if not current_user: return "Login First"
    price = 500 if "Orange" in plan_name else 400
    if db.purchase(current_user[0], plan_name, price, "CONNECTIVITY"):
        return f"✅ Activated: {plan_name}. QR sent to email."
    return "❌ Insufficient Funds"

def ui_buy_souvenir(item_name):
    """Purchase souvenir item"""
    global current_user
    if not current_user: return "Login First"
    price = 250
    if db.purchase(current_user[0], item_name, price, "SOUVENIR"):
        return f"✅ Purchased: {item_name}. Pickup at Airport Zone B."
    return "❌ Insufficient Funds"

def ui_claim_offer(offer_name):
    """Claim exclusive offer voucher"""
    global current_user
    if not current_user: return "Login First"
    return f"✅ VOUCHER CLAIMED: {offer_name}. Saved to Wallet."

def ui_claim_welcome_gift():
    """Claim the welcome gift - Procedure Doc 1030 compliance"""
    global current_user
    if not current_user: return "❌ Login required"
    
    if db.claim_gift(current_user[0]):
        return "✅ Gift QR Generated! Pick up at Airport Zone A."
    else:
        return "❌ Gift already claimed or unavailable."

def ui_demo_login():
    """Demo login with auto-activation and deep data"""
    global current_user
    name = "Diplomat-DEMO-001"
    full_name = "Demo User"
    # Fix Demo Nationality: Force to "USA" for Visa functionality
    uid = db.register_traveler(name, full_name, "D999999", "USA", "Foreign", "2030-01-01", "BIO-DEMO-KEY", "Diplomat", "Official Visit", "Cairo Marriott Hotel")
    
    # Activate wallet for demo user
    db.activate_wallet(uid, "DEMO-CARD-1234-5678-9012")
    
    # Top up with demo funds
    db.top_up(uid, 50000) 
    
    current_user = db.get_traveler(uid)
    return (
        f"✅ DEMO MODE ACTIVATED: {name}",
        gr.Group(visible=True),
        gr.Group(visible=False),
        f"EGP {current_user[8]}",
        f"🌿 {current_user[11]}",
        "✅ ACCOUNT ACTIVE - All features available",
        gr.update(value="PAY:CAIRO_METRO:50:EGP"),  # Auto-fill QR input
        gr.update(visible=True)  # Show demo badge
    )

# ==============================================================================
# 🎨 GRADIO INTERFACE - ENHANCED QR SCANNER & LOGO
# ==============================================================================

css = """
body { background-color: #F5F5DC; }
.gradio-container { font-family: sans-serif; }
button.primary { background-color: #D4AF37 !important; color: white !important; font-weight: bold; }
button.secondary { background-color: #2F4F4F !important; color: white !important; }
.logo-container { text-align: center; margin-bottom: 20px; }
.system-status { background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
"""

# Initialize database instance
db = HorusDB()

# Generate README on startup
ReadmeGenerator.generate_readme()

with gr.Blocks(css=css, title="Horus Key Platinum v10.2") as demo:
    # LOGO EMBEDDING
    gr.Markdown("<div style='text-align: center;'><img src='file/horus_logo.png' alt='Horus Logo' width='180'/></div>")
    gr.Markdown(f"# 👁️ {HorusConfig.APP_NAME}")
    
    # SYSTEM STATUS DISPLAY
    system_status = HorusConfig.get_system_status()
    status_text = f"""
    <div class='system-status'>
        <strong>🔧 System Status:</strong> 
        Platform: {system_status['platform']} | 
        QR Scanner: {'✅' if system_status['qr_scanner'] else '❌'} | 
        Camera: {'✅' if system_status['camera'] else '❌'} | 
        AI Chat: {'✅' if system_status['ai'] else '❌'}
    </div>
    """
    gr.HTML(status_text)
    
    # DEMO MODE BADGE
    with gr.Row():
        demo_badge = gr.Markdown("", visible=False)  # Hidden by default
    
    # STATUS BAR
    with gr.Row():
        status = gr.Textbox(label="Identity Status", value="Awaiting Biometrics")
        bal = gr.Textbox(label="Wallet Balance", value="---")
        score = gr.Textbox(label="Green Score", value="---")
        activation_status = gr.Textbox(label="Account Status", value="---")
        
    # ENTRY GATE - DEEP DATA UPGRADE
    with gr.Row():
        cam = gr.Image(sources=["webcam"], label="Biometric Scanner", type="numpy")
        with gr.Column():
            passport = gr.Textbox(label="Passport Number", value="A1234567")
            full_name = gr.Textbox(label="Full Name (as in Passport)", value="John Doe")
            passport_expiry = gr.Textbox(label="Passport Expiry (YYYY-MM-DD)", value="2028-12-31")
            nat = gr.Dropdown(["USA", "Egypt", "UK", "Germany", "Japan"], label="Nationality", value="USA")
            
            # DEEP DATA FIELDS (Procedure Doc 1030)
            gr.Markdown("**📋 Arrival Card Information**")
            occupation = gr.Textbox(label="Occupation", placeholder="e.g. Engineer, Doctor, Student")
            purpose_of_travel = gr.Dropdown(["Tourism", "Business", "Official Visit", "Study", "Medical", "Transit"], label="Purpose of Travel", value="Tourism")
            accommodation_address = gr.Textbox(label="Accommodation Address", placeholder="e.g. Cairo Marriott Hotel, Zamalek")
            
            with gr.Row():
                btn = gr.Button("SCAN FACE & ENTER ECOSYSTEM", variant="primary")
                btn_demo = gr.Button("🔑 DEMO ACCESS (Bypass Bio)", variant="secondary")

    # ACTIVATION PANEL
    with gr.Group(visible=False) as activation_panel:
        gr.Markdown("# 🔒 ACCOUNT ACTIVATION REQUIRED")
        gr.Markdown("### Deposit $200 USD to unlock all HORUS features")
        with gr.Row():
            card_input = gr.Textbox(label="Credit Card Number", placeholder="1234-5678-9012-3456", type="password")
            btn_activate = gr.Button("DEPOSIT $200 & ACTIVATE", variant="primary")
        activation_msg = gr.Textbox(label="Activation Status", interactive=False)
        btn_activate.click(ui_activate_wallet, inputs=[card_input], outputs=[activation_msg, gr.Group(visible=True), activation_panel])

    # MAIN APP GROUP
    with gr.Group(visible=False) as app:
        with gr.Tabs():
            # 1. VISA
            with gr.TabItem("🛂 Visa & Identity"):
                gr.Markdown("### 4.B Visa upon Arrival & 4.I Digital Access")
                btn_visa = gr.Button(f"Pay {HorusConfig.PRICING['visa_fee']} EGP & Issue Visa")
                with gr.Row():
                    out_v = gr.Textbox(label="Status")
                    img_v = gr.Image(label="Digital QR Stamp")
                    file_v = gr.File(label="Download E-Visa PDF")
                btn_visa.click(ui_issue_visa, outputs=[out_v, img_v, file_v])
                
            # 2. TRANSPORT (REAL EGYPT MODE)
            with gr.TabItem("🚕 Mobility"):
                gr.Markdown("### 4.D Booking & 4.E Eco-Travel")
                mode = gr.Dropdown([
                    "Cairo Monorail", "LRT (Electric Train)", "Electric Bus",
                    "Metro Line 1", "Metro Line 2", "Metro Line 3",
                    "Gas-Powered Taxi", "Private Car", "Online Ride-Hailing",
                    "Shared Shuttle", "Train", "Airport Transfer"
                ], label="Mode")
                dest = gr.Textbox(label="Destination", placeholder="e.g. Pyramids")
                btn_tr = gr.Button("Book Ride")
                out_tr = gr.Textbox(label="Receipt")
                btn_tr.click(ui_book_transport, inputs=[mode, dest], outputs=[out_tr])
            
            # 3. MONUMENTS (FAMILY MODE)
            with gr.TabItem("🏛️ Monuments"):
                gr.Markdown("### 4.F Heritage Tickets - Family Mode")
                with gr.Row():
                    monument_name = gr.Dropdown([
                        "Great Pyramid", "Karnak Temple", "GEM Museum", 
                        "Valley of Kings", "Abu Simbel"
                    ], label="Select Monument")
                    btn_info = gr.Button("📍 View Info")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Family Tickets**")
                        adults = gr.Number(minimum=0, value=1, label="Adults", precision=0)
                        students = gr.Number(minimum=0, value=0, label="Students", precision=0)
                        kids = gr.Number(minimum=0, value=0, label="Kids", precision=0)
                        btn_mon = gr.Button("Purchase Family Tickets", variant="primary")
                    with gr.Column():
                        monument_info = gr.Textbox(label="Monument Information", lines=4, interactive=False)
                        out_mon = gr.Textbox(label="Ticket Status")
                btn_mon.click(ui_book_monument_family, inputs=[monument_name, adults, students, kids], outputs=[out_mon])
                btn_info.click(ui_get_monument_info, inputs=[monument_name], outputs=[monument_info])

            # 4. WALLET & BANKING
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

            # 5. SCAN & PAY - ENHANCED QR SCANNER
            with gr.TabItem("📷 Scan & Pay"):
                gr.Markdown("### The Reverse QR - Enhanced Camera Scanning")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**📷 Camera QR Scanner**")
                        qr_cam = gr.Image(sources=["webcam"], type="pil", label="Scan QR Code")
                        btn_scan_cam = gr.Button("📷 SCAN QR FROM CAMERA", variant="primary")
                        scan_cam_result = gr.Textbox(label="Camera Scan Result", lines=4, interactive=False)
                        
                        gr.Markdown("**⌨️ Manual QR Entry**")
                        qr_input = gr.Textbox(
                            label="QR Code Data", 
                            placeholder="PAY:VENDOR_ID:AMOUNT:CURRENCY\nExample: PAY:CAIRO_METRO:50:EGP",
                            lines=3
                        )
                        btn_scan = gr.Button("📋 PROCESS MANUAL QR", variant="secondary")
                        scan_result = gr.Textbox(label="Manual Scan Result", lines=4, interactive=False)
                        
                        # Wire camera scanner to QRDecoder logic
                        btn_scan_cam.click(ui_scan_qr_from_camera, inputs=[qr_cam], outputs=[scan_cam_result])
                        btn_scan.click(ui_scan_qr, inputs=[qr_input], outputs=[scan_result])
                        
                        # Demo simulation button
                        btn_simulate = gr.Button("🟢 SIMULATE METRO SCAN", variant="secondary")
                        btn_simulate.click(ui_simulate_metro_scan, outputs=[scan_result])
                    
                    with gr.Column():
                        gr.Markdown("**Quick Examples**")
                        gr.Markdown("""
                        **Common QR Formats:**
                        - `PAY:CAIRO_METRO:50:EGP`
                        - `PAY:STARBUCKS_ZAMALEK:150:EGP`
                        - `PAY:UBER_RIDE:85:EGP`
                        - `PAY:PARKING_FEE:25:EGP`
                        """)
                        
                        balance_display = gr.Textbox(label="Wallet Balance", interactive=False)
                        refresh_balance_btn = gr.Button("🔄 Refresh Balance")
                        refresh_balance_btn.click(
                            lambda: f"EGP {current_user[8] if current_user else '0'}", 
                            outputs=[balance_display]
                        )

            # 6. MARKETPLACE
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

            # 7. OFFERS - WELCOME GIFT UPGRADE
            with gr.TabItem("🎁 Offers"):
                gr.Markdown("### 4.G Exclusive Deals & Welcome Gifts")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Exclusive Offers**")
                        offers = [f"{o[0]} - {o[1]}" for o in MarketplaceEngine.get_exclusive_offers()]
                        dd_offer = gr.Dropdown(offers, label="Select Offer")
                        btn_offer = gr.Button("Claim Voucher")
                        out_offer = gr.Textbox()
                        btn_offer.click(ui_claim_offer, inputs=[dd_offer], outputs=[out_offer])
                    
                    with gr.Column():
                        gr.Markdown("**🎁 WELCOME GIFT**")
                        gr.Markdown("*Special gift for new travelers*")
                        btn_gift = gr.Button("🎁 CLAIM FREE EGYPT GIFT", variant="primary")
                        out_gift = gr.Textbox(label="Gift Status", interactive=False)
                        btn_gift.click(ui_claim_welcome_gift, outputs=[out_gift])
                
            # 8. AI
            with gr.TabItem("🤖 Horus AI"):
                gr.Markdown(f"Powered by **{HorusConfig.AI_MODEL}**")
                if HorusConfig.AI_ENABLED:
                    gr.ChatInterface(fn=ask_ai, type="messages")
                else:
                    gr.Markdown("⚠️ AI Chat is not available. Please install google-generativeai package.")
                
            # 9. ADMIN
            with gr.TabItem("⚙️ Admin"):
                gr.Markdown("### System Sync (Force Push)")
                btn_s = gr.Button("Sync Code & Docs to GitHub", variant="stop")
                out_s = gr.TextArea(label="Diagnostic Logs")
                btn_s.click(GitAutopilot.sync_codebase, outputs=[out_s])
                
                gr.Markdown("### System Statistics")
                stats_display = gr.Textbox(label="System Stats", interactive=False, lines=5)
                refresh_stats_btn = gr.Button("🔄 Refresh Stats")
                refresh_stats_btn.click(
                    lambda: json.dumps(db.get_system_stats(), indent=2),
                    outputs=[stats_display]
                )

    # Event Wiring - DEEP DATA UPGRADE
    btn.click(ui_login, inputs=[cam, passport, nat, full_name, passport_expiry, occupation, purpose_of_travel, accommodation_address], outputs=[status, app, activation_panel, bal, score, activation_status])
    btn_demo.click(ui_demo_login, outputs=[status, app, activation_panel, bal, score, activation_status, qr_input, demo_badge])

# ==============================================================================
# 🚀 LAUNCH
# ==============================================================================

if __name__ == "__main__":
    # Final dependency check and installation
    logger.info("🚀 Starting HORUS v10.2 with self-healing architecture...")
    
    # Install dependencies one last time before launch
    if not install_dependencies():
        logger.error("❌ CRITICAL: Final dependency installation failed. Some features may not work.")
    
    # Display system status
    system_status = HorusConfig.get_system_status()
    logger.info(f"📊 System Status: {system_status}")
    
    # Launch the application
    logger.info("🌟 Launching HORUS application...")
    demo.queue().launch(share=True)
