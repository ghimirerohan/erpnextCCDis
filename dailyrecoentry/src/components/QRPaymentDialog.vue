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
            
            <!-- Loading State -->
            <div v-if="loading" class="flex flex-col items-center justify-center py-6 sm:py-8">
              <svg class="animate-spin h-10 w-10 sm:h-12 sm:w-12 text-blue-600 mb-3 sm:mb-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="text-sm sm:text-base text-gray-600">Generating QR code...</p>
            </div>
            
            <!-- QR Code Display -->
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
              
              <!-- Manual check message -->
              <p v-if="manualCheckMessage" class="mt-2 text-xs sm:text-sm text-amber-600 font-medium">
                {{ manualCheckMessage }}
              </p>
            </div>
            
            <!-- Success State -->
            <div v-else-if="status === 'SUCCESS'" class="flex flex-col items-center py-6 sm:py-8">
              <div class="flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-green-100 rounded-full mb-3 sm:mb-4">
                <svg class="w-8 h-8 sm:w-10 sm:h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <h4 class="text-lg sm:text-xl font-bold text-green-600 mb-1 sm:mb-2">Payment Successful!</h4>
              <p class="text-sm sm:text-base text-gray-600">QR payment of Rs. {{ formatAmount(amount) }} received</p>
            </div>
            
            <!-- Error State -->
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
            <!-- Manual Check Payment Button - appears after 5 seconds -->
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { call } from 'frappe-ui'
import { session } from '../../../shared/data/session'

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
  }
})

const emit = defineEmits(['close', 'success'])

const loading = ref(false)
const qrCode = ref(null)
const transactionId = ref(null)
const prn = ref(null)
const status = ref('PENDING')
const errorMessage = ref('')
const websocketUrl = ref('')
const merchantSocket = ref(null)
const showManualCheck = ref(false)
const checkingPayment = ref(false)
const manualCheckMessage = ref('')
let manualCheckTimer = null

// Get current username from session
const currentUser = session.user || 'Unknown'

watch(() => props.show, async (newValue) => {
  if (newValue) {
    await generateQR()
  } else {
    resetState()
  }
})

const generateQR = async () => {
  loading.value = true
  status.value = 'PENDING'
  try {
    console.log('🔵 Calling Fonepay API with:', { 
      amount: props.amount, 
      customer: props.customer,
      customerName: props.customerName,
      user: currentUser
    })
    
    // Use the same working Fonepay API as QRPay.vue
    const response = await call('custom_erp.api.fonepay.create_dynamic_qr', {
      amount: props.amount,
      customer: props.customer,
      remarks1: `${currentUser}`,
      remarks2: `${props.customerName}`,
      daily_sales_payment_reco_line: props.lineName || null
    })

    console.log('🟢 Fonepay API response:', response)

    if (response?.qr_message) {
      console.log('✅ QR message found, rendering...')
      qrCode.value = response.qr_message
      transactionId.value = response.tx_name
      prn.value = response.prn
      websocketUrl.value = response.websocket_url || ''
      loading.value = false // CRITICAL: Set loading to false BEFORE rendering QR
      
      // Wait for Vue to render the DOM with the QR container
      await nextTick()
      await nextTick() // Double nextTick for safety
      await new Promise(resolve => setTimeout(resolve, 300)) // Extra time for DOM
      
      // Render the QR code
      await renderQRCode(response.qr_message)
      
      // Connect to WebSocket for real-time status updates
      await connectToWebSocket(response.websocket_url || response.merchant_websocket_url)
      
      // Start 5-second timer to show manual check button
      manualCheckTimer = setTimeout(() => {
        showManualCheck.value = true
      }, 5000)
    } else {
      console.error('❌ No QR message in response:', response)
      status.value = 'ERROR'
      errorMessage.value = 'Failed to generate QR code - no QR message returned'
    }
  } catch (error) {
    console.error('❌ Exception during QR generation:', error)
    console.error('Error details:', { message: error.message, stack: error.stack, error })
    status.value = 'ERROR'
    errorMessage.value = error.message || 'Failed to generate QR code'
  } finally {
    loading.value = false
  }
}

// WebSocket connection for real-time payment status
const connectToWebSocket = async (url) => {
  console.log('🔌 [WEBSOCKET] Connecting to:', url)
  
  if (!url || typeof WebSocket === 'undefined') {
    console.error('❌ [WEBSOCKET] Invalid URL or WebSocket unavailable')
    return
  }
  
  // Close any existing connection
  closeWebSocket()
  
  try {
    const ws = new WebSocket(url)
    merchantSocket.value = ws
    
    ws.onopen = () => {
      console.log('✅ [WEBSOCKET] Connected and listening for payment status')
      status.value = 'PENDING'
    }
    
    ws.onerror = (event) => {
      console.error('❌ [WEBSOCKET] Error:', event)
    }
    
    ws.onclose = (event) => {
      console.log('🔌 [WEBSOCKET] Closed:', event.code, event.reason)
      merchantSocket.value = null
    }
    
    ws.onmessage = async (event) => {
      console.log('📨 [WEBSOCKET] Message received:', event.data)
      
      try {
        const data = JSON.parse(event.data)
        console.log('📦 [WEBSOCKET] Parsed data:', data)
        
        await handleWebSocketMessage(data)
      } catch (error) {
        console.warn('⚠️ [WEBSOCKET] Non-JSON message, ignoring')
      }
    }
  } catch (error) {
    console.error('❌ [WEBSOCKET] Connection failed:', error)
  }
}

const handleWebSocketMessage = async (data) => {
  console.log('💳 [PAYMENT] Processing WebSocket message...')
  
  let isSuccess = false
  let isScanned = false
  let parsedStatus = null
  
  // Parse transactionStatus if it's a JSON string
  if (data.transactionStatus && typeof data.transactionStatus === 'string') {
    try {
      parsedStatus = JSON.parse(data.transactionStatus)
      console.log('💳 [PAYMENT] Parsed status:', parsedStatus)
      
      if (parsedStatus.qrVerified === true && parsedStatus.paymentSuccess !== true) {
        isScanned = true
        console.log('📱 [PAYMENT] QR SCANNED (verified but not paid)')
      } else if (parsedStatus.paymentSuccess === true || parsedStatus.success === true) {
        isSuccess = true
        console.log('✅ [PAYMENT] PAYMENT SUCCESS!')
      }
    } catch (e) {
      console.warn('⚠️ [PAYMENT] Could not parse transactionStatus:', e)
    }
  }
  
  // Check if transactionStatus is already an object
  if (!isSuccess && data.transactionStatus && typeof data.transactionStatus === 'object') {
    const statusStr = String(data.transactionStatus).toUpperCase()
    isSuccess = statusStr === 'SUCCESS' || statusStr === 'COMPLETED'
    isScanned = statusStr === 'INITIATED' || statusStr === 'VERIFIED'
  }
  
  // Check root level fields
  if (!isSuccess) {
    isSuccess = data.paymentSuccess === true || data.success === true
  }
  
  console.log('💳 [PAYMENT] Status flags:', { isSuccess, isScanned })
  
  if (isScanned) {
    console.log('📱 QR Code scanned - waiting for payment confirmation')
    status.value = 'PENDING'
  }
  
  if (isSuccess) {
    console.log('🎉 [PAYMENT] SUCCESS! Verifying with backend...')
    
    try {
      // Verify with backend
      const verify = await call('custom_erp.api.fonepay.check_status', {
        txn_ref_id: prn.value || transactionId.value
      })
      
      console.log('✅ [PAYMENT] Backend verification:', verify)
      
      if (verify && verify.status === 'SUCCESS') {
        status.value = 'SUCCESS'
        closeWebSocket()
        // Emit success event with transaction details
        emit('success', {
          transactionId: transactionId.value,
          prn: prn.value,
          amount: props.amount
        })
      }
    } catch (error) {
      console.error('❌ [PAYMENT] Verification failed:', error)
    }
  }
}

const closeWebSocket = () => {
  if (merchantSocket.value) {
    console.log('🔌 [WEBSOCKET] Closing connection')
    merchantSocket.value.close()
    merchantSocket.value = null
  }
}

const renderQRCode = async (qrMessage) => {
  console.log('📲 renderQRCode called with message length:', qrMessage?.length)
  
  if (!qrMessage) {
    console.error('❌ No QR message provided')
    throw new Error('No QR message provided')
  }
  
  // Load QRCode.js library if not already loaded
  if (!window.QRCode) {
    console.log('📥 Loading QRCode library...')
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
    document.head.appendChild(script)
    await new Promise((resolve, reject) => {
      script.onload = () => {
        console.log('✅ QRCode library loaded')
        resolve()
      }
      script.onerror = () => {
        console.error('❌ Failed to load QRCode library')
        reject(new Error('Failed to load QRCode library'))
      }
    })
  } else {
    console.log('✅ QRCode library already loaded')
  }
  
  // Wait for Vue to render the DOM element
  console.log('⏳ Waiting for DOM...')
  await new Promise(resolve => setTimeout(resolve, 200))
  
  const qrContainer = document.getElementById('qr-code-container')
  if (!qrContainer) {
    console.error('❌ QR container not found in DOM')
    throw new Error('QR container not found')
  }
  
  console.log('✅ QR container found:', qrContainer)
  
  // Clear any existing QR code
  qrContainer.innerHTML = ''
  
  // Generate new QR code
  try {
    console.log('🎨 Generating QR code...')
    new window.QRCode(qrContainer, {
      text: qrMessage,
      width: 256,
      height: 256,
      colorDark: '#000000',
      colorLight: '#ffffff',
      correctLevel: window.QRCode.CorrectLevel?.H || 2
    })
    console.log('✅ QR code generated successfully')
  } catch (error) {
    console.error('❌ Error generating QR code:', error)
    throw error
  }
}

const checkPaymentManually = async () => {
  checkingPayment.value = true
  manualCheckMessage.value = ''
  
  try {
    console.log('🔍 [MANUAL CHECK] Checking payment status...')
    const verify = await call('custom_erp.api.fonepay.check_status', {
      txn_ref_id: prn.value || transactionId.value
    })
    
    console.log('🔍 [MANUAL CHECK] Result:', verify)
    
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
      // Clear message after 3 seconds
      setTimeout(() => {
        manualCheckMessage.value = ''
      }, 3000)
    }
  } catch (error) {
    console.error('❌ [MANUAL CHECK] Error:', error)
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
  loading.value = false
  qrCode.value = null
  transactionId.value = null
  prn.value = null
  status.value = 'PENDING'
  errorMessage.value = ''
  websocketUrl.value = ''
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

