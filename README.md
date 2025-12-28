<p align="center">
  <img src="https://img.shields.io/badge/Frappe-v15-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTUtMTAtNXpNMiAxN2wxMCA1IDEwLTV2LTJMMTIgMTUgMiAxMHY3eiIvPjwvc3ZnPg==" />
  <img src="https://img.shields.io/badge/ERPNext-Extended-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js" />
  <img src="https://img.shields.io/badge/PWA-Ready-5A0FC8?style=for-the-badge&logo=pwa" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<h1 align="center">
  ⚡ Custom ERP
  <br/>
  <sub>Powerful ERPNext Extensions & Vue PWA Suite</sub>
</h1>

<p align="center">
  <strong>🔥 Supercharge ERPNext with advanced overrides, Fonepay integration & 9 production-ready Vue PWA apps 🔥</strong>
</p>

<p align="center">
  <a href="#-key-features">Features</a> •
  <a href="#-pwa-applications">Apps</a> •
  <a href="#-installation">Installation</a> •
  <a href="#%EF%B8%8F-configuration">Configuration</a> •
  <a href="#-api-reference">API</a>
</p>

---

## 🎯 Key Features

### 💳 Fonepay QR Payment Integration
Complete dynamic QR payment solution for Nepal's Fonepay network:
- **Dynamic QR Generation** - Create payment QRs linked to customers/invoices
- **Real-time WebSocket Updates** - Live payment status tracking
- **Automatic Payment Entry** - Auto-create payment entries on successful transactions
- **Admin Dashboard** - Manage and process unprocessed transactions
- **Scheduled Processing** - Hourly job to handle pending payments

### 📊 Fixed Stock Valuation System
Override ERPNext's moving average with fixed valuation:
- **Consistent COGS** - Always use Item master's `valuation_rate`
- **Configurable** - Enable/disable via Custom ERP Settings
- **Comprehensive** - Works across all stock transaction types
- **Smart Fallbacks** - Falls back to standard_rate → Item Price

### 📱 9 Vue PWA Applications
Production-ready Progressive Web Apps for various workflows:

| App | Route | Purpose |
|-----|-------|---------|
| 🏠 **Home** | `/home` | Sales invoice dashboard with bill-wise & summary views |
| 💰 **QR Pay** | `/qrpay` | Dynamic Fonepay QR generator for payments |
| 👨‍💼 **QR Pay Admin** | `/qrpay-admin` | Manage unprocessed Fonepay transactions |
| 📈 **Pay Dashboard** | `/pay-dashboard` | Transaction analytics & statistics |
| 📤 **Upload Sales** | `/uploadsales` | Bulk CSV import for sales invoices |
| 📸 **Scanner** | `/scanner` | Invoice scanning & OCR document capture |
| 📋 **Upload Reco** | `/uploadreco` | Payment reconciliation CSV upload |
| 📝 **Daily Reco Entry** | `/dailyrecoentry` | Daily payment reconciliation entry |
| 🔐 **Test Login** | `/testlogin` | Authentication testing interface |

### 🔧 ERPNext Overrides
Smart document type extensions:
- **Purchase Invoice Override** - Enhanced purchase handling
- **Opening Invoice Tool** - CSV value sanitization & placeholder items
- **Stock Reconciliation** - UOM conversion & serial/batch bundle handling
- **Repost Item Valuation** - Allow cancellation with Stock Reconciliation

---

## 🚀 Installation

### Prerequisites

```
- Frappe Framework v15.x
- ERPNext v15.x
- Node.js 18.x+
- Yarn 1.22+
```

### Step 1: Get the App

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/your-org/custom_erp.git --branch main
```

### Step 2: Install on Site

```bash
bench --site your-site.local install-app custom_erp
bench --site your-site.local migrate
```

### Step 3: Build Frontend Assets

```bash
# Install frontend dependencies
cd apps/custom_erp
yarn install

# Build all Vue apps
yarn build

# Or use bench build
cd ../../
bench build --app custom_erp
```

### Step 4: Restart Services

```bash
bench restart
```

---

## ⚙️ Configuration

### Fonepay Integration Setup

Add Fonepay credentials to your site config:

```bash
nano sites/your-site.local/site_config.json
```

```json
{
  "fonepay": {
    "merchant_code": "YOUR_MERCHANT_CODE",
    "secret_key": "YOUR_SECRET_KEY",
    "username": "your-email@fonepay.com",
    "password": "your-password",
    "env": "dev",
    "ws_worker": "inprocess",
    "ws_timeout_seconds": 300,
    "scheduled_batch_size": 50,
    "scheduled_sleep_between": 0.2
  }
}
```

| Config | Description |
|--------|-------------|
| `merchant_code` | Your Fonepay merchant code |
| `secret_key` | HMAC secret for request signing |
| `env` | `dev` or `prod` |
| `ws_worker` | `inprocess` or `microservice` |
| `ws_timeout_seconds` | WebSocket listener timeout |

Environment variables can override any config:
```bash
export FONEPAY_SECRET_KEY=your-secret-key
```

### Fixed Valuation Rate Setup

1. Navigate to **Custom ERP Settings**
2. Enable **Fixed Valuation Rate** feature
3. Set `valuation_rate` in Item master for each item

---

## 📱 PWA Applications

### Tech Stack

```
Vue 3.5.x          - Reactive UI framework
Vue Router 4.x     - SPA routing
Frappe UI 0.1.x    - Frappe-styled components
TailwindCSS 3.4.x  - Utility-first CSS
Vite 5.x           - Lightning-fast builds
PWA Plugin         - Service workers & offline support
Socket.io          - Real-time updates
```

### Application Routes

All apps are accessible at your Frappe site:

```
https://your-site.local/qrpay
https://your-site.local/pay-dashboard
https://your-site.local/home
https://your-site.local/scanner
https://your-site.local/uploadsales
https://your-site.local/qrpay-admin
https://your-site.local/uploadreco
https://your-site.local/dailyrecoentry
```

### Building Individual Apps

```bash
cd apps/custom_erp

# Build all apps
yarn build

# The build process:
# 1. Builds each app with correct base paths
# 2. Generates HTML files in www/ directory
# 3. Organizes assets per-app
```

---

## 📡 API Reference

### Fonepay APIs

```python
# Create dynamic QR code
custom_erp.api.fonepay.create_dynamic_qr(
    amount,
    customer=None,
    sales_invoice=None,
    remarks1="",
    remarks2="",
    metadata=None
)

# Check QR payment status
custom_erp.api.fonepay.check_qr_status(prn)

# Finalize payment from WebSocket
custom_erp.api.fonepay.finalize_payment_from_ws(tx_name)

# Process unprocessed QRs manually
custom_erp.api.fonepay.process_unprocessed_qrs(
    tx_names=None,
    limit=100,
    sleep_between=0.2
)
```

### Upload Sales APIs

```python
# Transform and preview CSV data
custom_erp.api.uploadsales.transform_and_preview(csv_data)

# Enqueue bulk import job
custom_erp.api.uploadsales.enqueue_import_job(data)

# Get import job progress
custom_erp.api.uploadsales.get_job_progress(job_id)

# Get available drivers/vehicles
custom_erp.api.uploadsales.get_drivers()
custom_erp.api.uploadsales.get_vehicles()
```

### Payment Reconciliation APIs

```python
# Parse and validate CSV
custom_erp.api.payment_reco.parse_and_validate_csv(csv_data)

# Create payment reconciliations
custom_erp.api.payment_reco.create_payment_recos(data)

# Get driver reconciliation data
custom_erp.api.payment_reco.get_driver_reco_data(driver)

# Update payment entry
custom_erp.api.payment_reco.update_payment_entry(entry_data)
```

---

## 🏗️ Project Structure

```
custom_erp/
├── custom_erp/
│   ├── api/
│   │   ├── fonepay.py              # Fonepay QR integration
│   │   ├── uploadsales.py          # Bulk sales import
│   │   └── payment_reco.py         # Payment reconciliation
│   ├── doctype/
│   │   ├── fonepay_qr_transaction/ # QR transaction records
│   │   ├── daily_sales_payment_reco/
│   │   └── custom_erp_settings/
│   ├── stock_valuation/
│   │   └── stock_ledger_override.py # Fixed valuation logic
│   ├── purchase_invoice/
│   │   └── purchase_invoice_override.py
│   ├── sales_invoice/
│   │   └── sales_invoice.py
│   ├── opening_invoice_tool/
│   │   └── opening_invoice_creation_tool_override.py
│   ├── stock_reconciliation/
│   │   ├── stock_reconciliation_override.py
│   │   └── repost_item_valuation_override.py
│   ├── management/commands/        # CLI utilities
│   ├── fixtures/                   # Custom fields, print formats
│   ├── www/                        # Vue app entry points
│   └── hooks.py                    # App configuration
│
├── # Vue PWA Source Directories
├── qrpay/                          # QR Payment app
├── qrpay-admin/                    # QR Admin app
├── pay-dashboard/                  # Analytics dashboard
├── home/                           # Sales dashboard
├── scanner/                        # Invoice scanner
├── uploadsales/                    # Bulk upload app
├── uploadreco/                     # Reco upload app
├── dailyrecoentry/                 # Daily reco entry
├── shared/                         # Shared Vue components
│
├── # Build Configuration
├── build-apps.js                   # Multi-app build script
├── vite-single-app.config.js       # Single app Vite config
├── vite.config.js                  # Base Vite config
├── tailwind.config.js              # Tailwind configuration
├── package.json
└── yarn.lock
```

---

## 🔄 Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| `scheduled_process_unprocessed_qrs` | Hourly | Process pending Fonepay transactions |

---

## 🛠️ CLI Commands

### Manual Fonepay Processing

```bash
bench --site your-site.local execute \
  custom_erp.api.fonepay.scheduled_process_unprocessed_qrs
```

### Repost Sales Invoices

```bash
bench --site your-site.local execute \
  custom_erp.management.commands.repost_sales_invoices_with_updated_prices
```

### Submit Draft Invoices

```bash
bench --site your-site.local execute \
  custom_erp.management.commands.submit_draft_sales_invoices
```

---

## 🧪 Testing

### Run Python Tests

```bash
bench --site your-site.local run-tests --app custom_erp
```

### Test Fonepay Integration

```bash
bench --site your-site.local execute custom_erp.tests.test_fonepay.test_create_qr
```

---

## 📋 Fixtures Included

| Fixture | Description |
|---------|-------------|
| **Custom Fields** | Extended fields for core doctypes |
| **Property Setters** | Field property modifications |
| **Print Formats** | Custom print templates |
| **Workflows** | Custom workflow definitions |
| **Reports** | Custom report definitions |

---

## 🔒 Authentication

All PWA apps use Frappe's session authentication:
- Login once, authenticated across all apps
- Automatic redirect to login page for unauthenticated users
- Role-based access control via Frappe permissions

---

## 🤝 Contributing

### Development Setup

```bash
# Clone and install
cd apps/custom_erp
yarn install

# Run development server (hot reload)
yarn dev

# Build for production
yarn build

# Lint code
yarn lint
```

### Code Style

- **Python**: Follows Frappe coding standards
- **JavaScript/Vue**: Biome for linting and formatting
- **CSS**: TailwindCSS utility classes

---

## 📜 License

MIT License - see [LICENSE](license.txt) for details.

---

## 👨‍💻 Author

<p align="center">
  <strong>Developed by Rohan Ghimire</strong>
  <br/>
  <a href="mailto:ghimirerohan@gmail.com">📧 ghimirerohan@gmail.com</a>
</p>

---

## 🙏 Acknowledgments

- [Frappe Framework](https://frappeframework.com) - The awesome Python web framework
- [ERPNext](https://erpnext.com) - The world's best open-source ERP
- [Vue.js](https://vuejs.org) - The progressive JavaScript framework
- [Fonepay](https://fonepay.com) - Nepal's payment gateway

---

<p align="center">
  <strong>⭐ Star this repo if Custom ERP powers your business! ⭐</strong>
</p>

<p align="center">
  <sub>Made with ❤️ in Nepal 🇳🇵</sub>
</p>

