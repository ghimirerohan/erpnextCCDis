import frappe


def assign_roles_on_login(login_manager):
    user = login_manager.user
    if not user or user == "Guest":
        return

    # Dump ALL keys in the oauth2_user_info hash
    all_oauth_cache = frappe.cache().hgetall("oauth2_user_info") or {}

    frappe.log_error(
        f"user={user}\nall_oauth_keys={list(all_oauth_cache.keys())}\nall_oauth_data={all_oauth_cache}",
        "Authentik Cache Dump"
    )