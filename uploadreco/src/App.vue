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
import PWAInstallPrompt from '../../shared/components/PWAInstallPrompt.vue'
import { ensureInScopeManifest } from '../../shared/pwa-manifest'
import PWAUpdatePrompt from '../../shared/components/PWAUpdatePrompt.vue'

const route = useRoute()

const updateManifest = () => {
  ensureInScopeManifest()
}

watch(() => route.name, () => {
  updateManifest()
})

onMounted(() => {
  updateManifest()
})
</script>

<style>
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

@media (max-width: 768px) {
  html {
    scroll-padding-top: 80px;
  }
  
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

