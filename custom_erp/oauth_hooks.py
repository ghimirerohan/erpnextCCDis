import frappe


def on_user_insert(doc, method):
    groups = frappe.cache().get_value(f"authentik_groups:{doc.name}") or []
    if not groups:
        return
    # Clear cache FIRST to prevent loop
    frappe.cache().delete_value(f"authentik_groups:{doc.name}")
    _assign_roles(doc, groups)


def on_user_update(doc, method):
    groups = frappe.cache().get_value(f"authentik_groups:{doc.name}") or []
    if not groups:
        return
    # Clear cache FIRST to prevent loop
    frappe.cache().delete_value(f"authentik_groups:{doc.name}")
    _assign_roles(doc, groups)


def assign_roles_on_login(login_manager):
    user = login_manager.user
    if not user or user == "Guest":
        return
    groups = frappe.cache().get_value(f"authentik_groups:{user}") or []
    if not groups:
        return
    frappe.cache().delete_value(f"authentik_groups:{user}")
    user_doc = frappe.get_doc("User", user)
    _assign_roles(user_doc, groups)


def _assign_roles(user_doc, groups):
    try:
        all_profiles = {r.name for r in frappe.get_all("Role Profile")}

        for group in groups:
            if group in all_profiles:
                user_doc.role_profile_name = group
                break

        user_doc.user_type = "System User"
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(str(e)[:500], "Authentik Role Assign Error")