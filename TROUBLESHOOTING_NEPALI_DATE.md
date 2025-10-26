# Troubleshooting Nepali Date System

## Status Confirmed ✓
- ✓ Custom Field exists in database
- ✓ Setting is ENABLED (value = 1)
- ✓ JS files are built and linked
- ✓ All assets are in place

## Next Steps: Browser Debugging

### Step 1: Hard Refresh Your Browser
```
Press: Ctrl + Shift + R (Windows/Linux)
Press: Cmd + Shift + R (Mac)
```

This clears browser cache and reloads all assets.

### Step 2: Open Browser Developer Console

1. Open your ERPNext site in browser
2. Press **F12** (or right-click → Inspect)
3. Go to **Console** tab
4. Look for these messages:

#### Expected Messages (Good):
```
custom_erp: Applying Nepali date controls...
custom_erp: Nepali date controls applied successfully (UI only).
```

#### Problem Messages (Need attention):
```
custom_erp: Nepali calendar is disabled.
→ Setting not loading from boot
```

```
NepaliFunctions not found. Make sure nepali datepicker is loaded.
→ Library not loading
```

```
Frappe form controls not yet loaded.
→ Script loading too early
```

### Step 3: Check if Libraries are Loaded

In the **Console** tab, type these commands:

```javascript
// Check if NepaliFunctions exists
console.log(window.NepaliFunctions);
// Expected: Should show an object with functions like AD2BS, BS2AD

// Check if boot setting is loaded
console.log(frappe.boot.enable_nepali_calendar);
// Expected: true

// Check if adapter is loaded
console.log(custom_erp.nepali);
// Expected: Object with adToBs, bsToAd, initNepaliPicker functions

// Check if jQuery plugin is available
console.log(typeof $.fn.nepaliDatePicker);
// Expected: "function"

// Check if controls are patched
console.log(frappe.ui.form.ControlDate.name);
// Expected: "NepaliDateControl" (if patched)
```

### Step 4: Check Network Tab

1. In Developer Tools, go to **Network** tab
2. Refresh the page (F5)
3. Filter by "nepali" in the search box
4. Look for these files:

```
✓ sajan.nepaliFunctions.min.js (should be Status: 200)
✓ nepali.datepicker.v5.0.6.min.js (should be Status: 200)
✓ nepali_date_adapter.js (should be Status: 200)
✓ nepali_date_patch.js (should be Status: 200)
✓ nepali.datepicker.v5.0.6.min.css (should be Status: 200)
```

If any file shows 404, run:
```bash
cd /workspace/development/frappe-bench
bench build --app custom_erp --force
bench restart
```

### Step 5: Test on a Document

1. Go to any document with a date field (e.g., **Sales Invoice → New**)
2. Click on the **Date** field
3. **Expected:** Nepali Date Picker should appear with BS dates

If it doesn't work:

#### Debug in Console:
```javascript
// Create a test date field
var testInput = $('<input type="text" class="form-control">').appendTo('body');

// Try to initialize picker manually
custom_erp.nepali.initNepaliPicker(testInput, {
    onChange: function(e) {
        console.log('Date selected:', e.bs);
    }
});

// Check if it worked
console.log(testInput.data());
// Should show nepali-datepicker data
```

### Step 6: Check Loading Order

The scripts should load in this order:
1. sajan.nepaliFunctions.min.js (NepaliFunctions library)
2. nepali.datepicker.v5.0.6.min.js (jQuery plugin)
3. nepali_date_adapter.js (Conversion helpers)
4. nepali_date_patch.js (Control patches)

**To verify order** in Console:
```javascript
// This should run without errors
try {
    var testDate = NepaliFunctions.AD2BS('2024-10-19');
    console.log('AD to BS works:', testDate);
    
    var testBack = NepaliFunctions.BS2AD(testDate);
    console.log('BS to AD works:', testBack);
    
    console.log('✓ Conversion functions working');
} catch(e) {
    console.error('✗ Conversion failed:', e);
}
```

## Common Issues & Fixes

### Issue 1: "NepaliFunctions not found"

**Cause:** Library not loading

**Fix:**
```bash
cd /workspace/development/frappe-bench
bench build --app custom_erp --force
bench restart
```

Then hard refresh browser (Ctrl+Shift+R)

### Issue 2: "frappe.boot.enable_nepali_calendar is undefined"

**Cause:** Boot hook not working

**Check:**
```bash
cd /workspace/development/frappe-bench
bench --site development.localhost mariadb -e "SELECT value FROM \`tabSingles\` WHERE doctype='System Settings' AND field='enable_nepali_calendar';"
```

Should return: `1`

If it returns `0` or nothing:
1. Go to System Settings
2. Check "Enable Nepali Calendar"
3. Save
4. Logout and login again

### Issue 3: "$.fn.nepaliDatePicker is not a function"

**Cause:** jQuery plugin not loaded

**Fix:**
1. Check if `nepali.datepicker.v5.0.6.min.js` is loaded (Network tab)
2. Check console for JavaScript errors during page load
3. Rebuild: `bench build --app custom_erp --force`

### Issue 4: Controls not patching

**Cause:** Script loading before Frappe UI is ready

**Debug in Console:**
```javascript
// Check if Frappe controls exist
console.log(frappe.ui.form.ControlDate);
console.log(frappe.ui.form.ControlDatetime);

// If they exist but not patched, manually apply:
// (This is temporary, for testing only)
console.log('Attempting manual patch...');
// Reload the page instead
```

### Issue 5: Picker appears but dates don't convert

**Cause:** Conversion functions not working

**Debug:**
```javascript
// Test conversions
console.log(custom_erp.nepali.adToBs('2024-10-19')); // Should show BS date
console.log(custom_erp.nepali.bsToAd('2081-07-03')); // Should show AD date

// If undefined, check if adapter loaded:
console.log(typeof custom_erp.nepali);
```

## Quick Diagnostic Commands

Run these in browser console:

```javascript
// Full diagnostic
(function() {
    console.log('='.repeat(60));
    console.log('NEPALI DATE SYSTEM DIAGNOSTIC');
    console.log('='.repeat(60));
    
    console.log('\n1. Boot Setting:', frappe.boot.enable_nepali_calendar);
    console.log('2. NepaliFunctions:', typeof window.NepaliFunctions);
    console.log('3. jQuery Plugin:', typeof $.fn.nepaliDatePicker);
    console.log('4. Adapter:', typeof custom_erp.nepali);
    console.log('5. ControlDate:', frappe.ui.form.ControlDate?.name || 'Not loaded');
    console.log('6. ControlDatetime:', frappe.ui.form.ControlDatetime?.name || 'Not loaded');
    
    // Test conversion
    try {
        var bs = NepaliFunctions.AD2BS('2024-10-19');
        var ad = NepaliFunctions.BS2AD(bs);
        console.log('\n7. Conversion Test:');
        console.log('   AD → BS:', bs);
        console.log('   BS → AD:', ad);
        console.log('   ✓ Conversions working');
    } catch(e) {
        console.log('\n7. Conversion Test: ✗ FAILED', e.message);
    }
    
    console.log('\n' + '='.repeat(60));
})();
```

## If All Else Fails

1. **Check frappe logs:**
```bash
cd /workspace/development/frappe-bench
bench --site development.localhost watch
```

2. **Restart everything:**
```bash
cd /workspace/development/frappe-bench
bench restart
bench --site development.localhost clear-cache
```

3. **Rebuild from scratch:**
```bash
cd /workspace/development/frappe-bench
bench build --app custom_erp --force
bench migrate
bench restart
```

4. **Check if old override_date.js is interfering:**
```bash
# List all date-related JS in assets
ls -lh /workspace/development/frappe-bench/sites/assets/custom_erp/js/*date* 2>/dev/null
```

Look for `override_date.js` WITHOUT `.old` extension. If it exists, it might be conflicting.

## Success Indicators

When everything works:

1. **Console shows:**
   ```
   custom_erp: Applying Nepali date controls...
   custom_erp: Nepali date controls applied successfully (UI only).
   ```

2. **Date field behavior:**
   - Click on date field
   - Nepali calendar picker appears
   - Dates show in BS format (e.g., 2081-07-03)
   - Can select BS dates
   - Saves correctly

3. **Database verification:**
   - Open saved document
   - Check "Form → Show Debug Info"
   - Date field shows AD format (e.g., 2024-10-19)
   - UI displays BS format (e.g., 2081-07-03)

---

**Need more help?**
Check the full documentation at: `custom_erp/docs/nepali_date_system.md`

