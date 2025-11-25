# Custom Fields and Property Setters Summary

This document lists all custom fields and property setters that `custom_erp` app adds/modifies during installation.

## Custom Fields (custom_field.json)

### Address (2 fields)
1. **tax_category** (Tax Category) - Link field
   - Links to Tax Category doctype
   - Insert after: fax

2. **is_your_company_address** (Is Your Company Address) - Check field
   - Boolean field to mark company addresses
   - Insert after: linked_with

### Contact (1 field)
1. **is_billing_contact** (Is Billing Contact) - Check field
   - Boolean field to mark billing contacts
   - Insert after: is_primary_contact

### Print Settings (3 fields)
1. **compact_item_print** (Compact Item Print) - Check field
   - Default: 1 (enabled)
   - Insert after: with_letterhead

2. **print_uom_after_quantity** (Print UOM after Quantity) - Check field
   - Default: 0 (disabled)
   - Insert after: compact_item_print

3. **print_taxes_with_zero_amount** (Print taxes with zero amount) - Check field
   - Default: 0 (disabled)
   - Insert after: allow_print_for_cancelled

### Purchase Invoice (1 field)
1. **cust_bill_actual_amount** (Bill Actual Amount) - Currency field
   - Tracks actual bill amount
   - Insert after: rounded_total

### Purchase Invoice Item (2 fields)
1. **cust_leakage_qty** (Leakages) - Int field
   - Tracks leakage quantity
   - In list view: Yes
   - Non-negative: Yes
   - Insert after: qty

2. **cust_burst_qty** (Bursts) - Int field
   - Tracks burst quantity
   - In list view: Yes
   - Non-negative: Yes
   - Insert after: cust_leakage_qty

### Sales Invoice (2 fields)
1. **custom_vehicle_for_delivery** (Vehicle For Delivery) - Link field
   - Links to Vehicle doctype (from HRMS)
   - In list view: Yes
   - Module: Custom ERP
   - Insert after: customer

2. **custom_driver_for_vehicle** (Driver For Vehicle) - Link field
   - Links to Driver doctype (from HRMS)
   - In list view: Yes
   - Module: Custom ERP
   - Insert after: custom_vehicle_for_delivery

### Stock Reconciliation Item (1 field)
1. **entered_uom** (Entered UOM) - Link field
   - Links to UOM doctype
   - Fetches from: item_code.stock_uom
   - Fetch if empty: Yes
   - In list view: Yes
   - Insert after: qty

## Property Setters (property_setter.json)

### Sales Invoice (13 property setters)
1. **additional_discount_account.hidden** = 0 (show field)
2. **additional_discount_account.mandatory_depends_on** = `eval: doc.discount_amount`
3. **base_rounded_total.hidden** = 0
4. **base_rounded_total.print_hide** = 1
5. **rounded_total.hidden** = 0
6. **rounded_total.print_hide** = 0
7. **disable_rounded_total.default** = 0
8. **in_words.hidden** = 0
9. **in_words.print_hide** = 0
10. **tax_id.hidden** = 0
11. **tax_id.print_hide** = 0
12. **scan_barcode.hidden** = 0
13. **naming_series.options** = `ACC-SINV-.YYYY.-` and `ACC-SINV-RET-.YYYY.-`

### Sales Invoice Item (4 property setters)
1. **discount_account.hidden** = 0 (show field)
2. **discount_account.mandatory_depends_on** = `eval: doc.discount_amount`
3. **barcode.hidden** = 0
4. **target_warehouse.hidden** = 1

### Purchase Invoice (11 property setters)
1. **additional_discount_account.hidden** = 0 (show field) ⭐ NEW
2. **additional_discount_account.mandatory_depends_on** = `eval: doc.discount_amount` ⭐ NEW
3. **base_rounded_total.hidden** = 0
4. **base_rounded_total.print_hide** = 1
5. **rounded_total.hidden** = 0
6. **rounded_total.print_hide** = 0
7. **disable_rounded_total.default** = 0
8. **in_words.hidden** = 0
9. **in_words.print_hide** = 0
10. **scan_barcode.hidden** = 0
11. **naming_series.options** = `ACC-PINV-.YYYY.-` and `ACC-PINV-RET-.YYYY.-`

### Purchase Invoice Item (1 property setter)
1. **from_warehouse.hidden** = 1

## Missing Fields Check

To check if there are any custom fields in your database that are not in the fixtures, run:

```bash
bench --site [your-site-name] console
```

Then:
```python
exec(open('apps/custom_erp/export_missing_fields.py').read())
```

This will export Purchase Invoice custom fields to a JSON file for review.

## Installation Notes

- All custom fields are synced during `bench install-app` and `bench migrate`
- Property setters modify existing ERPNext fields (they don't create new fields)
- The `additional_discount_account` field in Purchase Invoice is a **standard ERPNext field** that is hidden by default. The property setters make it visible and mandatory when discount is applied.

## Missing Purchase Invoice Discount Account Field?

The `additional_discount_account` field in Purchase Invoice is a **standard ERPNext field**, not a custom field. It exists in ERPNext by default but is hidden.

The property setters we added will:
- Show the field (hidden = 0)
- Make it mandatory when discount_amount is set (mandatory_depends_on)

If you had created a **custom field** (not property setter) for discount account in Purchase Invoice, you'll need to export it from your development database and add it to `custom_field.json`.

