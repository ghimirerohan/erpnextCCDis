<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Summary Card Component -->
<template>
  <div class="rounded-xl shadow-xl p-4 sm:p-6 border-2" style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); border-color: #0284c7;">
    <div class="flex items-center justify-between mb-3 sm:mb-4 gap-2">
      <div class="min-w-0 flex-1">
        <h2 class="text-lg sm:text-xl lg:text-2xl font-bold truncate" style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{{ driverName }}</h2>
        <p class="text-xs sm:text-sm font-semibold truncate" style="color: #ffffff;">{{ todayDate }}</p>
        <p v-if="bsToday" class="text-xs mt-0.5 font-medium" style="color: #f0f9ff;">BS: {{ bsToday }}</p>
      </div>
      <button
        @click="$emit('view-all')"
        class="inline-flex items-center px-2 py-1.5 sm:px-3 sm:py-2 rounded-lg text-xs sm:text-sm font-bold transition-all duration-200 shadow-lg hover:shadow-xl flex-shrink-0"
        style="border: 2px solid #ffffff; color: #0284c7; background-color: #ffffff;"
      >
        View All
      </button>
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-3 lg:gap-4">
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Initial Total</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.initial_total_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Cash Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.cash_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">QR Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.qr_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Cheque Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.cheque_amount) }}</p>
      </div>
    </div>
    
    <div class="mt-3 sm:mt-4 pt-3 sm:pt-4" style="border-top: 2px solid rgba(255, 255, 255, 0.5);">
      <div class="flex justify-between items-center gap-2">
        <span class="font-bold text-base sm:text-lg lg:text-xl" style="color: #ffffff;">Remaining</span>
        <span class="text-xl sm:text-2xl lg:text-3xl font-bold truncate" style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{{ formatCurrency(summary.remaining_amount) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const props = defineProps({
  driverName: {
    type: String,
    required: true
  },
  summary: {
    type: Object,
    required: true
  }
})

defineEmits(['view-all'])

const bsToday = ref('')

const todayDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}

const loadNepaliDate = async () => {
  try {
    if (typeof window !== 'undefined' && !window.NepaliFunctions) {
      const script = document.createElement('script')
      script.src = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js'
      document.head.appendChild(script)
      await new Promise((resolve) => { 
        script.onload = resolve
        script.onerror = resolve
      })
    }
    
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const d = new Date()
      const bs = window.NepaliFunctions.AD2BS({ 
        year: d.getFullYear(), 
        month: d.getMonth() + 1, 
        day: d.getDate() 
      })
      bsToday.value = `${bs.year}-${String(bs.month).padStart(2, '0')}-${String(bs.day).padStart(2, '0')}`
    }
  } catch (error) {
    console.warn('Failed to load Nepali date:', error)
  }
}

onMounted(() => {
  loadNepaliDate()
})
</script>

