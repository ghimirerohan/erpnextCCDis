<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Customer Payment Entry View -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50">
    <!-- Header - Mobile Optimized -->
    <header class="bg-white shadow-md border-b-2 border-gray-300 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div class="flex items-center py-3 sm:py-4 gap-2 sm:gap-4">
          <button
            @click="goBack"
            class="inline-flex items-center justify-center p-2 sm:px-3 sm:py-2 border-2 border-gray-300 rounded-md shadow-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 flex-shrink-0"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <div class="min-w-0 flex-1">
            <h1 class="text-base sm:text-lg lg:text-2xl font-bold text-gray-900 truncate">{{ customerName }}</h1>
            <p class="text-xs sm:text-sm text-gray-600 font-mono truncate">{{ customerCode }}</p>
          </div>
        </div>
      </div>
    </header>

    <main v-if="lineData" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <!-- ALREADY SETTLED - Read-only view -->
      <div v-if="lineData.settled" class="space-y-6">
        <div class="bg-green-100 border-2 border-green-500 rounded-xl shadow-lg p-8 text-center">
          <svg class="w-20 h-20 text-green-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h2 class="text-3xl font-bold text-green-900 mb-2">Payment Already Settled</h2>
          <p class="text-lg text-green-700">This customer's payment has been completed and recorded.</p>
        </div>

        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-6">Payment Summary</h3>
          <div class="grid grid-cols-2 gap-6">
            <div class="border-r border-gray-200 pr-6">
              <p class="text-sm text-gray-600 mb-1">Initial Amount</p>
              <p class="text-3xl font-bold text-gray-900">{{ formatCurrency(lineData.initial_total_amount) }}</p>
            </div>
            <div class="pl-6">
              <p class="text-sm text-gray-600 mb-1">Total Collected</p>
              <p class="text-3xl font-bold text-green-600">{{ formatCurrency(getTotalCollected()) }}</p>
            </div>
          </div>

          <div class="mt-8 grid grid-cols-3 gap-4">
            <div v-if="lineData.cash_amount > 0" class="bg-green-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">Cash</p>
              <p class="text-xl font-semibold text-green-700">{{ formatCurrency(lineData.cash_amount) }}</p>
            </div>
            <div v-if="lineData.qr_amount > 0" class="bg-blue-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">QR Payment</p>
              <p class="text-xl font-semibold text-blue-700">{{ formatCurrency(lineData.qr_amount) }}</p>
            </div>
            <div v-if="lineData.cheque_amount > 0" class="bg-purple-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">Cheque</p>
              <p class="text-xl font-semibold text-purple-700">{{ formatCurrency(lineData.cheque_amount) }}</p>
            </div>
            <div v-if="lineData.credit_amount > 0" class="bg-red-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">Credit</p>
              <p class="text-xl font-semibold text-red-700">{{ formatCurrency(lineData.credit_amount) }}</p>
            </div>
            <div v-if="lineData.return_amount > 0" class="bg-orange-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">Return</p>
              <p class="text-xl font-semibold text-orange-700">{{ formatCurrency(lineData.return_amount) }}</p>
            </div>
            <div v-if="lineData.additional_amount > 0" class="bg-indigo-50 rounded-lg p-4">
              <p class="text-xs text-gray-600 mb-1">Additional</p>
              <p class="text-xl font-semibold text-indigo-700">{{ formatCurrency(lineData.additional_amount) }}</p>
            </div>
          </div>
        </div>

        <button
          @click="goBack"
          class="w-full inline-flex items-center justify-center px-6 py-4 border-2 border-gray-300 rounded-lg shadow-sm text-lg font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition-all"
        >
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          Back to List
        </button>
      </div>

      <!-- EDITABLE VIEW - Not yet settled -->
      <template v-else>
        <!-- Amount Summary -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Payment Summary</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Initial Amount</p>
              <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(lineData.initial_total_amount) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Remaining</p>
              <p class="text-2xl font-bold" :class="calculatedRemaining < 0 ? 'text-red-600' : 'text-sky-600'">
                {{ formatCurrency(calculatedRemaining) }}
              </p>
            </div>
          </div>
        </div>

      <!-- Mode Toggle -->
      <div v-if="!paymentCompleted" class="bg-white rounded-xl shadow-lg border border-gray-200 p-4">
        <div class="flex gap-2">
          <button
            @click="entryMode = 'whole'"
            :disabled="paymentInProgress"
            :class="[
              'flex-1 px-4 py-3 rounded-lg font-medium transition-colors',
              entryMode === 'whole' ? 'bg-sky-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              paymentInProgress && 'opacity-50 cursor-not-allowed'
            ]"
          >
            Whole Entry
          </button>
          <button
            @click="entryMode = 'breakdown'"
            :disabled="paymentInProgress"
            :class="[
              'flex-1 px-4 py-3 rounded-lg font-medium transition-colors',
              entryMode === 'breakdown' ? 'bg-sky-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              paymentInProgress && 'opacity-50 cursor-not-allowed'
            ]"
          >
            Breakdown Entry
          </button>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="paymentCompleted" class="bg-green-50 border-2 border-green-500 rounded-xl shadow-lg p-6">
        <div class="flex items-center">
          <svg class="w-12 h-12 text-green-600 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <h3 class="text-lg font-bold text-green-900">Payment Recorded Successfully!</h3>
            <p class="text-sm text-green-700">{{ completedPaymentType }} payment of {{ formatCurrency(lineData.initial_total_amount) }} has been saved.</p>
          </div>
        </div>
      </div>

      <!-- Whole Entry Mode - Mobile Optimized -->
      <div v-if="entryMode === 'whole' && !paymentCompleted" class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6">
        <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Select Payment Method</h3>
        <div class="grid grid-cols-2 gap-3 sm:gap-4">
          <button
            @click="handleWholeEntry('qr')"
            :disabled="paymentInProgress || saving"
            :class="[
              'flex flex-col items-center justify-center p-4 sm:p-6 border-2 rounded-xl transition-colors touch-manipulation min-h-[100px] sm:min-h-[120px]',
              paymentInProgress || saving ? 'opacity-50 cursor-not-allowed border-gray-300' : 'border-blue-300 hover:bg-blue-50 active:bg-blue-100'
            ]"
          >
            <svg class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-blue-600 mb-1 sm:mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path>
            </svg>
            <span class="text-sm sm:text-base lg:text-lg font-medium text-gray-900">QR Payment</span>
            <span class="text-xs sm:text-sm text-gray-600 font-semibold">{{ formatCurrency(lineData.initial_total_amount) }}</span>
          </button>

          <button
            @click="handleWholeEntry('cash')"
            :disabled="paymentInProgress || saving"
            :class="[
              'flex flex-col items-center justify-center p-4 sm:p-6 border-2 rounded-xl transition-colors touch-manipulation min-h-[100px] sm:min-h-[120px]',
              paymentInProgress || saving ? 'opacity-50 cursor-not-allowed border-gray-300' : 'border-green-300 hover:bg-green-50 active:bg-green-100'
            ]"
          >
            <svg class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-green-600 mb-1 sm:mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="text-sm sm:text-base lg:text-lg font-medium text-gray-900">Cash</span>
            <span class="text-xs sm:text-sm text-gray-600 font-semibold">{{ formatCurrency(lineData.initial_total_amount) }}</span>
          </button>

          <button
            @click="handleWholeEntry('cheque')"
            :disabled="paymentInProgress || saving"
            :class="[
              'flex flex-col items-center justify-center p-4 sm:p-6 border-2 rounded-xl transition-colors touch-manipulation min-h-[100px] sm:min-h-[120px]',
              paymentInProgress || saving ? 'opacity-50 cursor-not-allowed border-gray-300' : 'border-purple-300 hover:bg-purple-50 active:bg-purple-100'
            ]"
          >
            <svg class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-purple-600 mb-1 sm:mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <span class="text-sm sm:text-base lg:text-lg font-medium text-gray-900">Cheque</span>
            <span class="text-xs sm:text-sm text-gray-600 font-semibold">{{ formatCurrency(lineData.initial_total_amount) }}</span>
          </button>

          <button
            @click="handleWholeEntry('credit')"
            :disabled="paymentInProgress || saving"
            :class="[
              'flex flex-col items-center justify-center p-4 sm:p-6 border-2 rounded-xl transition-colors touch-manipulation min-h-[100px] sm:min-h-[120px]',
              paymentInProgress || saving ? 'opacity-50 cursor-not-allowed border-gray-300' : 'border-red-300 hover:bg-red-50 active:bg-red-100'
            ]"
          >
            <svg class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-red-600 mb-1 sm:mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
            </svg>
            <span class="text-sm sm:text-base lg:text-lg font-medium text-gray-900">Credit</span>
            <span class="text-xs sm:text-sm text-gray-600 font-semibold">Pay Later</span>
          </button>

          <button
            @click="handleWholeEntry('return')"
            :disabled="paymentInProgress || saving"
            :class="[
              'flex flex-col items-center justify-center p-4 sm:p-6 border-2 rounded-xl transition-colors col-span-2 touch-manipulation min-h-[100px] sm:min-h-[120px]',
              paymentInProgress || saving ? 'opacity-50 cursor-not-allowed border-gray-300' : 'border-orange-300 hover:bg-orange-50 active:bg-orange-100'
            ]"
          >
            <svg class="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-orange-600 mb-1 sm:mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
            </svg>
            <span class="text-sm sm:text-base lg:text-lg font-medium text-gray-900">Return</span>
            <span class="text-xs sm:text-sm text-gray-600 font-semibold">Full Return</span>
          </button>
        </div>
      </div>

      <!-- Breakdown Entry Mode -->
      <div v-if="entryMode === 'breakdown' && !paymentCompleted" class="space-y-4">
        <!-- Validation Error -->
        <div v-if="breakdownValidationError" class="bg-red-50 border-2 border-red-500 rounded-xl shadow-lg p-4">
          <div class="flex items-center">
            <svg class="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-red-900 font-medium">{{ breakdownValidationError }}</p>
          </div>
        </div>

        <!-- Amount Inputs - Mobile Optimized -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Breakdown Amounts</h3>
          
          <div class="space-y-3 sm:space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Return Amount</label>
              <input
                v-model.number="returnAmount"
                @input="validateBreakdown"
                type="number"
                inputmode="decimal"
                min="0"
                :class="[
                  'block w-full px-4 py-3 sm:py-2 text-base sm:text-sm border-2 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 touch-manipulation',
                  breakdownValidationError ? 'border-red-500' : 'border-gray-300'
                ]"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Additional Amount</label>
              <input
                v-model.number="additionalAmount"
                @input="validateBreakdown"
                type="number"
                inputmode="decimal"
                min="0"
                class="block w-full px-4 py-3 sm:py-2 text-base sm:text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 touch-manipulation"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Credit Amount</label>
              <input
                v-model.number="creditAmount"
                @input="validateBreakdown"
                type="number"
                inputmode="decimal"
                min="0"
                :class="[
                  'block w-full px-4 py-3 sm:py-2 text-base sm:text-sm border-2 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 touch-manipulation',
                  breakdownValidationError ? 'border-red-500' : 'border-gray-300'
                ]"
              />
            </div>
          </div>
        </div>

        <!-- Payment Method Buttons for Breakdown - Mobile Optimized -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6">
          <h3 class="text-sm sm:text-base lg:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">
            Payment Methods <span class="block sm:inline text-sky-600">(Remaining: {{ formatCurrency(calculatedRemaining) }})</span>
          </h3>
          <div class="grid grid-cols-3 gap-2 sm:gap-3 lg:gap-4">
            <!-- QR Payment - Mobile Optimized -->
            <div class="relative">
              <button
                @click="handleBreakdownPayment('qr')"
                :disabled="!canSelectPaymentMethod"
                :class="[
                  'w-full flex flex-col items-center justify-center p-3 sm:p-4 border-2 rounded-xl transition-all touch-manipulation min-h-[90px] sm:min-h-[100px]',
                  qrAmount > 0 ? 'border-blue-600 bg-blue-100 shadow-md' : 'border-blue-300 hover:bg-blue-50 active:bg-blue-100',
                  !canSelectPaymentMethod && 'opacity-50 cursor-not-allowed'
                ]"
              >
                <svg class="w-7 h-7 sm:w-8 sm:h-8 lg:w-10 lg:h-10 text-blue-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path>
                </svg>
                <span class="text-xs sm:text-sm font-medium text-gray-900">QR</span>
                <span :class="['font-bold mt-0.5 text-center', qrAmount > 0 ? 'text-base sm:text-lg lg:text-xl text-blue-700' : 'text-xs sm:text-sm text-gray-600']">
                  {{ formatCurrency(qrAmount) }}
                </span>
              </button>
              <!-- PAID Badge -->
              <div v-if="qrAmount > 0" class="absolute -top-1.5 -right-1.5 bg-green-600 text-white text-[10px] sm:text-xs font-extrabold px-2 py-1 sm:px-3 sm:py-1.5 rounded-full shadow-xl border-2 border-white z-10 animate-pulse">
                ✓ PAID
              </div>
            </div>

            <!-- Cash Payment - Mobile Optimized -->
            <div class="relative">
              <button
                @click="handleBreakdownPayment('cash')"
                :disabled="!canSelectPaymentMethod"
                :class="[
                  'w-full flex flex-col items-center justify-center p-3 sm:p-4 border-2 rounded-xl transition-all touch-manipulation min-h-[90px] sm:min-h-[100px]',
                  cashAmount > 0 ? 'border-green-600 bg-green-100 shadow-md' : 'border-green-300 hover:bg-green-50 active:bg-green-100',
                  !canSelectPaymentMethod && 'opacity-50 cursor-not-allowed'
                ]"
              >
                <svg class="w-7 h-7 sm:w-8 sm:h-8 lg:w-10 lg:h-10 text-green-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                <span class="text-xs sm:text-sm font-medium text-gray-900">Cash</span>
                <span :class="['font-bold mt-0.5 text-center', cashAmount > 0 ? 'text-base sm:text-lg lg:text-xl text-green-700' : 'text-xs sm:text-sm text-gray-600']">
                  {{ formatCurrency(cashAmount) }}
                </span>
              </button>
              <!-- PAID Badge -->
              <div v-if="cashAmount > 0" class="absolute -top-1.5 -right-1.5 bg-green-600 text-white text-[10px] sm:text-xs font-extrabold px-2 py-1 sm:px-3 sm:py-1.5 rounded-full shadow-xl border-2 border-white z-10 animate-pulse">
                ✓ PAID
              </div>
            </div>

            <!-- Cheque Payment - Mobile Optimized -->
            <div class="relative">
              <button
                @click="handleBreakdownPayment('cheque')"
                :disabled="!canSelectPaymentMethod"
                :class="[
                  'w-full flex flex-col items-center justify-center p-3 sm:p-4 border-2 rounded-xl transition-all touch-manipulation min-h-[90px] sm:min-h-[100px]',
                  chequeAmount > 0 ? 'border-purple-600 bg-purple-100 shadow-md' : 'border-purple-300 hover:bg-purple-50 active:bg-purple-100',
                  !canSelectPaymentMethod && 'opacity-50 cursor-not-allowed'
                ]"
              >
                <svg class="w-7 h-7 sm:w-8 sm:h-8 lg:w-10 lg:h-10 text-purple-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span class="text-xs sm:text-sm font-medium text-gray-900">Cheque</span>
                <span :class="['font-bold mt-0.5 text-center', chequeAmount > 0 ? 'text-base sm:text-lg lg:text-xl text-purple-700' : 'text-xs sm:text-sm text-gray-600']">
                  {{ formatCurrency(chequeAmount) }}
                </span>
              </button>
              <!-- PAID Badge -->
              <div v-if="chequeAmount > 0" class="absolute -top-1.5 -right-1.5 bg-green-600 text-white text-[10px] sm:text-xs font-extrabold px-2 py-1 sm:px-3 sm:py-1.5 rounded-full shadow-xl border-2 border-white z-10 animate-pulse">
                ✓ PAID
              </div>
            </div>
          </div>
        </div>

        <!-- Complete Payment Button for Breakdown -->
        <div v-if="calculatedRemaining === 0 && !breakdownValidationError" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <button
            @click="completeBreakdownPayment"
            :disabled="saving"
            class="w-full inline-flex items-center justify-center px-6 py-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="!saving" class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <svg v-else class="animate-spin w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ saving ? 'Saving...' : 'Complete Payment & Mark as Settled' }}
          </button>
        </div>
      </div>

      <!-- Complete Payment Button (for Whole Entry) -->
      <div v-if="paymentCompleted" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <button
          @click="completePayment"
          :disabled="saving"
          class="w-full inline-flex items-center justify-center px-6 py-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <svg v-if="!saving" class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <svg v-else class="animate-spin w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ saving ? 'Saving...' : 'Complete Payment & Mark as Settled' }}
        </button>
      </div>
      </template>
    </main>

    <!-- QR Payment Dialog -->
    <QRPaymentDialog
      :show="showQRDialog"
      :customer="customerCode"
      :customer-name="customerName"
      :amount="pendingQRAmount"
      @close="handleQRDialogClose"
      @success="handleQRSuccess"
    />

    <!-- Cheque Capture Dialog -->
    <ChequeCapture
      :show="showChequeDialog"
      :customer="customerCode"
      :customer-name="customerName"
      :amount="pendingChequeAmount"
      @close="handleChequeDialogClose"
      @success="handleChequeSuccess"
    />

    <!-- Success Acknowledgment Dialog -->
    <div v-if="showSuccessDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all">
        <!-- Success Icon -->
        <div class="flex justify-center mb-4">
          <div class="bg-green-100 rounded-full p-3">
            <svg class="w-16 h-16 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>

        <!-- Title -->
        <h2 class="text-2xl font-bold text-gray-900 text-center mb-2">
          {{ successDialogData.title }}
        </h2>
        
        <!-- Subtitle -->
        <p class="text-gray-600 text-center mb-6">
          {{ successDialogData.subtitle }}
        </p>

        <!-- Payment Details -->
        <div class="bg-gray-50 rounded-xl p-4 mb-6 space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-gray-600 font-medium">Customer</span>
            <span class="font-semibold text-gray-900">{{ successDialogData.customerName }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-600 font-medium">Payment Method</span>
            <span class="font-semibold text-gray-900">{{ successDialogData.paymentMethod }}</span>
          </div>
          <div class="flex justify-between items-center border-t pt-3">
            <span class="text-gray-600 font-medium">Amount</span>
            <span class="text-2xl font-bold text-green-600">{{ successDialogData.amount }}</span>
          </div>
          <div v-if="successDialogData.transactionId" class="flex justify-between items-center text-sm">
            <span class="text-gray-500">Transaction ID</span>
            <span class="font-mono text-gray-700">{{ successDialogData.transactionId }}</span>
          </div>
        </div>

        <!-- Action Button -->
        <button
          @click="closeSuccessDialog"
          class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors shadow-lg"
        >
          Continue
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { call } from 'frappe-ui'
import QRPaymentDialog from './components/QRPaymentDialog.vue'
import ChequeCapture from './components/ChequeCapture.vue'

const router = useRouter()
const route = useRoute()

const lineData = ref(null)
const customerName = ref('')
const customerCode = ref('')
const entryMode = ref('whole')

// Payment state
const paymentCompleted = ref(false)
const completedPaymentType = ref('')
const paymentInProgress = ref(false)

// Breakdown amounts
const returnAmount = ref(0)
const additionalAmount = ref(0)
const creditAmount = ref(0)
const cashAmount = ref(0)
const qrAmount = ref(0)
const chequeAmount = ref(0)

// Pending amounts for dialogs
const pendingQRAmount = ref(0)
const pendingChequeAmount = ref(0)

// Dialog states
const showQRDialog = ref(false)
const showChequeDialog = ref(false)
const saving = ref(false)
const showSuccessDialog = ref(false)
const successDialogData = ref({
  title: '',
  subtitle: '',
  customerName: '',
  paymentMethod: '',
  amount: '',
  transactionId: ''
})

// References
const qrTransactionRef = ref(null)
const chequeRef = ref(null)

// Validation
const breakdownValidationError = ref('')

const calculatedRemaining = computed(() => {
  const initial = lineData.value?.initial_total_amount || 0
  return initial + additionalAmount.value - returnAmount.value - creditAmount.value - cashAmount.value - qrAmount.value - chequeAmount.value
})

const canSelectPaymentMethod = computed(() => {
  return calculatedRemaining.value > 0 && !breakdownValidationError.value
})

const loadLineData = async () => {
  try {
    // Get line data from parent reco
    const driverName = route.query.driver
    if (!driverName) {
      console.error('Driver name not found in route query')
      alert('Error: Driver information not found. Please go back and select a driver.')
      return
    }
    
    const response = await call('custom_erp.custom_erp.api.payment_reco.get_driver_reco_data', { driver_name: driverName })
    if (response.success) {
      const lineName = route.params.lineName
      if (!lineName) {
        console.error('Line name not found in route params')
        alert('Error: Payment line information not found. Please go back and select a customer.')
        return
      }
      
      const line = response.data.lines.find(l => l.name === lineName)
      if (line) {
        lineData.value = line
        customerName.value = line.customer_name
        customerCode.value = line.customer
        
        // Update payment amounts from server to ensure UI is in sync
        cashAmount.value = line.cash_amount || 0
        qrAmount.value = line.qr_amount || 0
        chequeAmount.value = line.cheque_amount || 0
        creditAmount.value = line.credit_amount || 0
        returnAmount.value = line.return_amount || 0
        additionalAmount.value = line.additional_amount || 0
        
        // Update payment status
        if (line.settled) {
          paymentCompleted.value = true
        }
      } else {
        console.error('Line not found:', lineName, 'Available lines:', response.data.lines.map(l => l.name))
        alert('Error: Payment line not found. Please refresh the page or go back and try again.')
      }
    } else {
      console.error('API error:', response.message)
      alert('Error loading payment data: ' + response.message)
    }
  } catch (error) {
    console.error('Error loading line data:', error)
    alert('Error loading payment data: ' + (error.message || 'Unknown error'))
  }
}

const handleWholeEntry = async (type) => {
  if (paymentCompleted.value || paymentInProgress.value) return
  
  if (!lineData.value || !lineData.value.initial_total_amount) {
    alert('Error: Payment data not loaded. Please refresh the page.')
    return
  }
  
  const amount = lineData.value.initial_total_amount
  
  switch (type) {
    case 'qr':
      pendingQRAmount.value = amount
      showQRDialog.value = true
      break
      
    case 'cash':
      if (confirm(`Confirm CASH payment of ${formatCurrency(amount)}?\n\nThis will be saved immediately.`)) {
        paymentInProgress.value = true
        await saveWholePayment('cash', amount)
      }
      break
      
    case 'cheque':
      pendingChequeAmount.value = amount
      showChequeDialog.value = true
      break
      
    case 'credit':
      if (confirm(`Mark ${formatCurrency(amount)} as CREDIT?\n\nThis will be saved immediately.`)) {
        paymentInProgress.value = true
        await saveWholePayment('credit', amount)
      }
      break
      
    case 'return':
      if (confirm(`Mark ${formatCurrency(amount)} as RETURN?\n\nThis will be saved immediately.`)) {
        paymentInProgress.value = true
        await saveWholePayment('return', amount)
      }
      break
  }
}

const saveWholePayment = async (type, amount) => {
  try {
    saving.value = true
    
    // Validate lineData exists
    if (!lineData.value || !lineData.value.name) {
      throw new Error('Payment line data not loaded. Please refresh the page.')
    }
    
    const paymentData = {
      line_name: lineData.value.name,
      return_amount: 0,
      additional_amount: 0,
      credit_amount: 0,
      cash_amount: 0,
      qr_amount: 0,
      cheque_amount: 0,
      fonepay_qr_transaction: null,
      cheques_taageta: null,
      remarks: `Whole Entry: ${type.toUpperCase()}`
    }
    
    // Set the appropriate amount - DO NOT update UI state yet
    switch (type) {
      case 'cash':
        paymentData.cash_amount = amount
        break
      case 'credit':
        paymentData.credit_amount = amount
        break
      case 'return':
        paymentData.return_amount = amount
        break
      case 'qr':
        paymentData.qr_amount = amount
        paymentData.fonepay_qr_transaction = qrTransactionRef.value || null
        break
      case 'cheque':
        paymentData.cheque_amount = amount
        paymentData.cheques_taageta = chequeRef.value || null
        break
    }
    
    console.log('📤 Sending payment data:', JSON.stringify(paymentData, null, 2))
    const response = await call('custom_erp.custom_erp.api.payment_reco.update_payment_entry', paymentData)
    console.log('📥 Payment response:', JSON.stringify(response, null, 2))
    
    if (response.success) {
      // Only update UI state AFTER successful API response
      switch (type) {
        case 'cash':
          cashAmount.value = amount
          completedPaymentType.value = 'Cash'
          break
        case 'credit':
          creditAmount.value = amount
          completedPaymentType.value = 'Credit'
          break
        case 'return':
          returnAmount.value = amount
          completedPaymentType.value = 'Return'
          break
        case 'qr':
          qrAmount.value = amount
          completedPaymentType.value = 'QR'
          break
        case 'cheque':
          chequeAmount.value = amount
          completedPaymentType.value = 'Cheque'
          break
      }
      
      // Reload data from server to ensure UI is in sync
      await loadLineData()
      
      paymentCompleted.value = true
      paymentInProgress.value = false
    } else {
      const errorMsg = response.message || 'Unknown error occurred'
      console.error('❌ Payment API error:', errorMsg, response)
      alert('Error saving payment: ' + errorMsg)
      paymentInProgress.value = false
      // Do NOT update any UI state on error
    }
  } catch (error) {
    console.error('❌ Exception saving payment:', error)
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      response: error.response,
      data: error.data
    })
    const errorMsg = error.message || error.toString() || 'Unknown error occurred'
    alert('Error saving payment: ' + errorMsg)
    paymentInProgress.value = false
    // Do NOT update any UI state on error
  } finally {
    saving.value = false
  }
}

const handleQRSuccess = async (data) => {
  console.log('🎉 QR Payment Success!', data)
  
  // Handle both old format (string) and new format (object)
  let transactionId = ''
  if (typeof data === 'object' && data.transactionId) {
    qrTransactionRef.value = data.transactionId
    transactionId = data.transactionId
  } else {
    qrTransactionRef.value = data
    transactionId = data
  }
  
  showQRDialog.value = false
  
  // Save immediately after QR success
  if (entryMode.value === 'whole') {
    paymentInProgress.value = true
    await saveWholePayment('qr', pendingQRAmount.value)
  } else {
    qrAmount.value = pendingQRAmount.value
    
    // Show success acknowledgment dialog for breakdown entry
    showSuccessDialog.value = true
    successDialogData.value = {
      title: 'Payment Successful!',
      subtitle: 'QR payment has been recorded',
      customerName: customerName.value,
      paymentMethod: 'QR Payment',
      amount: formatCurrency(pendingQRAmount.value),
      transactionId: transactionId
    }
  }
}

const handleQRDialogClose = () => {
  showQRDialog.value = false
  pendingQRAmount.value = 0
}

const handleChequeSuccess = async (chequeId) => {
  chequeRef.value = chequeId
  showChequeDialog.value = false
  
  // Save immediately after cheque success
  if (entryMode.value === 'whole') {
    paymentInProgress.value = true
    await saveWholePayment('cheque', pendingChequeAmount.value)
  } else {
    chequeAmount.value = pendingChequeAmount.value
    
    // Show success acknowledgment dialog for breakdown entry
    showSuccessDialog.value = true
    successDialogData.value = {
      title: 'Payment Successful!',
      subtitle: 'Cheque payment has been recorded',
      customerName: customerName.value,
      paymentMethod: 'Cheque',
      amount: formatCurrency(pendingChequeAmount.value),
      transactionId: chequeId
    }
  }
}

const handleChequeDialogClose = () => {
  showChequeDialog.value = false
  pendingChequeAmount.value = 0
}

const closeSuccessDialog = () => {
  showSuccessDialog.value = false
  successDialogData.value = {
    title: '',
    subtitle: '',
    customerName: '',
    paymentMethod: '',
    amount: '',
    transactionId: ''
  }
}

const handleBreakdownPayment = (type) => {
  // Validate before allowing payment selection
  if (breakdownValidationError.value) {
    alert('Please fix the validation errors before selecting a payment method.')
    return
  }

  const remaining = calculatedRemaining.value
  
  switch (type) {
    case 'qr':
      pendingQRAmount.value = remaining
      showQRDialog.value = true
      break
    case 'cash':
      if (confirm(`Confirm cash payment of ${formatCurrency(remaining)}?`)) {
        cashAmount.value += remaining
        
        // Show success acknowledgment dialog for cash payment
        showSuccessDialog.value = true
        successDialogData.value = {
          title: 'Payment Successful!',
          subtitle: 'Cash payment has been recorded',
          customerName: customerName.value,
          paymentMethod: 'Cash',
          amount: formatCurrency(remaining),
          transactionId: ''
        }
      }
      break
    case 'cheque':
      pendingChequeAmount.value = remaining
      showChequeDialog.value = true
      break
  }
}

const validateBreakdown = () => {
  const initial = lineData.value?.initial_total_amount || 0
  const totalReduction = returnAmount.value + creditAmount.value
  
  if (totalReduction > initial) {
    breakdownValidationError.value = `Return + Credit (${formatCurrency(totalReduction)}) cannot exceed Initial Amount (${formatCurrency(initial)})`
  } else {
    breakdownValidationError.value = ''
  }
}

const completeBreakdownPayment = async () => {
  // Validation check
  if (calculatedRemaining.value !== 0) {
    alert('Please ensure the remaining amount is exactly 0 before completing payment.')
    return
  }

  if (breakdownValidationError.value) {
    alert('Please fix validation errors before completing payment.')
    return
  }

  const summary = []
  if (returnAmount.value > 0) summary.push(`Return: ${formatCurrency(returnAmount.value)}`)
  if (additionalAmount.value > 0) summary.push(`Additional: ${formatCurrency(additionalAmount.value)}`)
  if (creditAmount.value > 0) summary.push(`Credit: ${formatCurrency(creditAmount.value)}`)
  if (cashAmount.value > 0) summary.push(`Cash: ${formatCurrency(cashAmount.value)}`)
  if (qrAmount.value > 0) summary.push(`QR: ${formatCurrency(qrAmount.value)}`)
  if (chequeAmount.value > 0) summary.push(`Cheque: ${formatCurrency(chequeAmount.value)}`)

  const confirmMsg = `Complete Breakdown Payment and Mark as Settled?\n\n${summary.join('\n')}\n\nThis action cannot be undone.`
  
  if (!confirm(confirmMsg)) return

  try {
    saving.value = true
    
    // Validate lineData exists
    if (!lineData.value || !lineData.value.name) {
      throw new Error('Payment line data not loaded. Please refresh the page.')
    }
    
    const paymentData = {
      line_name: lineData.value.name,
      return_amount: returnAmount.value || 0,
      additional_amount: additionalAmount.value || 0,
      credit_amount: creditAmount.value || 0,
      cash_amount: cashAmount.value || 0,
      qr_amount: qrAmount.value || 0,
      cheque_amount: chequeAmount.value || 0,
      fonepay_qr_transaction: qrTransactionRef.value || null,
      cheques_taageta: chequeRef.value || null,
      remarks: `Breakdown Entry: ${summary.join(', ')}`
    }
    
    const response = await call('custom_erp.custom_erp.api.payment_reco.update_payment_entry', paymentData)
    
    if (response.success) {
      // Backend automatically marks as settled when remaining is 0
      alert('✅ Payment completed and marked as settled!')
      // Reload data to show settled view
      await loadLineData()
    } else {
      alert('Error completing payment: ' + response.message)
    }
  } catch (error) {
    console.error('Error completing breakdown payment:', error)
    alert('Error completing payment: ' + error.message)
  } finally {
    saving.value = false
  }
}

const getTotalCollected = () => {
  if (!lineData.value) return 0
  return (lineData.value.cash_amount || 0) + 
         (lineData.value.qr_amount || 0) + 
         (lineData.value.cheque_amount || 0)
}

const completePayment = async () => {
  if (!paymentCompleted.value) {
    alert('Please complete a payment method first.')
    return
  }
  
  if (!lineData.value || !lineData.value.initial_total_amount) {
    alert('Error: Payment data not loaded. Please refresh the page.')
    return
  }
  
  if (!confirm(`Complete and mark this payment as SETTLED?\n\nCustomer: ${customerName.value}\nAmount: ${formatCurrency(lineData.value.initial_total_amount)}\nPayment Type: ${completedPaymentType.value}\n\nThis action will finalize the transaction.`)) {
    return
  }
  
  saving.value = true
  try {
    // The payment is already saved, just navigate back
    alert('Payment completed and marked as settled!')
    goBack()
  } catch (error) {
    console.error('Error completing payment:', error)
    alert('Error completing payment: ' + error.message)
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push({ name: 'DailyRecoEntry' })
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}

const formatAmount = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    minimumFractionDigits: 0
  }).format(amount)
}

onMounted(() => {
  loadLineData()
})
</script>
