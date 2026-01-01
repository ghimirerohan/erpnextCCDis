import { createResource } from "frappe-ui"

// Navigation callback for authentication errors
let authErrorCallback = null

export function setAuthErrorCallback(callback) {
	authErrorCallback = callback
}

export const userResource = createResource({
	url: "frappe.auth.get_logged_user",
	cache: "User",
	onError(error) {
		// Prevent any default redirects from frappe-ui
		if (error && (error.exc_type === "AuthenticationError" || error.status === 401 || error.status === 403)) {
			// Always use our callback to prevent default redirects
			if (authErrorCallback) {
				authErrorCallback()
			} else {
				// Fallback: detect app from URL and redirect to app's login
				const path = window.location.pathname
				// List of known app names (exclude common Frappe paths)
				const appNames = ['qrpay', 'qrpay-admin', 'scanner', 'pay-dashboard', 'uploadsales', 'uploadreco', 'dailyrecoentry', 'dailytrnxs', 'home', 'testlogin', 'emp-attendance']
				const match = path.match(/^\/([^\/]+)/)
				if (match && appNames.includes(match[1])) {
					const appName = match[1]
					if (!path.includes('/login') && !path.includes('/account/login')) {
						// Use replace to prevent back button issues
						window.location.replace(`/${appName}/login`)
					}
				}
			}
			// Prevent default error handling that might cause redirects
			return false
		}
	},
})
