import frappe
from frappe import _
from frappe.utils.oauth import login_oauth_user
import requests


@frappe.whitelist(allow_guest=True)
def callback(code=None, state=None, **kwargs):
    if not code:
        frappe.throw(_("Invalid OAuth callback - no code provided"))

    social_key = frappe.get_doc("Social Login Key", "Authentik")
    base_url = social_key.base_url

    # Exchange code for token
    token_response = requests.post(
        f"{base_url}/application/o/token/",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{frappe.utils.get_url()}/api/method/custom_erp.api.authentik.callback",
            "client_id": social_key.client_id,
            "client_secret": social_key.get_password("client_secret"),
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        frappe.log_error(str(token_data)[:500], "Authentik Token Error")
        frappe.throw(_("Failed to get access token from Authentik"))

    # Fetch userinfo
    userinfo_response = requests.get(
        f"{base_url}/application/o/userinfo/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    info = userinfo_response.json()

    email = info.get("email")
    groups = info.get("groups", [])

    if not email:
        frappe.throw(_("Please ensure your Authentik profile has an email address"))

    # Store groups in cache
    frappe.cache().set_value(
        f"authentik_groups:{email}",
        groups,
        expires_in_sec=300
    )

    # Assign roles immediately if user already exists
    _assign_roles(email, groups)

    # Proceed with Frappe's standard OAuth login
    # This will create the user if not exists, then fire on_login
    login_oauth_user(info, provider="Authentik", state=state)


def _assign_roles(email, groups):
    """Assign Role Profile and System User type based on Authentik groups."""
    try:
        if not frappe.db.exists("User", email):
            return  # User not created yet, on_login hook will handle it

        if not groups:
            return

        all_profiles = {r.name for r in frappe.get_all("Role Profile")}
        user_doc = frappe.get_doc("User", email)
        changed = False

        for group in groups:
            if group in all_profiles:
                user_doc.role_profile_name = group
                changed = True
                break

        if user_doc.user_type != "System User":
            user_doc.user_type = "System User"
            changed = True

        if changed: 
            user_doc.save(ignore_permissions=True)
            frappe.db.commit()

    except Exception as e:
        frappe.log_error(str(e)[:500], "Authentik Role Assign Error")