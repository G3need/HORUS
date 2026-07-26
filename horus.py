# ==============================================================================
# HORUS v10.6.py - Sovereign Edition (Final Production Release)
# ==============================================================================

# STANDARD LIBRARY IMPORTS (Global Access)
import os, sys, subprocess, importlib.util, time, platform, json, logging, threading, random, base64, re, hashlib, warnings
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# Suppress specific warnings for cleaner output
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*css.*parameter.*")
warnings.filterwarnings("ignore", category=FutureWarning, module="google.colab")

def _install_and_import(package, pip_name=None):
    if pip_name is None: pip_name = package
    if importlib.util.find_spec(package) is None:
        print(f"📦 Installing {pip_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pip_name])
    return importlib.import_module(package)

# 1. System Drivers (Colab/Linux Safe)
if os.path.exists("/content"):
    try:
        subprocess.run(["ldconfig", "-p"], check=True, stdout=subprocess.DEVNULL)
    except:
        print("⚙️ Installing System Drivers...")
        subprocess.run(["apt-get", "update", "-qq"], check=True)
        subprocess.run(["apt-get", "install", "-y", "-qq", "libzbar0"], check=True)

# 2. Lazy Imports
print("🚀 Launching HORUS v12.0 Sovereign Edition...")
gr = _install_and_import("gradio")
qrcode = _install_and_import("qrcode")
reportlab = _install_and_import("reportlab")
cv2 = _install_and_import("cv2", "opencv-python-headless")
pyzbar = _install_and_import("pyzbar", "pyzbar")
# AI ENGINE SELECTOR
try:
    import google.genai as genai
    AI_LIB = "genai"
except ImportError:
    print("📦 Installing google-genai...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-genai"])
    import google.genai as genai
    AI_LIB = "genai"
sqlite3 = importlib.import_module("sqlite3")
datetime = importlib.import_module("datetime")

# Configure logging for system operations
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==============================================================================
# 🖼️ HORUS ASSETS MANAGEMENT
# ==============================================================================

class HorusAssets:
    # Paste your HUGE Base64 string inside these quotes
    LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AXHiAAAuZklEQVR42u2dd3gc1dX/v+femdmi5o6NTa+v7DiATSdICp0EEspuKAmEZgOhhtDyAqNJApgQWkIINiQkQAjsEgi9YwmCscEGA5ZoLuAmI9lW3TIz997z+2O1xhhT37zvzxbzeR79IWl2dnb2O+eee+455wIREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREDH4puwRfD/Mn7RASO7kokrK8oIJeamiAAoKOjldPprAE+LSTXhahHnUB9Peo7WhmpjCGiSHAR/WJyXTF9umtxJiU/W3Asmd0kf3RzJfNUuyS79T+o06fXWZxJyXWtXGSxvhGWiampqVE2NXnG82A+/vv0eN+Spm0L3X3jUORdQo1tSJsxhv1qaCQJkFrovGArLyDbyVIfGJLzEk5s7uChsfdpy6vaPvE+mZTMAkils4bwzRo+6ZslKFcg20qUzuo1f1s9ZfOe5asbwpw6OAzVbsqYLRMxIQQEtNZQoYY2gGENZgaBQESQEpCCQAT4voIKdbeQVoslMaM6kXisco+dZhKdVCy/z3S3zqpHvSHPM5GwBozflBGg9Bqrwb13juhd2HJ4vhAepVW4T8ISlVpr5H0DpRQEAZYlYVkCthQgAkAMMGAMYEzpuDBkhGEIrY1hkHAsIOZIqFAjNFhg2fLJuE33j6w/6EWitC75Zq5oHNtKSGXNQJ4EDEhhMUBgl4BWIvrYOnW/f/meQWfxFB0Ehzu2GB4EPgpFDSIgGbMgLYliyNDKdJEUyyBoqRTBUiDeW4QoWCC2dSGpEVap0N4crDfVyowWxINiNqCUQa4QIgyVsQgiHrMQKgViekM6OlM1JJEdsedf3/8mDJU0cITEQDYtmobXUkODpz62WLdXrXzrgx/Az5+mimpfKRnFQgAiQiLuQBkDbWiJlPQyOfEXpZOYHascvKhy63Pbv2iWx8zUt/CqEbmOlVupYnEXHQb7BKHZA9psZUmDfCGE74dsSaK4Y6Ho64IlxTNWUty53VDxDO3x9561h8qOsSM4NUAs2cYmLOJMSjQNryUA/dP8Wib6pN/CzJRfMGWXQk9XWgfB0YJ5axMqKK0Ri9kIFIOJ37ZE7CmZ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T54Wrr234LrEY7I/v49Bwu7yvGZ17rlP+ulsVt932a7pf/xyjxHAmhZJIIBTABpOai7aduy8UIEdy2zXs1Kd+reLJ+4sJH4qbfoREXFLbXa9ZfkDhQG/i70upUHAQOTv93a/LGZjUi6HJ1MXzFw93a2zGrxPbzS+hl6ACcL3DYwqHDjt5xNuEsaYABjd2VMct8PgIbut+5LyGmN6SvbZ287f5V5AHdvjFy51pLycBP3utOtef2Mg7Uv4jbVYxnBpDxs2xODxfXkFm3DwP67Y49cNXrP67PaSQC8ANlzaFRWBtFEUFgWSTDhUGa7oqB6xXnH0WyOiirjXFyBvEQ9XrLtGb77JZa4LkUpnB3wHwYHvvKM/V92wNWr0yFOU4bdDZWC0uuzv7j4/LDvdnxMXM44loKn62ZOubzn7pze0nHPG7+ftV5Gs/GPXR+1D1xdBLy/lnHbljHcFq4WOLVlxrOXQc59cE8+KhLXxWyzokgOe3OfUh3sraqqOIaK8CpUxYeHP97t1O3pes/qsBWhGqRBCG1XpunXWHW5d3HUhLKvmriAxoosIvB6hlErRQGAjtGEmNiKGb1CrygE/KzTc/wNWZ5+9bewHFz3/ZpLk6dKSQik9JFfsy86988cVLbVZXje7IBGzSs47A8RgoNkEbX0aAH5y1VNtZ3nZvrsu2e3AzPl7JNYvSgDM/RU+PKCd9W+MsFpb+2vt2ITMYGI231kxX01366wjrnzlLqWtW21Lwhg17vWWd/6yJgeqX1xr1vOMYWMMM6HoeTCTp80Jy8f+6bwJexf88NDUDTOLqf78+LVEVRK2gQazMVyaR7S2fjOs1kCdFVI2Cw0QQmWNlsKQAIZuvf8kMXHytNB166wt6uvP/vDJJ0bYko8UUqenXbBr56TGV87wiDjTWkr2u/EcGkJsDWdmMlqP/v3PD9yR2NhW2JcgLuyqlP9bbcTZBLBbW0f9acNrWii5V5yWDNtf3swxEODCyP6wxjei+97A7PMOYGFmQvXb79rn9hSKp/mhJpJE1VblPWMHx2+8p+f5tpJz79Lff/nwuYWAjjastolL+UB1deXdc9WLM8fpPb/dlctf6KuwjjVrCMFCUAEsADYxZVQNyOrhZMUB51076/1y5me5M07219/ZcnVXz7lhITxKGQNLiLAqnrxl9IhBtx1wybM9PMCd+AFrludlap0l75mhorOzp7vSULFP8JDKzavGV8vuzS+YWVh3c8yMC0f2bT3IrhxsDvfmrMxMmVAjOzpjKysX9o3CBAzr+YgxZimwFBi2JUxPHAaYgE8VqPZz5wXjKyynt3LLYtgzXwwRAFChg2pdI1alN7DuexH/Cw9Wf+/QKOkuslhffVhc5wN/1vBDa1WY8We9fj03j/9D7x8REREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREQEA+H9wzb3mFoil5wAAAABJRU5ErkJggg==" 
    
    @staticmethod
    def get_logo_path():
        """
        Robust Hybrid Loader:
        1. Checks if 'horus_logo_active.png' already exists locally.
        2. If not, creates it from the embedded Base64 string.
        3. Returns the absolute path guaranteed to work with Gradio.
        """
        import base64, os, re
        
        # 1. Define the persistent local path (Not Temp!)
        # In Colab, this usually maps to /content/horus_logo_active.png
        local_filename = "horus_logo_active.png"
        local_path = os.path.abspath(local_filename)
        
        # 2. If it already exists, just use it (Speed Optimization)
        if os.path.exists(local_path):
            print(f"✅ Found active logo at: {local_path}")
            return local_path

        # 3. Validation: Check if we have a valid Base64 string
        raw_b64 = HorusAssets.LOGO_B64
        if "PASTE_" in raw_b64 or len(raw_b64) < 100:
            print("⚠️ No embedded logo found. Using fallback.")
            return None

        # 4. Decode and Save to Local File
        try:
            print(f"🔄 Decoding embedded logo ({len(raw_b64)} chars)...")
            
            # Clean up the string (Remove headers like 'data:image/png;base64,')
            clean_b64 = re.sub(r'^data:image/.+;base64,', '', raw_b64.strip())
            
            # Decode
            img_data = base64.b64decode(clean_b64)
            
            # Write to disk
            with open(local_path, "wb") as f:
                f.write(img_data)
            
            print(f"✅ Success! Logo saved to: {local_path}")
            return local_path
            
        except Exception as e:
            print(f"❌ Logo Decode Error: {e}")
            return None

# ==============================================================================
# 🧠 ENTERPRISE MONITORING & LOGGING SYSTEM
# ==============================================================================

import threading
import json
from datetime import datetime
from collections import defaultdict

class EnterpriseMonitor:
    """Military-grade monitoring and logging system"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.alerts = []
        self.performance_data = {}
        self._lock = threading.Lock()
        self.start_time = datetime.now()
    
    def log_metric(self, metric_name: str, value: float, category: str = "general"):
        """Log a performance metric with timestamp"""
        with self._lock:
            timestamp = datetime.now().isoformat()
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
            timestamp = datetime.now().isoformat()
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
        uptime = datetime.now() - self.start_time
        
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
                'export_timestamp': datetime.now().isoformat()
            }, indent=2)

# Global enterprise monitor instance
enterprise_monitor = EnterpriseMonitor()

# ==============================================================================
# 🛠️ ENTERPRISE DEPENDENCY INSTALLER
# ==============================================================================

def is_linux_colab():
    """Check if running on Linux (Google Colab) environment"""
    try:
        if platform.system() != "Linux":
            return False
        return (
            "google.colab" in sys.modules or
            "COLAB_GPU" in os.environ or
            "COLAB_RELEASE_TAG" in os.environ or
            os.path.exists("/content")
        )
    except Exception:
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

def install_dependencies():
    """
    Enterprise dependency installer with system and Python package management
    """
    logger.info("🚀 Starting enterprise dependency installation...")
    
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
# HEAVY IMPORTS (Safe Import Pattern)
# ==============================================================================

def safe_import_with_error_handling():
    """Perform heavy imports with comprehensive error handling and resource management"""
    import_status = {}
    global gr, np, Image, cv2, pyzbar, qrcode, canvas, letter, ImageReader, pdfmetrics, TTFont, genai, sqlite3
    
    # Initialize all imports to None first
    gr = np = Image = cv2 = pyzbar = qrcode = canvas = letter = ImageReader = pdfmetrics = TTFont = genai = sqlite3 = None
    
    try:
        import gradio as gr
        import_status['gradio'] = True
        logger.info(" Gradio imported successfully")
    except ImportError as e:
        logger.error(f" Failed to import Gradio: {e}")
        import_status['gradio'] = False
        gr = None
    
    try:
        import numpy as np
        import_status['numpy'] = True
        logger.info(" NumPy imported successfully")
    except ImportError as e:
        logger.error(f" Failed to import NumPy: {e}")
        import_status['numpy'] = False
        np = None
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import_status['pillow'] = True
        logger.info(" PIL imported successfully")
    except ImportError as e:
        logger.error(f" Failed to import PIL: {e}")
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

# Run the enterprise installer
if not install_dependencies():
    logger.error("❌ CRITICAL: Dependency installation failed. Some features may not work.")
    # Don't exit, continue with limited functionality

# Perform safe imports
import_status = safe_import_with_error_handling()

# Re-check critical imports after installation
critical_imports = ['gradio', 'numpy', 'sqlite3']
failed_critical = [pkg for pkg in critical_imports if not import_status.get(pkg, False)]

if failed_critical:
    logger.error(f"❌ CRITICAL: Failed to import critical packages: {failed_critical}")
    logger.error("❌ Application may not function properly without these dependencies.")
    # Don't exit immediately, try to continue with limited functionality

# Log final import status
logger.info("📊 Final Import Status:")
for pkg, status in import_status.items():
    status_icon = "✅" if status else "❌"
    logger.info(f"  {status_icon} {pkg}: {'Available' if status else 'Missing'}")

def generate_dynamic_assets():
    """Generate assets with priority: Embedded > Local > Dynamic Fallback"""
    import os
    import base64
    from io import BytesIO
    
    # PRIORITY 1: Check Embedded Asset (The User's Paste)
    if hasattr(HorusAssets, 'LOGO_B64') and len(HorusAssets.LOGO_B64) > 1000:
        logger.info("✅ Found embedded Base64 logo in HorusAssets")
        raw_b64 = HorusAssets.LOGO_B64.strip()
        
        # Ensure it has the data URI prefix
        if not raw_b64.startswith("data:image"):
            return f"data:image/png;base64,{raw_b64}"
        return raw_b64

    logo_found = False
    logo_data = None
    
    # PRIORITY 2: Try to load from Colab root folder
    colab_logo_path = "/content/horus_logo.png"
    local_logo_path = "horus_logo.png"
    
    # Check Colab root first
    if os.path.exists(colab_logo_path):
        try:
            with open(colab_logo_path, "rb") as f:
                logo_bytes = f.read()
            logo_data = f"data:image/png;base64,{base64.b64encode(logo_bytes).decode()}"
            logo_found = True
            logger.info("✅ Logo loaded from Colab root folder")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load Colab logo: {e}")
    
    # Check local directory
    if not logo_found and os.path.exists(local_logo_path):
        try:
            with open(local_logo_path, "rb") as f:
                logo_bytes = f.read()
            logo_data = f"data:image/png;base64,{base64.b64encode(logo_bytes).decode()}"
            logo_found = True
            logger.info("✅ Logo loaded from local directory")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load local logo: {e}")
    
    # PRIORITY 3: Fallback: Generate dynamic logo
    if not logo_found:
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Generate high-quality base64 encoded logo
            img = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            
            # Draw outer glow
            for i in range(5):
                alpha = 50 - i * 10
                d.ellipse([10-i*2, 10-i*2, 290+i*2, 290+i*2], 
                         outline=(212, 175, 55, alpha), width=2)
            
            # Draw main circles
            d.ellipse([20, 20, 280, 280], outline="#D4AF37", width=12)
            d.ellipse([40, 40, 260, 260], outline="#D4AF37", width=6)
            
            # Draw eye symbol
            d.ellipse([100, 100, 200, 200], outline="#D4AF37", width=8)
            d.ellipse([125, 125, 175, 175], fill="#D4AF37")
            
            # Draw pupil
            d.ellipse([140, 140, 160, 160], fill="#1a1a1a")
            d.ellipse([145, 145, 155, 155], fill="#D4AF37")
            
            # Draw HORUS text
            try:
                font = ImageFont.truetype("arial.ttf", 28)
                font_bold = ImageFont.truetype("arialbd.ttf", 28)
            except:
                font = ImageFont.load_default()
                font_bold = font
            
            # Calculate text position for centering
            text = "HORUS"
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_x = (300 - text_width) // 2
            
            d.text((text_x, 220), text, fill="#D4AF37", font=font_bold)
            
            # Convert to base64 for embedding
            buffer = BytesIO()
            img.save(buffer, format='PNG', optimize=True)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            logo_data = f"data:image/png;base64,{img_str}"
            logger.info("✅ High-quality dynamic logo generated successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to generate dynamic logo: {e}")
            # Ultimate fallback: SVG logo
            logo_data = "data:image/svg+xml;base64," + base64.b64encode(
                '''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
                    <defs>
                        <radialGradient id="gold">
                            <stop offset="0%" style="stop-color:#D4AF37;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#B8941F;stop-opacity:1" />
                        </radialGradient>
                    </defs>
                    <circle cx="150" cy="150" r="130" fill="none" stroke="url(#gold)" stroke-width="12"/>
                    <circle cx="150" cy="150" r="110" fill="none" stroke="url(#gold)" stroke-width="6"/>
                    <circle cx="150" cy="150" r="50" fill="url(#gold)"/>
                    <circle cx="150" cy="150" r="20" fill="#1a1a1a"/>
                    <circle cx="150" cy="150" r="8" fill="url(#gold)"/>
                    <text x="150" y="220" text-anchor="middle" fill="url(#gold)" font-size="28" font-weight="bold">HORUS</text>
                </svg>'''.encode()
            ).decode()
    
    return logo_data

# Additional standard library imports
import json
import hashlib
import random
import threading
import datetime
import io
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple

# ==============================================================================
# 🏛️ ENTERPRISE CONFIGURATION & UTILITIES
# ==============================================================================

@dataclass
class HorusConfig:
    """Enterprise configuration for HORUS v12.0"""
    APP_NAME: str = "Horus Key Enterprise v12.0 - Sovereign Edition"
    DB_NAME: str = "horus_sovereign.db"
    AI_MODEL: str = "gemini-3.6-flash"
    AI_FALLBACK_MODELS: list = field(default_factory=lambda: [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3-flash-preview",
        "gemini-2.5-flash"
    ])
    AI_ENABLED: bool = False  # Set after import checking
    VERSION: str = "12.0.0-Sovereign"

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
    SOVEREIGN_EDITION: bool = True
    
    # Hardcoded Gemini API Keys
    GEMINI_KEYS: list = field(default_factory=lambda: [
        k.strip() for k in (
            os.getenv("GEMINI_KEYS") or 
            os.getenv("GEMINI_API_KEY") or 
            os.getenv("GOOGLE_API_KEY") or ""
        ).split(",") if k.strip()
    ])

    def __post_init__(self):
        """Post-initialization to set dynamic values"""
        # Update dynamic values based on import status
        if 'import_status' in globals():
            self.QR_SCANNER_ENABLED = HorusConfig.QR_SCANNER_ENABLED = import_status.get('pyzbar', False)
            self.CAMERA_ENABLED = HorusConfig.CAMERA_ENABLED = import_status.get('opencv', False)
            # EXPLICIT: Set AI_ENABLED based on actual import success
            self.AI_ENABLED = HorusConfig.AI_ENABLED = import_status.get('genai', False)
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
            "sovereign_edition": cls.SOVEREIGN_EDITION
        }

    @staticmethod
    def get_key():
        """Get a random Gemini API key with masked logging"""
        import random
        key = random.choice(HorusConfig.GEMINI_KEYS)
        # Mask key for logs
        print(f"🔑 Using AI Key: ...{key[-6:]}")
        return key

# Create global config instance AFTER imports are checked and class is defined
config = HorusConfig()
logger.info(f"🔧 Config created with AI_ENABLED: {config.AI_ENABLED}")

class ReadmeGenerator:
    """Enterprise README generator with comprehensive troubleshooting and features"""
    
    @staticmethod
    def generate_readme():
        """Generate comprehensive enterprise README with advanced features"""
        system_status = HorusConfig.get_system_status()
        
        readme_content = f"""
# {HorusConfig.APP_NAME}

## 🚀 Enterprise Edition - Advanced QR & AI Capabilities

## 📋 System Requirements

### Core Dependencies (Auto-Installed)
- **Python 3.8+**
- **Gradio 4.0+** - Advanced web interface
- **SQLite3** - Enterprise database (built-in)
- **NumPy** - High-performance numerical operations

### Advanced QR Scanner Dependencies
- **Pyzbar** - Enterprise QR code decoding
- **OpenCV** - Professional image processing
- **Pillow** - Advanced image handling
- **libzbar0** - System QR library (auto-installed on Linux)

### Enterprise AI Dependencies
- **Google Generative AI** - Advanced AI chat capabilities
- **ReportLab** - Professional PDF generation

### System Dependencies (Linux/Colab)
- **libzbar0** - Enterprise QR code library (auto-installed)

## 🔧 Installation

### Enterprise Installation (Recommended)
```bash
python horus.py
```
The application will automatically detect and install all system and Python dependencies.

### Manual Installation
```bash
# System dependencies (Linux/Colab only)
sudo apt-get update
sudo apt-get install -y libzbar0

# Python dependencies
pip install gradio>=4.0.0 pyzbar qrcode[pil] pillow opencv-python reportlab numpy google-genai
```

## 🛠️ Enterprise Features

### Advanced QR Scanning
- **Real-time QR Detection**: Multiple QR codes in single image
- **Payment Validation**: Enterprise-grade QR format validation
- **Camera Integration**: Professional webcam support
- **Manual Fallback**: Text input for manual QR entry

### Enhanced AI Capabilities
- **Intelligent Chat**: Context-aware AI assistance
- **Travel Recommendations**: Personalized suggestions
- **Document Analysis**: AI-powered document processing
- **Multi-language Support**: Global traveler assistance

### Enterprise Security
- **Biometric Authentication**: SHA-512 facial recognition
- **Wallet Protection**: Advanced transaction security
- **Data Encryption**: Enterprise-grade data protection
- **Audit Trails**: Comprehensive logging system

## 🛠️ Troubleshooting

### QR Scanner Issues
**Issue**: "No QR code detected" or QR decoding errors
**Solution**:
1. Ensure proper lighting and clear QR code visibility
2. Check camera permissions and functionality
3. Verify pyzbar installation: `pip install --upgrade pyzbar`
4. On Linux: `sudo apt-get install -y libzbar0`
5. Try manual QR entry as fallback

### Camera Not Working
**Issue**: "HARDWARE ERROR: WEBCAM DATA INVALID"
**Solution**:
1. Check browser camera permissions
2. Try different browser (Chrome/Firefox/Edge)
3. Ensure OpenCV is installed: `pip install --upgrade opencv-python`
4. Verify camera hardware functionality
5. Restart browser and application

### AI Chat Not Working
**Issue**: "Configuration Error: Please grant access to 'GEMINI_KEYS'"
**Solution**:
1. Set environment variable: `export GEMINI_KEYS="your-api-key"`
2. In Colab: Add GEMINI_KEYS to notebook secrets
3. Get API key from: https://makersuite.google.com/app/apikey
4. Verify Google Generative AI installation: `pip install --upgrade google-genai`

### PDF Generation Issues
**Issue**: Visa PDF not downloading or corrupted
**Solution**:
1. Ensure ReportLab is installed: `pip install --upgrade reportlab`
2. Check browser download settings and permissions
3. Try different browser for PDF downloads
4. Verify sufficient disk space for PDF generation

### System Dependency Issues
**Issue**: Package installation failures
**Solution**:
1. Run system update: `sudo apt-get update`
2. Install build tools: `sudo apt-get install build-essential`
3. Check Python version compatibility
4. Use virtual environment for isolation

## 📊 Enterprise System Status

Current system capabilities:
- **Platform**: {system_status['platform']}
- **Colab Environment**: {system_status['is_colab']}
- **QR Scanner**: {'✅ Enterprise Ready' if system_status['qr_scanner'] else '❌ Not Available'}
- **Camera**: {'✅ Professional Ready' if system_status['camera'] else '❌ Not Available'}
- **AI Chat**: {'✅ Enhanced Ready' if system_status['ai'] else '❌ Not Available'}
- **Enterprise Mode**: {'✅ Active' if system_status['enterprise_mode'] else '❌ Inactive'}
- **Advanced QR**: {'✅ Enabled' if system_status['advanced_qr'] else '❌ Disabled'}
- **Enhanced AI**: {'✅ Enabled' if system_status['enhanced_ai'] else '❌ Disabled'}

## 🎯 Enterprise Features

### Core Features
- ✅ **Biometric Security**: Enterprise-grade SHA-512 authentication
- ✅ **Wallet & Banking**: Advanced financial integration
- ✅ **Family Mode**: Multi-visitor enterprise ticketing
- ✅ **Green Score**: Environmental impact tracking
- ✅ **Real Egypt Transport**: Authentic enterprise mobility

### Advanced Features
- ✅ **Deep Data**: 15-field enterprise arrival card compliance
- ✅ **Welcome Gift**: Enterprise airport pickup system
- ✅ **Demo Mode**: Professional demonstration capabilities
- ✅ **AI Chat**: Enterprise intelligent assistant
- ✅ **Git Sync**: Automated enterprise repository management
- ✅ **Document Issuance**: Professional PDF generation

### Enterprise Enhancements
- ✅ **Advanced QR**: Multi-QR detection and validation
- ✅ **Enhanced AI**: Context-aware intelligent assistance
- ✅ **System Healing**: Automatic dependency resolution
- ✅ **Professional UI**: Enterprise-grade interface design
- ✅ **Comprehensive Logging**: Enterprise audit trails
- ✅ **Error Recovery**: Robust error handling and recovery

## 🚀 Quick Start

### Enterprise Demo
1. Run the application: `python horus.py`
2. Click "🔑 DEMO ACCESS" for instant enterprise testing
3. Experience advanced QR scanning with camera integration
4. Test enhanced AI chat capabilities
5. Explore all enterprise features with full functionality

### Full Registration
1. Use "SCAN FACE & ENTER ECOSYSTEM" for complete registration
2. Fill deep data fields for enterprise compliance
3. Activate wallet with $200 USD deposit (demo bypasses this)
4. Experience enterprise-grade travel management
5. Utilize advanced QR scanning and AI features

## 📞 Enterprise Support

For enterprise support and assistance:
1. Check the comprehensive troubleshooting section above
2. Verify all dependencies are properly installed
3. Review system status in the application
4. Check detailed logs for enterprise debugging
5. Contact enterprise support for advanced issues

## 🔧 Enterprise Configuration

### Environment Variables
- `GEMINI_KEYS`: Google AI API keys for enhanced chat
- `HORUS_ENTERPRISE`: Enable enterprise-specific features
- `HORUS_DEBUG`: Enable detailed debugging logs
- `HORUS_QR_ADVANCED`: Enable advanced QR features

### Custom Configuration
Enterprise features can be customized through the HorusConfig class:
- Advanced QR processing parameters
- Enhanced AI model selection
- Enterprise security settings
- Professional UI customization

---
*HORUS v10.3 - Enterprise Smart Travel Platform with Advanced QR & AI*
"""
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        logger.info(" Enterprise README.md generated successfully")
        return "README.md"

# ==============================================================================
# ENTERPRISE SECURITY & BIOMETRICS
# ==============================================================================

class HorusSecurity:
    """Enterprise security class with advanced biometric handling"""
    
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
        Enterprise biometric scanning with comprehensive None handling
        SECURITY FIX: Prevent "HARDWARE ERROR" with proper None input handling
        """
        # SECURITY FIX: Strict None input handling
        if image is None:
            logger.warning("Enterprise biometric scan received None input")
            return None
        
        # SECURITY FIX: Validate numpy array type and shape
        if not isinstance(image, np.ndarray):
            logger.warning(f"Enterprise biometric scan received invalid type: {type(image)}")
            return None
        
        # SECURITY FIX: Validate image dimensions
        if len(image.shape) < 2 or len(image.shape) > 3:
            logger.warning(f"Enterprise biometric scan received invalid image shape: {image.shape}")
            return None
        
        try:
            # Convert numpy array to PIL Image for processing
            if len(image.shape) == 3:
                # RGB image, convert to PIL
                pil_image = Image.fromarray(image.astype('uint8'))
            else:
                # Grayscale image, convert to PIL
                pil_image = Image.fromarray(image.astype('uint8'), mode='L')
            
            # Enterprise biometric processing (in production, use advanced face recognition)
            # For demo, we'll generate a consistent hash based on image properties
            img_bytes = pil_image.tobytes()
            bio_hash = hashlib.sha512(img_bytes).hexdigest()
            
            logger.info("Enterprise biometric scan successful")
            return bio_hash
            
        except Exception as e:
            logger.error(f"Enterprise biometric scan failed: {str(e)}")
            return None

# ==============================================================================
# 📱 ENTERPRISE QR DECODING ENHANCEMENT
# ==============================================================================

class QRDecoder:
    """
    Enterprise QR Code Decoding class with advanced multi-QR support
    Supports decoding from webcam images and various QR formats with enhanced validation
    """
    
    @staticmethod
    def decode_from_image(image) -> List[str]:
        """
        Decode multiple QR codes from numpy array image with enhanced preprocessing
        Returns list of decoded QR data strings
        """
        if image is None:
            logger.warning("Enterprise QR decode received None image")
            return []
        
        # Check if pyzbar is available
        if pyzbar is None:
            logger.warning("Enterprise QR decode: pyzbar not available")
            return []
        
        try:
            # Convert numpy array to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(image.astype('uint8'))
            else:
                pil_image = Image.fromarray(image.astype('uint8'), mode='L')
            
            # Convert PIL to OpenCV format for preprocessing
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # ENHANCED PREPROCESSING FOR LOW-LIGHT WEBCAM FEEDS
            # Step 1: Convert to grayscale for better QR detection
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Step 2: Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Step 3: Adaptive thresholding for better contrast in varying lighting
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Step 4: Additional contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(thresh)
            
            # Try decoding with original image first (best quality)
            decoded_objects = pyzbar.decode(opencv_image)
            
            # If no QR codes found, try with preprocessed image
            if not decoded_objects:
                logger.info("🔍 No QR codes in original image, trying enhanced preprocessing...")
                decoded_objects = pyzbar.decode(enhanced)
                
                # If still no codes, try with thresholded image
                if not decoded_objects:
                    logger.info("🔍 Trying thresholded image...")
                    decoded_objects = pyzbar.decode(thresh)
            
            # Extract data from decoded objects
            qr_data = []
            for obj in decoded_objects:
                try:
                    decoded_text = obj.data.decode('utf-8')
                    qr_data.append(decoded_text)
                    logger.info(f"✅ Successfully decoded QR: {decoded_text[:50]}...")
                except Exception as decode_error:
                    logger.warning(f"⚠️ Failed to decode QR data: {decode_error}")
            
            logger.info(f"Enterprise decoded {len(qr_data)} QR codes from image (preprocessing: {'enhanced' if len(qr_data) > 0 else 'failed'})")
            return qr_data
            
        except Exception as e:
            logger.error(f"Enterprise QR decoding failed: {str(e)}")
            return []
    
    @staticmethod
    def validate_payment_qr(qr_data: str) -> bool:
        """
        Enterprise validation for QR data following payment format: PAY:VENDOR_ID:AMOUNT:CURRENCY
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
        Enterprise parsing of payment QR data into structured dictionary
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
    
    @staticmethod
    def validate_multiple_qr_codes(qr_data_list: List[str]) -> List[Dict[str, str]]:
        """
        Enterprise validation for multiple QR codes
        Returns list of valid payment QR data dictionaries
        """
        valid_qr_codes = []
        for qr_data in qr_data_list:
            parsed = QRDecoder.parse_payment_qr(qr_data)
            if parsed:
                valid_qr_codes.append(parsed)
        return valid_qr_codes

# ==============================================================================
# 🧠 ENTERPRISE LOGIC ENGINES
# ==============================================================================

class VisaPolicy:
    """Enterprise visa policy enforcement with comprehensive eligibility management"""
    
    ELIGIBLE_COUNTRIES = [
        "Albania", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahrain", "Belarus", "Belgium", "Bolivia", "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hong Kong", "Hungary", "Iceland", "India", "Ireland", "Italy", "Japan", "Kazakhstan", "Kuwait", "Latvia", "Lithuania", "Luxembourg", "Malaysia", "Malta", "Mexico", "Moldova", "Monaco", "Montenegro", "Netherlands", "New Zealand", "North Macedonia", "Norway", "Oman", "Paraguay", "Peru", "Poland", "Portugal", "Qatar", "Romania", "Russia", "San Marino", "Saudi Arabia", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sweden", "Switzerland", "Taiwan", "Ukraine", "UAE", "UK", "USA", "Uruguay", "Vatican City", "Venezuela"
    ]
    
    RESTRICTED_COUNTRIES = [
        "Iran", "Afghanistan", "Syria", "Yemen", "Libya", "Somalia", 
        "North Korea", "Sudan", "Lebanon", "Iraq", "Palestine"
    ]
    
    @staticmethod
    def get_nationality_group(nationality: str) -> str:
        """Enterprise nationality classification for pricing and policy purposes"""
        if nationality == "Egypt":
            return "Egyptian"
        elif nationality in ["Jordan", "Lebanon", "Morocco", "Tunisia", "Algeria", "Libya", "Sudan"]:
            return "Arab"
        else:
            return "Foreign"
    
    @staticmethod
    def check_eligibility(nationality: str) -> bool:
        """Enterprise check if nationality is eligible for Visa on Arrival"""
        return nationality in VisaPolicy.ELIGIBLE_COUNTRIES
    
    @staticmethod
    def is_restricted(nationality: str) -> bool:
        """Enterprise check if nationality is restricted from all services"""
        return nationality in VisaPolicy.RESTRICTED_COUNTRIES
    
    @staticmethod
    def get_visa_requirements(nationality: str) -> Dict[str, str]:
        """Enterprise visa requirements information"""
        if VisaPolicy.is_restricted(nationality):
            return {
                "status": "RESTRICTED",
                "message": "Visa not available. Please contact embassy.",
                "processing_time": "N/A"
            }
        elif VisaPolicy.check_eligibility(nationality):
            return {
                "status": "ELIGIBLE",
                "message": "Visa on Arrival available",
                "processing_time": "30 minutes"
            }
        else:
            return {
                "status": "EMBASSY_REQUIRED",
                "message": "Please apply at nearest Egyptian consulate",
                "processing_time": "3-5 business days"
            }

class PriceCalculator:
    """Enterprise pricing calculator with dynamic pricing and visitor management"""
    
    @staticmethod
    def calculate_ticket_price(base_price: float, nationality_group: str, visitor_type: str, quantity: int = 1) -> float:
        """Enterprise ticket price calculation with multiple factors"""
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
        """Enterprise visa fee calculation"""
        return config.PRICING["visa_fee"]
    
    @staticmethod
    def get_activation_deposit() -> int:
        """Enterprise activation deposit amount"""
        return config.PRICING["activation_deposit"]
    
    @staticmethod
    def calculate_group_discount(total_price: float, group_size: int) -> float:
        """Enterprise group discount calculation"""
        if group_size >= 10:
            return total_price * 0.8  # 20% discount for groups
        elif group_size >= 5:
            return total_price * 0.9  # 10% discount for small groups
        else:
            return total_price

class EcoEngine:
    """Enterprise environmental impact calculator with advanced scoring"""
    
    @staticmethod
    def calculate_impact(mode: str) -> Tuple[int, str]:
        """Enterprise green points calculation for transport mode"""
        if mode in ["Cairo Monorail", "LRT (Electric Train)", "Electric Bus", "Metro Line 1", "Metro Line 2", "Metro Line 3"]:
            return 20, "🌿 Eco-Friendly"
        elif mode in ["Shared Shuttle", "Train", "Electric Scooter"]:
            return 10, "🍃 Shared Transport"
        elif mode in ["Gas-Powered Taxi", "Private Car", "Online Ride-Hailing"]:
            return 0, "🚗 Private Transport"
        else:
            return 5, "⚡ Mixed Transport"
    
    @staticmethod
    def calculate_carbon_footprint(mode: str, distance_km: float) -> float:
        """Enterprise carbon footprint calculation in kg CO2"""
        footprint_factors = {
            "Cairo Monorail": 0.02,
            "LRT (Electric Train)": 0.03,
            "Electric Bus": 0.04,
            "Metro Line 1": 0.05,
            "Metro Line 2": 0.05,
            "Metro Line 3": 0.05,
            "Gas-Powered Taxi": 0.20,
            "Private Car": 0.25,
            "Online Ride-Hailing": 0.18,
            "Shared Shuttle": 0.08,
            "Train": 0.06
        }
        
        factor = footprint_factors.get(mode, 0.15)
        return factor * distance_km
    
    @staticmethod
    def get_eco_recommendations(current_score: int) -> List[str]:
        """Enterprise eco-friendly recommendations based on current score"""
        recommendations = []
        
        if current_score < 50:
            recommendations.append("🌱 Try using electric transport for +20 points")
            recommendations.append("🚌 Consider shared shuttle services for +10 points")
        elif current_score < 100:
            recommendations.append("🚇 Use Metro Lines for daily commuting")
            recommendations.append("🚴 Consider walking for short distances")
        else:
            recommendations.append("🏆 Excellent eco-score! Keep up the green travel")
            recommendations.append("🌍 Share your eco-friendly travel tips")
        
        return recommendations

class MarketplaceEngine:
    """Enterprise marketplace engine with advanced product management"""
    
    @staticmethod
    def get_esims() -> List[Tuple[str, str, int]]:
        """Enterprise eSIM plans with enhanced features"""
        return [
            ("Orange Egypt Enterprise", "50GB + Unlimited Calls + Priority Support", config.PRICING["esim_orange"]),
            ("Vodafone Business", "40GB + Unlimited Calls + Global Roaming", config.PRICING["esim_vodafone"]),
            ("Etisalat Premium", "60GB + Unlimited Calls + 5G Access", 700),
            ("WE International", "30GB + Unlimited Calls + Airport Lounge", 600)
        ]
    
    @staticmethod
    def get_souvenirs() -> List[Tuple[str, str, int]]:
        """Enterprise souvenir items with premium options"""
        return [
            ("Pharaonic Amulet Gold", "24K Gold-plated Authentic Egyptian Jewelry", 1500),
            ("Papyrus Scroll Deluxe", "Hand-painted Ancient Art with Certificate", 800),
            ("Alabaster Statue Premium", "Large Pyramid Replica with LED Base", 1200),
            ("Egyptian Silk Scarf", "Premium Silk with Traditional Patterns", 400),
            ("Essential Oil Set", "Authentic Egyptian Essential Oils", 300)
        ]
    
    @staticmethod
    def get_transport_cards() -> List[Tuple[str, str, int]]:
        """Unified transport cards for seamless travel across Egypt"""
        return [
            ("Unified Egypt Metro/Bus Card (Physical NFC)", "Physical NFC card for unlimited Metro & Bus access", 150),
            ("Virtual Transit Pass (7-Day)", "Digital pass for 7 days unlimited transit access", 300),
            ("Premium Transit Bundle (30-Day)", "30-day unlimited access + Priority boarding", 800),
            ("Tourist Transit Package", "7-day pass + Airport transfer + City map", 450)
        ]
    
    @staticmethod
    def get_exclusive_offers() -> List[Tuple[str, str]]:
        """Enterprise exclusive offers with enhanced benefits"""
        return [
            ("Pyramids Sunset VIP Tour", "Private guide + Dinner + Transportation", "30% off"),
            ("Nile Dinner Cruise Premium", "VIP deck + Live entertainment + Drinks", "Free upgrade"),
            ("Luxor Temple Priority Access", "Skip-the-line + Private guide + Photography", "Priority entry"),
            ("Red Sea Resort Package", "5-star resort + Activities + Transfers", "25% discount"),
            ("Cairo Food Tour", "Professional guide + 10 tastings + Cultural insights", "20% off")
        ]
    
    @staticmethod
    def get_enterprise_packages() -> List[Tuple[str, str, int]]:
        """Enterprise travel packages for corporate clients"""
        return [
            ("Executive Egypt Tour", "7-day luxury tour with VIP services", 50000),
            ("Corporate Conference Package", "Venue + Accommodation + Activities", 30000),
            ("Team Building Adventure", "Desert safari + Activities + Meals", 15000),
            ("Cultural Immersion Program", "Museum tours + Workshops + Guides", 10000)
        ]

class DocumentIssuer:
    """Enterprise document generation engine with advanced security features"""
    
    @staticmethod
    def generate_visa_pdf(traveler_info: Dict[str, str], stamp: str, data: str) -> str:
        """Generate enterprise visa PDF with enhanced security features"""
        filename = f"visa_{traveler_info['passport']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Try to load fonts, fallback to default if not available
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Enterprise header with security features
        c.setFont(font_name, 16)
        c.drawString(100, 750, "ARAB REPUBLIC OF EGYPT")
        c.drawString(100, 730, "MINISTRY OF FOREIGN AFFAIRS")
        c.drawString(100, 710, "ENTERPRISE VISA SYSTEM")
        
        # Enhanced visa details
        c.setFont(font_name, 12)
        c.drawString(100, 680, f"Visa Number: {stamp}")
        c.drawString(100, 660, f"Name: {traveler_info['full_name']}")
        c.drawString(100, 640, f"Passport: {traveler_info['passport']}")
        c.drawString(100, 620, f"Nationality: {traveler_info['nationality']}")
        c.drawString(100, 600, f"Type: Enterprise Tourist Visa")
        c.drawString(100, 580, f"Valid Until: {datetime.datetime.now() + datetime.timedelta(days=180)}")
        c.drawString(100, 560, f"Issued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Enterprise security watermark
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 400, "EGYPT")
        c.drawString(200, 350, "ENTERPRISE")
        
        # Security features
        c.setFillColorRGB(0.8, 0.8, 0.8)
        c.setFont(font_name, 8)
        c.drawString(400, 100, f"Security Code: {hashlib.md5(stamp.encode()).hexdigest()[:8]}")
        
        c.save()
        return filename
    
    @staticmethod
    def generate_group_ticket_pdf(ticket_info_list: List[Dict[str, any]]) -> str:
        """Generate enterprise group ticket PDF with master QR code and family member list"""
        import random
        
        # Generate unique master ticket ID
        master_id = f"GRP-{random.randint(100000, 999999)}"
        filename = f"group_ticket_{master_id}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Enterprise group ticket header
        c.setFont(font_name, 18)
        c.drawString(100, 750, "EGYPT ENTERPRISE GROUP TICKET")
        c.setFont(font_name, 14)
        c.drawString(100, 730, f"Master Ticket ID: {master_id}")
        
        # Calculate total visitors and price
        total_visitors = sum(ticket['quantity'] for ticket in ticket_info_list)
        total_price = sum(ticket['price'] for ticket in ticket_info_list)
        monument_name = ticket_info_list[0]['monument_name'] if ticket_info_list else "Unknown"
        
        # Group summary
        c.setFont(font_name, 12)
        c.drawString(100, 700, f"Monument: {monument_name}")
        c.drawString(100, 680, f"Total Visitors: {total_visitors}")
        c.drawString(100, 660, f"Total Price: EGP {total_price}")
        c.drawString(100, 640, f"Issued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Visitor breakdown section
        y_position = 600
        c.setFont(font_name, 14, "bold")
        c.drawString(100, y_position, "VISITOR BREAKDOWN:")
        y_position -= 25
        
        c.setFont(font_name, 11)
        for ticket in ticket_info_list:
            visitor_info = f"• {ticket['quantity']} x {ticket['visitor_type']}(s) - EGP {ticket['price']}"
            c.drawString(120, y_position, visitor_info)
            y_position -= 20
            
            # Add individual visitor details if available
            if 'visitor_names' in ticket and ticket['visitor_names']:
                for name in ticket['visitor_names']:
                    c.drawString(140, y_position, f"  - {name}")
                    y_position -= 15
            
            y_position -= 10  # Extra spacing between ticket types
        
        # Master QR Code section
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 600, "MASTER QR CODE")
        c.rect(400, 450, 120, 120)  # QR Code placeholder
        c.setFont(font_name, 10)
        c.drawString(425, 440, "Scan for group entry")
        
        # Enterprise security features
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 300, "GROUP")
        c.drawString(200, 250, "TICKET")
        
        # Security code and validation
        c.setFillColorRGB(0.8, 0.8, 0.8)
        c.setFont(font_name, 8)
        security_code = hashlib.md5(f"{master_id}{total_price}".encode()).hexdigest()[:8]
        c.drawString(400, 100, f"Security Code: {security_code}")
        c.drawString(400, 90, f"Valid for: {monument_name}")
        c.drawString(400, 80, f"Group Size: {total_visitors}")
        
        # Footer
        c.setFillColorRGB(0, 0, 0)
        c.setFont(font_name, 10)
        c.drawString(100, 50, "This ticket admits all listed visitors. Present at entrance for scanning.")
        c.drawString(100, 35, "Unauthorized duplication is prohibited and will result in legal action.")
        
        c.save()
        logger.info(f"✅ Group ticket PDF generated: {filename} for {total_visitors} visitors")
        return filename
    
    @staticmethod
    def generate_transport_card_pdf(card_info: Dict[str, any]) -> str:
        """Generate enterprise transport card PDF with NFC and QR code features"""
        filename = f"transport_card_{card_info['id']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Transport card header
        c.setFont(font_name, 18)
        c.drawString(100, 750, "EGYPT UNIFIED TRANSIT CARD")
        c.setFont(font_name, 14)
        c.drawString(100, 730, f"Card ID: {card_info['id']}")
        
        # Card details
        c.setFont(font_name, 12)
        c.drawString(100, 700, f"Card Type: {card_info['card_name']}")
        c.drawString(100, 680, f"Description: {card_info['description']}")
        c.drawString(100, 660, f"Price: EGP {card_info['price']}")
        c.drawString(100, 640, f"Purchaser: {card_info['purchaser']}")
        c.drawString(100, 620, f"Issued: {card_info['created_at']}")
        
        # Transit access information
        c.setFont(font_name, 12, "bold")
        c.drawString(100, 580, "TRANSIT ACCESS:")
        c.setFont(font_name, 11)
        c.drawString(120, 560, "• Cairo Metro Lines 1, 2, 3")
        c.drawString(120, 545, "• Cairo Monorail System")
        c.drawString(120, 530, "• Public Buses (All Routes)")
        c.drawString(120, 515, "• LRT (Light Rail Transit)")
        
        # QR Code section
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 600, "QR CODE")
        c.rect(400, 500, 100, 100)
        c.setFont(font_name, 10)
        c.drawString(425, 490, "Scan for validation")
        
        # NFC indicator
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 450, "NFC ENABLED")
        c.circle(450, 420, 15, outline="black", width=2)
        c.setFont(font_name, 10)
        c.drawString(425, 395, "Tap at readers")
        
        # Enterprise security features
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 300, "TRANSIT")
        c.drawString(200, 250, "CARD")
        
        # Security code and validation
        c.setFillColorRGB(0.8, 0.8, 0.8)
        c.setFont(font_name, 8)
        security_code = hashlib.md5(f"{card_info['id']}{card_info['price']}".encode()).hexdigest()[:8]
        c.drawString(400, 100, f"Security Code: {security_code}")
        c.drawString(400, 90, f"Valid for: All Egypt Transit")
        c.drawString(400, 80, f"Card Type: {card_info['card_name']}")
        
        # Footer
        c.setFillColorRGB(0, 0, 0)
        c.setFont(font_name, 10)
        c.drawString(100, 50, "This card is valid for unlimited transit access within validity period.")
        c.drawString(100, 35, "Report lost cards immediately. Replacement fees apply.")
        
        c.save()
        logger.info(f"✅ Transport card PDF generated: {filename}")
        return filename
    
    @staticmethod
    def generate_ticket_pdf(ticket_info: Dict[str, any]) -> str:
        """Generate enterprise ticket PDF with QR code"""
        filename = f"ticket_{ticket_info['id']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Ticket header
        c.setFont(font_name, 14)
        c.drawString(100, 750, f"ENTERPRISE TICKET - {ticket_info['monument_name']}")
        
        # Ticket details
        c.setFont(font_name, 12)
        c.drawString(100, 720, f"Ticket ID: {ticket_info['id']}")
        c.drawString(100, 700, f"Visitor Type: {ticket_info['visitor_type']}")
        c.drawString(100, 680, f"Quantity: {ticket_info['quantity']}")
        c.drawString(100, 660, f"Price: EGP {ticket_info['price']}")
        c.drawString(100, 640, f"Date: {ticket_info['created_at']}")
        
        # QR Code placeholder
        c.rect(400, 600, 100, 100)
        c.drawString(425, 580, "QR CODE")
        
        c.save()
        return filename
    
    @staticmethod
    def generate_group_ticket_pdf(ticket_info_list: List[Dict[str, any]]) -> str:
        """Generate enterprise group ticket PDF with master QR code and family member list"""
        import random
        
        # Generate unique master ticket ID
        master_id = f"GRP-{random.randint(100000, 999999)}"
        filename = f"group_ticket_{master_id}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Enterprise group ticket header
        c.setFont(font_name, 18)
        c.drawString(100, 750, "EGYPT ENTERPRISE GROUP TICKET")
        c.setFont(font_name, 14)
        c.drawString(100, 730, f"Master Ticket ID: {master_id}")
        
        # Calculate total visitors and price
        total_visitors = sum(ticket['quantity'] for ticket in ticket_info_list)
        total_price = sum(ticket['price'] for ticket in ticket_info_list)
        monument_name = ticket_info_list[0]['monument_name'] if ticket_info_list else "Unknown"
        
        # Group summary
        c.setFont(font_name, 12)
        c.drawString(100, 700, f"Monument: {monument_name}")
        c.drawString(100, 680, f"Total Visitors: {total_visitors}")
        c.drawString(100, 660, f"Total Price: EGP {total_price}")
        c.drawString(100, 640, f"Issued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Visitor breakdown section
        y_position = 600
        c.setFont(font_name, 14, "bold")
        c.drawString(100, y_position, "VISITOR BREAKDOWN:")
        y_position -= 25
        
        c.setFont(font_name, 11)
        for ticket in ticket_info_list:
            visitor_info = f"• {ticket['quantity']} x {ticket['visitor_type']}(s) - EGP {ticket['price']}"
            c.drawString(120, y_position, visitor_info)
            y_position -= 20
            
            # Add individual visitor details if available
            if 'visitor_names' in ticket and ticket['visitor_names']:
                for name in ticket['visitor_names']:
                    c.drawString(140, y_position, f"  - {name}")
                    y_position -= 15
            
            y_position -= 10  # Extra spacing between ticket types
        
        # Master QR Code section
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 600, "MASTER QR CODE")
        c.rect(400, 450, 120, 120)  # QR Code placeholder
        c.setFont(font_name, 10)
        c.drawString(425, 440, "Scan for group entry")
        
        # Enterprise security features
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 300, "GROUP")
        c.drawString(200, 250, "TICKET")
        
        # Security code and validation
        c.setFillColorRGB(0.8, 0.8, 0.8)
        c.setFont(font_name, 8)
        security_code = hashlib.md5(f"{master_id}{total_price}".encode()).hexdigest()[:8]
        c.drawString(400, 100, f"Security Code: {security_code}")
        c.drawString(400, 90, f"Valid for: {monument_name}")
        c.drawString(400, 80, f"Group Size: {total_visitors}")
        
        # Footer
        c.setFillColorRGB(0, 0, 0)
        c.setFont(font_name, 10)
        c.drawString(100, 50, "This ticket admits all listed visitors. Present at entrance for scanning.")
        c.drawString(100, 35, "Unauthorized duplication is prohibited and will result in legal action.")
        
        c.save()
        logger.info(f"✅ Group ticket PDF generated: {filename} for {total_visitors} visitors")
        return filename
    
    @staticmethod
    def generate_transport_card_pdf(card_info: Dict[str, any]) -> str:
        """Generate enterprise transport card PDF with NFC and QR code features"""
        filename = f"transport_card_{card_info['id']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        try:
            pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
            font_name = "Arial"
        except:
            font_name = "Helvetica"
        
        # Transport card header
        c.setFont(font_name, 18)
        c.drawString(100, 750, "EGYPT UNIFIED TRANSIT CARD")
        c.setFont(font_name, 14)
        c.drawString(100, 730, f"Card ID: {card_info['id']}")
        
        # Card details
        c.setFont(font_name, 12)
        c.drawString(100, 700, f"Card Type: {card_info['card_name']}")
        c.drawString(100, 680, f"Description: {card_info['description']}")
        c.drawString(100, 660, f"Price: EGP {card_info['price']}")
        c.drawString(100, 640, f"Purchaser: {card_info['purchaser']}")
        c.drawString(100, 620, f"Issued: {card_info['created_at']}")
        
        # Transit access information
        c.setFont(font_name, 12, "bold")
        c.drawString(100, 580, "TRANSIT ACCESS:")
        c.setFont(font_name, 11)
        c.drawString(120, 560, "• Cairo Metro Lines 1, 2, 3")
        c.drawString(120, 545, "• Cairo Monorail System")
        c.drawString(120, 530, "• Public Buses (All Routes)")
        c.drawString(120, 515, "• LRT (Light Rail Transit)")
        
        # QR Code section
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 600, "QR CODE")
        c.rect(400, 500, 100, 100)
        c.setFont(font_name, 10)
        c.drawString(425, 490, "Scan for validation")
        
        # NFC indicator
        c.setFont(font_name, 12, "bold")
        c.drawString(400, 450, "NFC ENABLED")
        c.circle(450, 420, 15, outline="black", width=2)
        c.setFont(font_name, 10)
        c.drawString(425, 395, "Tap at readers")
        
        # Enterprise security features
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setFont(font_name, 48)
        c.drawString(200, 300, "TRANSIT")
        c.drawString(200, 250, "CARD")
        
        # Security code and validation
        c.setFillColorRGB(0.8, 0.8, 0.8)
        c.setFont(font_name, 8)
        security_code = hashlib.md5(f"{card_info['id']}{card_info['price']}".encode()).hexdigest()[:8]
        c.drawString(400, 100, f"Security Code: {security_code}")
        c.drawString(400, 90, f"Valid for: All Egypt Transit")
        c.drawString(400, 80, f"Card Type: {card_info['card_name']}")
        
        # Footer
        c.setFillColorRGB(0, 0, 0)
        c.setFont(font_name, 10)
        c.drawString(100, 50, "This card is valid for unlimited transit access within validity period.")
        c.drawString(100, 35, "Report lost cards immediately. Replacement fees apply.")
        
        c.save()
        logger.info(f"✅ Transport card PDF generated: {filename}")
        return filename

# ==============================================================================
# 🧠 PROCEDURE DOC 1030 COMPLIANCE - ARRIVAL LOGIC ENGINE
# ==============================================================================

class ArrivalLogic:
    """Procedure Doc 1030 compliance engine for arrival card validation"""
    
    @staticmethod
    def validate_submission_time(arrival_date_str: str, is_demo_user: bool = False) -> bool:
        """
        Validate that arrival card is submitted at least 72 hours prior to arrival
        Demo users bypass the 72-hour rule for testing purposes
        
        Args:
            arrival_date_str: Arrival date string in YYYY-MM-DD format
            is_demo_user: Boolean indicating if this is a demo user
            
        Returns:
            True if submission is valid (>= 72 hours before arrival) or demo user, False otherwise
        """
        # Demo users bypass the 72-hour rule
        if is_demo_user:
            logger.info("🔍 Demo user detected - bypassing 72-hour arrival validation")
            return True
            
        try:
            from datetime import datetime, timedelta
            
            # Parse arrival date
            arrival_date = datetime.strptime(arrival_date_str.strip(), '%Y-%m-%d')
            current_time = datetime.now()
            
            # Calculate time difference
            time_difference = arrival_date - current_time
            hours_until_arrival = time_difference.total_seconds() / 3600
            
            # Check if submission is at least 72 hours before arrival
            is_valid = hours_until_arrival >= 72
            
            logger.info(f"🔍 Arrival validation: {arrival_date_str} - {hours_until_arrival:.1f} hours until arrival - Valid: {is_valid}")
            
            return is_valid
            
        except ValueError as e:
            logger.error(f"❌ Invalid date format in arrival validation: {arrival_date_str} - {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error in arrival validation: {e}")
            return False
    
    @staticmethod
    def get_validation_message(arrival_date_str: str, is_demo_user: bool = False) -> str:
        """
        Get detailed validation message for arrival card submission
        Demo users receive special bypass message
        
        Args:
            arrival_date_str: Arrival date string in YYYY-MM-DD format
            is_demo_user: Boolean indicating if this is a demo user
            
        Returns:
            Validation message with details
        """
        # Demo users bypass validation
        if is_demo_user:
            return "✅ DEMO MODE: Arrival card accepted (72-hour rule bypassed for testing)"
            
        try:
            from datetime import datetime, timedelta
            
            # Parse arrival date
            arrival_date = datetime.strptime(arrival_date_str.strip(), '%Y-%m-%d')
            current_time = datetime.now()
            
            # Calculate time difference
            time_difference = arrival_date - current_time
            hours_until_arrival = time_difference.total_seconds() / 3600
            days_until_arrival = hours_until_arrival / 24
            
            if hours_until_arrival >= 72:
                return f"✅ ARRIVAL CARD ACCEPTED: Submitted {days_until_arrival:.1f} days before arrival (meets 72-hour requirement)"
            else:
                return f"❌ ARRIVAL CARD REJECTED: Must be submitted 72 hours prior to arrival. Only {hours_until_arrival:.1f} hours remaining."
                
        except ValueError:
            return "❌ INVALID DATE FORMAT: Please use YYYY-MM-DD format"
        except Exception as e:
            return f"❌ VALIDATION ERROR: {e}"

# ==============================================================================
# 🗄️ ENTERPRISE DATABASE LAYER - DEEP DATA COMPLIANCE
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
        if not hasattr(self, 'initialized'):
            self.conn = sqlite3.connect(HorusConfig.DB_NAME, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self._init_schema()
            self.initialized = True
    
    def _init_schema(self):
        """Initialize enterprise database schema with deep data fields"""
        # Drop existing tables for clean migration
        self.cursor.execute("DROP TABLE IF EXISTS travelers")
        self.cursor.execute("DROP TABLE IF EXISTS tickets")
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute("DROP TABLE IF EXISTS monuments")
        self.cursor.execute("DROP TABLE IF EXISTS visas")
        self.cursor.execute("DROP TABLE IF EXISTS enterprise_packages")
        self.cursor.execute("DROP TABLE IF EXISTS ai_interactions")
        
        # Updated travelers table with DEEP DATA fields (19 total)
        self.cursor.execute('''
            CREATE TABLE travelers (\n                id INTEGER PRIMARY KEY, \n                name TEXT, \n                full_name TEXT,\n                passport_number TEXT UNIQUE, \n                nationality TEXT,\n                nationality_group TEXT,\n                passport_expiry TEXT,\n                biometric_hash TEXT, \n                wallet_balance REAL DEFAULT 0, \n                wallet_status TEXT DEFAULT 'LOCKED',\n                bank_linked BOOLEAN DEFAULT 0,\n                green_points INTEGER DEFAULT 0, \n                has_claimed_gift BOOLEAN DEFAULT 0,\n                created_at TEXT,\n                -- ALL 19 DEEP DATA FIELDS (2026 Procedure Compliance)\n                dob TEXT,\n                gender TEXT,\n                phone TEXT,\n                email TEXT,\n                arrival_date TEXT,\n                country_boarded TEXT,\n                flight_number TEXT,\n                mode_of_arrival TEXT,\n                departure_date TEXT,\n                country_residence TEXT,\n                visa_no TEXT,\n                issued_by TEXT,\n                accommodation_type TEXT,\n                accommodation_address TEXT,\n                occupation TEXT,\n                purpose_of_travel TEXT,\n                passport_issue_date TEXT,\n                transport_mode TEXT,\n                departure_mode TEXT,\n                departure_flight_number TEXT
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
                qr_hash TEXT,
                status TEXT DEFAULT 'ACTIVE',
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
                payment_method TEXT,
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
                google_maps_link TEXT,
                opening_hours TEXT,
                accessibility_info TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE visas (
                id INTEGER PRIMARY KEY,
                traveler_id INTEGER,
                stamp TEXT UNIQUE,
                status TEXT DEFAULT 'ACTIVE',
                issued_at TEXT,
                expires_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE enterprise_packages (
                id INTEGER PRIMARY KEY,
                package_name TEXT,
                description TEXT,
                price REAL,
                duration_days INTEGER,
                features TEXT,
                created_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE ai_interactions (
                id INTEGER PRIMARY KEY,
                traveler_id INTEGER,
                question TEXT,
                response TEXT,
                category TEXT,
                created_at TEXT
            )
        ''')
        
        # Seed monuments with enhanced information
        monuments_data = [
            ("Great Pyramid", "The last surviving Wonder of the Ancient World", 600, "Giza Plateau, Egypt", "https://maps.google.com/?q=Great+Pyramid+Giza", "8:00-17:00", "Wheelchair accessible"),
            ("Karnak Temple", "Largest ancient religious site in the world", 400, "Luxor, Egypt", "https://maps.google.com/?q=Karnak+Temple+Luxor", "6:00-18:00", "Partial accessibility"),
            ("GEM Museum", "Grand Egyptian Museum - Home to Tutankhamun treasures", 300, "Giza, Egypt", "https://maps.google.com/?q=Grand+Egyptian+Museum", "9:00-17:00", "Fully accessible"),
            ("Valley of Kings", "Royal burial ground of pharaohs", 350, "Luxor, Egypt", "https://maps.google.com/?q=Valley+of+Kings+Luxor", "6:00-17:00", "Limited accessibility"),
            ("Abu Simbel", "Massive rock temples built by Ramesses II", 450, "Aswan, Egypt", "https://maps.google.com/?q=Abu+Simbel+Aswan", "7:00-17:00", "Wheelchair accessible")
        ]
        
        self.cursor.executemany('''
            INSERT INTO monuments (name, description, base_price_foreigner, location, google_maps_link, opening_hours, accessibility_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', monuments_data)
        
        # Seed enterprise packages
        packages_data = [
            ("Executive Egypt Tour", "7-day luxury tour with VIP services", 50000, 7, "Private guide, 5-star hotels, VIP transport, exclusive access"),
            ("Corporate Conference Package", "Complete conference organization", 30000, 3, "Venue booking, accommodation, activities, catering"),
            ("Team Building Adventure", "Desert safari with team activities", 15000, 2, "Desert safari, team activities, meals, transport"),
            ("Cultural Immersion Program", "Deep cultural experience", 10000, 5, "Museum tours, workshops, cultural guides")
        ]
        
        self.cursor.executemany('''
            INSERT INTO enterprise_packages (package_name, description, price, duration_days, features, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [(pkg[0], pkg[1], pkg[2], pkg[3], pkg[4], datetime.datetime.now().isoformat()) for pkg in packages_data])
        
        self.conn.commit()
        logger.info("Enterprise database schema initialized with deep data fields")
    
    def register_traveler(
        self, 
        name, 
        full_name, 
        passport, 
        nationality, 
        nationality_group, 
        expiry, 
        bio_hash, 
        dob, 
        gender, 
        phone, 
        email, 
        arrival_date, 
        country_boarded, 
        flight_number, 
        mode_of_arrival, 
        departure_date, 
        country_residence, 
        visa_no, 
        issued_by, 
        accommodation_type, 
        accommodation_address, 
        occupation, 
        purpose_of_travel,
        passport_issue_date=None,
        transport_mode=None,
        departure_mode=None,
        departure_flight_number=None
    ):
        """Register traveler with deep data fields and Procedure Doc 1030 compliance"""
        sql = '''INSERT INTO travelers (
            name, full_name, passport_number, nationality, nationality_group, 
            passport_expiry, biometric_hash, wallet_balance, wallet_status, bank_linked, green_points, has_claimed_gift, created_at,
            dob, gender, phone, email, arrival_date, country_boarded, flight_number, mode_of_arrival, 
            departure_date, country_residence, visa_no, issued_by, accommodation_type, accommodation_address, occupation, 
            purpose_of_travel, passport_issue_date, transport_mode, departure_mode, departure_flight_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        params = (
            name,
            full_name,
            passport,
            nationality,
            nationality_group,
            expiry,
            bio_hash,
            0,  # wallet_balance
            'LOCKED',  # wallet_status
            0,  # bank_linked
            0,  # green_points
            0,  # has_claimed_gift
            datetime.datetime.now().isoformat(),  # created_at
            dob,
            gender,
            phone,
            email,
            arrival_date,
            country_boarded,
            flight_number,
            mode_of_arrival,
            departure_date,
            country_residence,
            visa_no,
            issued_by,
            accommodation_type,
            accommodation_address,
            occupation,
            purpose_of_travel,
            passport_issue_date,
            transport_mode,
            departure_mode,
            departure_flight_number
        )
        
        self.cursor.execute(sql, params)
        self.conn.commit()
        logger.info(f"Enterprise traveler registered: {name} with Procedure Doc 1030 compliance")
        return self.cursor.lastrowid
    
    def get_traveler(self, tid):
        """Get traveler information by ID"""
        self.cursor.execute("SELECT * FROM travelers WHERE id=?", (tid,))
        return self.cursor.fetchone()
    
    def activate_wallet(self, tid, card_number):
        """Activate wallet with $200 USD deposit and enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_status='ACTIVE', wallet_balance=?, bank_linked=1 WHERE id=?", 
                              (config.PRICING["activation_deposit"], tid))
            self.conn.commit()
            logger.info(f"Enterprise wallet activated for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise wallet activation failed: {e}")
            return False
    
    def top_up(self, tid, amount):
        """Add funds to wallet with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance+? WHERE id=?", (amount, tid))
            self.conn.commit()
            logger.info(f"Enterprise wallet topped up: {amount} EGP for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise wallet top-up failed: {e}")
            return False
    
    def purchase(self, tid, description, amount, category, payment_method="WALLET"):
        """Process purchase transaction with comprehensive enterprise logging"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and traveler[8] >= amount:  # wallet_balance check
                self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance-? WHERE id=?", (amount, tid))
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, payment_method, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                  (tid, description, amount, category, payment_method, datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Enterprise purchase processed: {description} - {amount} EGP for traveler {tid}")
                return True
            else:
                logger.warning(f"Enterprise insufficient funds for traveler {tid}: balance={traveler[8] if traveler else 0}, required={amount}")
                return False
        except Exception as e:
            logger.error(f"Enterprise purchase processing failed: {e}")
            return False
    
    def create_ticket(self, traveler_id, monument_name, visitor_type, quantity, price):
        """Create ticket record with QR hash and enterprise logging"""
        try:
            qr_hash = hashlib.sha256(f"{traveler_id}{monument_name}{datetime.datetime.now()}".encode()).hexdigest()
            self.cursor.execute('''
                INSERT INTO tickets (traveler_id, monument_name, visitor_type, quantity, price, qr_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (traveler_id, monument_name, visitor_type, quantity, price, qr_hash, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise ticket created: {monument_name} - {quantity} {visitor_type} for traveler {traveler_id}")
            return True
        except Exception as e:
            logger.error(f"Enterprise ticket creation failed: {e}")
            return False
    
    def add_green_points(self, tid, points):
        """Add green points to traveler with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET green_points=green_points+? WHERE id=?", (points, tid))
            self.conn.commit()
            logger.info(f"Enterprise green points added: {points} points for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise green points addition failed: {e}")
            return False
    
    def claim_gift(self, tid):
        """Claim welcome gift with enterprise logging and status tracking"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and not traveler[12]:  # has_claimed_gift is at index 12
                self.cursor.execute("UPDATE travelers SET has_claimed_gift = 1 WHERE id=?", (tid,))
                # Log gift transaction
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, payment_method, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                  (tid, "Enterprise Welcome Gift Claimed", 0, "GIFT", "SYSTEM", datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Enterprise welcome gift claimed for traveler {tid}")
                return True
            else:
                logger.warning(f"Enterprise gift claim failed for traveler {tid}: already claimed or not found")
                return False
        except Exception as e:
            logger.error(f"Enterprise gift claim failed: {e}")
            return False
    
    def link_bank(self, tid, bank_name):
        """Link bank account to traveler with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET bank_linked=1 WHERE id=?", (tid,))
            self.conn.commit()
            logger.info(f"Enterprise bank linked: {bank_name} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise bank linking failed: {e}")
            return False
    
    def add_visa(self, tid, stamp):
        """Add visa record with enterprise logging"""
        try:
            expires_at = datetime.datetime.now() + datetime.timedelta(days=180)
            self.cursor.execute("INSERT INTO visas (traveler_id, stamp, issued_at, expires_at) VALUES (?, ?, ?, ?)",
                              (tid, stamp, datetime.datetime.now().isoformat(), expires_at.isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise visa added: {stamp} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise visa addition failed: {e}")
            return False
    
    def log_ai_interaction(self, tid, question, response, category):
        """Log AI interaction for enterprise analytics"""
        try:
            self.cursor.execute('''
                INSERT INTO ai_interactions (traveler_id, question, response, category, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (tid, question, response, category, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise AI interaction logged for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise AI interaction logging failed: {e}")
            return False
    
    def get_data(self, table):
        """Generic data retrieval with enterprise error handling"""
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Enterprise data retrieval failed for table {table}: {e}")
            return []
    
    def get_system_stats(self):
        """Get comprehensive enterprise system statistics"""
        try:
            stats = {}
            stats['total_travelers'] = self.cursor.execute("SELECT COUNT(*) FROM travelers").fetchone()[0]
            stats['active_wallets'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE wallet_status='ACTIVE'").fetchone()[0]
            stats['total_transactions'] = self.cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            stats['total_visas'] = self.cursor.execute("SELECT COUNT(*) FROM visas").fetchone()[0]
            stats['gifts_claimed'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE has_claimed_gift=1").fetchone()[0]
            stats['total_tickets'] = self.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            stats['ai_interactions'] = self.cursor.execute("SELECT COUNT(*) FROM ai_interactions").fetchone()[0]
            stats['enterprise_packages'] = self.cursor.execute("SELECT COUNT(*) FROM enterprise_packages").fetchone()[0]
            return stats
        except Exception as e:
            logger.error(f"Enterprise system stats retrieval failed: {e}")
            return {}
    
    def get_enterprise_analytics(self):
        """Get enterprise analytics for business intelligence"""
        try:
            analytics = {}
            
            # Revenue analytics
            analytics['total_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions").fetchone()[0] or 0
            analytics['visa_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='GOVT'").fetchone()[0] or 0
            analytics['transport_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='TRANSPORT'").fetchone()[0] or 0
            analytics['monument_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='MONUMENTS'").fetchone()[0] or 0
            
            # User analytics
            analytics['avg_wallet_balance'] = self.cursor.execute("SELECT AVG(wallet_balance) FROM travelers WHERE wallet_status='ACTIVE'").fetchone()[0] or 0
            analytics['avg_green_points'] = self.cursor.execute("SELECT AVG(green_points) FROM travelers").fetchone()[0] or 0
            stats = self.get_system_stats()
            analytics['gift_claim_rate'] = (stats['gifts_claimed'] / stats['total_travelers'] * 100) if stats['total_travelers'] > 0 else 0
            
            # Popular destinations
            analytics['top_monuments'] = self.cursor.execute('''
                SELECT monument_name, COUNT(*) as visits 
                FROM tickets 
                GROUP BY monument_name 
                ORDER BY visits DESC 
                LIMIT 5
            ''').fetchall()
            
            return analytics
        except Exception as e:
            logger.error(f"Enterprise analytics retrieval failed: {e}")
            return {}

# ==============================================================================
        return self.cursor.fetchone()
    
    def activate_wallet(self, tid, card_number):
        """Activate wallet with $200 USD deposit and enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_status='ACTIVE', wallet_balance=?, bank_linked=1 WHERE id=?", 
                              (config.PRICING["activation_deposit"], tid))
            self.conn.commit()
            logger.info(f"Enterprise wallet activated for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise wallet activation failed: {e}")
            return False
    
    def top_up(self, tid, amount):
        """Add funds to wallet with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance+? WHERE id=?", (amount, tid))
            self.conn.commit()
            logger.info(f"Enterprise wallet topped up: {amount} EGP for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise wallet top-up failed: {e}")
            return False
    
    def purchase(self, tid, description, amount, category, payment_method="WALLET"):
        """Process purchase transaction with comprehensive enterprise logging"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and traveler[8] >= amount:  # wallet_balance check
                self.cursor.execute("UPDATE travelers SET wallet_balance=wallet_balance-? WHERE id=?", (amount, tid))
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, payment_method, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                  (tid, description, amount, category, payment_method, datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Enterprise purchase processed: {description} - {amount} EGP for traveler {tid}")
                return True
            else:
                logger.warning(f"Enterprise insufficient funds for traveler {tid}: balance={traveler[8] if traveler else 0}, required={amount}")
                return False
        except Exception as e:
            logger.error(f"Enterprise purchase processing failed: {e}")
            return False
    
    def create_ticket(self, traveler_id, monument_name, visitor_type, quantity, price):
        """Create ticket record with QR hash and enterprise logging"""
        try:
            qr_hash = hashlib.sha256(f"{traveler_id}{monument_name}{datetime.datetime.now()}".encode()).hexdigest()
            self.cursor.execute('''
                INSERT INTO tickets (traveler_id, monument_name, visitor_type, quantity, price, qr_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (traveler_id, monument_name, visitor_type, quantity, price, qr_hash, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise ticket created: {monument_name} - {quantity} {visitor_type} for traveler {traveler_id}")
            return True
        except Exception as e:
            logger.error(f"Enterprise ticket creation failed: {e}")
            return False
    
    def add_green_points(self, tid, points):
        """Add green points to traveler with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET green_points=green_points+? WHERE id=?", (points, tid))
            self.conn.commit()
            logger.info(f"Enterprise green points added: {points} points for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise green points addition failed: {e}")
            return False
    
    def claim_gift(self, tid):
        """Claim welcome gift with enterprise logging and status tracking"""
        try:
            traveler = self.get_traveler(tid)
            if traveler and not traveler[12]:  # has_claimed_gift is at index 12
                self.cursor.execute("UPDATE travelers SET has_claimed_gift = 1 WHERE id=?", (tid,))
                # Log gift transaction
                self.cursor.execute("INSERT INTO transactions (traveler_id, description, amount, category, payment_method, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                  (tid, "Enterprise Welcome Gift Claimed", 0, "GIFT", "SYSTEM", datetime.datetime.now().isoformat()))
                self.conn.commit()
                logger.info(f"Enterprise welcome gift claimed for traveler {tid}")
                return True
            else:
                logger.warning(f"Enterprise gift claim failed for traveler {tid}: already claimed or not found")
                return False
        except Exception as e:
            logger.error(f"Enterprise gift claim failed: {e}")
            return False
    
    def link_bank(self, tid, bank_name):
        """Link bank account to traveler with enterprise logging"""
        try:
            self.cursor.execute("UPDATE travelers SET bank_linked=1 WHERE id=?", (tid,))
            self.conn.commit()
            logger.info(f"Enterprise bank linked: {bank_name} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise bank linking failed: {e}")
            return False
    
    def add_visa(self, tid, stamp):
        """Add visa record with enterprise logging"""
        try:
            expires_at = datetime.datetime.now() + datetime.timedelta(days=180)
            self.cursor.execute("INSERT INTO visas (traveler_id, stamp, issued_at, expires_at) VALUES (?, ?, ?, ?)",
                              (tid, stamp, datetime.datetime.now().isoformat(), expires_at.isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise visa added: {stamp} for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise visa addition failed: {e}")
            return False
    
    def log_ai_interaction(self, tid, question, response, category):
        """Log AI interaction for enterprise analytics"""
        try:
            self.cursor.execute('''
                INSERT INTO ai_interactions (traveler_id, question, response, category, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (tid, question, response, category, datetime.datetime.now().isoformat()))
            self.conn.commit()
            logger.info(f"Enterprise AI interaction logged for traveler {tid}")
            return True
        except Exception as e:
            logger.error(f"Enterprise AI interaction logging failed: {e}")
            return False
    
    def get_data(self, table):
        """Generic data retrieval with enterprise error handling"""
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Enterprise data retrieval failed for table {table}: {e}")
            return []
    
    def get_system_stats(self):
        """Get comprehensive enterprise system statistics"""
        try:
            stats = {}
            stats['total_travelers'] = self.cursor.execute("SELECT COUNT(*) FROM travelers").fetchone()[0]
            stats['active_wallets'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE wallet_status='ACTIVE'").fetchone()[0]
            stats['total_transactions'] = self.cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            stats['total_visas'] = self.cursor.execute("SELECT COUNT(*) FROM visas").fetchone()[0]
            stats['gifts_claimed'] = self.cursor.execute("SELECT COUNT(*) FROM travelers WHERE has_claimed_gift=1").fetchone()[0]
            stats['total_tickets'] = self.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            stats['ai_interactions'] = self.cursor.execute("SELECT COUNT(*) FROM ai_interactions").fetchone()[0]
            stats['enterprise_packages'] = self.cursor.execute("SELECT COUNT(*) FROM enterprise_packages").fetchone()[0]
            return stats
        except Exception as e:
            logger.error(f"Enterprise system stats retrieval failed: {e}")
            return {}
    
    def get_enterprise_analytics(self):
        """Get enterprise analytics for business intelligence"""
        try:
            analytics = {}
            
            # Revenue analytics
            analytics['total_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions").fetchone()[0] or 0
            analytics['visa_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='GOVT'").fetchone()[0] or 0
            analytics['transport_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='TRANSPORT'").fetchone()[0] or 0
            analytics['monument_revenue'] = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category='MONUMENTS'").fetchone()[0] or 0
            
            # User analytics
            analytics['avg_wallet_balance'] = self.cursor.execute("SELECT AVG(wallet_balance) FROM travelers WHERE wallet_status='ACTIVE'").fetchone()[0] or 0
            analytics['avg_green_points'] = self.cursor.execute("SELECT AVG(green_points) FROM travelers").fetchone()[0] or 0
            analytics['gift_claim_rate'] = (stats['gifts_claimed'] / stats['total_travelers'] * 100) if stats['total_travelers'] > 0 else 0
            
            # Popular destinations
            analytics['top_monuments'] = self.cursor.execute('''
                SELECT monument_name, COUNT(*) as visits 
                FROM tickets 
                GROUP BY monument_name 
                ORDER BY visits DESC 
                LIMIT 5
            ''').fetchall()
            
            return analytics
        except Exception as e:
            logger.error(f"Enterprise analytics retrieval failed: {e}")
            return {}

# ==============================================================================
# 🤖 ENTERPRISE GIT AUTOPILOT & AI SERVICES
# ==============================================================================

class GitAutopilot:
    """Enterprise automated Git repository management with comprehensive logging"""
    
    @staticmethod
    def sync_codebase():
        """Sync codebase to GitHub repository with enterprise error handling"""
        try:
            # Initialize git repository if not exists
            if not os.path.exists(".git"):
                logger.info("Initializing Enterprise Git repository...")
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
            commit_msg = f"HORUS v{HorusConfig.VERSION} - Enterprise Auto-sync {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            logger.info(f"Committing changes: {commit_msg}")
            os.system(f'git commit -m "{commit_msg}"')
            
            # Push to remote (if configured)
            # os.system("git push origin main")
            
            logger.info(f"Enterprise code synced successfully. Commit: {commit_msg}")
            return f"✅ Enterprise code synced successfully. Commit: {commit_msg}"
        except Exception as e:
            logger.error(f"Enterprise Git sync failed: {str(e)}")
            return f"❌ Sync failed: {str(e)}"

# Global key rotation counter for enterprise load balancing
_key_rotation_counter = 0

def get_rotated_key():
    """Get API key with enterprise rotation logic using hardcoded keys"""
    global _key_rotation_counter
    
    # Use hardcoded keys from config
    keys = config.GEMINI_KEYS
    logger.info(f"DEBUG: Using {len(keys)} hardcoded AI keys.")
    
    if not keys or not keys[0] or (len(keys) == 1 and not keys[0].strip()):
        logger.error("❌ No GEMINI_KEYS found in Colab secrets or environment variables")
        logger.info("💡 In Colab: Add GEMINI_KEYS to secrets (comma-separated for multiple keys)")
        logger.info("💡 Locally: Set environment variable: export GEMINI_KEYS='key1,key2,key3'")
        return None
    
    # Filter out empty keys and strip whitespace
    valid_keys = [key.strip() for key in keys if key.strip()]
    logger.info(f"DEBUG: Found {len(valid_keys)} valid AI keys after filtering.")
    
    if not valid_keys:
        logger.error("❌ No valid API keys found after filtering")
        return None
    
    # Validate key format (Gemini keys are typically 39 characters starting with 'AIza')
    for key in valid_keys[:]:  # Use slice to avoid modifying list during iteration
        if not key.startswith('AIza') or len(key) < 20:
            logger.warning(f"⚠️ Invalid Gemini API key format: {key[:10]}...")
            valid_keys.remove(key)
    
    if not valid_keys:
        logger.error("❌ No valid Gemini API keys found (should start with 'AIza')")
        return None
    
    # Enterprise rotation strategy: Use random choice with fallback to round-robin
    try:
        # Primary strategy: Random selection for load distribution
        selected_key = random.choice(valid_keys)
        _key_rotation_counter += 1
        
        logger.info(f"🔑 Enterprise AI key rotation: Using key {_key_rotation_counter % len(valid_keys) + 1}/{len(valid_keys)}")
        logger.info(f"🔑 Key format valid: {selected_key[:10]}...{selected_key[-4:]}")
        return selected_key
    except Exception as e:
        logger.error(f"❌ Key rotation error: {e}")
        # Fallback to first key
        return valid_keys[0]

def ask_ai(msg, history):
    """Enterprise AI chat interface with multi-model fallback chain (3.6 -> 3.5 -> 3.0 -> 2.5)"""
    if not config.AI_ENABLED:
        return "⚠️ Enterprise AI Chat is not available. Please install google-genai package."
    
    key = get_rotated_key()
    if not key: 
        return "⚠️ Configuration Error: Please set GEMINI_KEYS environment variable with your API key."
    
    client = genai.Client(api_key=key)
    models_to_try = [config.AI_MODEL] + [m for m in getattr(config, 'AI_FALLBACK_MODELS', ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3-flash-preview", "gemini-2.5-flash"]) if m != config.AI_MODEL]
    
    last_error = None
    for model_name in models_to_try:
        try:
            res = client.models.generate_content(
                model=model_name, 
                contents=msg
            )
            logger.info(f"Enterprise AI response generated using {model_name} for message: {msg[:50]}...")
            return res.text
        except Exception as e:
            logger.warning(f"⚠️ Model {model_name} failed: {e}. Trying next fallback model...")
            last_error = e
            
    logger.error(f"Enterprise AI chat error across all models: {last_error}")
    return f"AI Error (All models exhausted): {last_error}"

# ==============================================================================
# 📱 ENTERPRISE UI (PLATINUM DASHBOARD) - ENHANCED WITH SELF-HEALING
# ==============================================================================

current_user = None

def ui_login(image, passport, nationality, full_name, passport_expiry, occupation, purpose_of_travel, accommodation_address, dob, gender, phone, arrival_date, country_boarded, flight_number, mode_of_arrival, departure_date, passport_issue_date, transport_mode, accommodation_type, departure_mode, departure_flight, visa_no, issued_by):
    """Enterprise login with Procedure Doc 1030 compliance and 72-hour validation"""
    global current_user
    
    # Check if this is a demo login (bypass 72-hour rule)
    is_demo_user = full_name.strip().lower() == "demo user"
    
    # CRITICAL FIX: Check for None image first
    if image is None:
        return "⚠️ Waiting for biometric scan...", gr.update(), gr.update(), "", "", ""
    
    # Robust numpy check
    if not isinstance(image, np.ndarray):
        return "❌ HARDWARE ERROR: WEBCAM DATA INVALID", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Full Name regex (letters, spaces, hyphens only)
    import re
    if not re.match(r'^[a-zA-Z\s\-]+$', full_name.strip()):
        return "❌ INVALID FULL NAME: Use letters, spaces, and hyphens only", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Passport Number regex (alphanumeric)
    if not re.match(r'^[A-Za-z0-9]+$', passport.strip()):
        return "❌ INVALID PASSPORT: Use letters and numbers only", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Passport Expiry regex (YYYY-MM-DD format)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', passport_expiry.strip()):
        return "❌ INVALID PASSPORT EXPIRY: Use YYYY-MM-DD format", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Date of Birth regex (YYYY-MM-DD format)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob.strip()):
        return "❌ INVALID DATE OF BIRTH: Use YYYY-MM-DD format", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Phone regex (international format)
    if not re.match(r'^\+?[1-9]\d{1,14}$', phone.strip().replace(' ', '').replace('-', '')):
        return "❌ INVALID PHONE: Use international format (e.g., +20123456789)", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Arrival Date regex (YYYY-MM-DD format)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', arrival_date.strip()):
        return "❌ INVALID ARRIVAL DATE: Use YYYY-MM-DD format", gr.update(), gr.update(), "", "", ""
    
    # STRICT VALIDATION: Departure Date regex (YYYY-MM-DD format)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', departure_date.strip()):
        return "❌ INVALID DEPARTURE DATE: Use YYYY-MM-DD format", gr.update(), gr.update(), "", "", ""
    
    # Additional validation: Check if passport expiry is in the future
    try:
        from datetime import datetime
        expiry_date = datetime.strptime(passport_expiry.strip(), '%Y-%m-%d')
        if expiry_date <= datetime.now():
            return "❌ PASSPORT EXPIRED: Passport must be valid for future travel", gr.update(), gr.update(), "", "", ""
    except ValueError:
        return "❌ INVALID DATE: Check passport expiry format", gr.update(), gr.update(), "", "", ""
    
    # PROCEDURE DOC 1030 COMPLIANCE: 72-hour validation (bypass for demo users)
    if not ArrivalLogic.validate_submission_time(arrival_date.strip(), is_demo_user):
        validation_message = ArrivalLogic.get_validation_message(arrival_date.strip(), is_demo_user)
        return f"❌ {validation_message}", gr.update(), gr.update(), "", "", ""
    
    bio_hash = HorusSecurity.scan_face(image)
    if not bio_hash:
        return "❌ BIOMETRIC SCAN FAILED", gr.update(), gr.update(), "", "", ""

    nationality_group = VisaPolicy.get_nationality_group(nationality)
    name = f"Traveler-{nationality[:3].upper()}-{passport[-4:]}"
    
    # Register with PROCEDURE DOC 1030 COMPLIANCE fields (all validated)
    uid = db.register_traveler(
        name, 
        full_name.strip(), 
        passport.strip(), 
        nationality, 
        nationality_group, 
        passport_expiry.strip(), 
        bio_hash, 
        dob.strip(),
        gender.strip(),
        phone.strip(),
        "traveler@horus.com",  # email
        arrival_date.strip(),
        country_boarded.strip(),
        flight_number.strip(),
        mode_of_arrival.strip(),
        departure_date.strip(),
        country_boarded.strip(),  # country_residence
        visa_no.strip() if visa_no else "TBD",  # visa_no
        issued_by.strip() if issued_by else "TBD",  # issued_by
        accommodation_type.strip() if accommodation_type else "Hotel",  # accommodation_type
        accommodation_address.strip(),  # accommodation_address
        occupation.strip(),  # occupation
        purpose_of_travel.strip(),  # purpose_of_travel
        passport_issue_date.strip() if passport_issue_date else "TBD",  # passport_issue_date
        transport_mode.strip() if transport_mode else "Commercial",  # transport_mode
        departure_mode.strip() if departure_mode else "Air",  # departure_mode
        departure_flight.strip() if departure_flight else "TBD"  # departure_flight_number
    )
    current_user = db.get_traveler(uid)
    
    wallet_status = current_user[9]
    wallet_balance = current_user[8]
    green_points = current_user[11]
    
    if wallet_status == 'LOCKED':
        return (
            f"✅ Verified: {name} - WALLET LOCKED",
            gr.Group(visible=False),  # Hide main app
            gr.Group(visible=True),   # Show activation panel
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "🔒 ACCOUNT LOCKED - Deposit $200 USD to activate",
            "",  # QR input placeholder
            gr.update(visible=False),  # Hide demo badge
            gr.update(visible=True)    # Show quick wallet button
        )
    else:
        return (
            f"✅ Verified: {name} - ACCOUNT ACTIVE",
            gr.Group(visible=True),   # Show main app
            gr.Group(visible=False),  # Hide activation panel
            f"EGP {wallet_balance}",
            f"🌿 {green_points}",
            "✅ ACCOUNT ACTIVE - All features available",
            "",  # QR input placeholder
            gr.update(visible=False),  # Hide demo badge
            gr.update(visible=False)   # Hide quick wallet button
        )

def ui_create_wallet(card_number, expiry, cvv):
    """Create wallet with enterprise validation and $200 USD deposit"""
    global current_user
    
    if not current_user: 
        return "❌ Login required", gr.update(), gr.update(), "", "", ""
    
    # Validate card number (basic check)
    if not card_number or len(card_number.replace('-', '').replace(' ', '')) < 16:
        return "❌ Invalid card number", gr.update(), gr.update(), "", "", ""
    
    # Validate expiry (MM/YY format)
    import re
    if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry.strip()):
        return "❌ Invalid expiry format (use MM/YY)", gr.update(), gr.update(), "", "", ""
    
    # Validate CVV
    if not cvv or len(cvv.strip()) < 3 or len(cvv.strip()) > 4:
        return "❌ Invalid CVV", gr.update(), gr.update(), "", "", ""
    
    try:
        # Activate wallet
        db.activate_wallet(current_user[0], card_number.replace('-', '').replace(' ', ''))
        
        # Deposit $200 USD (10,000 EGP)
        db.top_up(current_user[0], 10000)
        
        # Refresh user data
        current_user = db.get_traveler(current_user[0])
        
        return (
            "✅ Wallet activated! $200 USD deposited successfully",
            gr.Group(visible=True),   # Show main app
            gr.Group(visible=False),  # Hide activation panel
            f"EGP {current_user[8]}",
            f"🌿 {current_user[11]}",
            "✅ ACCOUNT ACTIVE - All features available"
        )
    except Exception as e:
        return f"❌ Activation failed: {str(e)}", gr.update(), gr.update(), "", "", ""

def ui_change_language(language):
    """Handle language change (placeholder for future implementation)"""
    return f"Language changed to {language} (Translation coming soon)"

def ui_link_bank(bank_name):
    """Link bank account to traveler with enterprise logging"""
    if not current_user: return "❌ Login required"
    if db.link_bank(current_user[0], bank_name):
        return f"✅ Bank linked: {bank_name}"
    else:
        return "❌ Bank linking failed"

def process_qr_payment(qr_string):
    """Process QR payment with enhanced validation and enterprise logging"""
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
        logger.error(f"Enterprise QR Payment Error: {e}")
        return "❌ Error processing QR payment"

def ui_scan_qr(qr_input):
    """Scan QR code from manual input"""
    return process_qr_payment(qr_input)

def ui_scan_qr_from_camera(image):
    """Enterprise QR scanning from webcam using QRDecoder"""
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
        logger.error(f"Enterprise QR Camera Scan Error: {e}")
        return f"❌ QR scanning failed: {str(e)}"

def ui_simulate_metro_scan():
    """Simulate scanning a Cairo Metro QR code for demo purposes"""
    simulated_qr = "PAY:CAIRO_METRO:50:EGP"
    result = process_qr_payment(simulated_qr)
    # Add transaction ID for visibility
    transaction_id = f"TXN-{random.randint(100000, 999999)}"
    return f"{result}\n📋 Transaction ID: {transaction_id}"

def ui_book_transport(mode, dest, pax, bags):
    """Book transportation with green points calculation and passenger/baggage pricing"""
    global current_user
    if not current_user: return "Login First"
    
    # Calculate cost: (25 * pax) + (5 * bags)
    cost = (25 * int(pax)) + (5 * int(bags))
    
    pts, lbl = EcoEngine.calculate_impact(mode)
    if db.purchase(current_user[0], f"Transport: {mode} to {dest} ({pax} Pax, {bags} Bags)", cost, "TRANSPORT"):
        db.add_green_points(current_user[0], pts)
        return f"✅ Booked {mode} to {dest}. Cost: EGP {cost}. +{pts} Points."
    return "❌ No Funds"

def ui_get_monument_info(monument_name):
    """Get monument information including Google Maps link"""
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found"
    
    return f"📍 {monument_name}\n🗺️ Location: {target[4]}\n📄 Description: {target[2]}\n🕒 Hours: {target[6] if len(target) > 6 else 'N/A'}\n♿ Accessibility: {target[7] if len(target) > 7 else 'N/A'}"

def ui_buy_transport_card(card_name):
    """Purchase unified transport card with enterprise validation"""
    global current_user
    if not current_user: 
        return "❌ Login required", None
    
    transport_cards = MarketplaceEngine.get_transport_cards()
    selected_card = next((card for card in transport_cards if card[0] == card_name), None)
    
    if not selected_card:
        return "❌ Invalid transport card selected", None
    
    card_name_display, description, price = selected_card
    
    # Check wallet balance
    if current_user[8] < price:
        return f"❌ Insufficient funds. Current balance: EGP {current_user[8]}, Required: EGP {price}", None
    
    # Process purchase
    if db.purchase(current_user[0], f"Transport Card: {card_name_display}", price, "TRANSPORT"):
        # Generate transport card PDF
        card_info = {
            'id': f"TC-{random.randint(100000, 999999)}",
            'card_name': card_name_display,
            'description': description,
            'price': price,
            'purchaser': current_user[1],
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        pdf_filename = DocumentIssuer.generate_transport_card_pdf(card_info)
        return f"✅ Transport card purchased: {card_name_display} - EGP {price}", pdf_filename
    
    return "❌ Purchase failed. Please try again.", None

def ui_book_monument_family(monument_name, adults, students, kids):
    """
    FAMILY MODE: Book monument tickets for multiple visitor types with group PDF generation
    Calculate: (Adults * Price) + (Students * Price * 0.5) + (Kids * Price * 0.3)
    """
    global current_user
    if not current_user: return "Login First", None
    
    monuments = db.get_data("monuments")
    target = next((m for m in monuments if m[1] == monument_name), None)
    if not target: return "Error: Monument Not Found", None
    
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
        return "❌ Please select at least one visitor", None
    
    if db.purchase(current_user[0], f"Family Ticket: {monument_name}", total_price, "MONUMENTS"):
        # Create ticket records for each visitor type
        ticket_info_list = []
        
        if adults > 0:
            db.create_ticket(current_user[0], monument_name, "Adult", adults, adult_price)
            ticket_info_list.append({
                'monument_name': monument_name,
                'visitor_type': 'Adult',
                'quantity': adults,
                'price': adult_price
            })
        
        if students > 0:
            db.create_ticket(current_user[0], monument_name, "Student", students, student_price)
            ticket_info_list.append({
                'monument_name': monument_name,
                'visitor_type': 'Student',
                'quantity': students,
                'price': student_price
            })
        
        if kids > 0:
            db.create_ticket(current_user[0], monument_name, "Kid", kids, kid_price)
            ticket_info_list.append({
                'monument_name': monument_name,
                'visitor_type': 'Kid',
                'quantity': kids,
                'price': kid_price
            })
        
        # Generate group ticket PDF
        group_pdf = DocumentIssuer.generate_group_ticket_pdf(ticket_info_list)
        
        return f"✅ ISSUED: {adults} Adults, {students} Students, {kids} Kids for {monument_name}. Total: {total_price} EGP.", group_pdf
    
    return "❌ Insufficient Funds", None

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
    price = 600 if "Orange" in plan_name else 500
    if db.purchase(current_user[0], plan_name, price, "CONNECTIVITY"):
        return f"✅ Activated: {plan_name}. QR sent to email."
    return "❌ Insufficient Funds"

def ui_buy_souvenir(item_name):
    """Purchase souvenir item"""
    global current_user
    if not current_user: return "Login First"
    price = 300 if "Gold" in item_name else 250
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
    """Demo login with auto-activation and deep data (18 arguments)"""
    global current_user
    name = "Diplomat-DEMO-001"
    full_name = "Demo User"
    # Fix Demo Nationality: Force to "USA" for Visa functionality with all 18 required arguments
    uid = db.register_traveler(
        name, 
        full_name, 
        "D999999", 
        "USA", 
        "Foreign", 
        "2030-01-01", 
        "BIO-DEMO-KEY", 
        "1990-01-01",  # dob
        "Male",  # gender
        "+20123456789",  # phone
        "demo@horus.com",  # email
        "2026-10-01",  # arrival_date
        "USA",  # country_boarded
        "DEMO-001",  # flight_number
        "Air",  # mode_of_arrival
        "2026-10-10",  # departure_date
        "Egypt",  # country_residence
        "DEMO-VISA-001",  # visa_no
        "USA Embassy",  # issued_by
        "Hotel",  # accommodation_type
        "Cairo Marriott Hotel, Zamalek",  # accommodation_address
        "Diplomat",  # occupation
        "Official Visit"  # purpose_of_travel
    )
    
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

def ui_top_up(amount):
    """Top up wallet with real database backend integration"""
    global current_user
    
    if not current_user: 
        return "❌ Error: Not logged in", "---"
    
    try:
        # Database Call - Add funds to wallet
        new_balance = db.top_up(current_user[0], float(amount))
        
        # Refresh Global User State to get updated balance
        current_user = db.get_traveler(current_user[0])
        
        # Return receipt message and updated balance
        return f"✅ RECEIPT: Successfully added ${amount} (EGP {amount*50})", f"EGP {current_user[8]:,.2f}"
    
    except Exception as e:
        return f"❌ Top-up failed: {str(e)}", f"EGP {current_user[8]:,.2f}"

def ui_ai_chat_with_logging(msg, history):
    """Enterprise AI chat with interaction logging"""
    global current_user
    
    if not current_user:
        return "❌ Login required for AI chat"
    
    # Log the question
    question = msg if isinstance(msg, str) else str(msg)
    
    # Get AI response
    response = ask_ai(msg, history)
    
    # Log the interaction for analytics
    db.log_ai_interaction(current_user[0], question, response, "GENERAL")
    
    return response

# ==============================================================================
# 🎨 ENTERPRISE GRADIO INTERFACE - ENHANCED QR SCANNER & LOGO
# ==============================================================================

css = """
body { background-color: #1a1a1a; }
.gradio-container { font-family: 'Segoe UI', sans-serif; background-color: #1a1a1a; }

/* SOVEREIGN HEADER FIX - HIGH VISIBILITY */
.sovereign-header { 
    position: relative; 
    top: 0; 
    left: 0;
    width: 100%;
    text-align: center;
    padding: 15px 0;
    background: linear-gradient(135deg, #D4AF37, #B8941F);
    color: #000000; 
    font-size: 16px; 
    letter-spacing: 3px;
    font-weight: 700;
    z-index: 1000; 
    pointer-events: none; 
    text-transform: uppercase;
    border-radius: 0 0 15px 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
}

/* SYSTEM STATUS - HIGH CONTRAST */
.system-status { 
    background: linear-gradient(135deg, #2a2a2a, #1a1a1a); 
    color: #ffffff; 
    padding: 20px; 
    border-left: 5px solid #D4AF37; 
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    font-size: 14px;
    margin: 15px 0;
}

/* BUTTONS - 2026 STYLE */
button.primary { 
    background: linear-gradient(135deg, #D4AF37, #B8941F) !important; 
    color: #000000 !important; 
    font-weight: 700 !important; 
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
}

button.secondary { 
    background: linear-gradient(135deg, #2F4F4F, #1C3A3A) !important; 
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

/* TABS - MODERN STYLE */
.gradio-tabs .tab-nav {
    background: #2a2a2a !important;
    border-radius: 10px !important;
    padding: 5px !important;
}

.gradio-tabs .tab-nav button {
    color: #ffffff !important;
    border-radius: 8px !important;
    margin: 2px !important;
    transition: all 0.3s ease !important;
}

.gradio-tabs .tab-nav button.selected {
    background: linear-gradient(135deg, #D4AF37, #B8941F) !important;
    color: #000000 !important;
}

/* INPUTS - DARK THEME */
.gradio-textbox, .gradio-dropdown {
    background: #2a2a2a !important;
    border: 1px solid #444444 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

.gradio-textbox input, .gradio-dropdown select {
    background: transparent !important;
    color: #ffffff !important;
}

/* MARKDOWN HEADINGS */
.markdown h1 {
    color: #D4AF37 !important;
    font-weight: 700 !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
}

.markdown h2 {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.markdown h3 {
    color: #D4AF37 !important;
    font-weight: 600 !important;
}
"""

# Initialize database instance
db = HorusDB()

# Generate README on startup
ReadmeGenerator.generate_readme()

with gr.Blocks(css=css, title="Horus Key Enterprise v12.0") as demo:
    # UPDATED HEADER - CLEAN BRANDING
    gr.HTML("<div class='sovereign-header'>✨ HORUS SOVEREIGN ECOSYSTEM | SECURE CONNECTED ✨</div>")
    
    # DYNAMIC LOGO (Military-grade asset loading with perfect centering)
    logo_data = generate_dynamic_assets()
    gr.HTML(f"""
    <div style='display: flex; justify-content: center; align-items: center; margin: 30px 0;'>
        <img src='{logo_data}' alt='Horus Logo' width='300' 
             style='border-radius: 15px; transition: all 0.3s ease;' />
    </div>
    """)
    gr.Markdown(f"# 👁️ {config.APP_NAME}")
    
    # SYSTEM STATUS DISPLAY - HIGH CONTRAST
    system_status = HorusConfig.get_system_status()
    status_text = f"""
    <div class='system-status'>
        <strong>🔧 Enterprise System Status:</strong> 
        Platform: {system_status['platform']} | 
        QR Scanner: {'✅ Enterprise Ready' if system_status['qr_scanner'] else '❌ Not Available'} | 
        Camera: {'✅ Professional Ready' if system_status['camera'] else '❌ Not Available'} | 
        AI Chat: {'✅ Gemini AI Ready' if system_status['ai'] else '❌ Not Available'} | 
        Enterprise Mode: {'✅ Active' if system_status['enterprise_mode'] else '❌ Inactive'}
    </div>
    """
    gr.HTML(status_text)
    
    # DEMO MODE BADGE
    with gr.Row():
        demo_badge = gr.Markdown("", visible=False)  # Hidden by default
    
        # STATUS BAR WITH LANGUAGE SELECTOR
    with gr.Row():
        status = gr.Textbox(label="Identity Status", value="Awaiting Biometrics")
        bal = gr.Textbox (label="Wallet Balance", value="---")
        score = gr.Textbox(label="Green Score", value="---")
        activation_status = gr.Textbox(label="Account Status", value="---")
        language_selector = gr.Dropdown(["English", "Arabic", "French", "German", "Russian"], label="Language", value="English")
        btn_quick_wallet = gr.Button("💳 Quick Wallet", variant="secondary", visible=False)
        
    # ENTRY GATE - DEEP DATA UPGRADE (Sovereign Edition)
    with gr.Row():
        cam = gr.Image(sources=["webcam"], label="Biometric Scanner", type="numpy")
        with gr.Column():
            # Basic Information
            gr.Markdown("**📋 Basic Information**")
            passport = gr.Textbox(label="Passport Number", value="A1234567")
            full_name = gr.Textbox(label="Full Name (as in Passport)", value="John Doe")
            passport_expiry = gr.Textbox(label="Passport Expiry (YYYY-MM-DD)", value="2028-12-31")
            nat = gr.Dropdown(["USA", "Egypt", "UK", "Germany", "Japan"], label="Nationality", value="USA")
            
            # Personal Information
            gr.Markdown("**👤 Personal Information**")
            with gr.Row():
                dob = gr.Textbox(label="Date of Birth (YYYY-MM-DD)", value="1990-01-01")
                gender = gr.Dropdown(["Male", "Female", "Other"], label="Gender", value="Male")
            phone = gr.Textbox(label="Phone Number", value="+20123456789")
            
            # Travel Information
            gr.Markdown("**✈️ Travel Information**")
            with gr.Row():
                arrival_date = gr.Textbox(label="Arrival Date (YYYY-MM-DD)", value="2026-12-25")
                departure_date = gr.Textbox(label="Departure Date (YYYY-MM-DD)", value="2026-12-30")
            with gr.Row():
                country_boarded = gr.Textbox(label="Country Boarded", value="USA")
                flight_number = gr.Textbox(label="Flight Number", value="MS123")
            mode_of_arrival = gr.Dropdown(["Air", "Sea", "Land"], label="Mode of Arrival", value="Air")
            
            # DEEP DATA FIELDS (Procedure Doc 1030)
            gr.Markdown("**📋 Enterprise Arrival Card Information**")
            occupation = gr.Textbox(label="Occupation", placeholder="e.g. Engineer, Doctor, Student")
            purpose_of_travel = gr.Dropdown(["Tourism", "Business", "Official Visit", "Study", "Medical", "Transit"], label="Purpose of Travel", value="Tourism")
            accommodation_address = gr.Textbox(label="Accommodation Address", placeholder="e.g. Cairo Marriott Hotel, Zamalek")
            
            # Additional DEEP DATA FIELDS
            gr.Markdown("**📋 Additional Travel Information**")
            with gr.Row():
                passport_issue_date = gr.Textbox(label="Passport Issue Date (YYYY-MM-DD)", placeholder="2020-01-01")
                transport_mode = gr.Dropdown(["Commercial", "Private", "Charter"], label="Transport Mode", value="Commercial")
            with gr.Row():
                accommodation_type = gr.Dropdown(["Hotel", "Apartment", "Resort", "Hostel", "Other"], label="Accommodation Type", value="Hotel")
                departure_mode = gr.Dropdown(["Air", "Sea", "Land"], label="Departure Mode", value="Air")
            with gr.Row():
                departure_flight = gr.Textbox(label="Departure Flight Number", placeholder="MS124")
                visa_no = gr.Textbox(label="Visa Number", placeholder="TBD")
                issued_by = gr.Textbox(label="Issued By", placeholder="TBD")
            
            with gr.Row():
                btn = gr.Button("SCAN FACE & ENTER ECOSYSTEM", variant="primary")
                btn_demo = gr.Button("🔑 DEMO ACCESS (Bypass Bio)", variant="secondary")

    # ACTIVATION PANEL
    with gr.Group(visible=False) as activation_panel:
        gr.Markdown("# 🔒 ACCOUNT ACTIVATION REQUIRED")
        gr.Markdown("### Deposit $200 USD to unlock all HORUS Enterprise features")
        with gr.Row():
            card_input = gr.Textbox(label="Credit Card Number", placeholder="1234-5678-9012-3456", type="password")
            expiry_input = gr.Textbox(label="Expiry (MM/YY)", placeholder="12/28")
            cvv_input = gr.Textbox(label="CVV", placeholder="123", type="password")
        btn_activate = gr.Button("DEPOSIT $200 & ACTIVATE", variant="primary")
        activation_msg = gr.Textbox(label="Activation Status", interactive=False)

    # MAIN APP GROUP
    with gr.Group(visible=False) as app:
        with gr.Tabs():
            # 1. VISA
            with gr.TabItem("🛂 Visa & Identity"):
                gr.Markdown("### 4.B Visa upon Arrival & 4.I Digital Access")
                gr.HTML("<a href='https://visaguide.world/online/egypt-e-visa/' target='_blank'>🔗 Check Official e-Visa Eligibility</a>")
                btn_visa = gr.Button(f"Pay {config.PRICING['visa_fee']} EGP & Issue Visa")
                with gr.Row():
                    out_v = gr.Textbox(label="Status")
                    img_v = gr.Image(label="Digital QR Stamp")
                    file_v = gr.File(label="Download E-Visa PDF")
                btn_visa.click(ui_issue_visa, outputs=[out_v, img_v, file_v])
                
            # 2. TRANSPORT (REAL EGYPT MODE)
            with gr.TabItem("🚕 Mobility"):
                gr.Markdown("### 4.D Booking & 4.E Eco-Travel")
                with gr.Row():
                    mode = gr.Dropdown([
                        "Cairo Monorail", "LRT (Electric Train)", "Electric Bus",
                        "Metro Line 1", "Metro Line 2", "Metro Line 3",
                        "Gas-Powered Taxi", "Private Car", "Online Ride-Hailing",
                        "Shared Shuttle", "Train", "Airport Transfer"
                    ], label="Mode")
                    dest = gr.Textbox(label="Destination", placeholder="e.g. Pyramids")
                with gr.Row():
                    pax = gr.Number(minimum=1, value=1, label="Passengers", precision=0)
                    bags = gr.Number(minimum=0, value=0, label="Bags", precision=0)
                btn_tr = gr.Button("Book Ride")
                out_tr = gr.Textbox(label="Receipt")
                btn_tr.click(ui_book_transport, inputs=[mode, dest, pax, bags], outputs=[out_tr])
            
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
                gr.Markdown("### 💳 Enterprise Wallet")
                with gr.Row():
                    gr.Textbox(label="Linked Payment Method", value="VISA **** 1234 (Foreign)", interactive=False)
                    gr.Textbox(label="Status", value="ACTIVE", interactive=False)
                
                gr.Markdown("### 💰 Top Up Funds")
                with gr.Row():
                    topup_amount = gr.Number(label="Amount ($)", value=200, precision=0)
                    btn_topup = gr.Button("Confirm Top-Up", variant="primary")
                
                topup_msg = gr.Textbox(label="Transaction Receipt")
                btn_topup.click(ui_top_up, inputs=[topup_amount], outputs=[topup_msg, bal])

            # 5. SCAN & PAY - ENHANCED QR SCANNER
            with gr.TabItem("📷 Scan & Pay"):
                gr.Markdown("### Enterprise QR Scanning - Advanced Multi-QR Support")
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**📷 Enterprise Camera QR Scanner**")
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
                        gr.Markdown("**Enterprise QR Examples**")
                        gr.Markdown("""
                        **Common QR Formats:**
                        - `PAY:CAIRO_METRO:50:EGP`
                        - `PAY:STARBUCKS_ZAMALEK:150:EGP`
                        - `PAY:UBER_RIDE:85:EGP`
                        - `PAY:PARKING_FEE:25:EGP`
                        
                        **Advanced Features:**
                        - Multi-QR code detection
                        - Enterprise validation
                        - Real-time processing
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
                
                # 📱 SIM & eSIM SECTION
                gr.Markdown("**📱 SIM & eSIM**")
                with gr.Row():
                    btn_orange = gr.Button("Buy Orange eSIM", variant="primary")
                    btn_vodafone = gr.Button("Buy Vodafone eSIM", variant="secondary")
                out_esim = gr.Textbox(label="eSIM Status")
                btn_orange.click(lambda: "✅ Orange eSIM purchase initiated - Check your email", outputs=[out_esim])
                btn_vodafone.click(lambda: "✅ Vodafone eSIM purchase initiated - Check your email", outputs=[out_esim])
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Enterprise eSIMs**")
                        plans = [f"{p[0]} ({p[2]} EGP)" for p in MarketplaceEngine.get_esims()]
                        dd_sim = gr.Dropdown(plans, label="Data Plan")
                        btn_sim = gr.Button("Activate eSIM")
                        out_sim = gr.Textbox()
                        btn_sim.click(ui_buy_esim, inputs=[dd_sim], outputs=[out_sim])
                    with gr.Column():
                        gr.Markdown("**Premium Souvenirs**")
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
                        gr.Markdown("**Enterprise Exclusive Offers**")
                        offers = [f"{o[0]} - {o[1]}" for o in MarketplaceEngine.get_exclusive_offers()]
                        dd_offer = gr.Dropdown(offers, label="Select Offer")
                        btn_offer = gr.Button("Claim Voucher")
                        out_offer = gr.Textbox()
                        btn_offer.click(ui_claim_offer, inputs=[dd_offer], outputs=[out_offer])
                    
                    with gr.Column():
                        gr.Markdown("**🎁 Enterprise Welcome Gift**")
                        gr.Markdown("*Special gift for enterprise travelers*")
                        btn_gift = gr.Button("🎁 CLAIM FREE EGYPT GIFT", variant="primary")
                        out_gift = gr.Textbox(label="Gift Status", interactive=False)
                        btn_gift.click(ui_claim_welcome_gift, outputs=[out_gift])
                
            # 8. AI
            with gr.TabItem("🤖 Horus AI"):
                gr.Markdown(f"Powered by **{config.AI_MODEL}**")
                if config.AI_ENABLED:
                    try:
                        gr.ChatInterface(fn=ui_ai_chat_with_logging, type="messages")
                    except TypeError:
                        gr.ChatInterface(fn=ui_ai_chat_with_logging)
                else:
                    gr.Markdown("⚠️ Enterprise AI Chat is not available. Please install google-genai package.")
                
            # 8. HELP & FAQ
            with gr.TabItem("❓ Help & FAQ"):
                gr.Markdown("### Frequently Asked Questions")
                
                with gr.Accordion("💳 Wallet Activation", open=False):
                    gr.Markdown("""
                    **How do I activate my wallet?**
                    - Deposit $200 USD using the activation panel
                    - Enter your card details (Card Number, MM/YY expiry, CVV)
                    - Once activated, you'll receive 10,000 EGP credit
                    
                    **What payment methods are accepted?**
                    - All major credit cards (Visa, Mastercard, American Express)
                    - Cards must be valid and not expired
                    
                    **Is my payment information secure?**
                    - Yes, all transactions are encrypted and secure
                    - We use enterprise-grade security for all payments
                    """)
                
                with gr.Accordion("🛂 Visa Rules", open=False):
                    gr.Markdown("""
                    **Who needs a visa for Egypt?**
                    - Check your eligibility using the link in the Visa tab
                    - 74 countries are eligible for Visa on Arrival
                    - Restricted countries must apply through embassies
                    
                    **What are the visa requirements?**
                    - Valid passport with at least 6 months validity
                    - Passport must not be expired
                    - Biometric registration required
                    
                    **How much does the visa cost?**
                    - Visa fee varies by nationality
                    - Check the Visa tab for exact pricing
                    """)
                
                with gr.Accordion("🌿 Green Score", open=False):
                    gr.Markdown("""
                    **What is the Green Score?**
                    - Points earned for using eco-friendly transport
                    - Electric/Metro transport: +20 points
                    - Shared transport: +10 points
                    - Private car: 0 points
                    
                    **How do I use my Green Score?**
                    - 100 points = 10% souvenir discount
                    - Higher scores unlock special rewards
                    - Track your environmental impact
                    
                    **Which transport is most eco-friendly?**
                    - Cairo Monorail and Metro Lines: Highest score
                    - Electric trains and buses: Good score
                    - Gas-powered vehicles: Lowest score
                    """)
                
            # 9. ADMIN
            with gr.TabItem("⚙️ Admin"):
                gr.Markdown("### Enterprise System Management")
                btn_s = gr.Button("Sync Code & Docs to GitHub", variant="stop")
                out_s = gr.TextArea(label="Diagnostic Logs")
                btn_s.click(GitAutopilot.sync_codebase, outputs=[out_s])
                
                gr.Markdown("### Enterprise Analytics")
                stats_display = gr.Textbox(label="System Stats", interactive=False, lines=8)
                refresh_stats_btn = gr.Button("🔄 Refresh Analytics")
                refresh_stats_btn.click(
                    lambda: json.dumps(db.get_system_stats(), indent=2),
                    outputs=[stats_display]
                )
                
                gr.Markdown("### Business Intelligence")
                analytics_display = gr.Textbox(label="Business Analytics", interactive=False, lines=10)
                refresh_analytics_btn = gr.Button("🔄 Refresh Analytics")
                refresh_analytics_btn.click(
                    lambda: json.dumps(db.get_enterprise_analytics(), indent=2),
                    outputs=[analytics_display]
                )

    # Event Wiring - 
    btn.click(ui_login, inputs=[cam, passport, nat, full_name, passport_expiry, occupation, purpose_of_travel, accommodation_address, dob, gender, phone, arrival_date, country_boarded, flight_number, mode_of_arrival, departure_date, passport_issue_date, transport_mode, accommodation_type, departure_mode, departure_flight, visa_no, issued_by], outputs=[status, app, activation_panel, bal, score, activation_status, qr_input, demo_badge, btn_quick_wallet])
    btn_demo.click(ui_demo_login, outputs=[status, app, activation_panel, bal, score, activation_status, qr_input, demo_badge])
    language_selector.change(ui_change_language, inputs=[language_selector], outputs=[status])
    btn_activate.click(ui_create_wallet, inputs=[card_input, expiry_input, cvv_input], outputs=[activation_msg, app, activation_panel, bal, score, activation_status])
    
    # Quick Wallet Button Event
    btn_quick_wallet.click(
        fn=lambda: (gr.Group(visible=False), gr.Group(visible=True), "💳 Please complete your deposit."),
        inputs=None,
        outputs=[app, activation_panel, status]
    )

# ==============================================================================
# 🚀 ENTERPRISE LAUNCH
# ==============================================================================

if __name__ == "__main__":
    # Final dependency check and installation
    logger.info("🚀 Starting HORUS v12.0 Sovereign Edition with advanced QR & AI...")
    
    # Install dependencies one last time before launch
    if not install_dependencies():
        logger.error("❌ Failed to install dependencies. Some features may not work.")
    
    # Final system status check
    final_status = HorusConfig.get_system_status()
    logger.info("📊 Final System Status:")
    for key, value in final_status.items():
        status_icon = "✅" if value or (isinstance(value, bool) and value) else "❌"
        logger.info(f"  {status_icon} {key}: {value}")
    
    # Launch with enterprise configuration
    logger.info("🚀 Launching HORUS v12.0 Sovereign Edition...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True,
        allowed_paths=["."],  # Allow file serving from current directory
        show_error=True,
        favicon_path=None,
        ssl_verify=False,
        quiet=False,
        inbrowser=True
    )