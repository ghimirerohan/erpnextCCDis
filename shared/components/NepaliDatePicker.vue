<template>
  <div class="nepali-date-picker-wrapper" ref="wrapperRef">
    <div class="relative">
      <input
        ref="inputRef"
        type="text"
        :value="displayDate"
        readonly
        :placeholder="placeholder"
        @click="toggleCalendar"
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 cursor-pointer bg-white"
      />
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    </div>
    
    <!-- Calendar Container - rendered inline when open -->
    <div 
      v-if="isOpen" 
      ref="calendarRef"
      class="ndp-calendar-container"
    >
      <!-- Calendar will be rendered here by the library -->
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { bsToAd, adToBs, getTodayBs } from '../utils/nepaliDate'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select date'
  }
})

const emit = defineEmits(['update:modelValue'])

const wrapperRef = ref(null)
const inputRef = ref(null)
const calendarRef = ref(null)
const displayDate = ref('')
const isOpen = ref(false)
let pickerInstance = null

// Inject styles for high z-index in modals
const injectStyles = () => {
  const styleId = 'nepali-datepicker-custom-styles'
  if (document.getElementById(styleId)) return
  
  const style = document.createElement('style')
  style.id = styleId
  style.textContent = `
    .nepali-date-picker-wrapper {
      position: relative;
    }
    
    .ndp-calendar-container {
      position: absolute;
      top: 100%;
      left: 0;
      z-index: 2147483647;
      margin-top: 4px;
    }
    
    .ndp-calendar-container .ndp-container {
      position: relative !important;
      z-index: 2147483647 !important;
      background: white !important;
      border: 1px solid #d1d5db !important;
      border-radius: 8px !important;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
    }
    
    .ndp-container.ndp-inline {
      display: block !important;
    }
    
    .ndp-container * {
      pointer-events: auto !important;
    }
    
    .ndp-container .ndp-table td {
      cursor: pointer !important;
    }
    
    .ndp-container .ndp-table td:hover:not(.ndp-disabled) {
      background-color: #e5e7eb !important;
    }
    
    .ndp-container .ndp-selected,
    .ndp-container .ndp-today.ndp-selected {
      background-color: #3b82f6 !important;
      color: white !important;
    }
    
    .ndp-container .ndp-today {
      border: 2px solid #3b82f6 !important;
    }
  `
  document.head.appendChild(style)
}

// Load dependencies
const loadDependencies = async () => {
  injectStyles()
  
  // Load jQuery if not present
  if (!window.jQuery) {
    await new Promise((resolve) => {
      const script = document.createElement('script')
      script.src = 'https://code.jquery.com/jquery-3.7.1.min.js'
      script.onload = resolve
      script.onerror = resolve
      document.head.appendChild(script)
    })
  }
  
  // Load CSS
  if (!document.querySelector('link[href*="nepali.datepicker"]')) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.css'
    document.head.appendChild(link)
  }
  
  // Load the datepicker JS
  if (!window.NepaliDatePicker) {
    await new Promise((resolve) => {
      const script = document.createElement('script')
      script.src = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js'
      script.onload = resolve
      script.onerror = resolve
      document.head.appendChild(script)
    })
  }
}

// Handle date selection
const handleDateSelect = (dateObj) => {
  if (!dateObj) return
  
  let bsDate
  if (typeof dateObj === 'string') {
    bsDate = dateObj
  } else if (dateObj.value) {
    bsDate = dateObj.value
  } else if (dateObj.year && dateObj.month && dateObj.day) {
    bsDate = `${dateObj.year}-${String(dateObj.month).padStart(2, '0')}-${String(dateObj.day).padStart(2, '0')}`
  }
  
  if (bsDate && bsDate !== displayDate.value) {
    displayDate.value = bsDate
    const adDate = bsToAd(bsDate)
    if (adDate) {
      emit('update:modelValue', adDate)
    }
  }
  
  // Close calendar after selection
  isOpen.value = false
}

// Toggle calendar visibility
const toggleCalendar = async () => {
  if (isOpen.value) {
    isOpen.value = false
    return
  }
  
  isOpen.value = true
  
  await nextTick()
  
  // Wait for the container to be rendered
  setTimeout(() => {
    initializeInlineCalendar()
  }, 50)
}

// Initialize inline calendar
const initializeInlineCalendar = () => {
  if (!calendarRef.value || !window.NepaliDatePicker) {
    console.error('NepaliDatePicker: Calendar container or library not available')
    return
  }
  
  // Clear previous content
  calendarRef.value.innerHTML = ''
  
  // Get current value
  let initialValue = null
  if (displayDate.value) {
    initialValue = displayDate.value
  }
  
  // Create inline picker
  try {
    pickerInstance = new window.NepaliDatePicker(calendarRef.value, {
      dateFormat: 'YYYY-MM-DD',
      inline: true,
      value: initialValue,
      onSelect: (dateObj) => {
        handleDateSelect(dateObj)
      }
    })
  } catch (e) {
    console.error('NepaliDatePicker: Failed to initialize', e)
  }
}

// Handle click outside to close
const handleClickOutside = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

// Watch for external modelValue changes
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    const bsDate = adToBs(newVal)
    if (bsDate && bsDate !== displayDate.value) {
      displayDate.value = bsDate
    }
  } else {
    displayDate.value = ''
  }
}, { immediate: true })

onMounted(async () => {
  await loadDependencies()
  
  // Set today's date if no value
  if (!props.modelValue) {
    const today = getTodayBs()
    if (today) {
      displayDate.value = today
      const adDate = bsToAd(today)
      if (adDate) {
        emit('update:modelValue', adDate)
      }
    }
  }
  
  // Add click outside listener
  document.addEventListener('mousedown', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside)
  isOpen.value = false
})
</script>

<style scoped>
.nepali-date-picker-wrapper input {
  background-color: white;
}
</style>
