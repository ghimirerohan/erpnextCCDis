<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Sales Invoice Dashboard</h1>
            <p class="text-sm text-gray-600">Welcome {{ session.user }}!</p>
          </div>
          <div class="flex gap-2">
          <Button @click="$router.push({ name: 'Scanner' })" theme="blue" variant="solid">
            Open Scanner
          </Button>
          <Button @click="session.logout.submit()" theme="gray" variant="outline">
            Logout
          </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Filters Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Filters</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="relative">
            <label class="block text-sm font-medium text-gray-700 mb-2">Customer</label>
            <div class="relative">
              <div v-if="selectionLocked" class="border border-gray-300 rounded-md p-3">
                <div class="text-sm font-medium text-gray-900">{{ selectedCustomer.customer_name }}</div>
                <div class="text-xs text-gray-600 mt-1">
                  <span>Code: {{ selectedCustomer.customer_code || '—' }}</span>
                  <span class="mx-2">|</span>
                  <span>Invoice: {{ selectedCustomer.invoice_no || '—' }}</span>
                </div>
                <div class="mt-2">
                  <button @click="resetSelection" class="text-sm text-blue-600 underline">Change selection</button>
                </div>
              </div>
              <div v-else>
                <div class="flex flex-wrap gap-2 mb-3">
                  <button
                    @click="selectMode = 'list'"
                    :class="[
                      'flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors',
                      selectMode === 'list' ? 'bg-blue-50 border-blue-400 text-blue-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    Customer List
                  </button>
                  <button
                    @click="selectMode = 'qr'"
                    :class="[
                      'flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors',
                      selectMode === 'qr' ? 'bg-blue-50 border-blue-400 text-blue-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    QR Scanner
                  </button>
                  <button
                    @click="selectMode = 'photo'"
                    :class="[
                      'flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors',
                      selectMode === 'photo' ? 'bg-blue-50 border-blue-400 text-blue-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    Photo / Camera
                  </button>
                </div>
                <div v-if="selectMode === 'qr'" class="p-3 border border-gray-200 rounded-md text-sm text-gray-700">
                  <div v-if="qrSupported">
                    <div class="mb-2">Point your camera at the QR code.</div>
                    <video ref="qrVideo" class="w-full rounded" autoplay playsinline muted></video>
                    <div class="mt-2 text-xs text-gray-500">Scanning...</div>
                  </div>
                  <div v-else>
                    QR scanning is not supported on this device/browser. Please use Photo.
                  </div>
                </div>
                <div v-else-if="selectMode === 'photo'" class="p-3 border border-gray-200 rounded-md">
                  <input type="file" accept="image/*" capture="environment" @change="onPhotoSelected" />
                  <div v-if="extractLoading" class="mt-2 text-sm text-gray-600">Processing image...</div>
                  <Alert v-if="extractError" theme="red" class="mt-2">{{ extractError }}</Alert>
                </div>
                <div v-else-if="selectMode === 'list'" class="p-3 border border-gray-200 rounded-md">
                  <Autocomplete
                    v-model="selectedCustomerLabel"
                    :options="customerOptions"
                    :loading="customerListLoading"
                    :debounce="300"
                    placeholder="Search by customer name or code..."
                    @update:query="handleCustomerQuery"
                    @select="onCustomerSelected"
                    :clearable="true"
                  />
                  <p v-if="!filters.customer" class="mt-2 text-sm text-gray-500">Start typing to search for a customer</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">From Date</label>
            <input 
              type="date" 
              v-model="filters.from_date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">To Date</label>
            <input 
              type="date" 
              v-model="filters.to_date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <Button 
            @click="loadData" 
            :loading="loading" 
            theme="blue" 
            variant="solid"
            :disabled="!filters.customer || !filters.from_date || !filters.to_date"
          >
            Load Data
          </Button>
        </div>
      </div>

      <!-- View Toggle -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">View Options</h2>
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button
              @click="viewMode = 'bill'"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                viewMode === 'bill' 
                  ? 'bg-white text-blue-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              Bill-wise View
            </button>
            <button
              @click="viewMode = 'summary'"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                viewMode === 'summary' 
                  ? 'bg-white text-blue-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              Summary View
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Loading data...</span>
      </div>

      <!-- Error State -->
      <Alert v-if="error" theme="red" class="mb-6">
        {{ error }}
      </Alert>

      <!-- Bill-wise View -->
      <div v-if="viewMode === 'bill' && !loading && data.length > 0" class="space-y-6">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">
              Sales Invoices ({{ data.length }} invoices)
            </h3>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Invoice
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Amount
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Outstanding
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="invoice in data" :key="invoice.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                    {{ invoice.name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(invoice.posting_date) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ invoice.customer_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <Badge :theme="getStatusTheme(invoice.status)">
                      {{ invoice.status }}
                    </Badge>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium">
                    {{ formatCurrency(invoice.grand_total) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ formatCurrency(invoice.outstanding_amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Invoice Details -->
        <div v-for="invoice in data" :key="`details-${invoice.name}`" class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h4 class="text-md font-semibold text-gray-900">
              Invoice: {{ invoice.name }} - {{ invoice.customer_name }}
            </h4>
            <p class="text-sm text-gray-600">
              Date: {{ formatDate(invoice.posting_date) }} | 
              Total: {{ formatCurrency(invoice.grand_total) }}
            </p>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Item
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Qty
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rate
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in invoice.items" :key="item.item_code" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ item.item_code }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-900">
                    {{ item.item_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ item.qty }} {{ item.uom }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ formatCurrency(item.rate) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium">
                    {{ formatCurrency(item.amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Summary View -->
      <div v-if="viewMode === 'summary' && !loading && summaryData.length > 0" class="space-y-6">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">
              Summary by Customer & Date ({{ summaryData.length }} groups)
            </h3>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Invoices
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Amount
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Net Total
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Outstanding
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="group in summaryData" :key="`${group.customer}-${group.posting_date}`" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ group.customer_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(group.posting_date) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                    {{ group.invoice_count }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium">
                    {{ formatCurrency(group.total_amount) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ formatCurrency(group.net_total) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ formatCurrency(group.outstanding_amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Item Summary -->
        <div v-for="group in summaryData" :key="`summary-${group.customer}-${group.posting_date}`" class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h4 class="text-md font-semibold text-gray-900">
              {{ group.customer_name }} - {{ formatDate(group.posting_date) }}
            </h4>
            <p class="text-sm text-gray-600">
              {{ group.invoice_count }} invoices | 
              Total: {{ formatCurrency(group.total_amount) }}
            </p>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Item
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Qty
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Rate
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Amount
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in group.items" :key="item.item_code" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ item.item_code }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-900">
                    {{ item.item_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ item.total_qty }} {{ item.uom }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                    {{ formatCurrency(item.avg_rate) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium">
                    {{ formatCurrency(item.total_amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && data.length === 0 && summaryData.length === 0" class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No data found</h3>
        <p class="text-gray-600">Try adjusting your filters or selecting a different date range.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from "vue"
import { createResource, Autocomplete } from "frappe-ui"
import { session } from "../data/session"

// Reactive data
const loading = ref(false)
const error = ref("")
const viewMode = ref("bill")
const data = ref([])
const summaryData = ref([])

const filters = reactive({
  customer: "",
  from_date: "",
  to_date: ""
})

// New customer selection flow state
const selectionLocked = ref(false)
const selectMode = ref('list')
const extractLoading = ref(false)
const extractError = ref("")
const selectedCustomer = ref({ customer: "", customer_name: "", customer_code: "", invoice_no: "" })
const qrSupported = typeof window !== 'undefined' && 'BarcodeDetector' in window
const qrVideo = ref(null)

// Customer list selection state
const selectedCustomerLabel = ref("")
const customerListLoading = ref(false)
const customerList = ref([])

// Computed options for autocomplete
const customerOptions = computed(() => {
  return customerList.value.map(c => ({
    label: c.customer_name || c.name,
    value: c.name,
    description: c.name
  }))
})

const salesInvoicesResource = createResource({
  url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoices",
  auto: false,
  onSuccess: (result) => {
    if (result.success) {
      data.value = result.data
      error.value = ""
    } else {
      error.value = result.error || "Failed to load sales invoices"
    }
  },
  onError: (err) => {
    error.value = "Failed to load sales invoices: " + err.message
  }
})

const salesInvoiceSummaryResource = createResource({
  url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoice_summary",
  auto: false,
  onSuccess: (result) => {
    if (result.success) {
      summaryData.value = result.data
      error.value = ""
    } else {
      error.value = result.error || "Failed to load summary data"
    }
  },
  onError: (err) => {
    error.value = "Failed to load summary data: " + err.message
  }
})

// Methods
const loadData = async () => {
  if (!filters.customer || !filters.from_date || !filters.to_date) {
    error.value = "Please fill in all required fields"
    return
  }

  loading.value = true
  error.value = ""

  try {
    const filtersParam = JSON.stringify(filters)
    
    if (viewMode.value === "bill") {
      await salesInvoicesResource.fetch({ filters: filtersParam })
    } else {
      await salesInvoiceSummaryResource.fetch({ filters: filtersParam })
    }
  } catch (err) {
    error.value = "Failed to load data: " + err.message
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ""
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return "0.00"
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const getStatusTheme = (status) => {
  const themes = {
    'Paid': 'green',
    'Unpaid': 'red',
    'Overdue': 'orange',
    'Draft': 'gray',
    'Submitted': 'blue'
  }
  return themes[status] || 'gray'
}

// New customer extraction + resolution methods
const resetSelection = () => {
  selectionLocked.value = false
  filters.customer = ""
  selectedCustomer.value = { customer: "", customer_name: "", customer_code: "", invoice_no: "" }
  selectedCustomerLabel.value = ""
  extractError.value = ""
  customerList.value = []
}

const onPhotoSelected = async (event) => {
  const file = event?.target?.files?.[0]
  if (!file) return
  extractError.value = ""
  extractLoading.value = true
  try {
    // Convert to base64 data URL and call Frappe server-side extractor
    const b64 = await new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(String(reader.result))
      reader.onerror = reject
      reader.readAsDataURL(file)
    })
    const res = await fetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_data: b64 })
    })
    const json = await res.json()
    const msg = json?.message || json
    if (!res.ok || !msg?.success || !msg?.data) {
      throw new Error(msg?.error || `Extraction failed (${res.status})`)
    }

    const invoiceBillNumber = msg.data.invoiceNumber || ''
    const customerName = msg.data.customerName || ''
    // Minimal resolver: try invoice number first; customerCode not available from full extractor
    const resolved = await resolveCustomer({ invoiceBillNumber, customerCode: '' })
    if (!resolved) {
      throw new Error('Could not find matching customer from code or invoice')
    }
    filters.customer = resolved.customer
    selectedCustomer.value = {
      customer: resolved.customer,
      customer_name: resolved.customer_name || customerName || resolved.customer,
      customer_code: '',
      invoice_no: invoiceBillNumber || ''
    }
    selectionLocked.value = true
  } catch (e) {
    extractError.value = e.message || 'Failed to process image'
  } finally {
    extractLoading.value = false
  }
}

async function resolveCustomer({ invoiceBillNumber, customerCode }) {
  // Priority 1: by customerCode
  if (customerCode) {
    // Try common fields one by one to avoid server errors on unknown fields
    const fieldsToTry = ['mobile_no', 'customer_code']
    for (const field of fieldsToTry) {
      try {
        const byCode = await findCustomerByField(field, customerCode)
        if (byCode) return byCode
      } catch (_) {
        // ignore and try next
      }
    }
  }
  // Fallback: use invoice number to read Sales Invoice and derive customer
  if (invoiceBillNumber) {
    try {
      const invRes = await fetch(`/api/resource/Sales%20Invoice/${encodeURIComponent(invoiceBillNumber)}`)
      if (invRes.ok) {
        const invJson = await invRes.json()
        const doc = invJson?.data
        if (doc?.customer) {
          return { customer: doc.customer, customer_name: doc.customer_name || doc.customer }
        }
      }
    } catch (_) {}
  }
  return null
}

async function findCustomerByField(field, value) {
  const params = new URLSearchParams()
  params.set('fields', JSON.stringify(['name', 'customer_name']))
  params.set('filters', JSON.stringify([[field, '=', String(value)]]))
  params.set('limit_page_length', '1')
  const res = await fetch(`/api/resource/Customer?${params.toString()}`)
  if (!res.ok) return null
  const json = await res.json()
  const list = json?.data
  if (Array.isArray(list) && list.length > 0) {
    return { customer: list[0].name, customer_name: list[0].customer_name || list[0].name }
  }
  return null
}

// Customer list query handler
const handleCustomerQuery = async (query) => {
  if (!query || query.length < 2) {
    customerList.value = []
    return
  }
  
  customerListLoading.value = true
  try {
    const params = new URLSearchParams()
    params.set('fields', JSON.stringify(['name', 'customer_name', 'customer_code', 'mobile_no']))
    params.set('filters', JSON.stringify([]))
    params.set('or_filters', JSON.stringify([
      ['customer_name', 'like', `%${query}%`],
      ['name', 'like', `%${query}%`],
      ['customer_code', 'like', `%${query}%`],
      ['mobile_no', 'like', `%${query}%`]
    ]))
    params.set('limit_page_length', '20')
    
    const res = await fetch(`/api/resource/Customer?${params.toString()}`)
    if (res.ok) {
      const json = await res.json()
      customerList.value = json?.data || []
    }
  } catch (e) {
    console.error('Failed to fetch customers:', e)
    customerList.value = []
  } finally {
    customerListLoading.value = false
  }
}

// Customer list selection handler
const onCustomerSelected = async (option) => {
  if (!option || !option.value) return
  
  try {
    // Fetch full customer details
    const res = await fetch(`/api/resource/Customer/${encodeURIComponent(option.value)}`)
    if (!res.ok) throw new Error('Failed to fetch customer details')
    
    const json = await res.json()
    const customer = json?.data
    
    if (customer) {
      filters.customer = customer.name
      selectedCustomer.value = {
        customer: customer.name,
        customer_name: customer.customer_name || customer.name,
        customer_code: customer.customer_code || customer.mobile_no || '',
        invoice_no: ''
      }
      selectedCustomerLabel.value = customer.customer_name || customer.name
      selectionLocked.value = true
    }
  } catch (e) {
    error.value = 'Failed to load customer details: ' + (e.message || 'Unknown error')
  }
}

// Watch for view mode changes
watch(viewMode, () => {
  if (filters.customer && filters.from_date && filters.to_date) {
    loadData()
  }
})

// Initialize
onMounted(() => {
  // Set default dates (last 30 days)
  const today = new Date()
  const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000))
  
  filters.to_date = today.toISOString().split('T')[0]
  filters.from_date = thirtyDaysAgo.toISOString().split('T')[0]
})
</script>

<style scoped>
/* Custom styles for better responsiveness */
@media (max-width: 768px) {
  .grid-cols-1.md\:grid-cols-3 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* Smooth transitions */
.transition-colors {
  transition: all 0.2s ease-in-out;
}

/* Hover effects */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

/* Custom scrollbar for tables */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
