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
        <div v-if="breakdownValidationError" class="bg-red-50 border-2 border-red-500 rounded-xl shadow-lg p-4">
          <div class="flex items-center">
            <svg class="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-red-900 font-medium">{{ breakdownValidationError }}</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-1">Adjustments</h3>
          <p class="text-xs sm:text-sm text-gray-500 mb-3">Return, additional, and credit first. Remaining is then split across cash, QR, and cheque.</p>

          <div class="space-y-3 sm:space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Return Amount</label>
              <input
                v-model.number="returnAmount"
                @input="onBreakdownInput"
                type="number"
                inputmode="decimal"
                min="0"
                :disabled="breakdownLocked"
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
                @input="onBreakdownInput"
                type="number"
                inputmode="decimal"
                min="0"
                :disabled="breakdownLocked"
                class="block w-full px-4 py-3 sm:py-2 text-base sm:text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 touch-manipulation"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Credit Amount</label>
              <input
                v-model.number="creditAmount"
                @input="onBreakdownInput"
                type="number"
                inputmode="decimal"
                min="0"
                :disabled="breakdownLocked"
                :class="[
                  'block w-full px-4 py-3 sm:py-2 text-base sm:text-sm border-2 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 touch-manipulation',
                  breakdownValidationError ? 'border-red-500' : 'border-gray-300'
                ]"
              />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6">
          <div class="flex items-start justify-between gap-3 mb-3">
            <div>
              <h3 class="text-sm sm:text-base lg:text-lg font-semibold text-gray-900">Collect as cash / QR / cheque</h3>
              <p class="text-xs sm:text-sm text-gray-500 mt-1">Split the amount to collect. QR opens Fonepay live; cheque asks for date and details.</p>
            </div>
            <span
              :class="[
                'shrink-0 text-sm font-bold px-3 py-1 rounded-full',
                calculatedRemaining === 0 ? 'bg-green-100 text-green-800' : 'bg-sky-100 text-sky-800'
              ]"
            >
              {{ calculatedRemaining === 0 ? 'Balanced' : formatCurrency(calculatedRemaining) }}
            </span>
          </div>

          <div class="space-y-3">
            <div
              :class="[
                'relative rounded-xl border-2 p-3 sm:p-4',
                cashAmount > 0 ? 'border-green-500 bg-green-50' : 'border-green-200'
              ]"
            >
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm font-semibold text-gray-900">Cash</label>
                <button
                  type="button"
                  class="text-xs font-medium text-green-700 underline disabled:opacity-40"
                  :disabled="breakdownLocked || calculatedRemaining + num(cashAmount) <= 0"
                  @click="fillRemaining('cash')"
                >
                  Fill rest
                </button>
              </div>
              <input
                v-model.number="cashAmount"
                @input="onBreakdownInput"
                type="number"
                inputmode="decimal"
                min="0"
                :disabled="breakdownLocked"
                class="block w-full px-4 py-3 text-base border-2 border-green-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 touch-manipulation"
              />
            </div>

            <div
              :class="[
                'relative rounded-xl border-2 p-3 sm:p-4',
                qrProcessed ? 'border-blue-600 bg-blue-50' : qrAmount > 0 ? 'border-blue-400 bg-blue-50/60' : 'border-blue-200'
              ]"
            >
              <div v-if="qrProcessed" class="absolute -top-2 -right-2 bg-green-600 text-white text-[10px] font-extrabold px-2 py-1 rounded-full shadow border-2 border-white">
                QR PAID
              </div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm font-semibold text-gray-900">Fonepay QR</label>
                <button
                  type="button"
                  class="text-xs font-medium text-blue-700 underline disabled:opacity-40"
                  :disabled="breakdownLocked || qrProcessed || calculatedRemaining + num(qrAmount) <= 0"
                  @click="fillRemaining('qr')"
                >
                  Fill rest
                </button>
              </div>
              <input
                v-model.number="qrAmount"
                @input="onQrAmountInput"
                type="number"
                inputmode="numeric"
                min="0"
                step="1"
                :disabled="breakdownLocked || qrProcessed"
                class="block w-full px-4 py-3 text-base border-2 border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 touch-manipulation"
              />
              <p class="mt-1 text-xs text-blue-700">Fonepay only accepts whole rupees. Paisa is rounded up (e.g. 150.37 → 151). A live QR is shown and must succeed before saving.</p>
            </div>

            <div
              :class="[
                'relative rounded-xl border-2 p-3 sm:p-4',
                chequeProcessed ? 'border-purple-600 bg-purple-50' : chequeAmount > 0 ? 'border-purple-400 bg-purple-50/60' : 'border-purple-200'
              ]"
            >
              <div v-if="chequeProcessed" class="absolute -top-2 -right-2 bg-green-600 text-white text-[10px] font-extrabold px-2 py-1 rounded-full shadow border-2 border-white">
                CHEQUE SAVED
              </div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm font-semibold text-gray-900">Cheque</label>
                <button
                  type="button"
                  class="text-xs font-medium text-purple-700 underline disabled:opacity-40"
                  :disabled="breakdownLocked || chequeProcessed || calculatedRemaining + num(chequeAmount) <= 0"
                  @click="fillRemaining('cheque')"
                >
                  Fill rest
                </button>
              </div>
              <input
                v-model.number="chequeAmount"
                @input="onBreakdownInput"
                type="number"
                inputmode="decimal"
                min="0"
                :disabled="breakdownLocked || chequeProcessed"
                class="block w-full px-4 py-3 text-base border-2 border-purple-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 touch-manipulation"
              />
              <p class="mt-1 text-xs text-purple-700">If this has an amount, cheque number, Nepali date, and institute are captured next.</p>
            </div>
          </div>
        </div>

        <div
          v-if="breakdownProcessing"
          class="bg-sky-50 border border-sky-200 rounded-xl p-4 text-sm text-sky-900"
        >
          <p class="font-semibold mb-2">Processing split</p>
          <ol class="list-decimal list-inside space-y-1">
            <li v-if="num(qrAmount) > 0" :class="qrProcessed ? 'text-green-700' : 'font-medium'">
              QR {{ formatCurrency(qrAmount) }} — {{ qrProcessed ? 'paid' : 'scan Fonepay now' }}
            </li>
            <li v-if="num(chequeAmount) > 0" :class="chequeProcessed ? 'text-green-700' : (qrProcessed || num(qrAmount) === 0 ? 'font-medium' : '')">
              Cheque {{ formatCurrency(chequeAmount) }} — {{ chequeProcessed ? 'details saved' : 'enter date and details' }}
            </li>
            <li>Save and mark settled</li>
          </ol>
        </div>

        <div v-if="canProcessBreakdown" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <button
            @click="startBreakdownProcess"
            :disabled="saving || breakdownProcessing"
            class="w-full inline-flex items-center justify-center px-6 py-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="!saving && !breakdownProcessing" class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <svg v-else class="animate-spin w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ processButtonLabel }}
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
      :line-name="lineData?.name"
      :company="company"
      :company-config="companyConfig"
      @close="handleQRDialogClose"
      @success="handleQRSuccess"
    />

    <!-- Cheque Capture Dialog -->
    <ChequeCapture
      :show="showChequeDialog"
      :customer="customerCode"
      :customer-name="customerName"
      :amount="pendingChequeAmount"
      :company="company"
      @close="handleChequeDialogClose"
      @success="handleChequeSuccess"
    />

    <!-- Non-blocking QR success banner — cheque capture can open underneath -->
    <Teleport to="body">
      <div
        v-if="qrSuccessToast.show"
        class="fixed top-3 left-3 right-3 sm:left-1/2 sm:right-auto sm:-translate-x-1/2 sm:w-[min(28rem,calc(100%-1.5rem))] z-[80] pointer-events-none"
        role="status"
        aria-live="polite"
      >
        <div class="pointer-events-auto flex items-start gap-3 rounded-xl border-2 border-green-600 bg-green-50 px-4 py-3 shadow-2xl">
          <div class="flex-shrink-0 mt-0.5">
            <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-bold text-green-900">QR payment succeeded</p>
            <p class="text-sm text-green-800 mt-0.5">
              Fonepay QR of <span class="font-semibold">{{ formatCurrency(qrSuccessToast.amount) }}</span> is recorded.
              <span v-if="showChequeDialog"> Continue with cheque details below.</span>
            </p>
          </div>
          <button
            type="button"
            class="flex-shrink-0 text-green-700 hover:text-green-900 p-1"
            aria-label="Dismiss"
            @click="dismissQrSuccessToast"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </Teleport>

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

    <!-- Payment Confirmation Dialog -->
    <div v-if="showConfirmDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all">
        <!-- Icon -->
        <div class="flex justify-center mb-4">
          <div :class="[
            'rounded-full p-3',
            confirmDialogData.type === 'cash' ? 'bg-green-100' :
            confirmDialogData.type === 'credit' ? 'bg-red-100' :
            confirmDialogData.type === 'return' ? 'bg-orange-100' : 'bg-gray-100'
          ]">
            <!-- Cash Icon -->
            <svg v-if="confirmDialogData.type === 'cash'" class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <!-- Credit Icon -->
            <svg v-else-if="confirmDialogData.type === 'credit'" class="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
            </svg>
            <!-- Return Icon -->
            <svg v-else-if="confirmDialogData.type === 'return'" class="w-12 h-12 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
            </svg>
          </div>
        </div>

        <!-- Title -->
        <h2 class="text-xl font-bold text-gray-900 text-center mb-2">
          {{ confirmDialogData.title }}
        </h2>
        
        <!-- Subtitle -->
        <p class="text-gray-600 text-center mb-4">
          {{ confirmDialogData.message }}
        </p>

        <!-- Payment Details -->
        <div class="bg-gray-50 rounded-xl p-4 mb-6 space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-gray-600 font-medium">Customer</span>
            <span class="font-semibold text-gray-900">{{ customerName }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-600 font-medium">Customer Code</span>
            <span class="font-mono text-gray-700">{{ customerCode }}</span>
          </div>
          <div class="flex justify-between items-center border-t pt-3">
            <span class="text-gray-600 font-medium">Amount</span>
            <span :class="[
              'text-2xl font-bold',
              confirmDialogData.type === 'cash' ? 'text-green-600' :
              confirmDialogData.type === 'credit' ? 'text-red-600' :
              confirmDialogData.type === 'return' ? 'text-orange-600' : 'text-gray-900'
            ]">{{ formatCurrency(confirmDialogData.amount) }}</span>
          </div>
        </div>

        <!-- Warning Note -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-6">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <p class="text-sm text-yellow-800">
              This action will be saved immediately and cannot be undone.
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3">
          <button
            @click="closeConfirmDialog"
            class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            @click="executeConfirmedPayment"
            :disabled="paymentInProgress"
            :class="[
              'flex-1 font-semibold py-3 px-6 rounded-lg transition-colors shadow-lg text-white',
              confirmDialogData.type === 'cash' ? 'bg-green-600 hover:bg-green-700' :
              confirmDialogData.type === 'credit' ? 'bg-red-600 hover:bg-red-700' :
              confirmDialogData.type === 'return' ? 'bg-orange-600 hover:bg-orange-700' : 'bg-gray-600 hover:bg-gray-700',
              paymentInProgress ? 'opacity-50 cursor-not-allowed' : ''
            ]"
          >
            {{ paymentInProgress ? 'Processing...' : 'Confirm' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { call } from 'frappe-ui'
import QRPaymentDialog from './components/QRPaymentDialog.vue'
import ChequeCapture from './components/ChequeCapture.vue'
import { isStaticQrMode } from './config/qrPaymentMode'
import { callUpdatePaymentEntry, getCachedDriverReco } from './offline/recoOffline'
import { ceilFonepayAmount } from '../../shared/utils/fonepayAmount'

const router = useRouter()
const route = useRoute()

const lineData = ref(null)
const customerName = ref('')
const customerCode = ref('')
const entryMode = ref('whole')
const company = ref('')  // Track company for Fonepay API selection
const companyConfig = ref(null)  // Company config for dynamic styling and API selection

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
const qrProcessed = ref(false)
const chequeProcessed = ref(false)
const breakdownProcessing = ref(false)
const qrSuccessToast = ref({ show: false, amount: 0 })
let qrSuccessToastTimer = null

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

// Confirmation dialog for Cash/Credit/Return
const showConfirmDialog = ref(false)
const confirmDialogData = ref({
  type: '',
  title: '',
  message: '',
  amount: 0,
  icon: '',
  iconColor: '',
  buttonColor: ''
})

// References
const qrTransactionRef = ref(null)
const pendingQrRemarks = ref('')
const chequeRef = ref(null)

// Validation
const breakdownValidationError = ref('')

const num = (value) => {
  const n = Number(value)
  return Number.isFinite(n) ? n : 0
}

const calculatedRemaining = computed(() => {
  const initial = num(lineData.value?.initial_total_amount)
  return (
    initial +
    num(additionalAmount.value) -
    num(returnAmount.value) -
    num(creditAmount.value) -
    num(cashAmount.value) -
    num(qrAmount.value) -
    num(chequeAmount.value)
  )
})

const breakdownLocked = computed(() => breakdownProcessing.value || paymentInProgress.value || saving.value)

const canProcessBreakdown = computed(() => {
  const rem = calculatedRemaining.value
  const qrCeilGap = rem < 0 && rem > -1 && num(qrAmount.value) > 0
  return (Math.abs(rem) < 0.005 || qrCeilGap) && !breakdownValidationError.value && !saving.value
})

const processButtonLabel = computed(() => {
  if (saving.value) return 'Saving...'
  if (showQRDialog.value) return 'Waiting for QR payment...'
  if (showChequeDialog.value) return 'Enter cheque details...'
  const steps = []
  if (num(qrAmount.value) > 0 && !qrProcessed.value) steps.push('QR')
  if (num(chequeAmount.value) > 0 && !chequeProcessed.value) steps.push('Cheque')
  if (steps.length) return `Process ${steps.join(' then ')} & Complete`
  return 'Complete Payment & Mark as Settled'
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

    let response
    try {
      response = await call('custom_erp.api.payment_reco.get_driver_reco_data', { driver_name: driverName })
    } catch (netErr) {
      const cached = await getCachedDriverReco(driverName)
      if (cached && cached.success) {
        response = cached
      } else {
        throw netErr
      }
    }
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
        // Extract company from reco for Fonepay API selection
        company.value = response.data.reco?.company || ''
        
        // Fetch company config for dynamic API selection
        if (company.value) {
          try {
            const configResponse = await call('custom_erp.api.payment_reco.get_company_config', {
              company_name: company.value
            })
            if (configResponse.success) {
              companyConfig.value = configResponse.data
            }
          } catch (err) {
            console.error('Error loading company config:', err)
          }
        }
        
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
      {
        const raw = num(lineData.value.initial_total_amount)
        pendingQRAmount.value = ceilFonepayAmount(raw)
        showQRDialog.value = true
      }
      break
      
    case 'cash':
      confirmDialogData.value = {
        type: 'cash',
        title: 'Confirm Cash Payment',
        message: 'Are you sure you want to record this as a cash payment?',
        amount: amount
      }
      showConfirmDialog.value = true
      break
      
    case 'cheque':
      pendingChequeAmount.value = amount
      showChequeDialog.value = true
      break
      
    case 'credit':
      confirmDialogData.value = {
        type: 'credit',
        title: 'Confirm Credit Entry',
        message: 'Are you sure you want to mark this amount as credit (pay later)?',
        amount: amount
      }
      showConfirmDialog.value = true
      break
      
    case 'return':
      confirmDialogData.value = {
        type: 'return',
        title: 'Confirm Full Return',
        message: 'Are you sure you want to mark this as a full return?',
        amount: amount
      }
      showConfirmDialog.value = true
      break
  }
}

const closeConfirmDialog = () => {
  showConfirmDialog.value = false
  confirmDialogData.value = {
    type: '',
    title: '',
    message: '',
    amount: 0
  }
}

const executeConfirmedPayment = async () => {
  const type = confirmDialogData.value.type
  const amount = confirmDialogData.value.amount
  
  paymentInProgress.value = true
  showConfirmDialog.value = false
  
  await saveWholePayment(type, amount)
  
  confirmDialogData.value = {
    type: '',
    title: '',
    message: '',
    amount: 0
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
        {
          const charged = ceilFonepayAmount(amount)
          const extra = charged - num(lineData.value.initial_total_amount)
          paymentData.qr_amount = charged
          if (extra > 0) {
            paymentData.additional_amount = extra
          }
        }
        if (isStaticQrMode()) {
          paymentData.fonepay_qr_transaction = null
          paymentData.remarks = `${paymentData.remarks} | Remarks: ${pendingQrRemarks.value || ''}`.trim()
        } else {
          paymentData.fonepay_qr_transaction = qrTransactionRef.value || null
        }
        break
      case 'cheque':
        paymentData.cheque_amount = amount
        paymentData.cheques_taageta = chequeRef.value || null
        break
    }
    
    console.log('📤 Sending payment data:', JSON.stringify(paymentData, null, 2))
    const response = await callUpdatePaymentEntry(call, paymentData)
    console.log('📥 Payment response:', JSON.stringify(response, null, 2))

    if (response.success) {
      if (response.queued) {
        alert(response.message || 'Payment queued — will sync when you are online.')
      }
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
          qrAmount.value = ceilFonepayAmount(amount)
          completedPaymentType.value = 'QR'
          pendingQrRemarks.value = ''
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

  let transactionId = ''
  if (typeof data === 'object' && data !== null && data.mode === 'static') {
    qrTransactionRef.value = null
    const note = data.qrRemarks || ''
    pendingQrRemarks.value = pendingQrRemarks.value
      ? `${pendingQrRemarks.value} || ${note}`
      : note
  } else if (typeof data === 'object' && data.transactionId) {
    qrTransactionRef.value = data.transactionId
    transactionId = data.transactionId
    pendingQrRemarks.value = ''
  } else {
    qrTransactionRef.value = data
    transactionId = data
    pendingQrRemarks.value = ''
  }

  showQRDialog.value = false

  const paid = ceilFonepayAmount(
    (typeof data === 'object' && data !== null && data.amount != null
      ? data.amount
      : pendingQRAmount.value) || pendingQRAmount.value
  )
  if (paid > 0) {
    pendingQRAmount.value = paid
  }

  if (entryMode.value === 'whole') {
    paymentInProgress.value = true
    await saveWholePayment('qr', pendingQRAmount.value)
  } else {
    qrProcessed.value = true
    if (paid > 0) {
      qrAmount.value = paid
    }
    showSuccessDialog.value = false
    showQrSuccessToast(num(qrAmount.value) || paid)
    await startBreakdownProcess()
  }
}

const handleQRDialogClose = () => {
  showQRDialog.value = false
  pendingQRAmount.value = 0
  if (entryMode.value !== 'whole') {
    pendingQrRemarks.value = ''
    abortBreakdownProcess()
  } else {
    pendingQrRemarks.value = ''
  }
}

const handleChequeSuccess = async (chequeId) => {
  chequeRef.value = chequeId
  showChequeDialog.value = false
  
  // Save immediately after cheque success
  if (entryMode.value === 'whole') {
    paymentInProgress.value = true
    await saveWholePayment('cheque', pendingChequeAmount.value)
  } else {
    chequeProcessed.value = true
    await startBreakdownProcess()
  }
}

const handleChequeDialogClose = () => {
  showChequeDialog.value = false
  pendingChequeAmount.value = 0
  if (entryMode.value !== 'whole') {
    abortBreakdownProcess()
  }
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

const dismissQrSuccessToast = () => {
  if (qrSuccessToastTimer) {
    clearTimeout(qrSuccessToastTimer)
    qrSuccessToastTimer = null
  }
  qrSuccessToast.value = { show: false, amount: qrSuccessToast.value.amount }
}

const showQrSuccessToast = (amount) => {
  dismissQrSuccessToast()
  qrSuccessToast.value = { show: true, amount: num(amount) }
  qrSuccessToastTimer = setTimeout(() => {
    qrSuccessToast.value = { ...qrSuccessToast.value, show: false }
    qrSuccessToastTimer = null
  }, 5500)
}

const onBreakdownInput = () => {
  if (!qrProcessed.value) {
    /* amount still editable */
  }
  validateBreakdown()
}

const onQrAmountInput = () => {
  const raw = num(qrAmount.value)
  qrAmount.value = raw <= 0 ? 0 : ceilFonepayAmount(raw)
  validateBreakdown()
}

const applyQrCeiling = (forcedAmount = null) => {
  if (qrProcessed.value && forcedAmount == null) return
  const raw = forcedAmount != null ? num(forcedAmount) : num(qrAmount.value)
  if (raw <= 0) {
    qrAmount.value = 0
    return
  }
  const ceiled = ceilFonepayAmount(raw)
  const extra = ceiled - raw
  qrAmount.value = ceiled
  if (extra > 0.0001) {
    additionalAmount.value = num(additionalAmount.value) + extra
  }
}

const fillRemaining = (field) => {
  if (breakdownLocked.value) return
  if (field === 'qr' && qrProcessed.value) return
  if (field === 'cheque' && chequeProcessed.value) return
  const current =
    field === 'cash' ? num(cashAmount.value) : field === 'qr' ? num(qrAmount.value) : num(chequeAmount.value)
  const rest = calculatedRemaining.value + current
  if (rest < 0) return
  if (field === 'cash') cashAmount.value = rest
  else if (field === 'qr') {
    qrAmount.value = rest
    applyQrCeiling()
  }
  else chequeAmount.value = rest
  validateBreakdown()
}

const abortBreakdownProcess = () => {
  breakdownProcessing.value = false
  paymentInProgress.value = false
}

const startBreakdownProcess = async () => {
  validateBreakdown()
  if (breakdownValidationError.value) {
    abortBreakdownProcess()
    return
  }
  if (Math.abs(calculatedRemaining.value) > 0.005) {
    const rem = calculatedRemaining.value
    const qrCeilGap = rem < 0 && rem > -1 && num(qrAmount.value) > 0
    if (!qrCeilGap) {
      abortBreakdownProcess()
      alert('Split cash, QR, and cheque so the remaining amount is exactly 0.')
      return
    }
  }

  breakdownProcessing.value = true
  paymentInProgress.value = true

  if (num(qrAmount.value) > 0 && !qrProcessed.value) {
    applyQrCeiling()
    pendingQRAmount.value = ceilFonepayAmount(num(qrAmount.value))
    showQRDialog.value = true
    return
  }
  if (num(chequeAmount.value) > 0 && !chequeProcessed.value) {
    pendingChequeAmount.value = num(chequeAmount.value)
    showChequeDialog.value = true
    return
  }

  try {
    await completeBreakdownPayment({ skipConfirm: true })
  } finally {
    abortBreakdownProcess()
  }
}

const handleBreakdownPayment = (type) => {
  fillRemaining(type)
}

const validateBreakdown = () => {
  const initial = num(lineData.value?.initial_total_amount)
  const amounts = [
    num(returnAmount.value),
    num(additionalAmount.value),
    num(creditAmount.value),
    num(cashAmount.value),
    num(qrAmount.value),
    num(chequeAmount.value),
  ]
  if (amounts.some((v) => v < 0)) {
    breakdownValidationError.value = 'Amounts cannot be negative'
    return
  }
  const totalReduction = num(returnAmount.value) + num(creditAmount.value)
  if (totalReduction > initial) {
    breakdownValidationError.value = `Return + Credit (${formatCurrency(totalReduction)}) cannot exceed Initial Amount (${formatCurrency(initial)})`
  } else {
    breakdownValidationError.value = ''
  }
}

const completeBreakdownPayment = async ({ skipConfirm = false } = {}) => {
  // Validation check
  if (Math.abs(calculatedRemaining.value) > 0.005) {
    const rem = calculatedRemaining.value
    const qrCeilGap = rem < 0 && rem > -1 && num(qrAmount.value) > 0
    if (!qrCeilGap) {
      alert('Please ensure the remaining amount is exactly 0 before completing payment.')
      return
    }
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

  if (!skipConfirm && !confirm(confirmMsg)) return

  try {
    saving.value = true
    
    // Validate lineData exists
    if (!lineData.value || !lineData.value.name) {
      throw new Error('Payment line data not loaded. Please refresh the page.')
    }
    
    let remarks = `Breakdown Entry: ${summary.join(', ')}`
    if (isStaticQrMode() && pendingQrRemarks.value) {
      remarks = `${remarks} | Remarks: ${pendingQrRemarks.value}`
    }

    const paymentData = {
      line_name: lineData.value.name,
      return_amount: returnAmount.value || 0,
      additional_amount: additionalAmount.value || 0,
      credit_amount: creditAmount.value || 0,
      cash_amount: cashAmount.value || 0,
      qr_amount: qrAmount.value || 0,
      cheque_amount: chequeAmount.value || 0,
      fonepay_qr_transaction: isStaticQrMode() ? null : (qrTransactionRef.value || null),
      cheques_taageta: chequeRef.value || null,
      remarks
    }

    const response = await callUpdatePaymentEntry(call, paymentData)

    if (response.success) {
      pendingQrRemarks.value = ''
      if (response.queued) {
        alert(
          response.message ||
            'Payment is queued and will sync when you are online. The server may not show settlement until sync completes.'
        )
      } else {
        alert('✅ Payment completed and marked as settled!')
      }
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

onUnmounted(() => {
  if (qrSuccessToastTimer) {
    clearTimeout(qrSuccessToastTimer)
    qrSuccessToastTimer = null
  }
})
</script>
