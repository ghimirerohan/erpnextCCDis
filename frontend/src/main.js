import { createApp } from "vue"
// ADDED BY AI: MULTI_PWA - Import scoped service worker registration
import { registerScopedSW } from "./register-sw"
// ADDED BY AI: PWA Installability - Check and debug PWA installability
import { checkPWAInstallability } from "./pwa-installability"

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"

import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "./index.css"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
}

const app = createApp(App)

// Configure frappeRequest with proper base URL and CSRF handling
// For PWA apps running under /jsapp/, API calls should still go to root /
const getBaseURL = () => {
	// Use boot data if available, otherwise detect from current location
	if (window.frappe?.boot?.api_key) {
		return window.frappe.boot.sites?.[0] || window.location.origin
	}
	// For PWA apps, API calls go to root, not /jsapp/
	const origin = window.location.origin
	return origin
}

// Configure frappeRequest with base URL
setConfig("resourceFetcher", (options) => {
	return frappeRequest({
		...options,
		baseURL: getBaseURL(),
		headers: {
			...options.headers,
			// CSRF token is automatically handled by frappe-ui via cookies
			// But ensure we're using the correct site name
			...(window.site_name && { "X-Frappe-Site-Name": window.site_name }),
		},
	})
})

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

const socket = initSocket()
app.config.globalProperties.$socket = socket

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.mount("#app")

// ADDED BY AI: MULTI_PWA - Register scoped service worker
registerScopedSW().then((registration) => {
  if (registration) {
    // If service worker is registered but not controlling, reload after a delay
    if (!navigator.serviceWorker.controller && registration.active) {
      console.log('🔄 Service Worker registered but not controlling. Reloading in 2 seconds...');
      setTimeout(() => {
        // Only reload if still not controlling (first visit)
        if (!navigator.serviceWorker.controller) {
          window.location.reload();
        }
      }, 2000);
    }
  }
  
  // Check PWA installability after service worker registration
  // Delay slightly to ensure manifest is loaded
  setTimeout(() => {
    checkPWAInstallability();
  }, 1500);
}).catch(err => {
  console.error('❌ Service Worker registration failed:', err);
  // Still check installability even if SW fails
  setTimeout(() => {
    checkPWAInstallability();
  }, 1000);
})
