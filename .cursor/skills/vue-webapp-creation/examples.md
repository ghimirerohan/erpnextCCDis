# Real App Examples

Examples from existing Vue apps in custom_erp for reference.

---

## Example 1: qrpay-horlicks

A QR payment app for Horlicks customer group with orange theme.

### Directory Structure
```
qrpay-horlicks/
├── index.html
└── src/
    ├── main.js
    ├── App.vue
    ├── router.js
    ├── QRPayHorlicks.vue
    └── PreviousTransactions.vue
```

### vite.config.js Entry
```javascript
const apps = [
  'qrpay',
  'qrpay-horlicks',  // Hyphenated
  'qrpay-admin',
  // ...
]
```

### build-apps.js Entry
```javascript
const apps = [
  'qrpay',
  'qrpay-horlicks',
  // ...
]

const appThemes = {
  'qrpay-horlicks': { 
    theme: '#f97316',      // Orange
    bg: '#ffffff', 
    name: 'QRPay Horlicks', 
    desc: 'Horlicks Fonepay QR Code Generator' 
  },
}
```

### WWW Files
- `custom_erp/www/qrpay-horlicks.html` (hyphenated)
- `custom_erp/www/qrpay_horlicks.py` (underscored)

### Router Base Path
```javascript
const router = createRouter({
  history: createWebHistory("/qrpay-horlicks"),
  routes,
})
```

### URL
`https://yourdomain.com/qrpay-horlicks`

---

## Example 2: pay-dashboard

Analytics dashboard with blue theme.

### Theme Config
```javascript
'pay-dashboard': { 
  theme: '#2563eb',      // Blue
  bg: '#ffffff', 
  name: 'Pay Dashboard', 
  desc: 'Payment Statistics Dashboard' 
},
```

### Features
- Company filter dropdown
- Date range filtering
- Summary cards with totals
- Data tables with pagination

---

## Example 3: qrpay

The original QR payment app with green theme.

### Theme Config
```javascript
'qrpay': { 
  theme: '#10b981',      // Green (emerald)
  bg: '#ffffff', 
  name: 'QRPay', 
  desc: 'Dynamic Fonepay QR Code Generator' 
},
```

### Features
- Customer search with autocomplete
- Dynamic QR code generation
- WebSocket for real-time payment status
- Payment confirmation dialogs
- Previous transactions history

---

## Theme Color Reference

| App | Color | Hex |
|-----|-------|-----|
| qrpay | Green | `#10b981` |
| qrpay-horlicks | Orange | `#f97316` |
| qrpay-admin | Purple | `#7c3aed` |
| pay-dashboard | Blue | `#2563eb` |
| scanner | Amber | `#f59e0b` |
| uploadsales | Emerald | `#059669` |
| uploadreco | Red | `#dc2626` |
| dailyrecoentry | Cyan | `#0891b2` |
| home | Indigo | `#6366f1` |

---

## Common Patterns

### Customer Search with Autocomplete
```vue
<CustomerSearch
  ref="customerSearchRef"
  v-model="selectedCustomerValue"
  label="Customer"
  :apiUrl="'custom_erp.api.fonepay.search_customers'"
  @select="handleCustomerSelect"
/>
```

### API Resource with Loading State
```javascript
const dataResource = createResource({
  url: 'custom_erp.api.my_app.get_data',
  auto: false,
  onSuccess: (response) => {
    data.value = response
    loading.value = false
  },
  onError: (error) => {
    console.error('Failed to load data', error)
    loading.value = false
  }
})

const loadData = () => {
  loading.value = true
  dataResource.fetch({ filters: currentFilters.value })
}
```

### Dashboard Summary Cards
```vue
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
  <div class="p-4 bg-green-50 rounded-lg border-2 border-green-200">
    <p class="text-sm text-green-600 font-medium uppercase">Total</p>
    <p class="text-2xl font-bold text-green-700">Rs. {{ formatNumber(summary.total) }}</p>
  </div>
  <div class="p-4 bg-yellow-50 rounded-lg border-2 border-yellow-200">
    <p class="text-sm text-yellow-600 font-medium uppercase">Pending</p>
    <p class="text-2xl font-bold text-yellow-700">{{ summary.pending }}</p>
  </div>
</div>
```

### Button with Loading State
```vue
<button
  @click="handleAction"
  :disabled="loading"
  class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg"
>
  <svg v-if="loading" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" class="opacity-25"/>
    <path d="M4 12a8 8 0 018-8" stroke="currentColor" stroke-width="4" fill="none" class="opacity-75"/>
  </svg>
  {{ loading ? 'Loading...' : 'Submit' }}
</button>
```

---

## Cloning an Existing App

To create a new app based on an existing one:

1. Copy the entire app directory:
   ```bash
   cp -r qrpay my-new-app
   ```

2. Rename main component file:
   ```bash
   mv my-new-app/src/QRPay.vue my-new-app/src/MyNewApp.vue
   ```

3. Update all internal references:
   - `router.js`: Component import, route names, base path
   - `App.vue`: Manifest app_name, theme color
   - `index.html`: Title, manifest link

4. Add to build configs (`vite.config.js`, `build-apps.js`)

5. Create WWW files with correct naming

6. Create/copy manifest and icons

7. Update any API endpoints if needed
