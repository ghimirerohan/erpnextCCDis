import frappe
from frappe import _
import os
import json

def before_request():
	"""Intercept requests to root-level app paths and handle authentication redirects"""
	
	try:
		path = frappe.local.request.path
		
		# List of known app names
		app_names = ['qrpay', 'qrpay-admin', 'scanner', 'pay-dashboard', 'uploadsales', 'uploadreco', 'dailyrecoentry', 'home', 'testlogin']
		
		# Extract app name from root-level path
		path_parts = [p for p in path.strip('/').split('/') if p]
		
		# Check if this is one of our app paths
		if not path_parts or path_parts[0] not in app_names:
			# Intercept /account/login redirects - convert to app-specific login
			if path and '/account/login' in path:
				handle_account_login_redirect(app_names)
			return
		
		app_name = path_parts[0]
		
		# Handle PWA files: sw.js and manifest.json - redirect to assets path
		# This allows proper caching and serving with correct headers via nginx/frappe
		if len(path_parts) >= 2:
			filename = path_parts[1]
			
			# Redirect sw.js to assets path
			if filename == 'sw.js':
				frappe.redirect_to_message(
					'Redirecting...',
					f'/assets/custom_erp/frontend/{app_name}/sw.js'
				)
				frappe.local.flags.redirect_location = f'/assets/custom_erp/frontend/{app_name}/sw.js'
				raise frappe.Redirect
			
			# Redirect manifest.json to assets path
			if filename == 'manifest.json':
				frappe.local.flags.redirect_location = f'/assets/custom_erp/frontend/{app_name}/manifest.json'
				raise frappe.Redirect
		
		# Handle trailing slash - redirect /appname to /appname/
		if path == f'/{app_name}':
			frappe.local.flags.redirect_location = f'/{app_name}/'
			raise frappe.Redirect
		
		# CRITICAL: If on login page, allow access and prevent any redirects
		normalized_path = path.rstrip('/') if path != '/' else path
		if normalized_path.endswith('/login'):
			return
		
		# Check if user is Guest (not authenticated)
		user = frappe.session.user
		
		if user == 'Guest':
			# Redirect to this app's login page
			app_login_path = f'/{app_name}/login'
			frappe.local.flags.redirect_location = app_login_path
			raise frappe.Redirect
			
	except frappe.Redirect:
		# Re-raise redirects
		raise
	except Exception as e:
		# Don't break the request if our hook fails
		frappe.log_error(f"Error in before_request hook: {str(e)}")
		pass


def handle_account_login_redirect(app_names):
	"""Handle /account/login redirects - convert to app-specific login"""
	path = frappe.local.request.path
	
	# Try to get app name from referrer
	referrer = frappe.local.request.headers.get('Referer', '')
	app_name = 'home'
	
	# Check referrer for app name (root-level paths)
	if referrer:
		# Extract path from referrer URL
		from urllib.parse import urlparse
		ref_path = urlparse(referrer).path
		ref_parts = [p for p in ref_path.strip('/').split('/') if p]
		if ref_parts and ref_parts[0] in app_names:
			app_name = ref_parts[0]
	
	# Try to get from cookies as fallback
	if app_name == 'home':
		app_cookie = frappe.local.request.cookies.get('last_app')
		if app_cookie and app_cookie in app_names:
			app_name = app_cookie
	
	app_login_path = f'/{app_name}/login'
	frappe.local.flags.redirect_location = app_login_path
	raise frappe.Redirect
