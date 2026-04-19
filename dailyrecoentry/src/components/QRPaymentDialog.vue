<!-- ADDED BY AI: DAILY_PAYMENT_RECO - QR Payment Dialog Component -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen px-3 py-4 sm:px-4 text-center">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <div class="relative inline-block bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all w-full max-w-sm sm:max-w-md mx-auto">
        <div class="bg-white px-4 pt-4 pb-3 sm:px-6 sm:pt-5 sm:pb-4">
          <div class="text-center">
            <h3 class="text-base sm:text-lg leading-6 font-semibold text-gray-900 mb-3 sm:mb-4 truncate" id="modal-title">
              QR Payment - {{ customerName }}
            </h3>

            <!-- Static Fonepay placard (no API) -->
            <div v-if="isStaticMode" class="flex flex-col items-stretch text-left">
              <div class="flex justify-center mb-3">
                <img
                  :src="staticImageUrl"
                  alt="Fonepay static QR — scan to pay"
                  class="max-w-[280px] w-full h-auto rounded-lg border-2 border-gray-200 bg-white"
                  loading="lazy"
                />
              </div>
              <p class="text-lg sm:text-xl font-bold text-gray-900 mb-1 text-center">Rs. {{ formatAmount(amount) }}</p>
              <p class="text-xs text-gray-500 mb-3 text-center">Scan with Fonepay app, then confirm below.</p>
              <label class="block text-sm font-medium text-gray-700 mb-1">Remarks <span class="text-red-600">*</span></label>
              <textarea
                v-model="staticUserRemarks"
                rows="3"
                class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                placeholder="Required — e.g. transaction reference, payer name"
              />
            </div>

            <!-- Dynamic: Loading State -->
            <div v-else-if="loading" class="flex flex-col items-center justify-center py-6 sm:py-8">
              <svg class="animate-spin h-10 w-10 sm:h-12 sm:w-12 text-blue-600 mb-3 sm:mb-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="text-sm sm:text-base text-gray-600">Generating QR code...</p>
            </div>

            <!-- Dynamic: QR Code Display -->
            <div v-else-if="qrCode && status === 'PENDING'" class="flex flex-col items-center">
              <div id="qr-code-container" class="mb-3 p-3 sm:p-4 bg-white rounded-lg border-2 border-gray-200"></div>
              <p class="text-lg sm:text-xl font-bold text-gray-900 mb-1 sm:mb-2">Rs. {{ formatAmount(amount) }}</p>
              <p class="text-xs sm:text-sm text-gray-600 mb-3 sm:mb-4">Scan to pay with Fonepay</p>

              <div class="flex items-center space-x-2 text-blue-600 bg-blue-50 px-4 py-2 rounded-lg">
                <svg class="animate-spin h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-xs sm:text-sm font-medium">Waiting for payment...</span>
              </div>

              <p v-if="manualCheckMessage" class="mt-2 text-xs sm:text-sm text-amber-600 font-medium">
                {{ manualCheckMessage }}
              </p>
            </div>

            <!-- Dynamic: Success State -->
            <div v-else-if="status === 'SUCCESS'" class="flex flex-col items-center py-6 sm:py-8">
              <div class="flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-green-100 rounded-full mb-3 sm:mb-4">
                <svg class="w-8 h-8 sm:w-10 sm:h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <h4 class="text-lg sm:text-xl font-bold text-green-600 mb-1 sm:mb-2">Payment Successful!</h4>
              <p class="text-sm sm:text-base text-gray-600">QR payment of Rs. {{ formatAmount(amount) }} received</p>
            </div>

            <!-- Dynamic: Error State -->
            <div v-else-if="status === 'ERROR'" class="flex flex-col items-center py-6 sm:py-8">
              <div class="flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-red-100 rounded-full mb-3 sm:mb-4">
                <svg class="w-8 h-8 sm:w-10 sm:h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </div>
              <h4 class="text-lg sm:text-xl font-bold text-red-600 mb-1 sm:mb-2">Payment Failed</h4>
              <p class="text-xs sm:text-sm text-gray-600">{{ errorMessage }}</p>
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-4 py-3 sm:px-6 flex flex-col-reverse sm:flex-row sm:justify-end gap-2 sm:gap-3">
          <template v-if="isStaticMode">
            <button
              type="button"
              @click="close"
              class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border-2 border-gray-300 shadow-md px-5 py-3 sm:px-4 sm:py-2 bg-white text-base sm:text-sm font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 touch-manipulation"
            >
              Cancel
            </button>
            <button
              type="button"
              @click="confirmStaticPayment"
              :disabled="!staticRemarksValid"
              class="qr-static-confirm-btn w-full sm:w-auto inline-flex justify-center items-center rounded-lg border-2 border-transparent shadow-md px-5 py-3 sm:px-4 sm:py-2 bg-sky-600 text-base sm:text-sm font-semibold hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 touch-manipulation disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Confirm
            </button>
          </template>
          <template v-else>
            <button
              v-if="status === 'SUCCESS'"
              type="button"
              @click="confirmSuccess"
              class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border-2 border-transparent shadow-md px-5 py-3 sm:px-4 sm:py-2 bg-green-600 text-base sm:text-sm font-semibold text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 touch-manipulation"
            >
              Done
            </button>
            <template v-else>
              <button
                type="button"
                @click="close"
                class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border-2 border-gray-300 shadow-md px-5 py-3 sm:px-4 sm:py-2 bg-white text-base sm:text-sm font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 touch-manipulation"
              >
                Cancel
              </button>
              <button
                v-if="showManualCheck && status === 'PENDING' && qrCode"
                type="button"
                @click="checkPaymentManually"
                :disabled="checkingPayment"
                class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border-2 border-blue-500 shadow-md px-5 py-3 sm:px-4 sm:py-2 bg-blue-50 text-base sm:text-sm font-semibold text-blue-700 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 touch-manipulation disabled:opacity-50"
              >
                <svg v-if="checkingPayment" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ checkingPayment ? 'Checking...' : 'Check Payment' }}
              </button>
            </template>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import { call } from 'frappe-ui'
import { session } from '../../../shared/data/session'
import { isStaticQrMode, STATIC_FONEPAY_QR_IMAGE_URL } from '../config/qrPaymentMode'
import { getTodayBs } from '../../../shared/utils/nepaliDate'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  customer: {
    type: String,
    required: true
  },
  customerName: {
    type: String,
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  lineName: {
    type: String,
    default: null
  },
  company: {
    type: String,
    default: ''
  },
  companyConfig: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'success'])

const isStaticMode = computed(() => isStaticQrMode())
const staticImageUrl = STATIC_FONEPAY_QR_IMAGE_URL
const staticUserRemarks = ref('')
const staticRemarksValid = computed(() => Boolean(staticUserRemarks.value && staticUserRemarks.value.trim()))

const loading = ref(false)
const qrCode = ref(null)
const transactionId = ref(null)
const prn = ref(null)
const status = ref('PENDING')
const errorMessage = ref('')
const merchantSocket = ref(null)
const showManualCheck = ref(false)
const checkingPayment = ref(false)
const manualCheckMessage = ref('')
let manualCheckTimer = null

const currentUser = session.user || 'Unknown'

function buildStaticQrStoredRemark(userText) {
	const bs = getTodayBs()
	const now = new Date()
	const time = now.toLocaleTimeString('en-GB', {
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
		hour12: false
	})
	const ad = now.toLocaleDateString('en-CA')
	return `${userText.trim()} | BS: ${bs} ${time} (AD: ${ad})`
}

function confirmStaticPayment() {
	const txt = staticUserRemarks.value?.trim()
	if (!txt) return
	const full = buildStaticQrStoredRemark(txt)
	const preview = `Amount: Rs. ${formatAmount(props.amount)}\n\nSave with remarks:\n${full}\n\nProceed?`
	if (!window.confirm(preview)) return
	emit('success', {
		mode: 'static',
		qrRemarks: full,
		amount: props.amount
	})
}

watch(() => props.show, async (newValue) => {
	if (newValue) {
		if (isStaticMode.value) {
			staticUserRemarks.value = ''
		} else {
			await generateQR()
		}
	} else {
		resetState()
	}
})

const generateQR = async () => {
	loading.value = true
	status.value = 'PENDING'
	try {
		const response = await call('custom_erp.api.fonepay.create_dynamic_qr_for_company', {
			amount: props.amount,
			company: props.company,
			customer: props.customer,
			remarks1: `${currentUser}`,
			remarks2: `${props.customerName}`,
			daily_sales_payment_reco_line: props.lineName || null
		})

		if (response?.qr_message) {
			qrCode.value = response.qr_message
			transactionId.value = response.tx_name
			prn.value = response.prn
			loading.value = false

			await nextTick()
			await nextTick()
			await new Promise(resolve => setTimeout(resolve, 300))

			await renderQRCode(response.qr_message)
			await connectToWebSocket(response.websocket_url || response.merchant_websocket_url)

			manualCheckTimer = setTimeout(() => {
				showManualCheck.value = true
			}, 5000)
		} else {
			status.value = 'ERROR'
			errorMessage.value = 'Failed to generate QR code - no QR message returned'
		}
	} catch (error) {
		status.value = 'ERROR'
		errorMessage.value = error.message || 'Failed to generate QR code'
	} finally {
		loading.value = false
	}
}

const connectToWebSocket = async (url) => {
	if (!url || typeof WebSocket === 'undefined') {
		return
	}
	closeWebSocket()
	try {
		const ws = new WebSocket(url)
		merchantSocket.value = ws
		ws.onopen = () => {
			status.value = 'PENDING'
		}
		ws.onerror = () => {}
		ws.onclose = () => {
			merchantSocket.value = null
		}
		ws.onmessage = async (event) => {
			try {
				const data = JSON.parse(event.data)
				await handleWebSocketMessage(data)
			} catch {
				/* ignore */
			}
		}
	} catch {
		/* ignore */
	}
}

const handleWebSocketMessage = async (data) => {
	let isSuccess = false
	let isScanned = false
	let parsedStatus = null

	if (data.transactionStatus && typeof data.transactionStatus === 'string') {
		try {
			parsedStatus = JSON.parse(data.transactionStatus)
			if (parsedStatus.qrVerified === true && parsedStatus.paymentSuccess !== true) {
				isScanned = true
			} else if (parsedStatus.paymentSuccess === true || parsedStatus.success === true) {
				isSuccess = true
			}
		} catch {
			/* ignore */
		}
	}

	if (!isSuccess && data.transactionStatus && typeof data.transactionStatus === 'object') {
		const statusStr = String(data.transactionStatus).toUpperCase()
		isSuccess = statusStr === 'SUCCESS' || statusStr === 'COMPLETED'
		isScanned = statusStr === 'INITIATED' || statusStr === 'VERIFIED'
	}

	if (!isSuccess) {
		isSuccess = data.paymentSuccess === true || data.success === true
	}

	if (isScanned) {
		status.value = 'PENDING'
	}

	if (isSuccess) {
		try {
			const verify = await call('custom_erp.api.fonepay.check_status', {
				txn_ref_id: prn.value || transactionId.value
			})
			if (verify && verify.status === 'SUCCESS') {
				status.value = 'SUCCESS'
				closeWebSocket()
				emit('success', {
					transactionId: transactionId.value,
					prn: prn.value,
					amount: props.amount
				})
			}
		} catch {
			/* ignore */
		}
	}
}

const closeWebSocket = () => {
	if (merchantSocket.value) {
		merchantSocket.value.close()
		merchantSocket.value = null
	}
}

const renderQRCode = async (qrMessage) => {
	if (!qrMessage) {
		throw new Error('No QR message provided')
	}
	if (!window.QRCode) {
		const script = document.createElement('script')
		script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
		document.head.appendChild(script)
		await new Promise((resolve, reject) => {
			script.onload = () => resolve()
			script.onerror = () => reject(new Error('Failed to load QRCode library'))
		})
	}
	await new Promise(resolve => setTimeout(resolve, 200))
	const qrContainer = document.getElementById('qr-code-container')
	if (!qrContainer) {
		throw new Error('QR container not found')
	}
	qrContainer.innerHTML = ''
	new window.QRCode(qrContainer, {
		text: qrMessage,
		width: 256,
		height: 256,
		colorDark: '#000000',
		colorLight: '#ffffff',
		correctLevel: window.QRCode.CorrectLevel?.H || 2
	})
}

const checkPaymentManually = async () => {
	checkingPayment.value = true
	manualCheckMessage.value = ''
	try {
		const verify = await call('custom_erp.api.fonepay.check_status', {
			txn_ref_id: prn.value || transactionId.value
		})
		if (verify && verify.status === 'SUCCESS') {
			status.value = 'SUCCESS'
			closeWebSocket()
			clearManualCheckTimer()
			emit('success', {
				transactionId: transactionId.value,
				prn: prn.value,
				amount: props.amount
			})
		} else {
			manualCheckMessage.value = 'Not confirmed yet'
			setTimeout(() => {
				manualCheckMessage.value = ''
			}, 3000)
		}
	} catch {
		manualCheckMessage.value = 'Not confirmed yet'
		setTimeout(() => {
			manualCheckMessage.value = ''
		}, 3000)
	} finally {
		checkingPayment.value = false
	}
}

const clearManualCheckTimer = () => {
	if (manualCheckTimer) {
		clearTimeout(manualCheckTimer)
		manualCheckTimer = null
	}
}

const confirmSuccess = () => {
	emit('success', transactionId.value)
	close()
}

const close = () => {
	closeWebSocket()
	emit('close')
}

const resetState = () => {
	closeWebSocket()
	clearManualCheckTimer()
	staticUserRemarks.value = ''
	loading.value = false
	qrCode.value = null
	transactionId.value = null
	prn.value = null
	status.value = 'PENDING'
	errorMessage.value = ''
	showManualCheck.value = false
	checkingPayment.value = false
	manualCheckMessage.value = ''
}

const formatAmount = (amount) => {
	return new Intl.NumberFormat('en-NP', {
		minimumFractionDigits: 0
	}).format(amount)
}
</script>

<style scoped>
/* Ensure label stays readable if global/app CSS overrides Tailwind text-white */
.qr-static-confirm-btn {
	color: #ffffff !important;
	-webkit-text-fill-color: #ffffff;
	opacity: 1;
	visibility: visible;
}
.qr-static-confirm-btn:disabled {
	color: #ffffff !important;
	-webkit-text-fill-color: #ffffff;
	opacity: 0.65;
}
</style>
