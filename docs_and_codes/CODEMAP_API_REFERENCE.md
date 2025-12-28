# Custom ERP - API Reference

## API Endpoint Structure

All API endpoints follow Frappe's convention:
```
POST /api/method/{module}.{function}
```

Authentication: Session-based (automatic via Frappe)
CSRF Protection: Automatic via `@frappe.whitelist()`

---

## Sales Invoice API

### get_sales_invoices
**Endpoint**: `custom_erp.custom_erp.sales_invoice.api.get_sales_invoices`

**Purpose**: Retrieve filtered list of sales invoices with item details.

**Parameters**:
```json
{
  "filters": "{\"customer\": \"CUST-001\", \"from_date\": \"2025-01-01\", \"to_date\": \"2025-01-31\"}"
}
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "name": "SINV-00001",
      "customer": "CUST-001",
      "customer_name": "ABC Company",
      "posting_date": "2025-01-15",
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

### get_sales_invoice_summary
**Endpoint**: `custom_erp.custom_erp.sales_invoice.api.get_sales_invoice_summary`

**Purpose**: Get grouped summary by customer and date.

**Parameters**:
```json
{
  "filters": "{\"customer\": \"CUST-001\", \"from_date\": \"2025-01-01\", \"to_date\": \"2025-01-31\"}"
}
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "customer": "CUST-001",
      "customer_name": "ABC Company",
      "posting_date": "2025-01-15",
      "invoice_count": 3,
      "total_amount": 30000.00,
      "net_total": 28000.00,
      "outstanding_amount": 15000.00,
      "items": [
        {
          "item_code": "ITEM-001",
          "item_name": "Product A",
          "total_qty": 30,
          "avg_rate": 100,
          "total_amount": 3000,
          "uom": "Nos"
        }
      ]
    }
  ]
}
```

---

### get_customers
**Endpoint**: `custom_erp.custom_erp.sales_invoice.api.get_customers`

**Purpose**: Get list of customers for dropdown.

**Parameters**: None

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "name": "CUST-001",
      "customer_name": "ABC Company"
    }
  ]
}
```

---

## Fonepay Payment API

### create_dynamic_qr
**Endpoint**: `custom_erp.api.fonepay.create_dynamic_qr`

**Purpose**: Generate dynamic QR code for payment.

**Parameters**:
```json
{
  "customer": "CUST-001",
  "amount": 1000.00,
  "sales_invoice": "SINV-00001"  // optional
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "qr_id": "QR-2025-00001",
    "qr_data": "data:image/png;base64,...",
    "amount": 1000.00,
    "customer": "CUST-001",
    "sales_invoice": "SINV-00001",
    "expires_at": "2025-01-15T10:30:00"
  }
}
```

---

### check_qr_status
**Endpoint**: `custom_erp.api.fonepay.check_qr_status`

**Purpose**: Poll payment status.

**Parameters**:
```json
{
  "qr_id": "QR-2025-00001"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "qr_id": "QR-2025-00001",
    "status": "paid",  // pending, paid, expired
    "payment_entry": "PAY-00001",
    "paid_at": "2025-01-15T10:15:00"
  }
}
```

---

### listen_to_ws
**Endpoint**: `custom_erp.api.fonepay.listen_to_ws`

**Purpose**: Start WebSocket listener for real-time payment updates.

**Parameters**:
```json
{
  "qr_id": "QR-2025-00001"
}
```

**Response**:
```json
{
  "success": true,
  "message": "WebSocket listener started"
}
```

**WebSocket Events**:
```javascript
// Frontend listens to:
socket.on("payment_status", (data) => {
  // data = { qr_id, status, payment_entry }
})
```

---

### finalize_payment_from_ws
**Endpoint**: `custom_erp.api.fonepay.finalize_payment_from_ws`

**Purpose**: Complete payment after WebSocket notification.

**Parameters**:
```json
{
  "qr_id": "QR-2025-00001",
  "payment_data": {
    "transaction_id": "FP123456",
    "amount": 1000.00,
    "paid_at": "2025-01-15T10:15:00"
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "payment_entry": "PAY-00001",
    "qr_id": "QR-2025-00001",
    "status": "paid"
  }
}
```

---

### process_unprocessed_qrs
**Endpoint**: `custom_erp.api.fonepay.process_unprocessed_qrs`

**Purpose**: Manually trigger batch processing of pending QRs.

**Parameters**: None

**Response**:
```json
{
  "success": true,
  "processed": 10,
  "paid": 3,
  "expired": 2,
  "pending": 5
}
```

---

## Upload Sales API

### transform_and_preview
**Endpoint**: `custom_erp.api.uploadsales.transform_and_preview`

**Purpose**: Parse CSV and return preview data.

**Parameters**:
```json
{
  "csv_data": "Date,Customer Name,Item Code,Qty,Rate\n2082.07.09,ABC Company,ITEM-001,10,100",
  "driver": "DRV-001",  // optional
  "vehicle": "VEH-001"  // optional
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "rows": [
      {
        "posting_date": "26/10/2025",
        "customer": "CUST-001",
        "customer_name": "ABC Company",
        "item_code": "ITEM-001",
        "qty": 10,
        "rate": 100,
        "amount": 1000,
        "valid": true,
        "errors": []
      }
    ],
    "summary": {
      "total_rows": 1,
      "valid_rows": 1,
      "invalid_rows": 0,
      "total_amount": 1000
    }
  }
}
```

---

### enqueue_import_job
**Endpoint**: `custom_erp.api.uploadsales.enqueue_import_job`

**Purpose**: Start background import job.

**Parameters**:
```json
{
  "transformed_data": { /* preview data */ },
  "driver": "DRV-001",
  "vehicle": "VEH-001"
}
```

**Response**:
```json
{
  "success": true,
  "job_id": "JOB-2025-00001",
  "message": "Import job started"
}
```

---

### get_job_progress
**Endpoint**: `custom_erp.api.uploadsales.get_job_progress`

**Purpose**: Get import job progress.

**Parameters**:
```json
{
  "job_id": "JOB-2025-00001"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "job_id": "JOB-2025-00001",
    "status": "running",  // pending, running, completed, failed
    "total": 100,
    "processed": 45,
    "success": 40,
    "errors": 5,
    "error_details": [
      {
        "row": 10,
        "error": "Customer not found"
      }
    ]
  }
}
```

**WebSocket Events**:
```javascript
// Real-time progress updates
socket.on("upload_sales_progress", (data) => {
  // data = { job_id, total, processed, success, errors }
})
```

---

### get_drivers
**Endpoint**: `custom_erp.api.uploadsales.get_drivers`

**Purpose**: Get list of drivers.

**Parameters**: None

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "name": "DRV-001",
      "driver_name": "John Doe"
    }
  ]
}
```

---

### get_vehicles
**Endpoint**: `custom_erp.api.uploadsales.get_vehicles`

**Purpose**: Get list of vehicles.

**Parameters**: None

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "name": "VEH-001",
      "license_plate": "BA-1-PA-1234"
    }
  ]
}
```

---

### download_error_csv
**Endpoint**: `custom_erp.api.uploadsales.download_error_csv`

**Purpose**: Download CSV of failed rows.

**Parameters**:
```json
{
  "job_id": "JOB-2025-00001"
}
```

**Response**: CSV file download

---

## Purchase Invoice API

### extract_invoice
**Endpoint**: `custom_erp.custom_erp.purchase_invoice.api.extract_invoice`

**Purpose**: Extract invoice data from image using OCR.

**Parameters**:
```json
{
  "image_data": "data:image/png;base64,..."
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "invoiceNumber": "INV-001",
    "customerName": "ABC Company",
    "date": "2025-01-15",
    "amount": 1000.00,
    "items": [
      {
        "description": "Product A",
        "quantity": 10,
        "rate": 100
      }
    ]
  }
}
```

---

## Error Handling

All API endpoints follow this error format:

```json
{
  "success": false,
  "error": "Error message here",
  "exc_type": "ValidationError"  // optional
}
```

Common error codes:
- `ValidationError`: Invalid input data
- `PermissionError`: Insufficient permissions
- `DoesNotExistError`: Resource not found
- `DuplicateEntryError`: Duplicate record

---

## Authentication

### Session-based Auth
All API calls require valid Frappe session:

```javascript
// Frontend (automatic via Frappe UI)
const resource = createResource({
  url: "custom_erp.api.method"
})

// Session cookie is automatically included
```

### Checking Auth Status
```javascript
// data/session.js
export const session = createResource({
  url: "frappe.auth.get_logged_user",
  auto: true
})

// Usage
if (session.isLoggedIn) {
  // User is authenticated
}
```

---

## Rate Limiting

No explicit rate limiting implemented. Relies on Frappe's default behavior.

---

## CORS

CORS is handled by Frappe. For development:

```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## WebSocket Events

### Connection
```javascript
socket.on("connect", () => {
  console.log("Connected:", socket.id)
})

socket.on("disconnect", () => {
  console.log("Disconnected")
})
```

### Custom Events

#### payment_status
```javascript
socket.on("payment_status", (data) => {
  // data = { qr_id, status, payment_entry, paid_at }
})
```

#### upload_sales_progress
```javascript
socket.on("upload_sales_progress", (data) => {
  // data = { job_id, total, processed, success, errors }
})
```

---

## Testing APIs

### Using curl
```bash
# Login first to get session cookie
curl -X POST http://localhost:8000/api/method/login \
  -H "Content-Type: application/json" \
  -d '{"usr": "admin@example.com", "pwd": "password"}' \
  -c cookies.txt

# Call API with session
curl -X POST http://localhost:8000/api/method/custom_erp.custom_erp.sales_invoice.api.get_customers \
  -b cookies.txt
```

### Using Frappe Console
```python
# bench --site [site] console
import frappe
from custom_erp.custom_erp.sales_invoice.api import get_sales_invoices

result = get_sales_invoices(filters='{"customer": "CUST-001"}')
print(result)
```

---

## API Versioning

Currently no versioning. All endpoints are v1 by default.

Future consideration: `/api/v2/method/...`

---

## Best Practices

1. **Always check `success` field** in response
2. **Handle errors gracefully** with try-catch
3. **Use Frappe UI resources** for automatic state management
4. **Validate input** before sending to API
5. **Use WebSocket** for real-time updates instead of polling
6. **Cache responses** when appropriate
7. **Batch operations** for bulk data

---

## Frontend Integration Example

```javascript
import { createResource } from "frappe-ui"

// Define resource
const invoicesResource = createResource({
  url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoices",
  auto: false,
  onSuccess: (result) => {
    if (result.success) {
      invoices.value = result.data
    } else {
      error.value = result.error
    }
  },
  onError: (err) => {
    error.value = "Network error: " + err.message
  }
})

// Fetch data
const loadInvoices = async () => {
  await invoicesResource.fetch({
    filters: JSON.stringify({
      customer: "CUST-001",
      from_date: "2025-01-01",
      to_date: "2025-01-31"
    })
  })
}

// Access state
invoicesResource.loading  // true/false
invoicesResource.data     // response data
invoicesResource.error    // error object
```
