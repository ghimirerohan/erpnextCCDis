#!/usr/bin/env python3
"""
Script to check custom fields and identify missing ones.
Run this in bench console or as a management command.
"""

import json
import sys
from pathlib import Path

def get_fixture_fields():
    """Get all custom fields from fixtures."""
    app_dir = Path(__file__).parent
    fixture_path = app_dir / "custom_erp" / "fixtures" / "custom_field.json"
    
    with open(fixture_path, 'r') as f:
        return json.load(f)

def get_property_setters():
    """Get all property setters from fixtures."""
    app_dir = Path(__file__).parent
    fixture_path = app_dir / "custom_erp" / "fixtures" / "property_setter.json"
    
    with open(fixture_path, 'r') as f:
        return json.load(f)

def analyze_fixtures():
    """Analyze what's in fixtures."""
    fields = get_fixture_fields()
    setters = get_property_setters()
    
    print("=" * 70)
    print("CUSTOM FIELDS IN FIXTURES (custom_field.json)")
    print("=" * 70)
    
    by_doctype = {}
    for field in fields:
        dt = field.get('dt', 'Unknown')
        if dt not in by_doctype:
            by_doctype[dt] = []
        by_doctype[dt].append(field)
    
    for dt in sorted(by_doctype.keys()):
        print(f"\n{dt} ({len(by_doctype[dt])} fields):")
        for field in by_doctype[dt]:
            print(f"  - {field.get('fieldname')} ({field.get('label')}) [{field.get('fieldtype')}]")
    
    print("\n" + "=" * 70)
    print("PROPERTY SETTERS IN FIXTURES (property_setter.json)")
    print("=" * 70)
    
    by_doctype_ps = {}
    for setter in setters:
        dt = setter.get('doc_type', 'Unknown')
        if dt not in by_doctype_ps:
            by_doctype_ps[dt] = []
        by_doctype_ps[dt].append(setter)
    
    for dt in sorted(by_doctype_ps.keys()):
        print(f"\n{dt} ({len(by_doctype_ps[dt])} property setters):")
        for ps in by_doctype_ps[dt]:
            field_name = ps.get('field_name', 'N/A')
            property_name = ps.get('property', 'N/A')
            print(f"  - {field_name}.{property_name} = {ps.get('value', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total Custom Fields: {len(fields)}")
    print(f"Total Property Setters: {len(setters)}")
    print(f"Doctypes with Custom Fields: {len(by_doctype)}")
    print(f"Doctypes with Property Setters: {len(by_doctype_ps)}")
    
    # Check for Purchase Invoice discount
    print("\n" + "=" * 70)
    print("PURCHASE INVOICE DISCOUNT FIELD CHECK")
    print("=" * 70)
    pi_fields = by_doctype.get('Purchase Invoice', [])
    pi_item_fields = by_doctype.get('Purchase Invoice Item', [])
    pi_setters = by_doctype_ps.get('Purchase Invoice', [])
    
    print(f"\nPurchase Invoice Custom Fields: {len(pi_fields)}")
    for field in pi_fields:
        if 'discount' in field.get('fieldname', '').lower() or 'discount' in field.get('label', '').lower():
            print(f"  ⚠️  DISCOUNT-RELATED: {field.get('fieldname')} - {field.get('label')}")
    
    print(f"\nPurchase Invoice Property Setters: {len(pi_setters)}")
    for ps in pi_setters:
        if 'discount' in ps.get('field_name', '').lower():
            print(f"  ⚠️  DISCOUNT-RELATED: {ps.get('field_name')}.{ps.get('property')}")
    
    # Check Sales Invoice for comparison
    si_fields = by_doctype.get('Sales Invoice', [])
    si_setters = by_doctype_ps.get('Sales Invoice', [])
    
    print(f"\nSales Invoice Custom Fields: {len(si_fields)}")
    print(f"Sales Invoice Property Setters: {len(si_setters)}")
    for ps in si_setters:
        if 'discount' in ps.get('field_name', '').lower():
            print(f"  ✅ DISCOUNT-RELATED (Sales Invoice): {ps.get('field_name')}.{ps.get('property')}")
    
    print("\n" + "=" * 70)
    print("NOTE: If Purchase Invoice discount_account field exists in your database")
    print("but not in fixtures, it needs to be added to custom_field.json")
    print("=" * 70)

if __name__ == "__main__":
    analyze_fixtures()

