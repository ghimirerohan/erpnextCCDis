<template>
  <div class="nepali-bs-picker-root" ref="rootRef">
    <label v-if="label" class="block text-sm font-semibold text-gray-700 mb-1.5">{{ label }}</label>
    <input
      ref="inputRef"
      type="text"
      :value="displayValue"
      readonly
      :placeholder="placeholder"
      @click="openCalendar"
      @touchstart.prevent="openCalendar"
      class="w-full px-3 py-2.5 border border-gray-300 rounded-lg bg-white cursor-pointer focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-gray-900"
    />

    <!-- Dropdown: official Nepali Datepicker v5 renders inside this container -->
    <div
      v-if="isOpen"
      ref="dropdownRef"
      class="nepali-bs-dropdown ndp-dropdown-wrapper"
      role="dialog"
      aria-label="Nepali BS date picker"
    >
      <div ref="pickerContainer" class="ndp-inline-container"></div>
      <div class="nepali-bs-dropdown-actions">
        <button type="button" class="nepali-bs-btn cancel" @click="closeCalendar">रद्द गर्नुहोस्</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { bsToAd, adToBs } from '../../../shared/utils/nepaliDate'

const NEPALI_DATEPICKER_CSS = 'https://nepalidatepicker.sajanmaharjan.com.np/v5/nepali.datepicker/css/nepali.datepicker.v5.0.6.min.css'
const NEPALI_DATEPICKER_JS = 'https://nepalidatepicker.sajanmaharjan.com.np/v5/nepali.datepicker/js/nepali.datepicker.v5.0.6.min.js'
const JQUERY_CDN = 'https://code.jquery.com/jquery-3.7.1.min.js'

// Contract: v-model is AD (Gregorian) YYYY-MM-DD. Input shows BS; library uses BS; we emit AD.
const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: 'Nepali BS Date' },
  placeholder: { type: String, default: 'Select BS date (tap to open calendar)' },
  /** Passed to official datepicker: show English day in each cell. See https://nepalidatepicker.sajanmaharjan.com.np/v5/ */
  miniEnglishDates: { type: Boolean, default: true }
})

const emit = defineEmits(['update:modelValue', 'select'])

const rootRef = ref(null)
const inputRef = ref(null)
const dropdownRef = ref(null)
const pickerContainer = ref(null)
const isOpen = ref(false)
const libReady = ref(false)
let pickerInstance = null

// Display: show BS in input (modelValue is AD)
const displayValue = computed(() => {
  const ad = props.modelValue
  if (!ad || typeof ad !== 'string') return ''
  return adToBs(ad.trim()) || ''
})

function handleDateSelect(dateObj) {
  let bsStr = ''
  if (typeof dateObj === 'string') {
    bsStr = dateObj
  } else if (dateObj && dateObj.value) {
    bsStr = dateObj.value
  } else if (dateObj && dateObj.year != null && dateObj.month != null && dateObj.day != null) {
    const m = dateObj.month
    const d = dateObj.day
    bsStr = `${dateObj.year}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`
  }
  if (!bsStr) return
  const adStr = bsToAd(bsStr)
  if (adStr) emit('update:modelValue', adStr)
  emit('select', { bs: bsStr, ad: adStr || '' })
  closeCalendar()
}

function openCalendar() {
  if (isOpen.value) return
  isOpen.value = true
  if (!libReady.value) {
    loadAndInit()
  } else {
    nextTick(() => initPicker())
  }
}

function closeCalendar() {
  isOpen.value = false
  if (pickerInstance && typeof pickerInstance.destroy === 'function') {
    try {
      pickerInstance.destroy(pickerContainer.value)
    } catch (_) {}
    pickerInstance = null
  }
}

function injectStyles() {
  const id = 'nepali-datepicker-v5-dropdown-styles'
  if (document.getElementById(id)) return
  const link = document.createElement('link')
  link.id = id
  link.rel = 'stylesheet'
  link.href = NEPALI_DATEPICKER_CSS
  document.head.appendChild(link)
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (src.includes('jquery') && window.jQuery) {
      resolve()
      return
    }
    const el = document.createElement('script')
    el.src = src
    el.onload = () => resolve()
    el.onerror = () => reject(new Error(`Failed to load ${src}`))
    document.head.appendChild(el)
  })
}

async function loadAndInit() {
  injectStyles()
  try {
    if (!window.jQuery) await loadScript(JQUERY_CDN)
    if (!window.NepaliDatePicker && !(typeof HTMLElement !== 'undefined' && HTMLElement.prototype.NepaliDatePicker)) {
      await loadScript(NEPALI_DATEPICKER_JS)
      await new Promise(r => setTimeout(r, 150))
    }
    if (typeof HTMLElement !== 'undefined' && HTMLElement.prototype.NepaliDatePicker && !window.NepaliDatePicker) {
      window.NepaliDatePicker = function (el, opts) {
        if (el && el.NepaliDatePicker) return el.NepaliDatePicker(opts)
        throw new Error('NepaliDatePicker: invalid element')
      }
    }
    libReady.value = true
    await nextTick()
    initPicker()
  } catch (e) {
    console.error('[NepaliBSDatePicker] Failed to load official datepicker', e)
    libReady.value = false
    isOpen.value = false
  }
}

function initPicker() {
  if (!pickerContainer.value || !(window.NepaliDatePicker || (typeof HTMLElement !== 'undefined' && HTMLElement.prototype.NepaliDatePicker))) return
  pickerContainer.value.innerHTML = ''
  const initialValue = displayValue.value || null
  try {
    pickerInstance = new window.NepaliDatePicker(pickerContainer.value, {
      dateFormat: 'YYYY-MM-DD',
      inline: true,
      miniEnglishDates: props.miniEnglishDates,
      value: initialValue,
      onSelect: (dateObj) => handleDateSelect(dateObj)
    })
  } catch (e) {
    console.error('[NepaliBSDatePicker] Init failed', e)
  }
}

function handleClickOutside(e) {
  if (rootRef.value && !rootRef.value.contains(e.target) && isOpen.value) {
    closeCalendar()
  }
}

watch(() => props.modelValue, () => {
  if (isOpen.value && pickerInstance && pickerContainer.value) {
    try {
      const bs = displayValue.value
      if (pickerInstance.setDate) pickerInstance.setDate(bs)
    } catch (_) {}
  }
})

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside)
  closeCalendar()
  isOpen.value = false
})
</script>

<style scoped>
.nepali-bs-picker-root {
  position: relative;
}
.nepali-bs-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  min-width: 100%;
  width: max-content;
  max-width: 360px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}
.ndp-inline-container {
  min-height: 280px;
}
/* Let official datepicker styles apply; only ensure container is visible */
.nepali-bs-dropdown :deep(.ndp-container) {
  position: relative !important;
  border: none !important;
  box-shadow: none !important;
}
.nepali-bs-dropdown-actions {
  padding: 10px 12px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}
.nepali-bs-btn {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid #d1d5db;
  background: #fff;
  color: #374151;
}
.nepali-bs-btn:hover {
  background: #e5e7eb;
}
</style>
