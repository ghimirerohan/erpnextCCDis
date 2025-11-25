<template>
  <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 shadow-lg flex flex-col items-center space-y-2">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="text-gray-700 font-medium">Verifying Payment...</p>
    </div>
  </div>
</template>

<script setup>
// ADDED BY AI: FONEPAY LIVE SOCKET - Loading overlay component for payment verification
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>

