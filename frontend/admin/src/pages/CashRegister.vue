<template>
  <div class="space-y-6">
    <h1 class="text-xl font-semibold text-gray-900 dark:text-white">{{ __('Cash register') }}</h1>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <p class="mb-3 text-sm font-medium text-gray-900 dark:text-white">{{ __('Add entry') }}</p>
        <label class="mb-1 block text-xs text-gray-500">{{ __('Entry type') }}</label>
        <select v-model="entryType" class="mb-3 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-950 dark:text-white">
          <option value="In">In</option>
          <option value="Out">Out</option>
        </select>
        <label class="mb-1 block text-xs text-gray-500">{{ __('Topic') }}</label>
        <select v-model="topic" class="mb-3 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-950 dark:text-white">
          <option v-for="t in topics" :key="t" :value="t">{{ t }}</option>
        </select>
        <label class="mb-1 block text-xs text-gray-500">{{ __('Payment mode') }}</label>
        <select v-model="paymentMode" class="mb-3 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-950 dark:text-white">
          <option v-for="m in payModes" :key="m" :value="m">{{ m }}</option>
        </select>
        <FormControl v-model="amount" type="number" :label="__('Amount')" class="mb-3" />
        <FormControl v-model="employeeRef" type="text" :label="__('Employee (name, optional)')" class="mb-3" />
        <FormControl v-model="customerRef" type="text" :label="__('Customer (name, optional)')" class="mb-3" />
        <FormControl v-model="remarks" type="textarea" :label="__('Remarks')" class="mb-3" />
        <Button :loading="addEntry.loading" class="w-full" @click="submitEntry">{{ __('Save entry') }}</Button>
        <p v-if="addEntry.error" class="mt-2 text-sm text-red-600">{{ addEntry.error?.message || addEntry.error }}</p>
      </div>

      <div class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
          <p class="text-sm font-medium text-gray-900 dark:text-white">{{ __('Today summary') }}</p>
          <Button variant="outline" size="sm" @click="reg.load()">{{ __('Refresh') }}</Button>
        </div>
        <div v-if="reg.loading" class="text-sm text-gray-500">{{ __('Loading…') }}</div>
        <p v-else-if="reg.error" class="text-sm text-red-600">{{ reg.error?.message || reg.error }}</p>
        <template v-else-if="reg.data">
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ __('Total in') }}: {{ fmtNPR(reg.data.total_in) }}</p>
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ __('Total out') }}: {{ fmtNPR(reg.data.total_out) }}</p>
          <p class="text-base font-semibold text-gray-900 dark:text-white">{{ __('Net') }}: {{ fmtNPR(reg.data.net) }}</p>
          <ul class="mt-4 max-h-96 divide-y divide-gray-100 overflow-y-auto text-sm dark:divide-gray-800">
            <li v-for="e in reg.data.entries" :key="e.name" class="py-2">
              <span class="font-medium">{{ e.topic }}</span>
              <span class="ml-2 text-gray-500">{{ e.entry_type }} · {{ e.payment_mode }}</span>
              <span class="float-right tabular-nums">{{ fmtNPR(e.amount) }}</span>
            </li>
            <li v-if="!reg.data.entries?.length" class="py-4 text-gray-500">{{ __('No entries') }}</li>
          </ul>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, FormControl, toast } from 'frappe-ui'
import { fmtNPR } from '@shared/utils'

const topics = ['Counter Sales', 'Employee Deposit', 'Advance Recovery', 'Utility Expense', 'Employee Advance', 'Purchase Expense', 'Other']
const payModes = ['Cash', 'QR', 'Bank Transfer', 'Cheque']

const entryType = ref('In')
const topic = ref('Counter Sales')
const paymentMode = ref('Cash')
const amount = ref('')
const employeeRef = ref('')
const customerRef = ref('')
const remarks = ref('')

const reg = createResource({
	url: 'custom_erp.api.admin.get_cash_register_summary',
	auto: true,
})

const addEntry = createResource({
	url: 'custom_erp.api.admin.add_cash_register_entry',
	auto: false,
	onSuccess() {
		toast.success(__('Entry saved'))
		amount.value = ''
		remarks.value = ''
		employeeRef.value = ''
		customerRef.value = ''
		reg.reload()
	},
	onError(e) {
		toast.error(e.message || __('Failed'))
	},
})

function submitEntry() {
	addEntry.submit({
		entry_type: entryType.value,
		topic: topic.value,
		payment_mode: paymentMode.value,
		amount: parseFloat(amount.value),
		employee_ref: employeeRef.value || undefined,
		customer_ref: customerRef.value || undefined,
		remarks: remarks.value || undefined,
	})
}
</script>
