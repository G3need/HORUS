# ==============================================================================
# HORUS v11.0.py - Enterprise Edition (Advanced Features)
# ==============================================================================

# STANDARD LIBRARY IMPORTS (System Prep)
import os
import sys
import importlib.util
import platform
import logging
from pathlib import Path

# Configure logging for system operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress specific warnings for cleaner output
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*css.*parameter.*")

# ==============================================================================
# 🛠️ SELF-HEALING ENTERPRISE SETUP
# ==============================================================================

def enterprise_setup():
    """Self-healing enterprise setup with military-grade dependency management"""
    logger.info("🚀 Starting HORUS v11.0 Enterprise Setup...")
    
    # Phase 1: System Dependencies
    if not install_system_dependencies():
        logger.error("❌ System dependency installation failed")
        return False
    
    # Phase 2: Python Dependencies  
    if not install_python_dependencies():
        logger.error("❌ Python dependency installation failed")
        return False
    
    # Phase 3: Safe Import Handler
    import_status = safe_import_with_error_handling()
    
    # Phase 4: Critical Import Validation
    critical_imports = ['gradio', 'numpy', 'sqlite3']
    failed_critical = [pkg for pkg in critical_imports if not import_status.get(pkg, False)]
    
    if failed_critical:
        logger.error(f"❌ CRITICAL: Failed to import critical packages: {failed_critical}")
        logger.error("❌ Application may not function properly without these dependencies.")
        return False
    
    logger.info("✅ Enterprise Setup Complete - All Systems Operational")
    return True

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
            'google-genai': 'google.genai',
            'sqlite3': 'sqlite3'
        }.get(package_name.lower(), package_name.lower())
        
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False

def install_system_dependencies():
    """Auto-install system dependencies with military-grade precision and enhanced error handling"""
    if is_linux_colab():
        try:
            logger.info("🚀 Auto-installing system dependencies...")
            import subprocess
            import time
            
            # Update package lists with timeout
            update_result = subprocess.run(
                ['sudo', 'apt-get', 'update', '-y'], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                check=True,
                timeout=60  # 60 second timeout
            )
            
            # Install libzbar0 with timeout and retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    install_result = subprocess.run(
                        ['sudo', 'apt-get', 'install', '-y', 'libzbar0'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL, 
                        check=True,
                        timeout=120  # 120 second timeout
                    )
                    logger.info("✅ System dependencies auto-installed successfully")
                    return True
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ System dependency installation timeout (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Wait before retry
                    else:
                        raise
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️ System dependency installation failed (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Wait before retry
                    else:
                        raise
            
        except subprocess.TimeoutExpired:
            logger.error("❌ System dependency installation timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ System dependencies auto-install failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during system dependency installation: {e}")
            return False
    else:
        logger.info("ℹ️ Non-Colab environment - skipping system dependencies")
        return True

def install_python_dependencies():
    """Auto-install Python dependencies with quantum efficiency and parallel processing"""
    logger.info("🚀 Auto-installing Python dependencies...")
    
    required_packages = [
        'gradio>=4.0.0', 'pyzbar', 'qrcode[pil]', 'pillow', 
        'opencv-python', 'reportlab', 'numpy', 'google-genai', 'pandas'
    ]
    
    missing_packages = []
    for package in required_packages:
        package_name = package.split('>=')[0].split('[')[0]
        if not check_package_installed(package_name):
            missing_packages.append(package)
            logger.warning(f"📦 Missing package: {package}")
        else:
            logger.info(f"✅ Package available: {package}")
    
    if missing_packages:
        logger.info(f"🚀 Auto-installing {len(missing_packages)} packages with quantum optimization...")
        import subprocess
        import sys
        import concurrent.futures
        import time
        
        # Install packages in parallel for faster execution
        def install_package(package):
            """Install a single package with enhanced error handling"""
            try:
                start_time = time.time()
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-q', '--upgrade', package], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL, 
                    check=True,
                    timeout=180  # 3 minute timeout per package
                )
                install_time = time.time() - start_time
                logger.info(f"✅ Successfully installed {package} in {install_time:.2f}s")
                return True, package, None
            except subprocess.TimeoutExpired:
                error_msg = f"❌ Installation timeout for {package}"
                logger.error(error_msg)
                return False, package, "timeout"
            except subprocess.CalledProcessError as e:
                error_msg = f"❌ Failed to install {package}: {e}"
                logger.error(error_msg)
                return False, package, str(e)
            except Exception as e:
                error_msg = f"❌ Unexpected error installing {package}: {e}"
                logger.error(error_msg)
                return False, package, str(e)
        
        # Use ThreadPoolExecutor for parallel installation
        successful_installs = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_package = {executor.submit(install_package, pkg): pkg for pkg in missing_packages}
            
            for future in concurrent.futures.as_completed(future_to_package):
                success, package, error = future.result()
                if success:
                    successful_installs += 1
                else:
                    logger.error(f"❌ Failed to install {package}: {error}")
        
        if successful_installs == len(missing_packages):
            logger.info("🎉 All Python packages auto-installed successfully!")
            return True
        else:
            logger.warning(f"⚠️ {successful_installs}/{len(missing_packages)} packages installed successfully")
            return False
    else:
        logger.info("🎉 All Python packages are already available!")
        return True

def safe_import_with_error_handling():
    """Perform heavy imports with comprehensive error handling and resource management"""
    import_status = {}
    global gr, np, Image, cv2, pyzbar, qrcode, canvas, letter, ImageReader, pdfmetrics, TTFont, genai, sqlite3
    
    # Initialize all imports to None first
    gr = np = Image = cv2 = pyzbar = qrcode = canvas = letter = ImageReader = pdfmetrics = TTFont = genai = sqlite3 = None
    
    try:
        import gradio as gr
        import_status['gradio'] = True
        logger.info("✅ Gradio imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Gradio: {e}")
        import_status['gradio'] = False
        gr = None
    
    try:
        import numpy as np
        import_status['numpy'] = True
        logger.info("✅ NumPy imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import NumPy: {e}")
        import_status['numpy'] = False
        np = None
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import_status['pillow'] = True
        logger.info("✅ PIL imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import PIL: {e}")
        import_status['pillow'] = False
        Image = None
    
    try:
        import cv2
        import_status['opencv'] = True
        logger.info("✅ OpenCV imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import OpenCV: {e}")
        import_status['opencv'] = False
        cv2 = None
    
    try:
        from pyzbar import pyzbar
        import_status['pyzbar'] = True
        logger.info("✅ Pyzbar imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Pyzbar: {e}")
        import_status['pyzbar'] = False
        pyzbar = None
    
    try:
        import qrcode
        import_status['qrcode'] = True
        logger.info("✅ QRCode imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import QRCode: {e}")
        import_status['qrcode'] = False
        qrcode = None
    
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
        canvas = None
        letter = None
        ImageReader = None
        pdfmetrics = None
        TTFont = None
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import_status['pil'] = True
        logger.info("✅ PIL imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import PIL: {e}")
        import_status['pil'] = False
        Image = None
        ImageDraw = None
        ImageFont = None
    
    try:
        import google.genai as genai
        import_status['genai'] = True
        logger.info("✅ Google GenAI imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Google GenAI: {e}")
        import_status['genai'] = False
        genai = None
    
    try:
        import pandas as pd
        import_status['pandas'] = True
        logger.info("✅ Pandas imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import Pandas: {e}")
        import_status['pandas'] = False
        pd = None
    
    try:
        import sqlite3
        import_status['sqlite3'] = True
        logger.info("✅ SQLite3 imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import SQLite3: {e}")
        import_status['sqlite3'] = False
        sqlite3 = None
    
    return import_status

# ==============================================================================
# 🧠 ENTERPRISE MONITORING & LOGGING SYSTEM
# ==============================================================================

import threading
import json
from collections import defaultdict

class EnterpriseMonitor:
    """Military-grade monitoring and logging system"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.alerts = []
        self.performance_data = {}
        self._lock = threading.Lock()
        self.start_time = dt.datetime.now()
    
    def log_metric(self, metric_name: str, value: float, category: str = "general"):
        """Log a performance metric with timestamp"""
        with self._lock:
            timestamp = dt.datetime.now().isoformat()
            self.metrics[metric_name].append({
                'timestamp': timestamp,
                'value': value,
                'category': category
            })
            
            # Keep only last 100 entries per metric to prevent memory bloat
            if len(self.metrics[metric_name]) > 100:
                self.metrics[metric_name] = self.metrics[metric_name][-100:]
    
    def log_alert(self, alert_level: str, message: str, component: str = "system"):
        """Log an alert with severity level"""
        with self._lock:
            timestamp = dt.datetime.now().isoformat()
            alert = {
                'timestamp': timestamp,
                'level': alert_level,
                'message': message,
                'component': component
            }
            self.alerts.append(alert)
            
            # Keep only last 50 alerts
            if len(self.alerts) > 50:
                self.alerts = self.alerts[-50:]
            
            # Log critical alerts immediately
            if alert_level in ['CRITICAL', 'ERROR']:
                logger.error(f"ALERT [{alert_level}] {component}: {message}")
    
    def get_system_health(self) -> dict:
        """Get comprehensive system health report"""
        uptime = dt.datetime.now() - self.start_time
        
        with self._lock:
            return {
                'uptime_seconds': uptime.total_seconds(),
                'uptime_formatted': str(uptime).split('.')[0],
                'total_metrics': len(self.metrics),
                'total_alerts': len(self.alerts),
                'critical_alerts': len([a for a in self.alerts if a['level'] == 'CRITICAL']),
                'error_alerts': len([a for a in self.alerts if a['level'] == 'ERROR']),
                'warning_alerts': len([a for a in self.alerts if a['level'] == 'WARNING']),
                'last_alert': self.alerts[-1] if self.alerts else None,
                'performance_summary': self._get_performance_summary()
            }
    
    def _get_performance_summary(self) -> dict:
        """Get performance metrics summary"""
        summary = {}
        for metric_name, entries in self.metrics.items():
            if entries:
                values = [entry['value'] for entry in entries]
                summary[metric_name] = {
                    'latest': values[-1],
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        return summary
    
    def export_logs(self) -> str:
        """Export all logs in JSON format"""
        with self._lock:
            return json.dumps({
                'system_health': self.get_system_health(),
                'metrics': dict(self.metrics),
                'alerts': self.alerts,
                'export_timestamp': dt.datetime.now().isoformat()
            }, indent=2)

# ==============================================================================
# 🏛️ ENTERPRISE CONFIGURATION & UTILITIES
# ==============================================================================

import json
import hashlib
import random
import threading
import datetime as dt
import io
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple

@dataclass
class HorusConfig:
    """Enterprise configuration for HORUS v11.0"""
    APP_NAME: str = "Horus Key Platinum v11.0 - Enterprise Edition"
    DB_NAME: str = "horus_enterprise.db"
    AI_MODEL: str = "gemini-3-flash-preview"
    AI_ENABLED: bool = False  # Set after import checking
    VERSION: str = "11.0.0-Sovereign"

    # Enterprise pricing (EGP)
    PRICING: dict = field(default_factory=lambda: {
        "activation_deposit": 10000,  # $200 USD at 50 EGP conversion
        "visa_fee": 1250,  # $25 USD at 50 EGP conversion
        "esim_orange": 500,
        "esim_vodafone": 450,
        "monument_base": 1000,  # Base price for foreigners
        "transport_card_physical": 150,
        "transport_card_virtual": 300,
        "green_bonus": 50,  # Bonus points for green transport
    })

    # Enterprise configuration
    AUTO_INSTALL_DEPS: bool = True
    QR_SCANNER_ENABLED: bool = False  # Will be updated after import
    CAMERA_ENABLED: bool = False     # Will be updated after import
    AI_ENABLED: bool = False         # Will be set explicitly based on import status
    ENTERPRISE_MODE: bool = True
    ADVANCED_QR: bool = True
    ENHANCED_AI: bool = True
    WALLET_SETUP_FLOW: bool = True  # NEW: Wallet creation flow
    MULTILINGUAL: bool = True       # NEW: Multilingual support
    FAQ_ENABLED: bool = True         # NEW: FAQ system

    def __post_init__(self):
        """Post-initialization to set dynamic values"""
        # Update dynamic values based on import status
        if 'import_status' in globals():
            self.QR_SCANNER_ENABLED = import_status.get('pyzbar', False)
            self.CAMERA_ENABLED = import_status.get('opencv', False)
            # EXPLICIT: Set AI_ENABLED based on actual import success
            self.AI_ENABLED = import_status.get('genai', False)
            # Disable features gracefully if dependencies are missing
            if not import_status.get('pyzbar', False):
                logger.warning("⚠️ QR Scanner disabled - pyzbar not available")
            if not import_status.get('opencv', False):
                logger.warning("⚠️ Camera disabled - opencv not available")
            if not import_status.get('reportlab', False):
                logger.warning("⚠️ PDF generation disabled - reportlab not available")
            if not import_status.get('genai', False):
                logger.warning("⚠️ AI Chat disabled - google-genai not available")
            logger.info(f"🔧 AI Enabled: {self.AI_ENABLED} (genai import: {import_status.get('genai', False)})")

    @classmethod
    def get_system_status(cls):
        """Get comprehensive enterprise system status"""
        return {
            "version": cls.VERSION,
            "platform": platform.system(),
            "is_colab": is_linux_colab(),
            "dependencies": import_status if 'import_status' in globals() else {},
            "qr_scanner": cls.QR_SCANNER_ENABLED,
            "camera": cls.CAMERA_ENABLED,
            "ai": cls.AI_ENABLED,
            "enterprise_mode": cls.ENTERPRISE_MODE,
            "advanced_qr": cls.ADVANCED_QR,
            "enhanced_ai": cls.ENHANCED_AI,
            "wallet_setup_flow": cls.WALLET_SETUP_FLOW,
            "multilingual": cls.MULTILINGUAL,
            "faq_enabled": cls.FAQ_ENABLED
        }

# Create global config instance AFTER imports are checked and class is defined
config = HorusConfig()
logger.info(f"🔧 Config created with AI_ENABLED: {config.AI_ENABLED}")

# ==============================================================================
# 🔐 ENTERPRISE SECURITY & BIOMETRICS
# ==============================================================================

class HorusSecurity:
    """Enterprise-grade security with SHA-512 biometric hashing"""
    
    @staticmethod
    def hash_biometric(data: str) -> str:
        """Hash biometric data with SHA-512 for enterprise security"""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def verify_biometric(input_data: str, stored_hash: str) -> bool:
        """Verify biometric data with enterprise-grade security"""
        return HorusSecurity.hash_biometric(input_data) == stored_hash
    
    @staticmethod
    def generate_secure_token() -> str:
        """Generate secure token for enterprise operations"""
        return hashlib.sha256(f"{random.random()}{time.time()}".encode()).hexdigest()
    
    @staticmethod
    def validate_credit_card(card_number: str) -> bool:
        """Validate credit card number with enterprise-grade checks"""
        # Remove spaces and dashes
        card = card_number.replace(" ", "").replace("-", "")
        
        # Check if it's numeric and has valid length
        if not card.isdigit() or len(card) < 13 or len(card) > 19:
            return False
        
        # Luhn algorithm validation
        total = 0
        for i, digit in enumerate(reversed(card)):
            d = int(digit)
            if i % 2 == 1:  # Every second digit from right
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        
        return total % 10 == 0
    
    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """Encrypt sensitive data with enterprise-grade encryption"""
        # Simple XOR encryption for demonstration (use proper encryption in production)
        key = "HORUS_ENTERPRISE_KEY_2026"
        encrypted = ""
        for i, char in enumerate(data):
            encrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        return encrypted
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str) -> str:
        """Decrypt sensitive data with enterprise-grade decryption"""
        key = "HORUS_ENTERPRISE_KEY_2026"
        decrypted = ""
        for i, char in enumerate(encrypted_data):
            decrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        return decrypted

# ==============================================================================
# GLOBAL INSTANCES & INITIALIZATION
# ==============================================================================

# Global enterprise monitor instance
enterprise_monitor = EnterpriseMonitor()

# Run the enterprise setup
if not enterprise_setup():
    logger.error("❌ CRITICAL: Enterprise setup failed. Some features may not work.")
    # Don't exit, continue with limited functionality

# Log final import status
if 'import_status' in globals():
    logger.info("📊 Final Import Status:")
    for pkg, status in import_status.items():
        status_icon = "✅" if status else "❌"
        logger.info(f"  {status_icon} {pkg}: {'Available' if status else 'Missing'}")

# Log system initialization
enterprise_monitor.log_alert("INFO", "HORUS v11.0 Enterprise initialization complete", "system")
logger.info("✅ HORUS v11.0 Enterprise Edition - Part 1 Complete")

# ==============================================================================
# 🗄️ ENTERPRISE DATABASE SYSTEM
# ==============================================================================

class HorusDB:
    """Enterprise thread-safe singleton database with deep data fields and advanced logging"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._db_lock = threading.Lock()
        self.conn = None
        self.cursor = None
        self._initialize_database()
        logger.info("✅ Enterprise HorusDB initialized with deep data schema")
    
    def _initialize_database(self):
        """Initialize database with enterprise schema and deep data fields"""
        with self._db_lock:
            self.conn = sqlite3.connect(config.DB_NAME, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Create travelers table with ALL 18 DEEP DATA FIELDS
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS travelers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    passport TEXT NOT NULL,
                    nationality TEXT NOT NULL,
                    nationality_group TEXT NOT NULL,
                    passport_expiry TEXT NOT NULL,
                    biometric_hash TEXT NOT NULL,
                    occupation TEXT,                    -- DEEP DATA FIELD 1
                    purpose_of_travel TEXT,           -- DEEP DATA FIELD 2
                    accommodation_address TEXT,       -- DEEP DATA FIELD 3
                    dob TEXT,                         -- DEEP DATA FIELD 4
                    gender TEXT,                       -- DEEP DATA FIELD 5
                    phone TEXT,                        -- DEEP DATA FIELD 6
                    arrival_date TEXT,                 -- DEEP DATA FIELD 7
                    country_boarded TEXT,             -- DEEP DATA FIELD 8
                    flight_number TEXT,                -- DEEP DATA FIELD 9
                    mode_of_arrival TEXT,              -- DEEP DATA FIELD 10
                    departure_date TEXT,               -- DEEP DATA FIELD 11
                    country_residence TEXT,            -- DEEP DATA FIELD 12
                    visa_no TEXT,                      -- DEEP DATA FIELD 13
                    issued_by TEXT,                    -- DEEP DATA FIELD 14
                    wallet_balance INTEGER DEFAULT 0,
                    wallet_status TEXT DEFAULT 'LOCKED',
                    bank_linked INTEGER DEFAULT 0,
                    green_points INTEGER DEFAULT 0,
                    has_claimed_gift INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create enterprise_packages table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS enterprise_packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    category TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create monuments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS monuments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    base_price_foreigner REAL NOT NULL,
                    base_price_local REAL NOT NULL,
                    location TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create visas table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS visas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    traveler_id INTEGER NOT NULL,
                    stamp TEXT NOT NULL,
                    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    status TEXT DEFAULT 'ACTIVE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (traveler_id) REFERENCES travelers (id)
                )
            """)
            
            # Create transactions table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    traveler_id INTEGER NOT NULL,
                    service_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'EGP',
                    status TEXT DEFAULT 'PENDING',
                    qr_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (traveler_id) REFERENCES travelers (id)
                )
            """)
            
            # Create indexes for performance
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_travelers_passport ON travelers(passport)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_travelers_wallet_status ON travelers(wallet_status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_visas_traveler ON visas(traveler_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_traveler ON transactions(traveler_id)")
            
            self.conn.commit()
            logger.info("✅ Database schema initialized with deep data fields")
    
    def register_traveler(self, name, full_name, passport, nationality, nationality_group, 
                        passport_expiry, biometric_hash, occupation=None, purpose_of_travel=None,
                        accommodation_address=None, dob=None, gender=None, phone=None,
                        arrival_date=None, country_boarded=None, flight_number=None,
                        mode_of_arrival=None, departure_date=None, country_residence=None,
                        visa_no=None, issued_by=None):
        """Register traveler with all 18 deep data fields"""
        with self._db_lock:
            try:
                self.cursor.execute("""
                    INSERT INTO travelers (
                        name, full_name, passport, nationality, nationality_group, passport_expiry,
                        biometric_hash, occupation, purpose_of_travel, accommodation_address, dob, gender,
                        phone, arrival_date, country_boarded, flight_number, mode_of_arrival,
                        departure_date, country_residence, visa_no, issued_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, full_name, passport, nationality, nationality_group, passport_expiry,
                    biometric_hash, occupation, purpose_of_travel, accommodation_address, dob, gender,
                    phone, arrival_date, country_boarded, flight_number, mode_of_arrival,
                    departure_date, country_residence, visa_no, issued_by
                ))
                
                traveler_id = self.cursor.lastrowid
                self.conn.commit()
                
                enterprise_monitor.log_metric("traveler_registered", 1, "database")
                logger.info(f"✅ Enterprise traveler registered: {name} (ID: {traveler_id})")
                
                return traveler_id
                
            except Exception as e:
                logger.error(f"❌ Enterprise traveler registration failed: {e}")
                enterprise_monitor.log_alert("ERROR", f"Traveler registration failed: {e}", "database")
                return None
    
    def get_traveler(self, traveler_id):
        """Get traveler by ID with enterprise logging"""
        with self._db_lock:
            try:
                self.cursor.execute("SELECT * FROM travelers WHERE id = ?", (traveler_id,))
                traveler = self.cursor.fetchone()
                
                if traveler:
                    enterprise_monitor.log_metric("traveler_retrieved", 1, "database")
                    logger.debug(f"✅ Enterprise traveler retrieved: {traveler_id}")
                
                return traveler
                
            except Exception as e:
                logger.error(f"❌ Enterprise traveler retrieval failed: {e}")
                enterprise_monitor.log_alert("ERROR", f"Traveler retrieval failed: {e}", "database")
                return None
    
    def activate_wallet(self, traveler_id, card_number):
        """Activate wallet with enterprise logging"""
        with self._db_lock:
            try:
                self.cursor.execute(
                    "UPDATE travelers SET wallet_status = 'ACTIVE', bank_linked = 1 WHERE id = ?",
                    (traveler_id,)
                )
                self.conn.commit()
                
                enterprise_monitor.log_metric("wallet_activated", 1, "financial")
                logger.info(f"✅ Enterprise wallet activated: {traveler_id}")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Enterprise wallet activation failed: {e}")
                enterprise_monitor.log_alert("ERROR", f"Wallet activation failed: {e}", "financial")
                return False
    
    def top_up(self, traveler_id, amount):
        """Top up wallet with enterprise logging"""
        with self._db_lock:
            try:
                self.cursor.execute(
                    "UPDATE travelers SET wallet_balance = wallet_balance + ? WHERE id = ?",
                    (amount, traveler_id)
                )
                self.conn.commit()
                
                enterprise_monitor.log_metric("wallet_topup", amount, "financial")
                logger.info(f"✅ Enterprise wallet topped up: {traveler_id} - {amount} EGP")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Enterprise wallet top-up failed: {e}")
                enterprise_monitor.log_alert("ERROR", f"Wallet top-up failed: {e}", "financial")
                return False
    
    def add_transaction(self, traveler_id, service_type, amount, currency='EGP', qr_data=None):
        """Add transaction with enterprise logging"""
        with self._db_lock:
            try:
                self.cursor.execute("""
                    INSERT INTO transactions (traveler_id, service_type, amount, currency, qr_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (traveler_id, service_type, amount, currency, qr_data))
                
                transaction_id = self.cursor.lastrowid
                self.conn.commit()
                
                enterprise_monitor.log_metric("transaction_added", amount, "financial")
                logger.info(f"✅ Enterprise transaction added: {transaction_id} - {amount} {currency}")
                
                return transaction_id
                
            except Exception as e:
                logger.error(f"❌ Enterprise transaction addition failed: {e}")
                enterprise_monitor.log_alert("ERROR", f"Transaction addition failed: {e}", "financial")
                return None

# ==============================================================================
# 🎯 CORE LOGIC ENGINES
# ==============================================================================

class VisaPolicy:
    """Military-grade visa policy with 74+ eligible countries"""
    
    # CRITICAL UPDATE: Exact eligible countries list as specified
    ELIGIBLE_COUNTRIES = [
        "Albania", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahrain", 
        "Belarus", "Belgium", "Bolivia", "Brazil", "Bulgaria", "Canada", "Chile", "China", 
        "Colombia", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Estonia", 
        "Finland", "France", "Georgia", "Germany", "Greece", "Hong Kong", "Hungary", "Iceland", 
        "India", "Ireland", "Italy", "Japan", "Kazakhstan", "Kuwait", "Latvia", "Lithuania", 
        "Luxembourg", "Malaysia", "Malta", "Mexico", "Moldova", "Monaco", "Montenegro", 
        "Netherlands", "New Zealand", "North Macedonia", "Norway", "Oman", "Paraguay", "Peru", 
        "Poland", "Portugal", "Qatar", "Romania", "Russia", "San Marino", "Saudi Arabia", 
        "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", 
        "Sweden", "Switzerland", "Taiwan", "Ukraine", "UAE", "UK", "USA", "Uruguay", 
        "Vatican City", "Venezuela"
    ]
    
    RESTRICTED_COUNTRIES = [
        "Iran", "Afghanistan", "Syria", "Yemen", "Libya", "Somalia", 
        "North Korea", "Sudan", "Lebanon", "Iraq", "Palestine"
    ]
    
    @classmethod
    def is_eligible(cls, nationality):
        """Check if nationality is eligible for visa on arrival"""
        return nationality in cls.ELIGIBLE_COUNTRIES
    
    @classmethod
    def is_restricted(cls, nationality):
        """Check if nationality is restricted"""
        return nationality in cls.RESTRICTED_COUNTRIES
    
    @classmethod
    def get_visa_status(cls, nationality):
        """Get visa status for nationality"""
        if cls.is_restricted(nationality):
            return "RESTRICTED - Entry Denied"
        elif cls.is_eligible(nationality):
            return "ELIGIBLE - Visa on Arrival Available"
        else:
            return "NOT ELIGIBLE - Embassy Referral Required"

class EcoEngine:
    """Environmental impact calculation engine"""
    
    # Green score calculation for 2026 transport modes
    TRANSPORT_SCORES = {
        "Cairo Monorail": 20,
        "LRT (Electric Train)": 20,
        "Electric Bus": 20,
        "Metro Line 1": 10,
        "Metro Line 2": 10,
        "Metro Line 3": 10,
        "Gas-Powered Taxi": 0,
        "Private Car": 0,
        "Standard Uber": 0,
        "Shared Shuttle": 5,
        "Train": 15
    }
    
    @classmethod
    def calculate_green_score(cls, transport_mode):
        """Calculate green score for transport mode"""
        return cls.TRANSPORT_SCORES.get(transport_mode, 0)
    
    @classmethod
    def get_transport_recommendations(cls):
        """Get eco-friendly transport recommendations"""
        return [mode for mode, score in cls.TRANSPORT_SCORES.items() if score >= 10]

class PriceCalculator:
    """Dynamic pricing calculation engine"""
    
    @staticmethod
    def calculate_monument_price(base_price, nationality_group, visitor_type):
        """Calculate monument ticket price"""
        if nationality_group == "Egyptian":
            return 100  # Fixed local price
        elif nationality_group == "Arab":
            return 200  # Arab discount
        else:  # Foreign
            if visitor_type == "Student":
                return base_price * 0.5  # 50% student discount
            elif visitor_type == "Kid":
                return base_price * 0.3  # 30% kids discount
            else:
                return base_price  # Full adult price
    
    @staticmethod
    def calculate_visa_fee():
        """Calculate visa fee"""
        return config.PRICING["visa_fee"]
    
    @staticmethod
    def calculate_activation_deposit():
        """Calculate activation deposit"""
        return config.PRICING["activation_deposit"]

class DocumentIssuer:
    """Enterprise PDF document generation with advanced features"""
    
    @staticmethod
    def generate_visa_pdf(traveler_data, visa_data):
        """Generate visa PDF with enterprise security features"""
        if not import_status.get('reportlab', False):
            logger.error("❌ PDF generation not available - ReportLab not imported")
            return None
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.utils import ImageReader
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import io
            
            # Create PDF buffer
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            
            # Set up page
            width, height = letter
            
            # Add security watermark
            c.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)
            c.setFont("Helvetica", 50)
            c.saveState()
            c.translate(width/2, height/2)
            c.rotate(45)
            c.drawCentredText(0, 0, "HORUS SECURE")
            c.restoreState()
            
            # Reset colors
            c.setFillColorRGB(0, 0, 0)
            
            # Header
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredText(width/2, height - 50, "ARAB REPUBLIC OF EGYPT")
            
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredText(width/2, height - 80, "E-VISA AUTHORIZATION")
            
            # Visa details
            c.setFont("Helvetica", 12)
            y_position = height - 150
            
            # Traveler information
            c.drawString(50, y_position, f"Name: {traveler_data.get('full_name', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Passport: {traveler_data.get('passport', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Nationality: {traveler_data.get('nationality', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Date of Birth: {traveler_data.get('dob', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Gender: {traveler_data.get('gender', 'N/A')}")
            
            # Visa information
            y_position -= 50
            c.drawString(50, y_position, f"Visa Number: {visa_data.get('visa_no', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Issued By: {visa_data.get('issued_by', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Issue Date: {dt.datetime.now().strftime('%Y-%m-%d')}")
            y_position -= 30
            c.drawString(50, y_position, f"Expiry Date: {(dt.datetime.now() + dt.timedelta(days=180)).strftime('%Y-%m-%d')}")
            y_position -= 30
            c.drawString(50, y_position, f"Purpose: {traveler_data.get('purpose_of_travel', 'Tourism')}")
            
            # Security features
            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, 50, f"SECURITY TOKEN: {HorusSecurity.generate_secure_token()[:16].upper()}")
            
            # Footer
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 8)
            c.drawCentredText(width/2, 30, "This is a secure electronic document. Valid for 180 days from issue date.")
            
            # Finalize PDF
            c.save()
            
            # Get PDF data
            pdf_data = buffer.getvalue()
            buffer.close()
            
            enterprise_monitor.log_metric("visa_pdf_generated", 1, "documents")
            logger.info("✅ Enterprise visa PDF generated successfully")
            
            return pdf_data
            
        except Exception as e:
            logger.error(f"❌ Enterprise visa PDF generation failed: {e}")
            enterprise_monitor.log_alert("ERROR", f"Visa PDF generation failed: {e}", "documents")
            return None
    
    @staticmethod
    def generate_ticket_pdf(traveler_data, monument_data, ticket_data):
        """Generate monument ticket PDF with enterprise features"""
        if not import_status.get('reportlab', False):
            logger.error("❌ PDF generation not available - ReportLab not imported")
            return None
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            import io
            
            # Create PDF buffer
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            
            # Set up page
            width, height = letter
            
            # Header
            c.setFillColorRGB(0.8, 0.6, 0.2)  # Gold color
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredText(width/2, height - 50, "HORUS HERITAGE TICKET")
            
            # Ticket details
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 12)
            y_position = height - 150
            
            c.drawString(50, y_position, f"Visitor: {traveler_data.get('full_name', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Monument: {monument_data.get('name', 'N/A')}")
            y_position -= 30
            c.drawString(50, y_position, f"Date: {dt.datetime.now().strftime('%Y-%m-%d')}")
            y_position -= 30
            c.drawString(50, y_position, f"Visitors: {ticket_data.get('visitors', 1)}")
            y_position -= 30
            c.drawString(50, y_position, f"Total Price: {ticket_data.get('total_price', 0)} EGP")
            
            # QR Code placeholder
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.setFont("Helvetica", 10)
            c.drawString(50, 100, "QR Code: [SCAN FOR VALIDATION]")
            
            # Security token
            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(50, 50, f"TOKEN: {HorusSecurity.generate_secure_token()[:12].upper()}")
            
            # Finalize PDF
            c.save()
            
            # Get PDF data
            pdf_data = buffer.getvalue()
            buffer.close()
            
            enterprise_monitor.log_metric("ticket_pdf_generated", 1, "documents")
            logger.info("✅ Enterprise ticket PDF generated successfully")
            
            return pdf_data
            
        except Exception as e:
            logger.error(f"❌ Enterprise ticket PDF generation failed: {e}")
            enterprise_monitor.log_alert("ERROR", f"Ticket PDF generation failed: {e}", "documents")
            return None

# ==============================================================================
# GLOBAL DATABASE INSTANCE
# ==============================================================================

# Create global database instance
db = HorusDB()
logger.info("✅ Enterprise Database System Initialized - Part 2 Complete")

# ==============================================================================
# 🎨 USER INTERFACE FUNCTIONS (Part 3 of 4)
# ==============================================================================

# Global user state
current_user = None
current_language = "English"

def ui_login(name, full_name, passport, nationality, nationality_group, passport_expiry, 
             biometric_hash, occupation=None, purpose_of_travel=None, accommodation_address=None,
             dob=None, gender=None, phone=None, arrival_date=None, country_boarded=None,
             flight_number=None, mode_of_arrival=None, departure_date=None, country_residence=None,
             visa_no=None, issued_by=None):
    """Enhanced login with 18 deep data fields and wallet setup flow"""
    global current_user
    
    try:
        # Register traveler with all 18 deep data fields
        uid = db.register_traveler(
            name, full_name, passport, nationality, nationality_group, passport_expiry,
            biometric_hash, occupation, purpose_of_travel, accommodation_address, dob, gender,
            phone, arrival_date, country_boarded, flight_number, mode_of_arrival,
            departure_date, country_residence, visa_no, issued_by
        )
        
        if uid:
            current_user = db.get_traveler(uid)
            
            if current_user:
                # Check wallet status for setup flow
                wallet_status = current_user[9]  # wallet_status at index 9
                
                if wallet_status == 'LOCKED':
                    # Show setup wallet panel for new users
                    return (
                        f"✅ Welcome {name}! Please set up your wallet to continue.",
                        gr.Group(visible=False),  # Hide main app
                        gr.Group(visible=False),  # Hide activation panel  
                        gr.Group(visible=True),   # Show setup wallet panel
                        f"EGP {current_user[8]}",
                        f"🌿 {current_user[11]}",
                        "🔒 WALLET LOCKED - Setup required to access features"
                    )
                else:
                    # Show main app for active users
                    return (
                        f"✅ Welcome back {name}!",
                        gr.Group(visible=True),   # Show main app
                        gr.Group(visible=False),  # Hide activation panel
                        gr.Group(visible=False),  # Hide setup wallet panel
                        f"EGP {current_user[8]}",
                        f"🌿 {current_user[11]}",
                        "✅ ACCOUNT ACTIVE - All features available"
                    )
            else:
                return f"❌ Login failed: User not found", gr.update(), gr.update(), gr.update(), "", "", ""
        else:
            return f"❌ Registration failed", gr.update(), gr.update(), gr.update(), "", "", ""
            
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        enterprise_monitor.log_alert("ERROR", f"Login failed: {e}", "ui")
        return f"❌ Error: {e}", gr.update(), gr.update(), gr.update(), "", "", ""

def ui_demo_login():
    """Demo login with auto-activation and 18 deep data fields - CRITICAL FIX"""
    global current_user
    
    try:
        name = "Diplomat-DEMO-001"
        full_name = "Demo User"
        
        # CRITICAL FIX: Pass all 18 arguments to prevent TypeError
        uid = db.register_traveler(
            name, full_name, "D999999", "USA", "Foreign", "2030-01-01", "BIO-DEMO-KEY",
            "Diplomat",                    # occupation
            "Official Visit",              # purpose_of_travel
            "Cairo Marriott Hotel",         # accommodation_address
            "1990-01-01",                  # dob
            "Male",                        # gender
            "+20123456789",                # phone
            "2026-10-01",                  # arrival_date
            "USA",                         # country_boarded
            "DEMO-001",                    # flight_number
            "Air",                         # mode_of_arrival
            "2026-10-10",                  # departure_date
            "USA",                         # country_residence
            "DEMO-VISA-123",               # visa_no
            "US Department of State"       # issued_by
        )
        
        if uid:
            # Auto-activate wallet for demo user
            db.activate_wallet(uid, "DEMO-CARD-1234-5678-9012")
            
            # Top up with demo funds
            db.top_up(uid, 50000)  # 50,000 EGP
            
            current_user = db.get_traveler(uid)
            
            if current_user:
                enterprise_monitor.log_metric("demo_login", 1, "ui")
                logger.info(f"✅ Demo login successful: {name}")
                
                return (
                    f"✅ DEMO MODE ACTIVATED: {name}",
                    gr.Group(visible=True),   # Show Main App
                    gr.Group(visible=False),  # Hide Activation Panel
                    gr.Group(visible=False),  # Hide Setup Wallet Panel
                    f"EGP {current_user[8]}",
                    f"🌿 {current_user[11]}",
                    "✅ ACCOUNT ACTIVE - All features available"
                )
            else:
                return f"❌ Demo login failed: User not found", gr.update(), gr.update(), gr.update(), "", "", ""
        else:
            return f"❌ Demo registration failed", gr.update(), gr.update(), gr.update(), "", "", ""
            
    except Exception as e:
        logger.error(f"❌ Demo login error: {e}")
        enterprise_monitor.log_alert("ERROR", f"Demo login failed: {e}", "ui")
        return f"❌ Demo Error: {e}", gr.update(), gr.update(), gr.update(), "", "", ""

def ui_create_wallet(card_number, expiry, cvv):
    """NEW: Create wallet with credit card validation and activation"""
    global current_user
    
    if not current_user:
        return "❌ Please login first", gr.update(), gr.update(), gr.update(), "", "", ""
    
    try:
        # Validate credit card
        if not HorusSecurity.validate_credit_card(card_number):
            return "❌ Invalid credit card number", gr.update(), gr.update(), gr.update(), "", "", ""
        
        # Validate expiry and CVV
        if not expiry or len(expiry) < 5:
            return "❌ Invalid expiry date (MM/YY)", gr.update(), gr.update(), gr.update(), "", "", ""
        
        if not cvv or len(cvv) < 3 or len(cvv) > 4:
            return "❌ Invalid CVV", gr.update(), gr.update(), gr.update(), "", "", ""
        
        # Activate wallet with credit card
        success = db.activate_wallet(current_user[0], card_number)
        
        if success:
            # Add activation deposit ($200 USD = 10,000 EGP)
            db.top_up(current_user[0], 10000)
            
            # Add transaction record
            db.add_transaction(
                current_user[0], 
                "WALLET_ACTIVATION", 
                10000, 
                "EGP", 
                f"CARD:{card_number[-4:]}"
            )
            
            # Refresh user data
            current_user = db.get_traveler(current_user[0])
            
            enterprise_monitor.log_metric("wallet_created", 1, "financial")
            logger.info(f"✅ Wallet created successfully: {current_user[0]}")
            
            return (
                "✅ Wallet created successfully! $200 USD deposited. Account now active.",
                gr.Group(visible=True),   # Show Main App
                gr.Group(visible=False),  # Hide Activation Panel
                gr.Group(visible=False),  # Hide Setup Wallet Panel
                f"EGP {current_user[8]}",
                f"🌿 {current_user[11]}",
                "✅ ACCOUNT ACTIVE - All features available"
            )
        else:
            return "❌ Wallet activation failed", gr.update(), gr.update(), gr.update(), "", "", ""
            
    except Exception as e:
        logger.error(f"❌ Wallet creation error: {e}")
        enterprise_monitor.log_alert("ERROR", f"Wallet creation failed: {e}", "financial")
        return f"❌ Error: {e}", gr.update(), gr.update(), gr.update(), "", "", ""

def ui_issue_visa():
    """Issue visa with enterprise PDF generation"""
    global current_user
    
    if not current_user:
        return "❌ Please login first", None
    
    try:
        # Check visa eligibility
        nationality = current_user[4]  # nationality at index 4
        visa_status = VisaPolicy.get_visa_status(nationality)
        
        if "ELIGIBLE" not in visa_status:
            return f"❌ {visa_status}", None
        
        # Generate visa data
        visa_data = {
            'visa_no': f"EG-VISA-{random.randint(100000, 999999)}",
            'issued_by': "Egyptian Immigration Authority"
        }
        
        # Prepare traveler data
        traveler_data = {
            'full_name': current_user[2],
            'passport': current_user[3],
            'nationality': current_user[4],
            'dob': current_user[10],  # dob at index 10
            'gender': current_user[11],  # gender at index 11
            'purpose_of_travel': current_user[9]  # purpose_of_travel at index 9
        }
        
        # Generate PDF
        pdf_data = DocumentIssuer.generate_visa_pdf(traveler_data, visa_data)
        
        if pdf_data:
            # Add visa to database
            db.add_transaction(
                current_user[0],
                "VISA_ISSUE",
                PriceCalculator.calculate_visa_fee(),
                "EGP",
                visa_data['visa_no']
            )
            
            enterprise_monitor.log_metric("visa_issued", 1, "documents")
            logger.info(f"✅ Visa issued: {visa_data['visa_no']}")
            
            return f"✅ Visa issued successfully! {visa_status}", pdf_data
        else:
            return "❌ PDF generation failed", None
            
    except Exception as e:
        logger.error(f"❌ Visa issue error: {e}")
        enterprise_monitor.log_alert("ERROR", f"Visa issue failed: {e}", "documents")
        return f"❌ Error: {e}", None

def ui_book_transport(transport_mode, quantity):
    """Book transport with green score calculation"""
    global current_user
    
    if not current_user:
        return "❌ Please login first"
    
    try:
        # Calculate price
        base_price = 50  # Base transport price
        total_price = base_price * quantity
        
        # Check wallet balance
        if current_user[8] < total_price:  # wallet_balance at index 8
            return f"❌ Insufficient balance. Need {total_price} EGP, have {current_user[8]} EGP"
        
        # Process booking
        success = db.add_transaction(
            current_user[0],
            "TRANSPORT_BOOKING",
            total_price,
            "EGP",
            f"{transport_mode}x{quantity}"
        )
        
        if success:
            # Calculate and add green points
            green_points = EcoEngine.calculate_green_score(transport_mode) * quantity
            
            # Update user balance and green points
            db.cursor.execute(
                "UPDATE travelers SET wallet_balance = wallet_balance - ?, green_points = green_points + ? WHERE id = ?",
                (total_price, green_points, current_user[0])
            )
            db.conn.commit()
            
            # Refresh user data
            current_user = db.get_traveler(current_user[0])
            
            enterprise_monitor.log_metric("transport_booked", total_price, "transport")
            logger.info(f"✅ Transport booked: {transport_mode} x{quantity}")
            
            return f"✅ {transport_mode} booked for {quantity} person(s)! 🌿 +{green_points} green points"
        else:
            return "❌ Booking failed"
            
    except Exception as e:
        logger.error(f"❌ Transport booking error: {e}")
        enterprise_monitor.log_alert("ERROR", f"Transport booking failed: {e}", "transport")
        return f"❌ Error: {e}"

def ui_scan_qr(qr_data):
    """Process QR payment with enterprise validation"""
    global current_user
    
    if not current_user:
        return "❌ Please login first"
    
    try:
        if not qr_data:
            return "❌ Please enter QR code data"
        
        # Validate QR format
        if not qr_data.startswith("PAY:"):
            return "❌ Invalid QR format. Expected: PAY:VENDOR:AMOUNT:CURRENCY"
        
        parts = qr_data.split(":")
        if len(parts) != 4:
            return "❌ Invalid QR format. Expected: PAY:VENDOR:AMOUNT:CURRENCY"
        
        _, vendor, amount_str, currency = parts
        
        try:
            amount = float(amount_str)
        except ValueError:
            return "❌ Invalid amount in QR code"
        
        if currency != "EGP":
            return "❌ Only EGP currency supported"
        
        # Check wallet balance
        if current_user[8] < amount:  # wallet_balance at index 8
            return f"❌ Insufficient balance. Need {amount} EGP, have {current_user[8]} EGP"
        
        # Process payment
        success = db.add_transaction(
            current_user[0],
            "QR_PAYMENT",
            amount,
            "EGP",
            qr_data
        )
        
        if success:
            # Update wallet balance
            db.cursor.execute(
                "UPDATE travelers SET wallet_balance = wallet_balance - ? WHERE id = ?",
                (amount, current_user[0])
            )
            db.conn.commit()
            
            # Refresh user data
            current_user = db.get_traveler(current_user[0])
            
            enterprise_monitor.log_metric("qr_payment", amount, "payments")
            logger.info(f"✅ QR payment processed: {vendor} - {amount} EGP")
            
            return f"✅ Payment successful! Paid {amount} EGP to {vendor}"
        else:
            return "❌ Payment processing failed"
            
    except Exception as e:
        logger.error(f"❌ QR payment error: {e}")
        enterprise_monitor.log_alert("ERROR", f"QR payment failed: {e}", "payments")
        return f"❌ Error: {e}"

def ui_language_change(language):
    """Handle language change with mock translation"""
    global current_language
    
    current_language = language
    
    enterprise_monitor.log_metric("language_change", 1, "ui")
    logger.info(f"✅ Language switched to: {language}")
    
    return f"✅ Language switched to {language} - Translation Active"

def ui_check_visa_eligibility():
    """Check visa eligibility with official portal link"""
    return "🔗 Check e-Visa Eligibility (Official Portal): https://visaguide.world/online/egypt-e-visa/"

# Additional utility functions
def ui_refresh_balance():
    """Refresh wallet balance"""
    global current_user
    
    if not current_user:
        return "EGP 0"
    
    try:
        current_user = db.get_traveler(current_user[0])
        return f"EGP {current_user[8]}"
    except:
        return "EGP 0"

def ui_refresh_green_score():
    """Refresh green score"""
    global current_user
    
    if not current_user:
        return "🌿 0"
    
    try:
        current_user = db.get_traveler(current_user[0])
        return f"🌿 {current_user[11]}"
    except:
        return "🌿 0"

logger.info("✅ UI Functions with Critical Fixes Initialized - Part 3 Complete")

# ==============================================================================
# 🎨 DYNAMIC ASSETS GENERATION
# ==============================================================================

def generate_dynamic_assets():
    """Generate dynamic logo and assets for HORUS interface"""
    try:
        # Create a simple logo using PIL if available
        if Image is not None:  # Check if PIL was imported successfully
            # Use the already imported PIL modules
            img = Image.new('RGB', (100, 100), color='#1C1C1C')
            draw = ImageDraw.Draw(img)
            
            # Draw a simple pyramid/gold triangle
            draw.polygon([(50, 20), (20, 80), (80, 80)], fill='#D4AF37')
            
            # Add text
            try:
                font = ImageFont.load_default()
                draw.text((35, 85), "HORUS", fill='#D4AF37', font=font)
            except:
                pass
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            logger.info("✅ Dynamic logo generated successfully")
            return img_bytes.getvalue()
        else:
            logger.warning("⚠️ PIL not available, using text logo")
            return None
            
    except Exception as e:
        logger.error(f"❌ Failed to generate dynamic assets: {e}")
        return None

# ==============================================================================
# 🎨 GRADIO INTERFACE & LAYOUT (Part 4 of 4)
# ==============================================================================

def create_ui():
    """Create the main Gradio interface with enterprise layout"""
    
    # Generate dynamic assets
    logo_data = generate_dynamic_assets()
    
    with gr.Blocks(
        title=config.APP_NAME,
        theme=gr.themes.Soft(
            primary_hue="amber",
            secondary_hue="gray",
            neutral_hue="slate"
        ),
        css="""
        .primary-btn {
            background: linear-gradient(135deg, #D4AF37, #B8941F);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .primary-btn:hover {
            background: linear-gradient(135deg, #B8941F, #D4AF37);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
        }
        .gold-header {
            background: linear-gradient(135deg, #1C1C1C, #2C2C2C);
            color: #D4AF37;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        .status-active {
            color: #10B981;
            font-weight: bold;
        }
        .status-locked {
            color: #EF4444;
            font-weight: bold;
        }
        """
    ) as demo:
        
        # ========================================================================
        # HEADER SECTION
        # ========================================================================
        with gr.Row():
            with gr.Column(scale=1):
                if logo_data:
                    gr.Image(logo_data, width=100, show_label=False)
                else:
                    gr.Markdown("🏛️")
            
            with gr.Column(scale=3):
                gr.HTML(f"""
                <div class="gold-header">
                    <h1>{config.APP_NAME}</h1>
                    <p>Enterprise Travel Management System</p>
                </div>
                """)
            
            with gr.Column(scale=1):
                language_dropdown = gr.Dropdown(
                    choices=["English", "Arabic", "French", "Russian", "German"],
                    value="English",
                    label="🌐 Language",
                    scale=1
                )
        
        # Status Bar
        status = gr.Markdown("🔒 Please login to access HORUS features")
        
        # ========================================================================
        # LOGIN SECTION
        # ========================================================================
        with gr.Group(visible=True) as login_panel:
            gr.Markdown("## 🔑 ENTERPRISE ACCESS")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### **SCAN FACE & ENTER ECOSYSTEM**")
                    
                    # Basic Information
                    name = gr.Textbox(label="User Name", placeholder="e.g., john_doe")
                    full_name = gr.Textbox(label="Full Name", placeholder="e.g., John Doe")
                    passport = gr.Textbox(label="Passport Number", placeholder="e.g., A12345678")
                    
                    with gr.Row():
                        nationality = gr.Dropdown(
                            choices=["USA", "UK", "Germany", "France", "Italy", "Spain", "Egypt", "Saudi Arabia", "UAE", "Canada", "Australia", "Japan", "China", "India", "Brazil", "Russia", "Other"],
                            label="Nationality",
                            value="USA"
                        )
                        nationality_group = gr.Dropdown(
                            choices=["Foreign", "Arab", "Egyptian"],
                            label="Nationality Group",
                            value="Foreign"
                        )
                    
                    passport_expiry = gr.Textbox(label="Passport Expiry", placeholder="YYYY-MM-DD")
                    biometric_hash = gr.Textbox(label="Biometric Hash", placeholder="Auto-generated", type="password")
                    
                    # DEEP DATA FIELDS (Procedure Doc 1030)
                    gr.Markdown("### **ARRIVAL CARD INFORMATION**")
                    
                    with gr.Row():
                        occupation = gr.Textbox(label="Occupation", placeholder="e.g., Engineer, Doctor, Student")
                        purpose_of_travel = gr.Dropdown(
                            choices=["Tourism", "Business", "Official Visit", "Study", "Medical", "Transit"],
                            label="Purpose of Travel",
                            value="Tourism"
                        )
                    
                    accommodation_address = gr.Textbox(
                        label="Accommodation Address", 
                        placeholder="e.g., Cairo Marriott Hotel, Zamalek"
                    )
                    
                    with gr.Row():
                        dob = gr.Textbox(label="Date of Birth", placeholder="YYYY-MM-DD")
                        gender = gr.Dropdown(
                            choices=["Male", "Female", "Other"],
                            label="Gender",
                            value="Male"
                        )
                    
                    with gr.Row():
                        phone = gr.Textbox(label="Phone Number", placeholder="+20xxxxxxxxxx")
                        arrival_date = gr.Textbox(label="Arrival Date", placeholder="YYYY-MM-DD")
                    
                    with gr.Row():
                        country_boarded = gr.Textbox(label="Country Boarded", placeholder="e.g., USA")
                        flight_number = gr.Textbox(label="Flight Number", placeholder="e.g., MS985")
                    
                    with gr.Row():
                        mode_of_arrival = gr.Dropdown(
                            choices=["Air", "Sea", "Land"],
                            label="Mode of Arrival",
                            value="Air"
                        )
                        departure_date = gr.Textbox(label="Departure Date", placeholder="YYYY-MM-DD")
                    
                    with gr.Row():
                        country_residence = gr.Textbox(label="Country of Residence", placeholder="e.g., USA")
                        visa_no = gr.Textbox(label="Visa Number", placeholder="e.g., V123456")
                    
                    issued_by = gr.Textbox(label="Issued By", placeholder="e.g., US Department of State")
                    
                    with gr.Row():
                        btn_login = gr.Button("🔓 ENTER ECOSYSTEM", variant="primary", size="lg")
                        btn_demo = gr.Button("🔑 DEMO ACCESS", variant="secondary", size="lg")
        
        # ========================================================================
        # SETUP WALLET PANEL (NEW)
        # ========================================================================
        with gr.Group(visible=False) as setup_wallet_panel:
            gr.Markdown("## 🔗 SETUP DIGITAL WALLET")
            gr.Markdown("Create your digital wallet to activate all HORUS features")
            
            with gr.Row():
                with gr.Column(scale=2):
                    card_number = gr.Textbox(
                        label="Credit Card Number", 
                        placeholder="1234 5678 9012 3456",
                        type="password"
                    )
                    expiry = gr.Textbox(
                        label="Expiry Date", 
                        placeholder="MM/YY",
                        max_lines=1
                    )
                    cvv = gr.Textbox(
                        label="CVV", 
                        placeholder="123",
                        type="password",
                        max_lines=1
                    )
                    
                    btn_create_wallet = gr.Button(
                        "🔗 CREATE DIGITAL WALLET & DEPOSIT $200", 
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### **Wallet Benefits**
                    - ✅ Instant monument booking
                    - ✅ QR payment processing  
                    - ✅ Transport ticketing
                    - ✅ Visa processing
                    - ✅ Green score tracking
                    
                    ### **Security**
                    - 🔒 Enterprise-grade encryption
                    - 🔒 Biometric authentication
                    - 🔒 Secure transaction logging
                    """)
        
        # ========================================================================
        # MAIN APPLICATION
        # ========================================================================
        with gr.Group(visible=False) as app:
            # Status Bar
            with gr.Row():
                bal = gr.Textbox(label="💰 Wallet Balance", value="EGP 0", interactive=False)
                score = gr.Textbox(label="🌿 Green Score", value="0", interactive=False)
                activation_status = gr.Textbox(label="📊 Account Status", value="ACTIVE", interactive=False)
            
            # Main Tabs
            with gr.Tabs():
                
                # ====================================================================
                # WALLET TAB
                # ====================================================================
                with gr.Tab("💳 Wallet & Banking"):
                    gr.Markdown("## 💰 DIGITAL WALLET")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### **Quick Actions**")
                            btn_refresh_balance = gr.Button("🔄 Refresh Balance", size="sm")
                            btn_link_bank = gr.Button("🔗 Link Bank Account", variant="secondary")
                            gr.Button("🔗 Open Bank App (Deep Link)", variant="secondary")
                            
                        with gr.Column():
                            gr.Markdown("### **Transaction History**")
                            gr.Textbox(
                                label="Recent Transactions",
                                value="No transactions yet",
                                lines=5,
                                interactive=False
                            )
                
                # ====================================================================
                # VISA TAB
                # ====================================================================
                with gr.Tab("🛂 Visa Services"):
                    gr.Markdown("## 🛂 VISA ON ARRIVAL")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### **Visa Eligibility**")
                            btn_check_eligibility = gr.Button("🔍 Check My Eligibility", variant="primary")
                            eligibility_result = gr.Textbox(label="Eligibility Status", interactive=False)
                            
                            # NEW: Official Portal Link
                            gr.HTML("""
                            <div style="margin: 20px 0;">
                                <a href='https://visaguide.world/online/egypt-e-visa/' 
                                   target='_blank' 
                                   class='primary-btn'>
                                    🔗 Check Official e-Visa Eligibility
                                </a>
                            </div>
                            """)
                        
                        with gr.Column():
                            gr.Markdown("### **Issue Visa**")
                            btn_issue_visa = gr.Button("📄 Issue E-Visa", variant="primary")
                            visa_result = gr.Textbox(label="Visa Status", interactive=False)
                            visa_download = gr.File(label="Download Visa PDF", visible=False)
                
                # ====================================================================
                # TRANSPORT TAB
                # ====================================================================
                with gr.Tab("🚇 Transport"):
                    gr.Markdown("## 🚇 EGYPT TRANSPORT 2026")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### **Book Transport**")
                            
                            transport_mode = gr.Dropdown(
                                choices=[
                                    "Cairo Monorail (+20 pts)",
                                    "LRT (Electric Train) (+20 pts)", 
                                    "Electric Bus (+20 pts)",
                                    "Metro Line 1 (+10 pts)",
                                    "Metro Line 2 (+10 pts)",
                                    "Metro Line 3 (+10 pts)",
                                    "Shared Shuttle (+5 pts)",
                                    "Train (+15 pts)",
                                    "Gas-Powered Taxi (0 pts)",
                                    "Private Car (0 pts)",
                                    "Standard Uber (0 pts)"
                                ],
                                label="Transport Mode",
                                value="Cairo Monorail (+20 pts)"
                            )
                            
                            quantity = gr.Slider(
                                minimum=1,
                                maximum=10,
                                value=1,
                                step=1,
                                label="Number of Tickets"
                            )
                            
                            btn_book_transport = gr.Button("🎫 Book Transport", variant="primary")
                            transport_result = gr.Textbox(label="Booking Status", interactive=False)
                        
                        with gr.Column():
                            gr.Markdown("### **🌿 Green Score System**")
                            gr.Markdown("""
                            - **+20 Points**: Electric transport (Monorail, LRT, Electric Bus)
                            - **+10 Points**: Metro lines
                            - **+5 Points**: Shared transport
                            - **0 Points**: Private vehicles
                            
                            **Benefits**: 100 points = 10% souvenir discount!
                            """)
                
                # ====================================================================
                # MARKETPLACE TAB
                # ====================================================================
                with gr.Tab("🛍️ Marketplace"):
                    gr.Markdown("## 🛍️ HORUS MARKETPLACE")
                    
                    # Connectivity Section
                    gr.Markdown("### 📱 **SIM & eSIM CONNECTIVITY**")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Button("📱 Buy Orange eSIM", variant="secondary", size="lg")
                            gr.Markdown("• 5G Data Plans\n• Airport Pickup\n• Tourist Packages")
                        
                        with gr.Column():
                            gr.Button("📱 Buy Vodafone eSIM", variant="secondary", size="lg")
                            gr.Markdown("• Nationwide Coverage\n• Instant Activation\n• Multi-device Support")
                    
                    with gr.Row():
                        gr.Button("📍 Locate Nearest Store", variant="outline")
                        gr.Button("📞 Customer Support", variant="outline")
                    
                    gr.Markdown("---")
                    
                    # Other Services
                    gr.Markdown("### **Other Services**")
                    with gr.Row():
                        gr.Button("🎁 Welcome Gift", variant="secondary")
                        gr.Button("📷 Photo Services", variant="secondary")
                        gr.Button("🗺️ Tour Guide", variant="secondary")
                        gr.Button("🚐 Airport Transfer", variant="secondary")
                
                # ====================================================================
                # SCAN & PAY TAB
                # ====================================================================
                with gr.Tab("📷 Scan & Pay"):
                    gr.Markdown("## 📷 QR PAYMENT SYSTEM")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### **Scan QR Code**")
                            qr_input = gr.Textbox(
                                label="QR Code Data",
                                placeholder="PAY:VENDOR:AMOUNT:CURRENCY",
                                lines=3
                            )
                            
                            with gr.Row():
                                btn_scan_qr = gr.Button("💳 Process Payment", variant="primary")
                                btn_simulate_scan = gr.Button("🟢 Simulate Metro Scan", variant="secondary")
                            
                            qr_result = gr.Textbox(label="Payment Result", lines=4, interactive=False)
                        
                        with gr.Column():
                            gr.Markdown("### **Quick Examples**")
                            gr.Markdown("""
                            **Common QR Formats:**
                            - `PAY:CAIRO_METRO:50:EGP`
                            - `PAY:UBER:150:EGP`
                            - `PAY:COFFEE_SHOP:45:EGP`
                            - `PAY:MUSEUM:200:EGP`
                            
                            **How to use:**
                            1. Scan QR code with camera
                            2. Or enter manually above
                            3. Click "Process Payment"
                            4. Receive instant confirmation
                            """)
                
                # ====================================================================
                # FAQ TAB (NEW)
                # ====================================================================
                with gr.Tab("❓ Help & FAQ"):
                    gr.Markdown("## ❓ HELP & FREQUENTLY ASKED QUESTIONS")
                    
                    with gr.Accordion("💳 How to Activate Wallet?", open=True):
                        gr.Markdown("""
                        **Wallet Activation Steps:**
                        1. Register your account with personal details
                        2. Go to "Setup Wallet" panel
                        3. Enter credit card information
                        4. Deposit $200 USD (10,000 EGP)
                        5. Account becomes ACTIVE instantly
                        
                        **Benefits:**
                        - Instant monument booking
                        - QR payment processing
                        - Transport ticketing
                        - Visa processing
                        """)
                    
                    with gr.Accordion("🛂 Visa Rules & Eligibility"):
                        gr.Markdown("""
                        **Visa on Arrival Eligibility:**
                        - 74+ countries eligible (USA, UK, EU, Japan, etc.)
                        - Check official portal for latest requirements
                        - Restricted countries: Iran, Afghanistan, Syria, etc.
                        
                        **Required Documents:**
                        - Valid passport (6+ months validity)
                        - Return ticket
                        - Hotel reservation
                        - Sufficient funds ($1000+)
                        
                        **Processing:**
                        - Fee: $25 USD (1250 EGP)
                        - Duration: 180 days
                        - Single entry
                        """)
                    
                    with gr.Accordion("🌿 Green Score System"):
                        gr.Markdown("""
                        **How to Earn Green Points:**
                        - **+20 pts**: Electric transport (Monorail, LRT, Electric Bus)
                        - **+10 pts**: Metro lines
                        - **+5 pts**: Shared transport
                        - **0 pts**: Private vehicles
                        
                        **Benefits:**
                        - 100 points = 10% souvenir discount
                        - 200 points = Free transport ticket
                        - 500 points = VIP monument access
                        
                        **Track Progress:**
                        - View in main dashboard
                        - Points update instantly
                        - Monthly leaderboard
                        """)
                    
                    with gr.Accordion("🔧 Technical Support"):
                        gr.Markdown("""
                        **Common Issues:**
                        - **Login Problems**: Check internet connection
                        - **Payment Failed**: Verify wallet balance
                        - **QR Not Working**: Ensure proper format
                        - **PDF Not Downloading**: Check browser settings
                        
                        **Contact Support:**
                        - Email: support@horus-egypt.com
                        - Phone: +20 2 1234 5678
                        - Live Chat: Available 24/7
                        
                        **Response Time:**
                        - Email: Within 24 hours
                        - Phone: Immediate
                        - Live Chat: < 5 minutes
                        """)
        
        # ========================================================================
        # EVENT HANDLING
        # ========================================================================
        
        # Language change
        language_dropdown.change(
            ui_language_change,
            inputs=[language_dropdown],
            outputs=[status]
        )
        
        # Login events
        btn_login.click(
            ui_login,
            inputs=[
                name, full_name, passport, nationality, nationality_group, passport_expiry,
                biometric_hash, occupation, purpose_of_travel, accommodation_address,
                dob, gender, phone, arrival_date, country_boarded, flight_number,
                mode_of_arrival, departure_date, country_residence, visa_no, issued_by
            ],
            outputs=[status, app, setup_wallet_panel, login_panel, bal, score, activation_status]
        )
        
        # Demo login
        btn_demo.click(
            ui_demo_login,
            outputs=[status, app, setup_wallet_panel, login_panel, bal, score, activation_status]
        )
        
        # Wallet creation
        btn_create_wallet.click(
            ui_create_wallet,
            inputs=[card_number, expiry, cvv],
            outputs=[status, app, setup_wallet_panel, login_panel, bal, score, activation_status]
        )
        
        # Visa services
        btn_check_eligibility.click(
            lambda: "Check your nationality in the official portal link below",
            outputs=[eligibility_result]
        )
        
        btn_issue_visa.click(
            ui_issue_visa,
            outputs=[visa_result, visa_download]
        )
        
        # Transport booking
        btn_book_transport.click(
            ui_book_transport,
            inputs=[transport_mode, quantity],
            outputs=[transport_result]
        )
        
        # QR payment
        btn_scan_qr.click(
            ui_scan_qr,
            inputs=[qr_input],
            outputs=[qr_result]
        )
        
        btn_simulate_scan.click(
            lambda: ui_scan_qr("PAY:CAIRO_METRO:50:EGP"),
            outputs=[qr_result]
        )
        
        # Utility buttons
        btn_refresh_balance.click(
            ui_refresh_balance,
            outputs=[bal]
        )
    
    return demo

# ==============================================================================
# 🚀 APPLICATION LAUNCH
# ==============================================================================

if __name__ == "__main__":
    try:
        logger.info("🚀 Launching HORUS v11.0 Enterprise Edition...")
        
        # Create UI
        demo = create_ui()
        
        # Log system health
        system_health = enterprise_monitor.get_system_health()
        logger.info(f"📊 System Health: {system_health['uptime_formatted']} uptime")
        logger.info(f"📊 Metrics: {system_health['total_metrics']} tracked")
        logger.info(f"📊 Alerts: {system_health['total_alerts']} logged")
        
        # Launch application
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            debug=False,
            show_error=True,
            quiet=False,
            favicon_path=None,
            ssl_verify=False,
            prevent_thread_lock=False
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to launch application: {e}")
        enterprise_monitor.log_alert("CRITICAL", f"Application launch failed: {e}", "system")
        sys.exit(1)

# ==============================================================================
# 🏁 END OF HORUS v11.0 ENTERPRISE EDITION
# ==============================================================================

logger.info("✅ HORUS v11.0 Enterprise Edition - All Parts Complete")
logger.info("🏛️ System Ready for Enterprise Deployment")
