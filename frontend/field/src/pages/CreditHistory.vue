<template>
  <div class="field-form-page space-y-4 p-4 [&_label]:text-ink-gray-7">
    <section class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm">
      <FormControl
        v-model="customerId"
        type="text"
        size="md"
        variant="outline"
        :label="__('Customer ID')"
        :placeholder="__('CUST-00001')"
      />
      <Button
        class="mt-4 w-full"
        size="lg"
        variant="solid"
        theme="blue"
        :loading="outstanding.loading"
        @click="loadOutstanding"
      >
        {{ __('Load outstanding') }}
      </Button>
    </section>

    <div
      v-if="outstanding.error"
      class="rounded-lg border border-outline-red-2 bg-surface-red-2 px-4 py-3 text-sm text-ink-red-4"
      role="alert"
    >
      {{ outstanding.error }}
    </div>

    <section
      v-if="outstanding.data"
      class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm"
    >
      <p class="mb-3 text-sm font-medium text-ink-gray-8">{{ __('Unpaid invoices') }}</p>
      <ul class="space-y-2 text-sm">
        <li
          v-for="inv in outstanding.data.invoices"
          :key="inv.name"
          class="flex justify-between gap-2 border-b border-outline-gray-1 pb-2 text-ink-gray-9 last:border-0"
        >
          <span class="font-medium">{{ inv.name }}</span>
          <span class="tabular-nums font-medium">{{ fmtNPR(inv.outstanding_amount) }}</span>
        </li>
        <li v-if="!outstanding.data.invoices?.length" class="text-ink-gray-5">
          {{ __('None') }}
        </li>
      </ul>
      <p class="mb-3 mt-4 text-sm font-medium text-ink-gray-8">
        {{ __('Cheque payments (history)') }}
      </p>
      <ul class="space-y-2 text-sm">
        <li
          v-for="ch in outstanding.data.cheques"
          :key="ch.name"
          class="border-b border-outline-gray-1 pb-2 text-ink-gray-8 last:border-0"
        >
          {{ ch.cheque_number || ch.name }} — {{ fmtNPR(ch.amount) }}
        </li>
        <li v-if="!outstanding.data.cheques?.length" class="text-ink-gray-5">
          {{ __('None') }}
        </li>
      </ul>
    </section>

    <section class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm">
      <p class="mb-3 text-sm font-medium text-ink-gray-8">
        {{ __('My recent field payments') }}
      </p>
      <div v-if="history.loading" class="text-sm text-ink-gray-6">{{ __('Loading…') }}</div>
      <p v-else-if="history.error" class="text-sm text-ink-red-4">{{ history.error }}</p>
      <ul v-else class="divide-y divide-outline-gray-1">
        <li v-for="row in history.data || []" :key="row.name" class="flex justify-between gap-3 py-3">
          <div class="min-w-0">
            <span class="text-base font-medium text-ink-gray-9">{{ row.customer_name }}</span>
            <Badge
              :label="row.payment_mode"
              variant="subtle"
              size="md"
              class="ml-2 align-middle"
              :theme="modeColor(row.payment_mode)"
            />
          </div>
          <span class="shrink-0 tabular-nums text-base font-semibold text-ink-gray-9">
            {{ fmtNPR(row.amount) }}
          </span>
        </li>
        <li v-if="!(history.data || []).length" class="py-6 text-center text-sm text-ink-gray-5">
          {{ __('No records') }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, FormControl, Badge } from 'frappe-ui'
import { fmtNPR, MODE_COLORS } from '@shared/utils'

const customerId = ref('')

const outstanding = createResource({
	url: 'custom_erp.api.field.get_customer_outstanding',
	auto: false,
})

const history = createResource({
	url: 'custom_erp.api.field.get_field_payment_history',
	auto: true,
})

function loadOutstanding() {
	if (!customerId.value?.trim()) return
	outstanding.submit({ customer: customerId.value.trim() })
}

function modeColor(mode) {
	return MODE_COLORS[mode] || 'gray'
}
</script>
