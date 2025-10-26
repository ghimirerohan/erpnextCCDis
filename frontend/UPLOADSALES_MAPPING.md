# Upload Sales Invoice - Data Mapping Documentation

**ADDED BY AI: UPLOAD_SALES**

## Overview
This document describes the transformation logic from input CSV format to ERPNext Sales Invoice import format.

## Input CSV Format
Source file: `Input_processing_ready_sales_invoice.csv`

### Input Columns:
1. Date - Nepali date format (YYYY.MM.DD) e.g., "2082.07.09"
2. InvoiceNo - Invoice identifier e.g., "8283-010755"
3. LocationCode - e.g., "0070000154"
4. LocationName - e.g., "Riya Trade and Suppliers"
5. PANCardNumber - Location PAN e.g., "302226124"
6. Name of Customer - Customer name e.g., "Khanal Kirana Pasal"
7. PAN No - Customer PAN number e.g., "608333430"
8. Name of Product - Item name e.g., "1.5LPLASN1X6 COKE SLD 200"
9. QTY - Quantity with decimals e.g., "3.00"
10. Unit - Unit of measure e.g., "CS"
11. Total Sales - Total sales amount
12. Non Taxable Sales - Non-taxable portion
13. Discount - Discount amount
14. Taxable Sales(Rs) - Taxable amount
15. VAT(Rs) - VAT amount
16. Export Product/Service Price (Rs)
17. Export Country
18. Export PP No
19. Export PP Date

## Output CSV Format
Target file: `output_import_ready_sales_invoice.csv`

### Output Columns:
1. Is Return (Credit Note) - "-" or "1"
2. Date - Gregorian date (DD/MM/YYYY) e.g., "26/10/2025"
3. ID - Invoice number from input
4. Customer - Customer ID from ERPNext Customer doctype
5. Item (Items) - Item code from ERPNext Item doctype
6. Quantity (Items) - Quantity value
7. Distributed Discount Amount (Items) - Discount from input
8. Item Name (Items) - Item name from input
9. Currency - "NPR"
10. Update Stock - "1"
11. Exchange Rate - "1"
12. Price List Currency - "NPR"
13. Price List Exchange Rate - "1"
14. Update Outstanding for Self - "0"
15. Update Billed Amount in Sales Order - "0"
16. Update Billed Amount in Delivery Note - "1"
17. Debit To - "Debtors - RTAS"
18. Price List - "Standard Selling"
19. Sales Taxes and Charges Template - "Nepal Tax - RTAS"
20. Account Head (Sales Taxes and Charges) - "VAT - RTAS"
21. Description (Sales Taxes and Charges) - "VAT @ 13.0"
22. Type (Sales Taxes and Charges) - "On Net Total"
23. Tax Rate (Sales Taxes and Charges) - "13"
24. Cost Center (Items) - "Main - RTAS"
25. Income Account (Items) - "Sales - RTAS"
26. UOM (Items) - Unit from input

## Transformation Rules

### 1. Is Return (Credit Note) Detection
- **Rule**: Check if `InvoiceNo` starts with "SRV" (case-sensitive)
- **Logic**:
  ```python
  is_return = "1" if invoice_no.startswith("SRV") else "-"
  ```
- **Output**: "1" for returns, "-" for normal invoices

### 2. Date Conversion
- **Input**: Nepali date "2082.07.09" (YYYY.MM.DD format)
- **Output**: Gregorian date "26/10/2025" (DD/MM/YYYY format)
- **Logic**: Use Nepali date library to convert BS to AD
- **Example**: 2082.07.09 BS → 26/10/2025 AD

### 3. Customer Lookup
- **Input Fields**: "Name of Customer", "PAN No"
- **Lookup Logic**:
  1. If PAN No is present and not empty:
     - Search Customer doctype: `customer_name = {Name of Customer} AND pan_no = {PAN No}`
     - If not found, fallback: Search by `customer_name = {Name of Customer}` only
  2. If PAN No is empty/null:
     - Search Customer doctype: `customer_name = {Name of Customer}`
  3. If multiple customers found, pick the first result
  4. If no customer found, record error and skip invoice
- **Output**: Customer.name field (e.g., "CUST-00123")

### 4. Item Lookup
- **Input Field**: "Name of Product"
- **Lookup Logic**:
  1. Search Item doctype: `item_name = {Name of Product}` (exact match)
  2. If found, use `item_code` field
  3. If not found, record error for that line item
- **Output**: Item.item_code field (e.g., "ITEM-00456")

### 5. Invoice Grouping Format
- **Rule**: Multiple rows with same InvoiceNo are grouped together
- **First row** of each invoice group contains:
  - All invoice-level fields: Is Return, Date, ID, Customer
  - All fixed fields: Currency, Update Stock, Exchange Rate, etc.
  - First item details
- **Subsequent rows** of same invoice:
  - Leave blank: Is Return, Date, ID, Customer, all fixed fields
  - Only populate: Item, Quantity, Discount, Item Name, Cost Center, Income Account, UOM
- **Example**:
  ```
  Row 1: "- ", "26/10/2025", "8283-010755", "CUST-001", "ITEM-001", 3, 0, "COKE", "NPR", 1, ...
  Row 2: "", "", "", "", "ITEM-002", 0.02, 325.96, "COKE", "", "", ...
  Row 3: "", "", "", "", "ITEM-003", 1, 0, "SPRITE", "", "", ...
  ```

### 6. Fixed Field Values
These fields have constant values for all invoices:
- Currency: "NPR"
- Update Stock: "1"
- Exchange Rate: "1"
- Price List Currency: "NPR"
- Price List Exchange Rate: "1"
- Update Outstanding for Self: "0"
- Update Billed Amount in Sales Order: "0"
- Update Billed Amount in Delivery Note: "1"
- Debit To: "Debtors - RTAS"
- Price List: "Standard Selling"
- Sales Taxes and Charges Template: "Nepal Tax - RTAS"
- Account Head (Sales Taxes and Charges): "VAT - RTAS"
- Description (Sales Taxes and Charges): "VAT @ 13.0"
- Type (Sales Taxes and Charges): "On Net Total"
- Tax Rate (Sales Taxes and Charges): "13"
- Cost Center (Items): "Main - RTAS"
- Income Account (Items): "Sales - RTAS"

### 7. Quantity and Discount Mapping
- **Quantity**: Direct copy from "QTY" field
- **Distributed Discount Amount**: Direct copy from "Discount" field
- **UOM**: Direct copy from "Unit" field

### 8. Skip Existing Invoices
- Before creating Sales Invoice, check if `Sales Invoice.name = {InvoiceNo}` exists
- If exists: Skip entire invoice, mark as "skipped" in summary
- If not exists: Proceed with creation

### 9. Sales Invoice Creation
- **Doctype**: Sales Invoice
- **name**: Use InvoiceNo from input
- **customer**: Customer ID from lookup
- **posting_date**: Converted Gregorian date
- **update_stock**: 1 (always)
- **driver**: Selected driver from UI
- **is_return**: 1 if InvoiceNo starts with "SRV", else 0
- **items**: Array of item lines with validated item_code
- **Status**: Draft (NOT submitted - only insert, do not submit)

## Error Handling

### Error CSV Format
When errors occur, generate a CSV with:
- All original input columns
- Additional column: "Error Message" (appended at end)

### Error Types:
1. **Customer Not Found**: "Customer '{name}' with PAN '{pan}' not found in system"
2. **Item Not Found**: "Item '{item_name}' not found in system"
3. **Date Conversion Error**: "Unable to convert Nepali date '{date}' to Gregorian"
4. **Invoice Creation Error**: "Error creating invoice: {error_message}"
5. **Validation Error**: "Validation failed: {error_message}"

### Error Handling Strategy:
- Continue processing remaining invoices even if one fails
- Accumulate errors for error CSV
- Include failed invoice in error count but not imported count

## Real-time Progress Updates

### Progress Events
Publish via `frappe.publish_realtime` with event name: `uploadsales_progress`

### Progress Data Structure:
```python
{
    "processed": 50,           # Number of invoices processed so far
    "total": 100,              # Total invoices to process
    "current_invoice": "8283-010755",  # Currently processing invoice
    "success_count": 45,       # Successfully imported
    "skipped_count": 3,        # Skipped (already exist)
    "error_count": 2,          # Failed with errors
    "total_amount": 250000.00, # Sum of grand_total for imported invoices
    "last_message": "Processing invoice 8283-010755..." # Status message
}
```

## Summary Report Structure
After completion, return:
```python
{
    "success": True,
    "total_attempted": 100,
    "imported_count": 95,
    "skipped_count": 3,
    "error_count": 2,
    "total_amount": 250000.00,
    "error_csv_path": "/files/upload_sales_errors_20251026.csv",
    "duration_seconds": 45.2
}
```

## Notes
- All monetary amounts in NPR (Nepali Rupees)
- VAT rate fixed at 13%
- Company assumed as "RTAS" based on sample data
- Cost Center and Income Account use "RTAS" suffix
- Date format in output must be DD/MM/YYYY (not YYYY-MM-DD)

