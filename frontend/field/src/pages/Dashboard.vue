<template>
  <div class="space-y-4 p-4">
    <template v-if="dashboard.loading">
      <div class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div
            v-for="i in 2"
            :key="i"
            class="h-24 animate-pulse rounded-lg border border-outline-gray-1 bg-white"
          />
        </div>
        <div
          class="h-32 animate-pulse rounded-lg border border-outline-gray-1 bg-white"
        />
      </div>
    </template>

    <div
      v-else-if="dashboard.error"
      class="rounded-lg border border-outline-red-2 bg-surface-red-2 px-4 py-3 text-base text-ink-red-4"
      role="alert"
    >
      {{ __('Could not load dashboard') }}: {{ dashboard.error }}
    </div>

    <template v-else-if="dashboard.data">
      <Alert
        v-if="dashboard.data.field_preview"
        theme="yellow"
        variant="subtle"
        :dismissable="true"
        :title="__('Preview mode')"
        :description="
          dashboard.data.field_preview_message ||
          __('Link an Employee to this user to use field collection features.')
        "
      />

      <!-- KPI row — desk-style: white cards, subtle border, clear hierarchy -->
      <div class="grid grid-cols-2 gap-3">
        <div
          class="rounded-lg border border-outline-gray-1 bg-white px-4 py-4 shadow-sm"
        >
          <p class="text-xs font-medium uppercase tracking-wide text-ink-gray-6">
            {{ __('Total Collected') }}
          </p>
          <p class="mt-2 text-2xl font-semibold tabular-nums tracking-tight text-ink-gray-9">
            {{ fmtNPR(dashboard.data.total_collected) }}
          </p>
        </div>
        <div
          v-if="dashboard.data.reco"
          class="rounded-lg border border-outline-green-2 bg-surface-green-2 px-4 py-4 shadow-sm"
        >
          <p class="text-xs font-medium uppercase tracking-wide text-ink-green-3">
            {{ __('Expected (reco net)') }}
          </p>
          <p class="mt-2 text-2xl font-semibold tabular-nums tracking-tight text-ink-green-4">
            {{ fmtNPR(dashboard.data.reco.total_expected) }}
          </p>
        </div>
      </div>

      <!-- By mode -->
      <section
        class="overflow-hidden rounded-lg border border-outline-gray-1 bg-white shadow-sm"
      >
        <div
          class="border-b border-outline-gray-1 bg-surface-gray-2 px-4 py-2.5 text-sm font-medium text-ink-gray-8"
        >
          {{ __('By Mode') }}
        </div>
        <div class="divide-y divide-outline-gray-1 px-4 py-1">
          <div
            v-for="(amt, mode) in dashboard.data.mode_totals"
            :key="mode"
            class="flex items-center justify-between gap-3 py-3"
          >
            <Badge :label="mode" :theme="modeColor(mode)" variant="subtle" size="md" />
            <span class="text-base font-medium tabular-nums text-ink-gray-9">
              {{ fmtNPR(amt) }}
            </span>
          </div>
          <p
            v-if="!Object.keys(dashboard.data.mode_totals || {}).length"
            class="py-6 text-center text-sm text-ink-gray-5"
          >
            {{ __('No payments yet today') }}
          </p>
        </div>
      </section>

      <!-- Assigned customers -->
      <section
        v-if="dashboard.data.assigned_customers.length"
        class="overflow-hidden rounded-lg border border-outline-gray-1 bg-white shadow-sm"
      >
        <div
          class="border-b border-outline-gray-1 bg-surface-gray-2 px-4 py-2.5 text-sm font-medium text-ink-gray-8"
        >
          {{ __('Assigned Customers') }}
        </div>
        <ul class="divide-y divide-outline-gray-1">
          <li
            v-for="cust in dashboard.data.assigned_customers"
            :key="cust.customer"
            class="flex items-center justify-between gap-3 px-4 py-3.5"
          >
            <div class="min-w-0 flex-1">
              <p class="truncate text-base font-medium text-ink-gray-9">
                {{ cust.customer_name }}
              </p>
              <p class="mt-1 text-sm leading-snug text-ink-gray-6">
                <span class="font-medium text-ink-gray-7">{{ __('Expected') }}</span>
                {{ fmtNPR(cust.expected_amount) }}
                <span class="text-ink-gray-4"> · </span>
                <span class="font-medium text-ink-gray-7">{{ __('Outstanding') }}</span>
                {{ fmtNPR(cust.outstanding_amount) }}
              </p>
            </div>
            <Button
              size="sm"
              variant="solid"
              theme="gray"
              :label="__('Pay')"
              icon-left="arrow-right"
              @click="$router.push(`/payment/${cust.customer}`)"
            />
          </li>
        </ul>
      </section>

      <!-- Today's payments -->
      <section
        v-if="dashboard.data.payments.length"
        class="overflow-hidden rounded-lg border border-outline-gray-1 bg-white shadow-sm"
      >
        <div
          class="border-b border-outline-gray-1 bg-surface-gray-2 px-4 py-2.5 text-sm font-medium text-ink-gray-8"
        >
          {{ __("Today's Payments") }}
        </div>
        <ul class="divide-y divide-outline-gray-1">
          <li
            v-for="p in dashboard.data.payments"
            :key="p.name"
            class="flex items-start justify-between gap-3 px-4 py-3.5"
          >
            <div class="min-w-0">
              <p class="text-base font-medium text-ink-gray-9">
                {{ p.customer_name }}
              </p>
              <Badge
                :label="p.payment_mode"
                :theme="modeColor(p.payment_mode)"
                variant="subtle"
                size="md"
                class="mt-1.5"
              />
            </div>
            <span class="shrink-0 text-base font-semibold tabular-nums text-ink-gray-9">
              {{ fmtNPR(p.amount) }}
            </span>
          </li>
        </ul>
      </section>
    </template>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, inject } from 'vue'
import { createResource, Button, Badge, Alert } from 'frappe-ui'
import { fmtNPR, MODE_COLORS } from '@shared/utils'

const socket = inject('$socket')

const dashboard = createResource({
	url: 'custom_erp.api.field.get_my_dashboard',
	auto: true,
	cache: 'field-dashboard',
})

function modeColor(mode) {
	return MODE_COLORS[mode] || 'gray'
}

function reloadDash() {
	dashboard.reload()
}

onMounted(() => {
	socket?.on('ccdis:field_payment_submitted', reloadDash)
})
onUnmounted(() => {
	socket?.off('ccdis:field_payment_submitted', reloadDash)
})
</script>
