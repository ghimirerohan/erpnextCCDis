<template>
  <div class="app-container">
    <router-view />
    <PWAInstallPrompt />
    <PWAUpdatePrompt />
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import PWAInstallPrompt from './components/PWAInstallPrompt.vue'
import PWAUpdatePrompt from './components/PWAUpdatePrompt.vue'

// Update manifest link when route changes
const route = useRoute()

const updateManifest = () => {
  const manifestMap = {
    'Home': '/manifest-home.json',
    'QRPay': '/manifest-qrpay.json',
    'QRPayAdmin': '/manifest-qrpay-admin.json',
    'Scanner': '/manifest-scanner.json',
    'PayDashboard': '/manifest-pay-dashboard.json',
    'UploadSales': '/manifest-uploadsales.json',
  }
  
  // Get manifest path based on route name
  const manifestPath = manifestMap[route.name] || '/manifest-home.json'
  
  // Remove all existing manifest links
  const existingLinks = document.querySelectorAll('link[rel="manifest"]')
  existingLinks.forEach(link => link.remove())
  
  // Add new manifest link
  const link = document.createElement('link')
  link.rel = 'manifest'
  link.href = manifestPath
  document.head.appendChild(link)
  
  // Update theme color meta tag based on route
  const themeColors = {
    'Home': '#3b82f6',
    'QRPay': '#10b981',
    'QRPayAdmin': '#2563eb',
    'Scanner': '#7c3aed',
    'PayDashboard': '#2563eb',
    'UploadSales': '#059669',
  }
  
  let themeMeta = document.querySelector('meta[name="theme-color"]')
  if (!themeMeta) {
    themeMeta = document.createElement('meta')
    themeMeta.name = 'theme-color'
    document.head.appendChild(themeMeta)
  }
  themeMeta.content = themeColors[route.name] || '#3b82f6'
}

watch(() => route.name, () => {
  updateManifest()
})

onMounted(() => {
  updateManifest()
  
  // Log current PWA manifest for debugging
  const manifestLink = document.querySelector('link[rel="manifest"]')
  if (manifestLink) {
    console.log(`📱 PWA Manifest loaded: ${manifestLink.href} for route: ${route.name}`)
    console.log(`📱 PWA Scope will be: /jsapp/${route.path === '/' ? '' : route.path.replace(/^\//, '')}/`)
  }
})
</script>

<style>
/* Global mobile optimizations */
html {
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
}

body {
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

/* Prevent layout shifts on mobile */
@media (max-width: 768px) {
  html {
    scroll-padding-top: 80px;
  }
  
  /* Prevent iOS zoom on input focus */
  input[type="text"],
  input[type="number"],
  input[type="email"],
  input[type="tel"],
  input[type="search"],
  select,
  textarea {
    font-size: 16px !important;
  }
}
</style>
