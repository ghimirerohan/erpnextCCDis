<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex items-center mb-6">
      <div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3">
        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900">Import Complete</h2>
    </div>

    <!-- Summary Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <div class="text-3xl font-bold text-gray-900">{{ summary.total }}</div>
        <div class="text-sm text-gray-600 mt-1">Total Invoices</div>
      </div>
      <div class="bg-green-50 border border-green-200 rounded-lg p-6">
        <div class="text-3xl font-bold text-green-600">{{ summary.imported }}</div>
        <div class="text-sm text-green-700 mt-1">Successfully Imported</div>
      </div>
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <div class="text-3xl font-bold text-yellow-600">{{ summary.skipped }}</div>
        <div class="text-sm text-yellow-700 mt-1">Skipped (Already Exist)</div>
      </div>
      <div class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="text-3xl font-bold text-red-600">{{ summary.errors }}</div>
        <div class="text-sm text-red-700 mt-1">Errors</div>
      </div>
    </div>

    <!-- Total Amount -->
    <div class="bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 rounded-lg p-6 mb-6">
      <div class="flex items-center justify-between">
        <div>
          <div class="text-sm text-indigo-700 font-medium">Total Amount Imported</div>
          <div class="text-3xl font-bold text-indigo-900 mt-2">{{ formatAmount(summary.amount) }}</div>
        </div>
        <div class="flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full">
          <svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-4">
      <button
        @click="$emit('start-new')"
        class="flex-1 inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
        </svg>
        Import Another File
      </button>
      
      <button
        @click="$emit('redo-import')"
        class="flex-1 inline-flex items-center justify-center px-6 py-3 border border-indigo-300 text-base font-medium rounded-lg shadow-sm text-indigo-700 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        Redo Import
      </button>

      <a
        v-if="summary.importLogUrl"
        :href="summary.importLogUrl"
        target="_blank"
        class="flex-1 inline-flex items-center justify-center px-6 py-3 border border-indigo-300 text-base font-medium rounded-lg shadow-sm text-indigo-700 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        View Import Log
      </a>

      <a
        v-if="summary.errors > 0 && summary.errorCsvPath"
        :href="summary.errorCsvPath"
        download
        class="flex-1 inline-flex items-center justify-center px-6 py-3 border border-red-300 text-base font-medium rounded-lg shadow-sm text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        Download Error CSV
      </a>
    </div>

    <!-- Success Message -->
    <div v-if="summary.imported > 0" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-green-800">
            Successfully imported {{ summary.imported }} sales invoice{{ summary.imported !== 1 ? 's' : '' }}!
          </p>
          <p class="text-sm text-green-700 mt-1">
            All invoices are in draft status. You can review and submit them from the Sales Invoice list.
          </p>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="summary.errors > 0" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-red-800">
            {{ summary.errors }} invoice{{ summary.errors !== 1 ? 's' : '' }} failed to import
          </p>
          <p class="text-sm text-red-700 mt-1">
            Download the error CSV to see details and fix the issues.
          </p>
          
          <!-- Error Details -->
          <div v-if="summary.errorDetails && summary.errorDetails.length > 0" class="mt-3">
            <details class="text-sm">
              <summary class="cursor-pointer text-red-800 font-medium hover:text-red-900">
                View Error Details ({{ summary.errorDetails.length }} errors)
              </summary>
              <div class="mt-2 pl-4 border-l-2 border-red-300">
                <div v-for="(error, index) in summary.errorDetails" :key="index" class="mb-2 text-red-700">
                  {{ error }}
                </div>
              </div>
            </details>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
defineProps({
  summary: {
    type: Object,
    default: () => ({
      total: 0,
      imported: 0,
      skipped: 0,
      errors: 0,
      amount: 0,
      errorCsvPath: null,
      importLogUrl: null,
      errorDetails: []
    })
  }
})

defineEmits(['start-new', 'redo-import'])

function formatAmount(amount) {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 2
  }).format(amount)
}
</script>

