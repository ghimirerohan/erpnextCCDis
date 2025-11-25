import frappe

def get_context(context):
	"""Context for qrpay app"""
	context.no_cache = 1
	return context
