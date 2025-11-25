# Custom ERP - Codebase Overview

## Project Structure

This is a **Frappe Framework** custom app with a modern **Vue.js 3** frontend, designed to extend ERPNext with custom business logic and mobile-friendly Progressive Web Apps (PWAs).

```
custom_erp/
├── custom_erp/                    # Python backend (Frappe app)
│   ├── api/                       # API endpoints
│   │   ├── fonepay.py            # Fonepay payment integration
│   │   └── uploadsales.py        # Bulk sales invoice upload
│   ├── custom_erp/               # Core business logic modules
│   │   ├── opening_invoice_tool/ # Invoice creation tools
│   │   ├── purchase_invoice/     # Purchase invoice overrides
│   │   ├── sales_invoice/        # Sales invoice customizations
│   │   ├── stock_reconciliation/ # Stock management
│   │   └── stock_valuation/      # Valuation rate fixes
│   ├── management/commands/      # CLI management commands
│   ├── config/                   # App configuration
│   ├── fixtures/                 # Data fixtures
│   ├── patches/                  # Database migration patches
│   ├── public/                   # Static assets (built frontend)
│   ├── hooks.py                  # Frappe hooks configuration
│   ├── boot.py                   # Boot session settings
│   └── install.py                # Installation scripts
│
└── frontend/                      # Vue.js 3 SPA
    ├── src/
    │   ├── apps/                 # Feature modules
    │   │   └── uploadsales/      # CSV upload & import app
    │   ├── components/           # Reusable Vue components
    │   ├── pages/                # Route pages
    │   │   ├── Home.vue          # Sales invoice dashboard
    │   │   ├── Login.vue         # Authentication
    │   │   ├── QRPay.vue         # Fonepay QR payment
    │   │   ├── QRPayAdmin.vue    # Payment admin panel
    │   │   ├── PayDashboard.vue  # Payment dashboard
    │   │   └── Scanner.vue       # Invoice scanner
    │   ├── data/                 # Data layer (Frappe resources)
    │   ├── router.js             # Vue Router config
    │   ├── main.js               # App entry point
    │   └── App.vue               # Root component
    ├── public/                   # PWA assets (manifests, icons)
    ├── vite.config.js            # Vite build config
    └── package.json              # Node dependencies
```

## Technology Stack

### Backend
- **Framework**: Frappe Framework (Python)
- **Database**: MariaDB/MySQL
- **ORM**: Frappe ORM
- **API**: RESTful JSON API with `@frappe.whitelist()`
- **Real-time**: WebSocket support via frappe.socketio

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **UI Library**: Frappe UI components
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State**: Vue Composition API (reactive refs)
- **PWA**: Service Workers, Web Manifests

## Key Features

### 1. **Sales Invoice Management**
- Dashboard with bill-wise and summary views
- Customer filtering with QR/photo scanning
- Date range filtering
- Real-time data from ERPNext

### 2. **Fonepay Payment Integration**
- Dynamic QR code generation
- WebSocket-based payment status tracking
- Automatic payment entry creation
- Scheduled batch processing

### 3. **Upload Sales (Bulk Import)**
- CSV upload with preview
- Nepali date conversion
- Customer resolution
- Background job processing with progress tracking

### 4. **Stock Valuation Overrides**
- Fixed valuation rate enforcement
- Custom GL entry handling
- Repost item valuation customizations

### 5. **PWA Support**
- Offline capability
- Install prompts
- Service worker updates
- Multiple app scopes (/jsapp/*)

## Architecture Patterns

### Backend (Frappe)

#### 1. **Hooks System**
```python
# hooks.py - Event-driven architecture
doc_events = {
    "Sales Invoice": {
        "before_insert": [...],
        "before_save": [...],
        "on_submit": [...]
    }
}
```

#### 2. **Whitelisted APIs**
```python
# API endpoints exposed to frontend
@frappe.whitelist()
def create_dynamic_qr(customer, amount, sales_invoice=None):
    # Implementation
```

#### 3. **DocType Overrides**
```python
override_doctype_class = {
    "Purchase Invoice": "custom_erp.custom_erp.purchase_invoice.purchase_invoice_override.PurchaseInvoiceOverride"
}
```

### Frontend (Vue.js)

#### 1. **Frappe Resource Pattern**
```javascript
const salesInvoicesResource = createResource({
  url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoices",
  auto: false,
  onSuccess: (result) => { /* ... */ }
})
```

#### 2. **Composition API**
```javascript
import { ref, reactive, computed, onMounted } from "vue"

const loading = ref(false)
const filters = reactive({ customer: "", from_date: "", to_date: "" })
```

#### 3. **Route-based Code Splitting**
```javascript
{
  path: "/uploadsales",
  component: () => import("@/apps/uploadsales/UploadSales.vue")
}
```

## Data Flow

### Request Flow (Frontend → Backend)
```
Vue Component
  ↓ (createResource)
Frappe UI Resource
  ↓ (HTTP POST)
/api/method/{module}.{function}
  ↓ (@frappe.whitelist())
Python Function
  ↓ (frappe.db.*)
Database Query
  ↓
Return JSON Response
```

### Real-time Flow (WebSocket)
```
Backend Event
  ↓ (frappe.publish_realtime)
Redis Pub/Sub
  ↓ (socketio)
Frontend Socket Listener
  ↓ (reactive update)
Vue Component Re-render
```

## Configuration Files

### Backend Configuration
- **hooks.py**: App hooks, event handlers, overrides
- **boot.py**: Session boot settings
- **install.py**: Post-install setup
- **site_config.json**: Site-specific config (Fonepay credentials)

### Frontend Configuration
- **vite.config.js**: Build settings, PWA config
- **router.js**: Route definitions
- **package.json**: Dependencies, scripts
- **tailwind.config.js**: Tailwind customization

## API Endpoints

### Sales Invoice API
- `get_sales_invoices`: Filtered invoice list
- `get_sales_invoice_summary`: Grouped summary data
- `get_customers`: Customer dropdown data

### Fonepay API
- `create_dynamic_qr`: Generate payment QR
- `check_qr_status`: Poll payment status
- `finalize_payment_from_ws`: Complete payment
- `process_unprocessed_qrs`: Batch processing

### Upload Sales API
- `transform_and_preview`: CSV preview
- `enqueue_import_job`: Start background import
- `get_job_progress`: Track import progress
- `get_drivers`: Fetch driver list
- `get_vehicles`: Fetch vehicle list

## Development Workflow

### Backend Development
```bash
# Watch for changes
bench --site [site] watch

# Console access
bench --site [site] console

# Run tests
bench run-tests --app custom_erp
```

### Frontend Development
```bash
cd frontend
npm run dev  # Vite dev server on :5173
```

### Production Build
```bash
cd frontend
npm run build  # Outputs to custom_erp/public/frontend/
```

## Key Design Decisions

1. **Frappe Overrides vs Hooks**: Use hooks for event-driven logic, overrides for core behavior changes
2. **Vue Composition API**: Modern, TypeScript-friendly, better code organization
3. **Frappe UI Resources**: Declarative data fetching with built-in loading/error states
4. **PWA Architecture**: Scoped service workers for multiple apps under /jsapp/*
5. **Background Jobs**: Use Frappe's enqueue for long-running operations
6. **Real-time Updates**: WebSocket for payment status, progress tracking

## Security Considerations

- All API endpoints use `@frappe.whitelist()` for CSRF protection
- Session-based authentication via Frappe
- HMAC signing for Fonepay API calls
- File upload validation and sanitization
- SQL injection prevention via Frappe ORM

## Performance Optimizations

- Route-based code splitting (lazy loading)
- Resource caching via Frappe UI
- Database query optimization (indexed fields)
- Background job processing for bulk operations
- Service worker caching for offline support

## Testing Strategy

- **Backend**: Unit tests with `frappe.tests`
- **Frontend**: Component testing (to be implemented)
- **Integration**: End-to-end API tests
- **Manual**: PWA testing guide included

## Deployment

### Installation
```bash
bench get-app custom_erp https://github.com/ghimirerohan/erpnextCCDis.git
bench install-app custom_erp
```

### Post-Install
- Frontend auto-builds during installation
- Custom fields created automatically
- Fixtures loaded from JSON files

### Configuration
- Set Fonepay credentials in site_config.json
- Configure HRMS dependencies (Driver, Vehicle)
- Set up scheduled jobs (hourly QR processing)

## Troubleshooting

See dedicated documentation:
- `DEBUGGING_GUIDE.md` - Frontend debugging
- `PRODUCTION_MEMORY_GUIDE.md` - Memory optimization
- `PWA_TESTING_GUIDE.md` - PWA validation
- `TROUBLESHOOTING_NEPALI_DATE.md` - Date conversion issues
