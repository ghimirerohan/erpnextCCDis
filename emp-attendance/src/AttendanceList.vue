<template>
  <div class="min-h-screen font-sans bg-gray-50 text-gray-900 pb-12">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-gray-200 supports-[backdrop-filter]:bg-white/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- App Branding -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-600 shadow-lg shadow-emerald-600/20 text-white">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900 tracking-tight">Employee Attendance</h1>
              <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Dashboard</p>
            </div>
          </div>
          
          <!-- Logout Button -->
          <button
            @click="session.logout.submit()"
            class="group inline-flex items-center px-4 py-2 rounded-lg text-sm font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
          >
            <svg class="w-4 h-4 mr-2 text-gray-500 group-hover:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      <!-- Date & Actions Bar -->
      <section class="bg-white rounded-2xl shadow-sm border border-gray-200 p-1 flex flex-col md:flex-row gap-2">
        <!-- Date Display -->
        <div class="px-6 py-4 flex flex-col justify-center flex-1 border-b md:border-b-0 md:border-r border-gray-100">
          <div class="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-1">Selected Date</div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-gray-900 tracking-tight">{{ selectedDateBs || bsToday }}</span>
            <span class="text-sm font-bold text-gray-500">BS</span>
          </div>
          <div class="text-sm font-semibold text-gray-600 mt-1 flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            {{ selectedDate || adToday }} (AD)
          </div>
        </div>

        <!-- Controls -->
        <div class="flex-1 p-4 flex flex-col sm:flex-row items-center gap-4">
          <div class="w-full sm:flex-1 relative">
            <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5 ml-1">Change Date</label>
            <div class="relative">
               <NepaliDatePicker
                v-model="selectedDate"
                @update:modelValue="handleDateChange"
                placeholder="Select date (BS)"
                class="w-full font-medium"
              />
            </div>
          </div>
          
          <div class="flex w-full sm:w-auto gap-3 self-end">
             <button
              @click="refreshData"
              :disabled="loading"
              class="flex-1 sm:flex-none inline-flex items-center justify-center px-5 py-3 rounded-xl font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-all duration-200 active:scale-95 disabled:opacity-50 h-[50px] mt-auto border border-gray-200"
            >
              <svg :class="{'animate-spin': loading}" class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
            <button
              @click="syncAttendance"
              :disabled="syncing"
              class="flex-1 sm:flex-none inline-flex items-center justify-center px-6 py-3 rounded-xl font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-200 active:scale-95 disabled:opacity-70 h-[50px] mt-auto min-w-[140px]"
            >
              <svg v-if="syncing" class="animate-spin w-5 h-5 mr-2" style="color: rgba(101, 87, 52, 1);" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"/>
                <path d="M4 12a8 8 0 018-8" stroke-width="4" class="opacity-75"/>
              </svg>
              <svg v-else class="w-5 h-5 mr-2" style="color: rgba(101, 87, 52, 1);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <span style="color: var(--ink-gray-7);">{{ syncing ? 'Syncing...' : 'Sync Now' }}</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Stats Overview -->
      <section class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
        <!-- Total -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-gray-300 transition-colors">
          <div class="flex justify-between items-start">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Total Teams</span>
            <div class="p-1.5 bg-gray-50 rounded-lg text-gray-500">
               <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900">{{ summary.total || 0 }}</div>
        </div>

        <!-- Present (Attendance Marked) -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-emerald-300 transition-colors relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-emerald-100 transition-colors"></div>
          <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">Present</span>
            <div class="p-1.5 bg-emerald-100 rounded-lg text-emerald-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.present || 0 }}</div>
        </div>

        <!-- Checked In (Real-time - No attendance yet) -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-cyan-300 transition-colors relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-24 h-24 bg-cyan-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-cyan-100 transition-colors"></div>
          <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-cyan-700 uppercase tracking-wider">Checked In</span>
            <div class="p-1.5 bg-cyan-100 rounded-lg text-cyan-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.checked_in || 0 }}</div>
        </div>

        <!-- Absent -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-red-300 transition-colors relative overflow-hidden group">
           <div class="absolute right-0 top-0 w-24 h-24 bg-red-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-red-100 transition-colors"></div>
           <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-red-700 uppercase tracking-wider">Absent</span>
             <div class="p-1.5 bg-red-100 rounded-lg text-red-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.absent || 0 }}</div>
        </div>

        <!-- On Time -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-blue-300 transition-colors relative overflow-hidden group">
           <div class="absolute right-0 top-0 w-24 h-24 bg-blue-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-blue-100 transition-colors"></div>
           <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-blue-700 uppercase tracking-wider">On Time</span>
            <div class="p-1.5 bg-blue-100 rounded-lg text-blue-700">
               <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.on_time_entry || 0 }}</div>
        </div>

        <!-- Late Entry -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-amber-300 transition-colors relative overflow-hidden group">
           <div class="absolute right-0 top-0 w-24 h-24 bg-amber-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-amber-100 transition-colors"></div>
           <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-amber-700 uppercase tracking-wider">Late Entry</span>
            <div class="p-1.5 bg-amber-100 rounded-lg text-amber-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.late_entry || 0 }}</div>
        </div>

        <!-- Early Exit -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between h-32 hover:border-purple-300 transition-colors relative overflow-hidden group">
           <div class="absolute right-0 top-0 w-24 h-24 bg-purple-50 rounded-bl-full -mr-4 -mt-4 z-0 group-hover:bg-purple-100 transition-colors"></div>
           <div class="flex justify-between items-start relative z-10">
            <span class="text-xs font-bold text-purple-700 uppercase tracking-wider">Early Exit</span>
            <div class="p-1.5 bg-purple-100 rounded-lg text-purple-700">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7"></path></svg>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 relative z-10">{{ summary.early_exit || 0 }}</div>
        </div>
      </section>

      <!-- Employee List -->
      <section>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 tracking-tight">Attendance List</h2>
             <p class="text-sm font-medium text-gray-500 mt-1">Real-time attendance status for all employees</p>
          </div>
          <div class="mt-4 sm:mt-0 flex items-center space-x-2 text-xs font-bold text-gray-500 bg-white px-3 py-2 rounded-lg border border-gray-200 shadow-sm uppercase tracking-wide">
            <span class="text-gray-900 text-sm">{{ employees.length }}</span>
            <span>Employees found</span>
          </div>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-24 bg-white rounded-3xl border border-gray-200 shadow-sm">
          <div class="relative w-16 h-16">
            <div class="absolute top-0 left-0 w-full h-full border-4 border-gray-100 rounded-full"></div>
            <div class="absolute top-0 left-0 w-full h-full border-4 border-emerald-500 rounded-full border-t-transparent animate-spin"></div>
          </div>
          <p class="mt-6 text-gray-500 font-medium animate-pulse">Fetching attendance data...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="!employees.length" class="flex flex-col items-center justify-center py-24 bg-white rounded-3xl border border-gray-200 shadow-sm">
          <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-6">
            <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900">No Records Found</h3>
          <p class="text-gray-500 mt-2 text-center max-w-xs font-medium">There are no attendance records available for <br> <span class="font-bold text-gray-800">{{ selectedDateBs || bsToday }}</span></p>
          <button @click="selectedDate = null; refreshData()" class="mt-6 px-6 py-2.5 text-sm font-bold text-emerald-700 bg-emerald-50 rounded-xl hover:bg-emerald-100 transition-colors">
            Reset to Today
          </button>
        </div>
        
        <!-- Employee Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="emp in employees"
            :key="emp.employee"
            @click="viewEmployeeHistory(emp)"
            class="group rounded-2xl border shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col relative overflow-hidden bg-white"
            :class="emp.status === 'Present' ? 'border-emerald-200' : 'border-gray-200'"
          >
            <!-- Card Header (Colored based on status) -->
            <div 
              class="px-6 py-4 border-b flex items-center justify-between"
              :class="{
                'present-card-header border-emerald-200': emp.status?.toLowerCase() === 'present',
                'bg-cyan-50 border-cyan-100': emp.status?.toLowerCase() === 'checked in',
                'bg-red-50 border-red-100': emp.status?.toLowerCase() === 'absent',
                'bg-amber-50 border-amber-100': emp.status?.toLowerCase() === 'half day',
                'bg-blue-50 border-blue-100': emp.status?.toLowerCase() === 'on leave',
                'bg-gray-50 border-gray-100': !emp.status
              }"
            >
              <div class="flex items-center space-x-3">
                 <div 
                  class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-sm"
                  :style="{ background: getAvatarGradient(emp) }"
                >
                  {{ getInitials(emp.employee_name) }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-gray-900 leading-snug">{{ emp.employee_name }}</h3>
                  <div class="text-[10px] font-semibold text-gray-500 tracking-wide">{{ emp.employee }}</div>
                </div>
              </div>
              
              <span 
                class="inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-wider border shadow-sm"
                :class="getStatusBadgeClass(emp.status)"
              >
                {{ emp.status || 'Unknown' }}
              </span>
            </div>

            <!-- Card Body -->
            <div class="p-6">
              <!-- Time Cards -->
              <div class="grid grid-cols-2 gap-4">
                <!-- Check In -->
                <div class="rounded-xl p-3 border transition-colors bg-gray-50/50 border-gray-100" 
                    :class="{'!bg-white !border-gray-200 shadow-sm': emp.in_time}">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Check In</span>
                    <div v-if="emp.late_entry" class="text-[9px] font-black text-amber-600 bg-amber-100 px-1.5 py-0.5 rounded uppercase tracking-wide">Late</div>
                  </div>
                  <div class="flex items-baseline space-x-1">
                     <div class="text-lg font-extrabold" :class="emp.in_time ? (emp.late_entry ? 'text-amber-600' : 'text-gray-900') : 'text-gray-300'">
                      {{ emp.in_time ? formatTime12Hour(emp.in_time) : '-- : --' }}
                    </div>
                  </div>
                </div>

                <!-- Check Out -->
                <div class="rounded-xl p-3 border transition-colors bg-gray-50/50 border-gray-100"
                     :class="{'!bg-white !border-gray-200 shadow-sm': emp.out_time}">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Check Out</span>
                    <div v-if="emp.early_exit" class="text-[9px] font-black text-purple-600 bg-purple-100 px-1.5 py-0.5 rounded uppercase tracking-wide">Early</div>
                  </div>
                   <div class="flex items-baseline space-x-1">
                     <div class="text-lg font-extrabold" :class="emp.out_time ? (emp.early_exit ? 'text-purple-600' : 'text-gray-900') : 'text-gray-300'">
                      {{ emp.out_time ? formatTime12Hour(emp.out_time) : '-- : --' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="mx-6 mb-4 pt-4 border-t border-dashed border-gray-200 flex items-center justify-center">
              <span class="text-xs text-emerald-600 font-bold group-hover:underline decoration-2 underline-offset-4 transition-all uppercase tracking-wide flex items-center">
                View History
                <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </span>
            </div>

          </div>
        </div>
      </section>
    </main>
    
    <!-- Sync Result Dialog -->
    <Dialog v-model="showSyncDialog" :dismissable="true">
      <template #body>
        <div class="p-8 text-center max-w-sm mx-auto bg-white rounded-3xl">
          <div class="w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center shadow-lg transform rotate-3" 
               :class="syncResult.success ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600'">
            <svg v-if="syncResult.success" class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ syncResult.title }}</h3>
          <p class="text-gray-500 mb-8 leading-relaxed font-medium">{{ syncResult.message }}</p>
          
          <div v-if="syncResult.processed > 0" class="bg-gray-50 rounded-2xl p-5 mb-8 border border-gray-100">
            <div class="text-4xl font-black text-emerald-600">{{ syncResult.processed }}</div>
            <div class="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Records Processed</div>
          </div>
          
          <button 
            @click="showSyncDialog = false"
            class="w-full py-4 px-6 rounded-xl font-bold text-white bg-gray-900 hover:bg-gray-800 transition-all duration-200 shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
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
  checked_in: 0,  // Real-time check-ins before attendance is marked
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
    'linear-gradient(135deg, #10b981 0%, #059669 100%)', // Emerald
    'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', // Blue
    'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)', // Violet
    'linear-gradient(135deg, #ec4899 0%, #db2777 100%)', // Pink
    'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', // Amber
    'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', // Cyan
  ]
  // Use a hash of employee name to keep it consistent
  let hash = 0;
  if(emp.employee_name) {
    for (let i = 0; i < emp.employee_name.length; i++) {
        hash = emp.employee_name.charCodeAt(i) + ((hash << 5) - hash);
    }
  }
  const index = Math.abs(hash) % colors.length
  return colors[index]
}

const getStatusBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'present') {
    return 'present-badge'
  } else if (s === 'checked in') {
    return 'bg-cyan-100 text-cyan-800 border-cyan-200'  // Real-time check-in status
  } else if (s === 'absent') {
    return 'bg-red-100 text-red-800 border-red-200'
  } else if (s === 'half day') {
    return 'bg-amber-100 text-amber-800 border-amber-200'
  } else if (s === 'on leave') {
    return 'bg-blue-100 text-blue-800 border-blue-200'
  }
  return 'bg-gray-100 text-gray-800 border-gray-200'
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
    await attendanceResource.fetch({
      date: dateToFetch,
    })
    
    // createResource stores the response in .data property
    const res = attendanceResource.data
    
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
      // Small delay to let the animation play
      setTimeout(async () => {
        if (res.processed === 0) {
          syncResult.value = {
            success: true,
            title: 'All Caught Up',
            message: res.message || 'No new check-ins found to process.',
            processed: 0
          }
        } else {
          syncResult.value = {
            success: true,
            title: 'Sync Successful',
            message: res.message || 'Attendance records have been updated.',
            processed: res.processed || 0
          }
          await refreshData()
        }
        showSyncDialog.value = true
      }, 500)
    } else {
        syncResult.value = {
        success: false,
        title: 'Sync Failed',
        message: res?.message || 'Unable to sync data at this time.',
        processed: 0
      }
      showSyncDialog.value = true
    }
  } catch (error) {
    console.error('Failed to sync attendance:', error)
    syncResult.value = {
      success: false,
      title: 'Connection Error',
      message: 'Could not connect to the server. Please check your internet.',
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

watch(selectedDate, async (newVal) => {
  if (newVal) {
    await refreshData()
  }
})

onMounted(async () => {
  bsToday.value = getTodayBs()
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
  min-height: 48px;
}

.present-badge {
  background-color: rgba(203, 231, 207, 1);
  color: rgba(48, 104, 44, 1);
  border-color: rgba(78, 194, 46, 1);
}

.present-card-header {
  background-color: rgba(195, 234, 221, 1);
  background-image: none;
}
</style>
