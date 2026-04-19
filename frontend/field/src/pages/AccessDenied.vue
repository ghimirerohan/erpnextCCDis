<template>
  <div class="mx-auto max-w-md space-y-4 p-6">
    <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ __('Access denied') }}</h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      {{
        __(
          'Your account does not have the Field User (or supervisor) role required for this app. Ask an administrator to assign the correct role.',
        )
      }}
    </p>
    <Button variant="outline" @click="goDesk">{{ __('Open Desk') }}</Button>
  </div>
</template>

<script setup>
import { Button } from 'frappe-ui'

function goDesk() {
	window.location.href = '/app'
}
</script>
