<template>
  <div class="min-h-screen" style="background: linear-gradient(to bottom right, #ecfeff, #ffffff, #f0fdfa);">
    <!-- Header -->
    <header class="sticky top-0 z-20" style="background-color: #ffffff; border-bottom: 1px solid #e5e7eb; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4 sm:py-6">
          <div class="flex items-center space-x-3 sm:space-x-4">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 rounded-lg" style="background-color: #0891b2;">
              <svg class="w-5 h-5 sm:w-6 sm:h-6" style="color: #ffffff;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl sm:text-2xl font-bold" style="color: #111827;">Daily Transactions</h1>
              <p class="text-xs sm:text-sm" style="color: #4b5563;">Payment Reconciliation Dashboard</p>
            </div>
          </div>
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 rounded-md shadow-sm text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
            style="background-color: #ffffff; color: #374151; border: 1px solid #d1d5db;"
          >
            <svg class="w-4 h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8">
      <!-- Date & Company Selection Card -->
      <section class="rounded-xl shadow-lg p-6 sm:p-8" style="background-color: #ffffff; border: 1px solid #e5e7eb;">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 sm:gap-6">
          <!-- Today Info -->
          <div class="space-y-2">
            <div class="text-xs sm:text-sm" style="color: #6b7280;">Today (BS)</div>
            <div class="text-xl sm:text-2xl font-bold" style="color: #111827;">
              {{ bsToday }}
              <span class="text-sm font-normal text-gray-500 ml-1">({{ adToday }})</span>
            </div>
            <div class="text-sm sm:text-base" style="color: #374151;">
              <span class="font-medium">{{ session.user }}</span>
            </div>
          </div>
          
          <!-- Company Filter -->
          <div class="space-y-2">
            <div class="text-xs sm:text-sm uppercase tracking-wide" style="color: #4b5563;">Company</div>
            <select
              v-model="selectedCompany"
              @change="handleCompanyChange"
              class="select-dropdown min-w-[200px]"
              :style="getCompanySelectStyle()"
            >
              <option v-for="company in companyOptions" :key="company.value" :value="company.value">
                {{ company.label }}
              </option>
            </select>
            <!-- Company Badge Display -->
            <div v-if="selectedCompany" class="flex items-center gap-2 mt-1">
              <CompanyBadge :company="selectedCompany" size="md" />
              <span class="text-xs text-gray-600">{{ selectedCompany === 'PadmaShree Trade Link' ? 'Horlicks' : 'Multi-Brand' }}</span>
            </div>
          </div>
          
          <!-- Date Picker -->
          <div class="flex-1 sm:text-center space-y-2 lg:max-w-md lg:mx-auto">
            <div class="text-xs sm:text-sm uppercase tracking-wide mb-2" style="color: #4b5563;">Select Date</div>
            <NepaliDatePicker
              v-model="selectedDate"
              @update:modelValue="handleDateChange"
              placeholder="Select a date (BS)"
              :show-english-date="true"
            />
            <div v-if="selectedDateBs" class="text-sm text-gray-600 mt-2">
              Selected: <span class="font-semibold">{{ selectedDateBs }}</span>
              <span class="text-xs text-gray-500 ml-1">({{ selectedDate }})</span>
            </div>
            <button
              v-if="selectedDate"
              @click="clearDateFilter"
              class="mt-2 text-xs text-cyan-600 hover:text-cyan-800 underline"
            >
              Clear Date Filter (Show Today)
            </button>
          </div>
          
          <!-- Refresh Button -->
          <div class="flex flex-col gap-2">
            <button
              @click="refreshAll"
              :disabled="loading"
              class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 active:scale-95 transition"
              style="background-color: #0891b2; color: #ffffff;"
            >
              <svg v-if="loading" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </section>

      <!-- Summary Cards -->
      <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <!-- Net Total -->
        <div class="rounded-xl shadow-md p-4 sm:p-6" style="background-color: #ffffff; border: 1px solid #e5e7eb;">
          <div class="text-xs sm:text-sm mb-1" style="color: #6b7280;">Net Total</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #111827;">{{ formatAmount(summary.net_total_amount) }}</div>
          <div class="text-xs mt-1" style="color: #6b7280;">{{ summary.total_records || 0 }} records</div>
        </div>
        
        <!-- Cash -->
        <div @click="navigateToSummaryCategory('cash')" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #f0fdf4; border: 1px solid #bbf7d0;">
          <div class="text-xs sm:text-sm mb-1" style="color: #15803d;">Cash</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #16a34a;">{{ formatAmount(summary.cash_amount) }}</div>
        </div>
        
        <!-- QR -->
        <div @click="navigateToSummaryCategory('qr')" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #eff6ff; border: 1px solid #bfdbfe;">
          <div class="text-xs sm:text-sm mb-1" style="color: #1d4ed8;">QR Payment</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #2563eb;">{{ formatAmount(summary.qr_amount) }}</div>
        </div>
        
        <!-- Cheque -->
        <div @click="navigateToSummaryCategory('cheque')" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #faf5ff; border: 1px solid #e9d5ff;">
          <div class="text-xs sm:text-sm mb-1" style="color: #7e22ce;">Cheque</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #9333ea;">{{ formatAmount(summary.cheque_amount) }}</div>
        </div>
        
        <!-- Credit -->
        <div @click="navigateToSummaryCategory('credit')" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #fef2f2; border: 1px solid #fecaca;">
          <div class="text-xs sm:text-sm mb-1" style="color: #b91c1c;">Credit</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #dc2626;">{{ formatAmount(summary.credit_amount) }}</div>
        </div>
        
        <!-- Return -->
        <div @click="navigateToSummaryCategory('return')" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #fff7ed; border: 1px solid #fed7aa;">
          <div class="text-xs sm:text-sm mb-1" style="color: #c2410c;">Return</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #ea580c;">{{ formatAmount(summary.return_amount) }}</div>
        </div>
        
        <!-- Expense -->
        <div class="rounded-xl shadow-md p-4 sm:p-6" style="background-color: #f3f4f6; border: 1px solid #d1d5db;">
          <div class="text-xs sm:text-sm mb-1" style="color: #374151;">Expense</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #4b5563;">{{ formatAmount(summary.expense_amount) }}</div>
        </div>
        
        <!-- Remaining -->
        <div @click="navigateToSummaryCategory('', true)" class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95" style="background-color: #ecfeff; border: 2px solid #22d3ee;">
          <div class="text-xs sm:text-sm mb-1" style="color: #0e7490;">Remaining</div>
          <div class="text-lg sm:text-2xl font-bold" style="color: #0891b2;">{{ formatAmount(summary.remaining_amount) }}</div>
        </div>
        <!-- Cheque Settlement Info (Added by AI) -->
        <div 
          @click="selectedViewMode = 'cheques'"
          class="rounded-xl shadow-md p-4 sm:p-6 cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1" 
          style="background-color: #fff1f2; border: 1px solid #fecdd3;"
        >
          <div class="flex items-center justify-between mb-3">
             <div class="text-xs sm:text-sm font-semibold" style="color: #be123c;">Cheque Settlement</div>
             <svg class="w-4 h-4 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </div>
          
          <!-- Total Pending -->
          <div class="flex justify-between items-baseline mb-2">
            <div class="text-xs text-gray-500">Pending ({{ summary.cheque_settlement_info?.total_pending_count || 0 }})</div>
            <div class="font-bold text-lg" style="color: #be123c;">
              {{ formatAmount(summary.cheque_settlement_info?.total_pending_amount || 0) }}
            </div>
          </div>
          
          <!-- Due Today -->
          <div class="pt-2 border-t border-rose-200 mt-2">
            <div class="flex justify-between items-center mb-1">
              <div class="text-xs text-rose-700 font-medium">Due Today / Late</div>
              <div class="text-xs font-bold text-rose-700 bg-rose-100 px-2 py-0.5 rounded-full">{{ summary.cheque_settlement_info?.due_today_count || 0 }}</div>
            </div>
            <div class="text-right text-base font-bold text-rose-800">
              {{ formatAmount(summary.cheque_settlement_info?.due_today_amount || 0) }}
            </div>
          </div>
        </div>
      </section>

      <!-- View Mode Switcher and Filters -->
      <section class="rounded-xl shadow-lg p-6 sm:p-8" style="background-color: #ffffff; border: 1px solid #e5e7eb;">
        <div class="space-y-4">
          <!-- View Mode Switcher -->
          <div>
            <label class="block text-sm font-semibold mb-3" style="color: #374151;">View Mode</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="mode in viewModes"
                :key="mode.value"
                @click="selectedViewMode = mode.value"
                :style="selectedViewMode === mode.value 
                  ? 'background-color: #0891b2; color: #ffffff; border: 2px solid #0891b2; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'
                  : 'background-color: #ffffff; color: #1f2937; border: 2px solid #d1d5db;'"
                class="px-4 py-2.5 rounded-lg text-sm font-semibold transition-all"
              >
                {{ mode.label }}
              </button>
            </div>
          </div>

          <!-- Filters -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
            <!-- Driver/User Filter -->
            <div>
              <label class="block text-sm font-semibold mb-2" style="color: #374151;">Filter by Driver</label>
              <select
                v-model="selectedDriver"
                @change="applyFilters"
                class="select-dropdown"
                style="color: #111827; background-color: #ffffff;"
              >
                <option value="" style="color: #111827;">All Drivers</option>
                <option v-for="driver in driverOptions" :key="driver.value" :value="driver.value" style="color: #111827;">
                  {{ driver.label }}
                </option>
              </select>
            </div>

            <!-- Customer Filter -->
            <div>
              <label class="block text-sm font-semibold mb-2" style="color: #374151;">Filter by Customer</label>
              <select
                v-model="selectedCustomer"
                @change="applyFilters"
                class="select-dropdown"
                style="color: #111827; background-color: #ffffff;"
              >
                <option value="" style="color: #111827;">All Customers</option>
                <option v-for="customer in customerOptions" :key="customer.value" :value="customer.value" style="color: #111827;">
                  {{ customer.label }}
                </option>
              </select>
            </div>
            
            <!-- Category Filter -->
            <div>
              <label class="block text-sm font-semibold mb-2" style="color: #374151;">Filter by Category</label>
              <select
                v-model="selectedCategory"
                @change="applyFilters"
                class="select-dropdown"
                style="color: #111827; background-color: #ffffff;"
              >
                <option value="" style="color: #111827;">All Categories</option>
                <option value="cash" style="color: #111827;">Cash</option>
                <option value="qr" style="color: #111827;">QR Payment</option>
                <option value="cheque" style="color: #111827;">Cheque</option>
                <option value="credit" style="color: #111827;">Credit</option>
                <option value="return" style="color: #111827;">Return</option>
              </select>
            </div>

            <!-- Settled Filter -->
            <div>
              <label class="block text-sm font-semibold mb-2" style="color: #374151;">Status</label>
              <select
                v-model="selectedStatus"
                @change="applyFilters"
                class="select-dropdown"
                style="color: #111827; background-color: #ffffff;"
              >
                <option value="" style="color: #111827;">All Status</option>
                <option value="settled" style="color: #111827;">Settled</option>
                <option value="pending" style="color: #111827;">Pending</option>
              </select>
            </div>
          </div>

          <!-- Active Filters Display -->
          <div v-if="hasActiveFilters" class="pt-2 border-t border-gray-200">
            <div class="flex items-center justify-between mb-2">
              <div class="text-xs font-medium text-gray-600">Active Filters:</div>
              <button 
                @click="clearAllFilters" 
                class="text-xs font-medium text-red-600 hover:text-red-800 hover:underline transition-colors flex items-center gap-1"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Clear All
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-if="selectedCompany"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium"
                :class="selectedCompany === 'PadmaShree Trade Link' ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-800'"
              >
                <CompanyBadge :company="selectedCompany" size="sm" class="mr-1" />
                Company: {{ selectedCompany === 'PadmaShree Trade Link' ? 'PadmaShree' : 'Riya' }}
                <button @click="clearCompanyFilter" class="ml-2 hover:opacity-70">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedDriver"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-cyan-100 text-cyan-800"
              >
                Driver: {{ getDriverLabel(selectedDriver) }}
                <button @click="clearDriverFilter" class="ml-2 hover:text-cyan-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedCustomer"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                Customer: {{ getCustomerLabel(selectedCustomer) }}
                <button @click="clearCustomerFilter" class="ml-2 hover:text-green-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedCategory"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
              >
                Category: {{ selectedCategory }}
                <button @click="clearCategoryFilter" class="ml-2 hover:text-purple-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedStatus"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800"
              >
                Status: {{ selectedStatus }}
                <button @click="clearStatusFilter" class="ml-2 hover:text-amber-600">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Data Display Section -->
      <section class="rounded-xl shadow-lg p-6 sm:p-8" style="background-color: #ffffff; border: 1px solid #e5e7eb;">
        <!-- Loading State -->
        <div v-if="loadingData" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 mx-auto" style="border-bottom: 2px solid #0891b2;"></div>
          <p class="mt-4" style="color: #4b5563;">Loading data...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="!hasData" class="text-center py-12">
          <svg class="mx-auto h-12 w-12" style="color: #9ca3af;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="mt-4" style="color: #4b5563;">No data found{{ selectedDate ? ` for ${selectedDateBs}` : ' for today' }}.</p>
        </div>

        <!-- Driver-wise View -->
        <div v-else-if="selectedViewMode === 'driver'">
          <h3 class="text-lg font-semibold mb-4" style="color: #111827;">Collections by Driver</h3>
          <div class="space-y-4">
            <div
              v-for="(item, index) in driverData"
              :key="item.driver"
              class="driver-card rounded-xl overflow-hidden transition-all"
              style="background-color: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
            >
              <!-- Driver Header -->
              <div class="p-4" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-bottom: 1px solid #e5e7eb;">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="relative">
                      <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm" 
                           :style="{ backgroundColor: getDriverColor(index) }">
                        {{ getInitials(item.driver_name) }}
                      </div>
                      <!-- Company Badge - shown when "All Companies" is selected -->
                      <CompanyBadge 
                        v-if="!selectedCompany && item.company"
                        :company="item.company" 
                        size="sm" 
                        class="absolute -top-1 -right-1"
                      />
                    </div>
                    <div>
                      <div class="flex items-center gap-2">
                        <span class="font-semibold text-base" style="color: #111827;">{{ item.driver_name }}</span>
                        <CompanyBadge v-if="selectedCompany" :company="selectedCompany" size="sm" />
                      </div>
                      <div class="text-xs" style="color: #6b7280;">{{ item.line_count }} customer{{ item.line_count !== 1 ? 's' : '' }}</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-xs" style="color: #6b7280;">Total Collection</div>
                    <div class="text-lg font-bold" style="color: #111827;">{{ formatAmount(item.net_total_amount) }}</div>
                  </div>
                </div>
                <!-- Additional Info Row -->
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-gray-200/50">
                  <div class="flex items-center gap-4 text-xs">
                    <div>
                      <span style="color: #6b7280;">Initial: </span>
                      <span class="font-medium" style="color: #374151;">{{ formatAmountShort(item.initial_total_amount) }}</span>
                    </div>
                    <div v-if="item.additional_amount">
                      <span style="color: #059669;">+Add: </span>
                      <span class="font-medium" style="color: #059669;">{{ formatAmountShort(item.additional_amount) }}</span>
                    </div>
                  </div>
                  <div class="text-xs">
                    <span style="color: #6b7280;">Net: </span>
                    <span class="font-semibold" style="color: #0891b2;">{{ formatAmountShort(item.net_total_amount) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Payment Categories Grid - Mobile First -->
              <div class="p-4">
                <!-- Row 1: Cash & QR (Primary collections) -->
                <div class="grid grid-cols-2 gap-3 mb-3">
                  <div @click="navigateToDriverCategory(item, 'cash')" class="category-pill cursor-pointer hover:shadow-md transition-all active:scale-95" style="background-color: #dcfce7; border: 1px solid #86efac; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #16a34a;"></div>
                      <span class="text-xs font-medium" style="color: #15803d;">Cash</span>
                    </div>
                    <div class="text-base font-bold" style="color: #16a34a;">{{ formatAmount(item.cash_amount) }}</div>
                  </div>
                  <div @click="navigateToDriverCategory(item, 'qr')" class="category-pill cursor-pointer hover:shadow-md transition-all active:scale-95" style="background-color: #dbeafe; border: 1px solid #93c5fd; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #2563eb;"></div>
                      <span class="text-xs font-medium" style="color: #1d4ed8;">QR Payment</span>
                    </div>
                    <div class="text-base font-bold" style="color: #2563eb;">{{ formatAmount(item.qr_amount) }}</div>
                  </div>
                </div>
                
                <!-- Row 2: Cheque & Credit -->
                <div class="grid grid-cols-2 gap-3 mb-3">
                  <div @click="navigateToDriverCategory(item, 'cheque')" class="category-pill cursor-pointer hover:shadow-md transition-all active:scale-95" style="background-color: #f3e8ff; border: 1px solid #d8b4fe; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #9333ea;"></div>
                      <span class="text-xs font-medium" style="color: #7e22ce;">Cheque</span>
                    </div>
                    <div class="text-base font-bold" style="color: #9333ea;">{{ formatAmount(item.cheque_amount || 0) }}</div>
                  </div>
                  <div @click="navigateToDriverCategory(item, 'credit')" class="category-pill cursor-pointer hover:shadow-md transition-all active:scale-95" style="background-color: #fee2e2; border: 1px solid #fca5a5; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #dc2626;"></div>
                      <span class="text-xs font-medium" style="color: #b91c1c;">Credit</span>
                    </div>
                    <div class="text-base font-bold" style="color: #dc2626;">{{ formatAmount(item.credit_amount || 0) }}</div>
                  </div>
                </div>
                
                <!-- Row 3: Return & Expense -->
                <div class="grid grid-cols-2 gap-3 mb-3">
                  <div @click="navigateToDriverCategory(item, 'return')" class="category-pill cursor-pointer hover:shadow-md transition-all active:scale-95" style="background-color: #ffedd5; border: 1px solid #fdba74; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #ea580c;"></div>
                      <span class="text-xs font-medium" style="color: #c2410c;">Return</span>
                    </div>
                    <div class="text-base font-bold" style="color: #ea580c;">{{ formatAmount(item.return_amount || 0) }}</div>
                  </div>
                  <div class="category-pill" style="background-color: #f3f4f6; border: 1px solid #d1d5db; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #4b5563;"></div>
                      <span class="text-xs font-medium" style="color: #374151;">Expense</span>
                    </div>
                    <div class="text-base font-bold" style="color: #4b5563;">{{ formatAmount(item.expense_amount || 0) }}</div>
                  </div>
                </div>
                
                <!-- Row 4: Cash Received & Cash Difference -->
                <div class="grid grid-cols-2 gap-3 mb-3">
                  <div class="category-pill" style="background-color: #dcfce7; border: 1px solid #86efac; border-radius: 0.75rem; padding: 0.75rem;">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" style="background-color: #22c55e;"></div>
                      <span class="text-xs font-medium" style="color: #15803d;">Cash Received</span>
                    </div>
                    <div class="text-base font-bold" style="color: #16a34a;">{{ formatAmount(item.cash_received || 0) }}</div>
                  </div>
                  <div class="category-pill" 
                       :style="{ 
                         backgroundColor: (item.cash_difference || 0) >= 0 ? '#dcfce7' : '#fee2e2',
                         border: (item.cash_difference || 0) >= 0 ? '1px solid #86efac' : '1px solid #fca5a5',
                         borderRadius: '0.75rem',
                         padding: '0.75rem'
                       }">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: (item.cash_difference || 0) >= 0 ? '#22c55e' : '#dc2626' }"></div>
                      <span class="text-xs font-medium" :style="{ color: (item.cash_difference || 0) >= 0 ? '#15803d' : '#b91c1c' }">Cash Difference</span>
                    </div>
                    <div class="text-base font-bold" :style="{ color: (item.cash_difference || 0) >= 0 ? '#16a34a' : '#dc2626' }">
                      {{ (item.cash_difference || 0) >= 0 ? '+' : '' }}{{ formatAmount(item.cash_difference || 0) }}
                    </div>
                  </div>
                </div>
                
                <!-- Remaining Amount Highlight -->
                <div @click="navigateToDriverCategory(item, '', true)" 
                     class="remaining-highlight p-3 rounded-xl cursor-pointer hover:shadow-md transition-all active:scale-[0.98]" 
                     :style="{ 
                       backgroundColor: (item.remaining_amount || 0) > 0 ? '#ecfeff' : '#f0fdf4',
                       border: (item.remaining_amount || 0) > 0 ? '2px solid #22d3ee' : '2px solid #86efac'
                     }">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <svg class="w-5 h-5" :style="{ color: (item.remaining_amount || 0) > 0 ? '#0891b2' : '#16a34a' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path v-if="(item.remaining_amount || 0) > 0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <span class="text-sm font-medium" :style="{ color: (item.remaining_amount || 0) > 0 ? '#0e7490' : '#15803d' }">
                        {{ (item.remaining_amount || 0) > 0 ? 'Remaining Balance' : 'Fully Collected' }}
                      </span>
                    </div>
                    <div class="text-lg font-bold" :style="{ color: (item.remaining_amount || 0) > 0 ? '#0891b2' : '#16a34a' }">
                      {{ formatAmount(item.remaining_amount || 0) }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- View Details Button -->
              <div class="px-4 pb-4">
                <button 
                  @click="viewDriverDetails(item)"
                  class="w-full py-2.5 rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-2"
                  style="background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                  View All Transactions
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Customer-wise View -->
        <div v-else-if="selectedViewMode === 'customer'">
          <h3 class="text-lg font-semibold mb-4" style="color: #111827;">Payments by Customer</h3>
          <div class="space-y-4">
            <div
              v-for="(item, index) in customerData"
              :key="item.customer"
              class="customer-card rounded-xl overflow-hidden transition-all"
              style="background-color: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
            >
              <!-- Customer Header -->
              <div class="p-4" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-bottom: 1px solid #e5e7eb;">
                <div class="flex items-start justify-between gap-3">
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <div class="relative">
                      <div class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold text-sm" 
                           :style="{ backgroundColor: getCustomerColor(index) }">
                        {{ getInitials(item.customer_name) }}
                      </div>
                      <!-- Company Badge - shown when "All Companies" is selected -->
                      <CompanyBadge 
                        v-if="!selectedCompany && item.company"
                        :company="item.company" 
                        size="sm" 
                        class="absolute -top-1 -right-1"
                      />
                    </div>
                    <div class="min-w-0 flex-1">
                      <div class="flex items-center gap-2">
                        <span class="font-semibold text-base truncate" style="color: #111827;">{{ item.customer_name }}</span>
                        <CompanyBadge v-if="selectedCompany" :company="selectedCompany" size="sm" />
                      </div>
                      <div class="text-xs truncate" style="color: #6b7280;">{{ item.customer }}</div>
                      <div class="flex items-center gap-1 mt-1">
                        <svg class="w-3 h-3" style="color: #9ca3af;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                        </svg>
                        <span class="text-xs" style="color: #6b7280;">{{ item.driver_name }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <div class="text-xs" style="color: #6b7280;">Total</div>
                    <div class="text-lg font-bold" style="color: #111827;">{{ formatAmount(item.net_total_amount) }}</div>
                    <!-- Status Badge -->
                    <span
                      v-if="item.settled"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold mt-1"
                      style="background-color: #dcfce7; color: #15803d;"
                    >
                      ✓ Settled
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold mt-1"
                      style="background-color: #fef3c7; color: #92400e;"
                    >
                      ○ Pending
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Payment Categories - Compact Grid -->
              <div class="p-3">
                <div class="grid grid-cols-3 gap-2">
                  <!-- Cash -->
                  <div class="text-center p-2 rounded-lg" style="background-color: #f0fdf4;">
                    <div class="text-xs font-medium" style="color: #15803d;">Cash</div>
                    <div class="text-sm font-bold" style="color: #16a34a;">{{ formatAmount(item.cash_amount) }}</div>
                  </div>
                  <!-- QR -->
                  <div class="text-center p-2 rounded-lg" style="background-color: #eff6ff;">
                    <div class="text-xs font-medium" style="color: #1d4ed8;">QR</div>
                    <div class="text-sm font-bold" style="color: #2563eb;">{{ formatAmount(item.qr_amount) }}</div>
                  </div>
                  <!-- Cheque -->
                  <div class="text-center p-2 rounded-lg" style="background-color: #faf5ff;">
                    <div class="text-xs font-medium" style="color: #7e22ce;">Cheque</div>
                    <div class="text-sm font-bold" style="color: #9333ea;">{{ formatAmount(item.cheque_amount || 0) }}</div>
                  </div>
                  <!-- Credit -->
                  <div class="text-center p-2 rounded-lg" style="background-color: #fef2f2;">
                    <div class="text-xs font-medium" style="color: #b91c1c;">Credit</div>
                    <div class="text-sm font-bold" style="color: #dc2626;">{{ formatAmount(item.credit_amount || 0) }}</div>
                  </div>
                  <!-- Return -->
                  <div class="text-center p-2 rounded-lg" style="background-color: #fff7ed;">
                    <div class="text-xs font-medium" style="color: #c2410c;">Return</div>
                    <div class="text-sm font-bold" style="color: #ea580c;">{{ formatAmount(item.return_amount || 0) }}</div>
                  </div>
                  <!-- Remaining -->
                  <div class="text-center p-2 rounded-lg" 
                       :style="{ backgroundColor: (item.remaining_amount || 0) > 0 ? '#ecfeff' : '#f0fdf4' }">
                    <div class="text-xs font-medium" :style="{ color: (item.remaining_amount || 0) > 0 ? '#0e7490' : '#15803d' }">Remaining</div>
                    <div class="text-sm font-bold" :style="{ color: (item.remaining_amount || 0) > 0 ? '#0891b2' : '#16a34a' }">{{ formatAmount(item.remaining_amount || 0) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Category-wise View -->
        <div v-else-if="selectedViewMode === 'category'">
          <h3 class="text-lg font-semibold mb-4" style="color: #111827;">Breakdown by Category</h3>
          <div class="grid grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            <!-- Cash Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #dcfce7; border: 2px solid #86efac;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #16a34a;"></div>
                <span class="text-sm font-semibold" style="color: #15803d;">Cash</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #16a34a;">{{ formatAmount(summary.cash_amount) }}</div>
              <div class="text-xs" style="color: #15803d;">{{ categoryBreakdown.cash_count || 0 }} transactions</div>
            </div>
            
            <!-- QR Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #dbeafe; border: 2px solid #93c5fd;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #2563eb;"></div>
                <span class="text-sm font-semibold" style="color: #1d4ed8;">QR Payment</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #2563eb;">{{ formatAmount(summary.qr_amount) }}</div>
              <div class="text-xs" style="color: #1d4ed8;">{{ categoryBreakdown.qr_count || 0 }} transactions</div>
            </div>
            
            <!-- Cheque Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #f3e8ff; border: 2px solid #d8b4fe;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #9333ea;"></div>
                <span class="text-sm font-semibold" style="color: #7e22ce;">Cheque</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #9333ea;">{{ formatAmount(summary.cheque_amount) }}</div>
              <div class="text-xs" style="color: #7e22ce;">{{ categoryBreakdown.cheque_count || 0 }} transactions</div>
            </div>
            
            <!-- Credit Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #fee2e2; border: 2px solid #fca5a5;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #dc2626;"></div>
                <span class="text-sm font-semibold" style="color: #b91c1c;">Credit</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #dc2626;">{{ formatAmount(summary.credit_amount) }}</div>
              <div class="text-xs" style="color: #b91c1c;">{{ categoryBreakdown.credit_count || 0 }} transactions</div>
            </div>
            
            <!-- Return Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #ffedd5; border: 2px solid #fdba74;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #ea580c;"></div>
                <span class="text-sm font-semibold" style="color: #c2410c;">Return</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #ea580c;">{{ formatAmount(summary.return_amount) }}</div>
              <div class="text-xs" style="color: #c2410c;">{{ categoryBreakdown.return_count || 0 }} transactions</div>
            </div>
            
            <!-- Remaining Category -->
            <div class="category-card p-4 rounded-xl" style="background-color: #ecfeff; border: 2px solid #22d3ee;">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full" style="background-color: #0891b2;"></div>
                <span class="text-sm font-semibold" style="color: #0e7490;">Remaining</span>
              </div>
              <div class="text-xl sm:text-2xl font-bold mb-1" style="color: #0891b2;">{{ formatAmount(summary.remaining_amount) }}</div>
              <div class="text-xs" style="color: #0e7490;">Uncollected balance</div>
            </div>
          </div>
        </div>

        <!-- Detail View -->
        <div v-else-if="selectedViewMode === 'detail'">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold" style="color: #111827;">All Transaction Details</h3>
            <span class="text-sm" style="color: #6b7280;">{{ detailData.length }} items</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="(line, idx) in detailData"
              :key="line.name"
              class="detail-card rounded-xl overflow-hidden"
              style="background-color: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
            >
              <!-- Header -->
              <div class="p-3" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-bottom: 1px solid #e5e7eb;">
                <div class="flex items-start justify-between gap-2">
                  <div class="flex items-center gap-2 flex-1 min-w-0">
                    <div class="relative">
                      <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs font-bold"
                           :style="{ backgroundColor: getCustomerColor(idx) }">
                        {{ getInitials(line.customer_name || line.customer) }}
                      </div>
                      <!-- Company Badge - shown when "All Companies" is selected -->
                      <CompanyBadge 
                        v-if="!selectedCompany && line.company"
                        :company="line.company" 
                        size="sm" 
                        class="absolute -top-1 -right-1"
                      />
                    </div>
                    <div class="min-w-0 flex-1">
                      <div class="flex items-center gap-2">
                        <span class="font-semibold text-sm truncate" style="color: #111827;">{{ line.customer_name || line.customer }}</span>
                        <CompanyBadge v-if="selectedCompany" :company="selectedCompany" size="sm" />
                      </div>
                      <div class="text-xs" style="color: #6b7280;">{{ line.driver_name }}</div>
                    </div>
                  </div>
                  <div class="flex-shrink-0 flex flex-col items-end">
                    <div class="text-base font-bold" style="color: #111827;">{{ formatAmount(line.net_total_amount) }}</div>
                    <span
                      v-if="line.settled"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold"
                      style="background-color: #dcfce7; color: #15803d;"
                    >✓ Settled</span>
                    <span
                      v-else
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold"
                      style="background-color: #fef3c7; color: #92400e;"
                    >○ Pending</span>
                  </div>
                </div>
              </div>
              
              <!-- Payment Breakdown -->
              <div class="p-3">
                <div class="grid grid-cols-3 gap-2 mb-2">
                  <div v-if="line.cash_amount" class="text-center p-2 rounded-lg" style="background-color: #f0fdf4;">
                    <div class="text-xs" style="color: #15803d;">Cash</div>
                    <div class="text-sm font-bold" style="color: #16a34a;">{{ formatAmount(line.cash_amount) }}</div>
                  </div>
                  <div v-if="line.qr_amount" class="text-center p-2 rounded-lg" style="background-color: #eff6ff;">
                    <div class="text-xs" style="color: #1d4ed8;">QR</div>
                    <div class="text-sm font-bold" style="color: #2563eb;">{{ formatAmount(line.qr_amount) }}</div>
                  </div>
                  <div v-if="line.cheque_amount" class="text-center p-2 rounded-lg" style="background-color: #faf5ff;">
                    <div class="text-xs" style="color: #7e22ce;">Cheque</div>
                    <div class="text-sm font-bold" style="color: #9333ea;">{{ formatAmount(line.cheque_amount) }}</div>
                  </div>
                  <div v-if="line.credit_amount" class="text-center p-2 rounded-lg" style="background-color: #fef2f2;">
                    <div class="text-xs" style="color: #b91c1c;">Credit</div>
                    <div class="text-sm font-bold" style="color: #dc2626;">{{ formatAmount(line.credit_amount) }}</div>
                  </div>
                  <div v-if="line.return_amount" class="text-center p-2 rounded-lg" style="background-color: #fff7ed;">
                    <div class="text-xs" style="color: #c2410c;">Return</div>
                    <div class="text-sm font-bold" style="color: #ea580c;">{{ formatAmount(line.return_amount) }}</div>
                  </div>
                  <div v-if="line.remaining_amount" class="text-center p-2 rounded-lg" style="background-color: #ecfeff;">
                    <div class="text-xs" style="color: #0e7490;">Remaining</div>
                    <div class="text-sm font-bold" style="color: #0891b2;">{{ formatAmount(line.remaining_amount) }}</div>
                  </div>
                </div>
                <!-- Show message if no payment breakdown to display -->
                <div v-if="!line.cash_amount && !line.qr_amount && !line.cheque_amount && !line.credit_amount && !line.return_amount && !line.remaining_amount"
                     class="text-center p-2 rounded-lg" style="background-color: #f3f4f6;">
                  <span class="text-xs" style="color: #6b7280;">No payment breakdown available</span>
                </div>
                <!-- Remarks if any -->
                <div v-if="line.remarks" class="mt-2 pt-2" style="border-top: 1px solid #e5e7eb;">
                  <div class="text-xs" style="color: #6b7280;">
                    <span class="font-medium">Note:</span> {{ line.remarks }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      
      <!-- Cheques View -->
      <div v-else-if="selectedViewMode === 'cheques'">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h3 class="text-lg font-semibold" style="color: #111827;">Pending Cheques</h3>
          
          <!-- Cheque Filters/Sort -->
          <div class="flex flex-wrap gap-2 w-full sm:w-auto">
            <select v-model="chequeSort" class="select-dropdown text-sm p-2 border rounded-lg">
              <option value="date_asc">Date: Oldest First</option>
              <option value="date_desc">Date: Newest First</option>
              <option value="amount_desc">Amount: High to Low</option>
              <option value="amount_asc">Amount: Low to High</option>
            </select>
            
            <select v-model="chequeFilterStatus" class="select-dropdown text-sm p-2 border rounded-lg">
               <option value="all">All Pending</option>
               <option value="due_today">Due Today/Late</option>
               <option value="future">Future Dated</option>
            </select>
          </div>
        </div>

        <div class="space-y-3">
           <div v-if="loadingCheques" class="text-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 mx-auto border-b-2 border-rose-600"></div>
           </div>
           <div v-else-if="!filteredCheques.length" class="text-center py-8 text-gray-500">
              No cheques found matching filters.
           </div>
           <div
             v-for="cheque in filteredCheques"
             :key="cheque.name"
             class="rounded-xl p-4 transition-all hover:shadow-md"
             style="background-color: #ffffff; border: 1px solid #e5e7eb;"
           >
             <div class="flex flex-col sm:flex-row justify-between gap-4">
               <div class="flex items-start gap-3">
                 <div class="relative">
                   <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-rose-500">
                      {{ getInitials(cheque.customer_name) }}
                   </div>
                   <!-- Company Badge - shown when "All Companies" is selected -->
                   <CompanyBadge 
                     v-if="!selectedCompany"
                     :company="getChequeCompany(cheque)" 
                     size="sm" 
                     class="absolute -top-1 -right-1"
                   />
                 </div>
                 <div>
                   <div class="flex items-center gap-2">
                     <span class="font-semibold text-gray-900">{{ cheque.customer_name }}</span>
                     <CompanyBadge v-if="selectedCompany" :company="selectedCompany" size="sm" />
                   </div>
                   <div class="text-xs text-gray-500">Cheque No: {{ cheque.cheque_no }}</div>
                   <div class="text-xs text-gray-500">{{ cheque.bank_name }}</div>
                   <div v-if="cheque.brought_by_full_name" class="text-xs text-gray-600 mt-1">
                     Bought by: {{ cheque.brought_by_full_name }}
                   </div>
                 </div>
               </div>
               
               <div class="text-right">
                  <div class="font-bold text-lg text-gray-900">{{ formatAmount(cheque.amount) }}</div>
                  <div class="mt-1 inline-flex items-center px-2 py-1 rounded bg-gray-100 text-xs font-medium text-gray-700">
                     BS: {{ cheque.cheque_date_nepali }}
                  </div>
                  <div class="text-xs mt-1" :class="isDue(cheque.cheque_date_nepali) ? 'text-rose-600 font-bold' : 'text-green-600'">
                     {{ getDueStatus(cheque.cheque_date_nepali) }}
                  </div>
               </div>
             </div>
           </div>
        </div>
      </div>
    </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { session } from '../../shared/data/session'
import NepaliDatePicker from '../../shared/components/NepaliDatePicker.vue'
import CompanyBadge from '../../shared/components/CompanyBadge.vue'
import { adToBs, getTodayBs } from '../../shared/utils/nepaliDate'

// State
const summary = ref({
  net_total_amount: 0,
  cash_amount: 0,
  qr_amount: 0,
  cheque_amount: 0,
  credit_amount: 0,
  return_amount: 0,
  expense_amount: 0,
  remaining_amount: 0,
  total_records: 0,
  cheque_settlement_info: {
    total_pending_count: 0,
    total_pending_amount: 0,
    due_today_count: 0,
    due_today_amount: 0,
    today_bs: ''
  }
})

const categoryBreakdown = ref({
  cash_count: 0,
  qr_count: 0,
  cheque_count: 0,
  credit_count: 0,
  return_count: 0,
})

const chequeData = ref([])
const loadingCheques = ref(false)
const chequeSort = ref('date_asc')
const chequeFilterStatus = ref('all')

const bsToday = ref(getTodayBs())
const adToday = ref(new Date().toLocaleDateString('en-CA'))
const selectedDate = ref(null)
const selectedDateBs = computed(() => {
  return selectedDate.value ? adToBs(selectedDate.value) : ''
})

const loading = ref(false)
const loadingData = ref(false)

// View mode
const viewModes = [
  { value: 'driver', label: 'By Driver' },
  { value: 'customer', label: 'By Customer' },
  { value: 'category', label: 'By Category' },
  { value: 'detail', label: 'Details' },
  { value: 'cheques', label: 'Cheque List' },
]
const selectedViewMode = ref('driver')

// Filters
const selectedDriver = ref('')
const selectedCustomer = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')
const selectedCompany = ref('') // '' = All companies
const driverOptions = ref([])
const customerOptions = ref([])

// Company options
const companyOptions = [
  { value: '', label: 'All Companies' },
  { value: 'PadmaShree Trade Link', label: 'PadmaShree Trade Link' },
  { value: 'Riya Trades and Suppliers', label: 'Riya Trades and Suppliers' },
]

// Data
const driverData = ref([])
const customerData = ref([])
const detailData = ref([])

// API Resources
const summaryResource = createResource({
  url: 'custom_erp.api.payment_reco.get_daily_transactions_summary',
  auto: false,
})

const driverDataResource = createResource({
  url: 'custom_erp.api.payment_reco.get_daily_transactions_by_user',
  auto: false,
})

const customerDataResource = createResource({
  url: 'custom_erp.api.payment_reco.get_daily_transactions_by_customer',
  auto: false,
})

const detailDataResource = createResource({
  url: 'custom_erp.api.payment_reco.get_daily_transactions_details',
  auto: false,
})

const chequeListResource = createResource({
  url: 'custom_erp.api.payment_reco.get_due_cheques',
  auto: false,
  onSuccess: (data) => {
    // Handle both wrapped and unwrapped data
    const list = data?.success ? data.data : (Array.isArray(data) ? data : (data?.data || []))
    chequeData.value = list
    loadingCheques.value = false
  },
  onError: (err) => {
    console.error('Failed to load cheques', err)
    loadingCheques.value = false
  }
})

// Computed
const hasActiveFilters = computed(() => {
  return Boolean(selectedDriver.value || selectedCustomer.value || selectedCategory.value || selectedStatus.value || selectedCompany.value)
})

const hasData = computed(() => {
  if (selectedViewMode.value === 'driver') return driverData.value.length > 0
  if (selectedViewMode.value === 'customer') return customerData.value.length > 0
  if (selectedViewMode.value === 'category') return summary.value.total_records > 0
  if (selectedViewMode.value === 'detail') return detailData.value.length > 0
  if (selectedViewMode.value === 'cheques') return true // Always show container, handle empty state inside
  return false
})

const filteredCheques = computed(() => {
  let items = [...chequeData.value]
  const today = summary.value.cheque_settlement_info?.today_bs || getTodayBs()
  
  // Filter
  if (chequeFilterStatus.value === 'due_today') {
     items = items.filter(c => c.cheque_date_nepali <= today)
  } else if (chequeFilterStatus.value === 'future') {
     items = items.filter(c => c.cheque_date_nepali > today)
  }
  
  // Sort
  items.sort((a, b) => {
    if (chequeSort.value === 'amount_desc') return b.amount - a.amount
    if (chequeSort.value === 'amount_asc') return a.amount - b.amount
    if (chequeSort.value === 'date_desc') return b.cheque_date_nepali.localeCompare(a.cheque_date_nepali)
    return a.cheque_date_nepali.localeCompare(b.cheque_date_nepali) // date_asc default
  })
  
  return items
})

watch(selectedViewMode, (newMode) => {
  if (newMode === 'cheques') {
    loadingCheques.value = true
    chequeListResource.submit({ company: selectedCompany.value || undefined })
  }
})

// Methods
const formatAmount = (amount) => {
  const num = Number(amount) || 0
  return 'NPR ' + num.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

const formatAmountShort = (amount) => {
  const num = Number(amount) || 0
  return 'NPR ' + num.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

const getDriverLabel = (driverValue) => {
  const driver = driverOptions.value.find(d => d.value === driverValue)
  return driver ? driver.label : driverValue
}

const getCustomerLabel = (customerValue) => {
  const customer = customerOptions.value.find(c => c.value === customerValue)
  return customer ? customer.label : customerValue
}

const isDue = (dateBs) => {
  const today = summary.value.cheque_settlement_info?.today_bs || getTodayBs()
  return dateBs <= today
}

const getDueStatus = (dateBs) => {
  const today = summary.value.cheque_settlement_info?.today_bs || getTodayBs()
  if (dateBs < today) return 'Overdue'
  if (dateBs === today) return 'Due Today'
  return 'Future'
}

// Helper functions for UI
const driverColors = ['#0891b2', '#059669', '#7c3aed', '#db2777', '#ea580c', '#ca8a04', '#0284c7', '#4f46e5']
const customerColors = ['#059669', '#0891b2', '#7c3aed', '#db2777', '#ea580c', '#ca8a04', '#4f46e5', '#0284c7']

const getDriverColor = (index) => {
  return driverColors[index % driverColors.length]
}

const getCustomerColor = (index) => {
  return customerColors[index % customerColors.length]
}

const getInitials = (name) => {
  if (!name) return '?'
  const words = name.trim().split(' ')
  if (words.length >= 2) {
    return (words[0][0] + words[words.length - 1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const viewDriverDetails = (driverItem) => {
  // Set the driver filter and switch to detail view
  selectedDriver.value = driverItem.driver
  selectedViewMode.value = 'detail'
  applyFilters()
}

// Navigate to details with category filter (from driver card)
const navigateToDriverCategory = (driverItem, category, isRemaining = false) => {
  selectedDriver.value = driverItem.driver
  if (isRemaining) {
    selectedCategory.value = ''
    selectedStatus.value = 'pending'
  } else {
    selectedCategory.value = category
    selectedStatus.value = ''
  }
  selectedViewMode.value = 'detail'
  applyFilters()
}

// Navigate to details with category filter only (from summary cards)
const navigateToSummaryCategory = (category, isRemaining = false) => {
  selectedDriver.value = ''
  selectedCustomer.value = ''
  if (isRemaining) {
    selectedCategory.value = ''
    selectedStatus.value = 'pending'
  } else {
    selectedCategory.value = category
    selectedStatus.value = ''
  }
  selectedViewMode.value = 'detail'
  applyFilters()
}

const viewCustomerDetails = (customerItem) => {
  // Set the customer filter and switch to detail view
  selectedCustomer.value = customerItem.customer
  selectedViewMode.value = 'detail'
  applyFilters()
}

const clearDriverFilter = () => {
  selectedDriver.value = ''
  applyFilters()
}

const clearCustomerFilter = () => {
  selectedCustomer.value = ''
  applyFilters()
}

const clearCategoryFilter = () => {
  selectedCategory.value = ''
  applyFilters()
}

const clearStatusFilter = () => {
  selectedStatus.value = ''
  applyFilters()
}

const clearCompanyFilter = () => {
  selectedCompany.value = ''
  applyFilters()
}

const handleCompanyChange = () => {
  // Reload all data with the new company filter
  refreshAll()
}

// Get style for company select based on selected company
const getCompanySelectStyle = () => {
  if (selectedCompany.value === 'PadmaShree Trade Link') {
    return 'border-color: #0077B6; background-color: #E6F4FA; color: #0077B6;'
  } else if (selectedCompany.value === 'Riya Trades and Suppliers') {
    return 'border-color: #F40009; background-color: #FEE6E6; color: #F40009;'
  }
  return 'color: #111827; background-color: #ffffff;'
}

// Get company for cheque (blank = Riya)
const getChequeCompany = (cheque) => {
  return cheque.company || 'Riya Trades and Suppliers'
}

const clearAllFilters = () => {
  selectedDriver.value = ''
  selectedCustomer.value = ''
  selectedCategory.value = ''
  selectedStatus.value = ''
  selectedCompany.value = ''
  applyFilters()
}

watch(selectedDate, (newVal) => {
  console.log('DailyTransactions: watcher triggered for selectedDate:', newVal);
  if (newVal) {
    refreshAll()
  }
})

const handleDateChange = async (adDate) => {
  console.log('DailyTransactions: handleDateChange called with', adDate);
  // #region agent log
  fetch('http://localhost:7242/ingest/438788ef-4596-4099-9ba4-470042d02997',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'DailyTransactions.vue:handleDateChange',message:'Date change handler triggered',data:{adDate},timestamp:Date.now(),sessionId:'debug-data-sync',hypothesisId:'F/G'})}).catch(()=>{});
  // #endregion
  if (selectedDate.value !== adDate) {
    selectedDate.value = adDate
    // refreshAll is handled by the watch above
  }
}

const clearDateFilter = async () => {
  selectedDate.value = null
  bsToday.value = getTodayBs()
  await refreshAll()
}

const loadSummary = async () => {
  console.log('DailyTransactions: loadSummary calling with date:', selectedDate.value, 'company:', selectedCompany.value);
  try {
    const res = await summaryResource.fetch({
      date: selectedDate.value || undefined,
      company: selectedCompany.value || undefined,
    })
    
    // Support both raw response and unwrapped data
    const data = res?.success ? res.data : (res?.net_total_amount !== undefined ? res : null)
    
    if (data) {
      summary.value = {
        net_total_amount: Number(data.net_total_amount || 0),
        cash_amount: Number(data.cash_amount || 0),
        qr_amount: Number(data.qr_amount || 0),
        cheque_amount: Number(data.cheque_amount || 0),
        credit_amount: Number(data.credit_amount || 0),
        return_amount: Number(data.return_amount || 0),
        expense_amount: Number(data.expense_amount || 0),
        remaining_amount: Number(data.remaining_amount || 0),
        total_records: Number(data.total_records || 0),
        cheque_settlement_info: data.cheque_settlement_info || {},
      }
      
      categoryBreakdown.value = {
        cash_count: Number(data.cash_count || 0),
        qr_count: Number(data.qr_count || 0),
        cheque_count: Number(data.cheque_count || 0),
        credit_count: Number(data.credit_count || 0),
        return_count: Number(data.return_count || 0),
      }
      
      // Update filter options from summary data
      if (data.drivers) {
        driverOptions.value = data.drivers.map(d => ({
          value: d.driver,
          label: d.driver_name,
        }))
      }
      
      if (data.customers) {
        customerOptions.value = data.customers.map(c => ({
          value: c.customer,
          label: c.customer_name || c.customer,
        }))
      }
    }
  } catch (error) {
    console.error('Failed to load summary', error)
  }
}

const loadDriverData = async () => {
  loadingData.value = true
  try {
    const res = await driverDataResource.fetch({
      date: selectedDate.value || undefined,
      driver_filter: selectedDriver.value || undefined,
      status_filter: selectedStatus.value || undefined,
      company: selectedCompany.value || undefined,
    })
    
    const data = res?.success ? res.data : (Array.isArray(res) ? res : null)
    
    if (data) {
      driverData.value = data
    }
  } catch (error) {
    console.error('Failed to load driver data', error)
    driverData.value = []
  } finally {
    loadingData.value = false
  }
}

const loadCustomerData = async () => {
  loadingData.value = true
  try {
    const res = await customerDataResource.fetch({
      date: selectedDate.value || undefined,
      driver_filter: selectedDriver.value || undefined,
      customer_filter: selectedCustomer.value || undefined,
      status_filter: selectedStatus.value || undefined,
      company: selectedCompany.value || undefined,
    })
    
    const data = res?.success ? res.data : (Array.isArray(res) ? res : null)
    
    if (data) {
      customerData.value = data
    }
  } catch (error) {
    console.error('Failed to load customer data', error)
    customerData.value = []
  } finally {
    loadingData.value = false
  }
}

const loadDetailData = async () => {
  loadingData.value = true
  try {
    const res = await detailDataResource.fetch({
      date: selectedDate.value || undefined,
      driver_filter: selectedDriver.value || undefined,
      customer_filter: selectedCustomer.value || undefined,
      category_filter: selectedCategory.value || undefined,
      status_filter: selectedStatus.value || undefined,
      company: selectedCompany.value || undefined,
    })
    
    const data = res?.success ? res.data : (Array.isArray(res) ? res : null)
    
    if (data) {
      detailData.value = data
    }
  } catch (error) {
    console.error('Failed to load detail data', error)
    detailData.value = []
  } finally {
    loadingData.value = false
  }
}

const applyFilters = async () => {
  if (selectedViewMode.value === 'driver') {
    await loadDriverData()
  } else if (selectedViewMode.value === 'customer') {
    await loadCustomerData()
  } else if (selectedViewMode.value === 'detail') {
    await loadDetailData()
  }
  // Category view uses summary data which is already loaded
}

const refreshAll = async () => {
  console.error('DailyTransactions: refreshAll START', { loading: loading.value, selectedDate: selectedDate.value });
  // #region agent log
  fetch('http://localhost:7242/ingest/438788ef-4596-4099-9ba4-470042d02997',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'DailyTransactions.vue:refreshAll',message:'Refreshing all data',data:{selectedDate:selectedDate.value},timestamp:Date.now(),sessionId:'debug-data-sync',hypothesisId:'H'})}).catch(()=>{});
  // #endregion
  loading.value = true
  try {
    console.error('DailyTransactions: fetching summary for', selectedDate.value);
    await loadSummary()
    console.error('DailyTransactions: summary loaded');
    await applyFilters()
    console.error('DailyTransactions: filters applied');
  } catch (err) {
    console.error('DailyTransactions: refreshAll ERROR', err);
  } finally {
    loading.value = false
    console.error('DailyTransactions: refreshAll END');
  }
}

// Watch for view mode changes
watch(selectedViewMode, async () => {
  await applyFilters()
})

onMounted(async () => {
  bsToday.value = getTodayBs()
  
  // Initialize with today's AD date in YYYY-MM-DD format
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const todayStr = `${year}-${month}-${day}`
  
  selectedDate.value = todayStr
  
  await refreshAll()
})
</script>

<style scoped>
button, select {
  min-height: 44px;
}

/* Ensure select dropdowns have visible text */
.select-dropdown {
  width: 100%;
  padding: 0.625rem 2.5rem 0.625rem 0.875rem;
  height: 44px;
  border: 2px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
  background-color: #ffffff;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  cursor: pointer;
}

.select-dropdown:focus {
  outline: none;
  border-color: #0891b2;
  box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1);
}

.select-dropdown option {
  color: #111827;
  background-color: #ffffff;
  padding: 0.5rem;
}

@media (max-width: 640px) {
  section {
    padding: 1rem !important;
  }
  
  .select-dropdown {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}
</style>

