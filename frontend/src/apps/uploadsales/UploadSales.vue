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

      <!-- Driver Selection -->
      <DriverSelect
        v-if="csvContent && !showProgress && !showSummary"
        v-model="selectedDriver"
        :drivers="drivers"
        :loading="loadingDrivers"
      />

      <!-- Preview Table -->
      <PreviewTable
        v-if="previewData.length > 0 && !showProgress && !showSummary"
        :preview-data="previewData"
        :total-invoices="totalInvoices"
      />

      <!-- Start Import Button -->
      <div v-if="csvContent && !showProgress && !showSummary" class="flex justify-center">
        <button
          @click="startImport"
          :disabled="!selectedDriver || importing"
          class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg shadow-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
          </svg>
          {{ selectedDriver ? 'Start Import' : 'Please select a driver first' }}
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
const drivers = ref([])
const loadingDrivers = ref(false)
const previewData = ref([])
const totalInvoices = ref(0)
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

// Load drivers on mount
onMounted(async () => {
  await loadDrivers()
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
    } else {
      alert('Error generating preview: ' + (response.error || 'Unknown error'))
    }
  } catch (error) {
    console.error('Error handling file upload:', error)
    alert('Error processing file: ' + error.message)
  }
}

// Start import
async function startImport() {
  if (!selectedDriver.value) {
    alert('Please select a driver')
    return
  }

  if (!confirm(`Import ${totalInvoices.value} invoices with driver ${selectedDriver.value}?`)) {
    return
  }

  importing.value = true
  showProgress.value = true

  try {
    const response = await call('custom_erp.custom_erp.api.uploadsales.enqueue_import_job', {
      driver_id: selectedDriver.value,
      csv_content: csvContent.value
    })

    if (response.success) {
      // Subscribe to progress events
      subscribeToProgress()
    } else {
      alert('Error starting import: ' + (response.error || 'Unknown error'))
      showProgress.value = false
    }
  } catch (error) {
    console.error('Error starting import:', error)
    alert('Error starting import: ' + error.message)
    showProgress.value = false
  } finally {
    importing.value = false
  }
}

// Subscribe to real-time progress
function subscribeToProgress() {
  if (!window.frappe || !window.frappe.realtime) {
    console.error('Frappe realtime not available')
    return
  }

  window.frappe.realtime.on('uploadsales_progress', (data) => {
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
      showProgress.value = false
      showSummary.value = true
      summary.value = {
        total: data.total || 0,
        imported: data.imported_count || 0,
        skipped: data.skipped_count || 0,
        errors: data.error_count || 0,
        amount: data.total_amount || 0,
        errorCsvPath: data.error_csv_path || null
      }

      // Unsubscribe
      window.frappe.realtime.off('uploadsales_progress')
    }
  })
}

// Reset upload
function resetUpload() {
  csvContent.value = null
  selectedDriver.value = null
  previewData.value = []
  totalInvoices.value = 0
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

