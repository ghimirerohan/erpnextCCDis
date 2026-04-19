import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { frappeRequest, resourcesPlugin, setConfig } from 'frappe-ui'
import { syncCsrfFromBoot } from '@shared/frappe-boot'
import { initSocket } from '@shared/socket'
import '../index.css'

syncCsrfFromBoot()
setConfig('resourceFetcher', (options) => {
	syncCsrfFromBoot()
	return frappeRequest(options)
})

if (typeof window !== 'undefined' && typeof window.__ !== 'function') {
	window.__ = (s) => s
}

const app = createApp(App)
app.config.globalProperties.__ = window.__
app.use(router)
app.use(createPinia())
app.use(resourcesPlugin)
app.provide('$socket', initSocket())
app.mount('#app-admin')
