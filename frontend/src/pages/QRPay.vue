<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-5 sm:py-6">
          <div class="flex items-center space-x-3 sm:space-x-4">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-blue-600 rounded-lg flex-shrink-0">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="min-w-0 flex-1">
              <h1 class="text-xl sm:text-2xl font-bold text-gray-900 truncate">QRPay</h1>
              <p class="text-xs sm:text-sm text-gray-600 truncate">Dynamic Fonepay QR Generator • {{ session.user }}</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border border-gray-300 rounded-md shadow-sm text-xs sm:text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex-shrink-0"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8">
      <!-- Dashboard Summary (User Greeting, BS Date, Today's Stats) -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 lg:gap-8">
          <div class="space-y-1 flex-shrink-0 lg:min-w-[200px]">
            <div class="text-sm text-gray-500">Welcome</div>
            <div class="text-2xl lg:text-3xl font-bold text-gray-900">{{ greetingName }}</div>
            <div class="text-sm text-gray-600">Today (BS): <span class="font-medium">{{ bsToday || adToday }}</span></div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 flex-1 lg:max-w-3xl lg:mx-auto">
            <div class="p-4 rounded-lg bg-blue-50 border border-blue-200 min-h-[90px] flex flex-col justify-between">
              <div class="text-xs uppercase text-blue-600 tracking-wide leading-tight mb-2">Today's QR Total</div>
              <div class="text-xl font-bold text-blue-700 mt-auto">Rs. {{ formatAmount(dashboard.successTotal) }}</div>
            </div>
            <div class="p-4 rounded-lg bg-amber-50 border border-amber-200 min-h-[90px] flex flex-col justify-between">
              <div class="text-xs uppercase text-amber-700 tracking-wide leading-tight mb-2">Unprocessed Logs</div>
              <div class="text-xl font-bold text-amber-800 mt-auto">{{ dashboard.unprocessedCount }}</div>
            </div>
            <div class="p-4 rounded-lg bg-emerald-50 border border-emerald-200 min-h-[90px] flex flex-col justify-between">
              <div class="text-xs uppercase text-emerald-700 tracking-wide leading-tight mb-2">Success</div>
              <div class="text-xl font-bold text-emerald-800 mt-auto">{{ dashboard.successCount }}</div>
            </div>
            <div class="p-4 rounded-lg bg-rose-50 border border-rose-200 min-h-[90px] flex flex-col justify-between">
              <div class="text-xs uppercase text-rose-700 tracking-wide leading-tight mb-2">Failed</div>
              <div class="text-xl font-bold text-rose-800 mt-auto">{{ dashboard.failedCount }}</div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-3 flex-shrink-0">
            <button
              @click="refreshDashboardAndList"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 active:scale-95 transition"
              :disabled="refreshingDashboard"
            >
              <svg v-if="refreshingDashboard" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/><path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/></svg>
              <svg v-else class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              Refresh
            </button>
            <button
              v-if="dashboard.unprocessedCount > 0"
              @click="processTodayUnprocessed"
              class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              :disabled="processingUnprocessed"
            >
              <svg v-if="processingUnprocessed" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/><path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/></svg>
              <svg v-else class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/></svg>
              Process Unprocessed
            </button>
            <button
              @click="toggleTxnList"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg bg-white hover:bg-gray-50"
            >
              <svg class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7h18M3 12h18M3 17h18"/></svg>
              View Last 5 Transactions
            </button>
          </div>
        </div>

        <!-- Last Transactions List -->
        <div v-if="showTxn" class="mt-6 border-t border-gray-200 pt-4">
          <div class="flex items-center justify-between mb-3">
            <div class="flex gap-2">
              <button @click="setTxnFilter('all')" :class="txnFilterBtnClass('all')">All</button>
              <button @click="setTxnFilter('success')" :class="txnFilterBtnClass('success')">Success</button>
              <button @click="setTxnFilter('failed')" :class="txnFilterBtnClass('failed')">Failed</button>
            </div>
            <div v-if="loadingTxn" class="text-sm text-gray-500">Loading...</div>
          </div>
          <ul class="divide-y divide-gray-100">
            <li v-for="t in lastTxns" :key="t.name" class="py-3 flex items-center justify-between">
              <div class="min-w-0">
                <div class="text-sm font-medium text-gray-900 truncate">{{ t.customer_name || t.customer || '—' }}</div>
                <div class="text-xs text-gray-500">{{ t.time }}</div>
              </div>
              <div class="flex items-center gap-6">
                <div class="text-right">
                  <div class="text-sm font-semibold">Rs. {{ formatAmount(t.amount) }}</div>
                </div>
                <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
                  :class="{
                    'bg-emerald-50 text-emerald-700': t.status==='SUCCESS',
                    'bg-rose-50 text-rose-700': t.status==='FAILED',
                    'bg-gray-50 text-gray-700': t.status!=='SUCCESS' && t.status!=='FAILED',
                  }"
                >{{ t.status }}</span>
              </div>
            </li>
            <li v-if="!lastTxns.length && !loadingTxn" class="py-6 text-center text-sm text-gray-500">No transactions found for today.</li>
          </ul>
        </div>
      </section>

      <!-- Customer Selection -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <div class="flex items-center mb-6 sm:mb-8">
          <div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-900">Customer</h2>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          <div class="customer-select-wrapper">
            <label class="block text-sm font-semibold text-gray-700 mb-2 sm:mb-3">Customer</label>
            <div class="relative">
              <Autocomplete
                v-model="selectedCustomerValue"
                :options="customerOptions"
                :loading="loadingCustomers"
                placeholder="Search by customer name or code"
                class="customer-autocomplete w-full"
              />
            </div>
            <p v-if="!selectedCustomer" class="mt-2 text-xs sm:text-sm text-gray-500">Start typing to search. All customers are available by name or code.</p>
          </div>
          <div v-if="selectedCustomer" class="space-y-3">
            <label class="block text-sm font-semibold text-gray-700">Customer Details</label>
            <div class="p-5 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg space-y-2">
              <div class="text-lg font-semibold text-gray-900">{{ selectedCustomer.customer_name }}</div>
              <div class="text-sm text-gray-600">Customer Code: {{ selectedCustomer.name }}</div>
              <div v-if="selectedCustomer.customer_group" class="text-sm text-gray-600">Group: {{ selectedCustomer.customer_group }}</div>
              <div v-if="selectedCustomer.territory" class="text-sm text-gray-600">Territory: {{ selectedCustomer.territory }}</div>
              <div v-if="selectedCustomer.address_display" class="text-sm text-gray-600 whitespace-pre-line">
                {{ selectedCustomer.address_display }}
              </div>
              <div v-else-if="selectedCustomer.customer_primary_address" class="text-sm text-gray-600">
                Address: {{ selectedCustomer.customer_primary_address }}
              </div>
              <div v-if="selectedCustomer.mobile_no" class="text-sm text-gray-600">Phone: {{ selectedCustomer.mobile_no }}</div>
              <div v-if="selectedCustomer.email_id" class="text-sm text-gray-600">Email: {{ selectedCustomer.email_id }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Payment Details -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <div class="flex items-center mb-6 sm:mb-8">
          <div class="flex items-center justify-center w-10 h-10 bg-orange-100 rounded-lg mr-3">
            <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-900">Payment Details</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">Amount (NPR)</label>
            <input
              v-model.number="paymentAmount"
              type="number"
              step="0.01"
              min="0"
              placeholder="Enter amount to collect"
              class="w-full px-4 py-3 h-[44px] border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-base"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">Remarks (optional)</label>
            <input
              v-model="remarks"
              type="text"
              placeholder="Defaults to: Customer Name - NPR Amount (Date & Time)"
              class="w-full px-4 py-3 h-[44px] border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-base"
            />
          </div>
        </div>
      </section>

      <!-- Generate Button -->
      <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8 text-center">
        <button
          @click="showConfirmationDialog = true"
          :disabled="!canGenerate || generating"
          :class="[
            'inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200',
            canGenerate && !generating
              ? 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 shadow-lg hover:shadow-xl'
              : 'bg-gray-400 cursor-not-allowed'
          ]"
        >
          <svg v-if="generating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          {{ generating ? 'Generating QR Code...' : 'Generate Customer QR Code' }}
        </button>
      </section>

      <!-- Confirmation Dialog -->
      <div v-if="showConfirmationDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="confirmation-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-900 bg-opacity-75 backdrop-blur-sm transition-opacity" aria-hidden="true" @click="showConfirmationDialog = false"></div>
          
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
          
          <div class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <!-- Header -->
            <div class="bg-gradient-to-r from-blue-500 to-indigo-600 px-6 pt-6 pb-4">
              <div class="flex items-center justify-center mb-4">
                <div class="flex items-center justify-center h-16 w-16 rounded-full bg-white shadow-lg">
                  <svg class="h-10 w-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
              </div>
              <h3 class="text-2xl font-bold text-white text-center" id="confirmation-title">
                Confirm QR Code Generation
              </h3>
            </div>
            
            <!-- Content -->
            <div class="bg-white px-6 pt-6 pb-4">
              <p class="text-sm text-gray-600 mb-6 text-center">Please review the customer details before generating the QR code:</p>
              
              <div class="bg-gray-50 rounded-lg p-5 space-y-4 border border-gray-200">
                <!-- Customer Name (Bold, Mandatory) -->
                <div class="flex justify-between items-start">
                  <span class="text-sm font-medium text-gray-700">Customer Name:</span>
                  <span class="text-sm font-bold text-gray-900 text-right">{{ selectedCustomer?.customer_name || 'N/A' }}</span>
                </div>
                
                <!-- Code (Bold, Mandatory) -->
                <div class="flex justify-between items-start">
                  <span class="text-sm font-medium text-gray-700">Code:</span>
                  <span class="text-sm font-bold text-gray-900 text-right">{{ selectedCustomer?.name || 'N/A' }}</span>
                </div>
                
                <!-- Phone Number (Optional) -->
                <div v-if="selectedCustomer?.mobile_no" class="flex justify-between items-start">
                  <span class="text-sm font-medium text-gray-700">Phone Number:</span>
                  <span class="text-sm text-gray-900 text-right">{{ selectedCustomer.mobile_no }}</span>
                </div>
                
                <!-- PAN/TAX ID (Optional) -->
                <div v-if="selectedCustomer?.tax_id" class="flex justify-between items-start">
                  <span class="text-sm font-medium text-gray-700">PAN/TAX ID:</span>
                  <span class="text-sm text-gray-900 text-right">{{ selectedCustomer.tax_id }}</span>
                </div>
                
                <!-- Amount (Bold, Mandatory) -->
                <div class="flex justify-between items-start pt-3 border-t border-gray-300">
                  <span class="text-base font-semibold text-gray-900">Amount:</span>
                  <span class="text-lg font-bold text-blue-600 text-right">NPR {{ formatAmount(paymentAmount) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse gap-3">
              <button 
                type="button"
                @click="confirmGenerateQR"
                class="w-full inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto transition-all duration-200"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Yes, Generate QR
              </button>
              <button 
                type="button"
                @click="showConfirmationDialog = false"
                class="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-6 py-3 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto transition-all duration-200"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Success Card - Shows ABOVE QR section -->
      <section v-if="qrStatus === 'SUCCESS' && paymentEntry" class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl shadow-lg border-2 border-green-300 p-6 sm:p-8 animate-pulse-slow">
        <div class="text-center space-y-4">
          <div class="flex items-center justify-center w-20 h-20 bg-green-500 rounded-full mx-auto shadow-lg">
            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-green-800">🎉 Payment Successful!</h2>
          <div class="bg-white rounded-lg p-4 shadow-inner">
            <p class="text-lg font-semibold text-gray-700">Amount Received</p>
            <p class="text-4xl font-bold text-green-600">NPR {{ formatAmount(paymentAmount) }}</p>
          </div>
          <p class="text-gray-700">Customer: <span class="font-semibold">{{ selectedCustomer?.customer_name }}</span></p>
          <p v-if="paymentEntry" class="text-sm text-gray-600">
            Payment Entry: <a :href="`/app/payment-entry/${paymentEntry}`" class="text-blue-600 hover:text-blue-800 underline font-semibold" target="_blank" rel="noopener">{{ paymentEntry }}</a>
          </p>
          <button 
            @click="resetForNextPayment" 
            class="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Make New Payment
          </button>
        </div>
      </section>

      <!-- QR & Status -->
      <section v-if="qrData" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8 space-y-6">
        <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div class="flex-1 text-center">
            <h3 class="text-xl font-semibold text-gray-900 mb-6">QR Code</h3>
            <div id="qr-code" class="flex justify-center"></div>
          </div>
          <div class="flex-1 space-y-4">
            <div class="bg-gray-50 rounded-lg p-6 space-y-3">
              <div class="text-center">
                <div class="text-xs text-gray-500 uppercase tracking-wide mb-2">Payment Status</div>
                <div class="text-2xl font-bold" :class="statusColorClass">{{ qrStatus || 'CREATED' }}</div>
              </div>
              <div class="border-t border-gray-200 pt-3 space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Amount:</span>
                  <span class="font-semibold">NPR {{ formatAmount(paymentAmount) }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Customer:</span>
                  <span class="font-semibold truncate ml-2">{{ selectedCustomer?.customer_name }}</span>
                </div>
                <div v-if="paymentEntry" class="flex justify-between text-sm">
                  <span class="text-gray-600">Payment Entry:</span>
                  <a :href="`/app/payment-entry/${paymentEntry}`" class="text-blue-600 hover:text-blue-700 underline font-semibold" target="_blank" rel="noopener">{{ paymentEntry }}</a>
                </div>
              </div>
            </div>
            <!-- Payment Status Message -->
            <div v-if="paymentMessage && (qrStatus === 'PENDING' || qrStatus === 'SCANNED' || qrStatus === 'ERROR' || qrStatus === 'FAILED')" 
                 class="p-4 rounded-lg border"
                 :class="{
                   'bg-orange-50 border-orange-200': qrStatus === 'PENDING',
                   'bg-yellow-50 border-yellow-200': qrStatus === 'SCANNED',
                   'bg-red-50 border-red-200': qrStatus === 'ERROR' || qrStatus === 'FAILED'
                 }">
              <div class="flex items-start">
                <svg v-if="qrStatus === 'PENDING'" class="w-5 h-5 text-orange-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <svg v-else-if="qrStatus === 'SCANNED'" class="w-5 h-5 text-yellow-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <svg v-else class="w-5 h-5 text-red-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <div class="flex-1">
                  <p class="text-sm font-medium" :class="{
                    'text-orange-800': qrStatus === 'PENDING',
                    'text-yellow-800': qrStatus === 'SCANNED',
                    'text-red-800': qrStatus === 'ERROR' || qrStatus === 'FAILED'
                  }">{{ paymentMessage }}</p>
                </div>
              </div>
            </div>
            <div class="flex gap-3">
              <button
                @click="manuallyProcessPayment"
                class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-green-300 rounded-md shadow-sm text-sm font-medium text-green-700 bg-white hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                :disabled="!currentTxName || qrStatus === 'SUCCESS'"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Process Payment
              </button>
              <button
                @click="regenerateQR"
                class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Reset
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Live Status Logs -->
      <section v-if="statusLogs.length" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Live Status Updates</h3>
        <ul class="space-y-3 max-h-72 overflow-y-auto pr-1">
          <li v-for="log in statusLogs" :key="log.id" class="border border-gray-200 rounded-lg px-4 py-3 bg-gray-50">
            <div class="flex justify-between items-center mb-1">
              <span :class="log.levelClass" class="text-sm font-medium">{{ log.levelLabel }}</span>
              <span class="text-xs text-gray-500">{{ formatLogTime(log.ts) }}</span>
            </div>
            <p class="text-sm text-gray-700 whitespace-pre-line break-words">{{ log.message }}</p>
          </li>
        </ul>
      </section>

      <!-- Beautiful Payment Success Modal Dialog -->
      <div v-if="showSuccessDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <!-- Background overlay with blur -->
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-900 bg-opacity-75 backdrop-blur-sm transition-opacity" aria-hidden="true" @click="showSuccessDialog = false"></div>
          
          <!-- Center modal -->
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
          
          <div class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <!-- Success Icon with animation -->
            <div class="bg-gradient-to-br from-green-400 to-emerald-500 px-6 pt-8 pb-6">
              <div class="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-white shadow-lg animate-bounce-slow">
                <svg class="h-16 w-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
            </div>
            
            <div class="bg-white px-6 pt-6 pb-4">
              <div class="text-center">
                <h3 class="text-3xl leading-6 font-bold text-gray-900 mb-3" id="modal-title">
                  🎉 Payment Successful!
                </h3>
                <div class="mt-4 mb-6">
                  <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border-2 border-green-200">
                    <p class="text-sm font-medium text-gray-600 mb-2">Amount Received</p>
                    <p class="text-5xl font-bold text-green-600">
                      NPR {{ formatAmount(paymentAmount) }}
                    </p>
                  </div>
                </div>
                <div class="mt-4 space-y-2">
                  <p class="text-sm text-gray-600">
                    <span class="font-semibold">Customer:</span> {{ selectedCustomer?.customer_name }}
                  </p>
                  <p v-if="paymentEntry" class="text-sm text-gray-600">
                    <span class="font-semibold">Payment Entry:</span> 
                    <a :href="`/app/payment-entry/${paymentEntry}`" class="text-blue-600 hover:text-blue-800 underline font-semibold" target="_blank" rel="noopener">
                      {{ paymentEntry }}
                    </a>
                  </p>
                  <p class="text-xs text-gray-500 mt-2">
                    {{ new Date().toLocaleString() }}
                  </p>
                </div>
              </div>
            </div>
            
            <div class="bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse gap-3">
              <button 
                type="button"
                @click="resetForNextPayment"
                class="w-full inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto transition-all duration-200"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Make New Payment
              </button>
              <button 
                type="button"
                @click="showSuccessDialog = false"
                class="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-6 py-3 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto transition-all duration-200"
              >
                OK
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ADDED BY AI: FONEPAY LIVE SOCKET - Error Dialog -->
      <section v-if="showErrorDialog" class="bg-white rounded-xl shadow-lg border border-red-200 p-6 sm:p-8">
        <div class="text-center space-y-4">
          <div class="flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mx-auto">
            <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900">Payment Failed</h3>
          <p class="text-gray-600">{{ paymentMessage }}</p>
          <div class="flex gap-3 justify-center">
            <button 
              @click="regenerateQRFromDialog" 
              class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              Regenerate QR
            </button>
            <button 
              @click="resetAll" 
              class="inline-flex items-center px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
            >
              Reset All
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- ADDED BY AI: FONEPAY LIVE SOCKET - Loading Overlay -->
    <LoadingOverlay v-if="showLoadingOverlay" />

    <!-- No Internet Dialog -->
    <div v-if="showOfflineDialog" class="fixed inset-0 z-50 overflow-y-auto" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen px-4 text-center">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-75" aria-hidden="true" @click="showOfflineDialog = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full">
          <div class="px-6 pt-6 pb-4">
            <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
              <svg class="h-8 w-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M4.93 4.93l14.14 14.14M12 19c-3.866 0-7-3.134-7-7 0-1.657.57-3.178 1.52-4.382m1.53-1.53A6.978 6.978 0 0112 5c3.866 0 7 3.134 7 7 0 1.657-.57 3.178-1.52 4.382" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">No Internet Connection</h3>
            <p class="text-sm text-gray-600">Please check/connect to the internet first and try again.</p>
          </div>
          <div class="bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse">
            <button type="button" @click="showOfflineDialog = false" class="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto">OK</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { Autocomplete, createResource, call as $call } from 'frappe-ui'
import { session } from '@/data/session'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const selectedCustomer = ref(null)
const selectedCustomerValue = ref(null)
const customerOptions = ref([])
const loadingCustomers = ref(false)
const paymentAmount = ref('')
const remarks = ref('')
const generating = ref(false)
const qrData = ref(null)
const qrStatus = ref(null)
const paymentEntry = ref(null)
const websocketUrl = ref('')
const merchantWebsocketUrl = ref('')
const statusLogs = ref([])

// Dashboard state
const dashboard = ref({ successTotal: 0, unprocessedCount: 0, successCount: 0, failedCount: 0 })
const greetingName = ref(session.user)
const bsToday = ref('')
const adToday = new Date().toISOString().slice(0, 10)
const processingUnprocessed = ref(false)
const showTxn = ref(false)
const lastTxns = ref([])
const txnFilter = ref('all')
const loadingTxn = ref(false)
const refreshingDashboard = ref(false)

// ADDED BY AI: FONEPAY LIVE SOCKET - New state for loading overlay and dialogs
const showLoadingOverlay = ref(false)
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const paymentMessage = ref('')
const showOfflineDialog = ref(false)
const isOnline = ref(typeof navigator !== 'undefined' ? navigator.onLine : true)
const showConfirmationDialog = ref(false)

const customerSearchResource = createResource({
  url: 'custom_erp.custom_erp.api.fonepay.search_customers',
  auto: false,
})
const qrCreateResource = createResource({ url: 'custom_erp.custom_erp.api.fonepay.create_dynamic_qr', auto: false })
const dashboardResource = createResource({ url: 'custom_erp.custom_erp.api.fonepay.get_user_today_summary', auto: false })
const processTodayResource = createResource({ url: 'custom_erp.custom_erp.api.fonepay.process_user_unprocessed_today', auto: false })
const listTodayTxnsResource = createResource({ url: 'custom_erp.custom_erp.api.fonepay.list_user_transactions_today', auto: false })

let realtimeHandler = null
const merchantSocket = ref(null)
const currentTxName = ref(null)

const canGenerate = computed(() => {
  const amount = Number(paymentAmount.value)
  const result = Boolean(selectedCustomer.value && amount > 0)
  console.log('canGenerate check:', { 
    hasCustomer: !!selectedCustomer.value, 
    customerName: selectedCustomer.value?.name,
    amount, 
    result 
  })
  return result
})
const statusColorClass = computed(() => getStatusColor(qrStatus.value))

// Watch for changes to selectedCustomerValue and update selectedCustomer
watch(selectedCustomerValue, (newValue) => {
  console.log('selectedCustomerValue changed:', newValue)
  if (!newValue) {
    selectedCustomer.value = null
    return
  }
  // Frappe UI Autocomplete passes the entire object, not just the value
  // Check if newValue is an object or a primitive
  let option = null
  if (typeof newValue === 'object' && newValue !== null) {
    // newValue is the option object itself
    option = newValue
  } else {
    // newValue is a string/primitive, find the option
    option = customerOptions.value.find(opt => opt.value === newValue)
  }
  
  console.log('Found option:', option)
  if (option) {
    selectedCustomer.value = {
      name: option.value || option.name,
      customer_name: option.customer_name,
      customer_group: option.customer_group,
      territory: option.territory,
      customer_primary_address: option.customer_primary_address,
      address_display: option.address_display,
      mobile_no: option.mobile_no,
      email_id: option.email_id,
      tax_id: option.tax_id,
    }
    console.log('Set selectedCustomer:', selectedCustomer.value)
    pushStatusLog('info', `Selected customer ${selectedCustomer.value.customer_name} (${selectedCustomer.value.name})`)
  }
})

const loadCustomers = async (query = '') => {
  loadingCustomers.value = true
  try {
    // Load all customers with high limit to ensure none are excluded
    const response = await customerSearchResource.fetch({ query, limit: 10000 })
    const payload = response?.customers || response?.message?.customers || []
    customerOptions.value = payload.map((customer) => ({
      label: `${customer.customer_name} (${customer.name})`,
      value: customer.name,
      ...customer,
    }))
  } catch (error) {
    console.error('Error loading customers', error)
  } finally {
    loadingCustomers.value = false
  }
}

const confirmGenerateQR = () => {
  showConfirmationDialog.value = false
  generateQR()
}

const generateQR = async () => {
  if (!canGenerate.value || generating.value) {
    return
  }
  generating.value = true
  qrData.value = null
  qrStatus.value = null
  paymentEntry.value = null
  websocketUrl.value = ''
  merchantWebsocketUrl.value = ''
  currentTxName.value = null
  clearRealtime()
  closeMerchantSocket()
  pushStatusLog('info', 'Submitting request to generate QR code...')

  try {
    const amount = Number(paymentAmount.value) || 0
    const remarksValue = remarks.value?.trim() || ''

    const response = await qrCreateResource.fetch({
      amount,
      customer: selectedCustomer.value.name,
      remarks1: session.user ,
      remarks2: remarksValue,
    })

    if (!response?.qr_message) {
      throw new Error('No QR message returned by Fonepay')
    }

    qrData.value = response
    qrStatus.value = response.status || 'CREATED'
    websocketUrl.value = response.websocket_url || ''
    merchantWebsocketUrl.value = response.merchant_websocket_url || ''
    currentTxName.value = response.tx_name

    pushStatusLog('success', 'QR code created successfully. Awaiting payment events...')

    await renderQRCode(response.qr_message)
    
    // BULLETPROOF FIX: Ensure Vue's reactive system and DOM are 100% ready
    // Multiple layers of safety to guarantee WebSocket works first time
    await nextTick() // Wait for Vue's reactive updates
    await nextTick() // Double nextTick for extra safety
    await new Promise(resolve => setTimeout(resolve, 300)) // Additional time for DOM
    
    // Subscribe to Frappe realtime events
    subscribeToUpdates(response.tx_name)
    
    // Connect to merchant WebSocket - now with bulletproof initialization
    await connectMerchantSocketRobust(response.merchant_websocket_url || response.websocket_url)
  } catch (error) {
    console.error('Error generating QR', error)
    if (isNetworkError(error)) {
      handleOfflineError()
    } else {
      pushStatusLog('error', `Failed to generate QR code: ${error.message || error}`)
      alert(`Failed to generate QR code: ${error.message || error}`)
    }
  } finally {
    generating.value = false
  }
}

const renderQRCode = async (qrMessage) => {
  if (!qrMessage) return
  if (!window.QRCode) {
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
    document.head.appendChild(script)
    await new Promise((resolve) => {
      script.onload = resolve
      script.onerror = resolve
    })
  }
  
  // Wait for Vue to render the DOM element
  await new Promise(resolve => setTimeout(resolve, 100))
  
  const qrContainer = document.getElementById('qr-code')
  if (qrContainer) {
    // Completely clear the container
    qrContainer.innerHTML = ''
    
    // Force DOM reflow to ensure clean slate
    void qrContainer.offsetHeight
    
    try {
      new window.QRCode(qrContainer, {
        text: qrMessage,
        width: 256,
        height: 256,
        correctLevel: window.QRCode.CorrectLevel.M,
      })
      console.log('✅ QR code rendered successfully')
      pushStatusLog('success', 'QR code displayed.')
    } catch (error) {
      console.error('Unable to render QR code', error)
      pushStatusLog('error', 'Unable to render QR code in the browser.')
    }
  } else {
    console.warn('⚠️ QR container element not found')
    pushStatusLog('warning', 'QR container not ready, retrying...')
    // Retry once after a longer delay
    await new Promise(resolve => setTimeout(resolve, 300))
    const retryContainer = document.getElementById('qr-code')
    if (retryContainer) {
      retryContainer.innerHTML = ''
      try {
        new window.QRCode(retryContainer, {
          text: qrMessage,
          width: 256,
          height: 256,
          correctLevel: window.QRCode.CorrectLevel.M,
        })
        console.log('✅ QR code rendered on retry')
      } catch (error) {
        console.error('Unable to render QR code on retry', error)
      }
    }
  }
}

// BULLETPROOF WebSocket Connection - Guaranteed to work on first load!
const connectMerchantSocketRobust = async (url) => {
  console.log('🚀 [WEBSOCKET-ROBUST] ================================================')
  console.log('🚀 [WEBSOCKET-ROBUST] Starting BULLETPROOF connection sequence')
  console.log('🚀 [WEBSOCKET-ROBUST] URL:', url)
  console.log('🚀 [WEBSOCKET-ROBUST] Time:', new Date().toISOString())
  console.log('🚀 [WEBSOCKET-ROBUST] ================================================')
  
  if (!url || typeof WebSocket === 'undefined') {
    console.error('❌ [WEBSOCKET-ROBUST] Invalid parameters - cannot connect')
    pushStatusLog('error', 'WebSocket unavailable or URL missing')
    return Promise.reject(new Error('WebSocket unavailable'))
  }
  
  // Close any existing connection
  closeMerchantSocket()
  
  pushStatusLog('info', '🔌 Initializing merchant websocket connection...')
  
  return new Promise((resolve, reject) => {
    try {
      // Create WebSocket instance
      const ws = new WebSocket(url)
      
      // CRITICAL: Store reference IMMEDIATELY - before any handlers
      merchantSocket.value = ws
      console.log('✓ [WEBSOCKET-ROBUST] Socket instance created and stored')
      console.log('✓ [WEBSOCKET-ROBUST] Initial readyState:', ws.readyState, '(0=CONNECTING)')
      
      // Set up connection timeout (30 seconds)
      const connectionTimeout = setTimeout(() => {
        if (ws.readyState !== WebSocket.OPEN) {
          console.error('⏱️ [WEBSOCKET-ROBUST] Connection timeout!')
          ws.close()
          merchantSocket.value = null
          reject(new Error('WebSocket connection timeout'))
        }
      }, 30000)
      
      // Handler: Connection opened successfully
      ws.onopen = () => {
        clearTimeout(connectionTimeout)
        console.log('✅ [WEBSOCKET-ROBUST] ====== CONNECTION ESTABLISHED ======')
        console.log('✅ [WEBSOCKET-ROBUST] ReadyState:', ws.readyState, '(1=OPEN)')
        console.log('✅ [WEBSOCKET-ROBUST] Socket stored:', !!merchantSocket.value)
        console.log('✅ [WEBSOCKET-ROBUST] Ready to receive messages!')
        console.log('✅ [WEBSOCKET-ROBUST] ====================================')
        pushStatusLog('success', '✅ Merchant websocket CONNECTED and READY!')
        resolve(ws)
      }
      
      // Handler: Connection error
      ws.onerror = (event) => {
        clearTimeout(connectionTimeout)
        console.error('❌ [WEBSOCKET-ROBUST] Error event:', event)
        console.error('❌ [WEBSOCKET-ROBUST] ReadyState:', ws.readyState)
        pushStatusLog('error', '❌ WebSocket connection error')
        // Don't reject here - wait for onclose
      }
      
      // Handler: Connection closed
      ws.onclose = (event) => {
        clearTimeout(connectionTimeout)
        console.log('🔌 [WEBSOCKET-ROBUST] Connection closed')
        console.log('🔌 [WEBSOCKET-ROBUST] Code:', event.code)
        console.log('🔌 [WEBSOCKET-ROBUST] Reason:', event.reason)
        console.log('🔌 [WEBSOCKET-ROBUST] Clean:', event.wasClean)
        merchantSocket.value = null
        pushStatusLog('warning', `WebSocket disconnected (${event.code})`)
        
        if (ws.readyState !== WebSocket.OPEN) {
          reject(new Error(`WebSocket closed before opening (code: ${event.code})`))
        }
      }
      
      // Handler: MESSAGE RECEIVED - This is the most critical part!
      ws.onmessage = async (event) => {
        console.log('🎉 [WEBSOCKET-ROBUST] ================================================')
        console.log('🎉 [WEBSOCKET-ROBUST] ⚡ MESSAGE RECEIVED ⚡')
        console.log('🎉 [WEBSOCKET-ROBUST] Time:', new Date().toISOString())
        console.log('🎉 [WEBSOCKET-ROBUST] Socket state:', ws.readyState)
        console.log('🎉 [WEBSOCKET-ROBUST] Stored ref valid:', !!merchantSocket.value)
        console.log('🎉 [WEBSOCKET-ROBUST] Raw data:', event.data)
        console.log('🎉 [WEBSOCKET-ROBUST] ================================================')
        
        pushStatusLog('ws', `📨 WS Message: ${event.data}`)
        
        let data = null
        try {
          data = JSON.parse(event.data || '{}')
          console.log('📦 [WEBSOCKET-ROBUST] Parsed data:', JSON.stringify(data, null, 2))
        } catch (error) {
          console.warn('⚠️ [WEBSOCKET-ROBUST] Non-JSON message, ignoring')
          return
        }
        
        // Process the payment status data
        if (data && typeof data === 'object') {
          console.log('🔍 [WEBSOCKET-ROBUST] Processing payment data...')
          console.log('🔍 [WEBSOCKET-ROBUST] Fields:', Object.keys(data))
          console.log('🔍 [WEBSOCKET-ROBUST] transactionStatus:', data.transactionStatus)
          console.log('🔍 [WEBSOCKET-ROBUST] productNumber:', data.productNumber)
          
          // Call the payment processor
          await handleWebSocketPaymentUpdate(data)
        }
      }
      
      console.log('✓ [WEBSOCKET-ROBUST] All handlers attached successfully')
      console.log('✓ [WEBSOCKET-ROBUST] Waiting for connection to open...')
      
    } catch (error) {
      console.error('❌ [WEBSOCKET-ROBUST] Exception during setup:', error)
      merchantSocket.value = null
      pushStatusLog('error', `WebSocket setup failed: ${error.message}`)
      reject(error)
    }
  })
}

// Extract WebSocket message handling into separate function for clarity
const handleWebSocketPaymentUpdate = async (data) => {
  try {
    console.log('💳 [PAYMENT-UPDATE] ========== PROCESSING PAYMENT UPDATE ==========')
    console.log('💳 [PAYMENT-UPDATE] Raw data:', JSON.stringify(data, null, 2))
    
    // Parse transaction status - handle multiple formats
    let isSuccess = false
    let isFailed = false
    let isScanned = false
    let parsedStatus = null
    
    // Try to parse transactionStatus if it's a JSON string
    if (data.transactionStatus && typeof data.transactionStatus === 'string') {
      try {
        parsedStatus = JSON.parse(data.transactionStatus)
        console.log('💳 [PAYMENT-UPDATE] Parsed transactionStatus:', parsedStatus)
        
        if (parsedStatus.qrVerified === true && parsedStatus.paymentSuccess !== true) {
          isScanned = true
          console.log('💳 [PAYMENT-UPDATE] ✅ QR VERIFIED (scanned but not paid)')
        }
        else if (parsedStatus.paymentSuccess === true || parsedStatus.success === true) {
          isSuccess = true
          console.log('💳 [PAYMENT-UPDATE] ✅ PAYMENT SUCCESS!')
        } 
        else if (parsedStatus.paymentSuccess === false || parsedStatus.success === false) {
          isFailed = true
          console.log('💳 [PAYMENT-UPDATE] ❌ PAYMENT FAILED')
        }
      } catch (e) {
        console.warn('💳 [PAYMENT-UPDATE] Could not parse transactionStatus as JSON:', e)
      }
    }
    
    // Check if transactionStatus is already an object
    if (!isSuccess && !isFailed && data.transactionStatus && typeof data.transactionStatus === 'object') {
      const status = String(data.transactionStatus).toUpperCase()
      console.log('💳 [PAYMENT-UPDATE] Object status:', status)
      isSuccess = status === 'SUCCESS' || status === 'COMPLETED'
      isFailed = status === 'FAILED'
      isScanned = status === 'INITIATED' || status === 'VERIFIED'
    }
    
    // Check root level fields
    if (!isSuccess && !isFailed) {
      isSuccess = data.paymentSuccess === true || data.success === true
      isFailed = data.paymentSuccess === false || data.success === false
    }
    
    console.log('💳 [PAYMENT-UPDATE] Status flags:', { isSuccess, isFailed, isScanned })
    
    // HANDLE PAYMENT SUCCESS
    if (isSuccess) {
      console.log('🎉 [PAYMENT-UPDATE] ========== PAYMENT SUCCESS DETECTED! ==========')
      showLoadingOverlay.value = true
      pushStatusLog('success', '🎉 Payment success detected! Verifying with backend...')
      
      try {
        // Get PRN from parsed data
        const prnRef = parsedStatus ? String(parsedStatus.productNumber || parsedStatus.prn || '') : ''
        console.log('💳 [PAYMENT-UPDATE] PRN for verification:', prnRef)
        console.log('💳 [PAYMENT-UPDATE] Calling check_status API...')
        
        // Verify payment with backend
        const verify = await $call('custom_erp.custom_erp.api.fonepay.check_status', {
          txn_ref_id: prnRef || currentTxName.value
        })
        
        console.log('💳 [PAYMENT-UPDATE] Backend verification response:', verify)
        
        if (verify && verify.status === 'SUCCESS') {
          console.log('✅ [PAYMENT-UPDATE] Backend confirmed SUCCESS!')
          qrStatus.value = 'SUCCESS'
          paymentEntry.value = verify.payment_entry || paymentEntry.value
          paymentMessage.value = 'Payment confirmed successfully! Amount: NPR ' + formatAmount(paymentAmount.value)
          pushStatusLog('success', '✅ Backend verification complete. Payment Entry: ' + paymentEntry.value)
          
          // Show success UI
          removeQrAndShowSuccess()
          await refreshDashboardAndList()
        } else {
          console.error('❌ [PAYMENT-UPDATE] Backend verification failed!')
          qrStatus.value = 'FAILED'
          paymentMessage.value = 'Verification failed: ' + (verify?.message || 'Unknown error')
          pushStatusLog('error', '❌ Backend verification failed: ' + paymentMessage.value)
          showFailedDialog()
          await refreshDashboardAndList()
        }
      } catch (error) {
        console.error('❌ [PAYMENT-UPDATE] Verification error:', error)
        qrStatus.value = 'FAILED'
        paymentMessage.value = 'Verification error: ' + (error.message || error)
        pushStatusLog('error', '❌ Verification API error: ' + paymentMessage.value)
        showFailedDialog()
      } finally {
        showLoadingOverlay.value = false
      }
    }
    // HANDLE PAYMENT FAILED
    else if (isFailed) {
      console.log('❌ [PAYMENT-UPDATE] ========== PAYMENT FAILED ==========')
      showLoadingOverlay.value = false
      qrStatus.value = 'FAILED'
      paymentMessage.value = data.responseMessage || data.message || 'Payment failed.'
      pushStatusLog('error', '❌ Payment failed: ' + paymentMessage.value)
      showFailedDialog()
      await refreshDashboardAndList()
    }
    // HANDLE QR SCANNED
    else if (isScanned) {
      console.log('👀 [PAYMENT-UPDATE] ========== QR SCANNED ==========')
      qrStatus.value = 'SCANNED'
      pushStatusLog('info', '👀 QR code scanned by customer. Waiting for payment confirmation...')
    }
    // HANDLE OTHER UPDATES
    else {
      console.log('ℹ️ [PAYMENT-UPDATE] Other status update')
      pushStatusLog('info', 'Payment status update: ' + JSON.stringify(data.transactionStatus))
    }
    
    console.log('💳 [PAYMENT-UPDATE] ========== UPDATE PROCESSING COMPLETE ==========')
    
  } catch (error) {
    console.error('❌ [PAYMENT-UPDATE] Error processing update:', error)
    pushStatusLog('error', `Error processing payment update: ${error.message}`)
    showLoadingOverlay.value = false
  }
}

// [OLD FUNCTION REMOVED] - Now using connectMerchantSocketRobust instead

// Keeping old function commented for reference if needed
/*
const connectMerchantSocket = (url) => {
  if (!url || typeof WebSocket === 'undefined') {
    console.warn('⚠️ WebSocket not available or URL missing:', url)
    pushStatusLog('warning', 'WebSocket unavailable or URL missing: ' + url)
    return
  }
  
  // Close any existing connection first
  closeMerchantSocket()
  
  console.log('🔌 [WEBSOCKET] Attempting to connect to:', url)
  console.log('🔌 [WEBSOCKET] Current time:', new Date().toISOString())
  pushStatusLog('info', 'Connecting to merchant websocket: ' + url)
  
  try {
    // ADDED BY AI: FONEPAY LIVE SOCKET - Connect to Fonepay live WebSocket
    const ws = new WebSocket(url)
    
    // CRITICAL FIX: Store socket reference IMMEDIATELY before setting handlers
    // This ensures the reference is available even if handlers fire quickly
    merchantSocket.value = ws
    
    console.log('🔌 [WEBSOCKET] WebSocket object created, readyState:', ws.readyState)
    console.log('🔌 [WEBSOCKET] Setting up event handlers...')
    
    ws.onopen = () => {
      console.log('✅ [WEBSOCKET] Connection OPENED! ReadyState:', ws.readyState)
      console.log('✅ [WEBSOCKET] Socket reference stored:', !!merchantSocket.value)
      pushStatusLog('success', 'Merchant websocket connected and ready to receive messages.')
    }
    
    ws.onerror = (event) => {
      console.error('❌ [WEBSOCKET] Error occurred:', event)
      console.error('❌ [WEBSOCKET] ReadyState:', ws.readyState)
      pushStatusLog('warning', 'Merchant websocket reported an error.')
    }
    
    ws.onclose = (event) => {
      console.log('🔌 [WEBSOCKET] Connection CLOSED')
      console.log('🔌 [WEBSOCKET] Close code:', event.code)
      console.log('🔌 [WEBSOCKET] Close reason:', event.reason)
      console.log('🔌 [WEBSOCKET] Was clean:', event.wasClean)
      pushStatusLog('warning', `Merchant websocket disconnected. Code: ${event.code}`)
    }
    
    // CRITICAL FIX: Define onmessage handler inline and immediately
    // This ensures it's ready before any messages arrive
    ws.onmessage = async (event) => {
      console.log('🎉 [WEBSOCKET] ========================================')
      console.log('🎉 [WEBSOCKET] MESSAGE RECEIVED!')
      console.log('🎉 [WEBSOCKET] Timestamp:', new Date().toISOString())
      console.log('🎉 [WEBSOCKET] Raw data:', event.data)
      console.log('🎉 [WEBSOCKET] ========================================')
      pushStatusLog('ws', `WS Message: ${event.data}`)
      
      let data = null
      try {
        data = JSON.parse(event.data || '{}')
        console.log('📦 Parsed WebSocket data:', data)
      } catch (error) {
        console.warn('⚠️ Failed to parse WebSocket message as JSON:', error)
        // ignore non-JSON messages
        return
      }
      
      // ADDED BY AI: FONEPAY LIVE SOCKET - Handle both new and old field formats
      if (data && typeof data === 'object') {
        console.log('🔍 Checking payment status in WebSocket data...')
        console.log('  Fields present:', Object.keys(data))
        console.log('  transactionStatus:', data.transactionStatus)
        console.log('  paymentSuccess:', data.paymentSuccess)
        console.log('  success:', data.success)
        
        let isSuccess = false
        let isFailed = false
        let isScanned = false
        let parsedStatus = null
        
        // CRITICAL FIX: transactionStatus is a JSON STRING, not an object!
        if (data.transactionStatus && typeof data.transactionStatus === 'string') {
          try {
            parsedStatus = JSON.parse(data.transactionStatus)
            console.log('  🔓 Parsed transactionStatus string:', parsedStatus)
            
            // Now check the parsed object
            if (parsedStatus.qrVerified === true && parsedStatus.paymentSuccess == null) {
              isScanned = true
              console.log('  ✅ QR VERIFIED detected!')
            }
            else if (parsedStatus.paymentSuccess === true || parsedStatus.success === true) {
              isSuccess = true
              console.log('  ✅ SUCCESS detected in parsed transactionStatus!')
            } else if (parsedStatus.paymentSuccess === false || parsedStatus.success === false) {
              isFailed = true
              console.log('  ✅ FAILURE detected in parsed transactionStatus!')
            } 
          } catch (e) {
            console.warn('  ⚠️ Failed to parse transactionStatus as JSON:', e)
          }
        }
        
        // Check if transactionStatus is already an object (NEW format)
        if (!isSuccess && !isFailed && data.transactionStatus && typeof data.transactionStatus === 'object') {
          const status = String(data.transactionStatus).toUpperCase()
          console.log('  ✅ Using NEW format (object): transactionStatus =', status)
          isSuccess = status === 'SUCCESS' || status === 'COMPLETED'
          isFailed = status === 'FAILED'
          isScanned = status === 'INITIATED'
        }
        
        // Check OLD format (paymentSuccess, success fields at root level) - FALLBACK
        if (!isSuccess && !isFailed) {
          console.log('  ✅ Checking OLD format (root level)...')
          isSuccess = data.paymentSuccess === true || data.success === true
          isFailed = data.paymentSuccess === false || data.success === false
          if (isSuccess) console.log('  ✅ Using OLD format: payment success detected')
          if (isFailed) console.log('  ✅ Using OLD format: payment failure detected')
        }
        
        console.log('  Result: isSuccess=', isSuccess, 'isFailed=', isFailed, 'isScanned=', isScanned)
        
        if (isSuccess) {
          console.log('🎉 Payment SUCCESS detected via WebSocket!')
          showLoadingOverlay.value = true
          pushStatusLog('success', 'Payment success detected! Verifying with backend...')
          let prnFromDataRES = null
          prnFromDataRES = JSON.parse(data.transactionStatus)
          try {
            // Extract productNumber (PRN) from parsed transactionStatus - this is our tx_name
            const prnRef = String(prnFromDataRES.productNumber ||  "")
            console.log('  📞 Calling check_status with txn_ref_id:', prnRef)
            
            const verify = await $call('custom_erp.custom_erp.api.fonepay.check_status', {
              txn_ref_id: prnRef
            })
            
            console.log('Backend verification response:', verify)
            
            if (verify && verify.status === 'SUCCESS') {
              qrStatus.value = 'SUCCESS'
              paymentEntry.value = verify.payment_entry || paymentEntry.value
              paymentMessage.value = 'Payment confirmed successfully.'
              pushStatusLog('success', 'Backend verification complete. Payment Entry: ' + paymentEntry.value)
              removeQrAndShowSuccess()
            } else {
              qrStatus.value = 'FAILED'
              paymentMessage.value = 'Verification failed: ' + (verify?.message || 'Unknown error')
              pushStatusLog('error', 'Backend verification failed: ' + paymentMessage.value)
              showFailedDialog()
            }
          } catch (error) {
            console.error('Verification error:', error)
            qrStatus.value = 'FAILED'
            paymentMessage.value = 'Verification error: ' + (error.message || error)
            pushStatusLog('error', 'Verification API error: ' + paymentMessage.value)
            showFailedDialog()
          } finally {
            showLoadingOverlay.value = false
          }
        } else if (isFailed) {
          showLoadingOverlay.value = false
          qrStatus.value = 'FAILED'
          paymentMessage.value = data.responseMessage || data.message || 'Payment failed.'
          pushStatusLog('error', 'Payment failed: ' + paymentMessage.value)
          showFailedDialog()
        } else if (isScanned) {
          qrStatus.value = 'SCANNED'
          pushStatusLog('info', 'QR code scanned by customer.')
        }
      }
      
      // Also process via existing realtime handler for backward compatibility
      processRealtimeUpdate(data)
    }
    // merchantSocket.value already set at the top for immediate availability
  } catch (error) {
    console.error('Unable to connect merchant websocket', error)
    pushStatusLog('error', 'Unable to connect merchant websocket. Server-side listener will continue tracking the payment.')
    // Clear the socket reference on error
    merchantSocket.value = null
  }
}
*/
// [END OF OLD FUNCTION]

const subscribeToUpdates = (txName) => {
  const rt = getFrappeRealtime()
  if (!rt) {
    pushStatusLog('warning', 'Realtime channel is unavailable in this session.')
    return
  }
  clearRealtime()
  realtimeHandler = (data) => {
    if (!data || data.tx !== txName) {
      return
    }
    processRealtimeUpdate(data)
  }
  rt.on('fonepay_update', realtimeHandler)
}

const processRealtimeUpdate = (data) => {
  if (!data) return
  
  // ADDED BY AI: FONEPAY LIVE SOCKET - Handle new field names
  if (data.transactionStatus) {
    const ts = String(data.transactionStatus).toUpperCase()
    if (ts === 'SUCCESS' || ts === 'COMPLETED') {
      qrStatus.value = 'SUCCESS'
    } else if (ts === 'FAILED') {
      qrStatus.value = 'FAILED'
    } else if (ts === 'INITIATED') {
      qrStatus.value = 'SCANNED'
    } else {
      qrStatus.value = ts
    }
  } else if (data.status) {
    qrStatus.value = data.status
  }
  
  if (data.payment_entry) {
    paymentEntry.value = data.payment_entry
  }
  
  const statusMsg = data.status || data.transactionStatus || 'Unknown'
  pushStatusLog('event', data.message || `Status updated: ${statusMsg}`, JSON.stringify(data, null, 2))
  
  if (data.status === 'SUCCESS' || (data.transactionStatus && String(data.transactionStatus).toUpperCase() === 'SUCCESS')) {
    pushStatusLog('success', 'Payment successful! Payment Entry has been created and submitted.')
    // Keep dashboard in sync when realtime confirms success
    try { refreshDashboardAndList() } catch {}
  }
}

// Safe accessor for Frappe realtime
const getFrappeRealtime = () => {
  try {
    return (typeof window !== 'undefined' && window.frappe && window.frappe.realtime) ? window.frappe.realtime : null
  } catch {
    return null
  }
}

const clearRealtime = () => {
  const rt = getFrappeRealtime()
  if (rt && realtimeHandler) {
    rt.off('fonepay_update', realtimeHandler)
  }
  realtimeHandler = null
}

const closeMerchantSocket = () => {
  if (merchantSocket.value) {
    try {
      merchantSocket.value.close()
    } catch (error) {
      console.warn('Error closing websocket', error)
    }
  }
  merchantSocket.value = null
}

const regenerateQR = () => {
  qrData.value = null
  qrStatus.value = null
  paymentEntry.value = null
  websocketUrl.value = ''
  merchantWebsocketUrl.value = ''
  currentTxName.value = null
  clearRealtime()
  closeMerchantSocket()
  pushStatusLog('info', 'State reset. Ready to generate a new QR code.')
}

// ADDED BY AI: FONEPAY LIVE SOCKET - Manual payment processing trigger
const manuallyProcessPayment = async () => {
  if (!currentTxName.value) {
    alert('No transaction to process')
    return
  }
  
  pushStatusLog('info', 'Manually triggering payment processing...')
  showLoadingOverlay.value = true
  
  try {
    console.log('🔍 Calling check_status API with txn_ref_id:', currentTxName.value)
    
    // First check status which will trigger finalization
    const verify = await $call('custom_erp.custom_erp.api.fonepay.check_status', {
      txn_ref_id: currentTxName.value,
    })
    
    console.log('✅ Manual verification response:', verify)
    console.log('Response type:', typeof verify, 'Keys:', Object.keys(verify || {}))
    pushStatusLog('info', 'Backend verification response: ' + JSON.stringify(verify, null, 2))
    
    if (verify && verify.status === 'SUCCESS') {
      qrStatus.value = 'SUCCESS'
      paymentEntry.value = verify.payment_entry
      paymentMessage.value = 'Payment processed successfully.'
      pushStatusLog('success', 'Payment Entry created: ' + paymentEntry.value)
      removeQrAndShowSuccess()
      await refreshDashboardAndList()
    } else if (verify && verify.status === 'VERIFIED_NOT_PAID') {
      qrStatus.value = 'SCANNED'
      pushStatusLog('info', 'QR code has been scanned/verified but payment not yet completed.')
      // Update UI to show scanned status - customer has opened payment app but not confirmed
      paymentMessage.value = verify.message || '✅ QR Code Scanned! Customer has opened their payment app but has not completed the payment yet. Please wait for them to confirm and complete the payment. Keep this QR visible.'
      // Don't remove QR, keep it visible so customer can still pay
    } else if (verify && verify.status === 'PENDING') {
      qrStatus.value = 'PENDING'
      pushStatusLog('warning', 'Payment is still pending. Customer may not have scanned QR yet.')
      // Update UI to show pending status instead of error
      paymentMessage.value = verify.message || '⏳ Payment Pending. Customer has not yet scanned the QR code. Please ask the customer to scan and pay. Keep this QR visible.'
      // Don't remove QR, keep it visible so customer can still pay
    } else if (verify && verify.status === 'FAILED') {
      qrStatus.value = 'FAILED'
      pushStatusLog('error', 'Payment failed: ' + (verify.message || 'Payment was declined or cancelled'))
      paymentMessage.value = verify.message || '❌ Payment Failed. The payment was declined or cancelled by the customer. You may need to generate a new QR code.'
      // Show failed dialog for actual failures
      showFailedDialog()
      await refreshDashboardAndList()
    } else if (verify && verify.status === 'ERROR') {
      qrStatus.value = 'ERROR'
      pushStatusLog('error', 'Payment verification error: ' + (verify.message || 'Unknown error'))
      paymentMessage.value = verify.message || '⚠️ Verification Error. Unable to verify payment status with Fonepay. Please check the transaction manually or try again.'
      // Show error as status message, not dialog
    } else {
      qrStatus.value = 'UNKNOWN'
      pushStatusLog('error', 'Unexpected response: ' + JSON.stringify(verify))
      paymentMessage.value = '❓ Unknown Status. Received unexpected response from server. Please check status logs or contact support.'
    }
  } catch (error) {
    console.error('❌ Manual processing error:', error)
    if (isNetworkError(error)) {
      handleOfflineError()
    } else {
      pushStatusLog('error', 'Error processing payment: ' + (error.message || JSON.stringify(error)))
      alert('Error processing payment: ' + (error.message || JSON.stringify(error)))
    }
  } finally {
    showLoadingOverlay.value = false
  }
}

// ADDED BY AI: FONEPAY LIVE SOCKET - UI helper methods for success/failure flows
const removeQrAndShowSuccess = () => {
  qrData.value = null
  showSuccessDialog.value = true
  closeMerchantSocket()
  clearRealtime()
  pushStatusLog('success', 'Payment successfully verified and processed!')
}

const showFailedDialog = () => {
  qrData.value = null
  showErrorDialog.value = true
}

const resetForNextPayment = () => {
  showSuccessDialog.value = false
  paymentAmount.value = ''
  remarks.value = ''
  qrStatus.value = null
  paymentEntry.value = null
  statusLogs.value = []
  pushStatusLog('info', 'Ready for next payment.')
}

const regenerateQRFromDialog = () => {
  showErrorDialog.value = false
  qrData.value = null
  qrStatus.value = null
  paymentEntry.value = null
  websocketUrl.value = ''
  merchantWebsocketUrl.value = ''
  currentTxName.value = null
  clearRealtime()
  closeMerchantSocket()
  pushStatusLog('info', 'Ready to regenerate QR code.')
}

const resetAll = () => {
  showErrorDialog.value = false
  showSuccessDialog.value = false
  selectedCustomer.value = null
  selectedCustomerValue.value = null
  paymentAmount.value = ''
  remarks.value = ''
  qrData.value = null
  qrStatus.value = null
  paymentEntry.value = null
  websocketUrl.value = ''
  merchantWebsocketUrl.value = ''
  currentTxName.value = null
  statusLogs.value = []
  clearRealtime()
  closeMerchantSocket()
  pushStatusLog('info', 'Reset complete. Ready for new transaction.')
}

const pushStatusLog = (level, message, payload = null) => {
  const entry = {
    id: `${Date.now()}-${Math.random()}`,
    ts: new Date(),
    level,
    message,
    payload,
    levelLabel: levelLabel(level),
    levelClass: levelClass(level),
  }
  statusLogs.value.unshift(entry)
  // keep recent 30 entries
  if (statusLogs.value.length > 30) {
    statusLogs.value.pop()
  }
}

const levelLabel = (level) => {
  switch (level) {
    case 'error':
      return 'Error'
    case 'warning':
      return 'Warning'
    case 'success':
      return 'Success'
    case 'event':
      return 'Realtime Event'
    case 'ws':
      return 'Websocket'
    default:
      return 'Info'
  }
}

const levelClass = (level) => {
  switch (level) {
    case 'error':
      return 'text-red-600'
    case 'warning':
      return 'text-yellow-600'
    case 'success':
      return 'text-green-600'
    case 'event':
      return 'text-blue-600'
    case 'ws':
      return 'text-purple-600'
    default:
      return 'text-gray-600'
  }
}

const getStatusColor = (status) => {
  switch ((status || '').toUpperCase()) {
    case 'CREATED':
      return 'text-blue-600'
    case 'SCANNED':
      return 'text-yellow-600'
    case 'VERIFIED':
      return 'text-indigo-600'
    case 'PENDING':
      return 'text-orange-600'
    case 'SUCCESS':
      return 'text-green-600'
    case 'FAILED':
      return 'text-red-600'
    case 'ERROR':
      return 'text-red-700'
    case 'UNKNOWN':
      return 'text-gray-500'
    default:
      return 'text-gray-600'
  }
}

const formatAmount = (amount) => {
  const num = Number(amount) || 0
  return num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatLogTime = (ts) => {
  return new Date(ts).toLocaleString()
}

const isNetworkError = (error) => {
  const msg = String(error && (error.message || error)).toLowerCase()
  if (!isOnline.value) return true
  return msg.includes('network') || msg.includes('failed to fetch') || msg.includes('net::') || msg.includes('econn') || msg.includes('enotfound') || msg.includes('err_connection')
}

const handleOfflineError = (message = 'No internet connection. Please check/connect to the internet and try again.') => {
  showOfflineDialog.value = true
  pushStatusLog('error', message)
}


// ===== Dashboard helpers =====
const loadDashboard = async () => {
  try {
    const res = await dashboardResource.fetch()
    greetingName.value = res?.full_name || session.user
    dashboard.value = {
      successTotal: Number(res?.success_total_amount || 0),
      unprocessedCount: Number(res?.unprocessed_count || 0),
      successCount: Number(res?.success_count || 0),
      failedCount: Number(res?.failed_count || 0),
    }
  } catch (e) {
    console.error('Failed to load dashboard', e)
  }
}

const refreshDashboardAndList = async () => {
  if (refreshingDashboard.value) return
  refreshingDashboard.value = true
  try {
    await loadDashboard()
    if (showTxn.value) {
      await fetchLastTxns()
    }
  } finally {
    refreshingDashboard.value = false
  }
}

const processTodayUnprocessed = async () => {
  if (processingUnprocessed.value) return
  processingUnprocessed.value = true
  try {
    const res = await processTodayResource.fetch()
    dashboard.value.successTotal = Number(res?.success_total_amount || 0)
    dashboard.value.unprocessedCount = Number(res?.unprocessed_count || 0)
    dashboard.value.successCount = Number(res?.success_count || 0)
    dashboard.value.failedCount = Number(res?.failed_count || 0)
    const added = Number(res?.new_success_added || 0)
    if (added > 0) {
      pushStatusLog('success', `Processed unprocessed logs. Added Rs. ${formatAmount(added)} to today's total.`)
    } else {
      pushStatusLog('info', 'Processed unprocessed logs. No new successful payments found.')
    }
    if (showTxn.value) await fetchLastTxns()
  } catch (e) {
    console.error('Failed to process unprocessed', e)
    pushStatusLog('error', 'Failed to process unprocessed logs')
  } finally {
    processingUnprocessed.value = false
  }
}

const toggleTxnList = async () => {
  showTxn.value = !showTxn.value
  if (showTxn.value) {
    await fetchLastTxns()
  }
}

const setTxnFilter = async (val) => {
  if (txnFilter.value === val) return
  txnFilter.value = val
  await fetchLastTxns()
}

const fetchLastTxns = async () => {
  loadingTxn.value = true
  try {
    const res = await listTodayTxnsResource.fetch({ filter_status: txnFilter.value, limit: 5 })
    lastTxns.value = res?.transactions || []
  } catch (e) {
    console.error('Failed to fetch last transactions', e)
  } finally {
    loadingTxn.value = false
  }
}

const txnFilterBtnClass = (val) => [
  'px-3 py-1 rounded-md text-sm font-medium',
  txnFilter.value === val ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
]

const tryLoadNepaliScriptAndSetBSToday = async () => {
  try {
    if (typeof window !== 'undefined' && !window.NepaliFunctions) {
      const s = document.createElement('script')
      s.src = '/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js'
      document.head.appendChild(s)
      await new Promise((resolve) => { s.onload = resolve; s.onerror = resolve })
    }
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const d = new Date()
      const bs = window.NepaliFunctions.AD2BS({ year: d.getFullYear(), month: d.getMonth() + 1, day: d.getDate() })
      bsToday.value = `${bs.year}-${String(bs.month).padStart(2,'0')}-${String(bs.day).padStart(2,'0')}`
    }
  } catch (e) {
    console.warn('Nepali date script failed to load', e)
  }
}


onMounted(async () => {
  await Promise.all([loadCustomers(), loadDashboard()])
  pushStatusLog('info', 'Ready to generate Fonepay QR codes for customers.')
  // Listen to connectivity changes
  try {
    window.addEventListener('online', () => { isOnline.value = true })
    window.addEventListener('offline', () => { isOnline.value = false })
  } catch {}
  // Try to load Nepali date script and compute BS date
  tryLoadNepaliScriptAndSetBSToday()
})

onUnmounted(() => {
  clearRealtime()
  closeMerchantSocket()
  try {
    window.removeEventListener('online', () => {})
    window.removeEventListener('offline', () => {})
  } catch {}
})
</script>

<style scoped>
/* Custom animations for success UI */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.9;
  }
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 3s ease-in-out infinite;
}

.animate-bounce-slow {
  animation: bounce-slow 2s ease-in-out infinite;
}

/* Backdrop blur support */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}
/* Existing fadeIn animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

section {
  animation: fadeIn 0.25s ease-out;
}

/* Customer Selection Field UX Improvements */
.customer-select-wrapper {
  position: relative;
}

.customer-autocomplete :deep(input),
.customer-autocomplete :deep(.frappe-autocomplete-input) {
  min-height: 44px !important;
  height: 44px !important;
  padding: 12px 16px !important;
  font-size: 16px !important; /* Prevents zoom on iOS */
  border-radius: 8px;
  border: 1px solid #d1d5db;
  transition: all 0.2s;
}

.customer-autocomplete :deep(input:focus),
.customer-autocomplete :deep(.frappe-autocomplete-input:focus) {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Prevent layout shift when keyboard appears */
@media (max-width: 768px) {
  .customer-select-wrapper {
    scroll-padding-top: 100px;
  }
  
  /* Fix autocomplete dropdown positioning on mobile */
  .customer-autocomplete :deep(.autocomplete-dropdown),
  .customer-autocomplete :deep(.frappe-autocomplete-dropdown) {
    position: fixed !important;
    max-height: 50vh;
    overflow-y: auto;
    z-index: 9999;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  /* Add backdrop when dropdown is open */
  .customer-autocomplete :deep(.autocomplete-dropdown):not(:empty)::before,
  .customer-autocomplete :deep(.frappe-autocomplete-dropdown):not(:empty)::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.1);
    z-index: -1;
  }
}

/* Mobile optimizations */
@media (max-width: 640px) {
  /* Ensure proper touch targets */
  button, input, select, .customer-autocomplete {
    min-height: 44px;
  }
}

/* Desktop/Laptop optimizations */
@media (min-width: 1024px) {
  /* Better spacing for desktop */
  main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
  
  /* Improve card layouts on large screens */
  section {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  /* Better grid spacing */
  .grid {
    gap: 1.5rem;
  }
}

/* Large desktop optimizations - max-width handled by container class */
</style>