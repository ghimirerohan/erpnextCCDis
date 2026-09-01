"""In-scope PWA assets for custom_erp Vue SPAs.

Chrome / Safari will not install an app when the manifest is served from
`/api/method/...` (out of scope, and Frappe wraps whitelist JSON as
`{"message": ...}`). Serve raw `/{app}/manifest.json` and `/{app}/sw.js`.
"""

from __future__ import annotations

import json
import os

import frappe

PWA_SPA_APPS = (
	"qrpay",
	"qrpay-horlicks",
	"qrpay-admin",
	"scanner",
	"pay-dashboard",
	"uploadsales",
	"uploadreco",
	"dailyrecoentry",
	"dailytrnxs",
	"home",
	"testlogin",
	"ai-assistant",
	"emp-attendance",
)

APP_THEMES = {
	"qrpay": {"theme": "#10b981", "bg": "#ffffff", "name": "QRPay", "desc": "Dynamic Fonepay QR Code Generator"},
	"qrpay-horlicks": {
		"theme": "#f97316",
		"bg": "#ffffff",
		"name": "QRPay Horlicks",
		"desc": "Horlicks Fonepay QR Code Generator",
	},
	"qrpay-admin": {"theme": "#7c3aed", "bg": "#ffffff", "name": "QRPay Admin", "desc": "QRPay Administration Dashboard"},
	"scanner": {"theme": "#f59e0b", "bg": "#ffffff", "name": "Scanner", "desc": "Invoice and Document Scanner"},
	"pay-dashboard": {"theme": "#2563eb", "bg": "#ffffff", "name": "Pay Dashboard", "desc": "Payment Statistics Dashboard"},
	"uploadsales": {"theme": "#059669", "bg": "#ffffff", "name": "Upload Sales", "desc": "Upload and Process Sales Data"},
	"uploadreco": {"theme": "#dc2626", "bg": "#ffffff", "name": "Upload Reco", "desc": "Upload Reconciliation Data"},
	"dailyrecoentry": {"theme": "#0891b2", "bg": "#ffffff", "name": "Daily Reco", "desc": "Daily Reconciliation Entry"},
	"dailytrnxs": {
		"theme": "#7c3aed",
		"bg": "#ffffff",
		"name": "Daily Transactions",
		"desc": "Daily Payment Reconciliation Dashboard",
	},
	"home": {"theme": "#6366f1", "bg": "#ffffff", "name": "Home", "desc": "Application Home"},
	"testlogin": {"theme": "#64748b", "bg": "#ffffff", "name": "Test Login", "desc": "Login Test App"},
	"ai-assistant": {"theme": "#7c3aed", "bg": "#1e293b", "name": "Bidhi", "desc": "AI Voice ERP Assistant"},
	"emp-attendance": {
		"theme": "#059669",
		"bg": "#ffffff",
		"name": "Employee Attendance",
		"desc": "Employee Attendance Tracking and Management",
	},
}

MINIMAL_SW = """\
// custom_erp PWA service worker (installability fallback)
const CACHE_NAME = '{app}-cache-pwa';
self.addEventListener('install', (event) => {{
	event.waitUntil(self.skipWaiting());
}});
self.addEventListener('activate', (event) => {{
	event.waitUntil(self.clients.claim());
}});
self.addEventListener('fetch', (event) => {{
	if (event.request.method !== 'GET') return;
	event.respondWith(
		fetch(event.request).catch(() => caches.match(event.request))
	);
}});
"""


def sanitize_app_name(app_name: str | None) -> str:
	name = (app_name or "home").replace("..", "").replace("/", "").replace("\\", "")
	return name if name in PWA_SPA_APPS else ""


def parse_pwa_asset_path(path: str | None) -> tuple[str, str] | None:
	"""Return (app_name, filename) for in-scope PWA assets, else None."""
	if not path:
		return None
	parts = [p for p in path.strip("/").split("/") if p]
	if len(parts) != 2:
		return None
	app_name, filename = parts
	if app_name not in PWA_SPA_APPS:
		return None
	if filename == "manifest.json":
		return app_name, "manifest.json"
	if filename in ("sw.js", f"sw-{app_name}.js"):
		return app_name, "sw.js"
	return None


def build_manifest(app_name: str) -> dict:
	theme = APP_THEMES.get(app_name) or APP_THEMES["home"]
	icon_base = f"/assets/custom_erp/frontend/icons/{app_name}"
	legacy_icon = f"/assets/custom_erp/icons/{app_name}/icon-512x512.png"
	icon_192 = f"{icon_base}/icon-192x192.png"
	icon_512 = f"{icon_base}/icon-512x512.png"
	if not _public_file_exists(f"frontend/icons/{app_name}/icon-192x192.png"):
		icon_192 = legacy_icon
	if not _public_file_exists(f"frontend/icons/{app_name}/icon-512x512.png"):
		icon_512 = legacy_icon
	short_name = theme["name"].replace(" ", "")[:12]
	return {
		"id": f"/{app_name}/",
		"name": theme["name"],
		"short_name": short_name,
		"description": theme["desc"],
		"start_url": f"/{app_name}/",
		"scope": f"/{app_name}/",
		"display": "standalone",
		"display_override": ["standalone", "minimal-ui", "browser"],
		"orientation": "portrait-primary",
		"background_color": theme["bg"],
		"theme_color": theme["theme"],
		"lang": "en",
		"dir": "ltr",
		"icons": [
			{"src": icon_192, "sizes": "192x192", "type": "image/png", "purpose": "any"},
			{"src": icon_512, "sizes": "512x512", "type": "image/png", "purpose": "any"},
			{"src": icon_192, "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
			{"src": icon_512, "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
		],
		"categories": ["business", "finance"],
		"prefer_related_applications": False,
	}


def load_pwa_asset(app_name: str, filename: str) -> tuple[bytes, str, dict[str, str]]:
	"""Return (body, mime, extra_headers) for a PWA asset."""
	if filename == "manifest.json":
		body = _load_manifest_bytes(app_name)
		return body, "application/manifest+json; charset=utf-8", {
			"Cache-Control": "no-cache, no-store, must-revalidate",
		}
	body = _load_sw_bytes(app_name)
	return body, "application/javascript; charset=utf-8", {
		"Service-Worker-Allowed": f"/{app_name}/",
		"Cache-Control": "no-cache, no-store, must-revalidate",
	}


def _public_file_exists(relative: str) -> bool:
	path = frappe.get_app_path("custom_erp", "public", *relative.split("/"))
	return os.path.isfile(path)


def _read_public_bytes(relative: str) -> bytes | None:
	path = frappe.get_app_path("custom_erp", "public", *relative.split("/"))
	if os.path.isfile(path):
		with open(path, "rb") as f:
			return f.read()
	return None


def _load_manifest_bytes(app_name: str) -> bytes:
	raw = _read_public_bytes(f"frontend/{app_name}/manifest.json")
	if raw:
		try:
			data = json.loads(raw.decode("utf-8"))
			# Force in-scope identity even if an older build leaked an API URL.
			data["id"] = f"/{app_name}/"
			data["start_url"] = f"/{app_name}/"
			data["scope"] = f"/{app_name}/"
			data["display"] = data.get("display") or "standalone"
			if data.get("display") not in ("standalone", "fullscreen", "minimal-ui"):
				data["display"] = "standalone"
			return json.dumps(data, indent=2).encode("utf-8")
		except (ValueError, UnicodeDecodeError):
			pass
	legacy = _read_public_bytes(f"manifest-{app_name}.json")
	if legacy:
		try:
			data = json.loads(legacy.decode("utf-8"))
			data["id"] = f"/{app_name}/"
			data["start_url"] = f"/{app_name}/"
			data["scope"] = f"/{app_name}/"
			data["display"] = "standalone"
			return json.dumps(data, indent=2).encode("utf-8")
		except (ValueError, UnicodeDecodeError):
			pass
	return json.dumps(build_manifest(app_name), indent=2).encode("utf-8")


def _load_sw_bytes(app_name: str) -> bytes:
	raw = _read_public_bytes(f"frontend/{app_name}/sw.js")
	if raw:
		return raw
	return MINIMAL_SW.format(app=app_name).encode("utf-8")
