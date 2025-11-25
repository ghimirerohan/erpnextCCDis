<template>
  <div class="customer-select-wrapper" ref="wrapperRef">
    <label v-if="label" class="block text-sm font-semibold text-gray-700 mb-2 sm:mb-3">{{ label }}</label>
    <div class="relative">
      <!-- Search input - always visible -->
      <div class="relative" ref="inputContainerRef">
        <input
          ref="inputRef"
          v-model="customerSearchQuery"
          @focus="handleCustomerInputFocus"
          @input="handleCustomerInput"
          @click="handleCustomerInputClick"
          type="text"
          :placeholder="placeholder"
          :readonly="isMobile && !showCustomerDropdown"
          class="w-full px-4 py-3 h-[44px] border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-base"
          :class="{ 'border-blue-500': showCustomerDropdown, 'cursor-pointer': isMobile && !showCustomerDropdown }"
        />
        <!-- Loading indicator -->
        <div v-if="loadingCustomers" class="absolute right-3 top-1/2 transform -translate-y-1/2">
          <svg class="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <!-- Dropdown icon -->
        <div v-else class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
        
        <!-- Desktop dropdown - below input -->
        <div
          v-if="!isMobile && showCustomerDropdown && !loadingCustomers && customerOptions.length > 0 && filteredCustomerOptions.length > 0"
          ref="dropdownRef"
          class="customer-dropdown customer-dropdown-desktop"
        >
          <div
            v-for="(option, index) in filteredCustomerOptions"
            :key="option.value || index"
            @click="selectCustomer(option)"
            class="px-4 py-3 cursor-pointer hover:bg-blue-50 transition-colors border-b border-gray-100 last:border-b-0"
            :class="{ 'bg-blue-50': modelValue === option.value }"
          >
            <div class="font-medium text-gray-900">{{ option.customer_name }}</div>
            <div class="text-sm text-gray-500">{{ option.value }}</div>
          </div>
        </div>
        <!-- Desktop no results -->
        <div
          v-if="!isMobile && showCustomerDropdown && customerSearchQuery && !loadingCustomers && customerOptions.length > 0 && filteredCustomerOptions.length === 0"
          ref="dropdownRef"
          class="customer-dropdown customer-dropdown-desktop"
        >
          <div class="text-sm text-gray-500 text-center p-4">No customers found</div>
        </div>
      </div>
    </div>
    <p v-if="!modelValue && helpText" class="mt-2 text-xs sm:text-sm text-gray-500">{{ helpText }}</p>
    
    <!-- Mobile Bottom Sheet Modal -->
    <Teleport to="body">
      <Transition name="bottom-sheet">
        <div
          v-if="isMobile && showCustomerDropdown"
          class="customer-search-modal"
          @click.self="closeModal"
          @touchstart="handleTouchStart"
          @touchmove="handleTouchMove"
          @touchend="handleTouchEnd"
        >
          <!-- Backdrop -->
          <div class="customer-search-backdrop" @click="closeModal"></div>
          
          <!-- Bottom Sheet -->
          <div
            ref="bottomSheetRef"
            class="customer-search-bottom-sheet"
            :style="{ transform: `translateY(${sheetOffset}px)` }"
          >
            <!-- Handle bar -->
            <div class="customer-search-handle" @touchstart.stop="handleDragStart">
              <div class="customer-search-handle-bar"></div>
            </div>
            
            <!-- Header with search input -->
            <div class="customer-search-header">
              <div class="customer-search-header-top">
                <div class="customer-search-title">{{ label || 'Select Customer' }}</div>
                <button
                  @click="closeModal"
                  class="customer-search-close"
                  aria-label="Close"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
              <div class="customer-search-input-wrapper">
                <input
                  ref="modalInputRef"
                  v-model="customerSearchQuery"
                  @input="handleCustomerInput"
                  type="text"
                  :placeholder="placeholder"
                  class="customer-search-input"
                  autofocus
                />
                <button
                  v-if="customerSearchQuery"
                  @click="customerSearchQuery = ''; filterCustomers()"
                  class="customer-search-clear"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Results list -->
            <div class="customer-search-results" ref="resultsRef">
              <!-- Loading -->
              <div v-if="loadingCustomers" class="customer-search-loading">
                <svg class="animate-spin h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="ml-2 text-gray-600">Loading customers...</span>
              </div>
              
              <!-- No data -->
              <div v-else-if="customerOptions.length === 0" class="customer-search-empty">
                <svg class="w-12 h-12 text-gray-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                <p class="text-gray-500">No customers available</p>
              </div>
              
              <!-- No results -->
              <div v-else-if="customerSearchQuery && filteredCustomerOptions.length === 0" class="customer-search-empty">
                <svg class="w-12 h-12 text-gray-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                <p class="text-gray-500">No customers found</p>
                <p class="text-sm text-gray-400 mt-1">Try a different search term</p>
              </div>
              
              <!-- Results list -->
              <div v-else class="customer-search-list">
                <div
                  v-for="(option, index) in filteredCustomerOptions"
                  :key="option.value || index"
                  @click="selectCustomer(option)"
                  class="customer-search-item"
                  :class="{ 'customer-search-item-selected': modelValue === option.value }"
                >
                  <div class="customer-search-item-content">
                    <div class="customer-search-item-name">{{ option.customer_name }}</div>
                    <div class="customer-search-item-code">{{ option.value }}</div>
                  </div>
                  <svg v-if="modelValue === option.value" class="customer-search-item-check" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { createResource, call as $call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: null
  },
  label: {
    type: String,
    default: 'Customer'
  },
  placeholder: {
    type: String,
    default: 'Search by customer name or code'
  },
  helpText: {
    type: String,
    default: 'Start typing to search. All customers are available by name or code.'
  },
  apiUrl: {
    type: String,
    default: 'custom_erp.custom_erp.api.fonepay.search_customers'
  },
  limit: {
    type: Number,
    default: 10000
  },
  autoLoad: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'select'])

const customerOptions = ref([])
const filteredCustomerOptions = ref([])
const customerSearchQuery = ref('')
const showCustomerDropdown = ref(false)
const loadingCustomers = ref(false)

// Refs for DOM elements
const wrapperRef = ref(null)
const inputRef = ref(null)
const inputContainerRef = ref(null)
const dropdownRef = ref(null)
const bottomSheetRef = ref(null)
const modalInputRef = ref(null)
const resultsRef = ref(null)

// Mobile detection and bottom sheet handling
const isMobile = ref(false)
const sheetOffset = ref(0)
const isDragging = ref(false)
const dragStartY = ref(0)
const dragStartOffset = ref(0)

// Detect mobile device
const detectMobile = () => {
  isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                   window.innerWidth <= 768 ||
                   'ontouchstart' in window
}

// Handle input focus/click - open modal on mobile
const handleCustomerInputFocus = () => {
  detectMobile()
  filterCustomers()
  if (!isMobile.value) {
    showCustomerDropdown.value = true
  }
}

const handleCustomerInputClick = () => {
  detectMobile()
  if (isMobile.value) {
    filterCustomers()
    showCustomerDropdown.value = true
    // Focus modal input after it renders
    nextTick(() => {
      setTimeout(() => {
        if (modalInputRef.value) {
          modalInputRef.value.focus()
        }
      }, 300)
    })
  }
}

// Handle input change
const handleCustomerInput = () => {
  filterCustomers()
  if (!isMobile.value) {
    showCustomerDropdown.value = true
  }
}

// Close modal
const closeModal = () => {
  showCustomerDropdown.value = false
  sheetOffset.value = 0
  // Blur input to close keyboard
  if (modalInputRef.value) {
    modalInputRef.value.blur()
  }
}

// Bottom sheet drag handling
const handleTouchStart = (e) => {
  if (e.target === bottomSheetRef.value || bottomSheetRef.value?.contains(e.target)) {
    return
  }
  isDragging.value = true
  dragStartY.value = e.touches[0].clientY
  dragStartOffset.value = sheetOffset.value
}

const handleTouchMove = (e) => {
  if (!isDragging.value) return
  const deltaY = e.touches[0].clientY - dragStartY.value
  const newOffset = Math.max(0, dragStartOffset.value + deltaY)
  sheetOffset.value = newOffset
}

const handleTouchEnd = () => {
  if (!isDragging.value) return
  isDragging.value = false
  
  // If dragged down more than 100px, close modal
  if (sheetOffset.value > 100) {
    closeModal()
  } else {
    // Snap back to top
    sheetOffset.value = 0
  }
}

const handleDragStart = (e) => {
  isDragging.value = true
  dragStartY.value = e.touches[0].clientY
  dragStartOffset.value = sheetOffset.value
}

// Create resource for customer search
const customerSearchResource = createResource({
  url: props.apiUrl,
  auto: false,
  makeParams({ query, limit }) {
    return {
      query: query || '',
      limit: limit || props.limit
    }
  },
})

// Filter customers based on search query
const filterCustomers = () => {
  if (!customerSearchQuery.value || !customerSearchQuery.value.trim()) {
    // Show first 50 when no search query
    filteredCustomerOptions.value = customerOptions.value.slice(0, 50)
    return
  }
  
  const query = customerSearchQuery.value.toLowerCase().trim()
  filteredCustomerOptions.value = customerOptions.value.filter(option => {
    const name = (option.customer_name || '').toLowerCase()
    const code = (option.value || option.name || '').toLowerCase()
    const label = (option.label || '').toLowerCase()
    const matches = name.includes(query) || code.includes(query) || label.includes(query)
    return matches
  }).slice(0, 50) // Limit to 50 results for performance
}

// Handle customer selection
const selectCustomer = (option) => {
  const customerValue = option.value || option.name
  
  emit('update:modelValue', customerValue)
  emit('change', customerValue)
  emit('select', {
    value: customerValue,
    name: customerValue,
    customer_name: option.customer_name,
    customer_group: option.customer_group,
    territory: option.territory,
    customer_primary_address: option.customer_primary_address,
    address_display: option.address_display,
    mobile_no: option.mobile_no,
    email_id: option.email_id,
    tax_id: option.tax_id,
    ...option
  })
  
  customerSearchQuery.value = option.label || `${option.customer_name} (${option.value})`
  showCustomerDropdown.value = false
  sheetOffset.value = 0
}

// Handle input blur - delay to allow click events (desktop only)
const handleCustomerInputBlur = () => {
  if (!isMobile.value) {
    setTimeout(() => {
      showCustomerDropdown.value = false
    }, 200)
  }
}

// Load customers from API
const loadCustomers = async (query = '') => {
  loadingCustomers.value = true
  try {
    let response
    try {
      // Try using the resource first
      response = await customerSearchResource.fetch({ query: query || '', limit: props.limit })
    } catch (resourceError) {
      console.warn('Resource fetch failed, trying direct API call:', resourceError)
      // Fallback to direct API call
      response = await $call(props.apiUrl, {
        query: query || '',
        limit: props.limit
      })
    }
    
    // API returns: {"customers": [...]}
    let payload = []
    if (response) {
      if (Array.isArray(response)) {
        payload = response
      } else if (response.customers && Array.isArray(response.customers)) {
        payload = response.customers
      } else if (response.message) {
        // Frappe might wrap in message
        if (Array.isArray(response.message)) {
          payload = response.message
        } else if (response.message.customers && Array.isArray(response.message.customers)) {
          payload = response.message.customers
        }
      } else if (response.data && Array.isArray(response.data)) {
        payload = response.data
      }
    }
    
    customerOptions.value = payload.map((customer) => {
      const customerName = customer.customer_name || customer.name || ''
      const customerCode = customer.name || customer.customer_id || ''
      return {
        label: `${customerName} (${customerCode})`,
        value: customerCode,
        customer_name: customerName,
        name: customerCode,
        ...customer,
      }
    })
    
    // Initialize filtered options - show first 50
    filterCustomers()
  } catch (error) {
    console.error('Error loading customers:', error)
  } finally {
    loadingCustomers.value = false
  }
}

// Watch for changes to modelValue and update search query
watch(() => props.modelValue, (newValue) => {
  if (!newValue) {
    customerSearchQuery.value = ''
    return
  }
  
  // Find the option
  const option = customerOptions.value.find(opt => opt.value === newValue)
  
  if (option) {
    customerSearchQuery.value = option.label || `${option.customer_name} (${option.value})`
  }
})

// Load customers on mount if autoLoad is true
onMounted(() => {
  detectMobile()
  
  if (props.autoLoad) {
    loadCustomers()
  }
  
  // If modelValue is set, update search query
  if (props.modelValue) {
    const option = customerOptions.value.find(opt => opt.value === props.modelValue)
    if (option) {
      customerSearchQuery.value = option.label || `${option.customer_name} (${option.value})`
    }
  }
  
  // Listen for window resize
  window.addEventListener('resize', () => {
    detectMobile()
  })
  window.addEventListener('orientationchange', () => {
    setTimeout(() => {
      detectMobile()
    }, 300)
  })
  
  // Prevent body scroll when modal is open
  watch(showCustomerDropdown, (isOpen) => {
    if (isMobile.value) {
      if (isOpen) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  })
})

onUnmounted(() => {
  // Cleanup
  document.body.style.overflow = ''
  window.removeEventListener('resize', () => {})
  window.removeEventListener('orientationchange', () => {})
})

// Expose methods for parent components
defineExpose({
  loadCustomers,
  refresh: loadCustomers,
  clear: () => {
    customerSearchQuery.value = ''
    emit('update:modelValue', null)
    emit('change', null)
  }
})
</script>

<style scoped>
/* Desktop dropdown styles */
.customer-dropdown-desktop {
  position: absolute;
  z-index: 50;
  width: 100%;
  margin-top: 4px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  max-height: 60vh;
  overflow-y: auto;
}

/* Mobile Bottom Sheet Modal Styles */
.customer-search-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.customer-search-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

.customer-search-bottom-sheet {
  position: relative;
  width: 100%;
  max-width: 100%;
  background: white;
  border-radius: 24px 24px 0 0;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  touch-action: pan-y;
}

.customer-search-handle {
  padding: 12px 0 8px;
  display: flex;
  justify-content: center;
  cursor: grab;
  touch-action: none;
}

.customer-search-handle:active {
  cursor: grabbing;
}

.customer-search-handle-bar {
  width: 40px;
  height: 4px;
  background: #d1d5db;
  border-radius: 2px;
}

.customer-search-header {
  padding: 0 20px 16px;
  border-bottom: 1px solid #f3f4f6;
}

.customer-search-header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.customer-search-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  flex: 1;
}

.customer-search-close {
  padding: 8px;
  color: #6b7280;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  margin-left: 12px;
}

.customer-search-close:active {
  background: #f3f4f6;
  transform: scale(0.95);
  color: #111827;
}

.customer-search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.customer-search-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  background: #f9fafb;
  transition: all 0.2s;
}

.customer-search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.customer-search-clear {
  position: absolute;
  right: 8px;
  padding: 8px;
  color: #6b7280;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.customer-search-clear:active {
  background: #f3f4f6;
  transform: scale(0.95);
}

.customer-search-results {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 8px 0;
  min-height: 0;
}

.customer-search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.customer-search-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.customer-search-list {
  padding: 0;
}

.customer-search-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: all 0.15s;
  min-height: 56px;
  touch-action: manipulation;
}

.customer-search-item:active {
  background: #f9fafb;
  transform: scale(0.98);
}

.customer-search-item-selected {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
}

.customer-search-item-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.customer-search-item-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.customer-search-item-code {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  letter-spacing: 0.3px;
  line-height: 1.3;
}

.customer-search-item-check {
  width: 24px;
  height: 24px;
  color: #3b82f6;
  flex-shrink: 0;
  margin-left: 12px;
}

/* Bottom Sheet Transition */
.bottom-sheet-enter-active,
.bottom-sheet-leave-active {
  transition: opacity 0.3s ease;
}

.bottom-sheet-enter-active .customer-search-bottom-sheet,
.bottom-sheet-leave-active .customer-search-bottom-sheet {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.bottom-sheet-enter-from {
  opacity: 0;
}

.bottom-sheet-enter-from .customer-search-bottom-sheet {
  transform: translateY(100%);
}

.bottom-sheet-leave-to {
  opacity: 0;
}

.bottom-sheet-leave-to .customer-search-bottom-sheet {
  transform: translateY(100%);
}

/* Mobile optimizations */
@media (max-width: 640px) {
  button, input, select {
    min-height: 44px;
  }
  
  .customer-search-bottom-sheet {
    max-height: 85vh;
  }
}

/* Safe area support for notched devices */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .customer-search-bottom-sheet {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>

