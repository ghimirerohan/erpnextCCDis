# Custom ERP - Backend Architecture (Frappe)

## Module Structure

### Core Modules (`custom_erp/custom_erp/`)

```
custom_erp/
├── api/                          # Public API endpoints
│   ├── fonepay.py               # Fonepay payment integration
│   └── uploadsales.py           # Bulk sales invoice upload
│
├── custom_erp/                  # Business logic modules
│   ├── opening_invoice_tool/
│   │   ├── __init__.py
│   │   └── opening_invoice_creation_tool_override.py
│   │
│   ├── purchase_invoice/
│   │   ├── api.py              # Purchase invoice API
│   │   ├── memory_config.py    # Memory optimization
│   │   └── purchase_invoice_override.py
│   │
│   ├── sales_invoice/
│   │   ├── api.py              # Sales invoice API
│   │   ├── bulk_submit_sales_invoice.py
│   │   └── sales_invoice.py    # Sales invoice hooks
│   │
│   ├── stock_reconciliation/
│   │   ├── repost_item_valuation_override.py
│   │   ├── stock_reconciliation.py
│   │   └── stock_reconciliation_override.py
│   │
│   ├── stock_valuation/
│   │   ├── __init__.py
│   │   ├── stock_ledger_override.py  # Core valuation logic
│   │   └── test_functions.py
│   │
│   └── utils/
│       └── split_uom_cs_nos.py
│
├── management/commands/         # CLI management commands
│   ├── check_cs_nos_conversions.py
│   ├── config_repost.py
│   ├── fix_all_gl_entries.py
│   ├── fix_payment_entry_gl_entries.py
│   ├── fix_purchase_invoice_gl_entries.py
│   ├── fix_sales_invoice_gl_entries.py
│   ├── fix_stock_reconciliation_gl_entries.py
│   ├── recreate_stock_reco_gl_entries.py
│   ├── remove_all_payments.py
│   ├── remove_all_sales_invoices.py
│   ├── repost_sales_invoices_with_updated_prices.py
│   ├── submit_draft_sales_invoices.py
│   └── test_repost_script.py
│
├── config/                      # App configuration
├── fixtures/                    # Data fixtures (JSON)
├── patches/                     # Database migration patches
├── public/                      # Static assets
│   ├── frontend/               # Built Vue app
│   ├── js/                     # Custom JS
│   │   ├── invoice_scanner.js
│   │   ├── nepali_date_adapter.js
│   │   └── nepali_date_patch.js
│   ├── lib/                    # Third-party libraries
│   └── css/                    # Custom CSS
│
├── hooks.py                     # Frappe hooks configuration
├── boot.py                      # Boot session settings
└── install.py                   # Post-install setup
```

## Key Backend Components

### 1. Hooks Configuration (`hooks.py`)

The central configuration file that defines how the app integrates with Frappe/ERPNext.

#### Document Event Hooks
```python
doc_events = {
    "Sales Invoice": {
        "before_insert": [
            "custom_erp.custom_erp.sales_invoice.sales_invoice.before_insert",
            "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate_before_gl_creation",
        ],
        "before_save": [
            "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
        ],
        "on_submit": "custom_erp.custom_erp.stock_valuation.stock_ledger_override.ensure_fixed_valuation_rate",
    },
    # Similar hooks for Purchase Invoice, Stock Entry, Delivery Note, etc.
}
```

**Purpose**: Intercept document lifecycle events to inject custom logic.

#### Whitelisted Methods
```python
whitelisted_methods = [
    "custom_erp.api.fonepay.create_dynamic_qr",
    "custom_erp.api.fonepay.check_qr_status",
    "custom_erp.api.uploadsales.transform_and_preview",
    "custom_erp.api.uploadsales.enqueue_import_job",
    # ... more methods
]
```

**Purpose**: Expose Python functions as HTTP API endpoints accessible from frontend.

#### DocType Class Overrides
```python
override_doctype_class = {
    "Purchase Invoice": "custom_erp.custom_erp.purchase_invoice.purchase_invoice_override.PurchaseInvoiceOverride",
    "Opening Invoice Creation Tool": "custom_erp.custom_erp.opening_invoice_tool.opening_invoice_creation_tool_override.OpeningInvoiceCreationToolOverride",
    "Repost Item Valuation": "custom_erp.custom_erp.stock_reconciliation.repost_item_valuation_override.RepostItemValuationOverride"
}
```

**Purpose**: Replace core ERPNext classes with custom implementations.

#### Scheduled Tasks
```python
scheduler_events = {
    "hourly": [
        "custom_erp.api.fonepay.scheduled_process_unprocessed_qrs"
    ],
}
```

**Purpose**: Background jobs that run on a schedule.

#### Frontend Asset Injection
```python
app_include_js = [
    "/assets/custom_erp/lib/sajan.nepaliFunctions.min.js",
    "/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js",
    "/assets/custom_erp/js/nepali_date_adapter.js?v=5",
    "/assets/custom_erp/js/nepali_date_patch.js?v=5",
    "/assets/custom_erp/js/invoice_scanner.js"
]

app_include_css = [
    "/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.css",
    "/assets/custom_erp/css/nepali_date_overrides.css"
]
```

**Purpose**: Inject custom JS/CSS into Frappe Desk UI.

---

### 2. Fonepay Payment Integration (`api/fonepay.py`)

**Purpose**: Integration with Fonepay payment gateway for QR-based payments.

#### Key Functions

##### `create_dynamic_qr(customer, amount, sales_invoice=None)`
- Generates a dynamic QR code for payment
- Creates a QR record in the database
- Returns QR data and image URL
- **Whitelisted**: Yes

##### `check_qr_status(qr_id)`
- Polls Fonepay API for payment status
- Updates local QR record
- Returns current status
- **Whitelisted**: Yes

##### `listen_to_ws(qr_id)`
- Establishes WebSocket connection to Fonepay
- Listens for real-time payment notifications
- Uses background worker (inprocess or celery)
- **Whitelisted**: Yes

##### `finalize_payment_from_ws(qr_id, payment_data)`
- Called when payment is confirmed via WebSocket
- Creates Payment Entry in ERPNext
- Links to Sales Invoice if provided
- Uses database locks to prevent duplicates
- **Whitelisted**: Yes

##### `scheduled_process_unprocessed_qrs()`
- Runs hourly via scheduler
- Processes pending QR codes
- Batch processing with configurable size
- **Whitelisted**: Yes

#### Configuration (site_config.json)
```json
{
  "fonepay": {
    "merchant_code": "2005260033",
    "secret_key": "your-secret-key",
    "username": "username@fonepay.com",
    "password": "password",
    "env": "live",  // or "dev"
    "ws_worker": "inprocess",  // or "celery"
    "ws_timeout_seconds": 300,
    "scheduled_batch_size": 50,
    "scheduled_sleep_between": 0.2
  }
}
```

#### Database Schema
```python
# QR Payment Record (Custom DocType)
{
    "doctype": "QR Payment",
    "qr_id": "unique-id",
    "customer": "CUST-00001",
    "amount": 1000.00,
    "sales_invoice": "SINV-00001",
    "status": "pending",  // pending, paid, expired
    "qr_data": "base64-qr-image",
    "created_at": "2025-01-01 10:00:00",
    "paid_at": null
}
```

#### API Flow
```
Frontend                Backend                 Fonepay API
   |                       |                         |
   |-- create_dynamic_qr ->|                         |
   |                       |-- POST /thirdPartyDynamicQrDownload ->|
   |                       |<-- QR data --------------|
   |<-- QR image ---------|                         |
   |                       |                         |
   |-- listen_to_ws ------>|                         |
   |                       |-- WebSocket connect --->|
   |                       |<-- payment notification-|
   |                       |-- finalize_payment ---->|
   |<-- success ----------|                         |
```

---

### 3. Upload Sales API (`api/uploadsales.py`)

**Purpose**: Bulk import of sales invoices from CSV files.

#### Key Functions

##### `transform_and_preview(csv_data, driver=None, vehicle=None)`
- Parses CSV file
- Converts Nepali dates to Gregorian
- Resolves customer names to IDs
- Returns preview data
- **Whitelisted**: Yes

##### `enqueue_import_job(transformed_data, driver=None, vehicle=None)`
- Validates data
- Enqueues background job
- Returns job ID for tracking
- **Whitelisted**: Yes

##### `get_job_progress(job_id)`
- Returns current progress of import job
- Shows success/error counts
- **Whitelisted**: Yes

##### `run_data_import(data, driver=None, vehicle=None)`
- Actual import logic (runs in background)
- Creates Sales Invoices via Frappe Data Import
- Publishes real-time progress updates
- **Not whitelisted** (called internally)

#### CSV Format
```csv
Date,Customer Name,PAN No,Item Code,Qty,Rate,Amount
2082.07.09,ABC Company,123456789,ITEM-001,10,100,1000
```

#### Data Transformation Pipeline
```
CSV Upload
  ↓
Parse CSV (csv.DictReader)
  ↓
Convert Nepali Date → Gregorian
  ↓
Resolve Customer Name → Customer ID
  ↓
Validate Item Codes
  ↓
Transform to ERPNext format
  ↓
Preview (frontend)
  ↓
Enqueue Background Job
  ↓
Frappe Data Import
  ↓
Create Sales Invoices
```

---

### 4. Stock Valuation Override (`stock_valuation/stock_ledger_override.py`)

**Purpose**: Enforce fixed valuation rates for stock transactions to prevent rate changes.

#### Key Functions

##### `ensure_fixed_valuation_rate(doc, method=None)`
- Hook: `before_save`, `on_submit`
- Preserves original item rates
- Updates `valuation_rate` field
- Prevents GL entry mismatches

##### `ensure_fixed_valuation_rate_before_gl_creation(doc, method=None)`
- Hook: `before_insert`
- Sets valuation rate before GL entries are created
- Critical for accounting accuracy

##### `ensure_sle_fixed_valuation_rate(doc, method=None)`
- Hook: `before_insert` on Stock Ledger Entry
- Ensures SLE has correct valuation rate
- Prevents stock value discrepancies

##### `get_valuation_rate_for_item_details(item_code, ...)`
- Override: `erpnext.stock.get_item_details.get_valuation_rate`
- Returns fixed valuation rate for item
- Used in invoice creation

#### Problem Solved
ERPNext's default behavior updates item valuation rates based on purchase prices, which can cause:
- Incorrect GL entries
- Stock value mismatches
- Accounting discrepancies

This override ensures rates remain fixed unless explicitly changed.

---

### 5. Sales Invoice API (`sales_invoice/api.py`)

**Purpose**: Custom API endpoints for sales invoice data retrieval.

#### Key Functions

##### `get_sales_invoices(filters)`
- Returns filtered list of sales invoices
- Includes item details
- Supports customer, date range filters
- **Whitelisted**: Yes

##### `get_sales_invoice_summary(filters)`
- Returns grouped summary by customer and date
- Aggregates quantities and amounts
- **Whitelisted**: Yes

##### `get_customers()`
- Returns list of customers for dropdown
- **Whitelisted**: Yes

#### Response Format
```python
{
    "success": True,
    "data": [
        {
            "name": "SINV-00001",
            "customer": "CUST-00001",
            "customer_name": "ABC Company",
            "posting_date": "2025-01-01",
            "grand_total": 10000.00,
            "outstanding_amount": 5000.00,
            "status": "Submitted",
            "items": [
                {
                    "item_code": "ITEM-001",
                    "item_name": "Product A",
                    "qty": 10,
                    "rate": 100,
                    "amount": 1000,
                    "uom": "Nos"
                }
            ]
        }
    ]
}
```

---

### 6. Purchase Invoice Override (`purchase_invoice/purchase_invoice_override.py`)

**Purpose**: Custom behavior for purchase invoice processing.

#### Key Features
- Automatic attachment extraction from images
- OCR-based data extraction
- Custom validation logic
- Memory-optimized processing

---

### 7. Management Commands (`management/commands/`)

**Purpose**: CLI tools for data fixes and maintenance.

#### Key Commands

##### `fix_all_gl_entries.py`
- Fixes GL entries for all document types
- Runs in batch mode
- Logs progress

##### `fix_sales_invoice_gl_entries.py`
- Specifically fixes sales invoice GL entries
- Handles valuation rate mismatches

##### `repost_sales_invoices_with_updated_prices.py`
- Reposts invoices after price changes
- Updates stock ledger

##### `submit_draft_sales_invoices.py`
- Bulk submits draft invoices
- Validates before submission

#### Usage
```bash
bench --site [site-name] execute custom_erp.custom_erp.management.commands.fix_all_gl_entries.run
```

---

## Database Schema Extensions

### Custom Fields (via fixtures)
```python
# Sales Invoice custom fields
{
    "dt": "Sales Invoice",
    "fieldname": "custom_driver_for_vehicle",
    "fieldtype": "Link",
    "options": "Driver",
    "label": "Driver"
}

{
    "dt": "Sales Invoice",
    "fieldname": "custom_vehicle_for_delivery",
    "fieldtype": "Link",
    "options": "Vehicle",
    "label": "Vehicle"
}
```

### Custom DocTypes
- **QR Payment**: Fonepay payment tracking
- (Others defined in fixtures/)

---

## API Authentication

All whitelisted methods use Frappe's session-based authentication:

```python
@frappe.whitelist()
def my_api_function():
    # frappe.session.user is automatically available
    # CSRF protection is automatic
    pass
```

Frontend calls:
```javascript
// Frappe UI automatically includes session cookies
const resource = createResource({
  url: "custom_erp.api.fonepay.create_dynamic_qr",
  params: { customer: "CUST-001", amount: 1000 }
})
```

---

## Error Handling

### Standard Pattern
```python
@frappe.whitelist()
def my_function():
    try:
        # Logic here
        return {"success": True, "data": result}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "My Function Error")
        return {"success": False, "error": str(e)}
```

### Logging
```python
# Error logging
frappe.log_error(message, title)

# Info logging
frappe.logger().info("Message")

# Debug logging
frappe.logger().debug("Debug info")
```

---

## Performance Considerations

### Database Queries
```python
# Good: Use filters
invoices = frappe.get_all("Sales Invoice", 
    filters={"customer": customer, "posting_date": [">=", from_date]},
    fields=["name", "grand_total"]
)

# Bad: Load all then filter
invoices = frappe.get_all("Sales Invoice")
filtered = [inv for inv in invoices if inv.customer == customer]
```

### Background Jobs
```python
# For long-running tasks
frappe.enqueue(
    method="custom_erp.api.uploadsales.run_data_import",
    queue="long",
    timeout=3600,
    data=data
)
```

### Caching
```python
# Cache expensive queries
@frappe.whitelist()
def get_customers():
    return frappe.cache().get_value("customer_list",
        generator=lambda: frappe.get_all("Customer", fields=["name", "customer_name"])
    )
```

---

## Testing

### Unit Tests
```python
# test_sales_invoice.py
import frappe
import unittest

class TestSalesInvoice(unittest.TestCase):
    def test_valuation_rate_preserved(self):
        # Test logic
        pass
```

### Running Tests
```bash
bench --site [site] run-tests --app custom_erp
bench --site [site] run-tests --app custom_erp --module custom_erp.tests.test_sales_invoice
```

---

## Deployment Checklist

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build Frontend**
   ```bash
   cd frontend && npm ci && npm run build
   ```

3. **Install App**
   ```bash
   bench install-app custom_erp
   ```

4. **Configure Site**
   - Add Fonepay credentials to site_config.json
   - Set up scheduled jobs

5. **Migrate Database**
   ```bash
   bench --site [site] migrate
   ```

6. **Restart Services**
   ```bash
   bench restart
   ```
