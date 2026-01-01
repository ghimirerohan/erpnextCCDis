import { createApp } from "vue"
import { registerScopedSW } from "../../shared/register-sw"
import { checkPWAInstallability } from "../../shared/pwa-installability"

// IMPORTANT: Set auth callback BEFORE importing router or userResource
import { setAuthErrorCallback } from "../../shared/data/user"

// Set auth callback immediately to prevent default redirects
setAuthErrorCallback(() => {
  const currentPath = window.location.pathname
  const match = currentPath.match(/^\/([^\/]+)/)
  if (match) {
    const appName = match[1]
    if (!currentPath.includes('/login')) {
      window.location.href = `/${appName}/login`
    }
  }
})

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
    if (error && (error.exc_type === "AuthenticationError" || error.status === 401 || error.status === 403)) {
      const currentPath = window.location.pathname
      const match = currentPath.match(/^\/([^\/]+)/)
      if (match) {
        const appName = match[1]
        if (!currentPath.includes('/login') && !currentPath.includes('/account/login')) {
          window.location.replace(`/${appName}/login`)
          return Promise.reject(error)
        }
      }
    }
    return Promise.reject(error)
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

registerScopedSW().then((registration) => {
  if (registration) {
    if (!navigator.serviceWorker.controller && registration.active) {
      setTimeout(() => {
        if (!navigator.serviceWorker.controller) {
          window.location.reload();
        }
      }, 2000);
    }
  }
  setTimeout(() => {
    checkPWAInstallability();
  }, 1500);
}).catch(err => {
  console.error('Service Worker registration failed:', err);
  setTimeout(() => {
    checkPWAInstallability();
  }, 1000);
})

