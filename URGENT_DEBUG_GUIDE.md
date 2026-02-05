# URGENT: Nepali Date Picker Debugging Guide

## ⚠️ Browser Not Accessible - Manual Testing Required

Since the automated browser isn't available, **YOU** need to test the following manually.

## 🔍 Quick Diagnosis Steps

### Step 1: Test if Library is Loading

Open browser console and run:
```javascript
console.log({
  jQuery: !!window.jQuery,
  NepaliPicker_window: !!window.NepaliDatePicker,
  NepaliPicker_prototype: !!(HTMLElement.prototype.NepaliDatePicker),
  jQueryPlugin: !!(window.jQuery && jQuery.fn.NepaliDatePicker)
});
```

**Expected Output:** At least one of the NepaliPicker checks should be `true`

### Step 2: Check Network Tab

1. Open DevTools (F12) → Network tab
2. Filter for "nepali"
3. Check if these load with **200 OK**:
   - `nepali.datepicker.v5.0.6.min.js`
   - `nepali.datepicker.v5.0.6.min.css`

**If 404 errors:** The library files aren't being served correctly

### Step 3: Simple Test Page

1. Navigate to: `http://localhost:8080/test_simple_picker.html`
2. This is a standalone test page (no Vue, just pure library)
3. Click the "Initialize Picker" buttons
4. Check if ANY of the 3 tests work

**If even the simple test fails:** The problem is with the library files themselves, not the Vue component

### Step 4: Check Console for Vue Component

1. Navigate to: `http://localhost:8080/pay-dashboard`
2. Open console (should see `[NepaliDatePicker]` messages)
3. Click the date picker input
4. Note exactly what messages appear

## 🎯 Likely Root Causes & Fixes

### Cause 1: Library Files Not Being Served

**Symptoms:**
- 404 errors in network tab for nepali datepicker files
- `window.NepaliDatePicker` is undefined even in simple test

**Solution:**
```bash
cd /workspace/development/frappe-bench/apps/custom_erp
# Check if files exist
ls -la custom_erp/public/lib/nepali*

# If missing, they should be there. If they exist, restart servers:
# Stop yarn dev (Ctrl+C)
# Stop bench start (Ctrl+C)
cd /workspace/development/frappe-bench
bench start
# In new terminal:
cd /workspace/development/frappe-bench/apps/custom_erp
yarn dev
```

### Cause 2: Vue Component Not Re-compiling

**Symptoms:**
- Console shows OLD behavior (no `[NepaliDatePicker]` messages)
- Changes to NepaliDatePicker.vue not reflecting

**Solution:**
```bash
# Kill yarn dev and restart it
cd /workspace/development/frappe-bench/apps/custom_erp
# Ctrl+C to stop
yarn dev
```

Then hard refresh browser: `Ctrl+Shift+R`

### Cause 3: Click Event Not Firing

**Symptoms:**
- No console messages when clicking the input
- Input appears but nothing happens

**Possible Fix - Remove `readonly` attribute:**

Edit `/workspace/development/frappe-bench/apps/custom_erp/shared/components/NepaliDatePicker.vue`:

Find line 8:
```vue
readonly
```

Change it to:
```vue
:readonly="false"
```

or just remove the line entirely.

### Cause 4: Calendar Div Not Rendering

**Symptoms:**
- Console shows "calendarRef.value: false"
- `isOpen` becomes true but no container appears

**Check in console:**
```javascript
// Find all nepali picker wrappers
document.querySelectorAll('.nepali-date-picker-wrapper').forEach((el, i) => {
  console.log(`Picker ${i}:`, {
    wrapper: !!el,
    input: !!el.querySelector('input'),
    calendar: !!el.querySelector('.ndp-calendar-container')
  });
});
```

## 🛠️ Emergency Fix - Bypass Vue Component

If the component still doesn't work, here's a temporary workaround:

### Replace with Simple jQuery Implementation

1. Open the Vue file where date picker is used (e.g., `PayDashboard.vue`)
2. Replace the `<NepaliDatePicker>` component with a simple input:

```vue
<input 
  ref="datePickerRef"
  type="text" 
  class="w-full px-3 py-2 border border-gray-300 rounded-md"
  placeholder="Select date (BS)"
/>
```

3. Add this to the `<script setup>` section:

```javascript
import { ref, onMounted } from 'vue'

const datePickerRef = ref(null)
const selectedDate = ref(null)

onMounted(async () => {
  // Wait for jQuery and library to load
  await new Promise(resolve => {
    const checkLibrary = setInterval(() => {
      if (window.jQuery && (window.NepaliDatePicker || HTMLElement.prototype.NepaliDatePicker)) {
        clearInterval(checkLibrary)
        resolve()
      }
    }, 100)
  })
  
  // Initialize using jQuery
  if (window.jQuery && window.jQuery.fn.NepaliDatePicker) {
    window.jQuery(datePickerRef.value).NepaliDatePicker({
      dateFormat: 'YYYY-MM-DD',
      onSelect: (dateObj) => {
        console.log('Date selected:', dateObj)
        selectedDate.value = dateObj.value
      }
    })
  }
})
```

## 📋 Debugging Checklist

Run through this checklist and report results:

- [ ] Library files load without 404 errors (check Network tab)
- [ ] `window.jQuery` is defined
- [ ] At least ONE of these is true:
  - [ ] `window.NepaliDatePicker` exists
  - [ ] `HTMLElement.prototype.NepaliDatePicker` exists
  - [ ] `jQuery.fn.NepaliDatePicker` exists
- [ ] Simple test page works (`test_simple_picker.html`)
- [ ] Console shows `[NepaliDatePicker] Loading dependencies...`
- [ ] Console shows `[NepaliDatePicker] All dependencies loaded and ready!`
- [ ] Clicking input triggers `[NepaliDatePicker] toggleCalendar called...`
- [ ] Calendar container appears in DOM (check Elements tab)
- [ ] Calendar is visible (not hidden by CSS)

## 🚨 If Nothing Works

If you've tried everything and it still doesn't work, provide me with:

1. **Screenshot** of browser console showing all messages when you:
   - Load the page
   - Click the date picker

2. **Screenshot** of Network tab showing the nepali datepicker file requests

3. **Output** of this command in browser console:
```javascript
// Full diagnostic
{
  page: window.location.href,
  jquery: {
    loaded: !!window.jQuery,
    version: window.jQuery ? jQuery.fn.jquery : 'N/A'  
  },
  library: {
    window: !!window.NepaliDatePicker,
    prototype: !!(typeof HTMLElement !== 'undefined' && HTMLElement.prototype.NepaliDatePicker),
    jqueryPlugin: !!(window.jQuery && jQuery.fn.NepaliDatePicker)
  },
  dom: {
    pickers: document.querySelectorAll('.nepali-date-picker-wrapper').length,
    calendars: document.querySelectorAll('.ndp-calendar-container').length,
    inputs: document.querySelectorAll('.nepali-date-picker-wrapper input').length
  },
  files: {
    css: !!document.querySelector('link[href*="nepali.datepicker"]'),
    cssHref: document.querySelector('link[href*="nepali.datepicker"]')?.href || 'Not loaded'
  }
}
```

## 💡 Most Likely Issue

Based on the code review, I suspect the issue is:

**The Vue component's `readonly` attribute on the input is preventing click events**

Try this quick fix:
1. Edit: `/workspace/development/frappe-bench/apps/custom_erp/shared/components/NepaliDatePicker.vue`
2. Line 8, remove `readonly`
3. Save and hard refresh browser

---

**Report back with the checklist results and any error messages!**
