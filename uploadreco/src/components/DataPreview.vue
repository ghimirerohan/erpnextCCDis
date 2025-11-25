<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Data Preview Table -->
<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
    <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
      <h3 class="text-lg font-semibold text-gray-900">CSV Data Preview</h3>
      <p class="text-sm text-gray-600">{{ parsedRows.length }} rows • {{ Object.keys(groupedByLoadsheet).length }} load sheets</p>
    </div>
    
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Outlet Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Outlet Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Load Sheet</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Salesman</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(row, index) in displayRows" :key="index" :class="{ 'bg-red-50': !row.customer_exists }">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">{{ row.outlet_code }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ row.outlet_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ row.reference_no }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ row.salesman_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium">{{ formatCurrency(row.amount) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center">
              <span v-if="row.customer_exists" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                Valid
              </span>
              <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                Not Found
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="parsedRows.length > 10" class="px-6 py-4 border-t border-gray-200 bg-gray-50 text-center">
      <button
        @click="showAll = !showAll"
        class="text-sm text-purple-600 hover:text-purple-700 font-medium"
      >
        {{ showAll ? 'Show Less' : `Show All ${parsedRows.length} Rows` }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  parsedRows: {
    type: Array,
    required: true
  },
  groupedByLoadsheet: {
    type: Object,
    required: true
  }
})

const showAll = ref(false)

const displayRows = computed(() => {
  return showAll.value ? props.parsedRows : props.parsedRows.slice(0, 10)
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount)
}
</script>

