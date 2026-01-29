# Vue WebApp Templates

Complete file templates for creating a new Vue app. Replace `my-app`, `MyApp`, and theme colors as needed.

---

## index.html

**Location**: `my-app/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <title>My App - Your Description Here</title>
    <meta name="description" content="Your app description" />
    <meta name="application-name" content="My App" />
    <meta name="theme-color" content="#3b82f6" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <link rel="manifest" href="/manifest-my-app.json" />
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="./src/main.js"></script>
  </body>
</html>
```

---

## main.js

**Location**: `my-app/src/main.js`

```javascript
import { createApp } from "vue"
import { setConfig, frappeRequest, resourcesPlugin } from "frappe-ui"
import App from "./App.vue"
import router from "./router"
import "../../../shared/index.css"

// Configure frappe-ui
setConfig("resourceFetcher", frappeRequest)

const app = createApp(App)
app.use(resourcesPlugin)
app.use(router)
app.mount("#app")
```

---

## App.vue

**Location**: `my-app/src/App.vue`

Replace `my-app` and `#3b82f6` (theme color) as needed.

```vue
<template>
  <div class="app-container">
    <router-view />
    <PWAInstallPrompt />
    <PWAUpdatePrompt />
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import PWAInstallPrompt from '../../shared/components/PWAInstallPrompt.vue'
import PWAUpdatePrompt from '../../shared/components/PWAUpdatePrompt.vue'

const route = useRoute()

const updateManifest = () => {
  // Use API endpoint for manifest with proper headers
  const manifestPath = '/api/method/custom_erp.api.pwa.get_manifest?app_name=my-app'
  
  const existingLinks = document.querySelectorAll('link[rel="manifest"]')
  existingLinks.forEach(link => link.remove())
  
  const link = document.createElement('link')
  link.rel = 'manifest'
  link.href = manifestPath
  document.head.appendChild(link)
  
  let themeMeta = document.querySelector('meta[name="theme-color"]')
  if (!themeMeta) {
    themeMeta = document.createElement('meta')
    themeMeta.name = 'theme-color'
    document.head.appendChild(themeMeta)
  }
  themeMeta.content = '#3b82f6'  // Your theme color
}

watch(() => route.name, () => {
  updateManifest()
})

onMounted(() => {
  updateManifest()
  
  const manifestLink = document.querySelector('link[rel="manifest"]')
  if (manifestLink) {
    console.log(`📱 PWA Manifest loaded: ${manifestLink.href} for app: my-app`)
  }
})
</script>

<style>
html {
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
}

body {
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

@media (max-width: 768px) {
  html {
    scroll-padding-top: 80px;
  }
  
  input[type="text"],
  input[type="number"],
  input[type="email"],
  input[type="tel"],
  input[type="search"],
  select,
  textarea {
    font-size: 16px !important;
  }
}
</style>
```

---

## router.js

**Location**: `my-app/src/router.js`

Replace `my-app`, `MyApp` as needed.

```javascript
import { userResource, setAuthErrorCallback } from "../../shared/data/user"
import { createRouter, createWebHistory } from 'vue-router'
import { session, setNavigationCallbacks } from '../../shared/data/session'
import MyApp from './MyApp.vue'
import Login from '../../shared/components/Login.vue'

const routes = [
  {
    path: "/",
    name: "MyApp",
    component: MyApp,
    meta: { requiresAuth: true }
  },
  {
    name: "Login",
    path: "/login",
    component: Login,
  },
  // Add more routes as needed:
  // {
  //   path: '/other-page',
  //   name: 'OtherPage',
  //   component: () => import('./OtherPage.vue'),
  //   meta: { requiresAuth: true }
  // }
]

const router = createRouter({
  history: createWebHistory("/my-app"),  // MUST match your URL path
  routes,
})

let intendedRoute = null

setAuthErrorCallback(() => {
  if (router.currentRoute.value.name !== "Login") {
    intendedRoute = router.currentRoute.value.fullPath
    router.replace({ name: "Login" })
  }
})

setNavigationCallbacks({
  onLoginSuccess: (defaultRoute) => {
    // Use intended route if available, otherwise go to app root
    let targetRoute = intendedRoute || "/"
    
    // If defaultRoute is provided and it's within our app scope
    if (defaultRoute && defaultRoute.startsWith('/my-app')) {
      // Extract relative path from /my-app/...
      targetRoute = defaultRoute.replace('/my-app', '') || "/"
    }
    
    intendedRoute = null
    router.replace(targetRoute)
  },
  onLogoutSuccess: () => {
    router.replace({ name: "Login" })
  },
})

router.beforeEach(async (to, from, next) => {
  if (to.name !== "Login" && from.name !== "Login") {
    intendedRoute = to.fullPath
  }

  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
    if (error?.exc_type === "AuthenticationError" && to.name !== "Login") {
      intendedRoute = to.fullPath
      next({ name: "Login" })
      return
    }
  }

  if (to.name === "Login" && isLoggedIn) {
    next(intendedRoute || { name: "MyApp" })
    intendedRoute = null
  } else if (to.name !== "Login" && !isLoggedIn) {
    intendedRoute = to.fullPath
    next({ name: "Login" })
  } else {
    next()
  }
})

export default router
```

---

## Main Component (MyApp.vue)

**Location**: `my-app/src/MyApp.vue`

Basic template with header and content area. Customize as needed.

```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-500">Welcome</p>
            <h1 class="text-xl sm:text-2xl font-bold text-gray-900">My App</h1>
          </div>
          <div class="flex gap-3">
            <button
              @click="refresh"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6">
      <!-- Dashboard Cards -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Dashboard</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p class="text-sm text-blue-600 font-medium">Metric 1</p>
            <p class="text-2xl font-bold text-blue-700">{{ data.metric1 }}</p>
          </div>
          <div class="p-4 bg-green-50 rounded-lg border border-green-200">
            <p class="text-sm text-green-600 font-medium">Metric 2</p>
            <p class="text-2xl font-bold text-green-700">{{ data.metric2 }}</p>
          </div>
        </div>
      </section>

      <!-- Content Section -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Content</h2>
        <p class="text-gray-600">Your main content goes here.</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

// Reactive data
const data = ref({
  metric1: 0,
  metric2: 0
})

// API Resource example
const dataResource = createResource({
  url: 'custom_erp.api.my_app.get_data',
  auto: false,
  onSuccess: (response) => {
    data.value = response
  }
})

// Methods
const refresh = () => {
  dataResource.fetch()
}

// Lifecycle
onMounted(() => {
  refresh()
})
</script>
```

---

## Frappe WWW HTML

**Location**: `custom_erp/www/my-app.html`

This is a placeholder. The build process (`node build-apps.js`) will update it with correct asset hashes.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/assets/custom_erp/frontend/my-app/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <title>My App - Description</title>
    <meta name="description" content="Your app description" />
    <meta name="application-name" content="My App" />
    <meta name="theme-color" content="#3b82f6" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <link rel="manifest" href="/api/method/custom_erp.api.pwa.get_manifest?app_name=my-app" />
    <!-- Asset references will be added by build process -->
  </head>
  <body>
    <div id="app"></div>
  
          <script>
              {% for key in boot %}
              window["{{ key }}"] = {{ boot[key] | tojson }};
              {% endfor %}
          </script>
          </body>
          
</html>
```

---

## Frappe WWW Python

**Location**: `custom_erp/www/my_app.py`

**NOTE**: Filename uses underscores, not hyphens!

```python
import frappe

def get_context(context):
    """Context for my-app"""
    context.no_cache = 1
    return context
```

---

## PWA Manifest

**Location**: `public/manifest-my-app.json`

```json
{
  "id": "/my-app/",
  "name": "My App",
  "short_name": "MyApp",
  "description": "Your app description",
  "start_url": "/my-app/",
  "scope": "/my-app/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": [
    {
      "src": "/assets/custom_erp/icons/my-app/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/custom_erp/icons/my-app/icon-512x512.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["business", "finance"],
  "prefer_related_applications": false
}
```

---

## Backend API (Optional)

**Location**: `custom_erp/api/my_app.py`

```python
import frappe
from typing import Dict, Any, Optional, List

@frappe.whitelist()
def get_data(param: Optional[str] = None) -> Dict[str, Any]:
    """
    Get data for my-app.
    
    Args:
        param: Optional filter parameter
        
    Returns:
        Dict with data
    """
    user = frappe.session.user
    
    # Your logic here
    result = {
        "metric1": 100,
        "metric2": 50,
        "items": []
    }
    
    return result


@frappe.whitelist()
def create_record(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new record.
    
    Args:
        data: Record data
        
    Returns:
        Dict with created record info
    """
    # Validate and create
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        **data
    })
    doc.insert()
    frappe.db.commit()
    
    return {"name": doc.name, "status": "created"}
```
