"""
Override Frappe's website authentication to redirect to app-specific login pages

Note: This override is currently disabled because render_page doesn't exist in this Frappe version.
The routing is handled by the Python files in custom_erp/www/ instead.
"""
# Import frappe at module level to avoid scoping issues
import frappe

def override_website_auth():
	"""Monkey patch Frappe's website router to handle root-level app authentication"""
	
	# render_page doesn't exist in this Frappe version
	# Routing is handled by the Python files in custom_erp/www/ instead
	# This function is kept for compatibility but does nothing
	# Simply return without doing anything
	pass
