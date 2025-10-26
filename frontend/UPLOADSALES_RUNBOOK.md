# Upload Sales Invoice - User Guide & Runbook

**ADDED BY AI: UPLOAD_SALES**

## Overview
The Upload Sales Invoice feature allows bulk import of sales invoices from CSV files with real-time progress tracking and comprehensive error handling.

## Access
**URL**: `http://localhost:8000/jsapp/uploadsales` (or `https://your-domain.com/jsapp/uploadsales`)

## Required Permissions
- Sales Invoice: Create, Read
- Driver: Read (or Employee: Read as fallback)
- File: Create, Read (for error CSV downloads)

## Step-by-Step Usage Guide

### 1. Login
- Navigate to the Upload Sales URL
- Log in with your ERPNext credentials
- You must have Sales Invoice create permissions

### 2. Upload CSV File
- **Drag and drop** a CSV file onto the upload area, or **click** to browse
- Accepted file format: CSV
- Maximum file size: 10MB
- The system will automatically parse and transform your data

### 3. Review Preview
- After upload, you'll see a preview of the transformed data
- Preview shows the first 20 rows in ERPNext import format
- Total invoice count is displayed
- Review to ensure data looks correct

### 4. Select Driver
- Choose a driver from the dropdown menu
- This driver will be assigned to ALL imported invoices
- Driver selection is **required** before starting import

### 5. Start Import
- Click the **"Start Import"** button
- Confirm the import action when prompted
- The import runs as a background job

### 6. Monitor Progress
- Real-time progress bar shows X/Total invoices processed
- Statistics displayed:
  - **Imported**: Successfully created invoices
  - **Skipped**: Invoices that already exist (by Invoice ID)
  - **Errors**: Invoices that failed validation or creation
  - **Total Amount**: Sum of grand totals for imported invoices
- Current status message updates as each invoice is processed

### 7. Review Summary
- After completion, view the summary card with:
  - Total invoices attempted
  - Successfully imported count
  - Skipped count
  - Error count
  - Total amount imported
- All imported invoices are in **Draft** status (not submitted)
- You can review and submit them manually from Sales Invoice list

### 8. Handle Errors (if any)
- If errors occurred, a **"Download Error CSV"** button appears
- Click to download a CSV containing only failed rows
- Each error row includes an **"Error Message"** column explaining the failure
- Fix the issues in your source data and re-upload

### 9. Upload Another File
- Click **"Upload Another File"** to start a new import
- The interface resets to the upload screen

## Input CSV Format

### Required Columns:
1. `Date` - Nepali date in YYYY.MM.DD format (e.g., "2082.07.09")
2. `InvoiceNo` - Unique invoice identifier (e.g., "8283-010755")
3. `Name of Customer` - Customer name (must exist in ERPNext)
4. `PAN No` - Customer PAN number (optional, used for lookup)
5. `Name of Product` - Item name (must exist in ERPNext Item master)
6. `QTY` - Quantity (decimal allowed)
7. `Unit` - Unit of measure (e.g., "CS")
8. `Discount` - Discount amount (optional)

### Optional Columns:
- `LocationCode`, `LocationName`, `PANCardNumber` - Informational
- `Total Sales`, `Non Taxable Sales`, `Taxable Sales(Rs)`, `VAT(Rs)` - Informational
- Export-related columns - Not currently used

### Important Notes:
- **Multiple rows with same InvoiceNo** are grouped as one invoice with multiple items
- **InvoiceNo starting with "SRV"** are treated as return invoices (Credit Notes)
- **Customer lookup**: If PAN No provided, searches by Name + PAN; falls back to Name only
- **Item lookup**: Searches by exact item_name match
- **Date conversion**: Nepali dates are converted to Gregorian format

## Output Behavior

### Sales Invoice Creation:
- **Status**: Draft (not submitted)
- **Update Stock**: Set to 1 (stock will update)
- **Driver**: Assigned to selected driver
- **Is Return**: Set for invoices starting with "SRV"
- **Items**: All items validated and added
- **Naming**: Invoice name matches InvoiceNo from CSV

### Validation Rules:
1. **Customer must exist** in ERPNext Customer doctype
2. **Item must exist** in ERPNext Item doctype  
3. **InvoiceNo must be unique** - duplicates are skipped
4. **Date must be valid** Nepali date convertible to Gregorian

## Error Handling

### Common Errors and Solutions:

#### "Customer '{name}' with PAN '{pan}' not found"
**Solution**: 
- Ensure customer exists in ERPNext
- Verify customer name spelling matches exactly
- Check PAN number is correct
- Create missing customers before import

#### "Item '{item_name}' not found"
**Solution**:
- Ensure item exists in ERPNext Item master
- Verify item name spelling matches exactly (case-sensitive)
- Create missing items before import

#### "Invoice {number} already exists"
**Solution**:
- This invoice was already imported or created manually
- Check Sales Invoice list
- If it's a duplicate in your CSV, remove or rename it

#### "Unable to convert Nepali date '{date}'"
**Solution**:
- Check date format is YYYY.MM.DD (e.g., "2082.07.09")
- Ensure date is valid in Nepali calendar
- Remove extra spaces or quotes

## Error CSV Format

When errors occur, you can download an error CSV containing:
- **All original input columns**
- **Additional column**: `Error Message` - Describes what went wrong

### Using Error CSV:
1. Download error CSV
2. Review "Error Message" column
3. Fix issues in your original data source
4. Re-export corrected data
5. Upload again through this tool

## File Locations

### Error CSV Files:
- Stored in ERPNext Files
- Naming format: `upload_sales_errors_{job_id}.csv`
- Accessible via download link in summary screen
- Marked as private files (login required to download)

## Performance Notes

- **Processing speed**: ~100-200 invoices per minute (varies by system)
- **Background processing**: Import runs in background worker, won't block UI
- **Concurrent imports**: Multiple users can import simultaneously
- **Large files**: Files with 1000+ invoices will take several minutes

## Troubleshooting

### Import Not Starting
- **Check**: Driver is selected
- **Check**: You have Sales Invoice create permission
- **Check**: Background workers are running (`bench doctor`)

### Progress Not Updating
- **Check**: WebSocket connection is active
- **Solution**: Refresh page and check Summary after a few minutes
- **Check**: Browser console for JavaScript errors

### Slow Import Speed
- **Cause**: Complex item validations or stock calculations
- **Cause**: System load or slow database queries
- **Solution**: Import during off-peak hours
- **Solution**: Split large files into smaller batches

### Missing Drivers in Dropdown
- **Check**: Driver doctype exists in system (HR module)
- **Fallback**: System will use Employee doctype if Driver not found
- **Check**: Drivers/Employees have "Active" status

## Best Practices

1. **Test with small file first** (5-10 invoices) to verify data mapping
2. **Validate customers and items** exist before bulk import
3. **Use consistent naming** in your CSV exports
4. **Keep original CSV** for reference and re-import if needed
5. **Review preview carefully** before starting import
6. **Monitor first few imports** to catch issues early
7. **Handle errors promptly** - fix and re-import failed invoices

## Support

### Logs Location:
- **Application logs**: `frappe-bench/logs/`
- **Error logs**: ERPNext → Error Log doctype
- **Search**: Filter by "Upload Sales" in title

### Debug Mode:
- Enable developer mode in `site_config.json`
- Check browser console for frontend errors
- Check `frappe-bench/logs/worker.log` for background job errors

### Common Log Searches:
- Error Log title: "Upload Sales"
- Error Log title: "Nepali Date Conversion"
- Error Log title: "Customer Lookup"
- Error Log title: "Item Lookup"

## Advanced Features

### Customization Options:
The transformation logic can be customized in:
- **Backend**: `custom_erp/custom_erp/api/uploadsales.py`
- **Frontend**: `frontend/src/apps/uploadsales/`

### Configuration:
Fixed values like company, tax templates, accounts are hardcoded in backend.
To change these, edit the `generate_output_csv_rows()` and `create_sales_invoice_doc()` functions.

### Field Mapping:
To change how fields are mapped from input to output, edit the `transform_invoice_rows()` function in the backend API.

## Version History
- **v1.0** (2025-10-26): Initial release with CSV upload, preview, bulk import, and error handling

