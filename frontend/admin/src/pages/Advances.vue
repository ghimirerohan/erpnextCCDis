<template>
  <div class="grid gap-6 lg:grid-cols-2">
    <div class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
      <h2 class="mb-3 text-lg font-medium text-gray-900 dark:text-white">{{ __('Give advance') }}</h2>
      <FormControl v-model="employee" type="text" :label="__('Employee ID')" class="mb-3" />
      <FormControl v-model="amount" type="number" :label="__('Amount')" class="mb-3" />
      <FormControl v-model="remarks" type="textarea" :label="__('Remarks')" class="mb-3" />
      <Button :loading="give.loading" class="w-full" @click="submitGive">{{ __('Submit') }}</Button>
      <p v-if="give.error" class="mt-2 text-sm text-red-600">{{ give.error?.message || give.error }}</p>
    </div>

    <div class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
      <div class="mb-3 flex items-center justify-between">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white">{{ __('Outstanding') }}</h2>
        <Button variant="outline" size="sm" @click="summary.reload()">{{ __('Refresh') }}</Button>
      </div>
      <div v-if="summary.loading" class="text-sm text-gray-500">{{ __('Loading…') }}</div>
      <p v-else-if="summary.error" class="text-sm text-red-600">{{ summary.error?.message || summary.error }}</p>
      <template v-else-if="summary.data">
        <p class="mb-2 text-sm font-semibold text-gray-900 dark:text-white">
          {{ __('Total outstanding') }}: {{ fmtNPR(summary.data.total_outstanding) }}
        </p>
        <ul class="max-h-[28rem] divide-y divide-gray-100 overflow-y-auto text-sm dark:divide-gray-800">
          <li v-for="a in summary.data.advances" :key="a.name" class="py-2">
            <p class="font-medium text-gray-900 dark:text-white">{{ a.employee_name || a.employee }}</p>
            <p class="text-xs text-gray-500">{{ a.status }} · {{ fmtDate(a.advance_date) }}</p>
            <p class="tabular-nums text-gray-900 dark:text-white">{{ fmtNPR(a.balance) }}</p>
          </li>
          <li v-if="!summary.data.advances?.length" class="py-4 text-gray-500">{{ __('None') }}</li>
        </ul>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, FormControl, toast } from 'frappe-ui'
import { fmtNPR, fmtDate } from '@shared/utils'

const employee = ref('')
const amount = ref('')
const remarks = ref('')

const summary = createResource({
	url: 'custom_erp.api.admin.get_advances_summary',
	auto: true,
})

const give = createResource({
	url: 'custom_erp.api.admin.give_advance',
	auto: false,
	onSuccess() {
		toast.success(__('Advance recorded'))
		employee.value = ''
		amount.value = ''
		remarks.value = ''
		summary.reload()
	},
	onError(e) {
		toast.error(e.message || __('Failed'))
	},
})

function submitGive() {
	give.submit({
		employee: employee.value,
		amount: parseFloat(amount.value),
		remarks: remarks.value || undefined,
	})
}
</script>
