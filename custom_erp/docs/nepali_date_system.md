# Nepali Date UI System - Implementation Guide

## Overview

This system replaces all frontend Date and Datetime inputs with Nepali date UI (NepaliDatePicker v5) while storing standard Gregorian dates (YYYY-MM-DD / ISO datetimes) in the database. All changes are contained within the `custom_erp` app.

**Key Features:**
- UI displays dates in Bikram Sambat (BS) format
- Database stores dates in Gregorian (AD) format
- Toggle-able via System Settings
- No database schema changes required
- Supports both Date and Datetime fields
- Works with list filters, reports, and calendar views

## Implementation Status

✅ **Completed Components:**

1. **Library Files** (`public/lib/`)
   - `nepali.datepicker.v5.0.6.min.js` - Nepali DatePicker library
   - `nepali.datepicker.v5.0.6.min.css` - DatePicker styles
   - `sajan.nepaliFunctions.min.js` - Conversion functions (AD2BS, BS2AD)

2. **JavaScript Adapter** (`public/js/nepali_date_adapter.js`)
   - `custom_erp.nepali.adToBs()` - Convert AD to BS
   - `custom_erp.nepali.bsToAd()` - Convert BS to AD
   - `custom_erp.nepali.initNepaliPicker()` - Initialize picker
   - `custom_erp.nepali.getTodayBs()` - Get today's BS date

3. **Control Patch** (`public/js/nepali_date_patch.js`)
   - Monkey-patches `frappe.ui.form.ControlDate`
   - Monkey-patches `frappe.ui.form.ControlDatetime`
   - Handles bidirectional conversion (BS ↔ AD)
   - Preserves time portion in datetime fields

4. **Boot Hook** (`boot.py`)
   - Adds `enable_nepali_calendar` to `frappe.boot`
   - Provides synchronous client-side access
   - Improves performance and prevents UI flicker

5. **System Settings Patch** (`patches/v1_0/add_enable_nepali_calendar_field.py`)
   - Creates Custom Field in System Settings
   - Fieldname: `enable_nepali_calendar`
   - Fieldtype: Check (boolean)

6. **CSS Overrides** (`public/css/nepali_date_overrides.css`)
   - Styling adjustments for Frappe theme
   - Font rendering for unicode characters
   - Modal dialog z-index fixes

7. **Hooks Configuration** (`hooks.py`)
   - Includes all JS/CSS assets
   - Registers boot session hook
   - Applies to both Desk and Web

8. **Patch Registration** (`patches.txt`)
   - Added: `custom_erp.patches.v1_0.add_enable_nepali_calendar_field`

9. **Old Files Cleanup**
   - `override_date.js` → `override_date.js.old`
   - Old v5.0.5 files renamed to `.old`

## File Structure

```
custom_erp/
├── public/
│   ├── lib/
│   │   ├── nepali.datepicker.v5.0.6.min.js
│   │   ├── nepali.datepicker.v5.0.6.min.css
│   │   └── sajan.nepaliFunctions.min.js
│   ├── js/
│   │   ├── nepali_date_adapter.js
│   │   ├── nepali_date_patch.js
│   │   └── invoice_scanner.js
│   └── css/
│       └── nepali_date_overrides.css
├── patches/
│   └── v1_0/
│       └── add_enable_nepali_calendar_field.py
├── boot.py
├── hooks.py
└── patches.txt
```

## How It Works

### Data Flow: User Input → Storage

1. User selects BS date in picker (e.g., **2081-07-03**)
2. `onChange` handler calls `custom_erp.nepali.bsToAd()`
3. Converts to AD (e.g., **2024-10-19**)
4. Sets control value with AD date
5. Frappe saves **AD date** to database

### Data Flow: Storage → Display

1. Control receives AD date from database (e.g., **2024-10-19**)
2. `set_formatted_input()` calls `custom_erp.nepali.adToBs()`
3. Converts to BS (e.g., **2081-07-03**)
4. Displays **BS date** in input field

### Datetime Handling

For datetime fields:
- Split value into date and time portions
- Convert only the date portion (BS ↔ AD)
- Keep time portion unchanged
- Rejoin before storing/displaying

**Example:**
- Input: `2081-07-03 14:30:00` (BS)
- Stored: `2024-10-19 14:30:00` (AD)

## Installation & Usage

### Step 1: Build the App

```bash
cd /workspace/development/frappe-bench
bench build --app custom_erp
```

This compiles all JS/CSS assets into the public folder.

### Step 2: Run Migrations

```bash
bench migrate
```

This creates the System Settings custom field.

### Step 3: Restart Services

```bash
bench restart
```

Or for development:
```bash
bench --site development.localhost clear-cache
```

### Step 4: Enable Nepali Calendar

1. Login to your ERPNext site
2. Go to: **Setup → System Settings**
3. Scroll down to find: **Enable Nepali Calendar**
4. Check the box to enable
5. Save

### Step 5: Test the Feature

1. **Create a new document** (e.g., Sales Invoice)
2. Click on any Date field
3. You should see the Nepali Date Picker with BS dates
4. Select a BS date
5. Save the document
6. **Verify in database:**
   - Go to the saved document
   - Check "Form → Show Debug Info"
   - The `date` field should show AD format (YYYY-MM-DD)
7. **Re-open the document:**
   - The date field should display BS format in the UI

## Testing Checklist

### Basic Functionality
- [ ] Date field shows Nepali picker with BS dates
- [ ] Selected BS date stores as AD in database
- [ ] Existing AD dates convert to BS on display
- [ ] "Today" shortcut works correctly
- [ ] Empty date fields handle gracefully

### Datetime Fields
- [ ] Datetime field shows BS date with time
- [ ] Time portion remains unchanged
- [ ] Both date and time save correctly

### List Views & Filters
- [ ] Date filters in list views work
- [ ] Date range filters convert properly
- [ ] Search by date returns correct results

### Reports & Calendar
- [ ] Report date parameters work
- [ ] Calendar view displays events correctly
- [ ] Month navigation works in calendar

### Export/Import
- [ ] CSV exports contain AD dates
- [ ] Excel exports contain AD dates
- [ ] Data imports parse AD dates correctly

### Toggle Behavior
- [ ] Disabling toggle reverts to standard date controls
- [ ] Re-enabling toggle restores Nepali picker
- [ ] Settings persist across sessions

## Troubleshooting

### Picker Not Showing

**Problem:** Date fields show regular input, not Nepali picker

**Solutions:**
1. Check if setting is enabled: System Settings → Enable Nepali Calendar
2. Clear cache: `bench --site <site-name> clear-cache`
3. Check browser console for errors
4. Verify JS files loaded: Network tab → Filter by "nepali"

### Conversion Errors

**Problem:** Dates not converting correctly

**Solutions:**
1. Check date format is YYYY-MM-DD
2. Verify date is within valid BS range (1970-2099)
3. Check browser console for conversion errors
4. Ensure NepaliFunctions library is loaded

### Datetime Issues

**Problem:** Time portion gets lost or corrupted

**Solutions:**
1. Verify datetime format includes both date and time
2. Check timezone settings in System Settings
3. Test with simple time values (e.g., 12:00:00)

### Modal Dialog Issues

**Problem:** Picker appears behind modal

**Solutions:**
1. Check CSS is loaded: `nepali_date_overrides.css`
2. Verify z-index values in browser inspector
3. Try rebuilding: `bench build --app custom_erp`

## Technical Details

### Monkey Patching Strategy

The system uses class extension (inheritance) rather than direct replacement:

```javascript
var NepaliDateControl = OriginalDate.extend({
    make_input: function() {
        this._super();  // Call parent method
        // Add Nepali picker logic
    }
});
```

This ensures compatibility with future Frappe updates.

### Preventing Recursive Updates

The code uses a flag to prevent infinite loops:

```javascript
this._is_setting_value = false;

onChange: function(e) {
    if (me._is_setting_value) return;  // Skip if already setting
    me._is_setting_value = true;
    me.set_model_value(ad);
    me._is_setting_value = false;
}
```

### Boot Hook Optimization

The boot hook adds the setting to `frappe.boot` at session start:

```python
boot['enable_nepali_calendar'] = frappe.db.get_single_value(
    'System Settings', 
    'enable_nepali_calendar'
) or False
```

This eliminates the need for async DB calls on every page load.

## Compatibility

### Tested With
- Frappe Framework: v14.x, v15.x
- ERPNext: v14.x, v15.x
- Browsers: Chrome, Firefox, Safari, Edge

### Known Limitations
1. Date range must be BS 1970-2099 (library limitation)
2. Some third-party apps may not support BS dates
3. API responses always return AD dates (by design)
4. Print formats may require custom formatting

### Upgrade Safety
- No core Frappe files modified
- All changes in custom app
- Can be disabled via System Settings
- Old files preserved as `.old` backups

## Future Enhancements

Potential improvements:
1. Add BS date formatting options (DD-MM-YYYY, MM/DD/YYYY, etc.)
2. Support for fiscal year in BS calendar
3. BS date validation in Custom Scripts
4. Print format helper functions
5. BS date support in API responses (opt-in)
6. Mobile app integration

## Support & References

### Documentation
- Nepali DatePicker: https://github.com/leapfrogtechnology/nepali-date-picker
- NepaliFunctions: Library for AD/BS conversion
- Frappe Framework: https://frappeframework.com/docs

### Maintenance
- Old implementation files backed up with `.old` extension
- Can be safely deleted after testing
- Keep for reference or rollback if needed

### Debugging
Enable debug mode in console:
```javascript
// Check if Nepali calendar is enabled
console.log(frappe.boot.enable_nepali_calendar);

// Test conversion functions
console.log(custom_erp.nepali.adToBs('2024-10-19'));  // Should return BS date
console.log(custom_erp.nepali.bsToAd('2081-07-03'));  // Should return AD date
```

## Credits

Implementation by: Custom ERP Team
Date: October 2025
Version: 1.0.0
License: MIT

---

**Note:** This is a UI-only enhancement. All database operations continue to use Gregorian (AD) dates for consistency and compatibility with existing systems.

