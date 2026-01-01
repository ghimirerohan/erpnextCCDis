import frappe

def get_context(context):
	"""Context for Vue app"""
	context.no_cache = 1
	return context
