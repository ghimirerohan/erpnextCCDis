/**
 * Website /portal boot: `field-app.html` / `admin-app.html` inject `window.session_user`,
 * `window.user_roles`, `window.csrf_token` from `get_context` (see www/*.py).
 * Desk sets `window.__` and CSRF differently; keep this in sync with `frappeRequest`.
 */

export const FIELD_APP_ROLES = ['Field User', 'CC Admin', 'System Manager', 'Administrator']

/** Admin SPA: supervisors; Field User alone uses /field-app. */
export const ADMIN_APP_ROLES = ['CC Admin', 'System Manager', 'Administrator']

export function syncCsrfFromBoot() {
	if (typeof window === 'undefined') return
	const t = window.csrf_token || window.frappe?.csrf_token
	if (t && typeof t === 'string' && t.length && t !== '{{ csrf_token }}') {
		window.csrf_token = t
	}
}

export function websiteLoginUrl(redirectFullPath) {
	const path =
		redirectFullPath || `${window.location.pathname}${window.location.search || ''}`
	return `/login?redirect-to=${encodeURIComponent(path)}`
}

/**
 * @param {{ roles: string[] }} opts
 * @returns {{ ok: true } | { ok: false, reason: 'guest' | 'role' }}
 */
export function ensureWebsiteAuth(opts) {
	syncCsrfFromBoot()
	const user = typeof window !== 'undefined' ? window.session_user : null
	if (!user || user === 'Guest') {
		return { ok: false, reason: 'guest' }
	}
	const userRoles = (typeof window !== 'undefined' && window.user_roles) || []
	const allowed = opts.roles || []
	const ok = userRoles.some((r) => allowed.includes(r))
	if (!ok) {
		return { ok: false, reason: 'role' }
	}
	return { ok: true }
}
