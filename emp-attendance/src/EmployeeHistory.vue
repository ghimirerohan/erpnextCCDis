<template>
  <div class="min-h-screen" style="background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 50%, #ffffff 100%);">
    <!-- Header -->
    <header class="sticky top-0 z-20 bg-white border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Back Button & Title -->
          <div class="flex items-center space-x-3">
            <button 
              @click="goBack"
              class="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center hover:bg-gray-200 transition-all"
            >
              <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <div>
              <h1 class="text-lg sm:text-xl font-bold text-gray-900">Attendance History</h1>
              <p class="text-xs sm:text-sm text-gray-500">{{ employeeInfo?.employee_name || 'Loading...' }}</p>
            </div>
          </div>
          
          <!-- Refresh Button -->
          <button
            @click="refreshData"
            :disabled="loading"
            class="inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:outline-none transition-all"
          >
            <svg v-if="loading" class="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
              <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      
      <!-- Employee Info Card -->
      <section class="bg-white rounded-2xl shadow-lg p-4 sm:p-6 border border-gray-100">
        <div class="flex items-center gap-4">
          <div 
            class="w-16 h-16 sm:w-20 sm:h-20 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold text-xl sm:text-2xl"
            style="background: linear-gradient(135deg, #059669 0%, #047857 100%);"
          >
            {{ getInitials(employeeInfo?.employee_name) }}
          </div>
          <div class="flex-1 min-w-0">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 truncate">{{ employeeInfo?.employee_name || 'Loading...' }}</h2>
            <p class="text-sm text-gray-500">{{ employeeId }}</p>
            <p v-if="employeeInfo?.designation" class="text-xs text-gray-400 mt-1">{{ employeeInfo.designation }}</p>
          </div>
        </div>
      </section>
      
      <!-- Period Selector -->
      <section class="bg-white rounded-2xl shadow-lg p-4 sm:p-6 border border-gray-100">
        <label class="block text-sm font-semibold text-gray-700 mb-3">Select Period</label>
        <div class="flex gap-3">
          <button
            @click="selectPeriod(7)"
            :class="selectedPeriod === 7 
              ? 'bg-emerald-600 text-white border-emerald-600 shadow-md' 
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
            class="flex-1 py-3 px-4 rounded-xl text-sm font-semibold border-2 transition-all"
          >
            Last 7 Days
          </button>
          <button
            @click="selectPeriod(30)"
            :class="selectedPeriod === 30 
              ? 'bg-emerald-600 text-white border-emerald-600 shadow-md' 
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
            class="flex-1 py-3 px-4 rounded-xl text-sm font-semibold border-2 transition-all"
          >
            Last 30 Days
          </button>
        </div>
      </section>
      
      <!-- Summary Cards -->
      <section class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <!-- Present Days -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border: 1px solid #6ee7b7;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-emerald-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-emerald-700 font-medium">Present</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-emerald-800">{{ historySummary.present || 0 }}</div>
          <div class="text-xs text-emerald-600 mt-1">days</div>
        </div>
        
        <!-- Absent Days -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border: 1px solid #fca5a5;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-red-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-red-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-red-700 font-medium">Absent</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-red-800">{{ historySummary.absent || 0 }}</div>
          <div class="text-xs text-red-600 mt-1">days</div>
        </div>
        
        <!-- Late Entries -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 1px solid #fcd34d;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-amber-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-amber-700 font-medium">Late</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-amber-800">{{ historySummary.late_entries || 0 }}</div>
          <div class="text-xs text-amber-600 mt-1">entries</div>
        </div>
        
        <!-- Early Exits -->
        <div class="rounded-xl shadow-md p-4" style="background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); border: 1px solid #f9a8d4;">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-pink-200 flex items-center justify-center">
              <svg class="w-4 h-4 text-pink-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7"></path>
              </svg>
            </div>
            <span class="text-xs sm:text-sm text-pink-700 font-medium">Early Exit</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-pink-800">{{ historySummary.early_exits || 0 }}</div>
          <div class="text-xs text-pink-600 mt-1">exits</div>
        </div>
      </section>

      <!-- Attendance History List -->
      <section class="bg-white rounded-2xl shadow-lg p-4 sm:p-6 border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-gray-900">Attendance Records</h2>
          <span class="text-sm text-gray-500">{{ historyData.length }} records</span>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 mx-auto border-b-2 border-emerald-600"></div>
          <p class="mt-4 text-gray-500">Loading history...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="!historyData.length" class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="mt-4 text-gray-500 text-lg">No attendance records found</p>
          <p class="text-sm text-gray-400">for the selected period</p>
        </div>
        
        <!-- History Cards -->
        <div v-else class="space-y-2.5">
          <div
            v-for="record in historyData"
            :key="record.date"
            class="rounded-xl p-3 border-2 transition-all"
            :class="getRecordCardClass(record)"
          >
            <div class="flex items-start justify-between gap-3">
              <!-- Date Column -->
              <div class="flex-shrink-0">
                <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-xl flex flex-col items-center justify-center"
                     :class="record.status === 'Present' ? 'bg-emerald-500' : record.status === 'Absent' ? 'bg-red-200' : 'bg-gray-100'">
                  <div class="text-xs text-white uppercase font-semibold" 
                       :class="record.status === 'Present' ? 'text-white' : record.status === 'Absent' ? 'text-red-700' : 'text-gray-500'">
                    {{ getDayName(record.date) }}
                  </div>
                  <div class="text-lg sm:text-xl font-bold" 
                       :class="record.status === 'Present' ? 'text-white' : record.status === 'Absent' ? 'text-red-800' : 'text-gray-700'">
                    {{ getDay(record.date_bs) }}
                  </div>
                  <div class="text-xs" 
                       :class="record.status === 'Present' ? 'text-emerald-100' : record.status === 'Absent' ? 'text-red-600' : 'text-gray-500'">
                    {{ getMonthYear(record.date_bs) }}
                  </div>
                </div>
              </div>
              
              <!-- Details Column -->
              <div class="flex-1 min-w-0">
                <!-- Nepali Date Large -->
                <div class="font-bold text-gray-900 text-base mb-0.5">{{ record.date_bs }}</div>
                <div class="text-xs text-gray-500 mb-1.5">({{ record.date }})</div>
                
                <!-- Status Badge -->
                <span 
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold mb-2"
                  :class="getStatusBadgeClass(record.status)"
                >
                  {{ record.status || 'Unknown' }}
                </span>
                
                <!-- Time Info -->
                <div class="grid grid-cols-2 gap-2">
                  <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-lg p-2 border border-emerald-200">
                    <div class="flex items-center gap-1 mb-0.5">
                      <svg class="w-3 h-3 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14"></path>
                      </svg>
                      <span class="text-xs text-emerald-700 font-semibold">In</span>
                    </div>
                    <div class="text-sm font-bold" :class="record.late_entry ? 'text-amber-700' : 'text-emerald-800'">
                      {{ formatTime12Hour(record.in_time) }}
                    </div>
                  </div>
                  <div class="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-2 border border-red-200">
                    <div class="flex items-center gap-1 mb-0.5">
                      <svg class="w-3 h-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7"></path>
                      </svg>
                      <span class="text-xs text-red-700 font-semibold">Out</span>
                    </div>
                    <div class="text-sm font-bold" :class="record.early_exit ? 'text-pink-700' : 'text-red-800'">
                      {{ formatTime12Hour(record.out_time) }}
                    </div>
                  </div>
                </div>
                
                <!-- Flags -->
                <div v-if="record.late_entry || record.early_exit" class="flex gap-1.5 flex-wrap mt-2">
                  <span v-if="record.late_entry" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-700 border border-amber-300">
                    <svg class="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3"></path>
                    </svg>
                    Late
                  </span>
                  <span v-if="record.early_exit" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-pink-100 text-pink-700 border border-pink-300">
                    <svg class="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4"></path>
                    </svg>
                    Early
                  </span>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { createResource } from 'frappe-ui'
import { adToBs, formatTime12Hour } from '../../shared/utils/nepaliDate'

const props = defineProps({
  employeeId: {
    type: String,
    required: true
  }
})

const router = useRouter()

// State
const loading = ref(false)
const selectedPeriod = ref(7)
const employeeInfo = ref(null)
const historyData = ref([])
const historySummary = ref({
  present: 0,
  absent: 0,
  late_entries: 0,
  early_exits: 0,
})

// API Resource
const historyResource = createResource({
  url: 'custom_erp.api.emp_attendance.get_employee_history',
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

const goBack = () => {
  router.back()
}

const selectPeriod = async (days) => {
  selectedPeriod.value = days
  await refreshData()
}

const getRecordCardClass = (record) => {
  if (record.status === 'Present') {
    return 'border-emerald-400 bg-gradient-to-br from-emerald-100 to-emerald-50 shadow-emerald-100'
  } else if (record.status === 'Absent') {
    return 'border-red-200 bg-gradient-to-br from-red-50 to-white'
  } else if (record.status === 'Half Day') {
    return 'border-amber-200 bg-gradient-to-br from-amber-50 to-white'
  } else if (record.status === 'On Leave') {
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

const getDayName = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', { weekday: 'short' })
  } catch {
    return ''
  }
}

const getDay = (bsDateStr) => {
  if (!bsDateStr) return ''
  const parts = bsDateStr.split('-')
  return parts[2] || ''
}

const getMonthYear = (bsDateStr) => {
  if (!bsDateStr) return ''
  const months = ['Bai', 'Jes', 'Ash', 'Shr', 'Bha', 'Asw', 'Kar', 'Man', 'Pou', 'Mag', 'Fal', 'Cha']
  const parts = bsDateStr.split('-')
  if (parts.length >= 2) {
    const monthNum = parseInt(parts[1]) - 1
    return months[monthNum] || ''
  }
  return ''
}

const refreshData = async () => {
  loading.value = true
  try {
    const res = await historyResource.fetch({
      employee: props.employeeId,
      days: selectedPeriod.value,
    })
    
    if (res?.success) {
      employeeInfo.value = res.employee_info || null
      historyData.value = res.data || []
      historySummary.value = res.summary || historySummary.value
    } else if (res?.data) {
      employeeInfo.value = res.employee_info || null
      historyData.value = res.data || []
      historySummary.value = res.summary || historySummary.value
    }
  } catch (error) {
    console.error('Failed to fetch employee history:', error)
    historyData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
button, select, input {
  min-height: 44px;
}

@media (max-width: 640px) {
  section {
    padding: 1rem !important;
  }
}
</style>

