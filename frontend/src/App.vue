<template>
  <div>
    <router-view />
    <PWAInstallPrompt />
    <PWAUpdatePrompt />
  </div>
</template>

<script setup>
import PWAInstallPrompt from './components/PWAInstallPrompt.vue'
import PWAUpdatePrompt from './components/PWAUpdatePrompt.vue'
</script>
