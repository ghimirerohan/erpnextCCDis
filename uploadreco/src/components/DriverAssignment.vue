<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Driver Assignment Component -->
<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Assign Drivers to Load Sheets</h3>
    <p class="text-sm text-gray-600 mb-6">Select a driver for each load sheet. All load sheets must be assigned before proceeding.</p>
    
    <div class="space-y-4">
      <div v-for="loadsheet in loadsheets" :key="loadsheet" class="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
        <div class="flex-shrink-0 w-32">
          <span class="text-sm font-medium text-gray-700">{{ loadsheet }}</span>
          <span class="block text-xs text-gray-500">{{ getLoadsheetCount(loadsheet) }} customers</span>
        </div>
        
        <div class="flex-grow">
          <select
            v-model="assignments[loadsheet]"
            @change="emitAssignments"
            class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md"
          >
            <option value="">-- Select Driver --</option>
            <option v-for="driver in drivers" :key="driver.name" :value="driver.driver_name">
              {{ driver.driver_name }}
            </option>
          </select>
        </div>
        
        <div class="flex-shrink-0 w-8">
          <svg v-if="assignments[loadsheet]" class="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <svg v-else class="w-6 h-6 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
        </div>
      </div>
    </div>
    
    <div v-if="!allAssigned" class="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
      <div class="flex items-start">
        <svg class="w-5 h-5 text-yellow-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <p class="ml-3 text-sm text-yellow-700">
          Please assign drivers to all {{ unassignedCount }} remaining load sheets before proceeding.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  loadsheets: {
    type: Array,
    required: true
  },
  drivers: {
    type: Array,
    required: true
  },
  groupedData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:assignments', 'validation-changed'])

const assignments = ref({})

// Initialize assignments
watch(() => props.loadsheets, (newLoadsheets) => {
  newLoadsheets.forEach(loadsheet => {
    if (!assignments.value[loadsheet]) {
      assignments.value[loadsheet] = ''
    }
  })
}, { immediate: true })

const allAssigned = computed(() => {
  return props.loadsheets.every(loadsheet => assignments.value[loadsheet])
})

const unassignedCount = computed(() => {
  return props.loadsheets.filter(loadsheet => !assignments.value[loadsheet]).length
})

const getLoadsheetCount = (loadsheet) => {
  return props.groupedData[loadsheet]?.length || 0
}

const emitAssignments = () => {
  emit('update:assignments', assignments.value)
  emit('validation-changed', allAssigned.value)
}

// Watch for changes and emit
watch(allAssigned, (isValid) => {
  emit('validation-changed', isValid)
})
</script>

