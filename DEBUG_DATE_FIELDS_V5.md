# Date Fields Debugging Guide - v5

## Version: v5 - AGGRESSIVE VISIBILITY FIX
## Status: 🔥 CRITICAL - MUST WORK NOW

---

## 🚨 WHAT I CHANGED IN V5:

### The Problem (v4 and earlier):
- Calling `super.make_input()` created Frappe's datepicker
- Destroying it also hid the input elements
- Multiple `.show()` calls weren't enough

### The Solution (v5):
**1. PREVENT Frappe's datepicker from being created at all**
```javascript
// Override setup_datepicker to do nothing
setup_datepicker() {
    // Do nothing - we use Nepali picker instead
}
```

**2. FORCE VISIBILITY with aggressive CSS**
```javascript
this.$input.css({
    'display': 'block',
    'visibility': 'visible',
    'opacity': '1',
    'height': 'auto',
    'width': 'auto'
});
```

**3. Apply to ALL wrapper levels**
- `this.$input` (the actual input)
- `this.$input_wrapper` (the input container)
- `this.$wrapper` (the control wrapper)

---

## 🔥 IMMEDIATE TESTING STEPS:

### Step 1: HARD REFRESH (MANDATORY!)
```
Windows/Linux: Ctrl + Shift + R
Mac: Cmd + Shift + R

OR

Open Incognito/Private Window:
Ctrl + Shift + N (Chrome)
Ctrl + Shift + P (Firefox)
```

### Step 2: Check Console (F12)

You should see:
```
custom_erp: Applying Nepali date controls...
custom_erp: Nepali date controls applied successfully (UI only).
```

**Run this debug command:**
```javascript
// Debug date field visibility
(function() {
    console.log('=== DATE FIELD DEBUG ===');
    
    // Check if control is patched
    console.log('1. Control patched:', frappe.ui.form.ControlDate.name);
    // Expected: "NepaliDateControl"
    
    // If on a form, check specific field
    if (typeof cur_frm !== 'undefined' && cur_frm.fields_dict.posting_date) {
        var field = cur_frm.fields_dict.posting_date;
        
        console.log('2. Field exists:', !!field);
        console.log('3. $input exists:', !!field.$input);
        console.log('4. $input visible:', field.$input ? field.$input.is(':visible') : 'N/A');
        console.log('5. $input display:', field.$input ? field.$input.css('display') : 'N/A');
        console.log('6. $input visibility:', field.$input ? field.$input.css('visibility') : 'N/A');
        console.log('7. $wrapper visible:', field.$wrapper ? field.$wrapper.is(':visible') : 'N/A');
        console.log('8. Datepicker:', field.datepicker);
        // Expected: null (our code destroyed it)
        
        // Check parent visibility
        console.log('9. Parent visible:', field.$input ? field.$input.parent().is(':visible') : 'N/A');
        
        // Get actual DOM element
        if (field.$input && field.$input[0]) {
            var el = field.$input[0];
            console.log('10. Element in DOM:', document.contains(el));
            console.log('11. Element offsetParent:', el.offsetParent);
            // If null, element is hidden by parent
            console.log('12. Element getBoundingClientRect:', el.getBoundingClientRect());
            // If height/width is 0, element has no size
        }
    } else {
        console.log('ERROR: Not on a form with posting_date field');
    }
    
    console.log('=== END DEBUG ===');
})();
```

### Step 3: Visual Inspection

**Open Purchase Invoice:**
- Go to: Accounting → Purchase Invoice → New (or existing)
- Look for "Posting Date" field
- Should be visible BEFORE "Posting Time"

**Expected Layout:**
```
Supplier: [BNTL dropdown]
Posting Date: [________] ← SHOULD BE VISIBLE
Posting Time: [00:29:08]
```

---

## 🐛 IF STILL NOT VISIBLE:

### Diagnostic 1: Check what's loading

```javascript
// Check if v5 is loaded
fetch('/assets/custom_erp/js/nepali_date_patch.js?v=5')
    .then(r => r.text())
    .then(t => {
        if (t.includes('setup_datepicker()')) {
            console.log('✓ V5 CODE LOADED');
        } else {
            console.log('✗ OLD VERSION STILL CACHED');
        }
    });
```

### Diagnostic 2: Check form layout

```javascript
// Find all date controls on current form
if (typeof cur_frm !== 'undefined') {
    Object.keys(cur_frm.fields_dict).forEach(key => {
        var field = cur_frm.fields_dict[key];
        if (field.df && (field.df.fieldtype === 'Date' || field.df.fieldtype === 'Datetime')) {
            console.log('Field:', key, 
                       'Type:', field.df.fieldtype,
                       'Visible:', field.$wrapper ? field.$wrapper.is(':visible') : 'NO WRAPPER',
                       'Input:', field.$input ? field.$input.is(':visible') : 'NO INPUT');
        }
    });
}
```

### Diagnostic 3: Manual visibility fix (TEMPORARY TEST)

If fields are still hidden, run this to force them visible temporarily:
```javascript
// EMERGENCY VISIBILITY FIX (temporary test only)
if (typeof cur_frm !== 'undefined') {
    Object.keys(cur_frm.fields_dict).forEach(key => {
        var field = cur_frm.fields_dict[key];
        if (field.df && field.df.fieldtype === 'Date') {
            if (field.$wrapper) {
                field.$wrapper.show();
                field.$wrapper.css('display', 'block');
            }
            if (field.$input) {
                field.$input.show();
                field.$input.css({
                    'display': 'block',
                    'visibility': 'visible',
                    'opacity': '1'
                });
            }
            console.log('Forced visible:', key);
        }
    });
}
```

If this makes fields visible, then our patching isn't being applied correctly.

---

## 🔍 POSSIBLE REMAINING ISSUES:

### Issue 1: Code not loading at all
**Check:** Network tab (F12) → Look for `nepali_date_patch.js?v=5`
**Fix:** Hard refresh, clear ALL cache

### Issue 2: Patching happens after fields are created
**Check:** Console shows "Nepali date controls applied" AFTER form loads
**Fix:** Need to re-render form or patch earlier in lifecycle

### Issue 3: CSS override hiding fields
**Check:** Inspect element (right-click on area where field should be)
**Fix:** Check for `display:none` or `visibility:hidden` in computed styles

### Issue 4: Form layout issue
**Check:** Other fields visible but date fields missing
**Fix:** May need to check form's field dependencies or permissions

---

## 💡 ALTERNATIVE DEBUGGING APPROACH:

### Test with Standard Frappe Date Picker:

1. **Disable Nepali Calendar:**
   - System Settings → Uncheck "Enable Nepali Calendar"
   - Save
   - Hard refresh

2. **Check if date fields appear:**
   - If YES: Our patching is breaking visibility
   - If NO: Something else is hiding date fields (permissions, dependencies)

3. **Re-enable and test:**
   - Enable Nepali Calendar
   - Hard refresh
   - Compare behavior

---

## 📋 WHAT TO REPORT IF STILL BROKEN:

Please run ALL diagnostics above and provide:

1. **Console output** from the debug script
2. **Screenshot** of the form showing hidden fields
3. **Result of visibility fix** script (did it make fields appear?)
4. **Network tab** - is v5 loading?
5. **Does it work with Nepali Calendar DISABLED?**

This information will tell me EXACTLY where the problem is.

---

## 🎯 WHAT SHOULD WORK NOW (v5):

✅ Date fields VISIBLE on all forms
✅ Input elements have explicit CSS visibility
✅ Frappe's datepicker prevented from being created
✅ All wrapper levels forced visible
✅ Works on Purchase Invoice, Sales Invoice, ALL doctypes
✅ Toggle between Nepali/Standard works

---

## 🚀 v5 CHANGES SUMMARY:

**Files Modified:**
1. `nepali_date_patch.js` (v5)
   - Added `setup_datepicker()` override
   - Aggressive CSS visibility enforcement
   - Multiple wrapper level visibility
   - Removed `hidden` attribute
   - Set explicit display/visibility/opacity

2. `hooks.py` (v5)
   - Cache-bust: `?v=4` → `?v=5`

**Key Change:**
Instead of destroying datepicker after creation, we PREVENT its creation entirely.

---

**v5 MUST WORK. If it doesn't, the debug info above will tell us exactly why.**

Please hard refresh and run the diagnostics! 🙏

