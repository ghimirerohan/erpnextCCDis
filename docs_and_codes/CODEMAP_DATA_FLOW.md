# Custom ERP - Data Flow & Architecture Patterns

## Overview

This document describes how data flows through the system, from user interaction to database and back.

---

## Request-Response Flow

### Standard API Call Flow

```
┌─────────────┐
│   Browser   │
│  (Vue App)  │
└──────┬──────┘
       │ 1. User Action (click button)
       ▼
┌─────────────────────┐
│ Vue Component       │
│ - createResource()  │
│ - resource.fetch()  │
└──────┬──────────────┘
       │ 2. HTTP POST /api/method/...
       ▼
┌─────────────────────┐
│  Frappe UI          │
│  - Add CSRF token   │
│  - Add session      │
└──────┬──────────────┘
       │ 3. HTTP Request
       ▼
┌─────────────────────┐
│  Frappe Server      │
│  - Validate session │
│  - Check CSRF       │
└──────┬──────────────┘
       │ 4. Route to method
       ▼
┌─────────────────────┐
│  Python Function    │
│  @frappe.whitelist()│
└──────┬──────────────┘
       │ 5. Database query
       ▼
┌─────────────────────┐
│  MariaDB/MySQL      │
│  - Execute query    │
└──────┬──────────────┘
       │ 6. Return rows
       ▼
┌─────────────────────┐
│  Python Function    │
│  - Transform data   │
│  - Return JSON      │
└──────┬──────────────┘
       │ 7. JSON Response
       ▼
┌─────────────────────┐
│  Frappe Server      │
│  - Serialize JSON   │
└──────┬──────────────┘
       │ 8. HTTP Response
       ▼
┌─────────────────────┐
│  Frappe UI          │
│  - Parse response   │
│  - Update state     │
└──────┬──────────────┘
       │ 9. Trigger onSuccess
       ▼
┌─────────────────────┐
│  Vue Component      │
│  - Update reactive  │
│  - Re-render UI     │
└─────────────────────┘
```

---

## Real-time WebSocket Flow

### Payment Status Updates

```
┌──────────────┐                    ┌──────────────┐
│   Frontend   │                    │   Backend    │
│   (QRPay)    │                    │  (Fonepay)   │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │ 1. create_dynamic_qr()            │
       ├──────────────────────────────────>│
       │                                   │
       │ 2. QR data + qr_id                │
       │<──────────────────────────────────┤
       │                                   │
       │ 3. Display QR to user             │
       │                                   │
       │ 4. listen_to_ws(qr_id)            │
       ├──────────────────────────────────>│
       │                                   │
       │                                   │ 5. Connect to Fonepay WS
       │                                   ├────────────────────>
       │                                   │                    ┌──────────┐
       │                                   │                    │ Fonepay  │
       │                                   │                    │   API    │
       │                                   │                    └────┬─────┘
       │                                   │                         │
       │                                   │ 6. Payment notification │
       │                                   │<────────────────────────┤
       │                                   │                         │
       │                                   │ 7. finalize_payment()   │
       │                                   │ - Create Payment Entry  │
       │                                   │ - Link to Invoice       │
       │                                   │                         │
       │ 8. Publish to Socket.IO           │                         │
       │   frappe.publish_realtime()       │                         │
       │<──────────────────────────────────┤                         │
       │                                   │                         │
       │ 9. Update UI (paid status)        │                         │
       │                                   │                         │
```

### Upload Sales Progress

```
┌──────────────┐                    ┌──────────────┐
│   Frontend   │                    │   Backend    │
│ (UploadSales)│                    │   Worker     │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │ 1. enqueue_import_job()           │
       ├──────────────────────────────────>│
       │                                   │
       │ 2. job_id                         │
       │<──────────────────────────────────┤
       │                                   │
       │                                   │ 3. Start background job
       │                                   │    frappe.enqueue()
       │                                   │
       │                                   │ 4. Process rows
       │                                   │    for row in data:
       │                                   │      create_invoice(row)
       │                                   │
       │ 5. Progress update (every 10 rows)│
       │   frappe.publish_realtime()       │
       │<──────────────────────────────────┤
       │                                   │
       │ 6. Update progress bar            │
       │                                   │
       │                                   │ 7. Continue processing
       │                                   │
       │ 8. Final update (completed)       │
       │<──────────────────────────────────┤
       │                                   │
       │ 9. Show completion message        │
       │                                   │
```

---

## Component Data Flow

### Home.vue - Sales Invoice Dashboard

```
User Action: Select Customer
       │
       ▼
┌─────────────────────────────────┐
│ CustomerSearch Component        │
│ - handleCustomerQuery()         │
│ - Fetch matching customers      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ GET /api/resource/Customer      │
│ filters: [['name', 'like', '%']]│
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Display customer list           │
│ (Autocomplete dropdown)         │
└────────────┬────────────────────┘
             │
             ▼
User Action: Select customer from list
       │
       ▼
┌─────────────────────────────────┐
│ onCustomerSelected()            │
│ - Set filters.customer          │
│ - Lock selection                │
└────────────┬────────────────────┘
             │
             ▼
User Action: Click "Load Data"
       │
       ▼
┌─────────────────────────────────┐
│ loadData()                      │
│ - Validate filters              │
│ - Set loading = true            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ salesInvoicesResource.fetch()   │
│ params: { filters: JSON }       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Backend: get_sales_invoices()   │
│ - Parse filters                 │
│ - Query Sales Invoice           │
│ - Join with items               │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Return invoice data with items  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ onSuccess callback              │
│ - data.value = result.data      │
│ - loading = false               │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Vue reactivity triggers         │
│ - Re-render table               │
│ - Display invoice data          │
└─────────────────────────────────┘
```

---

## State Management Patterns

### 1. Local Component State

```javascript
// Simple reactive state
const loading = ref(false)
const data = ref([])
const error = ref("")

// Reactive object
const filters = reactive({
  customer: "",
  from_date: "",
  to_date: ""
})

// Computed derived state
const hasData = computed(() => data.value.length > 0)
const totalAmount = computed(() => 
  data.value.reduce((sum, item) => sum + item.amount, 0)
)
```

### 2. Frappe UI Resource State

```javascript
const resource = createResource({
  url: "...",
  auto: false
})

// Automatic state management
resource.loading  // boolean
resource.data     // response data
resource.error    // error object

// Manual state updates
resource.fetch()  // triggers loading = true
// onSuccess → loading = false, data = result
// onError → loading = false, error = err
```

### 3. Global Session State

```javascript
// data/session.js
export const session = createResource({
  url: "frappe.auth.get_logged_user",
  auto: true  // Fetch on mount
})

// Available everywhere
import { session } from "@/data/session"

if (session.isLoggedIn) {
  // User authenticated
}
```

### 4. WebSocket Event State

```javascript
// Inject socket
const socket = inject("$socket")

// Listen to events
socket.on("payment_status", (data) => {
  // Update local state
  paymentStatus.value = data.status
})

// Cleanup on unmount
onUnmounted(() => {
  socket.off("payment_status")
})
```

---

## Database Query Patterns

### 1. Simple List Query

```python
# Get all customers
customers = frappe.get_all(
    "Customer",
    fields=["name", "customer_name"],
    order_by="customer_name"
)
```

### 2. Filtered Query

```python
# Get invoices for customer in date range
invoices = frappe.get_all(
    "Sales Invoice",
    filters={
        "customer": customer,
        "posting_date": ["between", [from_date, to_date]],
        "docstatus": 1  # Submitted only
    },
    fields=["name", "grand_total", "outstanding_amount"]
)
```

### 3. Join Query (Child Table)

```python
# Get invoice with items
invoice = frappe.get_doc("Sales Invoice", invoice_name)

# Items are automatically loaded
for item in invoice.items:
    print(item.item_code, item.qty, item.rate)
```

### 4. SQL Query (Complex)

```python
# Custom SQL for complex queries
results = frappe.db.sql("""
    SELECT 
        si.name,
        si.customer,
        SUM(sii.amount) as total_amount
    FROM `tabSales Invoice` si
    JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
    WHERE si.customer = %(customer)s
    GROUP BY si.name
""", {"customer": customer}, as_dict=True)
```

### 5. Aggregation Query

```python
# Get summary data
summary = frappe.db.sql("""
    SELECT 
        customer,
        posting_date,
        COUNT(*) as invoice_count,
        SUM(grand_total) as total_amount
    FROM `tabSales Invoice`
    WHERE customer = %(customer)s
    GROUP BY customer, posting_date
""", {"customer": customer}, as_dict=True)
```

---

## Background Job Flow

### Enqueue Pattern

```python
# API endpoint
@frappe.whitelist()
def start_import(data):
    # Enqueue long-running task
    job = frappe.enqueue(
        method="custom_erp.api.uploadsales.run_data_import",
        queue="long",  # or "default", "short"
        timeout=3600,  # 1 hour
        is_async=True,
        job_name=f"import_sales_{frappe.utils.now()}",
        data=data
    )
    
    return {"success": True, "job_id": job.name}

# Background worker function
def run_data_import(data):
    total = len(data)
    
    for i, row in enumerate(data):
        try:
            # Create invoice
            create_invoice(row)
            
            # Publish progress every 10 rows
            if i % 10 == 0:
                frappe.publish_realtime(
                    "upload_sales_progress",
                    {
                        "total": total,
                        "processed": i + 1,
                        "success": success_count,
                        "errors": error_count
                    },
                    user=frappe.session.user
                )
        except Exception as e:
            error_count += 1
            frappe.log_error(str(e), "Import Error")
    
    # Final update
    frappe.publish_realtime(
        "upload_sales_progress",
        {"status": "completed", "total": total},
        user=frappe.session.user
    )
```

---

## Error Handling Flow

### Frontend Error Handling

```javascript
const loadData = async () => {
  loading.value = true
  error.value = ""
  
  try {
    await resource.fetch({ filters: JSON.stringify(filters) })
    
    if (resource.data.success) {
      data.value = resource.data.data
    } else {
      // Backend returned error
      error.value = resource.data.error || "Unknown error"
    }
  } catch (err) {
    // Network or parsing error
    error.value = "Failed to load data: " + err.message
  } finally {
    loading.value = false
  }
}
```

### Backend Error Handling

```python
@frappe.whitelist()
def get_sales_invoices(filters):
    try:
        # Parse filters
        filters_dict = json.loads(filters)
        
        # Validate
        if not filters_dict.get("customer"):
            return {"success": False, "error": "Customer is required"}
        
        # Query data
        invoices = frappe.get_all("Sales Invoice", filters=filters_dict)
        
        return {"success": True, "data": invoices}
        
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid filters format"}
    
    except frappe.PermissionError:
        return {"success": False, "error": "Insufficient permissions"}
    
    except Exception as e:
        # Log error for debugging
        frappe.log_error(frappe.get_traceback(), "Get Sales Invoices Error")
        return {"success": False, "error": str(e)}
```

---

## Caching Strategy

### 1. Frontend Resource Caching

```javascript
const resource = createResource({
  url: "...",
  cache: true,
  cacheKey: "customers_list"
})

// First call: fetches from server
await resource.fetch()

// Subsequent calls: returns cached data
await resource.fetch()  // Instant
```

### 2. Backend Query Caching

```python
def get_customers():
    # Cache for 5 minutes
    return frappe.cache().get_value(
        "customer_list",
        generator=lambda: frappe.get_all("Customer", fields=["name", "customer_name"]),
        expires_in_sec=300
    )
```

### 3. Browser LocalStorage

```javascript
// Store user preferences
localStorage.setItem("last_customer", customer)

// Retrieve on mount
onMounted(() => {
  const lastCustomer = localStorage.getItem("last_customer")
  if (lastCustomer) {
    filters.customer = lastCustomer
  }
})
```

---

## Optimistic Updates

### Pattern for Instant UI Feedback

```javascript
const deleteInvoice = async (invoiceId) => {
  // 1. Optimistically update UI
  const originalData = [...data.value]
  data.value = data.value.filter(inv => inv.name !== invoiceId)
  
  try {
    // 2. Send request to backend
    await deleteResource.fetch({ invoice_id: invoiceId })
    
    if (!deleteResource.data.success) {
      throw new Error(deleteResource.data.error)
    }
    
    // 3. Success - UI already updated
    showSuccessMessage("Invoice deleted")
    
  } catch (err) {
    // 4. Rollback on error
    data.value = originalData
    showErrorMessage("Failed to delete: " + err.message)
  }
}
```

---

## Data Transformation Pipeline

### Upload Sales Example

```
CSV File
   │
   ▼
┌─────────────────────────────────┐
│ 1. Parse CSV                    │
│    csv.DictReader()             │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 2. Transform Dates              │
│    Nepali → Gregorian           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 3. Resolve Customers            │
│    Name → Customer ID           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 4. Validate Items               │
│    Check item codes exist       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 5. Calculate Amounts            │
│    qty * rate = amount          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 6. Group by Invoice             │
│    Customer + Date → Invoice    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 7. Create ERPNext Format        │
│    Map to Sales Invoice schema  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 8. Preview to User              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 9. Background Import            │
│    Create actual invoices       │
└─────────────────────────────────┘
```

---

## Performance Considerations

### 1. Pagination

```python
# Backend
invoices = frappe.get_all(
    "Sales Invoice",
    filters=filters,
    fields=fields,
    limit_start=page * page_size,
    limit_page_length=page_size
)
```

### 2. Lazy Loading

```vue
<!-- Frontend -->
<template>
  <div v-for="invoice in visibleInvoices" :key="invoice.name">
    <!-- Only render visible items -->
  </div>
</template>

<script setup>
import { computed } from "vue"

const visibleInvoices = computed(() => {
  return invoices.value.slice(0, currentPage.value * pageSize)
})
</script>
```

### 3. Debouncing

```javascript
import { debounce } from "lodash"

const searchCustomers = debounce(async (query) => {
  // Only search after user stops typing for 300ms
  await customerResource.fetch({ query })
}, 300)
```

### 4. Request Deduplication

```javascript
// Frappe UI automatically deduplicates
resource.fetch()  // Request 1
resource.fetch()  // Ignored (request 1 still pending)
resource.fetch()  // Ignored
```

---

## Security Flow

### Authentication Check

```
Request
   │
   ▼
┌─────────────────────────────────┐
│ Frappe Middleware               │
│ - Check session cookie          │
│ - Validate CSRF token           │
└────────────┬────────────────────┘
             │
             ▼
        Authenticated?
             │
      ┌──────┴──────┐
      │             │
     Yes           No
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ Process  │  │ Return   │
│ Request  │  │ 403      │
└──────────┘  └──────────┘
```

### Permission Check

```python
@frappe.whitelist()
def get_sales_invoices(filters):
    # Frappe automatically checks if user has read permission
    # on Sales Invoice doctype
    
    invoices = frappe.get_all(
        "Sales Invoice",
        filters=filters
    )  # Raises PermissionError if no access
    
    return {"success": True, "data": invoices}
```

---

## Summary

Key data flow patterns:
1. **Request-Response**: Standard API calls via Frappe UI resources
2. **WebSocket**: Real-time updates for payments and progress
3. **Background Jobs**: Long-running tasks with progress tracking
4. **State Management**: Local, resource, global, and event-driven
5. **Error Handling**: Graceful degradation with user feedback
6. **Caching**: Multi-layer caching for performance
7. **Security**: Session-based auth with CSRF protection
