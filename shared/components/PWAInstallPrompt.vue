<template>
  <div
    v-if="showBanner"
    class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white border border-gray-200 rounded-xl shadow-lg p-4 z-50"
  >
    <div class="flex items-start gap-3">
      <div class="flex-shrink-0">
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <h3 class="text-sm font-semibold text-gray-900 mb-1">
          Install {{ appName }}
        </h3>
        <p class="text-sm text-gray-600 mb-3">
          <template v-if="isIos">
            Open the Share menu, then tap <span class="font-medium">Add to Home Screen</span> for a full-screen app.
          </template>
          <template v-else>
            Install {{ appName }} on this device for a native-like app with home-screen launch.
          </template>
        </p>
        <div class="flex gap-2">
          <button
            v-if="!isIos"
            @click="install"
            class="px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-md hover:bg-blue-600 transition-colors"
          >
            Install
          </button>
          <button
            @click="dismiss"
            class="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
          >
            {{ isIos ? 'Got it' : 'Not now' }}
          </button>
        </div>
      </div>
      <button
        @click="dismiss"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
        aria-label="Dismiss"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { getSpaAppName } from '../pwa-manifest'

const APP_LABELS = {
  Home: 'Custom ERP',
  QRPay: 'QRPay',
  QRPayAdmin: 'QRPay Admin',
  Scanner: 'Scanner',
  PayDashboard: 'Pay Dashboard',
  UploadSales: 'Upload Sales',
  qrpay: 'QRPay',
  'qrpay-horlicks': 'QRPay Horlicks',
  'qrpay-admin': 'QRPay Admin',
  scanner: 'Scanner',
  'pay-dashboard': 'Pay Dashboard',
  uploadsales: 'Upload Sales',
  uploadreco: 'Upload Reco',
  dailyrecoentry: 'Daily Reco',
  dailytrnxs: 'Daily Transactions',
  home: 'Home',
  testlogin: 'Test Login',
  'ai-assistant': 'Bidhi',
  'emp-attendance': 'Attendance',
}

const showBanner = ref(false)
const deferredPrompt = ref(null)
const isIos = ref(false)

const appName = computed(() => {
  const spa = getSpaAppName()
  return APP_LABELS[spa] || 'App'
})

function isStandalone() {
  return (
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true
  )
}

function capturePrompt(e) {
  const promptEvent = e.type === 'pwa-install-available' ? e.detail : e
  if (promptEvent && typeof promptEvent.preventDefault === 'function') {
    promptEvent.preventDefault()
  }
  if (promptEvent && typeof promptEvent.prompt === 'function') {
    deferredPrompt.value = promptEvent
    showBanner.value = true
  }
}

function onInstalled() {
  showBanner.value = false
  deferredPrompt.value = null
}

onMounted(() => {
  if (isStandalone()) return

  const ua = window.navigator.userAgent || ''
  isIos.value = /iphone|ipad|ipod/i.test(ua) && !window.MSStream

  window.addEventListener('beforeinstallprompt', capturePrompt)
  window.addEventListener('appinstalled', onInstalled)
  window.addEventListener('pwa-install-available', capturePrompt)

  if (isIos.value && !sessionStorage.getItem('pwa-ios-hint-dismissed')) {
    showBanner.value = true
  }
})

onUnmounted(() => {
  window.removeEventListener('beforeinstallprompt', capturePrompt)
  window.removeEventListener('appinstalled', onInstalled)
  window.removeEventListener('pwa-install-available', capturePrompt)
})

async function install() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  await deferredPrompt.value.userChoice
  deferredPrompt.value = null
  showBanner.value = false
}

function dismiss() {
  showBanner.value = false
  if (isIos.value) {
    sessionStorage.setItem('pwa-ios-hint-dismissed', '1')
  }
}
</script>
