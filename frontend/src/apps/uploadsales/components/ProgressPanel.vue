<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex items-center mb-6">
      <div class="flex items-center justify-center w-10 h-10 bg-yellow-100 rounded-lg mr-3">
        <svg class="w-5 h-5 text-yellow-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900">Importing Sales Invoices</h2>
    </div>

    <!-- Progress Bar -->
    <div class="mb-6">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-gray-700">
          Progress: {{ progress.processed }} / {{ progress.total }}
        </span>
        <span class="text-sm font-medium text-gray-700">
          {{ progressPercent }}%
        </span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          class="bg-indigo-600 h-4 rounded-full transition-all duration-300 ease-out"
          :style="{ width: progressPercent + '%' }"
        ></div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-green-600">{{ progress.imported }}</div>
        <div class="text-sm text-green-700">Imported</div>
      </div>
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-yellow-600">{{ progress.skipped }}</div>
        <div class="text-sm text-yellow-700">Skipped</div>
      </div>
      <div class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-red-600">{{ progress.errors }}</div>
        <div class="text-sm text-red-700">Errors</div>
      </div>
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-blue-600">{{ formatAmount(progress.amount) }}</div>
        <div class="text-sm text-blue-700">Total Amount</div>
      </div>
    </div>

    <!-- Current Status -->
    <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-5 h-5 text-gray-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="ml-3 flex-1">
          <p class="text-sm font-medium text-gray-900">Current Status</p>
          <p class="text-sm text-gray-600 mt-1">{{ progress.message || 'Processing...' }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
import { computed } from 'vue'

const props = defineProps({
  progress: {
    type: Object,
    default: () => ({
      processed: 0,
      total: 0,
      message: '',
      imported: 0,
      skipped: 0,
      errors: 0,
      amount: 0
    })
  }
})

const progressPercent = computed(() => {
  if (props.progress.total === 0) return 0
  return Math.round((props.progress.processed / props.progress.total) * 100)
})

function formatAmount(amount) {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 2
  }).format(amount)
}
</script>

