<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <h1 class="text-xl font-semibold text-gray-900 dark:text-white">{{ __('Field Collections Today') }}</h1>
      <Button variant="outline" @click="summary.reload()">{{ __('Refresh') }}</Button>
    </div>

    <div v-if="summary.error" class="rounded-lg bg-red-50 p-4 text-sm text-red-800 dark:bg-red-950 dark:text-red-200">
      {{ summary.error?.messages?.[0] || summary.error?.message || summary.error }}
    </div>

    <div v-if="summary.loading" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 4" :key="i" class="h-40 animate-pulse rounded-xl bg-gray-200 dark:bg-gray-800" />
    </div>

    <div v-else-if="summary.data" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="emp in summary.data.employees"
        :key="emp.employee"
        class="cursor-pointer rounded-xl bg-white p-5 shadow-sm ring-1 ring-gray-200 transition hover:ring-blue-300 dark:bg-gray-900 dark:ring-gray-700 dark:hover:ring-blue-700"
        @click="$router.push(`/employee/${emp.employee}`)"
      >
        <div class="flex items-start justify-between gap-2">
          <div>
            <p class="font-medium text-gray-900 dark:text-white">{{ emp.employee_name }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ emp.transaction_count }} {{ __('transactions') }}</p>
          </div>
          <span class="text-lg font-bold tabular-nums text-gray-900 dark:text-white">
            {{ fmtNPR(emp.total_collected) }}
          </span>
        </div>
        <div class="mt-3 flex flex-wrap gap-2">
          <div v-for="(amt, mode) in emp.mode_totals" :key="mode" class="flex items-center gap-1 text-xs">
            <Badge :label="mode" :theme="modeColor(mode)" size="sm" />
            <span class="font-medium tabular-nums">{{ fmtNPR(amt) }}</span>
          </div>
        </div>
        <div v-if="emp.expected_total != null" class="mt-3 border-t border-gray-100 pt-3 dark:border-gray-800">
          <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{{ __('Reco net expected') }}</span>
            <span>{{ fmtNPR(emp.expected_total) }}</span>
          </div>
          <div
            class="mt-1 flex justify-between text-xs"
            :class="emp.total_collected >= emp.expected_total ? 'text-green-600 dark:text-green-400' : 'text-orange-600 dark:text-orange-400'"
          >
            <span>{{ __('Variance') }}</span>
            <span class="tabular-nums">{{ fmtNPR(emp.total_collected - emp.expected_total) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, inject } from 'vue'
import { createResource, Button, Badge } from 'frappe-ui'
import { fmtNPR, MODE_COLORS } from '@shared/utils'

const socket = inject('$socket')

const summary = createResource({
	url: 'custom_erp.api.admin.get_field_summary',
	auto: true,
	cache: 'admin-field-summary',
})

function modeColor(mode) {
	return MODE_COLORS[mode] || 'gray'
}

function reloadSummary() {
	summary.reload()
}

onMounted(() => {
	socket?.on('ccdis:field_payment_submitted', reloadSummary)
	socket?.on('ccdis:erp_payment_submitted', reloadSummary)
})
onUnmounted(() => {
	socket?.off('ccdis:field_payment_submitted', reloadSummary)
	socket?.off('ccdis:erp_payment_submitted', reloadSummary)
})
</script>
