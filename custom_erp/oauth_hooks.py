import frappe


def assign_roles_on_login(login_manager):
    user = login_manager.user
    if not user or user == "Guest":
        return

    user_doc = frappe.get_doc("User", user)

    # Check if this user logged in via Authentik
    # social_logins is a child table, not a direct field
    is_authentik = any(
        sl.provider == "Authentik"
        for sl in user_doc.get("social_logins", [])
    )

    if not is_authentik:
        return

    # Get cached OAuth userinfo
    oauth_data = (
        frappe.cache().hget("oauth2_user_info", user) or
        frappe.cache().hget("oauth2_user_info", user_doc.name) or
        {}
    )

    frappe.log_error(
        f"user={user}\noauth_data={oauth_data}",
        "Authentik OAuth Login"
    )

    groups = oauth_data.get("groups", [])
    if not groups:
        # Still fix user_type even if no groups found
        if user_doc.user_type != "System User":
            user_doc.user_type = "System User"
            user_doc.save(ignore_permissions=True)
            frappe.db.commit()
        return

    all_profiles = {r.name for r in frappe.get_all("Role Profile")}

    for group in groups:
        if group in all_profiles:
            user_doc.role_profile_name = group
            break

    user_doc.user_type = "System User"
    user_doc.save(ignore_permissions=True)
    frappe.db.commit()