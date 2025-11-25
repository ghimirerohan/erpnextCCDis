# Sales Invoice Rate Fix Summary

## Problem Identified

The Sales Invoice was incorrectly using `valuation_rate` (purchase price) instead of `standard_rate` (selling price) for the `rate` and `base_rate` fields, despite the custom override in `before_insert` setting these correctly.

## Root Cause

The issue was caused by **multiple hooks** in the stock valuation system that were overriding the rates set in the Sales Invoice `before_insert` method:

1. **`before_save`** hook: `ensure_fixed_valuation_rate`
2. **`on_submit`** hook: `ensure_fixed_valuation_rate`  
3. **`before_insert`** hook: `ensure_fixed_valuation_rate_before_gl_creation`
4. **GL Entry Override**: `override_stock_controller_get_gl_entries`

These functions were designed to use `valuation_rate` for stock valuation purposes but were also overwriting the `rate` and `base_rate` fields that should use `standard_rate` for selling.

## Solution Applied

Modified the stock valuation override functions to **preserve** the `rate` and `base_rate` fields for Sales Invoice documents while still updating `valuation_rate` for stock valuation purposes.

### Files Modified

1. **`custom_erp/custom_erp/stock_valuation/stock_ledger_override.py`**
   - `ensure_fixed_valuation_rate_before_gl_creation()` - Added Sales Invoice check
   - `ensure_fixed_valuation_rate()` - Added Sales Invoice check  
   - `override_stock_controller_get_gl_entries()` - Added Sales Invoice check

2. **`custom_erp/custom_erp/sales_invoice/sales_invoice.py`**
   - Added logging for debugging
   - Added documentation header

### Key Changes

```python
# Before (problematic code):
item.rate = valuation_rate
item.base_rate = valuation_rate

# After (fixed code):
if doc.doctype == "Sales Invoice":
    # Don't override rate and base_rate for Sales Invoice
    # These should remain as standard_rate (selling price)
    pass
else:
    # For other doctypes, update the item's rate
    item.rate = valuation_rate
    item.base_rate = valuation_rate
```

## Result

- **Sales Invoice**: Now correctly uses `standard_rate` (selling price) for `rate` and `base_rate`
- **Other Documents**: Continue to use `valuation_rate` (purchase price) for stock valuation
- **Stock Valuation**: Still works correctly using `valuation_rate` for inventory calculations
- **GL Entries**: Sales Invoice GL entries now use the correct selling rates

## Testing

To verify the fix works:

1. Create a new Sales Invoice
2. Check that `rate` and `base_rate` are set to `standard_rate` from Item master
3. Verify that `valuation_rate` is set to the Item's `valuation_rate` for stock purposes
4. Submit the document and confirm rates remain unchanged
5. Check GL entries use the correct selling rates

## Logging

Added logging to help debug any future issues:
- Sales Invoice `before_insert` logs the rates being set
- Stock valuation functions log when they detect Sales Invoice and preserve rates

## Important Notes

- This fix **only affects Sales Invoice** documents
- All other stock transactions (Purchase Invoice, Stock Entry, etc.) continue to work as before
- The `valuation_rate` field is still updated for stock valuation purposes
- No changes were made to the core ERPNext logic
