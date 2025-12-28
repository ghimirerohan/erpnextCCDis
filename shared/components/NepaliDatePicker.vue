<template>
  <div class="nepali-date-picker relative">
    <div class="relative">
      <input
        ref="datepickerInput"
        type="text"
        :value="displayDate"
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

const datepickerInput = ref(null)
const displayDate = ref('')
const isLibraryLoaded = ref(false)

const loadLibrary = async () => {
  if (typeof window === 'undefined') return
  
  // Check if everything is already loaded and working
  if (window.NepaliFunctions && window.jQuery && window.jQuery.fn.nepaliDatePicker) {
    isLibraryLoaded.value = true
    return
  }

  console.log('NepaliDatePicker: Loading dependencies...');

  // Load jQuery if missing
  if (!window.jQuery) {
    await new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
      script.onload = () => {
        console.log('NepaliDatePicker: jQuery loaded from CDN');
        resolve();
      };
      script.onerror = () => {
        console.error('NepaliDatePicker: Failed to load jQuery from CDN');
        resolve();
      };
      document.head.appendChild(script);
    });
  }

  // Load CSS
  if (!document.querySelector('link[href*="nepali.datepicker.v5.0.6.min.css"]')) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.type = 'text/css'
    link.href = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.css'
    document.head.appendChild(link)
  }

  // Load JS - Force reload if plugin is missing even if script exists
  const existingScript = document.querySelector('script[src*="nepali.datepicker.v5.0.6.min.js"]');
  const needsScript = !existingScript || (window.jQuery && !window.jQuery.fn.nepaliDatePicker);

  if (needsScript) {
    if (existingScript) {
      console.log('NepaliDatePicker: Script exists but plugin missing, re-injecting...');
      // We don't necessarily need to remove the old one, but we need to ensure it runs again
      // with the current jQuery.
    }
    
    await new Promise((resolve) => {
      const script = document.createElement('script')
      // Add a timestamp to force reload if needed
      script.src = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js?v=' + Date.now();
      script.onload = () => {
        console.log('NepaliDatePicker: Library script loaded');
        isLibraryLoaded.value = true
        resolve()
      }
      script.onerror = () => {
        console.error('NepaliDatePicker: Failed to load library script');
        resolve()
      }
      document.head.appendChild(script)
    })
  } else {
    isLibraryLoaded.value = true
  }
}

const syncWithLibrary = (bsDate) => {
  if (!bsDate) return;
  
  if (bsDate !== displayDate.value) {
    displayDate.value = bsDate;
    const adDate = bsToAd(bsDate);
    if (adDate && adDate !== props.modelValue) {
      console.log('NepaliDatePicker: Syncing AD date to parent:', adDate);
      emit('update:modelValue', adDate);
    }
  }
}

const initPicker = () => {
  if (!datepickerInput.value || !window.jQuery || !window.jQuery.fn.nepaliDatePicker) {
    console.warn('NepaliDatePicker: Missing dependencies for init');
    return
  }

  const $input = window.jQuery(datepickerInput.value);
  
  $input.nepaliDatePicker({
    ndpYear: true,
    ndpMonth: true,
    ndpYearCount: 100,
    miniEnglishDates: true,
    onChange: function() {
      console.log('NepaliDatePicker: onChange fired');
      syncWithLibrary(datepickerInput.value.value);
    }
  });

  // Additional listener for the library's custom event if it exists
  $input.on('dateSelect', function(event) {
    console.log('NepaliDatePicker: dateSelect fired');
    const bsDate = (event.datePickerData && event.datePickerData.bsDate) || datepickerInput.value.value;
    syncWithLibrary(bsDate);
  });

  // Watch for any change in the DOM value directly (polling as fallback)
  const interval = setInterval(() => {
    if (datepickerInput.value && datepickerInput.value.value !== displayDate.value) {
      syncWithLibrary(datepickerInput.value.value);
    }
  }, 500);

  onBeforeUnmount(() => {
    clearInterval(interval);
    $input.off();
  });
}

// Update local display when modelValue (AD date) changes from parent
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    const bsDate = adToBs(newVal);
    if (bsDate !== displayDate.value) {
      displayDate.value = bsDate;
    }
  } else {
    displayDate.value = '';
  }
}, { immediate: true })

onMounted(async () => {
  await loadLibrary()
  await nextTick()
  initPicker()
  
  if (!props.modelValue) {
    const today = getTodayBs()
    if (today) displayDate.value = today
  }
})
</script>

<style scoped>
.nepali-date-picker input {
  background-color: white;
}

/* Library-specific styling overrides */
:deep(.ndp-container) {
  z-index: 9999 !important;
  font-family: inherit;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
</style>
