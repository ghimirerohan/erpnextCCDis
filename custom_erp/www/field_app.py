import frappe


def get_context(context):
	"""Inject website boot used by the Vue SPA (CSRF + auth hints for router guards)."""
	context.no_cache = 1
	from frappe.website.utils import get_boot_data

	boot = dict(get_boot_data())
	existing = context.get("boot")
	if existing:
		try:
			boot.update(dict(existing))
		except Exception:
			pass
	tok = None
	if getattr(frappe.local, "session", None) and getattr(frappe.session, "data", None):
		tok = frappe.session.data.get("csrf_token")
	if tok:
		boot["csrf_token"] = tok
	boot["session_user"] = frappe.session.user
	boot["user_roles"] = frappe.get_roles(frappe.session.user)
	context.boot = boot
	return context
