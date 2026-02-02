<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Unmatched Customers List with Create Option -->
<template>
  <div v-if="unmatchedCustomers.length > 0" class="bg-red-50 border-l-4 border-red-400 p-6 rounded-lg">
    <div class="flex items-start">
      <div class="flex-shrink-0">
        <svg class="h-6 w-6 text-red-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
        </svg>
      </div>
      <div class="ml-3 flex-1">
        <h3 class="text-lg font-semibold text-red-800 mb-3">
          ⚠️ Unmatched Customers Found ({{ remainingUnmatched.length }})
        </h3>
        <p class="text-sm text-red-700 mb-4">
          The following outlet codes were not found in the system. You must create these customers before proceeding.
        </p>

        <!-- Success message for created customers -->
        <div v-if="props.createdCustomers.length > 0" class="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 class="text-sm font-semibold text-green-800 mb-2 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            Created Customers ({{ props.createdCustomers.length }})
          </h4>
          <div class="flex flex-wrap gap-2">
            <span v-for="customer in props.createdCustomers" :key="customer.outlet_code" 
                  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              {{ customer.outlet_code }} - {{ customer.outlet_name }}
            </span>
          </div>
        </div>

        <!-- Unmatched customers list -->
        <div class="space-y-4">
          <div v-for="(customer, index) in remainingUnmatched" :key="customer.outlet_code"
               class="bg-white rounded-lg p-4 border border-red-200 shadow-sm">
            
            <!-- Customer Header -->
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-gray-200">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <span class="text-red-600 font-bold text-sm">{{ index + 1 }}</span>
                </div>
                <div>
                  <div class="flex items-center space-x-2">
                    <span class="font-mono text-sm bg-gray-100 px-2 py-0.5 rounded">{{ customer.outlet_code }}</span>
                    <span class="text-gray-800 font-medium">{{ customer.outlet_name }}</span>
                  </div>
                  <p class="text-xs text-gray-500 mt-0.5">Create this customer to continue</p>
                </div>
              </div>
              <button
                v-if="!customerForms[customer.outlet_code]?.expanded"
                @click="expandForm(customer.outlet_code)"
                class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-purple-600 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Create Customer
              </button>
              <button
                v-else
                @click="collapseForm(customer.outlet_code)"
                class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                Cancel
              </button>
            </div>

            <!-- Creation Form (Expandable) -->
            <div v-if="customerForms[customer.outlet_code]?.expanded" class="space-y-4">
              <!-- Read-only fields -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Outlet Code (ID)</label>
                  <input
                    type="text"
                    :value="customer.outlet_code"
                    disabled
                    class="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-lg text-sm text-gray-700 cursor-not-allowed"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Customer Name</label>
                  <input
                    type="text"
                    :value="customer.outlet_name"
                    disabled
                    class="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-lg text-sm text-gray-700 cursor-not-allowed"
                  />
                </div>
              </div>

              <!-- Editable fields -->
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <!-- Territory -->
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">
                    Territory <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="customerForms[customer.outlet_code].territory"
                    :class="[
                      'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500',
                      customerForms[customer.outlet_code]?.errors?.territory ? 'border-red-500 bg-red-50' : 'border-gray-300'
                    ]"
                    @change="clearError(customer.outlet_code, 'territory')"
                  >
                    <option value="">Select Territory</option>
                    <option v-for="territory in territories" :key="territory.name" :value="territory.name">
                      {{ territory.name }}
                    </option>
                  </select>
                  <p v-if="customerForms[customer.outlet_code]?.errors?.territory" class="mt-1 text-xs text-red-600">
                    {{ customerForms[customer.outlet_code].errors.territory }}
                  </p>
                </div>

                <!-- Tax ID -->
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">
                    Tax ID / PAN <span v-if="!isPadmashree" class="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    v-model="customerForms[customer.outlet_code].tax_id"
                    :placeholder="isPadmashree ? 'Enter Tax ID (optional)' : 'Enter Tax ID'"
                    :class="[
                      'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500',
                      customerForms[customer.outlet_code]?.errors?.tax_id ? 'border-red-500 bg-red-50' : 'border-gray-300'
                    ]"
                    @input="clearError(customer.outlet_code, 'tax_id')"
                  />
                  <p v-if="customerForms[customer.outlet_code]?.errors?.tax_id" class="mt-1 text-xs text-red-600">
                    {{ customerForms[customer.outlet_code].errors.tax_id }}
                  </p>
                </div>

                <!-- Phone Number -->
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">
                    Phone Number <span v-if="!isPadmashree" class="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    v-model="customerForms[customer.outlet_code].phone_number"
                    :placeholder="isPadmashree ? '10 digit number (optional)' : '10 digit number'"
                    maxlength="10"
                    :class="[
                      'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500',
                      customerForms[customer.outlet_code]?.errors?.phone_number ? 'border-red-500 bg-red-50' : 'border-gray-300'
                    ]"
                    @input="handlePhoneInput(customer.outlet_code, $event)"
                  />
                  <p v-if="customerForms[customer.outlet_code]?.errors?.phone_number" class="mt-1 text-xs text-red-600">
                    {{ customerForms[customer.outlet_code].errors.phone_number }}
                  </p>
                  <p v-else class="mt-1 text-xs text-gray-500">
                    {{ getPhoneDigitCount(customer.outlet_code) }}/10 digits
                  </p>
                </div>
              </div>

              <!-- Padmashree-specific fields -->
              <template v-if="isPadmashree">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <!-- Shipping Address (prefilled from CSV) -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Shipping Address</label>
                    <input
                      type="text"
                      v-model="customerForms[customer.outlet_code].shipping_address"
                      placeholder="Shipping address"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <!-- Area (prefilled from CSV) -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Area</label>
                    <input
                      type="text"
                      v-model="customerForms[customer.outlet_code].area"
                      placeholder="Area"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </template>

              <!-- Info about customer type -->
              <div :class="isPadmashree ? 'bg-blue-50 border-blue-200' : 'bg-blue-50 border-blue-200'" class="border rounded-lg p-3">
                <p class="text-xs" :class="isPadmashree ? 'text-blue-700' : 'text-blue-700'">
                  <span class="font-medium">Note:</span> Customer will be created as <span class="font-semibold">Company</span> type with 
                  <span class="font-semibold">{{ isPadmashree ? 'Horlicks' : 'Commercial' }}</span> customer group.
                </p>
              </div>

              <!-- Save Button -->
              <div class="flex justify-end pt-2">
                <button
                  @click="createCustomer(customer)"
                  :disabled="customerForms[customer.outlet_code]?.saving"
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg v-if="customerForms[customer.outlet_code]?.saving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  {{ customerForms[customer.outlet_code]?.saving ? 'Creating...' : 'Create Customer' }}
                </button>
              </div>

              <!-- Error message -->
              <div v-if="customerForms[customer.outlet_code]?.error" class="bg-red-100 border border-red-300 rounded-lg p-3">
                <p class="text-sm text-red-700">{{ customerForms[customer.outlet_code].error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- All customers created message -->
        <div v-if="remainingUnmatched.length === 0 && props.createdCustomers.length > 0" 
             class="bg-green-100 border border-green-300 rounded-lg p-4 mt-4">
          <div class="flex items-center">
            <svg class="w-6 h-6 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            <div>
              <h4 class="text-sm font-semibold text-green-800">All Customers Created!</h4>
              <p class="text-xs text-green-700 mt-0.5">All {{ props.createdCustomers.length }} customers have been created. You can now proceed with the reconciliation.</p>
            </div>
          </div>
        </div>

        <!-- Warning message when customers remain -->
        <p v-if="remainingUnmatched.length > 0" class="mt-4 text-sm text-red-600 font-medium flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          Please create all {{ remainingUnmatched.length }} remaining customer(s) before proceeding.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  unmatchedCustomers: {
    type: Array,
    required: true
  },
  createdCustomers: {
    type: Array,
    default: () => []
  },
  company: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['customer-created', 'all-customers-created'])

// Computed
const isPadmashree = computed(() => props.company === 'PadmaShree Trade Link')

// State
const territories = ref([])
const loadingTerritories = ref(false)
const customerForms = reactive({})

// Computed - use prop from parent for created customers
const remainingUnmatched = computed(() => {
  return props.unmatchedCustomers.filter(
    customer => !props.createdCustomers.some(c => c.outlet_code === customer.outlet_code)
  )
})

// Methods
const loadTerritories = async () => {
  loadingTerritories.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.get_territories_list')
    if (response.success) {
      territories.value = response.data
    } else {
      console.error('Error loading territories:', response.message)
    }
  } catch (error) {
    console.error('Error loading territories:', error)
  } finally {
    loadingTerritories.value = false
  }
}

const initializeForm = (outletCode) => {
  if (!customerForms[outletCode]) {
    // Find customer data for prefilling
    const customer = props.unmatchedCustomers.find(c => c.outlet_code === outletCode)
    
    customerForms[outletCode] = {
      expanded: false,
      territory: '',
      // Prefill tax_id from CSV (pan field for Padmashree)
      tax_id: customer?.pan || '',
      phone_number: '',
      // Padmashree-specific fields (prefilled from CSV)
      shipping_address: customer?.shipping_address || '',
      area: customer?.area || '',
      saving: false,
      error: null,
      errors: {}
    }
  }
}

const expandForm = (outletCode) => {
  initializeForm(outletCode)
  customerForms[outletCode].expanded = true
}

const collapseForm = (outletCode) => {
  if (customerForms[outletCode]) {
    customerForms[outletCode].expanded = false
    customerForms[outletCode].error = null
    customerForms[outletCode].errors = {}
  }
}

const clearError = (outletCode, field) => {
  if (customerForms[outletCode]?.errors) {
    delete customerForms[outletCode].errors[field]
  }
}

// Handle phone input - only allow digits
const handlePhoneInput = (outletCode, event) => {
  const form = customerForms[outletCode]
  if (form) {
    // Remove non-digits and limit to 10
    const digitsOnly = event.target.value.replace(/\D/g, '').slice(0, 10)
    form.phone_number = digitsOnly
    clearError(outletCode, 'phone_number')
  }
}

// Get phone digit count for display
const getPhoneDigitCount = (outletCode) => {
  const form = customerForms[outletCode]
  if (form && form.phone_number) {
    return form.phone_number.replace(/\D/g, '').length
  }
  return 0
}

const validateForm = (outletCode) => {
  const form = customerForms[outletCode]
  const errors = {}

  if (!form.territory) {
    errors.territory = 'Territory is required'
  }
  
  // For Riya, Tax ID is required; for Padmashree, it's optional
  if (!isPadmashree.value && (!form.tax_id || !form.tax_id.trim())) {
    errors.tax_id = 'Tax ID is required'
  }
  
  // Phone number validation
  // For Riya: required and must be exactly 10 digits
  // For Padmashree: optional, but if provided must be 10 digits
  const phoneDigits = (form.phone_number || '').replace(/\D/g, '')
  if (isPadmashree.value) {
    // Optional for Padmashree, but validate if provided
    if (phoneDigits && phoneDigits.length !== 10) {
      errors.phone_number = `Phone Number must be exactly 10 digits (currently ${phoneDigits.length})`
    }
  } else {
    // Required for Riya
    if (!phoneDigits) {
      errors.phone_number = 'Phone Number is required'
    } else if (phoneDigits.length !== 10) {
      errors.phone_number = `Phone Number must be exactly 10 digits (currently ${phoneDigits.length})`
    }
  }

  form.errors = errors
  return Object.keys(errors).length === 0
}

const createCustomer = async (customer) => {
  const outletCode = customer.outlet_code
  initializeForm(outletCode)
  
  if (!validateForm(outletCode)) {
    return
  }

  const form = customerForms[outletCode]
  form.saving = true
  form.error = null

  try {
    let response
    
    if (isPadmashree.value) {
      // Use Padmashree API with Horlicks customer group
      response = await call('custom_erp.api.payment_reco.create_customer_from_csv_padmashree', {
        outlet_code: customer.outlet_code,
        outlet_name: customer.outlet_name,
        territory: form.territory,
        tax_id: (form.tax_id || '').trim(),
        phone_number: (form.phone_number || '').trim(),
        shipping_address: (form.shipping_address || '').trim(),
        area: (form.area || '').trim()
      })
    } else {
      // Use Riya API with Commercial customer group
      response = await call('custom_erp.api.payment_reco.create_customer_from_csv', {
        outlet_code: customer.outlet_code,
        outlet_name: customer.outlet_name,
        territory: form.territory,
        tax_id: form.tax_id.trim(),
        phone_number: form.phone_number.trim()
      })
    }

    if (response.success) {
      // Emit event to parent - parent manages the created customers list
      emit('customer-created', {
        outlet_code: customer.outlet_code,
        outlet_name: customer.outlet_name,
        name: response.data.name
      })

      // Check if all customers are created (using nextTick to wait for prop update)
      // The parent will add to createdCustomers, which updates remainingUnmatched
      setTimeout(() => {
        // After the customer is added to props.createdCustomers by parent,
        // remainingUnmatched will be recomputed
        if (remainingUnmatched.value.length === 0) {
          emit('all-customers-created')
        }
      }, 100)

      // Collapse form after successful creation
      form.expanded = false
    } else {
      form.error = response.message
    }
  } catch (error) {
    console.error('Error creating customer:', error)
    form.error = error.message || 'Failed to create customer'
  } finally {
    form.saving = false
  }
}

// Initialize forms for all unmatched customers
const initializeForms = () => {
  props.unmatchedCustomers.forEach(customer => {
    initializeForm(customer.outlet_code)
  })
}

// Lifecycle
onMounted(() => {
  loadTerritories()
  initializeForms()
})
</script>
