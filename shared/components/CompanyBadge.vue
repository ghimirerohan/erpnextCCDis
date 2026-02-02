<!-- CompanyBadge.vue - Visual company distinction badge -->
<template>
  <span 
    :class="[
      'inline-flex items-center justify-center rounded-full text-white font-bold',
      sizeClasses,
      colorClasses
    ]"
    :title="companyTitle"
  >
    {{ badgeText }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  company: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg'
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const isPadmashree = computed(() => {
  return props.company === 'PadmaShree Trade Link'
})

const badgeText = computed(() => {
  return isPadmashree.value ? 'PS' : 'RS'
})

const companyTitle = computed(() => {
  return isPadmashree.value ? 'PadmaShree Trade Link' : 'Riya Trades and Suppliers'
})

// Horlicks brand blue: #0077B6
// Coca-Cola brand red: #F40009
const colorClasses = computed(() => {
  return isPadmashree.value 
    ? 'bg-[#0077B6] hover:bg-[#005f92]' 
    : 'bg-[#F40009] hover:bg-[#c50007]'
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-5 h-5 text-[10px]'
    case 'lg':
      return 'w-8 h-8 text-sm'
    default:
      return 'w-6 h-6 text-xs'
  }
})
</script>
