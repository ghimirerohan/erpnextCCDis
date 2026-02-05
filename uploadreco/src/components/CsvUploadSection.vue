<!-- ADDED BY AI: DAILY_PAYMENT_RECO - CSV Upload Section -->
<template>
  <div class="bg-white rounded-xl shadow-lg border-2 border-dashed p-8 transition-colors"
       :style="getBorderStyle()">
    <div class="text-center">
      <div class="flex items-center justify-center w-16 h-16 rounded-full mx-auto mb-4"
           :style="{ backgroundColor: companyConfig?.brand_colors?.bg || '#E9D5FF' }">
        <svg class="w-8 h-8" :style="{ color: companyConfig?.brand_colors?.primary || '#9333EA' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">
        Upload {{ companyLabel }} Payment Register CSV
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
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transition-all hover:opacity-90"
        :style="{ backgroundColor: companyConfig?.brand_colors?.primary || '#9333EA' }"
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
        <template v-if="isHorlicksCompany">
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
  },
  companyConfig: {
    type: Object,
    default: null
  }
})

// Check if company is horlicks-based
const isHorlicksCompany = computed(() => {
  return props.companyConfig?.main_product === 'horlicks' || props.companyConfig?.is_horlicks
})

// Get company label for display
const companyLabel = computed(() => {
  if (!props.companyConfig?.abbr) return props.company || 'Company'
  return props.companyConfig.abbr
})

// Get border style based on company colors
const getBorderStyle = () => {
  const color = props.companyConfig?.brand_colors?.primary || '#9333EA'
  return {
    borderColor: `${color}50`,
    '--hover-border-color': color
  }
}

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

<style scoped>
div:hover {
  border-color: var(--hover-border-color, #9333EA) !important;
}
</style>
