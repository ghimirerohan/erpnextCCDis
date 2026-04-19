<template>
  <div class="field-form-page space-y-4 p-4 [&_label]:text-ink-gray-7">
    <section
      class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm"
    >
      <FormControl
        v-model="searchQuery"
        type="text"
        size="md"
        variant="outline"
        :label="__('Search customer')"
        :placeholder="__('Name or code')"
      />
      <div v-if="customerSearch.loading" class="mt-2 text-sm text-ink-gray-6">
        {{ __('Searching…') }}
      </div>
      <ul
        v-else-if="searchResults.length"
        class="mt-2 max-h-48 divide-y divide-outline-gray-1 overflow-y-auto rounded-md border border-outline-gray-1 bg-surface-gray-2"
      >
        <li
          v-for="c in searchResults"
          :key="c.name"
          class="cursor-pointer px-3 py-2.5 text-sm text-ink-gray-9 transition-colors hover:bg-surface-gray-3"
          @click="pickCustomer(c)"
        >
          {{ c.customer_name }}
          <span class="text-ink-gray-5">({{ c.name }})</span>
        </li>
      </ul>
      <div
        v-if="selectedCustomer"
        class="mt-3 rounded-md border border-outline-gray-2 bg-surface-gray-2 px-3 py-3"
      >
        <p class="text-base font-medium text-ink-gray-9">
          {{ customerName || selectedCustomer }}
        </p>
        <p class="mt-0.5 text-sm text-ink-gray-6">{{ selectedCustomer }}</p>
      </div>
    </section>

    <section
      class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm"
    >
      <FormControl
        v-model="paymentMode"
        type="select"
        size="md"
        variant="outline"
        :label="__('Payment mode')"
        :options="PAYMENT_MODES"
      />
      <FormControl
        v-model="amount"
        type="number"
        class="mt-4"
        size="md"
        variant="outline"
        :label="__('Amount')"
      />
      <FormControl
        v-model="salesInvoice"
        type="text"
        class="mt-4"
        size="md"
        variant="outline"
        :label="__('Sales Invoice (optional)')"
      />

      <template v-if="paymentMode === 'Cheque'">
        <FormControl
          v-model="chequeNumber"
          type="text"
          class="mt-4"
          size="md"
          variant="outline"
          :label="__('Cheque number')"
        />
        <FormControl
          v-model="chequeDate"
          type="date"
          class="mt-4"
          size="md"
          variant="outline"
          :label="__('Cheque date')"
        />
        <FormControl
          v-model="chequeBank"
          type="text"
          class="mt-4"
          size="md"
          variant="outline"
          :label="__('Bank')"
        />
      </template>

      <FormControl
        v-model="remarks"
        type="textarea"
        class="mt-4"
        size="md"
        variant="outline"
        :label="__('Remarks')"
      />
    </section>

    <section
      v-if="paymentMode === 'QR'"
      class="rounded-lg border border-outline-gray-1 bg-white p-4 shadow-sm"
    >
      <Button
        class="w-full"
        size="lg"
        variant="solid"
        theme="blue"
        :loading="qrCreate.loading"
        @click="startQr"
      >
        {{ __('Generate Fonepay QR') }}
      </Button>
      <p v-if="qrCreate.error" class="mt-2 text-sm text-ink-red-4">{{ qrCreate.error }}</p>
      <div v-if="activePrn" class="mt-3 space-y-2 text-sm text-ink-gray-8">
        <p>
          <span class="text-ink-gray-6">{{ __('PRN') }}:</span>
          {{ activePrn }}
        </p>
        <Button
          variant="outline"
          theme="gray"
          size="md"
          class="w-full sm:w-auto"
          :loading="statusCheck.loading"
          @click="pollStatus"
        >
          {{ __('Refresh payment status') }}
        </Button>
        <p v-if="statusCheck.data" class="text-xs text-ink-gray-6">
          {{ __('Status') }}: {{ statusCheck.data.status }}
          {{ statusCheck.data.message || '' }}
        </p>
      </div>
    </section>

    <Button
      v-if="paymentMode !== 'QR'"
      class="w-full"
      size="lg"
      variant="solid"
      theme="blue"
      :loading="submitPayment.loading"
      :disabled="!canSubmit"
      @click="savePayment"
    >
      {{ __('Submit payment') }}
    </Button>
    <Button
      v-else
      class="w-full"
      size="lg"
      variant="solid"
      theme="blue"
      :loading="submitPayment.loading"
      :disabled="!canSubmitQr"
      @click="saveQrPayment"
    >
      {{ __('Record QR payment (after success)') }}
    </Button>

    <p v-if="submitPayment.error" class="text-sm text-ink-red-4">{{ submitPayment.error }}</p>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue'
import { createResource, Button, FormControl, toast } from 'frappe-ui'
import { PAYMENT_MODES } from '@shared/utils'

const props = defineProps({
	customer: { type: String, default: '' },
})

const socket = inject('$socket')

const searchQuery = ref('')
const searchResults = ref([])
const selectedCustomer = ref('')
const customerName = ref('')
const paymentMode = ref('Cash')
const amount = ref('')
const salesInvoice = ref('')
const recoReference = ref('')
const chequeNumber = ref('')
const chequeDate = ref('')
const chequeBank = ref('')
const remarks = ref('')
const activePrn = ref('')

const dashboard = createResource({
	url: 'custom_erp.api.field.get_my_dashboard',
	auto: true,
	onSuccess(d) {
		if (d?.reco?.name) recoReference.value = d.reco.name
	},
})

const customerSearch = createResource({
	url: 'custom_erp.api.field.search_customers_for_field',
	auto: false,
	onSuccess(data) {
		searchResults.value = data?.customers || []
	},
})

watch(searchQuery, (q) => {
	const s = (q || '').trim()
	if (s.length < 2) {
		searchResults.value = []
		return
	}
	customerSearch.fetch({ query: s })
})

function pickCustomer(c) {
	selectedCustomer.value = c.name
	customerName.value = c.customer_name || c.name
	searchQuery.value = ''
	searchResults.value = []
}

watch(
	() => props.customer,
	(c) => {
		if (c) {
			selectedCustomer.value = c
			customerSearch.fetch({ query: c }).then(() => {
				const hit = searchResults.value.find((x) => x.name === c)
				if (hit) pickCustomer(hit)
				else customerName.value = c
			})
		}
	},
	{ immediate: true },
)

const qrCreate = createResource({
	url: 'custom_erp.api.fonepay.create_dynamic_qr',
	auto: false,
	onSuccess(data) {
		activePrn.value = data?.prn || ''
		toast.success(__('QR created — scan with Fonepay app'))
	},
	onError(e) {
		toast.error(e.message || __('QR failed'))
	},
})

const statusCheck = createResource({
	url: 'custom_erp.api.fonepay.check_status',
	auto: false,
})

function startQr() {
	if (!selectedCustomer.value || !amount.value) {
		toast.error(__('Customer and amount required'))
		return
	}
	activePrn.value = ''
	qrCreate.submit({
		amount: parseFloat(amount.value),
		customer: selectedCustomer.value,
		sales_invoice: salesInvoice.value || undefined,
	})
}

function pollStatus() {
	if (!activePrn.value) return
	statusCheck.submit({ txn_ref_id: activePrn.value })
}

const submitPayment = createResource({
	url: 'custom_erp.api.field.submit_payment',
	auto: false,
	onSuccess() {
		toast.success(__('Payment recorded'))
		amount.value = ''
		chequeNumber.value = ''
		chequeDate.value = ''
		chequeBank.value = ''
		remarks.value = ''
		activePrn.value = ''
		dashboard.reload()
	},
	onError(e) {
		toast.error(e.message || __('Submit failed'))
	},
})

const canSubmit = computed(() => selectedCustomer.value && amount.value && parseFloat(amount.value) > 0)

const canSubmitQr = computed(() => canSubmit.value && activePrn.value)

function savePayment() {
	submitPayment.submit({
		customer: selectedCustomer.value,
		payment_mode: paymentMode.value,
		amount: parseFloat(amount.value),
		sales_invoice: salesInvoice.value || undefined,
		reco_reference: recoReference.value || undefined,
		cheque_number: chequeNumber.value || undefined,
		cheque_date: chequeDate.value || undefined,
		cheque_bank: chequeBank.value || undefined,
		fonepay_prn: undefined,
		remarks: remarks.value || undefined,
	})
}

function saveQrPayment() {
	submitPayment.submit({
		customer: selectedCustomer.value,
		payment_mode: 'QR',
		amount: parseFloat(amount.value),
		sales_invoice: salesInvoice.value || undefined,
		reco_reference: recoReference.value || undefined,
		fonepay_prn: activePrn.value,
		remarks: remarks.value || undefined,
	})
}

function onFonepaySocket(payload) {
	if (!payload?.prn || payload.prn !== activePrn.value) return
	if (payload.status === 'SUCCESS' || payload.normalized_status === 'SUCCESS') {
		toast.success(__('Fonepay payment successful'))
		pollStatus()
	}
}

onMounted(() => {
	socket?.on('fonepay_update', onFonepaySocket)
})
onUnmounted(() => {
	socket?.off('fonepay_update', onFonepaySocket)
})
</script>
