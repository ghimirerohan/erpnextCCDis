#!/bin/bash

# Custom ERP App Installation Script
# This script handles the frontend build process after the app is installed

echo "Installing Custom ERP App..."

# Check if we're in a Frappe bench environment
if [ ! -f "hooks.py" ]; then
    echo "Error: This script must be run from the app directory"
    exit 1
fi

# Install frontend dependencies and build
if [ -d "frontend" ]; then
    echo "Setting up frontend..."
    cd frontend
    
    # Install dependencies
    if command -v npm &> /dev/null; then
        echo "Installing npm dependencies..."
        npm install
        
        # Build the frontend
        echo "Building frontend..."
        npm run build
        
        echo "Frontend build completed successfully!"
    else
        echo "Warning: npm not found. Frontend build skipped."
        echo "Please install Node.js and npm to build the frontend."
    fi
    
    cd ..
else
    echo "Warning: frontend directory not found"
fi

echo "Custom ERP App installation completed!"
echo ""
echo "To complete the setup:"
echo "1. Run: bench install-app custom_erp"
echo "2. Run: bench migrate"
echo "3. Run: bench build"
echo ""
echo "For development:"
echo "- Frontend dev server: cd frontend && npm run dev"
