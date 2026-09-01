import { createApp } from "vue"
import { registerScopedSW } from "../../shared/register-sw"
import { checkPWAInstallability } from "../../shared/pwa-installability"
import { ensureInScopeManifest } from "../../shared/pwa-manifest"

// IMPORTANT: Set auth callback BEFORE importing router or userResource
// This prevents frappe-ui from doing default redirects
import { setAuthErrorCallback } from "../../shared/data/user"

// Set auth callback immediately to prevent default redirects
setAuthErrorCallback(() => {
	const currentPath = window.location.pathname
	const match = currentPath.match(/^\/([^\/]+)/)
	if (match) {
		const appName = match[1]
		if (!currentPath.includes('/login')) {
			// Prevent any default redirects by handling it ourselves
			window.location.href = `/${appName}/login`
		}
	}
})

import App from "./App.vue"
import { initSocket } from "../../shared/socket"

import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	FeatherIcon,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "../../shared/assets/index.css"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
	FeatherIcon,
}

const app = createApp(App)

const getBaseURL = () => {
	if (window.frappe?.boot?.api_key) {
		return window.frappe.boot.sites?.[0] || window.location.origin
	}
	return window.location.origin
}

setConfig("resourceFetcher", (options) => {
	return frappeRequest({
		...options,
		baseURL: getBaseURL(),
		headers: {
			...options.headers,
			...(window.site_name && { "X-Frappe-Site-Name": window.site_name }),
		},
	}).catch((error) => {
		// Intercept authentication errors and prevent default redirects
		if (error && (error.exc_type === "AuthenticationError" || error.status === 401 || error.status === 403)) {
			const currentPath = window.location.pathname
			const match = currentPath.match(/^\/([^\/]+)/)
			if (match) {
				const appName = match[1]
				if (!currentPath.includes('/login') && !currentPath.includes('/account/login')) {
					// Prevent default redirect, handle it ourselves
					window.location.replace(`/${appName}/login`)
					return Promise.reject(error) // Don't continue with default handling
				}
			}
		}
		// Re-throw other errors
		return Promise.reject(error)
	})
})

app.use(resourcesPlugin)
app.use(pageMetaPlugin)

const socket = initSocket()
app.config.globalProperties.$socket = socket
// Also expose on window for App.vue access to frappe.realtime
window.$socket = socket

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.mount("#app")

ensureInScopeManifest()
registerScopedSW().then(() => {
  setTimeout(() => checkPWAInstallability(), 1500)
}).catch((err) => {
  console.error("Service Worker registration failed:", err)
})
