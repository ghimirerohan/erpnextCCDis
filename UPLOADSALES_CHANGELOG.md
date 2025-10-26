# Upload Sales - Enhancement Changelog

## Date: October 26, 2025

## Summary
Enhanced the Upload Sales web application with vehicle selection, improved preview accuracy, better field positioning in Sales Invoice, and comprehensive reset/clear functionality.

---

## Changes Implemented

### 1. **Driver Field Positioning in Sales Invoice**

**Problem**: The driver field was positioned after `customer_name`, not next to the vehicle field.

**Solution**: 
- Updated `custom_erp/fixtures/custom_field.json`
- Changed `insert_after` from `"customer_name"` to `"vehicle_for_delivery"`
- Now driver field appears directly below vehicle field in Sales Invoice form

**Benefits**:
- Logical field grouping (vehicle and driver together)
- Better UX for users entering delivery information
- Automatically applied when `custom_erp` is installed/migrated

---

### 2. **Vehicle Selection in Upload Web App**

**Problem**: Only driver could be selected; vehicle wasn't available for selection.

**Solution**:

#### Backend (`custom_erp/api/uploadsales.py`):
- Added `get_vehicles()` API endpoint to fetch list of vehicles
- Updated `enqueue_import_job()` to accept `vehicle_id` parameter
- Updated `process_upload_sales_job()` to pass vehicle_id to invoice creation
- Updated `create_sales_invoice_doc()` to set `vehicle_for_delivery` field

#### Frontend (`frontend/src/apps/uploadsales/`):
- Updated `DriverSelect.vue` to show both driver and vehicle dropdowns
- Added vehicle loading on component mount
- Updated state management to track `selectedVehicle`
- Updated import confirmation message to include vehicle

#### Hooks:
- Registered `get_vehicles` in `hooks.py` whitelisted methods

**Benefits**:
- Users can now select both driver and vehicle during import
- Vehicle is optional (can be left blank)
- Both fields are set on all imported Sales Invoices

---

### 3. **Preview Shows Actual IDs Instead of Names**

**Problem**: Preview table showed customer names and item names instead of the actual IDs that would be imported.

**Solution**:
- Changed `transform_and_preview()` to use `validate_lookups=True`
- Preview now performs actual database lookups and returns:
  - Customer ID (from Customer doctype `name` field)
  - Item Code (from Item doctype `item_code` field)

**Benefits**:
- Preview is now 100% accurate to what will be imported
- Users can verify exact IDs before import
- Prevents confusion between display names and internal IDs

---

### 4. **Clear/Reset Functionality**

**Problem**: Users had to refresh the browser to start a new import.

**Solution**:

#### Clear File Button:
- Added "Clear File" button in file info card
- Shows after file is uploaded but before import starts
- Confirmation dialog prevents accidental clears
- Clears: file, driver, vehicle, preview data

#### Reset Upload Function:
- Enhanced existing `resetUpload()` function
- Now also resets vehicle selection
- Called after import completion to allow new import

**Benefits**:
- No need to refresh browser
- Quick way to start over
- Proper state cleanup prevents bugs
- Better user experience

---

## Technical Details

### API Endpoints Added
```python
# Get list of vehicles for selection
@frappe.whitelist()
def get_vehicles()
```

### API Endpoints Modified
```python
# Now accepts vehicle_id parameter
@frappe.whitelist()
def enqueue_import_job(driver_id, vehicle_id, csv_content)
```

### Database Changes
- Custom field positioning update (applied via `bench migrate`)
- No schema changes (driver and vehicle fields already existed)

### Frontend State Management
```javascript
// New state added
const selectedVehicle = ref(null)
const vehicles = ref([])
const loadingVehicles = ref(false)

// Enhanced functions
loadVehicles()  // Load vehicles on mount
clearFile()     // Clear all selections
resetUpload()   // Reset after import
```

---

## Files Changed

### Backend
1. `custom_erp/fixtures/custom_field.json` - Driver field position
2. `custom_erp/custom_erp/api/uploadsales.py` - Vehicle support & preview fix
3. `custom_erp/hooks.py` - Register get_vehicles endpoint

### Frontend
1. `frontend/src/apps/uploadsales/UploadSales.vue` - Main component updates
2. `frontend/src/apps/uploadsales/components/DriverSelect.vue` - Vehicle selector added

### Built Files
- `frontend/dist/` - Rebuilt frontend assets
- `custom_erp/public/frontend/` - Deployed assets

---

## Testing Checklist

### ✅ Driver Field Position
- [ ] Create new Sales Invoice in ERPNext
- [ ] Verify "Driver" field appears below "Vehicle For Delivery"

### ✅ Vehicle Selection
- [ ] Open Upload Sales app at `/jsapp/uploadsales`
- [ ] Upload CSV file
- [ ] Verify both Driver and Vehicle dropdowns appear
- [ ] Verify Vehicle dropdown loads vehicles
- [ ] Select driver and vehicle
- [ ] Start import
- [ ] Check created Sales Invoice has both driver and vehicle set

### ✅ Preview Accuracy
- [ ] Upload CSV file
- [ ] Check preview table Customer column shows Customer ID (not name)
- [ ] Check preview table Item Code column shows Item Code (not item name)

### ✅ Clear/Reset Functionality
- [ ] Upload CSV file
- [ ] Verify "Clear File" button appears
- [ ] Click "Clear File" and confirm
- [ ] Verify all fields reset (file, driver, vehicle, preview)
- [ ] Complete an import
- [ ] Click "Import Another File"
- [ ] Verify all state resets including vehicle

---

## Migration Steps (For Production)

```bash
# 1. Pull latest code
cd /path/to/frappe-bench/apps/custom_erp
git pull origin develop

# 2. Build frontend
cd frontend
npm install
npm run build

# 3. Run migrations
cd /path/to/frappe-bench
bench --site <site-name> migrate

# 4. Restart server
bench restart

# 5. Clear cache (optional but recommended)
bench --site <site-name> clear-cache
```

---

## Notes

1. **Backward Compatibility**: All changes are backward compatible. Existing Sales Invoices are not affected.

2. **Vehicle is Optional**: Users can leave vehicle blank if not needed. Only driver is required.

3. **Custom Field Persistence**: The driver field position is defined in fixtures, so it will be correctly positioned in all new installations.

4. **Preview Performance**: Preview now does database lookups for first 10 invoices. This is slightly slower but provides accurate IDs.

---

## Future Enhancements (Optional)

1. **Bulk Edit**: Allow changing driver/vehicle for specific invoices in preview
2. **Default Vehicle**: Set default vehicle per driver
3. **Vehicle Validation**: Check if vehicle is available/not in use
4. **Driver Assignment Rules**: Auto-suggest driver based on route/customer

---

## Support

If you encounter any issues:

1. Check `Error Log` in ERPNext for backend errors
2. Check browser console for frontend errors
3. Verify driver and vehicle doctypes exist and have active records
4. Ensure custom field was migrated successfully

For questions, contact the development team.

---

## ADDED BY AI: UPLOAD_SALES
All changes marked with "ADDED BY AI: UPLOAD_SALES" comments in code.

