#!/usr/bin/env python3
"""
Export custom fields from database that might be missing from fixtures.
Run this in bench console: bench --site [site-name] console
Then: exec(open('apps/custom_erp/export_missing_fields.py').read())
"""

import frappe
import json

def export_custom_fields():
    """Export all custom fields from database."""
    print("=" * 70)
    print("EXPORTING CUSTOM FIELDS FROM DATABASE")
    print("=" * 70)
    
    # Get all custom fields
    custom_fields = frappe.get_all(
        "Custom Field",
        fields=["*"],
        order_by="dt, fieldname"
    )
    
    # Group by doctype
    by_doctype = {}
    for cf in custom_fields:
        dt = cf.get('dt', 'Unknown')
        if dt not in by_doctype:
            by_doctype[dt] = []
        by_doctype[dt].append(cf)
    
    print(f"\nTotal Custom Fields in Database: {len(custom_fields)}")
    print(f"Doctypes: {len(by_doctype)}")
    
    # Check for Purchase Invoice discount fields
    print("\n" + "=" * 70)
    print("PURCHASE INVOICE CUSTOM FIELDS")
    print("=" * 70)
    
    pi_fields = by_doctype.get('Purchase Invoice', [])
    print(f"\nFound {len(pi_fields)} custom fields for Purchase Invoice:")
    for field in pi_fields:
        print(f"\n  Field: {field.get('fieldname')}")
        print(f"    Label: {field.get('label')}")
        print(f"    Type: {field.get('fieldtype')}")
        print(f"    Insert After: {field.get('insert_after')}")
        print(f"    Module: {field.get('module')}")
        if 'discount' in field.get('fieldname', '').lower() or 'discount' in field.get('label', '').lower():
            print(f"    ⚠️  THIS IS A DISCOUNT-RELATED FIELD!")
            print(f"\n    Full JSON:")
            print(json.dumps(field, indent=6, default=str))
    
    print("\n" + "=" * 70)
    print("PURCHASE INVOICE PROPERTY SETTERS")
    print("=" * 70)
    
    pi_property_setters = frappe.get_all(
        "Property Setter",
        filters={"doc_type": "Purchase Invoice"},
        fields=["*"],
        order_by="field_name, property"
    )
    
    print(f"\nFound {len(pi_property_setters)} property setters for Purchase Invoice:")
    for ps in pi_property_setters:
        field_name = ps.get('field_name', 'N/A')
        if 'discount' in field_name.lower():
            print(f"\n  ⚠️  DISCOUNT-RELATED: {field_name}.{ps.get('property')}")
            print(f"    Value: {ps.get('value')}")
            print(f"    Full JSON:")
            print(json.dumps(ps, indent=6, default=str))
    
    # Export to JSON file for easy comparison
    export_data = {
        'purchase_invoice_custom_fields': by_doctype.get('Purchase Invoice', []),
        'purchase_invoice_property_setters': pi_property_setters,
    }
    
    export_file = frappe.get_site_path('purchase_invoice_fields_export.json')
    with open(export_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"\n✅ Exported to: {export_file}")
    print("\nReview this file to see what fields/property setters exist")
    print("in your database but might be missing from fixtures.")

if __name__ == "__main__":
    export_custom_fields()
else:
    # Running in bench console
    try:
        export_custom_fields()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

