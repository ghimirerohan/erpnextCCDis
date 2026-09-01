"""Serve in-scope PWA files before SPA catch-all routes rewrite them to HTML."""

from werkzeug.wrappers import Response

import frappe
from custom_erp.pwa_assets import load_pwa_asset, parse_pwa_asset_path


class PWAAssetRenderer:
	def __init__(self, path, http_status_code=None):
		self.path = path
		self.http_status_code = http_status_code or 200
		self.parsed = parse_pwa_asset_path(self._request_path()) or self._from_rewritten_subpath()

	def _request_path(self) -> str:
		candidates = []
		# resolve_path stores the pre-rewrite path on frappe.local.path
		candidates.append(getattr(frappe.local, "path", "") or "")
		try:
			candidates.append(getattr(frappe.request, "path", "") or "")
		except Exception:
			pass
		candidates.append(self.path or "")
		for candidate in candidates:
			if parse_pwa_asset_path(candidate):
				return candidate
		return candidates[0] if candidates else ""

	def _from_rewritten_subpath(self):
		"""website_route_rules map /{app}/<path:subpath> to endpoint {app} and put the file in form_dict.subpath."""
		app = (self.path or "").strip("/")
		try:
			sub = frappe.form_dict.get("subpath")
		except Exception:
			sub = None
		if not app or not sub:
			return None
		return parse_pwa_asset_path(f"{app}/{sub}")

	def can_render(self):
		return self.parsed is not None

	def render(self):
		app_name, filename = self.parsed
		body, mime, extra = load_pwa_asset(app_name, filename)
		headers = {"Content-Type": mime, **extra}
		return Response(body, status=200, headers=headers)
