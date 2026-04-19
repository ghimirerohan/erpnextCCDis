<template>
  <FrappeUIProvider>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950">
    <nav class="sticky top-0 z-10 flex flex-wrap items-center gap-4 border-b bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-900 sm:px-6">
      <span class="text-base font-semibold text-gray-900 dark:text-white">CC Admin</span>
      <div class="ml-0 flex flex-wrap gap-2 sm:ml-4">
        <router-link
          v-for="tab in tabs"
          :key="tab.to"
          :to="tab.to"
          class="rounded-md px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
          active-class="bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300"
        >
          {{ __(tab.label) }}
        </router-link>
      </div>
    </nav>
    <main class="p-4 sm:p-6">
      <router-view />
    </main>
  </div>
  </FrappeUIProvider>
</template>

<script setup>
import { FrappeUIProvider } from 'frappe-ui'

const tabs = [
	{ to: '/', label: 'Field Summary' },
	{ to: '/register', label: 'Cash Register' },
	{ to: '/advances', label: 'Advances' },
]
</script>
