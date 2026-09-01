import { createApp } from "vue"
import { registerScopedSW } from "../../shared/register-sw"
import { checkPWAInstallability } from "../../shared/pwa-installability"

import App from "./App.vue"
import router from "./router"
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
}

const app = createApp(App)

// Configure frappeRequest with proper base URL and CSRF handling
const getBaseURL = () => {
	if (window.frappe?.boot?.api_key) {
		return window.frappe.boot.sites?.[0] || window.location.origin
	}
	const origin = window.location.origin
	return origin
}

setConfig("resourceFetcher", (options) => {
	return frappeRequest({
		...options,
		baseURL: getBaseURL(),
		headers: {
			...options.headers,
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

registerScopedSW().then(() => {
  setTimeout(() => {
    checkPWAInstallability();
  }, 1500);
}).catch(err => {
  console.error('❌ Service Worker registration failed:', err);
  setTimeout(() => {
    checkPWAInstallability();
  }, 1000);
})

