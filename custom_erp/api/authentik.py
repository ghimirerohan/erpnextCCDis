import frappe
from frappe import _
from frappe.utils.oauth import login_oauth_user
import requests


@frappe.whitelist(allow_guest=True)
def callback(code=None, state=None, **kwargs):
    """Custom Authentik OAuth callback that captures groups before login."""
    if not code:
        frappe.throw(_("Invalid OAuth callback - no code provided"))

    # Get Social Login Key config
    social_key = frappe.get_doc("Social Login Key", "Authentik")
    base_url = social_key.base_url  # https://auth.pnishana.com.np

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
        frappe.log_error(str(token_data), "Authentik Token Error")
        frappe.throw(_("Failed to get access token from Authentik"))

    # Fetch userinfo (includes groups)
    userinfo_response = requests.get(
        f"{base_url}/application/o/userinfo/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    info = userinfo_response.json()

    frappe.log_error(str(info), "Authentik Userinfo")

    email = info.get("email")
    groups = info.get("groups", [])

    if not email:
        frappe.throw(_("Please ensure your Authentik profile has an email address"))

    # Store groups in cache — keyed by email, lasts 5 minutes
    frappe.cache().set_value(
        f"authentik_groups:{email}",
        groups,
        expires_in_sec=300
    )

    # Proceed with Frappe's standard OAuth login
    login_oauth_user(info, provider="Authentik", state=state)