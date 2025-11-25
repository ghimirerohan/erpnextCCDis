<template>
  <div v-if="needRefresh" class="fixed top-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50">
    <div class="flex items-start gap-3">
      <div class="flex-shrink-0">
        <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-semibold text-gray-900 mb-1">
          Update Available
        </h3>
        <p class="text-sm text-gray-600 mb-3">
          A new version is available. Reload to update?
        </p>
        <div class="flex gap-2">
          <button
            @click="updateApp"
            class="px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-md hover:bg-green-600 transition-colors"
          >
            Reload Now
          </button>
          <button
            @click="close"
            class="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
          >
            Later
          </button>
        </div>
      </div>
      <button
        @click="close"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>

  <div v-if="offlineReady" class="fixed top-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50">
    <div class="flex items-start gap-3">
      <div class="flex-shrink-0">
        <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-semibold text-gray-900 mb-1">
          Ready to work offline
        </h3>
        <p class="text-sm text-gray-600">
          The app is now available offline
        </p>
      </div>
      <button
        @click="closeOffline"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const needRefresh = ref(false)
const offlineReady = ref(false)
let updateSWCallback = null

onMounted(() => {
  // This will be set by the main.js when registering the service worker
  // We expose a global function to communicate with this component
  window.__onSWNeedRefresh = (callback) => {
    needRefresh.value = true
    updateSWCallback = callback
  }

  window.__onSWOfflineReady = () => {
    offlineReady.value = true
    // Auto-hide after 5 seconds
    setTimeout(() => {
      offlineReady.value = false
    }, 5000)
  }
})

function updateApp() {
  if (updateSWCallback) {
    updateSWCallback(true)
  }
}

function close() {
  needRefresh.value = false
}

function closeOffline() {
  offlineReady.value = false
}
</script>

