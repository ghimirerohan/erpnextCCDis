<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <div class="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg mr-3">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Preview</h2>
          <p class="text-sm text-gray-600">First {{ previewData.length }} rows • Total {{ totalInvoices }} invoices</p>
        </div>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Is Return</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Date</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Invoice ID</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Customer</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Item Code</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Quantity</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Discount</th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Item Name</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(row, index) in previewData" :key="index" :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'">
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Is Return (Credit Note)'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Date'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ row['ID'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Customer'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Item (Items)'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Quantity (Items)'] || '' }}</td>
            <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-900">{{ row['Distributed Discount Amount (Items)'] || '' }}</td>
            <td class="px-3 py-4 text-sm text-gray-900">{{ row['Item Name (Items)'] || '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <p class="text-sm text-blue-800">
        <svg class="inline w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
        </svg>
        This is a preview of the transformed data. Please review before starting the import.
      </p>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
defineProps({
  previewData: {
    type: Array,
    default: () => []
  },
  totalInvoices: {
    type: Number,
    default: 0
  }
})
</script>

