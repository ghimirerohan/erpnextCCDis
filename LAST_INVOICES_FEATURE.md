# Last Invoices Feature

## Overview
This feature adds the ability to view the last 3 invoices (purchase or sales) directly from the Scanner page. The feature dynamically changes based on the selected invoice type.

## Features

### Frontend Changes (Scanner.vue)
1. **New Button**: Added "View Last 3 Purchase/Sales Invoices" button that changes text based on selected invoice type
2. **Modal Dialog**: Added a responsive modal dialog to display invoice data
3. **Dynamic Content**: Button text and data source change based on invoice type selection (purchase/sales)

### Backend Changes
1. **Purchase Invoice API**: Added `get_last_invoices()` function in `purchase_invoice/api.py`
2. **Sales Invoice API**: Added `get_last_invoices()` function in `sales_invoice/api.py`

## Functionality

### Button Behavior
- Button text changes dynamically: "View Last 3 Purchase Invoices" or "View Last 3 Sales Invoices"
- Button is disabled when no invoice type is selected
- Shows loading state while fetching data

### Data Display
Each invoice shows:
- **Invoice Name**: The document name (e.g., ACC-PINV-.YYYY.-00001)
- **Posting Date**: Formatted date (e.g., "15 Dec 2024")
- **Amount**: Grand total with Indian currency formatting (₹1,234.56)
- **Status**: Color-coded status badges (Draft, Submitted, Cancelled)
- **Supplier/Customer**: Party name (dynamically shows based on invoice type)
- **Invoice Number**: External invoice number (bill_no field)

### API Endpoints
- **Purchase**: `/api/method/custom_erp.custom_erp.purchase_invoice.api.get_last_invoices`
- **Sales**: `/api/method/custom_erp.custom_erp.sales_invoice.api.get_last_invoices`

### Data Filtering
- Returns last 3 invoices by posting date (most recent first)
- Excludes cancelled invoices (docstatus != 2)
- Includes only essential fields for performance

## Usage

1. **Select Invoice Type**: Choose between "Purchase" or "Sales" radio button
2. **Click Button**: Click "View Last 3 [Type] Invoices" button
3. **View Data**: Modal opens showing the last 3 invoices with key details
4. **Close**: Click "Close" button or click outside modal to dismiss

## Technical Details

### Frontend Components
- Reactive variables for dialog state and data
- Loading states and error handling
- Responsive grid layout for invoice display
- Status badges with appropriate styling

### Backend Functions
- Whitelisted API endpoints
- Proper error handling and logging
- Efficient database queries using `frappe.get_all()`
- Consistent response format

### Styling
- Tailwind CSS classes for responsive design
- Hover effects and transitions
- Color-coded status indicators
- Mobile-friendly layout

## Error Handling
- Network errors are caught and displayed to user
- Empty state handling when no invoices exist
- Loading states during API calls
- Graceful fallbacks for missing data

## Future Enhancements
- Pagination for viewing more invoices
- Filtering by date range
- Export functionality
- Direct links to invoice documents
- Real-time updates
