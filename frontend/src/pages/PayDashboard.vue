<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4 sm:py-6">
          <div class="flex items-center space-x-3 sm:space-x-4">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-blue-600 rounded-lg">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Pay Dashboard</h1>
              <p class="text-xs sm:text-sm text-gray-600">Today's Fonepay QR Statistics</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border border-gray-300 rounded-md shadow-sm text-xs sm:text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="w-4 h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8">
      <!-- Top Summary Card -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-6">
          <div class="space-y-2">
            <div class="text-xs sm:text-sm text-gray-500">Today (BS)</div>
            <div class="text-xl sm:text-2xl font-bold text-gray-900">{{ bsToday || adToday }}</div>
            <div class="text-sm sm:text-base text-gray-700">
              <span class="font-medium">{{ summary.current_user_full_name || summary.current_user || session.user }}</span>
            </div>
          </div>
          <div class="flex-1 sm:text-center space-y-2 lg:max-w-md lg:mx-auto">
            <div class="text-xs sm:text-sm uppercase text-gray-600 tracking-wide mb-2">Today's Total Success</div>
            <div class="text-2xl sm:text-3xl lg:text-4xl font-bold text-blue-600">NPR {{ formatAmount(summary.total_success_amount) }}</div>
            <div class="text-sm text-gray-500">{{ summary.total_success_count || 0 }} payments</div>
            <div v-if="summary.unprocessed_count > 0" class="pt-2 border-t border-gray-200">
              <div class="text-xs text-amber-700 font-medium mb-1">Unprocessed Transactions</div>
              <div class="text-lg sm:text-xl font-bold text-amber-600">{{ summary.unprocessed_count }}</div>
            </div>
          </div>
          <div class="flex flex-col gap-2">
            <button
              @click="refreshAll"
              :disabled="loading || processingUnprocessed"
              class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 active:scale-95 transition"
            >
              <svg v-if="loading" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
            <button
              v-if="summary.unprocessed_count >= 1"
              @click="processAllUnprocessed"
              :disabled="processingUnprocessed || loading"
              class="inline-flex items-center justify-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg shadow hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 active:scale-95 transition"
            >
              <svg v-if="processingUnprocessed" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Process All ({{ summary.unprocessed_count }})
            </button>
          </div>
        </div>
      </section>

      <!-- View Mode Switcher and Filters -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <div class="space-y-4">
          <!-- View Mode Switcher -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">View Mode</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="mode in viewModes"
                :key="mode.value"
                @click="selectedViewMode = mode.value"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                  selectedViewMode === mode.value
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ mode.label }}
              </button>
            </div>
          </div>

          <!-- Filters -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-gray-200">
            <!-- Username Filter -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Filter by Username</label>
              <select
                v-model="selectedUsername"
                @change="applyFilters"
                class="w-full px-3 py-2 h-[44px] border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Users</option>
                <option v-for="user in usernameOptions" :key="user.value" :value="user.value">
                  {{ user.label }}
                </option>
              </select>
            </div>

            <!-- Customer Filter -->
            <div class="customer-select-wrapper">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Filter by Customer</label>
              <div class="relative">
                <Autocomplete
                  v-model="selectedCustomerValue"
                  :options="customerOptions"
                  :loading="loadingCustomers"
                  placeholder="Search customer by name or code"
                  class="customer-autocomplete w-full text-sm"
                />
              </div>
            </div>
          </div>

          <!-- Active Filters Display -->
          <div v-if="hasActiveFilters" class="pt-2 border-t border-gray-200">
            <div class="text-xs font-medium text-gray-600 mb-2">Active Filters:</div>
            <div class="flex flex-wrap gap-2">
              <span
                v-if="selectedUsername"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                User: {{ getUsernameLabel(selectedUsername) }}
                <button @click="clearUsernameFilter" class="ml-2 hover:text-blue-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedCustomer"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                Customer: {{ selectedCustomer.customer_name || selectedCustomer.value }}
                <button @click="clearCustomerFilter" class="ml-2 hover:text-green-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Processing Result Message -->
      <section v-if="processResult && !processingUnprocessed" class="bg-white rounded-xl shadow-lg border-2 p-6 sm:p-8" :class="processResult.error ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'">
        <div class="flex items-start gap-3">
          <div v-if="processResult.error" class="flex-shrink-0">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div v-else class="flex-shrink-0">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold mb-2" :class="processResult.error ? 'text-red-800' : 'text-green-800'">
              {{ processResult.error ? 'Processing Error' : 'Processing Complete' }}
            </h4>
            <div class="text-sm space-y-1" :class="processResult.error ? 'text-red-700' : 'text-green-700'">
              <p v-if="processResult.error">{{ processResult.error }}</p>
              <template v-else>
                <p><strong>{{ processResult.processed_count }}</strong> transactions processed</p>
                <p><strong>{{ processResult.success_count }}</strong> successful, <strong>{{ processResult.failed_count }}</strong> failed</p>
                <p v-if="processResult.new_success_amount > 0" class="font-semibold">
                  Added NPR {{ formatAmount(processResult.new_success_amount) }} to today's total
                </p>
              </template>
            </div>
          </div>
          <button @click="processResult = null" class="flex-shrink-0 text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </section>

      <!-- Data Display Section -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <!-- Loading State -->
        <div v-if="loadingData" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Loading data...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="!hasData" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="mt-4 text-gray-600">No data found for today.</p>
        </div>

        <!-- Username-wise View -->
        <div v-else-if="selectedViewMode === 'username'">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Success Amount by Username</h3>
          <div class="space-y-3">
            <div
              v-for="item in usernameData"
              :key="item.username"
              :class="[
                'p-4 rounded-lg border-2 transition-all',
                item.username === session.user
                  ? 'bg-blue-50 border-blue-200 shadow-md'
                  : 'bg-gray-50 border-gray-200 hover:shadow-md'
              ]"
            >
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <span class="text-base sm:text-lg font-semibold text-gray-900">{{ item.full_name || item.username }}</span>
                    <span v-if="item.username === session.user" class="px-2 py-0.5 text-xs font-medium bg-blue-600 text-white rounded">
                      You
                    </span>
                  </div>
                  <div class="text-xs sm:text-sm text-gray-600 mt-1">{{ item.username }}</div>
                  <div class="text-xs text-gray-500 mt-1">{{ item.count }} payment{{ item.count !== 1 ? 's' : '' }}</div>
                </div>
                <div class="text-right">
                  <div class="text-xl sm:text-2xl font-bold text-blue-600">NPR {{ formatAmount(item.total_amount) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Customer-wise View -->
        <div v-else-if="selectedViewMode === 'customer'">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Success Amount by Customer</h3>
          <div class="space-y-3">
            <div
              v-for="item in customerData"
              :key="item.customer"
              class="p-4 rounded-lg bg-gray-50 border-2 border-gray-200 hover:shadow-md transition-all"
            >
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div class="flex-1">
                  <div class="text-base sm:text-lg font-semibold text-gray-900">{{ item.customer_name }}</div>
                  <div class="text-xs sm:text-sm text-gray-600 mt-1">Code: {{ item.customer }}</div>
                  <div class="text-xs text-gray-500 mt-1">{{ item.count }} payment{{ item.count !== 1 ? 's' : '' }}</div>
                </div>
                <div class="text-right">
                  <div class="text-xl sm:text-2xl font-bold text-green-600">NPR {{ formatAmount(item.total_amount) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Transaction-wise View -->
        <div v-else-if="selectedViewMode === 'transaction'">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Transaction Details</h3>
          <div class="overflow-x-auto">
            <div class="min-w-full space-y-3">
              <div
                v-for="txn in transactionData"
                :key="txn.name"
                class="p-4 rounded-lg bg-gray-50 border-2 border-gray-200 hover:shadow-md transition-all"
              >
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
                  <div>
                    <div class="text-xs text-gray-500 mb-1">Amount</div>
                    <div class="text-lg font-bold text-blue-600">NPR {{ formatAmount(txn.amount) }}</div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-500 mb-1">Customer</div>
                    <div class="text-sm font-medium text-gray-900">{{ txn.customer_name || txn.customer }}</div>
                    <div class="text-xs text-gray-600">{{ txn.customer }}</div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-500 mb-1">Created By</div>
                    <div class="text-sm font-medium text-gray-900">{{ txn.owner_full_name || txn.owner }}</div>
                    <div class="text-xs text-gray-600">{{ txn.owner }}</div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-500 mb-1">Time</div>
                    <div class="text-sm font-medium text-gray-900">{{ formatDateTime(txn.creation) }}</div>
                    <div v-if="txn.payment_entry" class="text-xs text-blue-600 mt-1">
                      <a :href="`/app/payment-entry/${txn.payment_entry}`" target="_blank" class="hover:underline">
                        View Payment
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Autocomplete, createResource, call as $call } from 'frappe-ui'
import { session } from '@/data/session'

// State
const summary = ref({
  current_user: '',
  current_user_full_name: '',
  total_success_amount: 0,
  total_success_count: 0,
  unprocessed_count: 0,
})
const bsToday = ref('')
const adToday = new Date().toISOString().slice(0, 10)
const loading = ref(false)
const loadingData = ref(false)
const loadingCustomers = ref(false)
const processingUnprocessed = ref(false)
const processResult = ref(null)

// View mode
const viewModes = [
  { value: 'username', label: 'Username-wise' },
  { value: 'customer', label: 'Customer-wise' },
  { value: 'transaction', label: 'Transaction-wise' },
]
const selectedViewMode = ref('username')

// Filters
const selectedUsername = ref('')
const selectedCustomerValue = ref(null)
const selectedCustomer = ref(null)
const usernameOptions = ref([])
const customerOptions = ref([])

// Data
const usernameData = ref([])
const customerData = ref([])
const transactionData = ref([])

// Resources
const summaryResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_pay_dashboard_summary',
  auto: false,
})

const usernameGroupedResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_username_grouped_totals',
  auto: false,
})

const customerGroupedResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_customer_grouped_totals',
  auto: false,
})

const transactionListResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_transaction_list',
  auto: false,
})

const filterCustomersResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_filter_customers_today',
  auto: false,
})

const filterUsernamesResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_filter_usernames_today',
  auto: false,
})

const unprocessedCountResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.get_today_unprocessed_count',
  auto: false,
})

const processAllResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.process_all_today_unprocessed',
  auto: false,
})

// Computed
const hasActiveFilters = computed(() => {
  return Boolean(selectedUsername.value || selectedCustomer.value)
})

const hasData = computed(() => {
  if (selectedViewMode.value === 'username') return usernameData.value.length > 0
  if (selectedViewMode.value === 'customer') return customerData.value.length > 0
  if (selectedViewMode.value === 'transaction') return transactionData.value.length > 0
  return false
})

// Methods
const formatAmount = (amount) => {
  const num = Number(amount) || 0
  return num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '—'
  const d = new Date(dateTime)
  return d.toLocaleString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

const getUsernameLabel = (username) => {
  const user = usernameOptions.value.find(u => u.value === username)
  return user ? user.label : username
}

const clearUsernameFilter = () => {
  selectedUsername.value = ''
  applyFilters()
}

const clearCustomerFilter = () => {
  selectedCustomerValue.value = null
  selectedCustomer.value = null
  applyFilters()
}

const loadSummary = async () => {
  try {
    const [summaryRes, unprocessedRes] = await Promise.all([
      summaryResource.fetch(),
      unprocessedCountResource.fetch(),
    ])
    summary.value = {
      current_user: summaryRes?.current_user || session.user,
      current_user_full_name: summaryRes?.current_user_full_name || session.user,
      total_success_amount: Number(summaryRes?.total_success_amount || 0),
      total_success_count: Number(summaryRes?.total_success_count || 0),
      unprocessed_count: Number(unprocessedRes?.unprocessed_count || 0),
    }
  } catch (error) {
    console.error('Failed to load summary', error)
  }
}

const loadUsernameData = async () => {
  loadingData.value = true
  try {
    const res = await usernameGroupedResource.fetch({
      username_filter: selectedUsername.value || undefined,
    })
    usernameData.value = res?.grouped_totals || []
  } catch (error) {
    console.error('Failed to load username data', error)
    usernameData.value = []
  } finally {
    loadingData.value = false
  }
}

const loadCustomerData = async () => {
  loadingData.value = true
  try {
    const res = await customerGroupedResource.fetch({
      customer_filter: selectedCustomer.value?.value || undefined,
      username_filter: selectedUsername.value || undefined,
    })
    customerData.value = res?.grouped_totals || []
  } catch (error) {
    console.error('Failed to load customer data', error)
    customerData.value = []
  } finally {
    loadingData.value = false
  }
}

const loadTransactionData = async () => {
  loadingData.value = true
  try {
    const res = await transactionListResource.fetch({
      username_filter: selectedUsername.value || undefined,
      customer_filter: selectedCustomer.value?.value || undefined,
      limit: 100,
    })
    transactionData.value = res?.transactions || []
  } catch (error) {
    console.error('Failed to load transaction data', error)
    transactionData.value = []
  } finally {
    loadingData.value = false
  }
}

const loadFilterOptions = async () => {
  try {
    const [customersRes, usernamesRes] = await Promise.all([
      filterCustomersResource.fetch(),
      filterUsernamesResource.fetch(),
    ])
    
    customerOptions.value = (customersRes?.customers || []).map(c => ({
      label: c.label,
      value: c.value,
      customer_name: c.customer_name,
    }))
    
    usernameOptions.value = usernamesRes?.usernames || []
  } catch (error) {
    console.error('Failed to load filter options', error)
  }
}

const applyFilters = async () => {
  if (selectedViewMode.value === 'username') {
    await loadUsernameData()
  } else if (selectedViewMode.value === 'customer') {
    await loadCustomerData()
  } else if (selectedViewMode.value === 'transaction') {
    await loadTransactionData()
  }
}

const processAllUnprocessed = async () => {
  if (processingUnprocessed.value || summary.value.unprocessed_count < 1) {
    return
  }
  
  processingUnprocessed.value = true
  processResult.value = null
  
  try {
    const res = await processAllResource.fetch()
    processResult.value = res
    
    // Show success message/notification
    if (res?.success_count > 0) {
      console.log(`Successfully processed ${res.success_count} transactions. Added NPR ${formatAmount(res.new_success_amount)}`)
    }
    
    // Refresh all data to reflect changes
    await refreshAll()
  } catch (error) {
    console.error('Failed to process unprocessed transactions', error)
    processResult.value = {
      error: error.message || 'Failed to process transactions',
    }
  } finally {
    processingUnprocessed.value = false
  }
}

const refreshAll = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadSummary(),
      loadFilterOptions(),
      applyFilters(),
    ])
  } finally {
    loading.value = false
  }
}

const tryLoadNepaliScriptAndSetBSToday = async () => {
  try {
    if (typeof window !== 'undefined' && !window.NepaliFunctions) {
      const s = document.createElement('script')
      s.src = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js'
      document.head.appendChild(s)
      await new Promise((resolve) => { s.onload = resolve; s.onerror = resolve })
    }
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const d = new Date()
      const bs = window.NepaliFunctions.AD2BS({ year: d.getFullYear(), month: d.getMonth() + 1, day: d.getDate() })
      bsToday.value = `${bs.year}-${String(bs.month).padStart(2,'0')}-${String(bs.day).padStart(2,'0')}`
    }
  } catch (e) {
    console.warn('Nepali date script failed to load', e)
  }
}

// Watch for view mode changes
watch(selectedViewMode, async () => {
  await applyFilters()
})

// Watch for username filter changes
watch(selectedUsername, async () => {
  await applyFilters()
})

// Watch for customer selection
watch(selectedCustomerValue, (newValue) => {
  if (!newValue) {
    selectedCustomer.value = null
    return
  }
  let option = null
  if (typeof newValue === 'object' && newValue !== null) {
    option = newValue
  } else {
    option = customerOptions.value.find(opt => opt.value === newValue)
  }
  if (option) {
    selectedCustomer.value = option
    applyFilters()
  }
})

onMounted(async () => {
  await Promise.all([
    loadSummary(),
    loadFilterOptions(),
    tryLoadNepaliScriptAndSetBSToday(),
  ])
  await applyFilters()
})
</script>

<style scoped>
/* Ensure mobile-friendly touch targets */
button, select {
  min-height: 44px;
}

/* Customer Selection Field UX Improvements */
.customer-select-wrapper {
  position: relative;
}

.customer-autocomplete :deep(input),
.customer-autocomplete :deep(.frappe-autocomplete-input) {
  min-height: 44px !important;
  height: 44px !important;
  padding: 12px 16px !important;
  font-size: 16px !important; /* Prevents zoom on iOS */
  border-radius: 8px;
  border: 1px solid #d1d5db;
  transition: all 0.2s;
}

.customer-autocomplete :deep(input:focus),
.customer-autocomplete :deep(.frappe-autocomplete-input:focus) {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Prevent layout shift when keyboard appears */
@media (max-width: 768px) {
  .customer-select-wrapper {
    scroll-padding-top: 100px;
  }
  
  /* Fix autocomplete dropdown positioning on mobile */
  .customer-autocomplete :deep(.autocomplete-dropdown),
  .customer-autocomplete :deep(.frappe-autocomplete-dropdown) {
    position: fixed !important;
    max-height: 50vh;
    overflow-y: auto;
    z-index: 9999;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
}

@media (max-width: 640px) {
  /* Optimize spacing for mobile */
  section {
    padding: 1rem !important;
  }
  
  /* Prevent horizontal scroll */
  body {
    overflow-x: hidden;
  }
  
  /* Better spacing for cards */
  .bg-white {
    padding: 1rem !important;
  }
}

/* Tablet optimizations */
@media (min-width: 641px) and (max-width: 1024px) {
  section {
    padding: 1.5rem;
  }
}

/* Desktop/Laptop optimizations */
@media (min-width: 1024px) {
  /* Better spacing for desktop */
  section {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  /* Improve card layouts */
  .bg-white {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }
}
</style>

