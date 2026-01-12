<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Summary Card Component -->
<template>
  <div class="rounded-xl shadow-xl p-4 sm:p-6 border-2" style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); border-color: #0284c7;">
    <div class="flex items-center justify-between mb-3 sm:mb-4 gap-2">
      <div class="min-w-0 flex-1">
        <h2 class="text-lg sm:text-xl lg:text-2xl font-bold truncate" style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{{ driverName }}</h2>
        <p class="text-xs sm:text-sm font-semibold truncate" style="color: #ffffff;">{{ formattedBsDate || todayDate }}</p>
        <p v-if="formattedBsDate" class="text-xs mt-0.5 font-medium" style="color: #f0f9ff;">AD: {{ todayDate }}</p>
      </div>
      <div class="flex gap-2 flex-shrink-0 flex-wrap justify-end">
        <!-- Process QR Logs Button -->
        <button
          v-if="unprocessedQrCount > 0"
          @click="openProcessQrDialog"
          class="inline-flex items-center px-2 py-1.5 sm:px-3 sm:py-2 rounded-lg text-xs sm:text-sm font-bold transition-all duration-200 shadow-lg hover:shadow-xl animate-pulse"
          style="border: 2px solid #3b82f6; color: #ffffff; background-color: #3b82f6;"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
          </svg>
          QR ({{ unprocessedQrCount }})
        </button>
        <button
          @click="openExpenseDialog"
          class="inline-flex items-center px-2 py-1.5 sm:px-3 sm:py-2 rounded-lg text-xs sm:text-sm font-bold transition-all duration-200 shadow-lg hover:shadow-xl"
          style="border: 2px solid #fbbf24; color: #92400e; background-color: #fef3c7;"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Expense
        </button>
      <button
        @click="$emit('view-all')"
          class="inline-flex items-center px-2 py-1.5 sm:px-3 sm:py-2 rounded-lg text-xs sm:text-sm font-bold transition-all duration-200 shadow-lg hover:shadow-xl"
        style="border: 2px solid #ffffff; color: #0284c7; background-color: #ffffff;"
      >
        View All
      </button>
      </div>
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-3 lg:gap-4">
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Net Total</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.net_total_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Cash Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.cash_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">QR Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.qr_amount) }}</p>
      </div>
      
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(255, 255, 255, 0.25); border: 2px solid rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px);">
        <p class="text-[10px] sm:text-xs font-bold mb-1" style="color: #ffffff;">Cheque Collected</p>
        <p class="text-sm sm:text-base lg:text-lg font-bold truncate" style="color: #ffffff;">{{ formatCurrency(summary.cheque_amount) }}</p>
      </div>
    </div>
    
    <!-- Expense Row -->
    <div v-if="summary.expense_amount > 0" class="mt-2 sm:mt-3">
      <div class="rounded-lg p-2 sm:p-3 shadow-lg" style="background-color: rgba(251, 191, 36, 0.3); border: 2px solid rgba(251, 191, 36, 0.6); backdrop-filter: blur(10px);">
        <div class="grid grid-cols-3 gap-2">
          <div class="text-center">
            <p class="text-[10px] sm:text-xs font-bold" style="color: #ffffff;">Expense</p>
            <p class="text-sm sm:text-base font-bold" style="color: #fef3c7;">- {{ formatCurrency(summary.expense_amount) }}</p>
          </div>
          <div class="text-center border-l border-r" style="border-color: rgba(255,255,255,0.3);">
            <p class="text-[10px] sm:text-xs font-bold" style="color: #ffffff;">Cash Expected</p>
            <p class="text-sm sm:text-base font-bold" style="color: #bbf7d0;">{{ formatCurrency(cashExpectedValue) }}</p>
          </div>
          <div class="text-center">
            <p class="text-[10px] sm:text-xs font-bold" style="color: #ffffff;">Cash Difference</p>
            <p class="text-sm sm:text-base font-bold" :style="{ color: (summary.cash_difference || 0) >= 0 ? '#bbf7d0' : '#fca5a5' }">
              {{ (summary.cash_difference || 0) >= 0 ? '+' : '' }}{{ formatCurrency(summary.cash_difference || 0) }}
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Cash Received & Difference Row -->
    <div class="mt-2 sm:mt-3">
      <div class="rounded-lg p-2 sm:p-3 shadow-lg cursor-pointer hover:opacity-90 transition-opacity" 
           @click="openCashReceivedDialog"
           style="background-color: rgba(34, 197, 94, 0.3); border: 2px solid rgba(34, 197, 94, 0.6); backdrop-filter: blur(10px);">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-[10px] sm:text-xs font-bold" style="color: #ffffff;">Cash Received</p>
            <p class="text-sm sm:text-base font-bold" style="color: #bbf7d0;">{{ formatCurrency(summary.cash_received || 0) }}</p>
          </div>
          <div class="text-right">
            <p class="text-[10px] sm:text-xs font-bold" style="color: #ffffff;">Cash Difference</p>
            <p class="text-sm sm:text-base font-bold" :style="{ color: (summary.cash_difference || 0) >= 0 ? '#bbf7d0' : '#fca5a5' }">
              {{ (summary.cash_difference || 0) >= 0 ? '+' : '' }}{{ formatCurrency(summary.cash_difference || 0) }}
            </p>
          </div>
        </div>
        <p class="text-[10px] mt-1 text-center" style="color: rgba(255,255,255,0.8);">Tap to enter cash received</p>
      </div>
    </div>
    
    <div class="mt-3 sm:mt-4 pt-3 sm:pt-4" style="border-top: 2px solid rgba(255, 255, 255, 0.5);">
      <div class="flex justify-between items-center gap-2">
        <span class="font-bold text-base sm:text-lg lg:text-xl" style="color: #ffffff;">Remaining</span>
        <span class="text-xl sm:text-2xl lg:text-3xl font-bold truncate" style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{{ formatCurrency(summary.remaining_amount) }}</span>
      </div>
    </div>
  </div>
  
  <!-- Expense Input Dialog -->
  <div v-if="showExpenseDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="expense-modal" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeExpenseDialog"></div>

      <div class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md w-full">
        <div class="bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-4">
          <h3 class="text-lg font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Record Expense
          </h3>
          <p class="text-amber-100 text-sm mt-1">Expense will be deducted from cash collected</p>
        </div>
        
        <div class="bg-white px-4 py-5 sm:p-6">
          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Current Cash Balance</label>
            <div class="text-2xl font-bold text-green-600">{{ formatCurrency(summary.cash_amount) }}</div>
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Current Expense</label>
            <div class="text-lg font-semibold text-amber-600">{{ formatCurrency(summary.expense_amount || 0) }}</div>
          </div>
          
          <div>
            <label for="expense-amount" class="block text-sm font-semibold text-gray-700 mb-2">
              Total Expense Amount <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">NPR</span>
              <input
                id="expense-amount"
                v-model.number="expenseInput"
                type="number"
                min="0"
                :max="maxExpense"
                step="1"
                placeholder="0"
                class="block w-full pl-14 pr-4 py-3 text-lg font-semibold border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-all"
                @keyup.enter="saveExpense"
              />
            </div>
            <p class="mt-1 text-xs text-gray-500">Maximum: {{ formatCurrency(maxExpense) }}</p>
          </div>
          
          <div v-if="expenseError" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ expenseError }}</p>
          </div>
        </div>
        
        <div class="bg-gray-50 px-4 py-3 sm:px-6 flex flex-col sm:flex-row-reverse gap-2">
          <button
            type="button"
            @click="saveExpense"
            :disabled="savingExpense"
            class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-4 py-2.5 bg-amber-600 text-base font-semibold text-white hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="savingExpense" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ savingExpense ? 'Saving...' : 'Save Expense' }}
          </button>
          <button
            type="button"
            @click="closeExpenseDialog"
            class="w-full sm:w-auto inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-4 py-2.5 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Process QR Logs Dialog -->
  <div v-if="showProcessQrDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="qr-process-modal" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeProcessQrDialog"></div>

      <div class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg w-full">
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-4">
          <h3 class="text-lg font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
            </svg>
            Process QR Payments
          </h3>
          <p class="text-blue-100 text-sm mt-1">Process successful QR transactions</p>
        </div>
        
        <div class="bg-white px-4 py-5 sm:p-6">
          <!-- Before Processing -->
          <div v-if="!qrProcessResults" class="space-y-4">
            <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-blue-700 font-medium">Unprocessed QR Logs</span>
                <span class="text-2xl font-bold text-blue-600">{{ unprocessedQrCount }}</span>
              </div>
              <div class="flex justify-between items-center mt-2">
                <span class="text-blue-600 text-sm">Total Amount</span>
                <span class="font-semibold text-blue-700">{{ formatCurrency(unprocessedQrAmount) }}</span>
              </div>
            </div>
            
            <div class="p-3 bg-amber-50 border border-amber-200 rounded-lg">
              <p class="text-sm text-amber-800">
                <strong>Note:</strong> If QR amount exceeds the line's initial amount, 
                the difference will be added to the <strong>Additional Amount</strong> field.
              </p>
            </div>
          </div>
          
          <!-- After Processing - Results -->
          <div v-else class="space-y-4">
            <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
              <div class="flex items-center mb-2">
                <svg class="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span class="font-bold text-green-700">Processing Complete!</span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span class="text-green-600">Success:</span>
                  <span class="font-semibold text-green-700">{{ qrProcessResults.summary?.success_count || 0 }}</span>
                </div>
                <div v-if="qrProcessResults.summary?.error_count > 0">
                  <span class="text-red-600">Errors:</span>
                  <span class="font-semibold text-red-700">{{ qrProcessResults.summary.error_count }}</span>
                </div>
                <div>
                  <span class="text-green-600">QR Applied:</span>
                  <span class="font-semibold">{{ formatCurrency(qrProcessResults.summary?.total_qr_applied || 0) }}</span>
                </div>
                <div v-if="qrProcessResults.summary?.total_additional > 0">
                  <span class="text-indigo-600">Additional:</span>
                  <span class="font-semibold text-indigo-700">{{ formatCurrency(qrProcessResults.summary.total_additional) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Processed Items List -->
            <div v-if="qrProcessResults.processed?.length > 0" class="max-h-48 overflow-y-auto">
              <p class="text-sm font-semibold text-gray-700 mb-2">Processed Transactions:</p>
              <div class="space-y-2">
                <div v-for="item in qrProcessResults.processed" :key="item.qr_name" 
                     :class="['p-2 rounded-lg text-sm', item.status === 'success' ? 'bg-green-50' : 'bg-red-50']">
                  <div class="flex justify-between">
                    <span class="font-medium">{{ item.customer_name || item.customer }}</span>
                    <span :class="item.status === 'success' ? 'text-green-600' : 'text-red-600'">
                      {{ formatCurrency(item.qr_amount) }}
                    </span>
                  </div>
                  <div v-if="item.additional_from_qr > 0" class="text-xs text-indigo-600">
                    +{{ formatCurrency(item.additional_from_qr) }} additional
                  </div>
                  <div v-if="item.status === 'error'" class="text-xs text-red-600">
                    Error: {{ item.error }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="qrProcessError" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ qrProcessError }}</p>
          </div>
        </div>
        
        <div class="bg-gray-50 px-4 py-3 sm:px-6 flex flex-col sm:flex-row-reverse gap-2">
          <button
            v-if="!qrProcessResults"
            type="button"
            @click="processQrLogs"
            :disabled="processingQr || unprocessedQrCount === 0"
            class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-4 py-2.5 bg-blue-600 text-base font-semibold text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="processingQr" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ processingQr ? 'Processing...' : 'Process QR Logs' }}
          </button>
          <button
            type="button"
            @click="closeProcessQrDialog"
            class="w-full sm:w-auto inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-4 py-2.5 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
          >
            {{ qrProcessResults ? 'Close' : 'Cancel' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Cash Received Input Dialog -->
  <div v-if="showCashReceivedDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="cash-received-modal" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeCashReceivedDialog"></div>

      <div class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md w-full">
        <div class="bg-gradient-to-r from-green-500 to-emerald-600 px-4 py-4">
          <h3 class="text-lg font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            Record Cash Received
          </h3>
          <p class="text-green-100 text-sm mt-1">Enter actual cash received from driver</p>
        </div>
        
        <div class="bg-white px-4 py-5 sm:p-6">
          <div class="mb-4 p-3 bg-gray-50 rounded-lg">
            <div class="flex justify-between items-center mb-2">
              <label class="text-sm font-semibold text-gray-700">Total Cash (after expense)</label>
              <span class="text-lg font-bold text-gray-900">{{ formatCurrency(totalCashAfterExpense) }}</span>
            </div>
            <p class="text-xs text-gray-500">This is the expected cash = Cash Collected - Expense</p>
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Current Cash Received</label>
            <div class="text-lg font-semibold text-green-600">{{ formatCurrency(summary.cash_received || 0) }}</div>
          </div>
          
          <div>
            <label for="cash-received-amount" class="block text-sm font-semibold text-gray-700 mb-2">
              Cash Received Amount <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">NPR</span>
              <input
                id="cash-received-amount"
                v-model.number="cashReceivedInput"
                type="number"
                min="0"
                step="1"
                placeholder="0"
                class="block w-full pl-14 pr-4 py-3 text-lg font-semibold border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all"
                @keyup.enter="saveCashReceived"
              />
            </div>
          </div>
          
          <!-- Live Difference Preview -->
          <div v-if="cashReceivedInput > 0" class="mt-4 p-3 rounded-lg" :class="cashDifferencePreview >= 0 ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium" :class="cashDifferencePreview >= 0 ? 'text-green-700' : 'text-red-700'">Cash Difference</span>
              <span class="text-lg font-bold" :class="cashDifferencePreview >= 0 ? 'text-green-700' : 'text-red-700'">
                {{ cashDifferencePreview >= 0 ? '+' : '' }}{{ formatCurrency(cashDifferencePreview) }}
              </span>
            </div>
            <p class="text-xs mt-1" :class="cashDifferencePreview >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ cashDifferencePreview >= 0 ? 'Surplus: More cash received than expected' : 'Shortage: Less cash received than expected' }}
            </p>
          </div>
          
          <div v-if="cashReceivedError" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ cashReceivedError }}</p>
          </div>
        </div>
        
        <div class="bg-gray-50 px-4 py-3 sm:px-6 flex flex-col sm:flex-row-reverse gap-2">
          <button
            type="button"
            @click="saveCashReceived"
            :disabled="savingCashReceived"
            class="w-full sm:w-auto inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-4 py-2.5 bg-green-600 text-base font-semibold text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="savingCashReceived" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ savingCashReceived ? 'Saving...' : 'Save Cash Received' }}
          </button>
          <button
            type="button"
            @click="closeCashReceivedDialog"
            class="w-full sm:w-auto inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-4 py-2.5 bg-white text-base font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  driverName: {
    type: String,
    required: true
  },
  summary: {
    type: Object,
    required: true
  },
  recoName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['view-all', 'expense-updated', 'qr-processed'])

const formattedBsDate = ref('')
const showExpenseDialog = ref(false)
const expenseInput = ref(0)
const savingExpense = ref(false)
const expenseError = ref('')

// Cash received state
const showCashReceivedDialog = ref(false)
const cashReceivedInput = ref(0)
const savingCashReceived = ref(false)
const cashReceivedError = ref('')

// QR Processing state
const showProcessQrDialog = ref(false)
const unprocessedQrCount = ref(0)
const unprocessedQrAmount = ref(0)
const processingQr = ref(false)
const qrProcessError = ref('')
const qrProcessResults = ref(null)

const todayDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

// Maximum expense is the sum of current cash + current expense (since expense comes from cash)
const maxExpense = computed(() => {
  const currentCash = props.summary.cash_amount || 0
  const currentExpense = props.summary.expense_amount || 0
  return currentCash + currentExpense
})

// Cash Expected = Cash Amount - Expense Amount
const cashExpectedValue = computed(() => {
  // Use the value from backend if available, otherwise calculate
  if (props.summary.cash_expected !== undefined && props.summary.cash_expected !== null) {
    return props.summary.cash_expected
  }
  return (props.summary.cash_amount || 0) - (props.summary.expense_amount || 0)
})

// Total cash after expense (the expected cash to receive)
const totalCashAfterExpense = computed(() => {
  return cashExpectedValue.value
})

// Live preview of cash difference
const cashDifferencePreview = computed(() => {
  return (cashReceivedInput.value || 0) - cashExpectedValue.value
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}

const openExpenseDialog = () => {
  expenseInput.value = props.summary.expense_amount || 0
  expenseError.value = ''
  showExpenseDialog.value = true
}

const closeExpenseDialog = () => {
  showExpenseDialog.value = false
  expenseError.value = ''
}

const saveExpense = async () => {
  if (expenseInput.value < 0) {
    expenseError.value = 'Expense amount cannot be negative'
    return
  }
  
  if (expenseInput.value > maxExpense.value) {
    expenseError.value = `Expense cannot exceed available cash (${formatCurrency(maxExpense.value)})`
    return
  }
  
  savingExpense.value = true
  expenseError.value = ''
  
  try {
    const response = await call('custom_erp.api.payment_reco.save_expense_amount', {
      reco_name: props.recoName,
      expense_amount: expenseInput.value
    })
    
    if (response.success) {
      emit('expense-updated', response.data)
      closeExpenseDialog()
    } else {
      expenseError.value = response.message || 'Failed to save expense'
    }
  } catch (error) {
    console.error('Error saving expense:', error)
    expenseError.value = 'Failed to save expense. Please try again.'
  } finally {
    savingExpense.value = false
  }
}

// Cash Received Dialog functions
const openCashReceivedDialog = () => {
  cashReceivedInput.value = props.summary.cash_received || 0
  cashReceivedError.value = ''
  showCashReceivedDialog.value = true
}

const closeCashReceivedDialog = () => {
  showCashReceivedDialog.value = false
  cashReceivedError.value = ''
}

const saveCashReceived = async () => {
  if (cashReceivedInput.value < 0) {
    cashReceivedError.value = 'Cash received amount cannot be negative'
    return
  }
  
  savingCashReceived.value = true
  cashReceivedError.value = ''
  
  try {
    const response = await call('custom_erp.api.payment_reco.save_cash_received', {
      reco_name: props.recoName,
      cash_received: cashReceivedInput.value
    })
    
    if (response.success) {
      emit('expense-updated', response.data)
      closeCashReceivedDialog()
    } else {
      cashReceivedError.value = response.message || 'Failed to save cash received'
    }
  } catch (error) {
    console.error('Error saving cash received:', error)
    cashReceivedError.value = 'Failed to save cash received. Please try again.'
  } finally {
    savingCashReceived.value = false
  }
}

const loadNepaliDate = async () => {
  try {
    const response = await call('custom_erp.api.payment_reco.get_current_nepali_date')
    if (response.success) {
      formattedBsDate.value = response.data.formatted
    }
  } catch (error) {
    console.warn('Failed to load Nepali date:', error)
  }
}

// QR Processing functions
const loadQrCount = async () => {
  try {
    const response = await call('custom_erp.api.payment_reco.get_unprocessed_qr_count_for_reco', {
      reco_name: props.recoName
    })
    if (response.success) {
      unprocessedQrCount.value = response.data.count || 0
      unprocessedQrAmount.value = response.data.total_amount || 0
    }
  } catch (error) {
    console.warn('Failed to load QR count:', error)
  }
}

const openProcessQrDialog = () => {
  qrProcessError.value = ''
  qrProcessResults.value = null
  showProcessQrDialog.value = true
}

const closeProcessQrDialog = () => {
  showProcessQrDialog.value = false
  qrProcessError.value = ''
  // If we processed something, emit event to refresh parent
  if (qrProcessResults.value && qrProcessResults.value.summary?.success_count > 0) {
    emit('qr-processed', qrProcessResults.value)
  }
  qrProcessResults.value = null
  // Reload the count
  loadQrCount()
}

const processQrLogs = async () => {
  processingQr.value = true
  qrProcessError.value = ''
  
  try {
    const response = await call('custom_erp.api.payment_reco.process_qr_logs_for_reco', {
      reco_name: props.recoName
    })
    
    if (response.success) {
      qrProcessResults.value = response.data
      // Emit to update parent summary
      if (response.data.summary?.success_count > 0) {
        emit('expense-updated', {
          qr_amount: response.data.summary.new_qr_amount,
          additional_amount: response.data.summary.new_additional_amount,
          remaining_amount: response.data.summary.new_remaining_amount
        })
      }
    } else {
      qrProcessError.value = response.message || 'Failed to process QR logs'
    }
  } catch (error) {
    console.error('Error processing QR logs:', error)
    qrProcessError.value = 'Failed to process QR logs. Please try again.'
  } finally {
    processingQr.value = false
  }
}

onMounted(() => {
  loadNepaliDate()
  loadQrCount()
})
</script>

