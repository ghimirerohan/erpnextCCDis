#!/usr/bin/env python3
"""
Test script for Fixed Valuation Rate Override

This script tests the fixed valuation rate functionality to ensure it's working correctly.
"""

import frappe
import sys

def test_fixed_valuation_rate():
    """
    Test the fixed valuation rate functionality.
    """
    print("Testing Fixed Valuation Rate Override...")
    
    # Test 1: Check if feature is enabled by default
    print("\n1. Testing feature status...")
    try:
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import is_fixed_valuation_rate_enabled
        enabled = is_fixed_valuation_rate_enabled()
        print(f"   ✅ Feature enabled: {enabled}")
        if not enabled:
            print("   ⚠️  Feature should be enabled by default!")
    except Exception as e:
        print(f"   ❌ Error checking feature status: {e}")
        return False
    
    # Test 2: Test get_valuation_rate function
    print("\n2. Testing get_valuation_rate function...")
    try:
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import get_valuation_rate
        
        # Get a test item
        items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
        if not items:
            print("   ⚠️  No stock items found for testing")
            return False
        
        test_item = items[0].name
        print(f"   Using test item: {test_item}")
        
        # Set a test valuation rate
        test_rate = 100.0
        frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
        
        # Test the function
        result_rate = get_valuation_rate(
            item_code=test_item,
            warehouse="Test Warehouse",
            voucher_type="Purchase Invoice",
            voucher_no="TEST-001"
        )
        
        print(f"   Expected rate: {test_rate}")
        print(f"   Actual rate: {result_rate}")
        
        if abs(result_rate - test_rate) < 0.01:
            print("   ✅ Fixed valuation rate working correctly!")
        else:
            print("   ❌ Fixed valuation rate not working correctly!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing get_valuation_rate: {e}")
        return False
    
    print("\n🎉 All tests passed! Fixed Valuation Rate Override is working correctly.")
    return True

def check_items_without_valuation_rate():
    """
    Check for items that don't have valuation_rate set.
    """
    print("\nChecking items without valuation_rate...")
    
    items = frappe.db.sql("""
        SELECT name, item_name, item_group, valuation_rate, standard_rate
        FROM `tabItem`
        WHERE (valuation_rate IS NULL OR valuation_rate = 0)
        AND (standard_rate IS NULL OR standard_rate = 0)
        AND is_stock_item = 1
        ORDER BY item_name
        LIMIT 10
    """, as_dict=True)
    
    if items:
        print(f"⚠️  Found {len(items)} items without valuation_rate:")
        for item in items:
            print(f"   - {item.item_name} ({item.name})")
        print("\nPlease set valuation_rate or standard_rate for these items.")
    else:
        print("✅ All stock items have valuation rates set.")

if __name__ == "__main__":
    if not frappe.db:
        print("❌ This script must be run from within Frappe bench")
        sys.exit(1)
    
    success = test_fixed_valuation_rate()
    check_items_without_valuation_rate()
    
    if success:
        print("\n✅ Fixed Valuation Rate Override is ready for use!")
    else:
        print("\n❌ Fixed Valuation Rate Override has issues that need to be resolved.")
        sys.exit(1)
