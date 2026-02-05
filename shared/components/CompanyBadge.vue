<!-- CompanyBadge.vue - Visual company distinction badge -->
<!-- Now supports dynamic configuration from Company doctype -->
<template>
  <span 
    :class="[
      'inline-flex items-center justify-center rounded-full text-white font-bold',
      sizeClasses
    ]"
    :style="colorStyles"
    :title="companyTitle"
  >
    {{ badgeText }}
  </span>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  // Company name (required)
  company: {
    type: String,
    default: ''
  },
  // Optional: pre-loaded company config to avoid API call
  companyConfig: {
    type: Object,
    default: null
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg'
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

// Brand color configuration (matches Python BRAND_COLORS)
const BRAND_COLORS = {
  horlicks: { primary: '#0077B6', hover: '#005f92' },
  cocacola: { primary: '#F40009', hover: '#c50007' }
}
const DEFAULT_BRAND = 'cocacola'

// Local state for fetched company config
const fetchedConfig = ref(null)

// Get effective config (from prop or fetched)
const effectiveConfig = computed(() => {
  return props.companyConfig || fetchedConfig.value
})

// Check if company is horlicks-based (using main_product)
const isHorlicks = computed(() => {
  if (effectiveConfig.value) {
    return effectiveConfig.value.main_product === 'horlicks' || effectiveConfig.value.is_horlicks
  }
  // Fallback: no config available, return false
  return false
})

// Get badge text from company abbreviation or generate from name
const badgeText = computed(() => {
  // Use abbr from config if available
  if (effectiveConfig.value?.abbr) {
    return effectiveConfig.value.abbr
  }
  // Fallback: generate from company name (first letters of first 2 words)
  if (props.company) {
    const words = props.company.trim().split(/\s+/)
    if (words.length >= 2) {
      return (words[0][0] + words[1][0]).toUpperCase()
    }
    return props.company.substring(0, 2).toUpperCase()
  }
  return '??'
})

// Company title for tooltip
const companyTitle = computed(() => {
  if (effectiveConfig.value?.company_name) {
    return effectiveConfig.value.company_name
  }
  return props.company || 'Unknown Company'
})

// Get brand colors based on main_product
const brandColors = computed(() => {
  // Use colors from config if available
  if (effectiveConfig.value?.brand_colors) {
    return {
      primary: effectiveConfig.value.brand_colors.primary,
      hover: effectiveConfig.value.brand_colors.hover
    }
  }
  // Derive from main_product
  const mainProduct = effectiveConfig.value?.main_product || ''
  return BRAND_COLORS[mainProduct] || BRAND_COLORS[DEFAULT_BRAND]
})

// Color styles (using inline styles for dynamic colors)
const colorStyles = computed(() => {
  return {
    backgroundColor: brandColors.value.primary,
    '--hover-bg': brandColors.value.hover
  }
})

// Size classes
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

// Fetch company config if not provided
const fetchCompanyConfig = async () => {
  if (!props.company || props.companyConfig) return
  
  try {
    const response = await call('custom_erp.api.payment_reco.get_company_config', {
      company_name: props.company
    })
    if (response.success) {
      fetchedConfig.value = response.data
    }
  } catch (error) {
    console.error('Failed to fetch company config:', error)
  }
}

// Watch for company changes and fetch config
watch(() => props.company, () => {
  if (props.company && !props.companyConfig) {
    fetchCompanyConfig()
  }
}, { immediate: true })

onMounted(() => {
  if (props.company && !props.companyConfig) {
    fetchCompanyConfig()
  }
})
</script>

<style scoped>
span:hover {
  background-color: var(--hover-bg) !important;
}
</style>
