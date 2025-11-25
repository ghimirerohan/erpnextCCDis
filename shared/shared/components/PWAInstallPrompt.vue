<template>
  <div v-if="showInstallPrompt" class="fixed bottom-4 left-4 right-4 md:left-auto md:w-96 bg-white border border-gray-200 rounded-lg shadow-lg p-4 z-50">
    <div class="flex items-start gap-3">
      <div class="flex-shrink-0">
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-semibold text-gray-900 mb-1">
          Install {{ appName }}
        </h3>
        <p class="text-sm text-gray-600 mb-3">
          Install {{ appName }} as an app for quick access and better experience
        </p>
        <div class="flex gap-2">
          <button
            @click="install"
            class="px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-md hover:bg-blue-600 transition-colors"
          >
            Install
          </button>
          <button
            @click="dismiss"
            class="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
          >
            Not now
          </button>
        </div>
      </div>
      <button
        @click="dismiss"
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
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showInstallPrompt = ref(false)
const deferredPrompt = ref(null)

// Get app name based on current route
const appName = computed(() => {
  const nameMap = {
    'Home': 'Custom ERP',
    'QRPay': 'QRPay',
    'QRPayAdmin': 'QRPay Admin',
    'Scanner': 'Scanner',
    'PayDashboard': 'Pay Dashboard',
    'UploadSales': 'Upload Sales',
  }
  return nameMap[route.name] || 'App'
})

onMounted(() => {
  // Listen for the beforeinstallprompt event
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault()
    // Save the event so it can be triggered later
    deferredPrompt.value = e
    // Show the install prompt
    showInstallPrompt.value = true
  })

  // Listen for the appinstalled event
  window.addEventListener('appinstalled', () => {
    console.log('PWA was installed')
    showInstallPrompt.value = false
    deferredPrompt.value = null
  })

  // Check if app is already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    // App is already installed
    showInstallPrompt.value = false
  }
})

async function install() {
  if (!deferredPrompt.value) {
    return
  }

  // Show the install prompt
  deferredPrompt.value.prompt()

  // Wait for the user to respond to the prompt
  const { outcome } = await deferredPrompt.value.userChoice

  console.log(`User response to install prompt: ${outcome}`)

  // Clear the deferredPrompt
  deferredPrompt.value = null
  showInstallPrompt.value = false
}

function dismiss() {
  showInstallPrompt.value = false
}
</script>

