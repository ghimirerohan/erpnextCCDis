import frappe
from custom_erp.api.authentik import _assign_roles


def assign_roles_on_login(login_manager):
    user = login_manager.user
    if not user or user == "Guest":
        return

    user_doc = frappe.get_doc("User", user)

    is_authentik = any(
        sl.provider == "authentik"
        for sl in user_doc.get("social_logins", [])
    )
    if not is_authentik:
        return

    groups = frappe.cache().get_value(f"authentik_groups:{user}") or []
    _assign_roles(user, groups)
    frappe.cache().delete_value(f"authentik_groups:{user}")