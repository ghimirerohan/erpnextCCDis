<!-- ADDED BY AI: DAILY_PAYMENT_RECO - Upload Reco Main Component -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center space-x-4">
            <div class="flex items-center justify-center w-12 h-12 bg-purple-600 rounded-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Payment Reconciliation Upload</h1>
              <p class="text-sm text-gray-600">Upload daily payment register • {{ session.user }}</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <!-- Company Selection Section (Required) -->
      <div class="bg-white rounded-xl shadow-lg border-2 p-6" :class="selectedCompany ? 'border-gray-200' : 'border-purple-500'">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="flex items-center space-x-3">
            <CompanyBadge v-if="selectedCompany" :company="selectedCompany" size="lg" />
            <div v-else class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Select Company</h3>
              <p class="text-sm text-gray-600">{{ selectedCompany ? companyDescription : 'Choose company to continue' }}</p>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <select
              v-model="selectedCompany"
              @change="handleCompanyChange"
              class="rounded-lg border-2 px-4 py-2.5 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-purple-500 min-w-[250px]"
              :class="selectedCompany ? 'border-gray-300 bg-white' : 'border-purple-500 bg-purple-50'"
            >
              <option :value="null">-- Select Company --</option>
              <option v-for="company in companiesList" :key="company.name" :value="company.name">
                {{ company.company_name }} {{ company.main_product ? `(${capitalizeFirst(company.main_product)})` : '' }}
              </option>
            </select>
          </div>
        </div>
        
        <!-- Company-specific info -->
        <div v-if="selectedCompany" class="mt-4 pt-4 border-t border-gray-200">
          <div v-if="isHorlicksCompany" class="flex items-start gap-3 p-3 rounded-lg border" :style="getCompanyInfoStyle()">
            <svg class="w-5 h-5 mt-0.5 flex-shrink-0" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="text-sm" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }">
              <p class="font-semibold">{{ currentCompanyConfig?.abbr || 'Horlicks' }} Mode:</p>
              <ul class="mt-1 space-y-1 list-disc list-inside opacity-90">
                <li>Works only with {{ capitalizeFirst(currentCompanyConfig?.main_product || 'horlicks') }} customer group</li>
                <li>Single driver for entire upload file</li>
                <li>No loadsheet number required</li>
                <li>Invoice numbers stored as Sales Reference</li>
              </ul>
            </div>
          </div>
          <div v-else class="flex items-start gap-3 p-3 rounded-lg border" :style="getCompanyInfoStyle()">
            <svg class="w-5 h-5 mt-0.5 flex-shrink-0" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#F40009' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="text-sm" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#F40009' }">
              <p class="font-semibold">{{ currentCompanyConfig?.abbr || 'Standard' }} Mode:</p>
              <ul class="mt-1 space-y-1 list-disc list-inside opacity-90">
                <li>Works with all customers except Horlicks</li>
                <li>Driver assigned per loadsheet</li>
                <li>CSV Format: Outlet Code, Outlet Name, Reference No, Amount</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Today's Summary Section (only show when company selected) -->
      <div v-if="selectedCompany && hasTodayRecords" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h3 class="text-xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            Today's Reconciliation Summary
          </h3>
          
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium text-gray-600">Filter:</label>
            <select 
              v-model="summaryDriver" 
              @change="fetchSummary"
              class="rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 sm:text-sm bg-gray-50"
            >
              <option :value="null">All of Today</option>
              <option v-for="driver in drivers" :key="driver.name" :value="driver.name">
                {{ driver.driver_name }}
              </option>
            </select>
            <button @click="fetchSummary" class="p-2 text-gray-400 hover:text-purple-600 transition-colors" title="Refresh Summary">
              <svg :class="{'animate-spin': loadingSummary}" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Settled Card -->
          <div class="bg-emerald-50 border border-emerald-100 rounded-xl p-5 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-2">
                <div class="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <h4 class="text-emerald-800 font-semibold text-sm uppercase tracking-wider">Settled Records</h4>
              </div>
              <span class="bg-emerald-200 text-emerald-800 text-xs font-bold px-2.5 py-1 rounded-full shadow-sm">
                {{ todaySummary.settled_count }} Records
              </span>
            </div>
            <div class="flex items-baseline space-x-1">
              <span class="text-sm font-medium text-emerald-600">Rs.</span>
              <span class="text-3xl font-extrabold text-emerald-900">
                {{ todaySummary.settled_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
              </span>
            </div>
          </div>
          
          <!-- Unsettled Card -->
          <div class="bg-rose-50 border border-rose-100 rounded-xl p-5 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-2">
                <div class="w-8 h-8 bg-rose-100 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h4 class="text-rose-800 font-semibold text-sm uppercase tracking-wider">Unsettled Records</h4>
              </div>
              <span class="bg-rose-200 text-rose-800 text-xs font-bold px-2.5 py-1 rounded-full shadow-sm">
                {{ todaySummary.unsettled_count }} Records
              </span>
            </div>
            <div class="flex items-baseline space-x-1">
              <span class="text-sm font-medium text-rose-600">Rs.</span>
              <span class="text-3xl font-extrabold text-rose-900">
                {{ todaySummary.unsettled_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- View/Edit Reco Lines Section -->
      <div v-if="selectedCompany && hasTodayRecords && !csvParsed" class="bg-white rounded-xl shadow-lg border-2 border-indigo-500 p-6 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h3 class="text-xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
            View/Edit Reco Lines
          </h3>
          
          <div class="flex items-center gap-2">
            <select 
              v-model="viewRecoDriver" 
              @change="loadRecoLines"
              class="rounded-lg border-2 border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-white px-4 py-2"
            >
              <option :value="null">-- Select a driver --</option>
              <option v-for="driver in drivers" :key="driver.name" :value="driver.driver_name">
                {{ driver.driver_name }}
              </option>
            </select>
            <button 
              @click="loadRecoLines" 
              :disabled="!viewRecoDriver"
              class="p-2 text-indigo-600 hover:text-indigo-800 disabled:text-gray-400 transition-colors" 
              title="Refresh Lines"
            >
              <svg :class="{'animate-spin': loadingRecoLines}" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loadingRecoLines" class="flex justify-center py-8">
          <svg class="animate-spin h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>

        <!-- Reco Lines List -->
        <div v-else-if="recoLinesData" class="space-y-4">
          <!-- Summary Bar -->
          <div class="flex flex-wrap gap-4 text-sm bg-gray-50 rounded-lg p-3">
            <span class="font-medium text-gray-700">Total: {{ formatCurrency(recoLinesData.summary.net_total_amount) }}</span>
            <span class="text-green-600">Settled: {{ recoLinesData.summary.settled_count }}</span>
            <span class="text-amber-600">Pending: {{ recoLinesData.summary.pending_count }}</span>
            <span class="text-indigo-600">Remaining: {{ formatCurrency(recoLinesData.summary.remaining_amount) }}</span>
          </div>

          <!-- Lines List -->
          <div class="border border-gray-200 rounded-lg max-h-80 overflow-y-auto divide-y divide-gray-200">
            <div
              v-for="(line, index) in recoLinesData.lines"
              :key="line.name"
              class="p-3 hover:bg-gray-50 flex items-center gap-3"
            >
              <div class="flex-shrink-0 w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center text-xs font-bold text-gray-600">
                {{ index + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ line.customer_name }}</p>
                  <span v-if="line.updated_later" class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold shadow-sm" style="background: linear-gradient(135deg, #818cf8, #6366f1); color: #ffffff; border: 1px solid #4f46e5;">
                    ✦ Added Later
                  </span>
                </div>
                <p class="text-xs text-gray-500 font-mono">{{ line.customer }}</p>
              </div>
              <div class="text-right flex-shrink-0">
                <p class="text-sm font-bold text-gray-900">{{ formatCurrency(line.net_total_amount) }}</p>
                <p v-if="line.remaining_amount > 0" class="text-xs text-amber-600">Rem: {{ formatCurrency(line.remaining_amount) }}</p>
              </div>
              <span
                :class="[
                  'px-2 py-0.5 rounded-full text-xs font-semibold',
                  line.settled ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'
                ]"
              >
                {{ line.settled ? 'Settled' : 'Pending' }}
              </span>
            </div>
          </div>

          <!-- Add Entry Button -->
          <div class="flex justify-center pt-4 pb-2">
            <button
              @click="openAddEntryDialogForReco"
              class="inline-flex items-center px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2"
              style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); color: #ffffff; border-color: #4f46e5; text-shadow: 0 1px 2px rgba(0,0,0,0.2);"
            >
              <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="filter: drop-shadow(0 1px 1px rgba(0,0,0,0.2));">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"></path>
              </svg>
              <span style="letter-spacing: 0.5px;">Add New Entry</span>
            </button>
          </div>
        </div>

        <!-- No Driver Selected -->
        <div v-else-if="!viewRecoDriver" class="text-center py-8 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
          <p class="font-medium">Select a driver to view their reco lines</p>
        </div>

        <!-- No Data for Driver -->
        <div v-else-if="recoLinesError" class="text-center py-8 text-amber-600">
          <svg class="mx-auto h-12 w-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
          <p class="font-medium">{{ recoLinesError }}</p>
        </div>
      </div>

      <!-- CSV Upload Section (only show when company selected) -->
      <CsvUploadSection
        v-if="selectedCompany && !csvParsed"
        :loading="uploading"
        :company="selectedCompany"
        :company-config="currentCompanyConfig"
        @file-selected="handleFileUpload"
      />

      <!-- File Info with Clear Button -->
      <div v-if="csvParsed" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-10 h-10 bg-purple-100 rounded-lg">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">CSV file loaded successfully</p>
              <p class="text-sm text-gray-500">{{ parsedData.parsed_rows?.length || 0 }} rows • {{ Object.keys(parsedData.grouped_by_loadsheet || {}).length }} load sheets</p>
            </div>
          </div>
          <button
            @click="clearFile"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            Clear File
          </button>
        </div>
      </div>

      <!-- Unmatched Customers Alert -->
      <UnmatchedList
        v-if="csvParsed"
        :unmatched-customers="parsedData.unmatched_customers || []"
        :created-customers="newlyCreatedCustomers"
        :company="selectedCompany"
        :company-config="currentCompanyConfig"
        @customer-created="handleCustomerCreated"
        @all-customers-created="handleAllCustomersCreated"
      />

      <!-- Data Preview Table -->
      <DataPreview
        v-if="csvParsed"
        :parsed-rows="parsedData.parsed_rows || []"
        :grouped-by-loadsheet="parsedData.grouped_by_loadsheet || {}"
      />

      <!-- Driver Assignment Section -->
      <div v-if="csvParsed" class="bg-white rounded-xl shadow-lg border-2 border-blue-500 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-900">
            📋 Step 2: Assign Drivers to Load Sheets
          </h3>
          <span v-if="loadingDrivers" class="text-sm text-blue-600">Loading drivers...</span>
          <span v-else-if="drivers.length === 0" class="text-sm text-red-600">⚠️ No drivers found</span>
          <span v-else class="text-sm text-green-600">✅ {{ drivers.length }} drivers loaded</span>
        </div>

        <!-- Loading State -->
        <div v-if="loadingDrivers" class="flex justify-center py-8">
          <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>

        <!-- No Drivers Warning -->
        <div v-else-if="drivers.length === 0" class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-red-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <div>
              <h4 class="text-sm font-medium text-red-800">No Drivers Found</h4>
              <p class="mt-1 text-sm text-red-700">
                No drivers exist in the system. Please create drivers in Frappe Desk first:
              </p>
              <p class="mt-2 text-sm text-red-700 font-mono">
                Desk → Driver → New Driver
              </p>
            </div>
          </div>
        </div>

        <!-- Driver Assignment - Different for Padmashree vs Riya -->
        
        <!-- Horlicks company: Single driver selector -->
        <template v-else-if="isHorlicksCompany">
          <div class="rounded-xl p-6" :style="getCompanyInfoStyle()">
            <div class="flex items-center gap-3 mb-4">
              <CompanyBadge :company="selectedCompany" :companyConfig="currentCompanyConfig" size="lg" />
              <div>
                <h3 class="text-lg font-bold" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }">Select Driver</h3>
                <p class="text-sm opacity-80" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }">Single driver for entire upload ({{ parsedData.row_count || 0 }} invoice rows, {{ uniqueCustomerCount }} unique customers)</p>
              </div>
            </div>
            
            <!-- Driver info from CSV if available -->
            <div v-if="padmashreeDriverInfo" class="mb-4 p-3 bg-white rounded-lg border border-blue-200">
              <p class="text-sm text-blue-800">
                <span class="font-medium">Driver from CSV:</span> {{ padmashreeDriverInfo.driver_name }}
                <span v-if="padmashreeDriverInfo.driver_mobile" class="ml-2">({{ padmashreeDriverInfo.driver_mobile }})</span>
              </p>
            </div>
            
            <div class="flex items-center gap-4">
              <label class="text-sm font-medium text-blue-800">Assign Driver:</label>
              <select
                v-model="selectedDriverPadmashree"
                class="flex-1 rounded-lg border-2 border-blue-300 px-4 py-2.5 text-sm font-medium bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option :value="null">-- Select Driver --</option>
                <option v-for="driver in drivers" :key="driver.name" :value="driver.driver_name">
                  {{ driver.driver_name }}
                </option>
              </select>
            </div>
            
            <div v-if="selectedDriverPadmashree" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-sm text-green-800 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span><strong>{{ selectedDriverPadmashree }}</strong> will receive <strong>{{ uniqueCustomerCount }}</strong> unique customers (from {{ parsedData.row_count || 0 }} invoices)</span>
              </p>
              <p class="text-sm text-green-700 mt-1">Total Amount: Rs. {{ (parsedData.total_amount || 0).toLocaleString() }}</p>
            </div>
          </div>
        </template>
        
        <!-- Riya: Per-loadsheet driver assignment -->
        <DriverAssignment
          v-else
          :loadsheets="loadsheetList"
          :drivers="drivers"
          :grouped-data="parsedData.grouped_by_loadsheet || {}"
          @update:assignments="driverAssignments = $event"
          @validation-changed="assignmentsValid = $event"
        />
      </div>

      <!-- Create Button -->
      <div v-if="csvParsed" class="space-y-4">
        <!-- Debug Info -->
        <div v-if="!canCreate" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-yellow-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            <div class="flex-1">
              <h3 class="text-sm font-medium text-yellow-800">Cannot Create Records Yet</h3>
              <div class="mt-2 text-sm text-yellow-700 space-y-1">
                <p v-if="!csvParsed">❌ CSV not uploaded</p>
                <p v-if="csvParsed && isPadmashree && !selectedDriverPadmashree">❌ Please select a driver for the upload</p>
                <p v-if="csvParsed && !isPadmashree && !assignmentsValid">❌ Driver assignment incomplete (all load sheets must have a selection, and at least one must have a driver)</p>
                <p v-if="csvParsed && remainingUnmatchedCount > 0">❌ {{ remainingUnmatchedCount }} unmatched customers need to be created</p>
                <p class="font-medium mt-2">Please complete the requirements above to enable the button.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Create Button -->
        <div class="flex justify-center">
          <button
            @click="showConfirmDialog = true"
            :disabled="!canCreate"
            class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Create Payment Reconciliation Records
          </button>
        </div>
      </div>
    </main>

    <!-- Confirmation Dialog -->
    <div v-if="showConfirmDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showConfirmDialog = false"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div 
                class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full sm:mx-0 sm:h-10 sm:w-10"
                :style="{ backgroundColor: currentCompanyConfig?.brand_colors?.bg || '#E6F4FA' }"
              >
                <svg :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Confirm Creation
                </h3>
                <div class="mt-4">
                  <p class="text-sm text-gray-500 mb-4">
                    You are about to create payment reconciliation records for the following:
                  </p>
                  <div class="bg-gray-50 rounded-lg p-4 space-y-2 max-h-64 overflow-y-auto">
                    <!-- Horlicks Mode: Single driver with all customers -->
                    <template v-if="isHorlicksCompany">
                      <div class="flex items-center gap-3 mb-3 pb-3 border-b border-gray-200">
                        <CompanyBadge :company="selectedCompany" :companyConfig="currentCompanyConfig" size="md" />
                        <span class="text-sm font-medium" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }">{{ currentCompanyConfig?.company_name || selectedCompany }}</span>
                      </div>
                      <div class="text-sm space-y-2">
                        <div class="flex justify-between">
                          <span class="text-gray-600">Driver:</span>
                          <span class="font-medium text-gray-900">{{ selectedDriverPadmashree }}</span>
                        </div>
                        <div class="flex justify-between">
                          <span class="text-gray-600">Invoice Rows:</span>
                          <span class="font-medium text-gray-900">{{ parsedData.row_count || 0 }}</span>
                        </div>
                        <div class="flex justify-between">
                          <span class="text-gray-600">Unique Customers:</span>
                          <span class="font-medium text-blue-600">{{ uniqueCustomerCount }}</span>
                        </div>
                        <div class="flex justify-between pt-2 border-t border-gray-200">
                          <span class="text-gray-600">Total Amount:</span>
                          <span class="font-bold text-blue-600">Rs. {{ (parsedData.total_amount || 0).toLocaleString() }}</span>
                        </div>
                        <p v-if="parsedData.row_count !== uniqueCustomerCount" class="text-xs text-gray-500 mt-2 italic">
                          * Multiple invoices for the same customer will be combined into single payment entries
                        </p>
                      </div>
                    </template>
                    
                    <!-- Non-horlicks Mode: Per-loadsheet driver assignment -->
                    <template v-else>
                      <div class="flex items-center gap-3 mb-3 pb-3 border-b border-gray-200">
                        <CompanyBadge :company="selectedCompany" :companyConfig="currentCompanyConfig" size="md" />
                        <span class="text-sm font-medium" :style="{ color: currentCompanyConfig?.brand_colors?.primary || '#F40009' }">{{ currentCompanyConfig?.company_name || selectedCompany }}</span>
                      </div>
                      <div v-for="(loadsheets, driver) in groupedAssignments" :key="driver" class="text-sm">
                        <span class="font-medium text-gray-900">{{ driver }}</span>
                        <span class="text-gray-600"> → {{ loadsheets.join(', ') }}</span>
                      </div>
                      <!-- Show skipped loadsheets if any -->
                      <div v-if="skippedLoadsheets.length > 0" class="text-sm pt-2 border-t border-gray-200 mt-2">
                        <span class="font-medium text-gray-500">⏭️ Skipped (None)</span>
                        <span class="text-gray-400"> → {{ skippedLoadsheets.join(', ') }}</span>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="createRecords"
              :disabled="creating"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              :style="{ backgroundColor: currentCompanyConfig?.brand_colors?.primary || '#0077B6' }"
              :class="isHorlicksCompany 
                ? 'hover:opacity-90 focus:ring-blue-500' 
                : 'bg-red-600 hover:bg-red-700 focus:ring-red-500'"
            >
              <svg v-if="creating" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ creating ? 'Creating...' : 'Confirm & Create' }}
            </button>
            <button
              type="button"
              @click="showConfirmDialog = false"
              :disabled="creating"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              :class="isPadmashree ? 'focus:ring-blue-500' : 'focus:ring-red-500'"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Dialog -->
    <div v-if="showSuccessDialog" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-green-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Success!
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ successMessage }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="closeSuccessDialog"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add New Entry Dialog for Reco -->
    <div v-if="showAddEntryDialogReco" class="fixed inset-0 z-50 flex items-center justify-center p-4" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="fixed inset-0 bg-gray-900 bg-opacity-60 transition-opacity" @click="closeAddEntryDialogReco"></div>

      <div class="relative bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all w-full max-w-lg mx-auto" style="border: 3px solid #4f46e5;">
        <div class="px-5 py-4" style="background: linear-gradient(135deg, #6366f1, #4f46e5);">
          <h3 class="text-xl leading-6 font-bold flex items-center" style="color: #ffffff !important;">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ffffff;">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span style="color: #ffffff !important;">{{ addEntryStepReco === 'input' ? 'Add New Entry' : 'Confirm New Entry' }}</span>
          </h3>
        </div>
        
        <div class="bg-white px-5 pt-5 pb-4">
          <!-- Step 1: Input -->
          <div v-if="addEntryStepReco === 'input'" class="space-y-5">
            <!-- Customer Search/Select -->
            <div>
              <label class="block text-sm font-bold mb-2" style="color: #1f2937 !important;">Customer</label>
              <div class="relative">
                <input
                  v-model="customerSearchQueryReco"
                  @input="filterCustomersReco"
                  @focus="showCustomerDropdownReco = true"
                  type="text"
                  placeholder="Search customer by name or code..."
                  class="block w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base"
                />
                <!-- Customer Dropdown -->
                <div v-if="showCustomerDropdownReco && filteredCustomersListReco.length > 0" 
                     class="absolute z-10 mt-1 w-full bg-white border-2 border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                  <div
                    v-for="customer in filteredCustomersListReco"
                    :key="customer.name"
                    @click="selectCustomerReco(customer)"
                    class="px-4 py-2.5 hover:bg-indigo-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                  >
                    <p class="font-medium text-gray-900">{{ customer.customer_name }}</p>
                    <p class="text-xs text-gray-500 font-mono">{{ customer.name }}</p>
                  </div>
                </div>
              </div>
              <!-- Selected Customer Display -->
              <div v-if="selectedCustomerForAddReco" class="mt-2 p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                <p class="text-sm font-semibold text-indigo-900">{{ selectedCustomerForAddReco.customer_name }}</p>
                <p class="text-xs text-indigo-700 font-mono">{{ selectedCustomerForAddReco.name }}</p>
              </div>
            </div>

            <!-- Amount Input -->
            <div>
              <label class="block text-sm font-bold mb-2" style="color: #1f2937 !important;">Amount</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 font-semibold" style="color: #374151 !important;">NPR</span>
                <input
                  v-model.number="newEntryAmountReco"
                  type="number"
                  inputmode="decimal"
                  min="0"
                  step="0.01"
                  placeholder="0"
                  class="block w-full pl-14 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base font-medium"
                />
              </div>
            </div>

            <!-- Info if customer exists in reco -->
            <div v-if="selectedCustomerForAddReco && existingCustomerInRecoForAdd" class="p-3 bg-amber-50 border border-amber-300 rounded-lg">
              <p class="text-sm text-amber-800">
                <strong>Note:</strong> This customer already exists in the reco. 
                Amount will be <strong>added</strong> to their current total ({{ formatCurrency(existingCustomerInRecoForAdd.initial_total_amount) }}).
              </p>
            </div>
          </div>

            <!-- Step 2: Confirmation -->
            <div v-else-if="addEntryStepReco === 'confirm'" class="space-y-4">
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
                  <span class="text-gray-600 font-medium">Driver:</span>
                  <span class="font-bold text-gray-900">{{ viewRecoDriver }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 font-medium">Customer:</span>
                  <span class="font-bold text-gray-900">{{ selectedCustomerForAddReco?.customer_name }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 font-medium">Customer Code:</span>
                  <span class="font-mono text-gray-700">{{ selectedCustomerForAddReco?.name }}</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-gray-300">
                  <span class="text-gray-600 font-medium">Amount to Add:</span>
                  <span class="font-bold text-xl text-indigo-600">{{ formatCurrency(newEntryAmountReco) }}</span>
                </div>
                <div v-if="existingCustomerInRecoForAdd" class="flex justify-between items-center text-sm">
                  <span class="text-gray-500">Current Amount:</span>
                  <span class="text-gray-600">{{ formatCurrency(existingCustomerInRecoForAdd.initial_total_amount) }}</span>
                </div>
                <div v-if="existingCustomerInRecoForAdd" class="flex justify-between items-center text-sm">
                  <span class="text-gray-500">New Total:</span>
                  <span class="font-semibold text-green-600">{{ formatCurrency(existingCustomerInRecoForAdd.initial_total_amount + newEntryAmountReco) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-50 px-4 py-4 sm:px-6">
            <div class="flex flex-row justify-end gap-3">
              <button
                type="button"
                @click="closeAddEntryDialogReco"
                :disabled="addingEntryReco"
                class="inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-5 py-2.5 bg-white text-base font-bold text-gray-700 hover:bg-gray-100 transition-all"
              >
                Cancel
              </button>
              <button
                v-if="addEntryStepReco === 'confirm'"
                type="button"
                @click="addEntryStepReco = 'input'"
                :disabled="addingEntryReco"
                class="inline-flex justify-center rounded-lg border-2 border-gray-300 shadow-sm px-5 py-2.5 bg-white text-base font-bold text-gray-700 hover:bg-gray-100 transition-all"
              >
                Back
              </button>
              <button
                v-if="addEntryStepReco === 'input'"
                type="button"
                @click="proceedToConfirmReco"
                :disabled="!canProceedToConfirmReco"
                class="inline-flex justify-center items-center rounded-lg shadow-sm px-5 py-2.5 text-base font-bold text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                style="background-color: #4f46e5 !important; border: 2px solid #4338ca !important;"
              >
                Continue
                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
              <button
                v-if="addEntryStepReco === 'confirm'"
                type="button"
                @click="submitNewEntryReco"
                :disabled="addingEntryReco"
                class="inline-flex justify-center items-center rounded-lg shadow-sm px-5 py-2.5 text-base font-bold text-white transition-all disabled:opacity-50"
                style="background-color: #16a34a !important; border: 2px solid #15803d !important;"
              >
                <svg v-if="addingEntryReco" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ addingEntryReco ? 'Adding...' : 'Confirm & Add' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { session } from '../../shared/data/session'
import { call } from 'frappe-ui'
import CsvUploadSection from './components/CsvUploadSection.vue'
import DataPreview from './components/DataPreview.vue'
import DriverAssignment from './components/DriverAssignment.vue'
import UnmatchedList from './components/UnmatchedList.vue'
import CompanyBadge from '../../shared/components/CompanyBadge.vue'

// Company Selection State
const selectedCompany = ref(null)
const companiesList = ref([])

// Get current company config from companiesList
const currentCompanyConfig = computed(() => {
  if (!selectedCompany.value) return null
  return companiesList.value.find(c => c.name === selectedCompany.value) || null
})

// Check if selected company is horlicks-based (replaces isPadmashree)
const isHorlicksCompany = computed(() => {
  return currentCompanyConfig.value?.main_product === 'horlicks' || currentCompanyConfig.value?.is_horlicks
})

// Backward compatibility alias
const isPadmashree = isHorlicksCompany

const companyDescription = computed(() => {
  if (isHorlicksCompany.value) {
    const product = currentCompanyConfig.value?.main_product || 'horlicks'
    return `${capitalizeFirst(product)} customers only`
  }
  if (selectedCompany.value) return 'All customers except Horlicks'
  return ''
})

// Helper function to capitalize first letter
const capitalizeFirst = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// Get company info box style based on brand colors
const getCompanyInfoStyle = () => {
  const colors = currentCompanyConfig.value?.brand_colors
  if (!colors) {
    return isHorlicksCompany.value 
      ? { backgroundColor: '#E6F4FA', borderColor: '#0077B6' }
      : { backgroundColor: '#FEE6E6', borderColor: '#F40009' }
  }
  return { backgroundColor: colors.bg, borderColor: colors.primary }
}

// Padmashree-specific state
const selectedDriverPadmashree = ref(null)
const padmashreeDriverInfo = ref(null)

// State
const uploading = ref(false)
const csvParsed = ref(false)
const parsedData = ref({})
const drivers = ref([])
const loadingDrivers = ref(false)
const driverAssignments = ref({})
const assignmentsValid = ref(false)
const showConfirmDialog = ref(false)
const creating = ref(false)
const showSuccessDialog = ref(false)
const successMessage = ref('')

// View/Edit Reco Lines State
const viewRecoDriver = ref(null)
const loadingRecoLines = ref(false)
const recoLinesData = ref(null)
const recoLinesError = ref('')

// Add Entry Dialog State (for Reco)
const showAddEntryDialogReco = ref(false)
const addEntryStepReco = ref('input')
const allCustomersReco = ref([])
const customerSearchQueryReco = ref('')
const filteredCustomersListReco = ref([])
const showCustomerDropdownReco = ref(false)
const selectedCustomerForAddReco = ref(null)
const newEntryAmountReco = ref(0)
const addingEntryReco = ref(false)
const newlyCreatedCustomers = ref([])  // Track customers created during this session

// Today's Summary State
const todaySummary = ref({
  settled_count: 0,
  settled_amount: 0,
  unsettled_count: 0,
  unsettled_amount: 0
})
const loadingSummary = ref(false)
const summaryDriver = ref(null)
const anyRecordsFoundToday = ref(false)

// Computed
const loadsheetList = computed(() => {
  return Object.keys(parsedData.value.grouped_by_loadsheet || {})
})

// Count remaining unmatched customers (original list minus newly created)
const remainingUnmatchedCount = computed(() => {
  const originalUnmatched = parsedData.value.unmatched_customers || []
  const createdCodes = new Set(newlyCreatedCustomers.value.map(c => c.outlet_code))
  return originalUnmatched.filter(c => !createdCodes.has(c.outlet_code)).length
})

const canCreate = computed(() => {
  if (!csvParsed.value) return false
  if (remainingUnmatchedCount.value > 0) return false
  
  if (isPadmashree.value) {
    // Padmashree: Only need a driver selected (single driver for all)
    return !!selectedDriverPadmashree.value
  } else {
    // Riya: Need all loadsheets assigned
    return assignmentsValid.value
  }
})

// Count unique customers from parsed rows (for Padmashree)
const uniqueCustomerCount = computed(() => {
  if (!parsedData.value?.parsed_rows) return 0
  const uniqueCustomers = new Set(parsedData.value.parsed_rows.map(r => r.outlet_code))
  return uniqueCustomers.size
})

// Group assignments by driver (excluding __none__ assignments)
const groupedAssignments = computed(() => {
  const grouped = {}
  for (const [loadsheet, driver] of Object.entries(driverAssignments.value)) {
    if (driver && driver !== '__none__') {
      if (!grouped[driver]) {
        grouped[driver] = []
      }
      grouped[driver].push(loadsheet)
    }
  }
  return grouped
})

// Get loadsheets that are set to skip (none)
const skippedLoadsheets = computed(() => {
  return Object.entries(driverAssignments.value)
    .filter(([_, driver]) => driver === '__none__')
    .map(([loadsheet, _]) => loadsheet)
})

const hasTodayRecords = computed(() => {
  return anyRecordsFoundToday.value || todaySummary.value.settled_count > 0 || todaySummary.value.unsettled_count > 0
})

// Check if selected customer already exists in reco
const existingCustomerInRecoForAdd = computed(() => {
  if (!selectedCustomerForAddReco.value || !recoLinesData.value?.lines) return null
  return recoLinesData.value.lines.find(line => line.customer === selectedCustomerForAddReco.value.name)
})

// Can proceed to confirmation
const canProceedToConfirmReco = computed(() => {
  return selectedCustomerForAddReco.value && newEntryAmountReco.value > 0
})

// Lifecycle
onMounted(async () => {
  loadDrivers()
  await loadCompanies()
})

// Extract companies array from API response (handles Frappe wrapper and all shapes)
function extractCompaniesList(raw) {
  if (raw == null) return []
  if (Array.isArray(raw)) return raw
  // Frappe HTTP body: { message: { success, data, message? } }
  const inner = raw.message
  if (inner != null && typeof inner === 'object') {
    if (Array.isArray(inner.data)) return inner.data
    if (Array.isArray(inner)) return inner
  }
  // Direct return: { success, data, message? }
  if (Array.isArray(raw.data)) return raw.data
  return []
}

// Fetch companies list
const loadCompanies = async () => {
  try {
    const raw = await call('custom_erp.api.payment_reco.get_companies_list')
    companiesList.value = extractCompaniesList(raw)
  } catch (error) {
    console.error('Failed to load companies:', error)
    companiesList.value = []
  }
}

// Watch for company changes
watch(selectedCompany, () => {
  if (selectedCompany.value) {
    fetchSummary()
  }
})

// Methods
const handleCompanyChange = () => {
  // Clear file data when company changes
  clearFile()
  // Reset Padmashree-specific state
  selectedDriverPadmashree.value = null
  padmashreeDriverInfo.value = null
  // Clear cached customers (will be reloaded with company filter when needed)
  allCustomersReco.value = []
  // Fetch summary for new company
  if (selectedCompany.value) {
    fetchSummary()
  }
}

const fetchSummary = async () => {
  if (!selectedCompany.value) return
  
  loadingSummary.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.get_today_reco_summary', {
      driver: summaryDriver.value,
      company: selectedCompany.value
    })
    if (response.success) {
      todaySummary.value = response.data
      
      // If we found any records (either globally or for this driver), 
      // mark that there is data for today so the UI stays visible
      if (todaySummary.value.settled_count > 0 || todaySummary.value.unsettled_count > 0) {
        anyRecordsFoundToday.value = true
      }
    }
  } catch (error) {
    console.error('Error fetching summary:', error)
  } finally {
    loadingSummary.value = false
  }
}

const handleFileUpload = async (csvContent) => {
  uploading.value = true
  try {
    // Use different parsing based on company
    const apiMethod = isPadmashree.value 
      ? 'custom_erp.api.payment_reco.parse_and_validate_csv_padmashree'
      : 'custom_erp.api.payment_reco.parse_and_validate_csv'
    
    const response = await call(apiMethod, {
      csv_content: csvContent
    })

    if (response.success) {
      parsedData.value = response.data
      csvParsed.value = true
      
      // For Padmashree, extract driver info from CSV
      if (isPadmashree.value && response.data.driver_info) {
        padmashreeDriverInfo.value = response.data.driver_info
      }
      
      // Drivers are already loaded in onMounted, but we can refresh just in case
      await loadDrivers()
    } else {
      alert('Error parsing CSV: ' + response.message)
    }
  } catch (error) {
    console.error('Error uploading CSV:', error)
    alert('Error uploading CSV: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const loadDrivers = async () => {
  loadingDrivers.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.get_drivers_list')
    if (response.success) {
      drivers.value = response.data
    } else {
      console.error('Error loading drivers:', response.message)
    }
  } catch (error) {
    console.error('Error loading drivers:', error)
  } finally {
    loadingDrivers.value = false
  }
}

const clearFile = () => {
  csvParsed.value = false
  parsedData.value = {}
  driverAssignments.value = {}
  assignmentsValid.value = false
  newlyCreatedCustomers.value = []
  // Reset Padmashree-specific state
  selectedDriverPadmashree.value = null
  padmashreeDriverInfo.value = null
}

const createRecords = async () => {
  creating.value = true
  try {
    let response
    
    if (isHorlicksCompany.value) {
      // Horlicks company: Single driver, no loadsheet grouping
      response = await call('custom_erp.api.payment_reco.create_payment_recos_horlicks', {
        driver: selectedDriverPadmashree.value,
        csv_data: JSON.stringify(parsedData.value.parsed_rows),
        company: selectedCompany.value
      })
    } else {
      // Non-horlicks: Driver per loadsheet
      response = await call('custom_erp.api.payment_reco.create_payment_recos', {
        driver_assignments: JSON.stringify(groupedAssignments.value),
        csv_data: JSON.stringify(parsedData.value.grouped_by_loadsheet),
        company: selectedCompany.value
      })
    }

    if (response.success) {
      successMessage.value = response.message
      showConfirmDialog.value = false
      showSuccessDialog.value = true
      // Refresh summary after successful creation
      fetchSummary()
    } else {
      alert('Error creating records: ' + response.message)
    }
  } catch (error) {
    console.error('Error creating records:', error)
    alert('Error creating records: ' + error.message)
  } finally {
    creating.value = false
  }
}

const closeSuccessDialog = () => {
  showSuccessDialog.value = false
  clearFile()
}

// Handle when a single customer is created
const handleCustomerCreated = (customer) => {
  // Add to newly created customers list (this persists throughout session)
  if (!newlyCreatedCustomers.value.some(c => c.outlet_code === customer.outlet_code)) {
    newlyCreatedCustomers.value.push({
      outlet_code: customer.outlet_code,
      outlet_name: customer.outlet_name,
      name: customer.name
    })
  }
  
  // Update customer_exists flag in parsed_rows and grouped_by_loadsheet
  if (parsedData.value.parsed_rows) {
    parsedData.value.parsed_rows.forEach(row => {
      if (row.outlet_code === customer.outlet_code) {
        row.customer_exists = true
      }
    })
  }
  
  if (parsedData.value.grouped_by_loadsheet) {
    Object.values(parsedData.value.grouped_by_loadsheet).forEach(rows => {
      rows.forEach(row => {
        if (row.outlet_code === customer.outlet_code) {
          row.customer_exists = true
        }
      })
    })
  }
}

// Handle when all customers are created - just a notification, state is already managed
const handleAllCustomersCreated = () => {
  // All customers created - canCreate will now be true via computed property
  console.log('All unmatched customers have been created')
}

// --- Reco Lines Methods ---

const loadRecoLines = async () => {
  if (!viewRecoDriver.value) {
    recoLinesData.value = null
    recoLinesError.value = ''
    return
  }
  
  loadingRecoLines.value = true
  recoLinesError.value = ''
  try {
    const response = await call('custom_erp.api.payment_reco.get_reco_lines_for_driver', {
      driver_name: viewRecoDriver.value,
      company: selectedCompany.value
    })
    
    if (response.success) {
      recoLinesData.value = response.data
      recoLinesError.value = ''
    } else {
      recoLinesData.value = null
      recoLinesError.value = response.message || 'No active reco found for this driver'
    }
  } catch (error) {
    console.error('Error loading reco lines:', error)
    recoLinesData.value = null
    recoLinesError.value = 'Error loading data'
  } finally {
    loadingRecoLines.value = false
  }
}

// --- Add Entry Dialog Methods (for Reco) ---

const openAddEntryDialogForReco = async () => {
  showAddEntryDialogReco.value = true
  addEntryStepReco.value = 'input'
  customerSearchQueryReco.value = ''
  selectedCustomerForAddReco.value = null
  newEntryAmountReco.value = 0
  filteredCustomersListReco.value = []
  showCustomerDropdownReco.value = false
  
  // Load customers filtered by company
  // Padmashree: Only Horlicks customers
  // Riya: All customers except Horlicks
  try {
    const response = await call('custom_erp.api.payment_reco.get_customers_for_company', {
      company: selectedCompany.value
    })
    if (response.success) {
      allCustomersReco.value = response.data
    }
  } catch (error) {
    console.error('Error loading customers:', error)
  }
}

const closeAddEntryDialogReco = () => {
  showAddEntryDialogReco.value = false
  addEntryStepReco.value = 'input'
  customerSearchQueryReco.value = ''
  selectedCustomerForAddReco.value = null
  newEntryAmountReco.value = 0
  filteredCustomersListReco.value = []
  showCustomerDropdownReco.value = false
}

const filterCustomersReco = () => {
  if (!customerSearchQueryReco.value || customerSearchQueryReco.value.length < 1) {
    filteredCustomersListReco.value = []
    showCustomerDropdownReco.value = false
    return
  }
  
  const query = customerSearchQueryReco.value.toLowerCase()
  filteredCustomersListReco.value = allCustomersReco.value
    .filter(c => 
      c.customer_name.toLowerCase().includes(query) || 
      c.name.toLowerCase().includes(query)
    )
    .slice(0, 20) // Limit results
  showCustomerDropdownReco.value = filteredCustomersListReco.value.length > 0
}

const selectCustomerReco = (customer) => {
  selectedCustomerForAddReco.value = customer
  customerSearchQueryReco.value = customer.customer_name
  showCustomerDropdownReco.value = false
  filteredCustomersListReco.value = []
}

const proceedToConfirmReco = () => {
  if (!canProceedToConfirmReco.value) return
  addEntryStepReco.value = 'confirm'
}

const submitNewEntryReco = async () => {
  if (!selectedCustomerForAddReco.value || newEntryAmountReco.value <= 0 || !recoLinesData.value?.reco_name) {
    return
  }
  
  addingEntryReco.value = true
  try {
    const response = await call('custom_erp.api.payment_reco.add_new_reco_entry', {
      reco_name: recoLinesData.value.reco_name,
      customer: selectedCustomerForAddReco.value.name,
      amount: newEntryAmountReco.value
    })
    
    if (response.success) {
      // Close dialog and reload data
      closeAddEntryDialogReco()
      await loadRecoLines()
      await fetchSummary()
      
      alert(response.message)
    } else {
      alert('Error: ' + response.message)
    }
  } catch (error) {
    console.error('Error adding new entry:', error)
    alert('Failed to add entry. Please try again.')
  } finally {
    addingEntryReco.value = false
  }
}

// Format currency helper
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 0
  }).format(amount || 0)
}
</script>

