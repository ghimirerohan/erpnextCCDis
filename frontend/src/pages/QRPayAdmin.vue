<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">QRPay Admin</h1>
            <p class="text-sm text-gray-600">Manage unprocessed Fonepay transactions</p>
          </div>
          <Button @click="session.logout.submit()" theme="gray" variant="outline">Logout</Button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-8">
      <!-- Action Buttons -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div class="flex flex-wrap gap-4">
          <Button 
            @click="processSelected" 
            :loading="processing"
            :disabled="selectedTransactions.length === 0"
            theme="blue"
          >
            Process Selected ({{ selectedTransactions.length }})
          </Button>
          <Button 
            @click="processAll" 
            :loading="processing"
            theme="green"
          >
            Process All ({{ unprocessedCount }})
          </Button>
          <Button 
            @click="exportSelected" 
            :disabled="selectedTransactions.length === 0"
            theme="gray" 
            variant="outline"
          >
            Export Selected CSV
          </Button>
          <Button 
            @click="refreshData" 
            :loading="loading"
            theme="gray" 
            variant="outline"
          >
            Refresh
          </Button>
        </div>
      </div>

      <!-- Transactions Table -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Unprocessed Transactions</h2>
          <p class="text-sm text-gray-600 mt-1">{{ transactions.length }} transactions found</p>
        </div>
        
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-2 text-gray-600">Loading transactions...</p>
        </div>
        
        <div v-else-if="transactions.length === 0" class="p-8 text-center">
          <div class="text-gray-400 text-6xl mb-4">📄</div>
          <p class="text-gray-600">No unprocessed transactions found</p>
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left">
                  <input 
                    type="checkbox" 
                    :checked="allSelected"
                    @change="toggleAll"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  PRN
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Invoice
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Retries
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timeout
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="transaction in transactions" 
                :key="transaction.name"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <input 
                    type="checkbox" 
                    :value="transaction.name"
                    v-model="selectedTransactions"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
                  {{ transaction.prn || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.creation) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.customer || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.sales_invoice || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ₹{{ formatAmount(transaction.amount) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="getStatusClass(transaction.status)">
                    {{ transaction.status || 'N/A' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.retries || 0 }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.timeout_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Processing Results Modal -->
      <div v-if="showResults" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Processing Results</h3>
          </div>
          
          <div class="px-6 py-4">
            <div class="mb-4">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700">Total Processed:</span>
                <span class="text-sm text-gray-900">{{ processingResults.count }}</span>
              </div>
            </div>
            
            <div class="space-y-2 max-h-60 overflow-y-auto">
              <div v-for="result in processingResults.results" :key="result.tx" 
                   class="flex items-center justify-between p-2 rounded"
                   :class="getResultClass(result.status)">
                <span class="text-sm font-medium">{{ result.tx }}</span>
                <span class="text-sm">{{ result.status }}</span>
              </div>
            </div>
          </div>
          
          <div class="px-6 py-4 border-t border-gray-200 flex justify-end">
            <Button @click="showResults = false" theme="gray" variant="outline">
              Close
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { session } from '@/data/session'

// State
const transactions = ref([])
const selectedTransactions = ref([])
const loading = ref(false)
const processing = ref(false)
const showResults = ref(false)
const processingResults = ref({ count: 0, results: [] })

// Resources
const transactionResource = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Fonepay QR Transaction',
    fields: ['name', 'prn', 'creation', 'customer', 'sales_invoice', 'amount', 'status', 'retries', 'timeout_at'],
    filters: { processed: 0 },
    order_by: 'creation asc',
    limit: 500
  },
  auto: false
})

// Computed
const allSelected = computed(() => {
  return transactions.value.length > 0 && selectedTransactions.value.length === transactions.value.length
})

const unprocessedCount = computed(() => {
  return transactions.value.length
})

// Methods
const loadTransactions = async () => {
  loading.value = true
  try {
    const res = await transactionResource.fetch()
    transactions.value = res || []
  } catch (error) {
    console.error('Error loading transactions:', error)
    alert('Failed to load transactions: ' + error.message)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadTransactions()
}

const toggleAll = () => {
  if (allSelected.value) {
    selectedTransactions.value = []
  } else {
    selectedTransactions.value = transactions.value.map(t => t.name)
  }
}

const processSelected = async () => {
  if (selectedTransactions.value.length === 0) return
  
  processing.value = true
  try {
    const res = await frappe.call({
      method: 'custom_erp.custom_erp.api.fonepay.process_unprocessed_qrs',
      args: { 
        tx_names: selectedTransactions.value.join(','), 
        limit: selectedTransactions.value.length 
      }
    })
    
    if (res.message) {
      processingResults.value = res.message
      showResults.value = true
      selectedTransactions.value = []
      await loadTransactions()
    }
  } catch (error) {
    console.error('Error processing transactions:', error)
    alert('Failed to process transactions: ' + error.message)
  } finally {
    processing.value = false
  }
}

const processAll = async () => {
  processing.value = true
  try {
    const res = await frappe.call({
      method: 'custom_erp.custom_erp.api.fonepay.process_unprocessed_qrs',
      args: { limit: 500 }
    })
    
    if (res.message) {
      processingResults.value = res.message
      showResults.value = true
      selectedTransactions.value = []
      await loadTransactions()
    }
  } catch (error) {
    console.error('Error processing all transactions:', error)
    alert('Failed to process all transactions: ' + error.message)
  } finally {
    processing.value = false
  }
}

const exportSelected = () => {
  if (selectedTransactions.value.length === 0) return
  
  const selectedData = transactions.value.filter(t => selectedTransactions.value.includes(t.name))
  const csvData = [
    ['Name', 'PRN', 'Created', 'Customer', 'Invoice', 'Amount', 'Status', 'Retries', 'Timeout'],
    ...selectedData.map(t => [
      t.name,
      t.prn || '',
      t.creation || '',
      t.customer || '',
      t.sales_invoice || '',
      t.amount || '',
      t.status || '',
      t.retries || 0,
      t.timeout_at || ''
    ])
  ]
  
  const csv = csvData.map(row => 
    row.map(cell => `"${(cell || '').toString().replace(/"/g, '""')}"`).join(',')
  ).join('\n')
  
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'qrpay_transactions.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const getStatusClass = (status) => {
  const classes = {
    'CREATED': 'bg-blue-100 text-blue-800',
    'VERIFIED': 'bg-yellow-100 text-yellow-800',
    'SCANNED': 'bg-purple-100 text-purple-800',
    'PENDING': 'bg-orange-100 text-orange-800',
    'SUCCESS': 'bg-green-100 text-green-800',
    'FAILED': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getResultClass = (status) => {
  if (status === 'SUCCESS') return 'bg-green-50 text-green-800'
  if (status === 'FAILED') return 'bg-red-50 text-red-800'
  if (status === 'ERROR') return 'bg-red-50 text-red-800'
  return 'bg-gray-50 text-gray-800'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

const formatAmount = (amount) => {
  if (!amount && amount !== 0) return '0.00'
  return Number(amount).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// Lifecycle
onMounted(() => {
  loadTransactions()
})
</script>

<style scoped>
/* Custom styles for QRPay Admin */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* Responsive table */
@media (max-width: 768px) {
  .overflow-x-auto {
    font-size: 0.875rem;
  }
}
</style>
