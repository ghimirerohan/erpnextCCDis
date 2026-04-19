<template>
  <div class="space-y-4">
    <Button variant="outline" @click="$router.push('/')">{{ __('Back') }}</Button>
    <h1 class="text-xl font-semibold text-gray-900 dark:text-white">{{ id }}</h1>

    <div class="flex flex-wrap gap-2 border-b border-gray-200 pb-2 dark:border-gray-800">
      <Button size="sm" :variant="tab === 'pay' ? 'solid' : 'outline'" @click="tab = 'pay'">{{ __('Payments') }}</Button>
      <Button size="sm" :variant="tab === 'adv' ? 'solid' : 'outline'" @click="tab = 'adv'">{{ __('Advances') }}</Button>
      <Button size="sm" :variant="tab === 'att' ? 'solid' : 'outline'" @click="tab = 'att'">{{ __('Attendance') }}</Button>
      <Button size="sm" :variant="tab === 'payroll' ? 'solid' : 'outline'" @click="tab = 'payroll'">{{ __('Payroll') }}</Button>
    </div>

    <div v-if="detail.loading" class="text-sm text-gray-500">{{ __('Loading…') }}</div>
    <p v-else-if="detail.error" class="text-sm text-red-600">{{ detail.error?.message || detail.error }}</p>

    <template v-else-if="detail.data">
      <div v-if="tab === 'pay'" class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <ul class="divide-y divide-gray-100 dark:divide-gray-800">
          <li v-for="p in detail.data.payments" :key="p.name" class="flex justify-between py-2 text-sm">
            <div>
              <span class="font-medium text-gray-900 dark:text-white">{{ p.customer_name }}</span>
              <Badge :label="p.payment_mode" class="ml-2" :theme="modeColor(p.payment_mode)" />
            </div>
            <span class="tabular-nums">{{ fmtNPR(p.amount) }}</span>
          </li>
          <li v-if="!detail.data.payments?.length" class="py-4 text-gray-500">{{ __('None') }}</li>
        </ul>
      </div>

      <div v-if="tab === 'adv'" class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <ul class="divide-y divide-gray-100 dark:divide-gray-800">
          <li v-for="a in detail.data.advances" :key="a.name" class="py-2 text-sm">
            <span class="font-medium">{{ a.name }}</span>
            <span class="ml-2 text-gray-500">{{ a.status }}</span>
            <span class="float-right tabular-nums">{{ fmtNPR(a.balance) }}</span>
          </li>
          <li v-if="!detail.data.advances?.length" class="py-4 text-gray-500">{{ __('None') }}</li>
        </ul>
      </div>

      <div v-if="tab === 'att'" class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <ul class="divide-y divide-gray-100 dark:divide-gray-800">
          <li v-for="a in detail.data.attendance" :key="`${a.attendance_date}-${a.status}`" class="flex justify-between py-2 text-sm">
            <span>{{ fmtDate(a.attendance_date) }}</span>
            <span>{{ a.status }}</span>
          </li>
          <li v-if="!detail.data.attendance?.length" class="py-4 text-gray-500">{{ __('None') }}</li>
        </ul>
      </div>

      <div v-if="tab === 'payroll'" class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
        <ul class="divide-y divide-gray-100 dark:divide-gray-800">
          <li v-for="s in detail.data.salary_slips" :key="s.name" class="py-2 text-sm">
            <span class="font-medium">{{ s.name }}</span>
            <span class="ml-2 text-gray-500">{{ fmtDate(s.start_date) }} – {{ fmtDate(s.end_date) }}</span>
            <span class="float-right tabular-nums">{{ fmtNPR(s.net_pay) }}</span>
          </li>
          <li v-if="!detail.data.salary_slips?.length" class="py-4 text-gray-500">{{ __('None') }}</li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createResource, Button, Badge } from 'frappe-ui'
import { fmtNPR, fmtDate, MODE_COLORS } from '@shared/utils'

const props = defineProps({
	id: { type: String, required: true },
})

const tab = ref('pay')

const detail = createResource({
	url: 'custom_erp.api.admin.get_employee_detail',
	auto: false,
})

watch(
	() => props.id,
	(emp) => {
		if (emp) detail.reload({ employee: emp })
	},
	{ immediate: true },
)

function modeColor(mode) {
	return MODE_COLORS[mode] || 'gray'
}
</script>
