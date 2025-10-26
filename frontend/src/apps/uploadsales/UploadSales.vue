<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center space-x-4">
            <div class="flex items-center justify-center w-12 h-12 bg-indigo-600 rounded-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Upload Sales Invoices</h1>
              <p class="text-sm text-gray-600">Bulk import sales invoices from CSV • {{ session.user }}</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
      <!-- Upload Area -->
      <UploadArea 
        v-if="!csvContent && !showProgress && !showSummary"
        @file-uploaded="handleFileUpload"
      />

      <!-- File Info with Clear Button -->
      <div v-if="csvContent && !showProgress && !showSummary" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">CSV file loaded</p>
              <p class="text-sm text-gray-500">Ready to import {{ totalInvoices }} invoices</p>
            </div>
          </div>
          <button
            @click="clearFile"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            Clear File
          </button>
        </div>
      </div>

      <!-- Driver & Vehicle Selection -->
      <DriverSelect
        v-if="csvContent && !showProgress && !showSummary"
        v-model:driverValue="selectedDriver"
        v-model:vehicleValue="selectedVehicle"
        :drivers="drivers"
        :vehicles="vehicles"
        :loading-drivers="loadingDrivers"
        :loading-vehicles="loadingVehicles"
      />

      <!-- Validation Errors -->
      <div v-if="validationErrors.length > 0 && !showProgress && !showSummary" class="bg-red-50 border-l-4 border-red-400 p-6 rounded-lg">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="ml-3 flex-1">
            <h3 class="text-lg font-semibold text-red-800 mb-3">
              Validation Errors Found ({{ validationErrors.length }} invoices skipped)
            </h3>
            <div class="text-sm text-red-700 space-y-2 max-h-64 overflow-y-auto">
              <div v-for="(error, index) in validationErrors" :key="index" class="flex items-start space-x-2 py-1">
                <span class="font-mono text-red-600">•</span>
                <span>{{ error }}</span>
              </div>
            </div>
            <p class="mt-3 text-sm text-red-600 font-medium">
              These invoices will not be imported. Please fix the data and try again.
            </p>
          </div>
        </div>
      </div>

      <!-- Preview Table -->
      <PreviewTable
        v-if="previewData.length > 0 && !showProgress && !showSummary"
        :preview-data="previewData"
        :total-invoices="validInvoiceCount"
      />

      <!-- Start Import Button -->
      <div v-if="csvContent && !showProgress && !showSummary" class="flex justify-center">
        <button
          @click="startImport"
          :disabled="!selectedDriver || importing || validInvoiceCount === 0"
          class="inline-flex items-center px-8 py-4 border-2 text-lg font-bold rounded-lg shadow-lg transition-all duration-200"
          :class="selectedDriver && validInvoiceCount > 0 ? 'bg-indigo-600 hover:bg-indigo-700 text-white border-indigo-600 hover:border-indigo-700' : 'bg-gray-300 text-gray-600 border-gray-300 cursor-not-allowed'"
        >
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
          </svg>
          <span class="font-bold">
            {{ !selectedDriver ? 'Please select a driver first' : (validInvoiceCount === 0 ? 'No valid invoices to import' : `Start Import (${validInvoiceCount} invoices)`) }}
          </span>
        </button>
      </div>

      <!-- Progress Panel -->
      <ProgressPanel
        v-if="showProgress"
        :progress="progress"
      />

      <!-- Summary Card -->
      <SummaryCard
        v-if="showSummary"
        :summary="summary"
        @start-new="resetUpload"
      />
    </main>
  </div>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
import { ref, onMounted } from 'vue'
import { session } from '@/data/session'
import { call } from 'frappe-ui'
import Papa from 'papaparse'
import UploadArea from './components/UploadArea.vue'
import DriverSelect from './components/DriverSelect.vue'
import PreviewTable from './components/PreviewTable.vue'
import ProgressPanel from './components/ProgressPanel.vue'
import SummaryCard from './components/SummaryCard.vue'

// State
const csvContent = ref(null)
const selectedDriver = ref(null)
const selectedVehicle = ref(null)
const drivers = ref([])
const vehicles = ref([])
const loadingDrivers = ref(false)
const loadingVehicles = ref(false)
const previewData = ref([])
const totalInvoices = ref(0)
const validInvoiceCount = ref(0)
const validationErrors = ref([])
const importing = ref(false)
const showProgress = ref(false)
const showSummary = ref(false)
const progress = ref({
  processed: 0,
  total: 0,
  message: '',
  imported: 0,
  skipped: 0,
  errors: 0,
  amount: 0
})
const summary = ref(null)

// Load drivers and vehicles on mount
onMounted(async () => {
  await Promise.all([loadDrivers(), loadVehicles()])
})

// Load drivers
async function loadDrivers() {
  loadingDrivers.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.uploadsales.get_drivers')
    if (response.success) {
      drivers.value = response.drivers
    }
  } catch (error) {
    console.error('Error loading drivers:', error)
  } finally {
    loadingDrivers.value = false
  }
}

// ADDED BY AI: UPLOAD_SALES - Load vehicles
async function loadVehicles() {
  loadingVehicles.value = true
  try {
    const response = await call('custom_erp.custom_erp.api.uploadsales.get_vehicles')
    if (response.success) {
      vehicles.value = response.vehicles
    }
  } catch (error) {
    console.error('Error loading vehicles:', error)
  } finally {
    loadingVehicles.value = false
  }
}

// Handle file upload
async function handleFileUpload(file) {
  try {
    // Parse CSV
    const text = await file.text()
    csvContent.value = text

    // Get preview
    const response = await call('custom_erp.custom_erp.api.uploadsales.transform_and_preview', {
      csv_content: text
    })

    if (response.success) {
      previewData.value = response.preview_rows || []
      totalInvoices.value = response.total_invoices || 0
      validInvoiceCount.value = response.valid_invoice_count || 0
      validationErrors.value = response.validation_errors || []
    } else {
      alert('Error generating preview: ' + (response.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error handling file upload:', error)
    alert('Error processing file: ' + error.message)
  }
}

// ADDED BY AI: UPLOAD_SALES - Clear file and reset selection
function clearFile() {
  if (confirm('Clear current file and selections?')) {
    csvContent.value = null
    selectedDriver.value = null
    selectedVehicle.value = null
    previewData.value = []
    totalInvoices.value = 0
    validInvoiceCount.value = 0
    validationErrors.value = []
  }
}

// Start import
async function startImport() {
  if (!selectedDriver.value) {
    alert('Please select a driver')
    return
  }

  let confirmMsg = `Import ${totalInvoices.value} invoices with driver ${selectedDriver.value}`
  if (selectedVehicle.value) {
    confirmMsg += ` and vehicle ${selectedVehicle.value}`
  }
  confirmMsg += '?'

  if (!confirm(confirmMsg)) {
    return
  }

  importing.value = true
  showProgress.value = true

  try {
    console.log('=== STARTING IMPORT ===')
    console.log('Driver ID:', selectedDriver.value)
    console.log('Vehicle ID:', selectedVehicle.value)
    console.log('CSV Content Length:', csvContent.value ? csvContent.value.length : 0)
    
    // Test API first
    console.log('Testing API connection...')
    console.log('Calling API:', 'custom_erp.custom_erp.api.uploadsales.test_api_v2')
    const testResponse = await call('custom_erp.custom_erp.api.uploadsales.test_api_v2')
    console.log('Test API V2 Response:', testResponse)
    
    if (testResponse.message === 'NEW CODE IS LOADED') {
      console.log('✅ NEW CODE IS RUNNING!')
    } else {
      console.log('⚠️ OLD CODE IS STILL RUNNING!')
    }
    
    // ADDED BY AI: UPLOAD_SALES - Now includes vehicle_id
    console.log('Calling main API:', 'custom_erp.custom_erp.api.uploadsales.enqueue_import_job')
    const response = await call('custom_erp.custom_erp.api.uploadsales.enqueue_import_job', {
      driver_id: selectedDriver.value,
      vehicle_id: selectedVehicle.value || '',
      csv_content: csvContent.value
    })
    
    console.log('API Response:', response)

    if (response.success) {
      // Subscribe to progress events with import_name
      subscribeToProgress(response.import_name)
    } else {
      alert('Error starting import: ' + (response.error || 'Unknown error'))
      showProgress.value = false
    }
  } catch (error) {
    console.error('=== IMPORT ERROR ===')
    console.error('Error:', error)
    console.error('Error message:', error.message)
    console.error('Error stack:', error.stack)
    alert('Error starting import: ' + error.message)
    showProgress.value = false
  } finally {
    importing.value = false
  }
}

// Subscribe to real-time progress
let progressInterval = null

function subscribeToProgress(jobId) {
  // Try WebSocket first
  if (window.frappe && window.frappe.realtime) {
    console.log('Using WebSocket for realtime updates')
    window.frappe.realtime.on('uploadsales_progress', (data) => {
      updateProgress(data)
    })
  } else {
    console.log('WebSocket not available, using polling fallback')
  }
  
  // Always use polling as fallback/backup
  startProgressPolling(jobId)
}

// ADDED BY AI: UPLOAD_SALES - Polling fallback for progress
function startProgressPolling(jobId) {
  // Clear any existing interval
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  
  // Poll every 500ms
  progressInterval = setInterval(async () => {
    try {
      const response = await call('custom_erp.custom_erp.api.uploadsales.get_job_progress', {
        job_id: jobId
      })
      
      if (response && response.success) {
        updateProgress(response.data)
      }
    } catch (error) {
      console.error('Error polling progress:', error)
    }
  }, 500)
}

// ADDED BY AI: UPLOAD_SALES - Update progress from data
function updateProgress(data) {
  if (!data) return
  
  progress.value = {
    processed: data.processed || 0,
    total: data.total || 0,
    message: data.current_message || '',
    imported: data.imported_count || 0,
    skipped: data.skipped_count || 0,
    errors: data.error_count || 0,
    amount: data.total_amount || 0
  }

  // Check if completed
  if (data.completed) {
    // Stop polling
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
    
    // Unsubscribe from WebSocket if available
    if (window.frappe && window.frappe.realtime) {
      window.frappe.realtime.off('uploadsales_progress')
    }
    
    showProgress.value = false
    showSummary.value = true
    summary.value = {
      total: data.total || 0,
      imported: data.imported_count || 0,
      skipped: data.skipped_count || 0,
      errors: data.error_count || 0,
      amount: data.total_amount || 0,
      errorCsvPath: data.error_csv_path || null,
      importLogUrl: data.import_log_url || null
    }
  }
}

// Reset upload - ADDED BY AI: UPLOAD_SALES - Now includes vehicle reset and validation errors
function resetUpload() {
  // Stop polling if active
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  
  csvContent.value = null
  selectedDriver.value = null
  selectedVehicle.value = null
  previewData.value = []
  totalInvoices.value = 0
  validInvoiceCount.value = 0
  validationErrors.value = []
  importing.value = false
  showProgress.value = false
  showSummary.value = false
  progress.value = {
    processed: 0,
    total: 0,
    message: '',
    imported: 0,
    skipped: 0,
    errors: 0,
    amount: 0
  }
  summary.value = null
}
</script>

