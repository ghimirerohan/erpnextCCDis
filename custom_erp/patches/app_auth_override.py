"""
Override Frappe's app.py get_context to prevent redirect to /login for our apps
"""
import frappe
from frappe import _

def override_app_auth():
	"""Monkey patch Frappe's app.py get_context to handle root-level app authentication"""
	
	# Import the original module
	import frappe.www.app as app_module
	original_get_context = app_module.get_context
	
	def custom_get_context(context):
		"""Custom get_context that handles root-level app authentication"""
		
		path = frappe.local.request.path
		app_names = ['qrpay', 'qrpay-admin', 'scanner', 'pay-dashboard', 'uploadsales', 'uploadreco', 'dailyrecoentry', 'home', 'testlogin']
		
		# Check if this is one of our app paths
		path_parts = [p for p in path.strip('/').split('/') if p]
		
		if path_parts and path_parts[0] in app_names:
			app_name = path_parts[0]
			normalized_path = path.rstrip('/') if path != '/' else path
			
			# If on login page, allow access without authentication
			if normalized_path.endswith('/login'):
				# Don't require authentication for login pages
				# Just set basic context
				context.update({
					"no_cache": 1,
					"app_name": app_name,
				})
				return context
			
			# If user is Guest, redirect to app's login instead of /login
			if frappe.session.user == "Guest":
				app_login_path = f'/{app_name}/login'
				frappe.logger().info(f"[custom_erp] app_auth_override: Redirecting Guest from {path} to {app_login_path}")
				frappe.local.response["type"] = "redirect"
				frappe.local.response["location"] = app_login_path
				frappe.local.response["http_status_code"] = 302
				raise frappe.Redirect(302)
		
		# For all other paths, use original behavior
		return original_get_context(context)
	
	# Replace the function
	app_module.get_context = custom_get_context
