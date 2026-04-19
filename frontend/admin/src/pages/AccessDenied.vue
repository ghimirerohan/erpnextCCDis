<template>
  <div class="mx-auto max-w-md space-y-4 p-6">
    <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ __('Access denied') }}</h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      {{
        __(
          'Your account does not have the CC Admin (or System Manager) role required for this app.',
        )
      }}
    </p>
    <Button variant="outline" @click="goField">{{ __('Open Field App') }}</Button>
    <Button class="ml-2" variant="outline" @click="goDesk">{{ __('Open Desk') }}</Button>
  </div>
</template>

<script setup>
import { Button } from 'frappe-ui'

function goField() {
	window.location.href = '/field-app'
}

function goDesk() {
	window.location.href = '/app'
}
</script>
