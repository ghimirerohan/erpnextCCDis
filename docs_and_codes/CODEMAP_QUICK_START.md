# Custom ERP - Quick Start Guide for Developers

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Frappe Bench installed
- Node.js 16+ and npm
- Python 3.10+
- MariaDB/MySQL

---

## Installation

### 1. Get the App
```bash
cd frappe-bench
bench get-app custom_erp https://github.com/ghimirerohan/erpnextCCDis.git
```

### 2. Install on Site
```bash
bench --site [your-site] install-app custom_erp
```

The installation automatically:
- ✅ Builds the frontend
- ✅ Creates custom fields
- ✅ Loads fixtures
- ✅ Sets up hooks

### 3. Configure Fonepay (Optional)
Edit `sites/[your-site]/site_config.json`:
```json
{
  "fonepay": {
    "merchant_code": "YOUR_CODE",
    "secret_key": "YOUR_KEY",
    "username": "user@fonepay.com",
    "password": "password",
    "env": "dev"
  }
}
```

### 4. Start Development
```bash
# Terminal 1: Backend
bench start

# Terminal 2: Frontend (optional for dev)
cd apps/custom_erp/frontend
npm run dev
```

---

## Project Structure at a Glance

```
custom_erp/
├── custom_erp/              # Python backend
│   ├── api/                # API endpoints
│   ├── custom_erp/         # Business logic
│   ├── hooks.py            # Frappe hooks
│   └── public/             # Built frontend
│
└── frontend/               # Vue.js frontend
    ├── src/
    │   ├── pages/         # Route pages
    │   ├── components/    # Shared components
    │   ├── apps/          # Feature modules
    │   └── router.js      # Routes
    └── vite.config.js     # Build config
```

---

## Key Files to Know

### Backend
- **`hooks.py`**: App configuration, event hooks, API whitelist
- **`api/fonepay.py`**: Fonepay payment integration
- **`api/uploadsales.py`**: Bulk sales invoice import
- **`sales_invoice/api.py`**: Sales invoice data APIs
- **`stock_valuation/stock_ledger_override.py`**: Valuation rate fixes

### Frontend
- **`router.js`**: Route definitions
- **`pages/Home.vue`**: Sales invoice dashboard
- **`pages/QRPay.vue`**: Payment interface
- **`apps/uploadsales/UploadSales.vue`**: CSV import

---

## Common Tasks

### Add a New API Endpoint

**1. Create Python function:**
```python
# custom_erp/custom_erp/api/my_module.py

import frappe

@frappe.whitelist()
def my_new_api(param1, param2):
    """My new API endpoint"""
    try:
        # Your logic here
        result = do_something(param1, param2)
        return {"success": True, "data": result}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "My API Error")
        return {"success": False, "error": str(e)}
```

**2. Whitelist in hooks.py:**
```python
# custom_erp/hooks.py

whitelisted_methods = [
    # ... existing methods
    "custom_erp.custom_erp.api.my_module.my_new_api",
]
```

**3. Call from frontend:**
```javascript
// frontend/src/pages/MyPage.vue

import { createResource } from "frappe-ui"

const myResource = createResource({
  url: "custom_erp.custom_erp.api.my_module.my_new_api",
  params: { param1: "value1", param2: "value2" }
})

await myResource.fetch()
```

---

### Add a New Page

**1. Create Vue component:**
```vue
<!-- frontend/src/pages/MyNewPage.vue -->

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My New Page</h1>
    <Button @click="loadData" :loading="loading">Load Data</Button>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { createResource } from "frappe-ui"

const loading = ref(false)
const data = ref([])

const dataResource = createResource({
  url: "custom_erp.custom_erp.api.my_module.my_new_api",
  onSuccess: (result) => {
    if (result.success) {
      data.value = result.data
    }
  }
})

const loadData = async () => {
  loading.value = true
  await dataResource.fetch()
  loading.value = false
}
</script>
```

**2. Add route:**
```javascript
// frontend/src/router.js

const routes = [
  // ... existing routes
  {
    path: "/my-new-page",
    name: "MyNewPage",
    component: () => import("@/pages/MyNewPage.vue")
  }
]
```

**3. Build frontend:**
```bash
cd frontend
npm run build
```

---

### Add a Document Hook

**1. Create hook function:**
```python
# custom_erp/custom_erp/my_module/my_hooks.py

import frappe

def before_save_sales_invoice(doc, method=None):
    """Custom logic before saving Sales Invoice"""
    # Your logic here
    doc.custom_field = calculate_something(doc)
```

**2. Register in hooks.py:**
```python
# custom_erp/hooks.py

doc_events = {
    "Sales Invoice": {
        "before_save": [
            "custom_erp.custom_erp.my_module.my_hooks.before_save_sales_invoice"
        ]
    }
}
```

---

### Add a Custom Field

**1. Create via Frappe UI:**
- Go to Customize Form
- Select doctype (e.g., Sales Invoice)
- Add field
- Export to fixtures

**2. Or create programmatically:**
```python
# custom_erp/install.py

def create_custom_fields():
    frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "Sales Invoice",
        "fieldname": "custom_my_field",
        "fieldtype": "Data",
        "label": "My Field",
        "insert_after": "customer"
    }).insert(ignore_if_duplicate=True)
```

---

## Development Workflow

### Backend Changes
```bash
# 1. Edit Python files
# 2. Restart bench
bench restart

# Or use watch mode
bench --site [site] watch
```

### Frontend Changes
```bash
# Development mode (hot reload)
cd frontend
npm run dev
# Visit http://localhost:5173

# Production build
npm run build
# Outputs to custom_erp/public/frontend/
```

### Database Changes
```bash
# Create migration
bench --site [site] console
>>> frappe.db.add_column("Sales Invoice", "my_column", "varchar(255)")

# Or create patch file
# custom_erp/patches/v1_0/add_my_column.py
```

---

## Testing

### Backend Tests
```bash
# Run all tests
bench --site [site] run-tests --app custom_erp

# Run specific test
bench --site [site] run-tests --app custom_erp --module custom_erp.tests.test_sales_invoice
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Manual API Testing
```bash
# Using bench console
bench --site [site] console

>>> from custom_erp.custom_erp.api.fonepay import create_dynamic_qr
>>> result = create_dynamic_qr("CUST-001", 1000)
>>> print(result)
```

---

## Debugging

### Backend Debugging
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use frappe.log
frappe.log_error(message, title)

# Check logs
tail -f sites/[site]/logs/error.log
```

### Frontend Debugging
```javascript
// Browser console
console.log("Debug:", data)

// Vue DevTools
// Install browser extension

// Check network requests
// Browser DevTools → Network tab
```

---

## Common Issues & Solutions

### Frontend not updating after build
```bash
# Clear cache
bench --site [site] clear-cache

# Hard reload browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)
```

### API returns 403 Forbidden
```python
# Check if method is whitelisted in hooks.py
whitelisted_methods = [
    "custom_erp.custom_erp.api.my_module.my_function"
]

# Or add @frappe.whitelist() decorator
@frappe.whitelist()
def my_function():
    pass
```

### WebSocket not connecting
```bash
# Check if socketio is running
bench --site [site] doctor

# Restart bench
bench restart
```

### Import errors
```bash
# Reinstall dependencies
cd frontend
npm ci

# Backend
bench --site [site] migrate
```

---

## Useful Commands

### Bench Commands
```bash
# Start development server
bench start

# Restart services
bench restart

# Clear cache
bench --site [site] clear-cache

# Migrate database
bench --site [site] migrate

# Console access
bench --site [site] console

# Build frontend
bench build --app custom_erp

# Update app
cd apps/custom_erp
git pull
bench --site [site] migrate
```

### Frontend Commands
```bash
cd frontend

# Install dependencies
npm ci

# Development server
npm run dev

# Production build
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

---

## Architecture Quick Reference

### Request Flow
```
User Action → Vue Component → Frappe UI Resource → 
HTTP POST → Frappe Server → Python Function → 
Database Query → Response → Update UI
```

### File Organization
```
Backend:  custom_erp/custom_erp/{module}/{file}.py
Frontend: frontend/src/{pages|components|apps}/{file}.vue
Routes:   frontend/src/router.js
Config:   custom_erp/hooks.py
```

### Key Patterns
- **API**: `@frappe.whitelist()` + whitelist in hooks.py
- **Frontend**: `createResource()` from frappe-ui
- **Hooks**: Register in `doc_events` in hooks.py
- **Real-time**: `frappe.publish_realtime()` + socket.on()

---

## Next Steps

1. **Read the codemaps**: 
   - `CODEMAP_OVERVIEW.md` - Architecture overview
   - `CODEMAP_BACKEND.md` - Backend details
   - `CODEMAP_FRONTEND.md` - Frontend details
   - `CODEMAP_API_REFERENCE.md` - API documentation

2. **Explore the code**:
   - Start with `hooks.py` to understand app structure
   - Look at `pages/Home.vue` for frontend patterns
   - Check `api/fonepay.py` for backend patterns

3. **Try making changes**:
   - Add a new field to Sales Invoice
   - Create a simple API endpoint
   - Add a new page to the frontend

4. **Join the community**:
   - Frappe Forum: https://discuss.frappe.io
   - GitHub Issues: Report bugs and request features

---

## Resources

- **Frappe Framework Docs**: https://frappeframework.com/docs
- **Vue.js 3 Docs**: https://vuejs.org/guide/
- **Frappe UI Docs**: https://frappeui.com
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## Getting Help

1. Check existing documentation in the repo
2. Search Frappe Forum for similar issues
3. Review error logs: `sites/[site]/logs/`
4. Use `bench doctor` to diagnose issues
5. Open GitHub issue with detailed description

---

Happy coding! 🎉
