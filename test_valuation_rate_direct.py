#!/usr/bin/env python3
"""
Direct test script for Fixed Valuation Rate Override

This script directly tests the valuation rate functions to ensure they're working.
"""

import frappe
import sys

def test_valuation_rate_functions():
    """
    Test the valuation rate functions directly.
    """
    print("Testing Fixed Valuation Rate Functions Directly...")
    
    # Test 1: Test get_valuation_rate function
    print("\n1. Testing get_valuation_rate function...")
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
        test_rate = 150.0
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
            print("   ✅ get_valuation_rate working correctly!")
        else:
            print("   ❌ get_valuation_rate not working correctly!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing get_valuation_rate: {e}")
        return False
    
    # Test 2: Test get_incoming_rate function
    print("\n2. Testing get_incoming_rate function...")
    try:
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import get_incoming_rate
        
        # Test the function
        args = {
            "item_code": test_item,
            "warehouse": "Test Warehouse",
            "voucher_type": "Purchase Invoice",
            "voucher_no": "TEST-002"
        }
        
        result_rate = get_incoming_rate(args)
        
        print(f"   Expected rate: {test_rate}")
        print(f"   Actual rate: {result_rate}")
        
        if abs(result_rate - test_rate) < 0.01:
            print("   ✅ get_incoming_rate working correctly!")
        else:
            print("   ❌ get_incoming_rate not working correctly!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing get_incoming_rate: {e}")
        return False
    
    # Test 3: Test get_valuation_rate_for_item_details function
    print("\n3. Testing get_valuation_rate_for_item_details function...")
    try:
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import get_valuation_rate_for_item_details
        
        # Test the function
        result = get_valuation_rate_for_item_details(
            item_code=test_item,
            company="Test Company",
            warehouse="Test Warehouse"
        )
        
        print(f"   Expected rate: {test_rate}")
        print(f"   Actual rate: {result.get('valuation_rate', 0)}")
        
        if abs(result.get('valuation_rate', 0) - test_rate) < 0.01:
            print("   ✅ get_valuation_rate_for_item_details working correctly!")
        else:
            print("   ❌ get_valuation_rate_for_item_details not working correctly!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing get_valuation_rate_for_item_details: {e}")
        return False
    
    # Test 4: Test fallback to standard_rate
    print("\n4. Testing fallback to standard_rate...")
    try:
        # Clear valuation_rate and set standard_rate
        frappe.db.set_value("Item", test_item, "valuation_rate", 0)
        standard_rate = 75.0
        frappe.db.set_value("Item", test_item, "standard_rate", standard_rate)
        
        result_rate = get_valuation_rate(
            item_code=test_item,
            warehouse="Test Warehouse",
            voucher_type="Purchase Invoice",
            voucher_no="TEST-003"
        )
        
        print(f"   Expected rate (standard_rate): {standard_rate}")
        print(f"   Actual rate: {result_rate}")
        
        if abs(result_rate - standard_rate) < 0.01:
            print("   ✅ Fallback to standard_rate working correctly!")
        else:
            print("   ❌ Fallback to standard_rate not working correctly!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing fallback: {e}")
        return False
    
    print("\n🎉 All valuation rate function tests passed!")
    return True

def test_override_status():
    """
    Test if the overrides are properly configured.
    """
    print("\nTesting Override Configuration...")
    
    # Check if the overrides are in hooks.py
    try:
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import is_fixed_valuation_rate_enabled
        enabled = is_fixed_valuation_rate_enabled()
        print(f"   ✅ Feature enabled: {enabled}")
        
        if not enabled:
            print("   ⚠️  Feature should be enabled!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking feature status: {e}")
        return False
    
    print("   ✅ Override configuration looks good!")
    return True

if __name__ == "__main__":
    if not frappe.db:
        print("❌ This script must be run from within Frappe bench")
        sys.exit(1)
    
    success1 = test_override_status()
    success2 = test_valuation_rate_functions()
    
    if success1 and success2:
        print("\n✅ Fixed Valuation Rate Override is working correctly!")
        print("\nNext steps:")
        print("1. Set valuation_rate in your Item masters")
        print("2. Create a stock transaction (Purchase Invoice, Sales Invoice, etc.)")
        print("3. Check that the valuation rate in SLE uses the fixed rate from Item master")
        print("4. Verify that COGS and Stock in Hand calculations use the fixed rate")
    else:
        print("\n❌ Fixed Valuation Rate Override has issues that need to be resolved.")
        sys.exit(1)
