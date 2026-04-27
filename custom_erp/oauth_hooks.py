import frappe


def assign_roles_on_login(login_manager):
    user = login_manager.user
    if not user or user == "Guest":
        return

    user_doc = frappe.get_doc("User", user)

    # Log EVERYTHING — no conditions yet
    social_logins = [
        {"provider": sl.provider, "userid": sl.userid}
        for sl in user_doc.get("social_logins", [])
    ]

    oauth_data_by_name = frappe.cache().hget("oauth2_user_info", user) or {}
    oauth_data_by_email = frappe.cache().hget("oauth2_user_info", user_doc.email) or {}

    frappe.log_error(
        f"user={user}\n"
        f"user_type={user_doc.user_type}\n"
        f"social_logins={social_logins}\n"
        f"oauth_by_name={oauth_data_by_name}\n"
        f"oauth_by_email={oauth_data_by_email}",
        "Authentik Debug"
    )