<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Upload Reco Main Component -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center space-x-4">
            <div class="flex items-center justify-center w-12 h-12 bg-purple-600 rounded-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Payment Reconciliation Upload</h1>
              <p class="text-sm text-gray-600">Upload daily payment register • {{ session.user }}</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <!-- CSV Upload Section -->
      <CsvUploadSection
        v-if="!csvParsed"
        :loading="uploading"
        @file-selected="handleFileUpload"
      />

      <!-- File Info with Clear Button -->
      <div v-if="csvParsed" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-10 h-10 bg-purple-100 rounded-lg">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">CSV file loaded successfully</p>
              <p class="text-sm text-gray-500">{{ parsedData.parsed_rows?.length || 0 }} rows • {{ Object.keys(parsedData.grouped_by_loadsheet || {}).length }} load sheets</p>
            </div>
          </div>
          <button
            @click="clearFile"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            Clear File
          </button>
        </div>
      </div>

      <!-- Unmatched Customers Alert -->
      <UnmatchedList
        v-if="csvParsed"
        :unmatched-customers="parsedData.unmatched_customers || []"
      />

      <!-- Data Preview Table -->
      <DataPreview
        v-if="csvParsed"
        :parsed-rows="parsedData.parsed_rows || []"
        :grouped-by-loadsheet="parsedData.grouped_by_loadsheet || {}"
      />

      <!-- Driver Assignment Section -->
      <div v-if="csvParsed" class="bg-white rounded-xl shadow-lg border-2 border-blue-500 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-900">
            📋 Step 2: Assign Drivers to Load Sheets
          </h3>
          <span v-if="loadingDrivers" class="text-sm text-blue-600">Loading drivers...</span>
          <span v-else-if="drivers.length === 0" class="text-sm text-red-600">⚠️ No drivers found</span>
          <span v-else class="text-sm text-green-600">✅ {{ drivers.length }} drivers loaded</span>
        </div>

        <!-- Loading State -->
        <div v-if="loadingDrivers" class="flex justify-center py-8">
          <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>

        <!-- No Drivers Warning -->
        <div v-else-if="drivers.length === 0" class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-red-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <div>
              <h4 class="text-sm font-medium text-red-800">No Drivers Found</h4>
              <p class="mt-1 text-sm text-red-700">
                No drivers exist in the system. Please create drivers in Frappe Desk first:
              </p>
              <p class="mt-2 text-sm text-red-700 font-mono">
                Desk → Driver → New Driver
              </p>
            </div>
          </div>
        </div>

        <!-- Driver Assignment Component -->
        <DriverAssignment
          v-else
          :loadsheets="loadsheetList"
          :drivers="drivers"
          :grouped-data="parsedData.grouped_by_loadsheet || {}"
          @update:assignments="driverAssignments = $event"
          @validation-changed="assignmentsValid = $event"
        />
      </div>

      <!-- Create Button -->
      <div v-if="csvParsed" class="space-y-4">
        <!-- Debug Info -->
        <div v-if="!canCreate" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-yellow-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            <div class="flex-1">
              <h3 class="text-sm font-medium text-yellow-800">Cannot Create Records Yet</h3>
              <div class="mt-2 text-sm text-yellow-700 space-y-1">
                <p v-if="!csvParsed">❌ CSV not uploaded</p>
                <p v-if="csvParsed && !assignmentsValid">❌ Not all load sheets have drivers assigned</p>
                <p v-if="csvParsed && parsedData.unmatched_customers?.length > 0">❌ {{ parsedData.unmatched_customers.length }} unmatched customers found</p>
                <p class="font-medium mt-2">Please complete the requirements above to enable the button.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Create Button -->
        <div class="flex justify-center">
          <button
            @click="showConfirmDialog = true"
            :disabled="!canCreate"
            class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Create Payment Reconciliation Records
          </button>
        </div>
      </div>
    </main>

    <!-- Confirmation Dialog -->
    <div v-if="showConfirmDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showConfirmDialog = false"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-purple-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Confirm Creation
                </h3>
                <div class="mt-4">
                  <p class="text-sm text-gray-500 mb-4">
                    You are about to create payment reconciliation records for the following drivers:
                  </p>
                  <div class="bg-gray-50 rounded-lg p-4 space-y-2 max-h-64 overflow-y-auto">
                    <div v-for="(loadsheets, driver) in groupedAssignments" :key="driver" class="text-sm">
                      <span class="font-medium text-gray-900">{{ driver }}</span>
                      <span class="text-gray-600"> → {{ loadsheets.join(', ') }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="createRecords"
              :disabled="creating"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              <svg v-if="creating" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ creating ? 'Creating...' : 'Confirm & Create' }}
            </button>
            <button
              type="button"
              @click="showConfirmDialog = false"
              :disabled="creating"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Dialog -->
    <div v-if="showSuccessDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-green-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Success!
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ successMessage }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="closeSuccessDialog"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { session } from '../../shared/data/session'
import { call } from 'frappe-ui'
import CsvUploadSection from './components/CsvUploadSection.vue'
import DataPreview from './components/DataPreview.vue'
import DriverAssignment from './components/DriverAssignment.vue'
import UnmatchedList from './components/UnmatchedList.vue'

// State
const uploading = ref(false)
const csvParsed = ref(false)
const parsedData = ref({})
const drivers = ref([])
const loadingDrivers = ref(false)
const driverAssignments = ref({})
const assignmentsValid = ref(false)
const showConfirmDialog = ref(false)
const creating = ref(false)
const showSuccessDialog = ref(false)
const successMessage = ref('')

// Computed
const loadsheetList = computed(() => {
  return Object.keys(parsedData.value.grouped_by_loadsheet || {})
})

const canCreate = computed(() => {
  return csvParsed.value && 
         assignmentsValid.value && 
         (parsedData.value.unmatched_customers?.length === 0)
})

const groupedAssignments = computed(() => {
  const grouped = {}
  for (const [loadsheet, driver] of Object.entries(driverAssignments.value)) {
    if (driver) {
      if (!grouped[driver]) {
        grouped[driver] = []
      }
      grouped[driver].push(loadsheet)
    }
  }
  return grouped
})

// Methods
const handleFileUpload = async (csvContent) => {
  uploading.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.payment_reco.parse_and_validate_csv', {
      csv_content: csvContent
    })

    if (response.success) {
      parsedData.value = response.data
      csvParsed.value = true
      
      // Load drivers
      await loadDrivers()
    } else {
      alert('Error parsing CSV: ' + response.message)
    }
  } catch (error) {
    console.error('Error uploading CSV:', error)
    alert('Error uploading CSV: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const loadDrivers = async () => {
  loadingDrivers.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.payment_reco.get_drivers_list')
    if (response.success) {
      drivers.value = response.data
    } else {
      console.error('Error loading drivers:', response.message)
      alert('Error loading drivers: ' + response.message)
    }
  } catch (error) {
    console.error('Error loading drivers:', error)
    alert('Error loading drivers. Please check if you have drivers in the system.')
  } finally {
    loadingDrivers.value = false
  }
}

const clearFile = () => {
  csvParsed.value = false
  parsedData.value = {}
  driverAssignments.value = {}
  assignmentsValid.value = false
}

const createRecords = async () => {
  creating.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.payment_reco.create_payment_recos', {
      driver_assignments: JSON.stringify(groupedAssignments.value),
      csv_data: JSON.stringify(parsedData.value.grouped_by_loadsheet)
    })

    if (response.success) {
      successMessage.value = response.message
      showConfirmDialog.value = false
      showSuccessDialog.value = true
    } else {
      alert('Error creating records: ' + response.message)
    }
  } catch (error) {
    console.error('Error creating records:', error)
    alert('Error creating records: ' + error.message)
  } finally {
    creating.value = false
  }
}

const closeSuccessDialog = () => {
  showSuccessDialog.value = false
  clearFile()
}
</script>

