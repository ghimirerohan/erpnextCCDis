import frappe
from frappe import _

def before_request():
	"""Intercept requests to root-level app paths and handle authentication redirects"""
	
	try:
		path = frappe.local.request.path
		
		# List of known app names
		app_names = ['qrpay', 'qrpay-admin', 'scanner', 'pay-dashboard', 'uploadsales', 'uploadreco', 'dailyrecoentry', 'home', 'testlogin']
		
		# Intercept /account/login redirects - convert to app-specific login
		if path and '/account/login' in path:
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
			frappe.logger().info(f"[custom_erp] before_request: Redirecting from {path} to {app_login_path}")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = app_login_path
			raise frappe.Redirect(302)
		
		# Extract app name from root-level path
		path_parts = [p for p in path.strip('/').split('/') if p]
		
		# Check if this is one of our app paths
		if not path_parts or path_parts[0] not in app_names:
			return
		
		app_name = path_parts[0]
		
		# Handle trailing slash - redirect /appname to /appname/
		if path == f'/{app_name}':
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = f'/{app_name}/'
			raise frappe.Redirect(302)
		
		# CRITICAL: If on login page, allow access and prevent any redirects
		normalized_path = path.rstrip('/') if path != '/' else path
		if normalized_path.endswith('/login'):
			# Store app name in cookie for future redirects
			frappe.local.response.set_cookie('last_app', app_name, max_age=3600, path='/')
			# Don't redirect - allow the login page to load
			return
		
		# Check if user is Guest (not authenticated)
		user = frappe.session.user
		
		if user == 'Guest':
			# Store app name in cookie before redirecting
			frappe.local.response.set_cookie('last_app', app_name, max_age=3600, path='/')
			
			# Redirect to this app's login page
			app_login_path = f'/{app_name}/login'
			frappe.logger().info(f"[custom_erp] before_request: Redirecting Guest from {path} to: {app_login_path}")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = app_login_path
			raise frappe.Redirect(302)
			
	except frappe.Redirect:
		# Re-raise redirects
		raise
	except Exception as e:
		# Don't break the request if our hook fails
		frappe.log_error(f"Error in before_request hook: {str(e)}")
		pass
