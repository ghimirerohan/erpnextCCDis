# CustomerSearch Component

A reusable, mobile-friendly customer search and selection component for Vue 3 applications. This component provides a better alternative to Frappe UI's Autocomplete component with improved mobile UX and keyboard handling.

## Features

- ✅ **Mobile-optimized**: Works perfectly on mobile devices with proper keyboard handling
- ✅ **Real-time search**: Filter customers by name or code as you type
- ✅ **Customizable**: Configurable API endpoint, labels, placeholders, and help text
- ✅ **Vue 3 compatible**: Uses Composition API with v-model support
- ✅ **Flexible**: Can be used with any customer search API endpoint

## Installation

The component is located at:
```
src/components/CustomerSearch.vue
```

## Basic Usage

```vue
<template>
  <CustomerSearch
    v-model="selectedCustomerId"
    label="Customer"
    @select="handleCustomerSelect"
  />
</template>

<script setup>
import { ref } from 'vue'
import CustomerSearch from '@/components/CustomerSearch.vue'

const selectedCustomerId = ref(null)

const handleCustomerSelect = (customerData) => {
  console.log('Selected customer:', customerData)
  // customerData contains: value, name, customer_name, customer_group, etc.
}
</script>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `modelValue` | String/Number | `null` | The selected customer ID (supports v-model) |
| `label` | String | `'Customer'` | Label text displayed above the input |
| `placeholder` | String | `'Search by customer name or code'` | Placeholder text for the input |
| `helpText` | String | `'Start typing to search...'` | Help text shown below the input when no customer is selected |
| `apiUrl` | String | `'custom_erp.custom_erp.api.fonepay.search_customers'` | API endpoint URL for fetching customers |
| `limit` | Number | `10000` | Maximum number of customers to fetch |
| `autoLoad` | Boolean | `true` | Whether to automatically load customers on mount |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `update:modelValue` | `customerId` | Emitted when customer selection changes (for v-model) |
| `change` | `customerId` | Emitted when customer selection changes |
| `select` | `customerData` | Emitted when a customer is selected, includes full customer object |

## Customer Data Structure

The `select` event emits a customer object with the following structure:

```javascript
{
  value: "CUST-001",              // Customer ID/code
  name: "CUST-001",               // Customer ID/code (alias)
  customer_name: "ABC Company",   // Customer name
  customer_group: "Retail",       // Customer group (if available)
  territory: "Nepal",             // Territory (if available)
  mobile_no: "1234567890",        // Mobile number (if available)
  email_id: "abc@example.com",    // Email (if available)
  tax_id: "TAX123",               // Tax ID (if available)
  address_display: "...",          // Formatted address (if available)
  customer_primary_address: "...", // Primary address (if available)
  // ... any other fields returned by the API
}
```

## API Response Format

The component expects the API to return data in one of these formats:

```javascript
// Preferred format
{
  "customers": [
    {
      "name": "CUST-001",
      "customer_name": "ABC Company",
      // ... other fields
    }
  ]
}

// Alternative formats also supported:
// - Direct array: [{...}, {...}]
// - Wrapped in message: { message: { customers: [...] } }
// - Wrapped in data: { data: [...] }
```

## Advanced Usage

### Custom API Endpoint

```vue
<CustomerSearch
  v-model="customerId"
  api-url="your.custom.api.endpoint"
  @select="handleSelect"
/>
```

### Manual Loading

```vue
<template>
  <CustomerSearch
    ref="customerSearchRef"
    v-model="customerId"
    :auto-load="false"
    @select="handleSelect"
  />
  <button @click="loadCustomers">Load Customers</button>
</template>

<script setup>
import { ref } from 'vue'
import CustomerSearch from '@/components/CustomerSearch.vue'

const customerSearchRef = ref(null)
const customerId = ref(null)

const loadCustomers = () => {
  customerSearchRef.value?.loadCustomers()
}
</script>
```

### Clearing Selection

```vue
<template>
  <CustomerSearch
    ref="customerSearchRef"
    v-model="customerId"
  />
  <button @click="clearSelection">Clear</button>
</template>

<script setup>
import { ref } from 'vue'
import CustomerSearch from '@/components/CustomerSearch.vue'

const customerSearchRef = ref(null)
const customerId = ref(null)

const clearSelection = () => {
  customerSearchRef.value?.clear()
}
</script>
```

## Exposed Methods

The component exposes these methods via template ref:

- `loadCustomers(query?: string)` - Manually load/refresh customers
- `refresh()` - Alias for `loadCustomers()`
- `clear()` - Clear the selection and reset the input

## Example: Full Integration

```vue
<template>
  <div>
    <CustomerSearch
      v-model="selectedCustomerId"
      label="Select Customer"
      placeholder="Type customer name or code..."
      help-text="Start typing to search for customers"
      @select="onCustomerSelect"
    />
    
    <div v-if="selectedCustomer" class="mt-4">
      <h3>Selected Customer Details</h3>
      <p>Name: {{ selectedCustomer.customer_name }}</p>
      <p>Code: {{ selectedCustomer.name }}</p>
      <p v-if="selectedCustomer.mobile_no">Phone: {{ selectedCustomer.mobile_no }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CustomerSearch from '@/components/CustomerSearch.vue'

const selectedCustomerId = ref(null)
const selectedCustomer = ref(null)

const onCustomerSelect = (customerData) => {
  selectedCustomer.value = customerData
  console.log('Customer selected:', customerData)
}
</script>
```

## Styling

The component uses Tailwind CSS classes and includes mobile-optimized styles. It's fully responsive and works well on:
- Mobile devices (iOS/Android)
- Tablets
- Desktop browsers

## Notes

- The component automatically handles keyboard positioning on mobile devices
- Search results are limited to 50 items for performance
- The component shows first 50 customers when focused (no search query)
- All customer data is cached after initial load for fast filtering

