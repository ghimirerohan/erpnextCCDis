<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Customer List View -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50">
    <!-- Header - Mobile Optimized -->
    <header class="bg-white shadow-md border-b-2 border-gray-300 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-3 sm:py-4">
          <div class="flex items-center space-x-2 sm:space-x-4 flex-1 min-w-0">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-sky-600 rounded-lg shadow-md flex-shrink-0">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <div class="min-w-0 flex-1">
              <h1 class="text-base sm:text-xl lg:text-2xl font-bold text-gray-900 truncate">Daily Payment Entry</h1>
              <p class="text-xs sm:text-sm text-gray-700 font-medium truncate">Collect payments • {{ session.user }}</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border-2 border-gray-300 rounded-md shadow-sm text-xs sm:text-sm font-semibold text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition-all duration-200 ml-2 flex-shrink-0"
          >
            <svg class="w-4 h-4 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <svg class="animate-spin h-12 w-12 text-sky-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Admin: Driver Selection -->
      <div v-else-if="!recoData && isAdmin && availableDrivers.length > 0" class="text-center py-12">
        <div class="max-w-md mx-auto">
          <svg class="mx-auto h-24 w-24 text-blue-500 drop-shadow" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          <h3 class="mt-4 text-2xl font-bold text-gray-900">Administrator View</h3>
          <p class="mt-2 text-gray-700 font-medium mb-6">Select a driver to view their payment reconciliation</p>
          
          <div class="bg-white rounded-xl shadow-lg border-2 border-blue-500 p-6">
            <label class="block text-sm font-semibold text-gray-900 mb-3 text-left">Select Driver</label>
            <select
              v-model="selectedDriver"
              @change="loadDriverData"
              class="block w-full px-4 py-3 text-base border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 rounded-lg bg-white text-gray-900 font-medium shadow-sm transition-all duration-200"
            >
              <option :value="null" class="text-gray-500">-- Choose a driver --</option>
              <option v-for="driver in availableDrivers" :key="driver.driver" :value="driver.driver_name" class="text-gray-900 font-medium">
                {{ driver.driver_name }} ({{ driver.count }} customers)
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else-if="!recoData && !isAdmin" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-4 text-xl font-medium text-gray-900">No Active Reconciliation</h3>
        <p class="mt-2 text-gray-600">No payment reconciliation found for your account.</p>
      </div>
      
      <!-- No Drivers Available (Admin) -->
      <div v-else-if="!recoData && isAdmin && availableDrivers.length === 0" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-4 text-xl font-medium text-gray-900">No Active Reconciliations</h3>
        <p class="mt-2 text-gray-600">No drivers have active payment reconciliations.</p>
      </div>

      <!-- Main Content -->
      <template v-else>
        <!-- Admin: Driver Switcher -->
        <div v-if="isAdmin && availableDrivers.length > 1" class="bg-blue-50 rounded-xl border-2 border-blue-300 p-4 shadow-md">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <label class="text-sm font-semibold text-gray-900 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              Switch Driver:
            </label>
            <select
              v-model="selectedDriver"
              @change="loadDriverData"
              class="px-4 py-2.5 border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 rounded-lg bg-white text-gray-900 font-medium shadow-sm transition-all duration-200 min-w-[250px]"
            >
              <option v-for="driver in availableDrivers" :key="driver.driver" :value="driver.driver_name" class="text-gray-900 font-medium">
                {{ driver.driver_name }} ({{ driver.count }} customers)
              </option>
            </select>
          </div>
        </div>

        <!-- Summary Card -->
        <SummaryCard
          :driver-name="driverName"
          :summary="recoData.summary"
          @view-all="showAllDialog = true"
        />

        <!-- Search & Filters -->
        <div class="bg-white rounded-xl shadow-lg border-2 border-gray-300 p-4 sm:p-6">
          <div class="flex flex-col gap-4">
            <!-- Search Input -->
            <div class="relative">
              <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by customer name or code..."
                class="block w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-base transition-all duration-200 bg-white text-gray-900 placeholder-gray-500"
              />
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <!-- Filter Buttons -->
            <div class="flex gap-2 flex-wrap">
              <button
                @click="setFilter(null)"
                :class="[
                  'px-4 py-2 rounded-lg font-semibold transition-all duration-200',
                  filterSettled === null 
                    ? 'bg-blue-600 text-white shadow-lg hover:bg-blue-700 border-2 border-blue-700' 
                    : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                ]"
              >
                All ({{ allCount }})
              </button>
              <button
                @click="setFilter(false)"
                :class="[
                  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  filterSettled === false 
                    ? 'bg-amber-600 text-white shadow-md hover:bg-amber-700' 
                    : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                ]"
              >
                Pending ({{ pendingCount }})
              </button>
              <button
                @click="setFilter(true)"
                :class="[
                  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  filterSettled === true 
                    ? 'bg-green-600 text-white shadow-md hover:bg-green-700' 
                    : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                ]"
              >
                Settled ({{ settledCount }})
              </button>
            </div>
          </div>
        </div>

        <!-- Customer List -->
        <div class="bg-white rounded-xl shadow-lg border-2 border-gray-300 overflow-hidden">
          <div v-if="filteredLines.length === 0" class="p-8 text-center">
            <svg class="mx-auto h-16 w-16 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <p class="text-gray-600 font-medium">No customers found matching your search.</p>
            <p class="text-sm text-gray-500 mt-1">Try adjusting your search or filter criteria.</p>
          </div>
          
          <div v-else class="divide-y divide-gray-200">
            <div
              v-for="line in filteredLines"
              :key="line.name"
              @click="openCustomerPayment(line)"
              class="p-3 sm:p-4 hover:bg-blue-50 cursor-pointer transition-colors active:bg-blue-100"
            >
              <!-- Mobile Layout (stacked) -->
              <div class="flex flex-col gap-2 md:hidden">
                <div class="flex items-start justify-between gap-2">
                  <div class="flex-1 min-w-0">
                    <h4 class="text-sm font-bold text-gray-900 leading-tight break-words">{{ line.customer_name }}</h4>
                    <p class="text-xs text-gray-600 font-mono mt-0.5">{{ line.customer }}</p>
                  </div>
                  <span
                    v-if="line.settled === 1 || line.settled === true"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-800 border border-green-300 flex-shrink-0"
                  >
                    <svg class="w-3 h-3 mr-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    Settled
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300 flex-shrink-0"
                  >
                    <svg class="w-3 h-3 mr-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                    </svg>
                    Pending
                  </span>
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-base font-bold text-gray-900">{{ formatCurrency(line.net_total_amount) }}</p>
                    <p class="text-xs text-gray-600">Remaining: {{ formatCurrency(line.remaining_amount) }}</p>
                  </div>
                  <svg class="w-5 h-5 text-gray-500 flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </div>
              </div>
              
              <!-- Desktop/Tablet Layout (horizontal) -->
              <div class="hidden md:flex items-start justify-between gap-3">
                <div class="flex-grow min-w-0">
                  <h4 class="text-base lg:text-lg font-semibold text-gray-900 break-words">{{ line.customer_name }}</h4>
                  <p class="text-xs sm:text-sm text-gray-600 font-mono mt-0.5">{{ line.customer }}</p>
                </div>
                <div class="text-right flex-shrink-0">
                  <p class="text-base lg:text-lg font-bold text-gray-900 whitespace-nowrap">{{ formatCurrency(line.net_total_amount) }}</p>
                  <p class="text-xs sm:text-sm text-gray-600 whitespace-nowrap">Remaining: {{ formatCurrency(line.remaining_amount) }}</p>
                </div>
                <div class="flex items-center gap-2 flex-shrink-0">
                  <span
                    v-if="line.settled === 1 || line.settled === true"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800 border border-green-300"
                  >
                    <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    Settled
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300"
                  >
                    <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                    </svg>
                    Pending
                  </span>
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </main>

    <!-- View All Dialog -->
    <div v-if="showAllDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showAllDialog = false"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">All Amount Details</h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Initial Total Amount:</span>
                <span class="font-semibold">{{ formatCurrency(recoData?.summary.initial_total_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Net Total Amount:</span>
                <span class="font-semibold">{{ formatCurrency(recoData?.summary.net_total_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Cash Amount:</span>
                <span class="font-semibold text-green-600">{{ formatCurrency(recoData?.summary.cash_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">QR Amount:</span>
                <span class="font-semibold text-blue-600">{{ formatCurrency(recoData?.summary.qr_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Cheque Amount:</span>
                <span class="font-semibold text-purple-600">{{ formatCurrency(recoData?.summary.cheque_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Return Amount:</span>
                <span class="font-semibold text-orange-600">{{ formatCurrency(recoData?.summary.return_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Credit Amount:</span>
                <span class="font-semibold text-red-600">{{ formatCurrency(recoData?.summary.credit_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Expense Amount:</span>
                <span class="font-semibold text-gray-600">{{ formatCurrency(recoData?.summary.expense_amount) }}</span>
              </div>
              <div class="flex justify-between py-3 border-t-2 border-gray-300 mt-2">
                <span class="text-gray-900 font-bold">Remaining Amount:</span>
                <span class="font-bold text-xl text-sky-600">{{ formatCurrency(recoData?.summary.remaining_amount) }}</span>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="showAllDialog = false"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-sky-600 text-base font-medium text-white hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '../../shared/data/session'
import { call } from 'frappe-ui'
import SummaryCard from './components/SummaryCard.vue'

const router = useRouter()

const loading = ref(true)
const recoData = ref(null)
const driverName = ref('')
const searchQuery = ref('')
const filterSettled = ref(null)
const showAllDialog = ref(false)
const isAdmin = ref(false)
const availableDrivers = ref([])
const selectedDriver = ref(null)

const filteredLines = computed(() => {
  if (!recoData.value?.lines) return []
  
  let lines = recoData.value.lines
  
  // Filter by settled status
  // Note: Backend returns 0/1, convert to boolean for comparison
  if (filterSettled.value !== null) {
    lines = lines.filter(line => !!line.settled === filterSettled.value)
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    lines = lines.filter(line => 
      line.customer_name.toLowerCase().includes(query) ||
      line.customer.toLowerCase().includes(query)
    )
  }
  
  return lines
})

const allCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.length
})

const pendingCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.filter(line => !line.settled || line.settled === 0).length
})

const settledCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.filter(line => line.settled === 1 || line.settled === true).length
})

const setFilter = (value) => {
  filterSettled.value = value
}

const loadData = async () => {
  loading.value = true
  try {
    // First, try to get driver data for current user
    const response = await call('custom_erp.custom_erp.api.payment_reco.get_driver_reco_data')
    
    isAdmin.value = response.is_admin || false
    
    if (response.success) {
      recoData.value = response.data
      driverName.value = response.data.reco.driver_name || session.user
      selectedDriver.value = driverName.value
    } else if (isAdmin.value) {
      // Admin user but no personal driver data - load all drivers
      await loadAllDrivers()
    }
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

const loadAllDrivers = async () => {
  try {
    const response = await call('custom_erp.custom_erp.api.payment_reco.get_all_active_recos')
    if (response.success) {
      availableDrivers.value = response.data
    }
  } catch (error) {
    console.error('Error loading drivers:', error)
  }
}

const loadDriverData = async () => {
  if (!selectedDriver.value) return
  
  loading.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.payment_reco.get_driver_reco_data', {
      driver_name: selectedDriver.value
    })
    
    if (response.success) {
      recoData.value = response.data
      driverName.value = response.data.reco.driver_name
      
      // Load all drivers list for admin if not already loaded
      if (isAdmin.value && availableDrivers.value.length === 0) {
        await loadAllDrivers()
      }
    } else {
      alert('Error: ' + response.message)
    }
  } catch (error) {
    console.error('Error loading driver data:', error)
    alert('Error loading driver data')
  } finally {
    loading.value = false
  }
}

const openCustomerPayment = (line) => {
  router.push({
    name: 'CustomerPayment',
    params: { lineName: line.name },
    query: { driver: driverName.value }
  })
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}

onMounted(() => {
  loadData()
})
</script>

