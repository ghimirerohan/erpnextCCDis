<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Unmatched Customers List -->
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
          ⚠️ Unmatched Customers Found ({{ unmatchedCustomers.length }})
        </h3>
        <p class="text-sm text-red-700 mb-4">
          The following outlet codes were not found in the system. These entries will be skipped during creation.
        </p>
        <div class="bg-white rounded-lg p-4 max-h-64 overflow-y-auto">
          <table class="min-w-full">
            <thead class="border-b border-red-200">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-red-800 uppercase">Outlet Code</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-red-800 uppercase">Outlet Name</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-red-100">
              <tr v-for="(customer, index) in unmatchedCustomers" :key="index">
                <td class="px-4 py-2 text-sm font-mono text-red-900">{{ customer.outlet_code }}</td>
                <td class="px-4 py-2 text-sm text-red-900">{{ customer.outlet_name }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="mt-4 text-sm text-red-600 font-medium">
          Please create these customers in the system or remove them from the CSV before proceeding.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  unmatchedCustomers: {
    type: Array,
    required: true
  }
})
</script>

