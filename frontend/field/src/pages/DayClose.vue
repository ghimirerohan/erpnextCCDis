<template>
  <div class="field-form-page space-y-4 p-4 [&_label]:text-ink-gray-7">
    <p class="text-base leading-snug text-ink-gray-7">
      {{
        __(
          'Count physical cash notes, then submit to compare with today’s cash collections in the system.',
        )
      }}
    </p>

    <section class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm">
      <div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <FormControl
          v-for="d in NPR_DENOMS"
          :key="d"
          v-model.number="counts[d]"
          type="number"
          size="md"
          variant="outline"
          :label="String(d)"
        />
      </div>
    </section>

    <section class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm">
      <FormControl
        v-model="expenseAmount"
        type="number"
        size="md"
        variant="outline"
        :label="__('Field expense amount (optional)')"
      />
      <FormControl
        v-model="expenseRemarks"
        type="textarea"
        class="mt-4"
        size="md"
        variant="outline"
        :label="__('Expense note (optional)')"
      />
    </section>

    <Button
      class="w-full"
      size="lg"
      variant="solid"
      theme="blue"
      :loading="cashCount.loading"
      @click="submit"
    >
      {{ __('Submit count') }}
    </Button>

    <div
      v-if="cashCount.error"
      class="rounded-lg border border-outline-red-2 bg-surface-red-2 px-4 py-3 text-sm text-ink-red-4"
      role="alert"
    >
      {{ cashCount.error }}
    </div>

    <section
      v-if="cashCount.data"
      class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm"
    >
      <p class="text-sm text-ink-gray-8">
        {{ __('Physical total') }}:
        <span class="font-semibold tabular-nums text-ink-gray-9">{{
          fmtNPR(cashCount.data.physical_total)
        }}</span>
      </p>
      <p class="mt-2 text-sm text-ink-gray-8">
        {{ __('System cash total') }}:
        <span class="font-semibold tabular-nums text-ink-gray-9">{{
          fmtNPR(cashCount.data.system_total)
        }}</span>
      </p>
      <p class="mt-3 text-lg font-semibold text-ink-gray-9">
        {{ __('Variance') }}: {{ fmtNPR(cashCount.data.variance) }}
      </p>
      <p v-if="cashCount.data.expense_note_logged" class="mt-2 text-xs text-ink-gray-6">
        {{ __('Expense note was logged for office follow-up.') }}
      </p>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { createResource, Button, FormControl, toast } from 'frappe-ui'
import { NPR_DENOMS, fmtNPR } from '@shared/utils'

const counts = reactive({})
for (const d of NPR_DENOMS) counts[d] = 0

const expenseAmount = ref('')
const expenseRemarks = ref('')

const cashCount = createResource({
	url: 'custom_erp.api.field.submit_cash_count',
	auto: false,
	onSuccess() {
		toast.success(__('Count submitted'))
	},
	onError(e) {
		toast.error(e.message || __('Failed'))
	},
})

function submit() {
	const denom = {}
	for (const d of NPR_DENOMS) {
		const n = parseInt(counts[d], 10) || 0
		if (n > 0) denom[String(d)] = n
	}
	cashCount.submit({
		denomination_counts: denom,
		expense_amount: expenseAmount.value || undefined,
		expense_remarks: expenseRemarks.value || undefined,
	})
}
</script>
