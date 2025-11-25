<template>
  <div class="nepali-date-picker relative">
    <div class="relative">
      <input
        type="text"
        :value="displayDate"
        @click="showPicker = !showPicker"
        readonly
        :placeholder="placeholder"
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 cursor-pointer"
      />
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    </div>
    
    <div v-if="showPicker" class="absolute z-50 mt-2 bg-white border border-gray-300 rounded-lg shadow-xl p-4 min-w-[280px]">
      <div class="flex items-center justify-between mb-4">
        <button @click="changeMonth(-1)" class="p-1 hover:bg-gray-100 rounded">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="text-center">
          <div class="font-semibold">{{ nepaliMonths[pickerMonth - 1] }} {{ pickerYear }}</div>
          <div class="text-xs text-gray-500">Bikram Sambat</div>
        </div>
        <button @click="changeMonth(1)" class="p-1 hover:bg-gray-100 rounded">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div v-for="day in ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']" :key="day" class="text-center text-xs font-medium text-gray-600 py-1">
          {{ day }}
        </div>
      </div>
      
      <div class="grid grid-cols-7 gap-1">
        <button
          v-for="day in daysInMonth"
          :key="day"
          @click="selectDay(day)"
          :class="[
            'p-2 text-sm rounded hover:bg-blue-100',
            day === pickerDay ? 'bg-blue-600 text-white hover:bg-blue-700' : 'text-gray-700'
          ]"
        >
          {{ day }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { bsToAd, adToBs, getTodayBs, formatBsDate } from '../utils/nepaliDate'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select date'
  },
  showEnglishDate: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const nepaliMonths = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']

const showPicker = ref(false)
const displayDate = ref('')
const pickerYear = ref(2081)
const pickerMonth = ref(1)
const pickerDay = ref(1)

const daysInMonth = computed(() => {
  // Simplified - using approximate days per month
  const daysPerMonth = {
    2080: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2081: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2082: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
  }
  
  const yearData = daysPerMonth[pickerYear.value] || [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
  const days = yearData[pickerMonth.value - 1] || 30
  
  return Array.from({ length: days }, (_, i) => i + 1)
})

const changeMonth = (delta) => {
  pickerMonth.value += delta
  if (pickerMonth.value > 12) {
    pickerMonth.value = 1
    pickerYear.value++
  } else if (pickerMonth.value < 1) {
    pickerMonth.value = 12
    pickerYear.value--
  }
}

const selectDay = (day) => {
  pickerDay.value = day
  const bsDate = `${pickerYear.value}-${String(pickerMonth.value).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  handleDateChange(bsDate)
  showPicker.value = false
}

const handleDateChange = (bsDate) => {
  displayDate.value = bsDate
  const adDate = bsToAd(bsDate)
  
  if (adDate) {
    emit('update:modelValue', adDate)
  }
}

// Initialize from modelValue
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    const bsDate = adToBs(newVal)
    displayDate.value = bsDate
    
    if (bsDate) {
      const [year, month, day] = bsDate.split('-').map(Number)
      pickerYear.value = year
      pickerMonth.value = month
      pickerDay.value = day
    }
  } else {
    displayDate.value = ''
  }
}, { immediate: true })

// Close picker when clicking outside
const handleClickOutside = (event) => {
  if (showPicker.value && !event.target.closest('.nepali-date-picker')) {
    showPicker.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  const today = getTodayBs()
  if (today && !props.modelValue) {
    const [year, month, day] = today.split('-').map(Number)
    pickerYear.value = year
    pickerMonth.value = month
    pickerDay.value = day
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.nepali-date-picker input {
  background-color: white;
}
</style>

