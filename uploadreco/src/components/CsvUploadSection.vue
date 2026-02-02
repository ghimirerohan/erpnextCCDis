<!-- ADDED BY AI: DAILY_PAYMENT_RECO - CSV Upload Section -->
<template>
  <div class="bg-white rounded-xl shadow-lg border-2 border-dashed p-8 transition-colors"
       :class="isPadmashree ? 'border-blue-300 hover:border-blue-400' : 'border-gray-300 hover:border-purple-400'">
    <div class="text-center">
      <div class="flex items-center justify-center w-16 h-16 rounded-full mx-auto mb-4"
           :class="isPadmashree ? 'bg-blue-100' : 'bg-purple-100'">
        <svg class="w-8 h-8" :class="isPadmashree ? 'text-blue-600' : 'text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">
        Upload {{ isPadmashree ? 'Padmashree' : 'Riya' }} Payment Register CSV
      </h3>
      <p class="text-gray-600 mb-6">Upload the daily payment reconciliation CSV file</p>
      
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        class="hidden"
        @change="handleFileSelect"
      />
      
      <button
        @click="$refs.fileInput.click()"
        :disabled="loading"
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transition-all"
        :class="isPadmashree ? 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500' : 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-500'"
      >
        <svg v-if="!loading" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
        </svg>
        <svg v-else class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ loading ? 'Processing...' : 'Choose CSV File' }}
      </button>
      
      <p class="text-sm text-gray-500 mt-4">
        <template v-if="isPadmashree">
          Supported format: Customer ID, Customer Ledger, Invoice Number, Net Amount, etc.
        </template>
        <template v-else>
          Supported format: Outlet Code, Outlet Name, Reference No, Amount
        </template>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  company: {
    type: String,
    default: ''
  }
})

const isPadmashree = computed(() => props.company === 'PadmaShree Trade Link')

const emit = defineEmits(['file-selected'])

const fileInput = ref(null)

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      emit('file-selected', e.target.result)
    }
    reader.readAsText(file)
  }
}
</script>

