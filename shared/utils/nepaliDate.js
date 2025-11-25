// Nepali Date Conversion Utilities
// Based on the Nepali calendar system (Bikram Sambat)

// This is a simplified version - for production, use nepali-date-converter library
// Reference date: 2000 Baisakh 1 BS = 1943 April 14 AD

/**
 * Bikram Sambat calendar data
 * Each entry is [year, [days in each month]]
 */
const bsCalendarData = {
  2080: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2081: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
  2082: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
}

/**
 * Convert BS (Bikram Sambat) date to AD (Gregorian) date
 * @param {string} bsDateStr - Date in YYYY-MM-DD format (BS)
 * @returns {string} Date in YYYY-MM-DD format (AD)
 */
export function bsToAd(bsDateStr) {
  if (!bsDateStr) return ''
  
  try {
    const [year, month, day] = bsDateStr.split('-').map(Number)
    
    // Reference: 2000/01/01 BS = 1943/04/14 AD
    const bsEpochYear = 2000
    const bsEpochMonth = 1
    const bsEpochDay = 1
    const adEpochDate = new Date(1943, 3, 14) // April 14, 1943
    
    // Calculate days from epoch
    let totalDays = 0
    
    // Add days for complete years
    for (let y = bsEpochYear; y < year; y++) {
      const yearData = bsCalendarData[y] || [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
      totalDays += yearData.reduce((sum, days) => sum + days, 0)
    }
    
    // Add days for complete months in current year
    const currentYearData = bsCalendarData[year] || [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
    for (let m = 0; m < month - 1; m++) {
      totalDays += currentYearData[m]
    }
    
    // Add remaining days
    totalDays += day - 1
    
    // Calculate AD date
    const adDate = new Date(adEpochDate.getTime() + totalDays * 24 * 60 * 60 * 1000)
    
    // Format as YYYY-MM-DD
    const adYear = adDate.getFullYear()
    const adMonth = String(adDate.getMonth() + 1).padStart(2, '0')
    const adDay = String(adDate.getDate()).padStart(2, '0')
    
    return `${adYear}-${adMonth}-${adDay}`
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
  if (!adDateStr) return ''
  
  try {
    const adDate = new Date(adDateStr)
    const adEpochDate = new Date(1943, 3, 14) // April 14, 1943 = 2000/01/01 BS
    
    // Calculate days difference
    const diffTime = adDate.getTime() - adEpochDate.getTime()
    const diffDays = Math.floor(diffTime / (24 * 60 * 60 * 1000))
    
    // Start from epoch
    let bsYear = 2000
    let bsMonth = 1
    let bsDay = 1
    let remainingDays = diffDays
    
    // Find the year
    while (remainingDays > 0) {
      const yearData = bsCalendarData[bsYear] || [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
      const daysInYear = yearData.reduce((sum, days) => sum + days, 0)
      
      if (remainingDays >= daysInYear) {
        remainingDays -= daysInYear
        bsYear++
      } else {
        break
      }
    }
    
    // Find the month
    const currentYearData = bsCalendarData[bsYear] || [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
    for (let i = 0; i < 12; i++) {
      const daysInMonth = currentYearData[i]
      if (remainingDays >= daysInMonth) {
        remainingDays -= daysInMonth
        bsMonth++
      } else {
        break
      }
    }
    
    // Remaining days
    bsDay += remainingDays
    
    return `${bsYear}-${String(bsMonth).padStart(2, '0')}-${String(bsDay).padStart(2, '0')}`
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
  const today = new Date()
  const adStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
  return adToBs(adStr)
}

/**
 * Format BS date for display
 * @param {string} bsDateStr - Date in YYYY-MM-DD format (BS)
 * @returns {string} Formatted date
 */
export function formatBsDate(bsDateStr) {
  if (!bsDateStr) return ''
  
  const [year, month, day] = bsDateStr.split('-')
  const months = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']
  return `${day} ${months[parseInt(month) - 1]} ${year}`
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

