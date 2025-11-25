<!-- ADDED BY AI: UPLOAD_SALES -->
<template>
  <section class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
    <div class="flex items-center mb-6">
      <div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3">
        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900">Select Driver & Vehicle</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Driver Selection -->
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">
          Driver <span class="text-red-500">*</span>
        </label>

        <select
          :value="driverValue"
          @change="$emit('update:driverValue', $event.target.value)"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white"
          :disabled="loadingDrivers"
        >
          <option value="">{{ loadingDrivers ? 'Loading drivers...' : 'Select a driver' }}</option>
          <option
            v-for="driver in drivers"
            :key="driver.name"
            :value="driver.name"
          >
            {{ driver.employee_name || driver.name }}
          </option>
        </select>

        <p class="mt-2 text-sm text-gray-500">
          Required: Driver for delivery
        </p>
      </div>

      <!-- Vehicle Selection -->
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">
          Vehicle <span class="text-gray-400">(Optional)</span>
        </label>

        <select
          :value="vehicleValue"
          @change="$emit('update:vehicleValue', $event.target.value)"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white"
          :disabled="loadingVehicles"
        >
          <option value="">{{ loadingVehicles ? 'Loading vehicles...' : 'Select a vehicle (optional)' }}</option>
          <option
            v-for="vehicle in vehicles"
            :key="vehicle.name"
            :value="vehicle.name"
          >
            {{ vehicle.license_plate ? `${vehicle.name} (${vehicle.license_plate})` : vehicle.name }}
          </option>
        </select>

        <p class="mt-2 text-sm text-gray-500">
          Optional: Vehicle for delivery
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
// ADDED BY AI: UPLOAD_SALES
defineProps({
  driverValue: {
    type: String,
    default: null
  },
  vehicleValue: {
    type: String,
    default: null
  },
  drivers: {
    type: Array,
    default: () => []
  },
  vehicles: {
    type: Array,
    default: () => []
  },
  loadingDrivers: {
    type: Boolean,
    default: false
  },
  loadingVehicles: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:driverValue', 'update:vehicleValue'])
</script>

