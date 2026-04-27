import frappe


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

    # Use our own cache key set in the callback
    groups = frappe.cache().get_value(f"authentik_groups:{user}") or []

    frappe.log_error(
        f"user={user}\ngroups={groups}",
        "Authentik Role Assignment"
    )

    all_profiles = {r.name for r in frappe.get_all("Role Profile")}

    for group in groups:
        if group in all_profiles:
            user_doc.role_profile_name = group
            break

    user_doc.user_type = "System User"
    user_doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Clear cache after use
    frappe.cache().delete_value(f"authentik_groups:{user}")