<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex flex-col items-center justify-center py-12">
      <!-- Loading Spinner -->
      <div class="flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-6">
        <svg class="w-8 h-8 text-indigo-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
      </div>
      
      <!-- Loading Message -->
      <h2 class="text-2xl font-semibold text-gray-900 mb-2">Importing Sales Invoices</h2>
      <p class="text-gray-600 text-center max-w-md">
        Please wait while we process your sales invoice data. This may take a few minutes depending on the number of invoices.
      </p>
      
      <!-- Loading Dots Animation -->
      <div class="flex space-x-1 mt-6">
        <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
        <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES - Simplified progress panel
// No props needed for simplified version
</script>

