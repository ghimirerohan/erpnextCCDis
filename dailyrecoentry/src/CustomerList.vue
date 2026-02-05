<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Customer List View (Fixed tag error) -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50">
    <!-- Header - Mobile Optimized -->
    <header class="bg-white shadow-md border-b-2 border-gray-300 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-3 sm:py-4">
          <div class="flex items-center space-x-2 sm:space-x-4 flex-1 min-w-0">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-white border-2 border-gray-300 rounded-lg shadow-md flex-shrink-0">
              <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: rgba(103, 101, 101, 1);">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <div class="min-w-0 flex-1">
              <h1 class="text-base sm:text-xl lg:text-2xl font-bold text-gray-900 truncate">Daily Payment Entry</h1>
              <p class="text-xs sm:text-sm text-gray-700 font-medium truncate">Collect payments • {{ session.user }}</p>
            </div>
          </div>
          <!-- Refresh Button -->
          <button
            @click="refreshData"
            :disabled="refreshing"
            class="inline-flex items-center justify-center w-10 h-10 sm:w-auto sm:px-4 sm:py-2 border-2 border-sky-500 rounded-md shadow-sm text-xs sm:text-sm font-semibold text-white bg-sky-600 hover:bg-sky-700 hover:border-sky-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition-all duration-200 ml-2 flex-shrink-0 disabled:opacity-50 active:scale-95"
            title="Refresh data"
          >
            <svg 
              :class="['w-5 h-5 sm:w-4 sm:h-4', 'refresh-button-svg', refreshing ? 'animate-spin' : '']" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              style="stroke: white;"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            <span class="hidden sm:inline sm:ml-2" style="color: rgba(103, 101, 101, 1);">Refresh</span>
          </button>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border-2 border-gray-300 rounded-md shadow-sm text-xs sm:text-sm font-semibold text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition-all duration-200 ml-2 flex-shrink-0"
          >
            <svg class="w-4 h-4 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <svg class="animate-spin h-12 w-12 text-sky-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Admin: Driver Selection -->
      <div v-else-if="!recoData && isAdmin && availableDrivers.length > 0" class="text-center py-12">
        <div class="max-w-md mx-auto">
          <svg class="mx-auto h-24 w-24 text-blue-500 drop-shadow" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          <h3 class="mt-4 text-2xl font-bold text-gray-900">Administrator View</h3>
          <p class="mt-2 text-gray-700 font-medium mb-6">Select a driver to view their payment reconciliation</p>
          
          <div class="bg-white rounded-xl shadow-lg border-2 border-blue-500 p-6">
            <label class="block text-sm font-semibold text-gray-900 mb-3 text-left">Select Driver</label>
            <select
              v-model="selectedDriver"
              @change="loadDriverData"
              class="block w-full px-4 py-3 text-base border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 rounded-lg bg-white text-gray-900 font-medium shadow-sm transition-all duration-200"
            >
              <option :value="null" class="text-gray-500">-- Choose a driver --</option>
              <option v-for="driver in availableDrivers" :key="driver.driver" :value="driver.driver_name" class="text-gray-900 font-medium">
                {{ driver.driver_name }} ({{ driver.count }} customers)
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else-if="!recoData && !isAdmin" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-4 text-xl font-medium text-gray-900">No Active Reconciliation</h3>
        <p class="mt-2 text-gray-600">No payment reconciliation found for your account.</p>
      </div>
      
      <!-- No Drivers Available (Admin) -->
      <div v-else-if="!recoData && isAdmin && availableDrivers.length === 0" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-4 text-xl font-medium text-gray-900">No Active Reconciliations</h3>
        <p class="mt-2 text-gray-600">No drivers have active payment reconciliations.</p>
      </div>

      <!-- Main Content -->
      <template v-else>
        <!-- Company Header Banner -->
        <div v-if="currentCompany" 
             class="rounded-xl border-2 p-4 shadow-md flex items-center justify-between"
             :style="{ backgroundColor: companyColors.bg, borderColor: companyColors.primary }">
          <div class="flex items-center gap-4">
            <CompanyBadge :company="currentCompany" :companyConfig="companyConfig" size="lg" />
            <div>
              <h2 class="text-lg font-bold" :style="{ color: companyColors.primary }">
                {{ currentCompany }}
              </h2>
              <p class="text-sm" :style="{ color: companyColors.primary, opacity: 0.8 }">
                {{ companyDistributionLabel }}
              </p>
            </div>
          </div>
          <div class="text-right">
            <span class="text-xs font-medium px-3 py-1 rounded-full"
                  :style="{ backgroundColor: companyColors.light, color: companyColors.text }">
              {{ companyAbbr }}
            </span>
          </div>
        </div>

        <!-- Admin: Driver Switcher -->
        <div v-if="isAdmin && availableDrivers.length > 1" class="bg-blue-50 rounded-xl border-2 border-blue-300 p-4 shadow-md">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <label class="text-sm font-semibold text-gray-900 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              Switch Driver:
            </label>
            <select
              v-model="selectedDriver"
              @change="loadDriverData"
              class="px-4 py-2.5 border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 rounded-lg bg-white text-gray-900 font-medium shadow-sm transition-all duration-200 min-w-[250px]"
            >
              <option v-for="driver in availableDrivers" :key="driver.driver" :value="driver.driver_name" class="text-gray-900 font-medium">
                {{ driver.driver_name }} ({{ driver.count }} customers)
              </option>
            </select>
          </div>
        </div>

        <!-- Summary Card -->
        <SummaryCard
          :driver-name="driverName"
          :summary="recoData.summary"
          :reco-name="recoData.reco.name"
          @view-all="showAllDialog = true"
          @expense-updated="handleExpenseUpdated"
          @qr-processed="handleQrProcessed"
        />

        <!-- Search & Filters -->
        <div class="bg-white rounded-xl shadow-lg border-2 border-gray-300 p-4 sm:p-6">
          <div class="flex flex-col gap-4">
            <!-- Search Input -->
            <div class="relative">
              <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by customer name or code..."
                class="block w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-base transition-all duration-200 bg-white text-gray-900 placeholder-gray-500"
              />
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <!-- Filter Buttons & Add Entry -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div class="flex gap-2 flex-wrap order-2 sm:order-1 items-center">
                <button
                  @click="setFilter(null)"
                  :class="[
                    'px-3 py-2 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all duration-200',
                    filterSettled === null 
                      ? 'bg-blue-600 text-white shadow-lg hover:bg-blue-700 border-2 border-blue-700' 
                      : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                  ]"
                >
                  All ({{ allCount }})
                </button>
                <button
                  @click="setFilter(false)"
                  :class="[
                    'px-3 py-2 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-all duration-200',
                    filterSettled === false 
                      ? 'bg-amber-600 text-white shadow-md hover:bg-amber-700' 
                      : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                  ]"
                >
                  Pending ({{ pendingCount }})
                </button>
                <button
                  @click="setFilter(true)"
                  :class="[
                    'px-3 py-2 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-all duration-200',
                    filterSettled === true 
                      ? 'bg-green-600 text-white shadow-md hover:bg-green-700' 
                      : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
                  ]"
                >
                  Settled ({{ settledCount }})
                </button>
                
                <!-- Add Entry Button - in filter bar -->
                <button
                  @click="openAddEntryDialog"
                  class="px-3 py-2 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all duration-200 shadow-md inline-flex items-center gap-1"
                  style="background-color: #0284c7 !important; color: #ffffff !important; border: 2px solid #0369a1 !important;"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ffffff !important;">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                  </svg>
                  <span class="sm:inline" style="color: #ffffff !important;">+ Add</span>
                </button>
              </div>

              <!-- Settle All as Cash Button -->
              <div v-if="filterSettled === false && pendingCount > 0" class="order-1 sm:order-2">
                <button
                  @click="confirmSettleAllCash"
                  class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2.5 rounded-lg shadow-lg transition-all active:scale-95 border-2 whitespace-nowrap"
                  style="background-color: #059669 !important; border-color: #047857 !important; color: #ffffff !important; font-weight: 800 !important; display: inline-flex !important;"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ffffff !important;">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
                  </svg>
                  <span style="color: #ffffff !important;">Remaining as Cash</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Customer List -->
        <div class="bg-white rounded-xl shadow-lg border-2 border-gray-300 overflow-hidden">
          <div v-if="filteredLines.length === 0" class="p-8 text-center">
            <svg class="mx-auto h-16 w-16 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <p class="text-gray-600 font-medium">No customers found matching your search.</p>
            <p class="text-sm text-gray-500 mt-1">Try adjusting your search or filter criteria.</p>
          </div>
          
          <div v-else class="divide-y divide-gray-200">
            <div
              v-for="(line, index) in filteredLines"
              :key="line.name"
              @click="openCustomerPayment(line)"
              class="p-3 sm:p-4 hover:bg-blue-50 cursor-pointer transition-colors active:bg-blue-100 flex gap-3 sm:gap-4 items-start"
            >
              <!-- Numbering -->
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-gray-100 rounded-full border border-gray-300 flex items-center justify-center text-xs sm:text-sm font-bold text-gray-600 mt-1">
                {{ index + 1 }}
              </div>

              <div class="flex-1 min-w-0">
                <!-- Mobile Layout (stacked) -->
                <div class="flex flex-col gap-2 md:hidden">
                  <div class="flex items-start justify-between gap-2">
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-1.5">
                        <h4 class="text-sm font-bold text-gray-900 leading-tight break-words">{{ line.customer_name }}</h4>
                        <span v-if="line.updated_later" class="text-[10px] font-semibold text-amber-700 bg-amber-50 border border-amber-300 px-1.5 py-0.5 rounded">Added</span>
                      </div>
                      <p class="text-xs text-gray-600 font-mono mt-0.5">{{ line.customer }}</p>
                    </div>
                    <span
                      v-if="line.settled === 1 || line.settled === true"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-800 border border-green-300 flex-shrink-0"
                    >
                      <svg class="w-3 h-3 mr-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                      Settled
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300 flex-shrink-0"
                    >
                      <svg class="w-3 h-3 mr-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                      </svg>
                      Pending
                    </span>
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-base font-bold text-gray-900">{{ formatCurrency(line.net_total_amount) }}</p>
                      <p v-if="line.remaining_amount > 0" class="text-xs text-gray-600">Remaining: {{ formatCurrency(line.remaining_amount) }}</p>
                      
                      <!-- Settled details for mobile -->
                      <div v-if="line.settled === 1 || line.settled === true" class="flex flex-wrap gap-1 mt-1">
                        <span v-if="line.cash_amount > 0" class="text-[10px] px-1.5 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded">Cash: {{ formatCurrency(line.cash_amount) }}</span>
                        <span v-if="line.qr_amount > 0" class="text-[10px] px-1.5 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded">QR: {{ formatCurrency(line.qr_amount) }}</span>
                        <span v-if="line.cheque_amount > 0" class="text-[10px] px-1.5 py-0.5 bg-purple-50 text-purple-700 border border-purple-200 rounded">Cheque: {{ formatCurrency(line.cheque_amount) }}</span>
                        <span v-if="line.credit_amount > 0" class="text-[10px] px-1.5 py-0.5 bg-red-50 text-red-700 border border-red-200 rounded">Credit: {{ formatCurrency(line.credit_amount) }}</span>
                        <span v-if="line.return_amount > 0" class="text-[10px] px-1.5 py-0.5 bg-orange-50 text-orange-700 border border-orange-200 rounded">Return: {{ formatCurrency(line.return_amount) }}</span>
                      </div>
                    </div>
                    <svg class="w-5 h-5 text-gray-500 flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
                
                <!-- Desktop/Tablet Layout (horizontal) -->
                <div class="hidden md:flex items-start justify-between gap-3">
                  <div class="flex-grow min-w-0">
                    <div class="flex items-center gap-2">
                      <h4 class="text-base lg:text-lg font-semibold text-gray-900 break-words">{{ line.customer_name }}</h4>
                      <span v-if="line.updated_later" class="text-xs font-semibold text-amber-700 bg-amber-50 border border-amber-300 px-1.5 py-0.5 rounded">Added</span>
                    </div>
                    <p class="text-xs sm:text-sm text-gray-600 font-mono mt-0.5">{{ line.customer }}</p>
                    
                    <!-- Settled details for desktop -->
                    <div v-if="line.settled === 1 || line.settled === true" class="flex flex-wrap gap-2 mt-2">
                      <span v-if="line.cash_amount > 0" class="text-xs px-2 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded-md font-medium">Cash: {{ formatCurrency(line.cash_amount) }}</span>
                      <span v-if="line.qr_amount > 0" class="text-xs px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-md font-medium">QR: {{ formatCurrency(line.qr_amount) }}</span>
                      <span v-if="line.cheque_amount > 0" class="text-xs px-2 py-0.5 bg-purple-50 text-purple-700 border border-purple-200 rounded-md font-medium">Cheque: {{ formatCurrency(line.cheque_amount) }}</span>
                      <span v-if="line.credit_amount > 0" class="text-xs px-2 py-0.5 bg-red-50 text-red-700 border border-red-200 rounded-md font-medium">Credit: {{ formatCurrency(line.credit_amount) }}</span>
                      <span v-if="line.return_amount > 0" class="text-xs px-2 py-0.5 bg-orange-50 text-orange-700 border border-orange-200 rounded-md font-medium">Return: {{ formatCurrency(line.return_amount) }}</span>
                    </div>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <p class="text-base lg:text-lg font-bold text-gray-900 whitespace-nowrap">{{ formatCurrency(line.net_total_amount) }}</p>
                    <p v-if="line.remaining_amount > 0" class="text-xs sm:text-sm text-gray-600 whitespace-nowrap font-medium">Remaining: {{ formatCurrency(line.remaining_amount) }}</p>
                  </div>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <span
                      v-if="line.settled === 1 || line.settled === true"
                      class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800 border border-green-300"
                    >
                      <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                      Settled
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300"
                    >
                      <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                      </svg>
                      Pending
                    </span>
                    <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </main>

    <!-- Add New Entry Dialog -->
    <div v-if="showAddEntryDialog" class="fixed inset-0 z-50 flex items-center justify-center p-4" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="fixed inset-0 bg-gray-900 bg-opacity-60 transition-opacity" @click="closeAddEntryDialog"></div>

      <div class="relative bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all w-full max-w-lg mx-auto" style="border: 3px solid #0284c7;">
        <div class="px-5 py-4" style="background: linear-gradient(135deg, #0284c7, #0369a1);">
          <h3 class="text-xl leading-6 font-bold flex items-center" style="color: #ffffff !important;">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ffffff;">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span style="color: #ffffff !important;">{{ addEntryStep === 'input' ? 'Add New Entry' : 'Confirm New Entry' }}</span>
          </h3>
        </div>
          
          <div class="bg-white px-5 pt-5 pb-4">
            <!-- Step 1: Input -->
            <div v-if="addEntryStep === 'input'" class="space-y-5">
              <!-- Customer Search/Select -->
              <div>
                <label class="block text-sm font-bold mb-2" style="color: #1f2937 !important;">Customer</label>
                <div class="relative">
                  <input
                    v-model="customerSearchQuery"
                    @input="filterCustomers"
                    @focus="showCustomerDropdown = true"
                    type="text"
                    placeholder="Search customer by name or code..."
                    class="block w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-base"
                  />
                  <!-- Customer Dropdown -->
                  <div v-if="showCustomerDropdown && filteredCustomersList.length > 0" 
                       class="absolute z-10 mt-1 w-full bg-white border-2 border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                    <div
                      v-for="customer in filteredCustomersList"
                      :key="customer.name"
                      @click="selectCustomer(customer)"
                      class="px-4 py-2.5 hover:bg-sky-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                    >
                      <p class="font-medium text-gray-900">{{ customer.customer_name }}</p>
                      <p class="text-xs text-gray-500 font-mono">{{ customer.name }}</p>
                    </div>
                  </div>
                </div>
                <!-- Selected Customer Display -->
                <div v-if="selectedCustomerForAdd" class="mt-2 p-3 bg-sky-50 border border-sky-200 rounded-lg">
                  <p class="text-sm font-semibold text-sky-900">{{ selectedCustomerForAdd.customer_name }}</p>
                  <p class="text-xs text-sky-700 font-mono">{{ selectedCustomerForAdd.name }}</p>
                </div>
              </div>

              <!-- Amount Input -->
              <div>
                <label class="block text-sm font-bold mb-2" style="color: #1f2937 !important;">Amount</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 font-semibold" style="color: #374151 !important;">NPR</span>
                  <input
                    v-model.number="newEntryAmount"
                    type="number"
                    inputmode="decimal"
                    min="0"
                    step="0.01"
                    placeholder="0"
                    class="block w-full pl-14 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-base font-medium"
                  />
                </div>
              </div>

              <!-- Info if customer exists in reco -->
              <div v-if="selectedCustomerForAdd && existingCustomerInReco" class="p-3 bg-amber-50 border border-amber-300 rounded-lg">
                <p class="text-sm text-amber-800">
                  <strong>Note:</strong> This customer already exists in the reco. 
                  Amount will be <strong>added</strong> to their current total ({{ formatCurrency(existingCustomerInReco.initial_total_amount) }}).
                </p>
              </div>
            </div>

            <!-- Step 2: Confirmation -->
            <div v-else-if="addEntryStep === 'confirm'" class="space-y-4">
              <div class="p-4 bg-amber-50 border-l-4 border-amber-400 text-amber-700">
                <div class="flex">
                  <svg class="h-5 w-5 text-amber-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                  </svg>
                  <p class="text-sm font-bold">Please confirm the details below.</p>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4 space-y-3 border border-gray-200">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 font-medium">Customer:</span>
                  <span class="font-bold text-gray-900">{{ selectedCustomerForAdd?.customer_name }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 font-medium">Customer Code:</span>
                  <span class="font-mono text-gray-700">{{ selectedCustomerForAdd?.name }}</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-gray-300">
                  <span class="text-gray-600 font-medium">Amount to Add:</span>
                  <span class="font-bold text-xl text-sky-600">{{ formatCurrency(newEntryAmount) }}</span>
                </div>
                <div v-if="existingCustomerInReco" class="flex justify-between items-center text-sm">
                  <span class="text-gray-500">Current Amount:</span>
                  <span class="text-gray-600">{{ formatCurrency(existingCustomerInReco.initial_total_amount) }}</span>
                </div>
                <div v-if="existingCustomerInReco" class="flex justify-between items-center text-sm">
                  <span class="text-gray-500">New Total:</span>
                  <span class="font-semibold text-green-600">{{ formatCurrency(existingCustomerInReco.initial_total_amount + newEntryAmount) }}</span>
                </div>
              </div>

              <p class="text-sm text-gray-600">
                {{ existingCustomerInReco 
                   ? 'This amount will be added to the existing customer record.' 
                   : 'A new entry will be created for this customer.' }}
              </p>
            </div>
          </div>
          
          <div class="bg-gray-50 px-4 py-4 sm:px-6">
            <div class="flex flex-row justify-end gap-3">
              <button
                type="button"
                @click="closeAddEntryDialog"
                :disabled="addingEntry"
                class="inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-5 py-2.5 bg-white text-base font-bold text-gray-700 hover:bg-gray-100 transition-all"
              >
                Cancel
              </button>
              <button
                v-if="addEntryStep === 'confirm'"
                type="button"
                @click="addEntryStep = 'input'"
                :disabled="addingEntry"
                class="inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-5 py-2.5 bg-white text-base font-bold text-gray-700 hover:bg-gray-100 transition-all"
              >
                Back
              </button>
              <button
                v-if="addEntryStep === 'input'"
                type="button"
                @click="proceedToConfirm"
                :disabled="!canProceedToConfirm"
                class="inline-flex justify-center items-center rounded-lg shadow-sm px-5 py-2.5 text-base font-bold text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                style="background-color: #0284c7 !important; border: 2px solid #0369a1 !important;"
              >
                Continue
                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
              <button
                v-if="addEntryStep === 'confirm'"
                type="button"
                @click="submitNewEntry"
                :disabled="addingEntry"
                class="inline-flex justify-center items-center rounded-lg shadow-sm px-5 py-2.5 text-base font-bold text-white transition-all disabled:opacity-50"
                style="background-color: #16a34a !important; border: 2px solid #15803d !important;"
              >
                <svg v-if="addingEntry" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ addingEntry ? 'Adding...' : 'Confirm & Add' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Settle All Cash Confirmation Dialog -->
    <div v-if="showSettleAllDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showSettleAllDialog = false"></div>

        <div class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border-2" style="border-color: #059669;">
          <div class="px-4 py-4 sm:px-6" style="background-color: #059669 !important;">
            <h3 class="text-xl leading-6 font-bold flex items-center" style="color: #ffffff !important;">
              <svg class="w-6 h-6 mr-2 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ffffff !important;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span style="color: #ffffff !important; opacity: 1 !important; visibility: visible !important;">Settle Pending as Cash?</span>
            </h3>
          </div>
          
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6">
            <div class="space-y-4">
              <div class="p-4 bg-amber-50 border-l-4 border-amber-400 text-amber-700">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-bold">This action cannot be undone.</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4 space-y-2 border border-gray-200">
                <div class="flex justify-between items-center text-sm">
                  <span class="text-gray-600 font-medium">Pending Customers:</span>
                  <span class="font-bold text-gray-900">{{ pendingCount }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-gray-600 font-medium">Total Remaining Amount:</span>
                  <span class="font-bold text-lg" style="color: #059669;">{{ formatCurrency(recoData?.summary.remaining_amount) }}</span>
                </div>
              </div>

              <p class="text-sm text-gray-600">
                This will mark all <span class="font-bold text-gray-900">{{ pendingCount }}</span> pending customer records as fully settled. 
                The remaining balance for each will be added to their <span class="font-bold" style="color: #059669;">Cash Payment</span> field.
              </p>
            </div>
          </div>
          
          <div class="bg-gray-50 px-4 py-3 sm:px-6 flex flex-col sm:flex-row-reverse gap-2">
            <button
              type="button"
              @click="settleAllAsCash"
              :disabled="settlingAll"
              class="inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-6 py-2.5 text-base font-bold transition-all disabled:opacity-50"
              style="background-color: #059669 !important; color: #ffffff !important;"
            >
              <svg v-if="settlingAll" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" style="color: #ffffff !important;">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span style="color: #ffffff !important; opacity: 1 !important; visibility: visible !important;">Yes, Settle All as Cash</span>
            </button>
            <button
              type="button"
              @click="showSettleAllDialog = false"
              class="inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-6 py-2.5 bg-white text-base font-bold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- View All Dialog -->
    <div v-if="showAllDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showAllDialog = false"></div>

        <div class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">All Amount Details</h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Initial Total Amount:</span>
                <span class="font-semibold">{{ formatCurrency(recoData?.summary.initial_total_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Additional Amount:</span>
                <span class="font-semibold text-indigo-600">{{ formatCurrency(recoData?.summary.additional_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Return Amount:</span>
                <span class="font-semibold text-orange-600">{{ formatCurrency(recoData?.summary.return_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Net Total Amount:</span>
                <span class="font-semibold">{{ formatCurrency(recoData?.summary.net_total_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Cash Amount:</span>
                <span class="font-semibold text-green-600">{{ formatCurrency(recoData?.summary.cash_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">QR Amount:</span>
                <span class="font-semibold text-blue-600">{{ formatCurrency(recoData?.summary.qr_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Cheque Amount:</span>
                <span class="font-semibold text-purple-600">{{ formatCurrency(recoData?.summary.cheque_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Credit Amount:</span>
                <span class="font-semibold text-red-600">{{ formatCurrency(recoData?.summary.credit_amount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-700">Expense Amount:</span>
                <span class="font-semibold text-gray-600">{{ formatCurrency(recoData?.summary.expense_amount) }}</span>
              </div>
              <div class="flex justify-between py-3 border-t-2 border-gray-300 mt-2">
                <span class="text-gray-900 font-bold">Remaining Amount:</span>
                <span class="font-bold text-xl text-sky-600">{{ formatCurrency(recoData?.summary.remaining_amount) }}</span>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="showAllDialog = false"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-sky-600 text-base font-medium text-white hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '../../shared/data/session'
import { call } from 'frappe-ui'
import SummaryCard from './components/SummaryCard.vue'
import CompanyBadge from '../../shared/components/CompanyBadge.vue'

const router = useRouter()

const loading = ref(true)
const recoData = ref(null)
const driverName = ref('')
const searchQuery = ref('')
const filterSettled = ref(null)
const showAllDialog = ref(false)
const isAdmin = ref(false)
const availableDrivers = ref([])
const selectedDriver = ref(null)
// Company state
const currentCompany = ref('')
const companyConfig = ref(null)

// Check if company is horlicks-based
const isHorlicksCompany = computed(() => {
  return companyConfig.value?.main_product === 'horlicks' || companyConfig.value?.is_horlicks
})

// Backward compatibility alias
const isPadmashree = isHorlicksCompany

// Get company distribution label
const companyDistributionLabel = computed(() => {
  if (isHorlicksCompany.value) {
    const product = companyConfig.value?.main_product
    return product ? `${product.charAt(0).toUpperCase() + product.slice(1)} Distribution` : 'Horlicks Distribution'
  }
  return 'General Distribution'
})

// Get company badge/abbreviation
const companyAbbr = computed(() => {
  return companyConfig.value?.abbr || (isHorlicksCompany.value ? 'PS' : 'RS')
})

// Get company style colors
const companyColors = computed(() => {
  if (companyConfig.value?.brand_colors) {
    return companyConfig.value.brand_colors
  }
  return isHorlicksCompany.value 
    ? { primary: '#0077B6', bg: '#E6F4FA', light: '#DBEAFE', text: '#1E40AF' }
    : { primary: '#F40009', bg: '#FEE6E6', light: '#FEE2E2', text: '#991B1B' }
})

const showSettleAllDialog = ref(false)
const settlingAll = ref(false)
const refreshing = ref(false)

// Add Entry Dialog State
const showAddEntryDialog = ref(false)
const addEntryStep = ref('input') // 'input' or 'confirm'
const allCustomers = ref([])
const customerSearchQuery = ref('')
const filteredCustomersList = ref([])
const showCustomerDropdown = ref(false)
const selectedCustomerForAdd = ref(null)
const newEntryAmount = ref(0)
const addingEntry = ref(false)

const filteredLines = computed(() => {
  if (!recoData.value?.lines) return []
  
  let lines = recoData.value.lines
  
  // Filter by settled status
  // Note: Backend returns 0/1, convert to boolean for comparison
  if (filterSettled.value !== null) {
    lines = lines.filter(line => !!line.settled === filterSettled.value)
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    lines = lines.filter(line => 
      line.customer_name.toLowerCase().includes(query) ||
      line.customer.toLowerCase().includes(query)
    )
  }
  
  return lines
})

const allCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.length
})

const pendingCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.filter(line => !line.settled || line.settled === 0).length
})

const settledCount = computed(() => {
  if (!recoData.value?.lines) return 0
  return recoData.value.lines.filter(line => line.settled === 1 || line.settled === true).length
})

// Check if selected customer already exists in reco
const existingCustomerInReco = computed(() => {
  if (!selectedCustomerForAdd.value || !recoData.value?.lines) return null
  return recoData.value.lines.find(line => line.customer === selectedCustomerForAdd.value.name)
})

// Can proceed to confirmation
const canProceedToConfirm = computed(() => {
  return selectedCustomerForAdd.value && newEntryAmount.value > 0
})

const setFilter = (value) => {
  filterSettled.value = value
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedDriver.value) {
      params.driver_name = selectedDriver.value
    }

    const response = await call('custom_erp.api.payment_reco.get_driver_reco_data', params)
    
    isAdmin.value = response.is_admin || false
    
    if (response.success) {
      recoData.value = response.data
      driverName.value = response.data.reco.driver_name || session.user
      selectedDriver.value = driverName.value
      // Extract company from response
      currentCompany.value = response.data.reco.company || ''
      
      // Fetch company config for dynamic styling
      if (currentCompany.value) {
        await loadCompanyConfig(currentCompany.value)
      }
      
      // If admin, also make sure available drivers are loaded
      if (isAdmin.value && availableDrivers.value.length === 0) {
        await loadAllDrivers()
      }
    } else if (isAdmin.value) {
      // Admin user but no driver data for selection - load all drivers list
      recoData.value = null
      currentCompany.value = ''
      companyConfig.value = null
      await loadAllDrivers()
    } else {
      recoData.value = null
      currentCompany.value = ''
      companyConfig.value = null
    }
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

// Load company config for dynamic styling
const loadCompanyConfig = async (company) => {
  try {
    const response = await call('custom_erp.api.payment_reco.get_company_config', {
      company_name: company
    })
    if (response.success) {
      companyConfig.value = response.data
    }
  } catch (error) {
    console.error('Error loading company config:', error)
  }
}

const loadAllDrivers = async () => {
  try {
    const response = await call('custom_erp.api.payment_reco.get_all_active_recos')
    if (response.success) {
      availableDrivers.value = response.data
    }
  } catch (error) {
    console.error('Error loading drivers:', error)
  }
}

const loadDriverData = async () => {
  await loadData()
}

const refreshData = async () => {
  refreshing.value = true
  try {
    // Reload all drivers if admin
    if (isAdmin.value) {
      await loadAllDrivers()
    }
    // Reload the main data
    await loadData()
  } catch (error) {
    console.error('Error refreshing data:', error)
  } finally {
    refreshing.value = false
  }
}

const openCustomerPayment = (line) => {
  router.push({
    name: 'CustomerPayment',
    params: { lineName: line.name },
    query: { driver: driverName.value }
  })
}

const confirmSettleAllCash = () => {
  showSettleAllDialog.value = true
}

const settleAllAsCash = async () => {
  if (!recoData.value?.reco?.name) return
  
  settlingAll.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.settle_all_pending_as_cash', {
      reco_name: recoData.value.reco.name
    })
    
    if (response.success) {
      showSettleAllDialog.value = false
      await loadData() // Reload everything
      alert(response.message)
    } else {
      alert('Error: ' + response.message)
    }
  } catch (error) {
    console.error('Error settling all as cash:', error)
    alert('Failed to settle all as cash. Please try again.')
  } finally {
    settlingAll.value = false
  }
}

const handleExpenseUpdated = (updatedSummary) => {
  // Update the summary with the new values from the backend
  if (recoData.value && updatedSummary) {
    recoData.value.summary = {
      ...recoData.value.summary,
      expense_amount: updatedSummary.expense_amount,
      cash_amount: updatedSummary.cash_amount,
      cash_expected: updatedSummary.cash_expected,
      remaining_amount: updatedSummary.remaining_amount,
      cash_received: updatedSummary.cash_received,
      cash_difference: updatedSummary.cash_difference,
      qr_amount: updatedSummary.qr_amount,
      additional_amount: updatedSummary.additional_amount
    }
  }
}

const handleQrProcessed = async (processResults) => {
  // QR logs were processed - reload the data to get updated line information
  console.log('QR logs processed:', processResults)
  await loadData()
}

// --- Add Entry Dialog Methods ---

const openAddEntryDialog = async () => {
  showAddEntryDialog.value = true
  addEntryStep.value = 'input'
  customerSearchQuery.value = ''
  selectedCustomerForAdd.value = null
  newEntryAmount.value = 0
  filteredCustomersList.value = []
  showCustomerDropdown.value = false
  
  // Load customers appropriate for the company
  // Padmashree: Horlicks customers only
  // Riya: Non-Horlicks customers only
  try {
    const response = await call('custom_erp.api.payment_reco.get_customers_for_company', {
      company: currentCompany.value
    })
    if (response.success) {
      allCustomers.value = response.data
    }
  } catch (error) {
    console.error('Error loading customers:', error)
  }
}

const closeAddEntryDialog = () => {
  showAddEntryDialog.value = false
  addEntryStep.value = 'input'
  customerSearchQuery.value = ''
  selectedCustomerForAdd.value = null
  newEntryAmount.value = 0
  filteredCustomersList.value = []
  showCustomerDropdown.value = false
}

const filterCustomers = () => {
  if (!customerSearchQuery.value || customerSearchQuery.value.length < 1) {
    filteredCustomersList.value = []
    showCustomerDropdown.value = false
    return
  }
  
  const query = customerSearchQuery.value.toLowerCase()
  filteredCustomersList.value = allCustomers.value
    .filter(c => 
      c.customer_name.toLowerCase().includes(query) || 
      c.name.toLowerCase().includes(query)
    )
    .slice(0, 20) // Limit results
  showCustomerDropdown.value = filteredCustomersList.value.length > 0
}

const selectCustomer = (customer) => {
  selectedCustomerForAdd.value = customer
  customerSearchQuery.value = customer.customer_name
  showCustomerDropdown.value = false
  filteredCustomersList.value = []
}

const proceedToConfirm = () => {
  if (!canProceedToConfirm.value) return
  addEntryStep.value = 'confirm'
}

const submitNewEntry = async () => {
  if (!selectedCustomerForAdd.value || newEntryAmount.value <= 0 || !recoData.value?.reco?.name) {
    return
  }
  
  addingEntry.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.add_new_reco_entry', {
      reco_name: recoData.value.reco.name,
      customer: selectedCustomerForAdd.value.name,
      amount: newEntryAmount.value
    })
    
    if (response.success) {
      // Update summary with new data
      if (response.data) {
        recoData.value.summary = {
          ...recoData.value.summary,
          ...response.data
        }
      }
      
      // Close dialog and reload data
      closeAddEntryDialog()
      await loadData()
      
      alert(response.message)
    } else {
      alert('Error: ' + response.message)
    }
  } catch (error) {
    console.error('Error adding new entry:', error)
    alert('Failed to add entry. Please try again.')
  } finally {
    addingEntry.value = false
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.refresh-button-svg {
  background-color: rgba(153, 153, 153, 1);
}
</style>
