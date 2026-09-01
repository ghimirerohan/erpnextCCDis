"""
PWA API fallbacks. Prefer in-scope `/{app}/manifest.json` and `/{app}/sw.js`
served by PWAAssetRenderer. These whitelist methods stay for older clients
and must return *raw* bytes (not Frappe `{message: ...}` JSON wrapping).
"""

import frappe
from custom_erp.pwa_assets import load_pwa_asset, sanitize_app_name


def _send_binary(body: bytes, filename: str, mime: str, extra_headers: dict | None = None):
	frappe.local.response_headers["Content-Type"] = mime
	for key, value in (extra_headers or {}).items():
		frappe.local.response_headers[key] = value
	frappe.response["type"] = "binary"
	frappe.response["filecontent"] = body
	frappe.response["filename"] = filename


@frappe.whitelist(allow_guest=True)
def get_service_worker(app_name=None):
	app_name = sanitize_app_name(app_name)
	if not app_name:
		frappe.throw("Unknown PWA app", frappe.DoesNotExistError)
	body, mime, extra = load_pwa_asset(app_name, "sw.js")
	_send_binary(body, "sw.js", mime, extra)


@frappe.whitelist(allow_guest=True)
def get_manifest(app_name=None):
	app_name = sanitize_app_name(app_name)
	if not app_name:
		frappe.throw("Unknown PWA app", frappe.DoesNotExistError)
	body, mime, extra = load_pwa_asset(app_name, "manifest.json")
	_send_binary(body, "manifest.json", mime, extra)
