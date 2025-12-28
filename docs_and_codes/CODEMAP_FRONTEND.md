# Custom ERP - Frontend Architecture (Vue.js 3)

## Directory Structure

```
frontend/
├── src/
│   ├── apps/uploadsales/        # Bulk import feature
│   ├── components/              # Shared components
│   ├── pages/                   # Route pages
│   ├── data/                    # Data layer (session, user)
│   ├── router.js                # Vue Router config
│   ├── main.js                  # App entry point
│   ├── App.vue                  # Root component
│   ├── socket.js                # WebSocket client
│   ├── register-sw.js           # Service worker registration
│   └── pwa-installability.js    # PWA install detection
├── public/                      # PWA assets (manifests, icons)
├── vite.config.js               # Build config
└── package.json                 # Dependencies
```

## Technology Stack

- **Vue.js 3**: Composition API, `<script setup>`
- **Vue Router 4**: Client-side routing
- **Frappe UI**: Component library + resource management
- **Vite 5**: Build tool
- **Tailwind CSS 3**: Styling
- **Socket.IO**: Real-time communication
- **Workbox**: Service worker/PWA

## Key Pages

### 1. Home.vue - Sales Invoice Dashboard
**Route**: `/`

Features:
- Customer selection (list/QR/photo)
- Date range filtering
- Bill-wise and summary views
- Real-time data loading

### 2. QRPay.vue - Payment Interface
**Route**: `/qrpay`

Features:
- Customer search
- Invoice selection
- QR code generation
- WebSocket payment tracking

### 3. UploadSales.vue - Bulk Import
**Route**: `/uploadsales`

Features:
- CSV upload with preview
- Driver/Vehicle selection
- Background import with progress
- Error reporting

### 4. Scanner.vue - Invoice Scanner
**Route**: `/scanner`

Features:
- Camera access
- QR code scanning
- Photo OCR extraction
- Customer resolution

## Frappe UI Resources

Declarative data fetching pattern:

```javascript
import { createResource } from "frappe-ui"

const resource = createResource({
  url: "custom_erp.api.method_name",
  auto: false,
  params: {},
  onSuccess: (result) => { /* handle */ },
  onError: (err) => { /* handle */ }
})

// Trigger fetch
resource.fetch({ param: value })

// Access state
resource.loading  // boolean
resource.data     // response
resource.error    // error object
```

## Vue Composition API

```javascript
import { ref, reactive, computed, onMounted, watch } from "vue"

// Reactive state
const loading = ref(false)
const filters = reactive({ customer: "", from_date: "", to_date: "" })

// Computed values
const hasFilters = computed(() => filters.customer && filters.from_date)

// Lifecycle
onMounted(() => { /* init */ })

// Watchers
watch(() => filters.customer, (newVal) => { /* react */ })
```

## Routing

```javascript
// router.js
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const router = createRouter({
  history: createWebHistory("/jsapp"),
  routes: [
    { path: "/", component: () => import("@/pages/Home.vue") },
    { path: "/qrpay", component: () => import("@/pages/QRPay.vue") },
    // ... more routes
  ]
})

// Auth guard
router.beforeEach(async (to, from, next) => {
  const isLoggedIn = session.isLoggedIn
  if (to.name !== "Login" && !isLoggedIn) {
    next({ name: "Login" })
  } else {
    next()
  }
})
```

## WebSocket Integration

```javascript
// socket.js
import { io } from "socket.io-client"

export function initSocket() {
  return io("/", {
    withCredentials: true,
    reconnection: true
  })
}

// Usage in components
const socket = inject("$socket")
socket.on("payment_status", (data) => { /* handle */ })
```

## PWA Configuration

### Service Worker Registration
```javascript
// register-sw.js
export async function registerScopedSW() {
  const registration = await navigator.serviceWorker.register('/sw.js', {
    scope: '/jsapp/'
  })
  return registration
}
```

### Web App Manifest
```json
{
  "name": "Custom ERP",
  "short_name": "ERP",
  "start_url": "/jsapp/",
  "scope": "/jsapp/",
  "display": "standalone",
  "theme_color": "#3b82f6",
  "icons": [...]
}
```

## Build Configuration

```javascript
// vite.config.js
export default defineConfig({
  plugins: [vue(), VitePWA({...})],
  build: {
    outDir: '../custom_erp/public/frontend',
    rollupOptions: {
      output: {
        manualChunks: {
          'frappe-ui': ['frappe-ui'],
          'vue-vendor': ['vue', 'vue-router']
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/socket.io': { target: 'http://localhost:9000', ws: true }
    }
  }
})
```

## Development Workflow

```bash
# Local dev
cd frontend
npm run dev  # http://localhost:5173

# Production build
npm run build  # Outputs to ../custom_erp/public/frontend/

# Preview build
npm run preview
```

## Performance Optimizations

1. **Code Splitting**: Lazy load routes
2. **Resource Caching**: Frappe UI cache option
3. **Image Optimization**: `loading="lazy"`
4. **Manual Chunks**: Separate vendor bundles

## Key Design Patterns

1. **Composition API**: Modern Vue 3 pattern
2. **Frappe Resources**: Declarative data fetching
3. **Route Guards**: Authentication checks
4. **WebSocket Events**: Real-time updates
5. **PWA Support**: Offline capability
6. **Scoped Service Workers**: Multiple app support

## Component Architecture

```vue
<template>
  <div class="container">
    <Button @click="loadData" :loading="loading">Load</Button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { createResource } from "frappe-ui"

const loading = ref(false)
const data = ref([])

const resource = createResource({
  url: "...",
  onSuccess: (result) => { data.value = result.data }
})

const loadData = () => resource.fetch()

onMounted(() => loadData())
</script>

<style scoped>
/* Component styles */
</style>
```

## Shared Components

- **CustomerSearch.vue**: Autocomplete customer search
- **LoadingOverlay.vue**: Full-screen loading
- **PWAInstallPrompt.vue**: Install prompt
- **PWAUpdatePrompt.vue**: Update notification

## State Management

Session and user data managed via Frappe UI resources:

```javascript
// data/session.js
export const session = createResource({
  url: "frappe.auth.get_logged_user",
  auto: true
})

session.logout = createResource({
  url: "frappe.handler.logout",
  onSuccess: () => window.location.href = "/account/login"
})
```

## API Integration

All API calls go through Frappe UI resources:

```javascript
const salesInvoices = createResource({
  url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoices",
  params: { filters: JSON.stringify(filters) }
})

await salesInvoices.fetch()
```

## Styling with Tailwind

```vue
<div class="container mx-auto px-4">
  <h1 class="text-2xl font-bold text-gray-900 mb-4">Title</h1>
  <Button class="bg-blue-600 hover:bg-blue-700">Click</Button>
</div>
```

## Deployment

Build outputs to `custom_erp/public/frontend/`:
- index.html
- assets/ (JS/CSS bundles)
- manifest.json
- sw.js

Served by Frappe at `/assets/custom_erp/frontend/`
