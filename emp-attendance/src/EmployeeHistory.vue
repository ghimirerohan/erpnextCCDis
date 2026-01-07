<template>
  <div class="min-h-screen font-sans bg-gray-50 text-gray-900 pb-12">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200 supports-[backdrop-filter]:bg-white/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Back Button & Title -->
          <div class="flex items-center space-x-4">
            <button 
              @click="goBack"
              class="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
            >
              <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <div>
              <h1 class="text-xl font-bold text-gray-900 tracking-tight">Attendance History</h1>
              <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Employee Details</p>
            </div>
          </div>
          
          <!-- Refresh Button -->
          <button
            @click="refreshData"
            :disabled="loading"
            class="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
          >
            <svg :class="{'animate-spin': loading}" class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      <!-- Employee Profile Card -->
      <section class="bg-white rounded-3xl shadow-sm border border-gray-200 p-6 flex flex-col sm:flex-row items-center sm:items-start gap-8 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-emerald-50 rounded-full -mr-32 -mt-32 blur-3xl opacity-50 pointer-events-none"></div>
        
        <div 
          class="w-24 h-24 rounded-2xl flex-shrink-0 flex items-center justify-center text-white font-bold text-3xl shadow-lg relative z-10"
          style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);"
        >
          {{ getInitials(employeeInfo?.employee_name) }}
        </div>
        
        <div class="flex-1 text-center sm:text-left min-w-0 relative z-10">
          <h2 class="text-3xl font-extrabold text-gray-900 truncate tracking-tight">{{ employeeInfo?.employee_name || 'Loading...' }}</h2>
          <div class="flex items-center justify-center sm:justify-start gap-3 mt-2 text-gray-500">
            <span class="bg-gray-100 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide text-gray-600">{{ employeeId }}</span>
            <span v-if="employeeInfo?.designation" class="flex items-center gap-1 text-sm font-semibold">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              {{ employeeInfo.designation }}
            </span>
          </div>
        </div>
        
        <!-- Period Selector -->
        <div class="flex w-full sm:w-auto bg-gray-100 p-1.5 rounded-xl relative z-10 self-center sm:self-start mt-4 sm:mt-0">
          <button
            @click="selectPeriod(7)"
            :class="selectedPeriod === 7 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-500 hover:text-gray-900'"
            class="flex-1 sm:flex-none py-2 px-6 rounded-lg text-sm font-bold transition-all duration-200"
          >
            Last 7 Days
          </button>
          <button
            @click="selectPeriod(30)"
             :class="selectedPeriod === 30 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-500 hover:text-gray-900'"
            class="flex-1 sm:flex-none py-2 px-6 rounded-lg text-sm font-bold transition-all duration-200"
          >
            Last 30 Days
          </button>
        </div>
      </section>
      
      <!-- Stats Summary -->
      <section class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Present Days -->
        <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:border-emerald-300 transition-all group">
          <div class="flex items-center justify-between mb-4">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Present</span>
            <div class="w-9 h-9 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:bg-emerald-100 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-gray-900">{{ historySummary.present || 0 }}</span>
            <span class="text-sm font-bold text-gray-500">days</span>
          </div>
        </div>
        
        <!-- Absent Days -->
        <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:border-red-300 transition-all group">
          <div class="flex items-center justify-between mb-4">
             <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Absent</span>
            <div class="w-9 h-9 rounded-xl bg-red-50 flex items-center justify-center text-red-600 group-hover:bg-red-100 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </div>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-gray-900">{{ historySummary.absent || 0 }}</span>
            <span class="text-sm font-bold text-gray-500">days</span>
          </div>
        </div>
        
        <!-- Late Entries -->
        <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:border-amber-300 transition-all group">
          <div class="flex items-center justify-between mb-4">
             <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Late Arrivals</span>
            <div class="w-9 h-9 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600 group-hover:bg-amber-100 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-gray-900">{{ historySummary.late_entries || 0 }}</span>
            <span class="text-sm font-bold text-gray-500">times</span>
          </div>
        </div>
        
        <!-- Early Exits -->
        <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:border-purple-300 transition-all group">
          <div class="flex items-center justify-between mb-4">
             <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Early Exits</span>
            <div class="w-9 h-9 rounded-xl bg-purple-50 flex items-center justify-center text-purple-600 group-hover:bg-purple-100 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7"></path></svg>
            </div>
          </div>
          <div class="flex items-baseline gap-1">
             <span class="text-3xl font-extrabold text-gray-900">{{ historySummary.early_exits || 0 }}</span>
            <span class="text-sm font-bold text-gray-500">times</span>
          </div>
        </div>
      </section>

      <!-- History List -->
      <section class="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-200 flex items-center justify-between bg-gray-50/50">
          <div>
            <h2 class="text-lg font-bold text-gray-900">Recent Activity</h2>
             <p class="text-sm font-medium text-gray-500">Log of daily attendance</p>
          </div>
          <span class="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-600 uppercase tracking-widest shadow-sm">{{ historyData.length }} RECORDS</span>
        </div>
        
        <!-- Loading -->
        <div v-if="loading" class="py-24 flex flex-col items-center">
          <div class="animate-spin rounded-full h-10 w-10 border-4 border-gray-100 border-t-emerald-500"></div>
           <p class="mt-4 text-gray-500 text-sm font-bold animate-pulse">Loading history...</p>
        </div>
        
        <!-- Empty -->
        <div v-else-if="!historyData.length" class="py-24 flex flex-col items-center text-center">
          <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          </div>
          <p class="text-gray-900 font-bold mb-1">No Attendance Records</p>
          <p class="text-gray-500 text-sm font-medium">No data found for the selected period</p>
        </div>
        
        <!-- List -->
        <div v-else class="divide-y divide-gray-100">
          <div
            v-for="record in historyData"
            :key="record.date"
            class="p-5 hover:bg-gray-50 transition-colors flex flex-col sm:flex-row gap-5 sm:items-center group"
          >
            <!-- Date Badge -->
            <div class="flex-shrink-0 flex items-center gap-5 sm:w-56">
              <div 
                class="w-16 h-16 rounded-2xl flex flex-col items-center justify-center flex-shrink-0 shadow-sm text-center border transition-colors"
                :class="getDateBadgeClass(record.status)"
              >
                <span class="text-[10px] uppercase font-bold tracking-wider opacity-90">{{ getDayName(record.date) }}</span>
                <span class="text-2xl font-black leading-none my-0.5">{{ getDay(record.date_bs) }}</span>
                <span class="text-[10px] uppercase font-bold tracking-wider opacity-90">{{ getMonthYear(record.date_bs) }}</span>
              </div>
              <div class="min-w-0">
                <div class="font-bold text-gray-900 text-lg">{{ record.date_bs }}</div>
                <div class="text-xs font-semibold text-gray-500 mt-0.5 flex items-center gap-1.5">
                  <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                  {{ record.date }}
                </div>
              </div>
            </div>
            
            <!-- Status Pill -->
            <div class="flex-shrink-0 sm:w-32">
               <span 
                class="inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wide border"
                :class="getStatusBadgeClass(record.status)"
              >
                <span class="w-2 h-2 rounded-full mr-2" :class="getStatusDotClass(record.status)"></span>
                {{ record.status || 'Unknown' }}
              </span>
            </div>
            
            <!-- Timing -->
            <div class="flex-1 grid grid-cols-2 gap-4">
              <div class="bg-gray-50 rounded-xl px-4 py-2.5 border border-transparent group-hover:border-gray-200 transition-colors flex items-center justify-between">
                <div>
                  <div class="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-0.5">In Time</div>
                  <div class="text-base font-bold text-gray-900" :class="{'text-amber-600': record.late_entry}">
                    {{ record.in_time ? formatTime12Hour(record.in_time) : '--:--' }}
                  </div>
                </div>
                 <div v-if="record.late_entry" class="text-[10px] font-bold text-amber-600 bg-amber-100 px-2 py-0.5 rounded uppercase tracking-wide border border-amber-200">Late</div>
              </div>
              
               <div class="bg-gray-50 rounded-xl px-4 py-2.5 border border-transparent group-hover:border-gray-200 transition-colors flex items-center justify-between">
                <div>
                   <div class="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-0.5">Out Time</div>
                  <div class="text-base font-bold text-gray-900" :class="{'text-purple-600': record.early_exit}">
                    {{ record.out_time ? formatTime12Hour(record.out_time) : '--:--' }}
                  </div>
                </div>
                 <div v-if="record.early_exit" class="text-[10px] font-bold text-purple-600 bg-purple-100 px-2 py-0.5 rounded uppercase tracking-wide border border-purple-200">Early</div>
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

const getDateBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'present') {
    return 'present-date-badge shadow-md'
  } else if (s === 'absent') {
    return 'bg-red-500 text-white border-red-500 shadow-md'
  } else if (s === 'half day') {
    return 'bg-amber-500 text-white border-amber-500 shadow-md'
  } else if (s === 'on leave') {
    return 'bg-blue-500 text-white border-blue-500 shadow-md'
  }
  return 'bg-gray-100 text-gray-500 border-gray-200'
}

const getStatusBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'present') {
    return 'present-badge'
  } else if (s === 'absent') {
    return 'bg-red-100 text-red-800 border-red-200'
  } else if (s === 'half day') {
    return 'bg-amber-100 text-amber-800 border-amber-200'
  } else if (s === 'on leave') {
    return 'bg-blue-100 text-blue-800 border-blue-200'
  }
  return 'bg-gray-100 text-gray-600 border-gray-200'
}

const getStatusDotClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'present') {
    return 'present-dot'
  } else if (s === 'absent') {
    return 'bg-red-500'
  } else if (s === 'half day') {
    return 'bg-amber-500'
  } else if (s === 'on leave') {
    return 'bg-blue-500'
  }
  return 'bg-gray-400'
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
  min-height: 48px;
}

.present-badge {
  background-color: rgba(203, 231, 207, 1);
  color: rgba(48, 104, 44, 1);
  border-color: rgba(78, 194, 46, 1);
}

.present-date-badge {
  background-color: rgba(69, 161, 75, 1);
  color: rgba(255, 255, 255, 1);
  border-color: rgba(69, 161, 75, 1);
}

.present-dot {
  background-color: rgba(25, 204, 37, 1);
}
</style>
