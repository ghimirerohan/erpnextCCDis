"""
PWA API endpoints for serving service workers and manifests
with proper headers for Android Chrome PWA installation
"""
import frappe
import os
import json


@frappe.whitelist(allow_guest=True)
def get_service_worker(app_name):
    """
    Serve service worker for a specific app with correct headers.
    Critical for Android Chrome PWA installation - the SW needs
    Service-Worker-Allowed header to control a broader scope.
    
    Args:
        app_name: Name of the app (e.g., 'qrpay', 'pay-dashboard')
    
    Returns:
        Service worker JavaScript content
    """
    if not app_name:
        app_name = 'home'
    
    # Sanitize app name to prevent path traversal
    app_name = app_name.replace('..', '').replace('/', '').replace('\\', '')
    
    # Path to the service worker file
    sw_path = frappe.get_app_path('custom_erp', 'public', 'frontend', app_name, 'sw.js')
    
    if not os.path.exists(sw_path):
        frappe.throw(f"Service worker not found for {app_name}", frappe.DoesNotExistError)
    
    with open(sw_path, 'r') as f:
        sw_content = f.read()
    
    # Set headers - must be set before response type
    frappe.local.response_headers['Content-Type'] = 'application/javascript; charset=utf-8'
    frappe.local.response_headers['Service-Worker-Allowed'] = f'/{app_name}/'
    frappe.local.response_headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    # Use binary response type for proper handling
    frappe.response['type'] = 'binary'
    frappe.response['filecontent'] = sw_content.encode('utf-8')
    frappe.response['filename'] = 'sw.js'


@frappe.whitelist(allow_guest=True)
def get_manifest(app_name):
    """
    Serve manifest for a specific app with proper Content-Type.
    
    Args:
        app_name: Name of the app (e.g., 'qrpay', 'pay-dashboard')
    
    Returns:
        Manifest JSON content as dict (Frappe will serialize it)
    """
    if not app_name:
        app_name = 'home'
    
    # Sanitize app name
    app_name = app_name.replace('..', '').replace('/', '').replace('\\', '')
    
    # Path to the manifest file
    manifest_path = frappe.get_app_path('custom_erp', 'public', 'frontend', app_name, 'manifest.json')
    
    if not os.path.exists(manifest_path):
        frappe.throw(f"Manifest not found for {app_name}", frappe.DoesNotExistError)
    
    with open(manifest_path, 'r') as f:
        manifest_dict = json.load(f)
    
    # Set headers for JSON response
    frappe.local.response_headers['Content-Type'] = 'application/manifest+json; charset=utf-8'
    frappe.local.response_headers['Cache-Control'] = 'no-cache'
    
    # Return as dict - Frappe will serialize it as JSON
    return manifest_dict
