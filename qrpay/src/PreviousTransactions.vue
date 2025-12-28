filter not w<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between py-4">
          <div class="flex items-center">
            <button 
              @click="$router.push('/')" 
              class="mr-3 p-2 rounded-full hover:bg-gray-100 text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
            </button>
            <h1 class="text-lg font-bold text-gray-900">Previous Transactions</h1>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Filters -->
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <div class="bg-white rounded-lg shadow p-1 flex w-full sm:w-auto">
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            @click="activeFilter = filter.value"
            class="flex-1 py-2 px-4 text-sm font-medium rounded-md transition-colors whitespace-nowrap"
            :class="activeFilter === filter.value ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
          >
            {{ filter.label }}
          </button>
        </div>

        <div class="w-full sm:w-auto">
          <select 
            v-model="activeStatus" 
            class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md shadow-sm"
          >
            <option value="All">All Status</option>
            <option value="SUCCESS">Success</option>
            <option value="FAILED">Failed</option>
            <option value="PENDING">Pending</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-12">
        <svg class="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Empty State -->
      <div v-else-if="!transactions.length" class="text-center py-12">
        <div class="mx-auto h-12 w-12 text-gray-400 mb-3">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900">No transactions found</h3>
        <p class="text-gray-500 mt-1">No transactions found for the selected period.</p>
      </div>

      <!-- Transactions List -->
      <div v-else class="space-y-6">
        <div v-for="(group, date) in groupedTransactions" :key="date">
          <h3 v-if="activeFilter !== 'today'" class="text-sm font-medium text-gray-500 mb-3 sticky top-20 bg-gray-50 py-1 z-10">
            {{ formatDateHeader(date) }}
          </h3>
          
          <div class="bg-white shadow overflow-hidden rounded-md">
            <ul class="divide-y divide-gray-200">
              <li v-for="tx in group" :key="tx.name">
                <div class="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors">
                  <div class="flex items-center justify-between">
                    <div class="flex flex-col">
                      <p class="text-sm font-medium text-blue-600 truncate">
                        {{ tx.customer || 'Unknown Customer' }}
                      </p>
                      <p class="text-xs text-gray-500 mt-1">
                        {{ tx.time }} • <span class="font-mono">{{ tx.customer_id || tx.name }}</span>
                      </p>
                    </div>
                    <div class="flex flex-col items-end">
                      <p class="text-sm font-bold text-gray-900">
                        Rs. {{ formatAmount(tx.amount) }}
                      </p>
                      <span 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full mt-1"
                        :class="getStatusClass(tx.status)"
                      >
                        {{ tx.status }}
                      </span>
                    </div>
                  </div>
                  <div v-if="tx.payment_entry" class="mt-2 text-xs text-gray-500 text-right">
                    PE: {{ tx.payment_entry }}
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

const props = defineProps({
  // No props needed as we fetch data internally
})

const filters = [
  { label: 'Today', value: 'today' },
  { label: 'This Week', value: 'week' },
  { label: 'This Month', value: 'month' },
]

const activeFilter = ref('today')
const activeStatus = ref('All')
const transactions = ref([])
const loading = ref(false)

const transactionsResource = createResource({
  url: 'custom_erp.api.fonepay.get_previous_transactions',
  auto: false,
})

const fetchTransactions = async () => {
  loading.value = true
  try {
    const response = await transactionsResource.fetch({
      filter_type: activeFilter.value,
      status_filter: activeStatus.value
    })
    if (response.success) {
      transactions.value = response.transactions
    }
  } catch (error) {
    console.error('Error fetching transactions:', error)
  } finally {
    loading.value = false
  }
}

// Watch for filter changes
watch([activeFilter, activeStatus], () => {
  fetchTransactions()
})

// Initial fetch
onMounted(() => {
  fetchTransactions()
})

// Group transactions by date
const groupedTransactions = computed(() => {
  if (activeFilter.value === 'today') {
    // For today, just one group (or no grouping needed visually, but structure consistent)
    return { 'Today': transactions.value }
  }
  
  const groups = {}
  transactions.value.forEach(tx => {
    const date = tx.date
    if (!groups[date]) {
      groups[date] = []
    }
    groups[date].push(tx)
  })
  return groups
})

// Helpers
const formatAmount = (amount) => {
  return Number(amount).toLocaleString('en-NP', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDateHeader = (dateStr) => {
  if (dateStr === 'Today') return 'Today'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}

const getStatusClass = (status) => {
  switch (status) {
    case 'SUCCESS':
      return 'bg-green-100 text-green-800'
    case 'FAILED':
      return 'bg-red-100 text-red-800'
    case 'PENDING':
      return 'bg-yellow-100 text-yellow-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>
