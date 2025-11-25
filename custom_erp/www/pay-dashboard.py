import frappe

def get_context(context):
	"""Context for pay-dashboard app"""
	context.no_cache = 1
	return context
