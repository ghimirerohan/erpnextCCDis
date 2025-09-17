# Fixed Valuation Rate Override for ERPNext

## Overview

This module overrides ERPNext's default stock valuation logic to always use the fixed rate from the Item master's `valuation_rate` field for all stock valuation calculations. This ensures that the valuation rate remains constant and does not change based on purchases, stock additions, or any other transaction.

## Key Features

- **Fixed Valuation Rate**: Always uses `Item.valuation_rate` for all stock transactions
- **Configurable**: Can be enabled/disabled via Custom ERP Settings
- **Comprehensive Coverage**: Works across all stock transaction types (Purchase, Sales, Stock Entry, etc.)
- **Fallback Logic**: Falls back to `standard_rate` and `Item Price` if `valuation_rate` is not set
- **Error Handling**: Provides clear error messages when valuation rates are missing
- **Backward Compatible**: Falls back to original ERPNext logic when feature is disabled

## Installation and Setup

1. Install the Custom ERP app
2. Migrate the app
3. Access Custom ERP Settings
4. Enable "Fixed Valuation Rate" feature

## Usage

Set the `valuation_rate` field in Item master. All stock transactions will automatically use this fixed rate for valuation and COGS calculations.

## Technical Details

- Monkey patches the following to always use Item.valuation_rate:
  - `erpnext.stock.stock_ledger.get_valuation_rate`
  - `erpnext.stock.utils.get_incoming_rate`
  - `erpnext.stock.stock_ledger.get_incoming_rate_for_return_entry`
  - `erpnext.controllers.stock_controller.StockController.get_gl_entries`
  - `erpnext.stock.get_item_details.get_valuation_rate` (via hook for UI/item details)
- Applies overrides at import and on session creation/after migrate via hooks.
- Document events ensure rows (`Purchase Invoice`, `Sales Invoice`, `Delivery Note`, `Stock Entry`, `Purchase Receipt`) and `Stock Ledger Entry` have `valuation_rate` enforced before insert/GL.

Notes:
- If `Item.valuation_rate` is empty, falls back to `standard_rate`, then buying `Item Price`.
- Throws a descriptive error if a non-zero rate is required but missing.
