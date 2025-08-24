<template>
  <div class="min-h-screen bg-gray-50">
    <div class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Invoice Scanner</h1>
            <p class="text-sm text-gray-600">Authenticated as {{ session.user }}</p>
          </div>
          <Button @click="session.logout.submit()" theme="gray" variant="outline">Logout</Button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-8">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Invoice Image Input</h2>
        
        <!-- Invoice Type Selection -->
        <div class="mb-4">
          <label class="block text-sm text-gray-700 mb-2">Invoice Type</label>
          <div class="flex gap-4">
            <label class="flex items-center gap-2">
              <input type="radio" value="purchase" v-model="finalize.type" /> Purchase
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" value="sales" v-model="finalize.type" /> Sales
            </label>
          </div>
        </div>
        
        <!-- Scanner Configuration -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Connection URL</label>
            <input type="text" 
                   v-model="scannerConfig.connectionUrl" 
                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                   placeholder="http://localhost:17890" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">DPI</label>
            <input type="number" 
                   v-model.number="scannerConfig.dpi" 
                   min="100" max="600" step="50"
                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                   placeholder="300" />
          </div>
        </div>
        
        <!-- Main Image Input Area -->
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors"
             @drop="onDrop"
             @dragover.prevent
             @dragenter="() => isDragOver = true"
             @dragleave="onDragLeave"
             :class="{'border-blue-400 bg-blue-50': isDragOver}">
          
          <!-- Image Preview -->
          <div v-if="selectedFile || capturedDataUrl || scannedImageBlob || scannedImageUrl" class="mb-4">
            <img v-if="imagePreviewUrl" 
                 :src="imagePreviewUrl" 
                 alt="Invoice Preview" 
                 class="max-w-full h-auto max-h-64 mx-auto rounded-lg shadow-md" />
            <div class="mt-2 flex justify-center space-x-2">
              <button @click="clearImage" 
                      class="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded">
                Remove Image
              </button>
            </div>
          </div>
          
          <!-- Upload Options -->
          <div v-if="!selectedFile && !capturedDataUrl && !scannedImageBlob && !scannedImageUrl" class="space-y-4">
            <div class="flex flex-col sm:flex-row gap-3 justify-center">
              <!-- File Upload -->
              <label class="flex-1 cursor-pointer">
                <input type="file" 
                       @change="onFileSelected" 
                       accept="image/*" 
                       class="hidden" />
                <div class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center">
                  📁 Upload from Local Storage
                </div>
              </label>
              
              <!-- Scanner -->
              <button @click="scan" 
                      :disabled="scanning"
                      class="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors">
                <span v-if="scanning">🔄 Scanning...</span>
                <span v-else>📷 Scan Document</span>
              </button>
            </div>
            
            <!-- Drag & Drop Instructions -->
            <div class="text-gray-500 text-sm">
              <p>Or drag and drop an image file here</p>
              <p class="text-xs mt-1">Supports: JPG, PNG, WebP</p>
            </div>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <Button theme="blue" :loading="extracting" @click="extractInvoice" :disabled="!canExtract">Extract Invoice</Button>
          <Alert v-if="extractError" theme="red">{{ extractError }}</Alert>
        </div>
      </div>

      <div v-if="invoice" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Extracted Data</h2>
        
        <!-- Invoice Type Indication -->
        <div v-if="invoiceType" class="mb-4 p-3 rounded-md" 
             :class="invoiceType === 'credit_note' ? 'bg-orange-50 border border-orange-200' : 'bg-blue-50 border border-blue-200'">
          <div class="flex items-center">
            <div v-if="invoiceType === 'credit_note'" class="flex-shrink-0 w-5 h-5 text-orange-400">
              ↶
            </div>
            <div v-else class="flex-shrink-0 w-5 h-5 text-blue-400">
              📄
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium" 
                 :class="invoiceType === 'credit_note' ? 'text-orange-800' : 'text-blue-800'">
                {{ invoiceType === 'credit_note' ? 'Credit Note (Return)' : 'Tax Invoice (Regular)' }}
              </p>
              <p class="text-sm" 
                 :class="invoiceType === 'credit_note' ? 'text-orange-700' : 'text-blue-700'">
                {{ invoiceType === 'credit_note' ? 'This is a return/credit note. Will be processed as a return transaction.' : 'This is a regular tax invoice.' }}
              </p>
              <p class="text-xs mt-1 text-gray-600">
                {{ detectionMethod === 'title' ? `Detected from document title: "${title}"` : 'Inferred from document content' }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
          <div>
            <label class="block text-sm text-gray-600 mb-1">Invoice Number</label>
            <input v-model="invoice.invoiceNumber" class="w-full px-3 py-2 border rounded" placeholder="INV-001" />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">Invoice Date</label>
            <input v-model="invoice.invoiceDate" type="date" class="w-full px-3 py-2 border rounded" />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">Supplier</label>
            <input v-model="finalize.supplierName" class="w-full px-3 py-2 border rounded" placeholder="bntl" />
          </div>
        </div>

        <!-- Invoice Type moved above to enforce selection before extraction -->

        <div class="mt-4 grid md:grid-cols-3 gap-3 sm:gap-4">
          <div>
            <label class="block text-sm text-gray-700 mb-2">Bill Actual Amount</label>
            <input type="number" step="0.01" class="w-full px-3 py-2 border rounded" v-model.number="finalize.billAmount" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 mb-2">Purchase Invoice Type</label>
            <div class="flex items-center mt-2">
              <input type="checkbox" 
                     v-model="finalize.isReturn" 
                     class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2" />
              <label class="ml-2 text-sm text-gray-700">Mark as Credit Note (Return)</label>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              When checked, will be processed as a return transaction. 
              {{ detectionMethod === 'title' ? 'Auto-detected from document title.' : 'Auto-detected from document content. Please verify.' }}
            </p>
            <p v-if="detectionMethod === 'inferred'" class="text-xs text-orange-600 mt-1">
              ⚠️ Detection was inferred. Please verify the invoice type is correct.
            </p>
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm text-gray-700 mb-2">Attach Final Photo</label>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors"
                 @drop="onFinalPhotoDrop"
                 @dragover.prevent
                 @dragenter="() => isFinalPhotoDragOver = true"
                 @dragleave="onFinalPhotoDragLeave"
                 :class="{'border-blue-400 bg-blue-50': isFinalPhotoDragOver}">
              
              <!-- Final Photo Preview -->
              <div v-if="finalize.finalPhotoFile" class="mb-4">
                <img v-if="finalPhotoPreviewUrl" 
                     :src="finalPhotoPreviewUrl" 
                     alt="Final Photo Preview" 
                     class="max-w-full h-auto max-h-32 mx-auto rounded-lg shadow-md" />
                <div class="mt-2 flex justify-center space-x-2">
                  <button @click="clearFinalPhoto" 
                          class="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded">
                    Remove Photo
                  </button>
                </div>
              </div>
              
              <!-- Final Photo Upload Options -->
              <div v-if="!finalize.finalPhotoFile" class="space-y-4">
                <div class="flex flex-col sm:flex-row gap-3 justify-center">
                  <!-- File Upload -->
                  <label class="flex-1 cursor-pointer">
                    <input type="file" 
                           @change="onFinalPhotoSelected" 
                           accept="image/*" 
                           class="hidden" />
                    <div class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center text-sm">
                      📁 Upload Photo
                    </div>
                  </label>
                  
                  <!-- Scanner -->
                  <button @click="scanFinalPhoto" 
                          :disabled="scanning"
                          class="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm">
                    <span v-if="scanning">🔄 Scanning...</span>
                    <span v-else>📷 Scan Photo</span>
                  </button>
                </div>
                
                <!-- Drag & Drop Instructions -->
                <div class="text-gray-500 text-xs">
                  <p>Or drag and drop a photo file here</p>
                </div>
              </div>
            </div>
          </div>
          <div class="md:col-span-3">
            <label class="block text-sm text-gray-700 mb-2">Discount (Rs)</label>
            <input type="number" step="0.01" class="w-full px-3 py-2 border rounded" v-model.number="invoice.totalDiscountAmount" />
          </div>
        </div>

        <div v-if="finalize.type==='purchase'" class="mt-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-semibold">Leakages & Bursts (per item)</h3>
            <div v-if="deletedRows.length > 0" class="flex items-center gap-2">
              <Button theme="blue" variant="outline" size="sm" @click="undoLastDelete" class="hover:bg-blue-50">
                <span class="mr-1 text-blue-600">↶</span> Undo Delete ({{ deletedRows.length }})
              </Button>
            </div>
          </div>
          
          <!-- Validation Status Summary -->
          <div v-if="itemValidation" class="mb-4 p-3 rounded-md" 
               :class="itemValidation.all_valid ? 'bg-green-50 border border-green-200' : 'bg-yellow-50 border border-yellow-200'">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div v-if="itemValidation.all_valid" class="flex-shrink-0 w-5 h-5 text-green-400">
                  ✓
                </div>
                <div v-else class="flex-shrink-0 w-5 h-5 text-yellow-400">
                  ⚠
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium" 
                     :class="itemValidation.all_valid ? 'text-green-800' : 'text-yellow-800'">
                    {{ itemValidation.all_valid ? 'All items are valid' : `${itemValidation.missing_items.length} items need to be added to master data` }}
                  </p>
                  <p v-if="!itemValidation.all_valid" class="text-sm text-yellow-700 mt-1">
                    Use the "+" button next to missing items to add them to the master data. After adding items, click "Re-validate Items" to check again.
                  </p>
                </div>
              </div>
              <div class="flex space-x-2">
                <Button theme="blue" variant="outline" size="sm" @click="validateItems">
                  Re-validate Items
                </Button>
                <Button theme="gray" variant="outline" size="sm" @click="resetItemStatuses">
                  Reset Statuses
                </Button>
              </div>
            </div>
          </div>
          
          <!-- Manual Validation Button (when no validation status) -->
          <div v-else-if="invoice?.items?.length > 0" class="mb-4 p-3 rounded-md bg-gray-50 border border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0 w-5 h-5 text-gray-400">
                  ℹ
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-800">
                    Validate items before creating invoice
                  </p>
                  <p class="text-sm text-gray-600 mt-1">
                    Click the button to check if all items exist in master data. Validation only runs when you click this button or the "Create Invoice" button.
                  </p>
                </div>
              </div>
              <Button theme="blue" variant="outline" size="sm" @click="validateItems" class="ml-4">
                Validate Items
              </Button>
            </div>
          </div>
          
          <div class="overflow-x-auto border border-gray-200 rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-2 sm:px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32 sm:w-48">Code</th>
                  <th class="px-2 sm:px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-48 sm:w-80">Description</th>
                  <th class="px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24">Qty</th>
                  <th class="px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24">UOM</th>
                  <th class="px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24">Leakages</th>
                  <th class="px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24">Bursts</th>
                  <th class="px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-16">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(it, idx) in invoice.items" :key="idx" 
                    :class="{'hover:bg-gray-50': true, 'bg-red-50': it.isMissing, 'bg-green-50': it.itemCreated}">
                  <td class="px-2 sm:px-3 py-3 text-sm">
                    <div class="flex items-center space-x-2">
                      <input class="w-full px-2 sm:px-3 py-2 border rounded text-sm" 
                             v-model="it.materialCode" 
                             :class="{'border-red-500': it.isMissing, 'border-green-500': it.itemCreated}"
                             placeholder="Item Code" />
                      <!-- Add button for missing items -->
                      <button v-if="it.isMissing && !it.itemCreated"
                              @click="openNewItemDialog(idx)"
                              class="flex-shrink-0 w-8 h-8 bg-blue-500 hover:bg-blue-600 text-white rounded-full flex items-center justify-center text-lg font-bold transition-colors add-button">
                        +
                      </button>
                      <!-- Success checkmark for created items -->
                      <span v-if="it.itemCreated" class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm">
                        ✓
                      </span>
                    </div>
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-sm">
                    <input class="w-full px-2 sm:px-3 py-2 border rounded text-sm" 
                           v-model="it.materialDescription" 
                           placeholder="Description" />
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-sm text-center">
                    <input type="number" class="w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center" 
                           v-model.number="it.salesQty" inputmode="numeric" />
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-sm text-center">
                    <select v-model="it.uom" class="px-2 sm:px-3 py-2 border rounded text-center w-16 sm:w-20">
                      <option value="CS">CS</option>
                      <option value="Nos">Nos</option>
                    </select>
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-sm text-center">
                    <input type="number" min="0" class="w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center" 
                           v-model.number="finalize.items[idx].leakages" inputmode="numeric" />
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-center">
                    <input type="number" min="0" class="w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center" 
                           v-model.number="finalize.items[idx].bursts" inputmode="numeric" />
                  </td>
                  <td class="px-2 sm:px-3 py-3 text-sm text-center">
                    <Button theme="red" variant="outline" size="sm" @click="deleteRow(idx)" class="text-red-600 hover:text-red-700">
                      <span class="text-xs">🗑️</span>
                    </Button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-6 flex justify-end">
          <Button theme="green" 
                  :loading="submitting || isProcessing" 
                  :disabled="!finalize.type || isProcessing" 
                  @click="confirmAndSubmit">
            {{ isProcessing ? 'Processing...' : `Create ${finalize.type==='purchase' ? 'Purchase' : 'Sales'} Invoice` }}
          </Button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- New Item Creation Dialog -->
  <div v-if="showNewItemDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Create New Item</h3>
        <p class="text-sm text-gray-500 mt-1">Add this item to the master data</p>
      </div>
      
      <div class="px-6 py-4 space-y-4">
        <!-- Item Code -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Item Code *</label>
          <input type="text" 
                 v-model="newItemData.item_code" 
                 class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="Enter item code" />
        </div>
        
        <!-- Item Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Item Name *</label>
          <input type="text" 
                 v-model="newItemData.item_name" 
                 class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="Enter item name" />
        </div>
        
        <!-- Selling Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Selling Price</label>
          <input type="number" 
                 v-model.number="newItemData.selling_price" 
                 step="0.01" min="0"
                 class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="0.00" />
        </div>
        
        <!-- Valuation Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Valuation Price *</label>
          <input type="number" 
                 v-model.number="newItemData.valuation_price" 
                 step="0.01" min="0"
                 class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="0.00" />
        </div>
        
        <!-- UOM Conversion -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nos in CS (UOM Conversion)</label>
          <input type="number" 
                 v-model.number="newItemData.uom_conversion" 
                 min="1" step="1"
                 class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                 placeholder="6" />
          <p class="text-xs text-gray-500 mt-1">How many Nos (pieces) are in 1 CS (Case)</p>
        </div>
      </div>
      
      <div class="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
        <button @click="showNewItemDialog = false" 
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors">
          Cancel
        </button>
        <button @click="createNewItem" 
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors">
          Create Item
        </button>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { createResource } from 'frappe-ui'
import { session } from '@/data/session'

const selectedFile = ref(null)
const selectedFileName = ref('')
const capturedDataUrl = ref('')
const extractError = ref('')
const extracting = ref(false)
const invoice = ref(null)
const submitting = ref(false)

// Scanner configuration
const scannerConfig = reactive({
  connectionUrl: 'http://localhost:17890',
  dpi: 300
})

// Drag and drop states
const isDragOver = ref(false)
const isFinalPhotoDragOver = ref(false)

// Scanner states
const scanning = ref(false)
const scannedImageBlob = ref(null)
const scannedImageUrl = ref('')

// Image preview URLs
const imagePreviewUrl = computed(() => {
  if (selectedFile.value) return URL.createObjectURL(selectedFile.value)
  if (capturedDataUrl.value) return capturedDataUrl.value
  if (scannedImageBlob.value) return URL.createObjectURL(scannedImageBlob.value)
  if (scannedImageUrl.value) return scannedImageUrl.value
  return null
})

const finalPhotoPreviewUrl = computed(() => {
  if (finalize.finalPhotoFile) return URL.createObjectURL(finalize.finalPhotoFile)
  return null
})

const finalize = reactive({
  type: 'purchase', // default purchase
  billAmount: null,
  finalPhotoFile: null,
  supplierName: 'bntl',
  items: [],
  isReturn: false, // New field for return/credit note
})

// Track deleted rows for undo functionality
const deletedRows = ref([])

// Item validation and new item creation
const itemValidation = ref(null)
const showNewItemDialog = ref(false)
const newItemData = reactive({
  item_code: '',
  item_name: '',
  selling_price: 0,
  valuation_price: 0,
  uom_conversion: 6, // Default CS = 6 Nos
  rowIndex: -1
})

// Add invoice type detection
const invoiceType = ref('') // 'tax_invoice' or 'credit_note'
const isProcessing = ref(false) // Prevent multiple submissions
const detectionMethod = ref('') // 'title' or 'inferred'

// Camera variables removed - replaced with scanner functionality

const onFileSelected = (e) => {
  const f = e?.target?.files?.[0]
  if (!f) return
  selectedFile.value = f
  selectedFileName.value = f.name
  capturedDataUrl.value = ''
}

const onFinalPhotoSelected = (e) => {
  const f = e?.target?.files?.[0]
  if (f) finalize.finalPhotoFile = f
}

// Drag and drop functions
const onDrop = (e) => {
  e.preventDefault()
  isDragOver.value = false
  
  const files = Array.from(e.dataTransfer.files)
  const imageFile = files.find(file => file.type.startsWith('image/'))
  
  if (imageFile) {
    selectedFile.value = imageFile
    selectedFileName.value = imageFile.name
    capturedDataUrl.value = ''
    scannedImageBlob.value = null
    scannedImageUrl.value = ''
  }
}

const onDragLeave = () => {
  isDragOver.value = false
}

const onFinalPhotoDrop = (e) => {
  e.preventDefault()
  isFinalPhotoDragOver.value = false
  
  const files = Array.from(e.dataTransfer.files)
  const imageFile = files.find(file => file.type.startsWith('image/'))
  
  if (imageFile) {
    finalize.finalPhotoFile = imageFile
  }
}

const onFinalPhotoDragLeave = () => {
  isFinalPhotoDragOver.value = false
}

// Scanner functions
const scan = async () => {
  try {
    scanning.value = true;

    // Trigger scan
    const res = await fetch(`${scannerConfig.connectionUrl}/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dpi: scannerConfig.dpi,
        mode: 'Color'
      })
    });

    if (!res.ok) {
      const error = await res.text()
      throw new Error(`Scan failed: ${error}`)
    }

    const { data, format } = await res.json();

    const byteArray = Uint8Array.from(atob(data), c => c.charCodeAt(0));
    const imageBlob = new Blob([byteArray], { type: `image/${format}` });
    
    // Set scanned image as the active source
    scannedImageBlob.value = imageBlob;
    scannedImageUrl.value = URL.createObjectURL(imageBlob);
    
    // Debug logging
    console.log('Scan completed:', {
      scannedImageBlob: !!scannedImageBlob.value,
      scannedImageUrl: !!scannedImageUrl.value,
      imagePreviewUrl: imagePreviewUrl.value,
      canExtract: canExtract.value
    });
    
    // Clear other image sources to avoid confusion
    selectedFile.value = null;
    selectedFileName.value = '';
    capturedDataUrl.value = '';

    alert('Document scanned successfully!');
  } catch (err) {
    alert('Scan failed: ' + err.message);
  } finally {
    scanning.value = false;
  }
}

const scanFinalPhoto = async () => {
  try {
    scanning.value = true;

    // Trigger scan
    const res = await fetch(`${scannerConfig.connectionUrl}/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dpi: scannerConfig.dpi,
        mode: 'Color'
      })
    });

    if (!res.ok) {
      const error = await res.text()
      throw new Error(`Scan failed: ${error}`)
    }

    const { data, format } = await res.json();

    const byteArray = Uint8Array.from(atob(data), c => c.charCodeAt(0));
    const imageBlob = new Blob([byteArray], { type: `image/${format}` });

    // Correctly update finalize.finalPhotoFile for the attachment preview
    finalize.finalPhotoFile = new File([imageBlob], `scanned_photo.${format}`, { type: `image/${format}` });

    alert('Photo scanned successfully!');
  } catch (err) {
    alert('Scan failed: ' + err.message);
  } finally {
    scanning.value = false;
  }
}

// Image management functions
const clearImage = () => {
  // Revoke object URLs to prevent memory leaks
  if (scannedImageUrl.value) {
    URL.revokeObjectURL(scannedImageUrl.value)
  }
  
  selectedFile.value = null
  selectedFileName.value = ''
  capturedDataUrl.value = ''
  scannedImageBlob.value = null
  scannedImageUrl.value = ''
}

const clearFinalPhoto = () => {
  finalize.finalPhotoFile = null
}

// Camera functions removed - replaced with scanner functionality

const canExtract = computed(() => {
  return !!selectedFile.value || !!capturedDataUrl.value || !!scannedImageBlob.value || !!scannedImageUrl.value
})

const safeJson = async (res) => {
  try {
    const text = await res.text()
    if (!text) return {}
    try { return JSON.parse(text) } catch (_) {}
    // try strip code fences or trailing commas
    const cleaned = text.trim().replace(/^```(?:json)?/i, '').replace(/```$/, '')
    return JSON.parse(cleaned)
  } catch (e) { return {} }
}

const robustFetch = async (url, opts = {}) => {
  const maxRetries = 2
  const retryDelays = [500, 1000]
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), 30000)
      const res = await fetch(url, { ...opts, signal: controller.signal })
      clearTimeout(timeout)
      // Retry on transient gateways
      if ([502, 503, 504].includes(res.status) && attempt < maxRetries) {
        await new Promise(r => setTimeout(r, retryDelays[attempt]))
        continue
      }
      return res
    } catch (e) {
      if (attempt < maxRetries) {
        await new Promise(r => setTimeout(r, retryDelays[attempt]))
        continue
      }
      throw new Error(e?.name === 'AbortError' ? 'Request timed out. Please try again.' : (e?.message || 'Network error'))
    }
  }
}

const extractInvoice = async () => {
  extractError.value = ''
  extracting.value = true
  invoice.value = null
  invoiceType.value = '' // Reset invoice type
  finalize.isReturn = false // Reset return flag
  detectionMethod.value = '' // Reset detection method
  try {
    if (!finalize.type) throw new Error('Select invoice type first')
    let res
    if (selectedFile.value) {
      const b64 = await toBase64(selectedFile.value)
      res = await robustFetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_data: b64 })
      })
    } else if (capturedDataUrl.value) {
      res = await robustFetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_data: capturedDataUrl.value })
      })
    } else if (scannedImageBlob.value) {
      const b64 = await toBase64(scannedImageBlob.value)
      res = await robustFetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_data: b64 })
      })
    } else {
      throw new Error('No input')
    }
    const data = await safeJson(res)
    const msg = data.message || data
    if (!res.ok || !msg?.success) throw new Error(msg?.error || 'Extraction failed')
    
    // Debug: Log the full response
    console.log('Full extraction response:', msg)
    console.log('Extracted data:', msg.data)
    
    // Detect purchase invoice type from the extracted title
    const title = msg.data?.title || ''
    console.log('Extracted title:', title) // Debug log
    
    // Try to detect from title first
    let detectedType = null
    let method = 'inferred'
    
    if (title.toLowerCase().includes('credit note')) {
      detectedType = 'credit_note'
      method = 'title'
      console.log('Detected Credit Note from title')
    } else if (title.toLowerCase().includes('tax invoice')) {
      detectedType = 'tax_invoice'
      method = 'title'
      console.log('Detected Tax Invoice from title')
    }
    
    // If title detection failed, try to infer from other fields
    if (!detectedType) {
      console.log('Title detection failed, trying to infer from other fields...')
      // Check if there are any negative amounts that might indicate a credit note
      // Note: We don't check for negative quantities anymore since we always make them positive
      const hasNegativeValues = msg.data?.items?.some(item => 
        (item.lineTotal && item.lineTotal < 0)
      )
      
      if (hasNegativeValues) {
        detectedType = 'credit_note'
        method = 'inferred'
        console.log('Inferred Credit Note from negative line totals')
      } else {
        detectedType = 'tax_invoice'
        method = 'inferred'
        console.log('Defaulting to Tax Invoice')
      }
    }
    
    // Set the invoice type and return flag
    invoiceType.value = detectedType
    finalize.isReturn = detectedType === 'credit_note'
    detectionMethod.value = method
    
    console.log('Final decision:', {
      detectedType,
      isReturn: finalize.isReturn,
      title: title,
      method: method
    })
    
    // Ensure editable model with safe defaults
    invoice.value = {
      invoiceNumber: msg.data?.invoiceNumber || '',
      invoiceDate: normalizeDateToISO(msg.data?.invoiceDate || ''),
      customerName: 'bntl',
      items: Array.isArray(msg.data?.items) ? msg.data.items.map(it => ({
        materialCode: it.materialCode || it.materialDescription || '',
        materialDescription: it.materialDescription || it.materialCode || '',
        salesQty: Math.abs(Number(it.salesQty || 0)), // Always make quantity positive
        uom: it.uom || 'CS',
        unitPrice: it.unitPrice,
        lineTotal: it.lineTotal,
        isMissing: false,
        itemCreated: false,
      })) : [],
      totalAmount: Number(msg.data?.totalAmount || 0),
      totalDiscountAmount: Number(msg.data?.totalDiscountAmount || 0),
    }
    // Prepare finalize items
    finalize.items = (invoice.value.items || []).map(() => ({ leakages: 0, bursts: 0 }))
    finalize.type = finalize.type || msg.invoiceType || 'purchase'
    // Auto-set billed actual from extracted total
    if (invoice.value.totalAmount && (finalize.billAmount === null || finalize.billAmount === undefined)) {
      finalize.billAmount = invoice.value.totalAmount
    }
    
    // Don't auto-validate - let user validate when ready
  } catch (e) {
    extractError.value = e?.message || 'Failed to extract invoice'
  } finally {
    extracting.value = false
  }
}

const toBase64 = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader()
  reader.onload = () => resolve(String(reader.result))
  reader.onerror = reject
  reader.readAsDataURL(file)
})

function normalizeDateToISO(input) {
  if (!input) return new Date().toISOString().slice(0, 10)
  // Already ISO yyyy-mm-dd
  if (/^\d{4}-\d{2}-\d{2}$/.test(input)) return input
  // dd/mm/yyyy or dd-mm-yyyy or dd.mm.yyyy
  let m = input.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})$/)
  if (m) {
    const d = m[1].padStart(2, '0')
    const mo = m[2].padStart(2, '0')
    const y = m[3]
    // If first is >12, treat as dd/mm; else assume dd/mm as well per requirement
    return `${y}-${mo}-${d}`
  }
  // mm/dd/yyyy (rare). If matches and first <=12, flip.
  m = input.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/)
  if (m) {
    const mo = m[1].padStart(2, '0')
    const d = m[2].padStart(2, '0')
    const y = m[3]
    return `${y}-${mo}-${d}`
  }
  // Fallback: try Date.parse
  const t = Date.parse(input)
  if (!isNaN(t)) return new Date(t).toISOString().slice(0, 10)
  return new Date().toISOString().slice(0, 10)
}

const parseMsg = (obj) => (obj && (obj.message ?? obj)) || {}

const submitInvoice = async () => {
  if (!invoice.value || !finalize.type || isProcessing.value) return
  
  isProcessing.value = true
  submitting.value = true
  
  try {
    const payload = {
      invoiceNumber: invoice.value.invoiceNumber,
      invoiceDate: invoice.value.invoiceDate,
      customerName: 'bntl',
      supplier: finalize.supplierName || 'bntl',
      discount_amount: invoice.value.totalDiscountAmount || 0,
      isReturn: finalize.isReturn,
      items: (invoice.value.items || []).map((it, idx) => ({
        materialCode: it.materialCode,
        materialDescription: it.materialDescription,
        salesQty: it.salesQty,
        uom: it.uom,
        unitPrice: it.unitPrice,
        lineTotal: it.lineTotal,
        ...(finalize.type === 'purchase' ? { leakages: finalize.items[idx]?.leakages || 0, bursts: finalize.items[idx]?.bursts || 0 } : {})
      }))
    }
    if (finalize.type === 'purchase') {
      if (finalize.billAmount) payload.cust_bill_actual_amount = finalize.billAmount
      if (finalize.finalPhotoFile) payload.photo_base64 = await toBase64(finalize.finalPhotoFile)
      const res = await robustFetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.create_purchase_invoice', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ payload })
      })
      const raw = await safeJson(res)
      const j = parseMsg(raw)
      if (!res.ok || !j?.success) throw new Error(j?.error || 'Failed to create Purchase Invoice')
      window.alert(`Purchase Invoice Created: ${j?.name}`)
    } else {
      const res = await robustFetch('/api/method/custom_erp.custom_erp.sales_invoice.api.create_sales_invoice', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ payload })
      })
      const raw = await safeJson(res)
      const j = parseMsg(raw)
      if (!res.ok || !j?.success) throw new Error(j?.error || 'Failed to create Sales Invoice')
      window.alert(`Sales Invoice Created: ${j?.name}`)
    }
  } catch (e) {
    // As a safety net, verify whether the invoice actually got created
    try {
      const verify = await checkForDuplicateInvoice(true)
      if (verify?.existingName) {
        window.alert(`Purchase Invoice Created: ${verify.existingName}`)
      } else {
        throw new Error(e?.message || 'Failed')
      }
    } catch (vErr) {
      window.alert(`Error: ${e?.message || 'Failed'}`)
    }
  } finally {
    submitting.value = false
    isProcessing.value = false
  }
}

const validateItems = async () => {
  try {
    // Reset all item statuses first
    invoice.value.items.forEach(item => {
      item.isMissing = false
      item.itemCreated = false
    })
    
    // Debug: Log what we're sending
    console.log('Sending items for validation:', invoice.value.items)
    console.log('Items type:', typeof invoice.value.items)
    console.log('Items length:', invoice.value.items?.length)
    console.log('JSON stringified:', JSON.stringify(invoice.value.items))
    console.log('Final request body:', JSON.stringify({ items: JSON.stringify(invoice.value.items) }))
    
    const res = await robustFetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.validate_items_master', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: JSON.stringify(invoice.value.items) })
    })
    
    // Debug: Log response
    console.log('Validation response status:', res.status)
    
    const data = await safeJson(res)
    console.log('Validation response data:', data)
    
    const msg = data.message || data
    if (!res.ok || !msg.success) throw new Error(msg.error || 'Validation failed')
    
    // Update item statuses based on validation results
    if (msg.validation && msg.validation.missing_items) {
      msg.validation.missing_items.forEach(missingItem => {
        const item = invoice.value.items.find(it => it.materialCode === missingItem.materialCode)
        if (item) {
          item.isMissing = true
        }
      })
    }
    
    itemValidation.value = msg.validation
    return msg.validation
  } catch (e) {
    console.error('Validation error:', e)
    window.alert(`Validation error: ${e?.message || 'Failed to validate items'}`)
    return { all_valid: false, missing_items: [], valid_items: [] }
  }
}

const showMissingItemsDialog = (missingItems) => {
  // Mark missing items in the UI
  invoice.value.items.forEach((item, index) => {
    const isMissing = missingItems.some(missing => missing.materialCode === item.materialCode)
    item.isMissing = isMissing
  })
  
  const missingCodes = missingItems.map(item => item.materialCode).join(', ')
  const ok = window.confirm(
    `The following items are not found in master data:\n\n${missingCodes}\n\n` +
    `Please add them as new items using the "+" button, or correct the item codes if there are typos.`
  )
}

const openNewItemDialog = (rowIndex) => {
  const item = invoice.value.items[rowIndex]
  newItemData.item_code = item.materialCode
  newItemData.item_name = item.materialDescription
  newItemData.rowIndex = rowIndex
  newItemData.selling_price = item.unitPrice || 0
  newItemData.valuation_price = item.unitPrice || 0
  newItemData.uom_conversion = item.uom === 'CS' ? 6 : 1
  showNewItemDialog.value = true
}

const createNewItem = async () => {
  try {
    const res = await fetch('/api/method/custom_erp.custom_erp.purchase_invoice.api.create_new_item_for_invoice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_data: JSON.stringify(newItemData) })
    })
    const data = await safeJson(res)
    const msg = data.message || data
    if (!res.ok || !msg.success) throw new Error(msg.error || 'Failed to create item')
    
    // Mark item as valid and remove add button
    const rowIndex = newItemData.rowIndex
    if (rowIndex >= 0 && rowIndex < invoice.value.items.length) {
      invoice.value.items[rowIndex].isMissing = false
      invoice.value.items[rowIndex].itemCreated = true
    }
    
    showNewItemDialog.value = false
    window.alert(`Item created successfully: ${msg.item_code}`)
    
    // Re-validate items
    await validateItems()
    
  } catch (e) {
    window.alert(`Error creating item: ${e?.message || 'Failed'}`)
  }
}

const handleItemCodeChange = (item, index) => {
  // Reset item status when code changes
  item.isMissing = false
  item.itemCreated = false
}

const onItemCodeChange = (item, index) => {
  // This function can be called when item code changes to reset status
  handleItemCodeChange(item, index)
}

const resetItemStatuses = () => {
  // Reset all item statuses
  invoice.value.items.forEach(item => {
    item.isMissing = false
    item.itemCreated = false
  })
  itemValidation.value = null
}

const checkForDuplicateInvoice = async (returnName = false) => {
  try {
    const apiEndpoint = finalize.type === 'purchase' 
      ? '/api/method/custom_erp.custom_erp.purchase_invoice.api.check_duplicate_invoice'
      : '/api/method/custom_erp.custom_erp.sales_invoice.api.check_duplicate_invoice'
    
    const res = await robustFetch(apiEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        supplier: finalize.supplierName,
        customer: finalize.supplierName,
        invoice_number: invoice.value.invoiceNumber,
        invoice_date: invoice.value.invoiceDate,
        invoice_type: finalize.type
      })
    })
    
    const raw = await safeJson(res)
    const msg = parseMsg(raw)
    
    if (!res.ok) return { isDuplicate: false }
    
    return { isDuplicate: !!msg.isDuplicate, existingName: msg.existing_invoice || null }
  } catch (e) {
    return { isDuplicate: false }
  }
}

const deleteRow = (index) => {
  if (!invoice.value?.items || index < 0 || index >= invoice.value.items.length) return
  
  // Store the deleted row data for undo
  const deletedRow = {
    index: index,
    item: { ...invoice.value.items[index] },
    finalizeItem: { ...finalize.items[index] }
  }
  
  // Remove from invoice items
  invoice.value.items.splice(index, 1)
  
  // Remove from finalize items
  finalize.items.splice(index, 1)
  
  // Add to deleted rows stack
  deletedRows.value.push(deletedRow)
}

const undoLastDelete = () => {
  if (deletedRows.value.length === 0) return
  
  // Get the last deleted row
  const lastDeleted = deletedRows.value.pop()
  
  // Insert back at the original position
  invoice.value.items.splice(lastDeleted.index, 0, lastDeleted.item)
  finalize.items.splice(lastDeleted.index, 0, lastDeleted.finalizeItem)
}

// Watch for changes in scanned image to ensure proper preview
watch([scannedImageBlob, scannedImageUrl], () => {
  console.log('Scanned image changed:', {
    scannedImageBlob: !!scannedImageBlob.value,
    scannedImageUrl: !!scannedImageUrl.value,
    imagePreviewUrl: imagePreviewUrl.value,
    canExtract: canExtract.value
  })
})

onMounted(() => {
  // ensure auth state already guarded by router; nothing additional for now
})

const confirmAndSubmit = async () => {
  if (!invoice.value || isProcessing.value) return

  // Validate items first
  const validationResult = await validateItems()
  if (!validationResult?.all_valid) {
    showMissingItemsDialog(validationResult?.missing_items || [])
    return
  }

  // Duplicate warning
  const dup = await checkForDuplicateInvoice(true)
  if (dup?.isDuplicate) {
    const proceedDup = window.confirm(
      `A ${finalize.type} invoice already exists with the same details.\n\n` +
      `Supplier: ${finalize.supplierName}\n` +
      `Invoice No: ${invoice.value.invoiceNumber}\n` +
      `Date: ${invoice.value.invoiceDate}\n` +
      `${dup.existingName ? `Existing: ${dup.existingName}\n` : ''}` +
      `Do you want to create it anyway?`
    )
    if (!proceedDup) return
  }

  const lines = [
    `Type: ${finalize.type}`,
    `Purchase Invoice Type: ${finalize.isReturn ? 'Credit Note (Return)' : 'Tax Invoice (Regular)'}`,
    `Invoice No: ${invoice.value.invoiceNumber}`,
    `Date: ${invoice.value.invoiceDate}`,
    `Party: ${invoice.value.customerName}`,
    `Items: ${invoice.value.items.length}`,
    `Billed Actual Total: ${finalize.billAmount ?? ''}`,
  ]
  const ok = window.confirm(`Confirm create ${finalize.type} invoice?\n\n` + lines.join('\n'))
  if (!ok) return

  await submitInvoice()
}
</script>

<style scoped>
/* Ensure table is responsive and scrollable */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* Ensure inputs don't overflow on small screens */
@media (max-width: 640px) {
  .w-16 {
    width: 4rem;
  }
  
  .w-20 {
    width: 5rem;
  }
  
  .w-32 {
    width: 8rem;
  }
  
  .w-48 {
    width: 12rem;
  }
  
  .w-80 {
    width: 20rem;
  }
}

/* Visual indicators for item status */
.bg-red-50 {
  background-color: #fef2f2;
}

.bg-green-50 {
  background-color: #f0fdf4;
}

.border-red-500 {
  border-color: #ef4444;
}

.border-green-500 {
  border-color: #22c55e;
}

/* Add button styling */
.add-button {
  transition: all 0.2s ease-in-out;
}

.add-button:hover {
  transform: scale(1.1);
}

/* Dialog animations */
.fixed {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Drag and drop styling */
.border-dashed {
  transition: all 0.2s ease-in-out;
}

.border-dashed:hover {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.border-dashed.border-blue-400 {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

/* Scanner button styling */
.scanner-button {
  transition: all 0.2s ease-in-out;
}

.scanner-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.scanner-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Image preview styling */
.image-preview {
  transition: all 0.3s ease-in-out;
}

.image-preview:hover {
  transform: scale(1.02);
}

/* Invoice type indication styling */
.invoice-type-indication {
  transition: all 0.2s ease-in-out;
}

.invoice-type-indication:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Checkbox styling */
input[type="checkbox"] {
  transition: all 0.2s ease-in-out;
}

input[type="checkbox"]:checked {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

input[type="checkbox"]:focus {
  outline: none;
  ring: 2px;
  ring-color: #3b82f6;
  ring-offset: 2px;
}

/* Processing state styling */
.processing-state {
  pointer-events: none;
  opacity: 0.7;
}

.processing-state button {
  cursor: not-allowed;
}
</style>


