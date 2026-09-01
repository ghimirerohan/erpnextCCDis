import json

import frappe

from custom_erp.pwa_assets import (
	PWA_SPA_APPS,
	build_manifest,
	load_pwa_asset,
	parse_pwa_asset_path,
	sanitize_app_name,
)
from custom_erp.pwa_renderer import PWAAssetRenderer


def test_parse_in_scope_paths():
	assert parse_pwa_asset_path("/dailyrecoentry/manifest.json") == ("dailyrecoentry", "manifest.json")
	assert parse_pwa_asset_path("/dailytrnxs/sw.js") == ("dailytrnxs", "sw.js")
	assert parse_pwa_asset_path("/uploadreco/sw-uploadreco.js") == ("uploadreco", "sw.js")
	assert parse_pwa_asset_path("/dailyrecoentry/login") is None
	assert parse_pwa_asset_path("/api/method/custom_erp.api.pwa.get_manifest") is None
	assert parse_pwa_asset_path("/unknown-app/manifest.json") is None


def test_sanitize_app_name():
	assert sanitize_app_name("dailyrecoentry") == "dailyrecoentry"
	assert sanitize_app_name("../etc") == ""
	assert sanitize_app_name("not-an-app") == ""


def test_manifest_is_installable():
	for app in ("dailyrecoentry", "dailytrnxs", "uploadreco"):
		manifest = build_manifest(app)
		assert manifest["display"] == "standalone"
		assert manifest["start_url"] == f"/{app}/"
		assert manifest["scope"] == f"/{app}/"
		assert manifest["id"] == f"/{app}/"
		sizes = {icon["sizes"] for icon in manifest["icons"]}
		assert "192x192" in sizes
		assert "512x512" in sizes
		assert all(icon["purpose"] in ("any", "maskable") for icon in manifest["icons"])


def test_load_manifest_is_raw_json():
	body, mime, extra = load_pwa_asset("dailyrecoentry", "manifest.json")
	assert "application/manifest+json" in mime
	data = json.loads(body.decode("utf-8"))
	assert "name" in data
	assert "message" not in data
	assert data["scope"] == "/dailyrecoentry/"


def test_load_sw_has_fetch_handler():
	body, mime, extra = load_pwa_asset("dailyrecoentry", "sw.js")
	assert "javascript" in mime
	assert extra.get("Service-Worker-Allowed") == "/dailyrecoentry/"
	assert "fetch" in body.decode("utf-8")


def test_renderer_matches_request_path():
	frappe.local.request = frappe._dict(path="/dailyrecoentry/manifest.json")
	renderer = PWAAssetRenderer("dailyrecoentry")
	assert renderer.can_render()
	response = renderer.render()
	assert response.status_code == 200
	assert "application/manifest+json" in response.headers.get("Content-Type", "")
	payload = json.loads(response.get_data(as_text=True))
	assert payload.get("start_url") == "/dailyrecoentry/"
	assert "dailyrecoentry" in PWA_SPA_APPS
