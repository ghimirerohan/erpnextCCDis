import frappe


def on_user_insert(doc, method):
    """Fires when any User is created — catches new Authentik SSO users."""
    groups = frappe.cache().get_value(f"authentik_groups:{doc.name}") or []

    frappe.log_error(
        f"INSERT: user={doc.name} | groups={groups}",
        "Authentik User Insert"
    )

    if not groups:
        return

    _assign_roles(doc, groups)


def on_user_update(doc, method):
    """Fires on every User save — catches returning Authentik users."""
    groups = frappe.cache().get_value(f"authentik_groups:{doc.name}") or []

    if not groups:
        return

    frappe.log_error(
        f"UPDATE: user={doc.name} | groups={groups}",
        "Authentik User Update"
    )

    _assign_roles(doc, groups)


def assign_roles_on_login(login_manager):
    """on_login hook — fallback for existing users."""
    user = login_manager.user
    if not user or user == "Guest":
        return

    groups = frappe.cache().get_value(f"authentik_groups:{user}") or []

    frappe.log_error(
        f"LOGIN: user={user} | groups={groups}",
        "Authentik On Login"
    )

    if not groups:
        return

    user_doc = frappe.get_doc("User", user)
    _assign_roles(user_doc, groups)


def _assign_roles(user_doc, groups):
    """Core assignment logic."""
    try:
        all_profiles = {r.name for r in frappe.get_all("Role Profile")}

        for group in groups:
            if group in all_profiles:
                user_doc.role_profile_name = group
                break

        user_doc.user_type = "System User"
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Clear cache after successful assignment
        frappe.cache().delete_value(f"authentik_groups:{user_doc.name}")

        frappe.log_error(
            f"ASSIGNED: user={user_doc.name} | profile={user_doc.role_profile_name}",
            "Authentik Role Assigned"
        )

    except Exception as e:
        frappe.log_error(str(e)[:500], "Authentik Role Assign Error")