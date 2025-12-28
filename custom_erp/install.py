import os
import subprocess
import sys
import shutil
from pathlib import Path

def migrate_add_updated_later_field():
    """
    Migration to add 'updated_later' field to Daily Sales Payment Reco Line table.
    This field tracks entries that were added/updated after the initial import.
    """
    try:
        import frappe
        
        table_name = "tabDaily Sales Payment Reco Line"
        column_name = "updated_later"
        
        # Check if the column already exists
        columns = frappe.db.sql(f"SHOW COLUMNS FROM `{table_name}` LIKE '{column_name}'")
        
        if not columns:
            print(f"   Adding '{column_name}' field to {table_name}...")
            frappe.db.sql(f"""
                ALTER TABLE `{table_name}` 
                ADD COLUMN `{column_name}` INT(1) NOT NULL DEFAULT 0
            """)
            frappe.db.commit()
            print(f"   ✅ '{column_name}' field added successfully.")
        else:
            print(f"   ✅ '{column_name}' field already exists in {table_name}.")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Could not add '{column_name}' field: {e}")
        return False


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
        
        if not frontend_build_dir.exists():
            print("⚠️  WARNING: Frontend build directory not found.")
            return False
        
        # Check for app directories (qrpay, pay-dashboard, etc.)
        app_names = ['qrpay', 'pay-dashboard', 'home', 'scanner', 'uploadsales', 'uploadreco', 'dailyrecoentry', 'qrpay-admin', 'testlogin']
        found_apps = []
        for app_name in app_names:
            app_path = frontend_build_dir / app_name
            if app_path.exists():
                found_apps.append(app_name)
        
        if found_apps:
            print(f"✅ Frontend build verified: {len(found_apps)} apps found ({', '.join(found_apps)})")
        else:
            print("⚠️  WARNING: No app directories found in frontend build.")
            return False
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not verify frontend build: {e}")
        return False


def after_install():
    """
    Build frontend after custom_erp installation to make apps accessible immediately.
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
    
    # Step 5: Run database migrations
    print("Step 5: Running database migrations...")
    migration_success = migrate_add_updated_later_field()
    print()
    
    # Summary
    print("="*60)
    print("Installation Summary")
    print("="*60)
    print(f"Frontend Build: {'✅ Success' if frontend_verified else '⚠️  Issues detected'}")
    print(f"Custom Fields: {'✅ Success' if fields_verified else '⚠️  Issues detected'}")
    print()
    print("The Vue apps should now be accessible at your site (e.g., /qrpay, /pay-dashboard).")
    print("Frontend apps (qrpay, uploadsales, etc.) are available as standalone PWAs.")
    print("="*60 + "\n")
