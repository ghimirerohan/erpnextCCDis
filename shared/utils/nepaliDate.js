// Nepali Date Conversion Utilities
// Using nepali-date-converter library for accuracy
import NepaliDate from 'nepali-date-converter'

/**
 * Convert BS (Bikram Sambat) date to AD (Gregorian) date
 * @param {string} bsDateStr - Date in YYYY-MM-DD format (BS)
 * @returns {string} Date in YYYY-MM-DD format (AD)
 */
export function bsToAd(bsDateStr) {
  console.log('nepaliDate: bsToAd called with', bsDateStr);
  if (!bsDateStr) return ''
  
  try {
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const bsObj = window.NepaliFunctions.ParseDate(bsDateStr)
      if (bsObj && bsObj.parsedDate) {
        const adObj = window.NepaliFunctions.BS2AD(bsObj.parsedDate)
        const result = `${adObj.year}-${String(adObj.month).padStart(2, '0')}-${String(adObj.day).padStart(2, '0')}`
        console.log('nepaliDate: bsToAd result (via NepaliFunctions)', result);
        return result
      }
    }
    const [year, month, day] = bsDateStr.split(/[-/]/).map(Number)
    const nd = new NepaliDate(year, month - 1, day)
    const adDate = nd.toJsDate()
    
    const adYear = adDate.getFullYear()
    const adMonth = String(adDate.getMonth() + 1).padStart(2, '0')
    const adDay = String(adDate.getDate()).padStart(2, '0')
    
    const result = `${adYear}-${adMonth}-${adDay}`
    console.log('nepaliDate: bsToAd result (via nepali-date-converter)', result);
    return result
  } catch (e) {
    console.error('BS to AD conversion failed:', e, bsDateStr)
    return ''
  }
}

/**
 * Convert AD (Gregorian) date to BS (Bikram Sambat) date
 * @param {string} adDateStr - Date in YYYY-MM-DD format (AD)
 * @returns {string} Date in YYYY-MM-DD format (BS)
 */
export function adToBs(adDateStr) {
  console.log('nepaliDate: adToBs called with', adDateStr);
  if (!adDateStr) return ''
  
  try {
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const adObj = window.NepaliFunctions.ParseDate(adDateStr)
      if (adObj && adObj.parsedDate) {
        const bsObj = window.NepaliFunctions.AD2BS(adObj.parsedDate)
        const result = `${bsObj.year}-${String(bsObj.month).padStart(2, '0')}-${String(bsObj.day).padStart(2, '0')}`
        console.log('nepaliDate: adToBs result (via NepaliFunctions)', result);
        return result
      }
    }
    const adDate = new Date(adDateStr)
    const nd = new NepaliDate(adDate)
    const result = nd.format('YYYY-MM-DD')
    console.log('nepaliDate: adToBs result (via nepali-date-converter)', result);
    return result
  } catch (e) {
    console.error('AD to BS conversion failed:', e, adDateStr)
    return ''
  }
}

/**
 * Get today's date in BS format
 * @returns {string} Today's date in YYYY-MM-DD format (BS)
 */
export function getTodayBs() {
  try {
    if (typeof window !== 'undefined' && window.NepaliFunctions) {
      const d = new Date()
      const bs = window.NepaliFunctions.AD2BS({ year: d.getFullYear(), month: d.getMonth() + 1, day: d.getDate() })
      return `${bs.year}-${String(bs.month).padStart(2, '0')}-${String(bs.day).padStart(2, '0')}`
    }
    const nd = new NepaliDate()
    return nd.format('YYYY-MM-DD')
  } catch (e) {
    console.error('Get Today BS failed:', e)
    // Fallback if library fails
    const today = new Date()
    return `${today.getFullYear() + 57}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
  }
}

/**
 * Format BS date for display
 * @param {string} bsDateStr - Date in YYYY-MM-DD format (BS)
 * @returns {string} Formatted date
 */
export function formatBsDate(bsDateStr) {
  if (!bsDateStr) return ''
  
  try {
     const [year, month, day] = bsDateStr.split(/[-/]/).map(Number)
     const months = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']
     if (month >= 1 && month <= 12) {
         return `${day} ${months[month - 1]} ${year}`
     }
     return bsDateStr
  } catch (e) {
      return bsDateStr
  }
}

// Nepali month names
export const nepaliMonths = [
  'Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
  'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra'
]

// Export all functions
export default {
  bsToAd,
  adToBs,
  getTodayBs,
  formatBsDate,
  nepaliMonths
}

