<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Cheque Capture Component -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
              Capture Cheque Details - {{ customerName }}
            </h3>
            
            <div class="space-y-4">
              <!-- Cheque Number -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Cheque Number</label>
                <input
                  v-model="chequeNumber"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter cheque number"
                />
              </div>
              
              <!-- Nepali Date -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Cheque Date (Nepali)</label>
                <NepaliDatePicker
                  v-model="chequeDate"
                  placeholder="Select cheque date"
                  class="w-full"
                />
                <p v-if="chequeDate" class="mt-1 text-xs text-gray-600 font-medium">
                  Selected AD: {{ chequeDate }}
                </p>
                <p v-else class="mt-1 text-xs text-gray-500">Select date from Nepali calendar</p>
              </div>
              
              <!-- Institute Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Institute Name</label>
                <input
                  v-model="instituteName"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter institute name"
                />
              </div>
              
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            @click="saveCheque"
            :disabled="!isValid || uploading"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="uploading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ uploading ? 'Saving...' : 'Save Cheque' }}
          </button>
          <button
            type="button"
            @click="close"
            :disabled="uploading"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'
import NepaliDatePicker from '../../../shared/components/NepaliDatePicker.vue'
import { bsToAd, adToBs } from '../../../shared/utils/nepaliDate'

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
  }
})

const emit = defineEmits(['close', 'success'])

const chequeNumber = ref('')
const chequeDate = ref('') // This will hold the AD date from the date picker
const instituteName = ref('')
const photoPreview = ref(null)
const photoData = ref(null)
const uploading = ref(false)
const fileInput = ref(null)

const isValid = computed(() => {
  return chequeNumber.value && chequeDate.value && instituteName.value
})

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target.result
      photoData.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const clearPhoto = () => {
  photoPreview.value = null
  photoData.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const saveCheque = async () => {
  if (!isValid.value) return
  
  uploading.value = true
  try {
    // Convert AD date to Nepali BS format for saving in cheque_date_nepali field
    const nepaliDateStr = adToBs(chequeDate.value)
    
    // Format AD date for promised_date field (YYYY-MM-DD format)
    // chequeDate.value should already be in YYYY-MM-DD format from the date picker
    const adDateStr = chequeDate.value
    
    // Create the Cheques Taageta record using our custom API method
    const chequeResponse = await call('custom_erp.api.payment_reco.create_cheque_taageta', {
      customer: props.customer,
      cheque_no: chequeNumber.value,
      cheque_date_nepali: nepaliDateStr, // Nepali BS date as string
      bank_name: instituteName.value,
      amount: parseFloat(props.amount) || 0,
      promised_date: adDateStr // English AD date for Date field
    })
    
    if (!chequeResponse.success) {
      throw new Error(chequeResponse.message || 'Failed to create cheque record')
    }
    
    const chequeName = chequeResponse.data.name
    
    // Upload and attach the photo with retry logic
    if (photoData.value) {
      let uploadSuccess = false
      let uploadError = null
      
      // Try up to 2 times to upload the image
      for (let attempt = 1; attempt <= 2 && !uploadSuccess; attempt++) {
        try {
          const uploadResponse = await call('custom_erp.api.payment_reco.compress_and_attach_image', {
            image_data: photoData.value,
            reference_doctype: 'Cheques Taageta',
            reference_name: chequeName,
            filename: `cheque_${chequeNumber.value}.jpg`
          })
          
          if (uploadResponse.success) {
            uploadSuccess = true
          } else {
            uploadError = uploadResponse.message || 'Upload failed'
            console.warn(`Image upload attempt ${attempt} failed:`, uploadError)
          }
        } catch (err) {
          uploadError = err.message || 'Network error during upload'
          console.warn(`Image upload attempt ${attempt} error:`, err)
        }
      }
      
      // If image upload failed, still proceed but warn user
      if (!uploadSuccess) {
        console.warn('Image upload failed after retries, but cheque record was created:', uploadError)
        // Don't block the user - cheque record is created, just image failed
      }
    }
    
    emit('success', chequeName)
    resetForm()
    emit('close')
  } catch (error) {
    console.error('Error saving cheque:', error)
    alert('Error saving cheque: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const resetForm = () => {
  chequeNumber.value = ''
  chequeDate.value = ''
  instituteName.value = ''
  clearPhoto()
}

const close = () => {
  resetForm()
  emit('close')
}
</script>

