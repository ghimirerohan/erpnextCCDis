<template>
  <div class="min-h-screen" style="background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 50%, #ffffff 100%);">
    <!-- Header -->
    <header class="sticky top-0 z-20 bg-white border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- App Branding -->
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 rounded-xl" style="background: linear-gradient(135deg, #059669 0%, #047857 100%);">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-lg sm:text-xl font-bold text-gray-900">Employee Attendance</h1>
              <p class="text-xs sm:text-sm text-gray-500">Track & Manage</p>
            </div>
          </div>
          
          <!-- Logout Button -->
          <button
            @click="session.logout.submit()"
            class="inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all"
          >
            <svg class="w-4 h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      
      <!-- Date Selection & Actions Card -->
      <section class="bg-white rounded-2xl shadow-lg p-4 sm:p-6 border border-gray-100">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <!-- Today's Date Display -->
          <div class="flex-shrink-0">
            <div class="text-xs text-gray-500 uppercase tracking-wide font-medium">Selected Date (BS)</div>
            <div class="text-xl sm:text-2xl font-bold text-gray-900 mt-1">
              {{ selectedDateBs || bsToday }}
              <span class="text-sm font-normal text-gray-500 ml-1">({{ selectedDate || adToday }})</span>
            </div>
            <div class="text-sm text-gray-600 mt-1">
              Logged in as: <span class="font-medium text-emerald-700">{{ session.user }}</span>
            </div>
          </div>
          
          <!-- Date Picker -->
          <div class="flex-1 max-w-xs">
            <label class="block text-xs text-gray-500 uppercase tracking-wide mb-2 font-medium">Select Date</label>
            <NepaliDatePicker
              v-model="selectedDate"
              @update:modelValue="handleDateChange"
              placeholder="Select date (BS)"
            />
          </div>
          
          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="refreshData"
              :disabled="loading"
              class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-semibold rounded-xl text-white shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all active:scale-95 disabled:opacity-50"
              style="background: linear-gradient(135deg, #059669 0%, #047857 100%);"
            >
              <svg v-if="loading" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
            
            <button
              @click="syncAttendance"
              :disabled="syncing"
              class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-semibold rounded-xl text-white shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all active:scale-95 disabled:opacity-50"
              style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);"
            >
              <svg v-if="syncing" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Sync Attendance
            </button>
          </div>
        </div>
      </section>

      <!-- Summary Cards Grid -->
      <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        <!-- Total Employees -->
        <div class="bg-white rounded-xl shadow-md p-4 border border-gray-100">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-gray-500 font-medium">Total</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-900">{{ summary.total || 0 }}</div>
        </div>
        
        <!-- Present -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border: 2px solid #047857;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-white bg-opacity-30 flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-white font-semibold">Present</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-white">{{ summary.present || 0 }}</div>
        </div>
        
        <!-- Absent -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border: 1px solid #fca5a5;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-red-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-red-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-red-700 font-medium">Absent</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-red-800">{{ summary.absent || 0 }}</div>
        </div>
        
        <!-- On Time Entry -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 1px solid #93c5fd;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-blue-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-blue-700 font-medium">On Time In</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-blue-800">{{ summary.on_time_entry || 0 }}</div>
        </div>
        
        <!-- Late Entry -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 1px solid #fcd34d;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-amber-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-amber-700 font-medium">Late Entry</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-amber-800">{{ summary.late_entry || 0 }}</div>
        </div>
        
        <!-- Early Exit -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); border: 1px solid #f9a8d4;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-pink-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-pink-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-pink-700 font-medium">Early Exit</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-pink-800">{{ summary.early_exit || 0 }}</div>
        </div>
      </section>

      <!-- Employee Attendance List -->
      <section class="bg-white rounded-2xl shadow-lg p-4 sm:p-6 border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-gray-900">Employee List</h2>
          <span class="text-sm text-gray-500">{{ employees.length }} employees</span>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 mx-auto border-b-2 border-emerald-600"></div>
          <p class="mt-4 text-gray-500">Loading attendance data...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="!employees.length" class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
          <p class="mt-4 text-gray-500 text-lg">No attendance records found</p>
          <p class="text-sm text-gray-400">for {{ selectedDateBs || bsToday }}</p>
        </div>
        
        <!-- Employee Cards Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="emp in employees"
            :key="emp.employee"
            @click="viewEmployeeHistory(emp)"
            class="employee-card rounded-xl p-3 border-2 transition-all hover:shadow-lg cursor-pointer active:scale-98"
            :class="getEmployeeCardClass(emp)"
          >
            <!-- Header with avatar and name -->
            <div class="flex items-start gap-2.5 mb-2.5">
              <div 
                class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold text-xs"
                :style="{ background: getAvatarGradient(emp) }"
              >
                {{ getInitials(emp.employee_name) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-semibold text-gray-900 truncate text-sm leading-tight">{{ emp.employee_name }}</div>
                <div class="text-xs text-gray-500 truncate mt-0.5">{{ emp.employee }}</div>
              </div>
              <!-- Status Badge -->
              <div class="flex-shrink-0">
                <span 
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold"
                  :class="getStatusBadgeClass(emp.status)"
                >
                  {{ emp.status || 'Unknown' }}
                </span>
              </div>
            </div>
            
            <!-- Time Info -->
            <div class="grid grid-cols-2 gap-2 mb-2">
              <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-lg p-2 border border-emerald-200">
                <div class="flex items-center gap-1 mb-1">
                  <svg class="w-3 h-3 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
                  </svg>
                  <span class="text-xs text-emerald-700 font-semibold">In</span>
                </div>
                <div class="text-base font-bold" :class="emp.late_entry ? 'text-amber-700' : 'text-emerald-800'">
                  {{ formatTime12Hour(emp.in_time) }}
                </div>
                <div v-if="emp.late_entry" class="text-xs text-amber-700 font-semibold mt-0.5">Late</div>
              </div>
              <div class="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-2 border border-red-200">
                <div class="flex items-center gap-1 mb-1">
                  <svg class="w-3 h-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                  </svg>
                  <span class="text-xs text-red-700 font-semibold">Out</span>
                </div>
                <div class="text-base font-bold" :class="emp.early_exit ? 'text-pink-700' : 'text-red-800'">
                  {{ formatTime12Hour(emp.out_time) }}
                </div>
                <div v-if="emp.early_exit" class="text-xs text-pink-700 font-semibold mt-0.5">Early</div>
              </div>
            </div>
            
            <!-- Flags Row -->
            <div v-if="emp.late_entry || emp.early_exit" class="flex gap-1.5 flex-wrap mb-1.5">
              <span v-if="emp.late_entry" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-700 border border-amber-300">
                <svg class="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3"></path>
                </svg>
                Late
              </span>
              <span v-if="emp.early_exit" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-pink-100 text-pink-700 border border-pink-300">
                <svg class="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4"></path>
                </svg>
                Early
              </span>
            </div>
            
            <!-- View Details Indicator -->
            <div class="flex items-center justify-end text-xs text-gray-400 pt-1 border-t border-gray-100">
              <span>Tap for history</span>
              <svg class="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
          </div>
        </div>
      </section>
    </main>
    
    <!-- Sync Result Dialog -->
    <Dialog v-model="showSyncDialog" :dismissable="true">
      <template #body>
        <div class="p-6 text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" 
               :class="syncResult.success ? 'bg-emerald-100' : 'bg-amber-100'">
            <svg v-if="syncResult.success" class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 mb-2">{{ syncResult.title }}</h3>
          <p class="text-gray-600 mb-4">{{ syncResult.message }}</p>
          <div v-if="syncResult.processed > 0" class="bg-gray-50 rounded-lg p-4 mb-4">
            <div class="text-3xl font-bold text-emerald-600">{{ syncResult.processed }}</div>
            <div class="text-sm text-gray-500">Attendance Records Processed</div>
          </div>
          <button 
            @click="showSyncDialog = false"
            class="w-full py-3 px-4 rounded-xl font-semibold text-white transition-all"
            style="background: linear-gradient(135deg, #059669 0%, #047857 100%);"
          >
            Close
          </button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { createResource, Dialog } from 'frappe-ui'
import { session } from '../../shared/data/session'
import NepaliDatePicker from '../../shared/components/NepaliDatePicker.vue'
import { adToBs, getTodayBs, formatTime12Hour } from '../../shared/utils/nepaliDate'

const router = useRouter()

// State
const loading = ref(false)
const syncing = ref(false)
const employees = ref([])
const summary = ref({
  total: 0,
  present: 0,
  absent: 0,
  on_time_entry: 0,
  late_entry: 0,
  early_exit: 0,
  on_time_exit: 0,
})

// Date state
const bsToday = ref(getTodayBs())
const adToday = ref(new Date().toLocaleDateString('en-CA'))
const selectedDate = ref(null)
const selectedDateBs = computed(() => selectedDate.value ? adToBs(selectedDate.value) : '')

// Sync dialog
const showSyncDialog = ref(false)
const syncResult = ref({
  success: true,
  title: '',
  message: '',
  processed: 0
})

// API Resources
const attendanceResource = createResource({
  url: 'custom_erp.api.emp_attendance.get_attendance_list',
  auto: false,
})

const syncResource = createResource({
  url: 'custom_erp.api.emp_attendance.sync_attendance',
  auto: false,
})

// Methods
const getInitials = (name) => {
  if (!name) return '?'
  const words = name.trim().split(' ')
  if (words.length >= 2) {
    return (words[0][0] + words[words.length - 1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const getAvatarGradient = (emp) => {
  const colors = [
    'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
  ]
  const index = emp.employee?.charCodeAt(emp.employee.length - 1) || 0
  return colors[index % colors.length]
}

const getEmployeeCardClass = (emp) => {
  if (emp.status === 'Present') {
    return 'border-emerald-400 bg-gradient-to-br from-emerald-100 to-emerald-50 shadow-emerald-100'
  } else if (emp.status === 'Absent') {
    return 'border-red-200 bg-gradient-to-br from-red-50 to-white'
  } else if (emp.status === 'Half Day') {
    return 'border-amber-200 bg-gradient-to-br from-amber-50 to-white'
  } else if (emp.status === 'On Leave') {
    return 'border-blue-200 bg-gradient-to-br from-blue-50 to-white'
  }
  return 'border-gray-200 bg-white'
}

const getStatusBadgeClass = (status) => {
  if (status === 'Present') {
    return 'bg-emerald-600 text-white border border-emerald-700 shadow-sm'
  } else if (status === 'Absent') {
    return 'bg-red-100 text-red-800 border border-red-200'
  } else if (status === 'Half Day') {
    return 'bg-amber-100 text-amber-800 border border-amber-200'
  } else if (status === 'On Leave') {
    return 'bg-blue-100 text-blue-800 border border-blue-200'
  }
  return 'bg-gray-100 text-gray-800 border border-gray-200'
}

const handleDateChange = async (adDate) => {
  if (selectedDate.value !== adDate) {
    selectedDate.value = adDate
    await refreshData()
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    const dateToFetch = selectedDate.value || adToday.value
    const res = await attendanceResource.fetch({
      date: dateToFetch,
    })
    
    if (res?.success) {
      employees.value = res.data || []
      summary.value = res.summary || summary.value
    } else if (res?.data) {
      employees.value = res.data || []
      summary.value = res.summary || summary.value
    }
  } catch (error) {
    console.error('Failed to fetch attendance data:', error)
    employees.value = []
  } finally {
    loading.value = false
  }
}

const syncAttendance = async () => {
  syncing.value = true
  try {
    const dateToSync = selectedDate.value || adToday.value
    const res = await syncResource.fetch({
      date: dateToSync,
    })
    
    if (res?.success) {
      if (res.processed === 0) {
        syncResult.value = {
          success: true,
          title: 'All Up to Date',
          message: res.message || 'No checkins left to process',
          processed: 0
        }
      } else {
        syncResult.value = {
          success: true,
          title: 'Sync Complete',
          message: res.message || 'Attendance records have been processed successfully.',
          processed: res.processed || 0
        }
        // Refresh data after successful sync
        await refreshData()
      }
    } else {
      syncResult.value = {
        success: false,
        title: 'Sync Issue',
        message: res?.message || 'Unable to sync attendance. Please try again.',
        processed: 0
      }
    }
    showSyncDialog.value = true
  } catch (error) {
    console.error('Failed to sync attendance:', error)
    syncResult.value = {
      success: false,
      title: 'Sync Failed',
      message: 'An error occurred while syncing attendance.',
      processed: 0
    }
    showSyncDialog.value = true
  } finally {
    syncing.value = false
  }
}

const viewEmployeeHistory = (emp) => {
  router.push({
    name: 'EmployeeHistory',
    params: { employeeId: emp.employee }
  })
}

// Watch for date changes from picker
watch(selectedDate, async (newVal) => {
  if (newVal) {
    await refreshData()
  }
})

onMounted(async () => {
  bsToday.value = getTodayBs()
  // Set today as default
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  selectedDate.value = `${year}-${month}-${day}`
  
  await refreshData()
})
</script>

<style scoped>
button, select, input {
  min-height: 44px;
}

.employee-card {
  transition: all 0.2s ease;
}

.employee-card:hover {
  transform: translateY(-2px);
}

.employee-card:active {
  transform: scale(0.98);
}

@media (max-width: 640px) {
  section {
    padding: 1rem !important;
  }
}
</style>

