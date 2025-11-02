import os
import subprocess
import sys
import shutil
from pathlib import Path

def check_hrms_dependencies():
    """Check if HRMS app is installed and required doctypes exist."""
    try:
        import frappe
        
        # Check if Driver doctype exists
        driver_exists = frappe.db.exists("DocType", "Driver")
        # Check if Vehicle doctype exists
        vehicle_exists = frappe.db.exists("DocType", "Vehicle")
        
        if not driver_exists:
            print("⚠️  WARNING: Driver doctype not found. HRMS app may not be installed.")
            print("   Driver field will be created but may not work without HRMS.")
        
        if not vehicle_exists:
            print("⚠️  WARNING: Vehicle doctype not found. HRMS app may not be installed.")
            print("   Vehicle field will be created but may not work without HRMS.")
        
        if driver_exists and vehicle_exists:
            print("✅ HRMS dependencies verified: Driver and Vehicle doctypes found.")
        
        return driver_exists, vehicle_exists
        
    except Exception as e:
        print(f"⚠️  Could not verify HRMS dependencies: {e}")
        print("   Installation will continue, but Driver/Vehicle fields may not work.")
        return False, False


def verify_custom_fields():
    """Verify that custom fields were created successfully."""
    try:
        import frappe
        
        driver_field = frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_driver_for_vehicle"})
        vehicle_field = frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_vehicle_for_delivery"})
        
        if driver_field:
            print("✅ Driver custom field verified.")
        else:
            print("⚠️  WARNING: Driver custom field not found after installation.")
        
        if vehicle_field:
            print("✅ Vehicle custom field verified.")
        else:
            print("⚠️  WARNING: Vehicle custom field not found after installation.")
        
        return driver_field and vehicle_field
        
    except Exception as e:
        print(f"⚠️  Could not verify custom fields: {e}")
        return False


def verify_frontend_build():
    """Verify that frontend build output exists."""
    try:
        app_dir = Path(__file__).parent.parent
        frontend_build_dir = app_dir / "custom_erp" / "public" / "frontend"
        jsapp_dir = frontend_build_dir / "jsapp" if frontend_build_dir.exists() else None
        
        if not frontend_build_dir.exists():
            print("⚠️  WARNING: Frontend build directory not found.")
            return False
        
        # Check for key files
        index_html = frontend_build_dir / "index.html"
        if not index_html.exists():
            print("⚠️  WARNING: Frontend index.html not found.")
            return False
        
        # Check for jsapp structure
        if jsapp_dir and jsapp_dir.exists():
            print(f"✅ Frontend build verified: {len(list(jsapp_dir.iterdir()))} sub-apps found.")
        else:
            print("⚠️  WARNING: jsapp directory structure not found.")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not verify frontend build: {e}")
        return False


def after_install():
    """
    Build frontend after custom_erp installation to make /jsapp accessible immediately.
    Enhanced with dependency checks, error handling, and verification.
    """
    print("\n" + "="*60)
    print("Custom ERP Installation - Post-Install Hook")
    print("="*60 + "\n")
    
    # Step 1: Check HRMS dependencies
    print("Step 1: Checking HRMS dependencies...")
    check_hrms_dependencies()
    print()
    
    # Step 2: Build frontend
    print("Step 2: Building frontend...")
    
    # Get the app directory
    app_dir = Path(__file__).parent.parent
    frontend_dir = app_dir / "frontend"
    original_cwd = os.getcwd()
    
    if not frontend_dir.exists():
        print("❌ ERROR: Frontend directory not found at:", frontend_dir)
        print("   Frontend build skipped. App installation will continue.")
        print("   You must build the frontend manually after installation.")
        return
    
    # Check for Node.js and npm
    node_check = shutil.which("node")
    npm_check = shutil.which("npm")
    
    if not node_check:
        print("❌ ERROR: Node.js not found. Frontend cannot be built.")
        print("   Please install Node.js: https://nodejs.org/")
        print("   After installing Node.js, run:")
        print(f"   cd {frontend_dir}")
        print("   npm ci && npm run build")
        raise RuntimeError("Node.js is required for frontend build")
    
    if not npm_check:
        print("❌ ERROR: npm not found. Frontend cannot be built.")
        print("   npm should be installed with Node.js.")
        raise RuntimeError("npm is required for frontend build")
    
    try:
        node_version = subprocess.check_output(['node', '--version'], stderr=subprocess.DEVNULL).decode().strip()
        npm_version = subprocess.check_output(['npm', '--version'], stderr=subprocess.DEVNULL).decode().strip()
        print(f"   Node.js version: {node_version}")
        print(f"   npm version: {npm_version}")
    except Exception as e:
        print(f"   ⚠️  Could not get Node.js/npm versions: {e}")
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install dependencies with better error handling
        print("   Installing frontend dependencies...")
        install_result = subprocess.run([
            "npm", "ci", 
            "--no-audit", 
            "--no-fund", 
            "--prefer-offline"
        ], check=True, capture_output=True, text=True, timeout=300)
        
        print("   ✅ Dependencies installed successfully.")
        
        # Build the frontend with timeout
        print("   Building frontend (this may take a few minutes)...")
        build_result = subprocess.run([
            "npm", "run", "build"
        ], check=True, capture_output=True, text=True, timeout=600)
        
        print("   ✅ Frontend build completed successfully!")
        
    except subprocess.TimeoutExpired:
        print("   ❌ ERROR: Frontend build timed out.")
        print("   This may indicate a system performance issue.")
        raise RuntimeError("Frontend build timed out")
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ ERROR: Frontend build failed!")
        print(f"   Command: {' '.join(e.cmd)}")
        if e.stdout:
            print(f"   stdout: {e.stdout[-500:]}")  # Last 500 chars
        if e.stderr:
            print(f"   stderr: {e.stderr[-500:]}")  # Last 500 chars
        raise RuntimeError(f"Frontend build failed: {e}")
        
    except Exception as e:
        print(f"   ❌ ERROR: Unexpected error during frontend build: {e}")
        raise RuntimeError(f"Frontend build error: {e}")
        
    finally:
        # Restore original working directory
        os.chdir(original_cwd)
    
    print()
    
    # Step 3: Verify frontend build
    print("Step 3: Verifying frontend build...")
    frontend_verified = verify_frontend_build()
    print()
    
    # Step 4: Verify custom fields
    print("Step 4: Verifying custom fields...")
    fields_verified = verify_custom_fields()
    print()
    
    # Summary
    print("="*60)
    print("Installation Summary")
    print("="*60)
    print(f"Frontend Build: {'✅ Success' if frontend_verified else '⚠️  Issues detected'}")
    print(f"Custom Fields: {'✅ Success' if fields_verified else '⚠️  Issues detected'}")
    print()
    print("The /jsapp route should now be accessible at your site.")
    print("Frontend apps (qrpay, uploadsales, etc.) are available as standalone PWAs.")
    print("="*60 + "\n")
