import os
import subprocess
import sys
import shutil
from pathlib import Path

def after_install():
    """Build frontend after custom_erp installation to make /jsapp accessible immediately."""
    print("Building custom_erp frontend...")
    
    # Get the app directory
    app_dir = Path(__file__).parent.parent
    frontend_dir = app_dir / "frontend"
    
    if not frontend_dir.exists():
        print("Frontend directory not found, skipping build.")
        return
    
    # Check for Node.js and npm
    node_check = shutil.which("node")
    npm_check = shutil.which("npm")
    
    if not node_check:
        print("Node.js not found. Please install Node.js to build the frontend.")
        print("Visit: https://nodejs.org/")
        return
    
    if not npm_check:
        print("npm not found. Please install npm to build the frontend.")
        return
    
    print(f"Node.js version: {subprocess.check_output(['node', '--version']).decode().strip()}")
    print(f"npm version: {subprocess.check_output(['npm', '--version']).decode().strip()}")
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install dependencies
        print("Installing frontend dependencies...")
        subprocess.run([
            "npm", "ci", 
            "--no-audit", 
            "--no-fund", 
            "--prefer-offline"
        ], check=True, capture_output=True, text=True)
        
        # Build the frontend
        print("Building frontend...")
        result = subprocess.run([
            "npm", "run", "build"
        ], check=True, capture_output=True, text=True)
        
        print("Frontend build completed successfully!")
        print("The /jsapp route is now accessible at your site.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error building frontend: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        print("You can manually build the frontend later by running:")
        print(f"cd {frontend_dir}")
        print("npm ci --no-audit --no-fund --prefer-offline")
        print("npm run build")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("You can manually build the frontend later by running:")
        print(f"cd {frontend_dir}")
        print("npm ci --no-audit --no-fund --prefer-offline")
        print("npm run build")
