<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex items-center mb-6">
      <div class="flex items-center justify-center w-10 h-10 bg-indigo-100 rounded-lg mr-3">
        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900">Upload CSV File</h2>
    </div>

    <div
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
      class="relative border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-200"
      :class="dragOver ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        @change="handleFileChange"
        class="hidden"
      />

      <div class="space-y-4">
        <div class="flex justify-center">
          <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>

        <div>
          <p class="text-lg font-medium text-gray-900">
            {{ dragOver ? 'Drop your CSV file here' : 'Drag and drop your CSV file here' }}
          </p>
          <p class="text-sm text-gray-500 mt-2">
            or click to browse
          </p>
        </div>

        <div class="text-xs text-gray-400">
          Accepted format: CSV file with sales invoice data
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-sm text-red-800">{{ error }}</p>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
import { ref } from 'vue'

const emit = defineEmits(['file-uploaded'])

const fileInput = ref(null)
const dragOver = ref(false)
const error = ref(null)

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (file) {
    validateAndEmitFile(file)
  }
}

function handleDrop(event) {
  dragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    validateAndEmitFile(file)
  }
}

function validateAndEmitFile(file) {
  error.value = null

  // Validate file type
  if (!file.name.endsWith('.csv')) {
    error.value = 'Please upload a CSV file'
    return
  }

  // Validate file size (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File size must be less than 10MB'
    return
  }

  emit('file-uploaded', file)
}
</script>

