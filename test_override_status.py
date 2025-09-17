#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test to check and apply fixed valuation rate overrides
"""

import sys
import os

# Add the frappe-bench directory to the Python path
sys.path.insert(0, '/workspace/development/frappe-bench')

def test_and_apply_overrides():
    """
    Test if overrides are working and apply them if needed.
    """
    try:
        import frappe
        
        # Initialize Frappe
        frappe.init(site='development.localhost')
        frappe.connect()
        
        print("✅ Frappe connected successfully")
        
        # Test 1: Check if our functions can be imported
        try:
            from custom_erp.custom_erp.custom_erp.stock_valuation.stock_ledger_override import (
                get_valuation_rate,
                is_fixed_valuation_rate_enabled,
                apply_overrides
            )
            print("✅ Custom ERP overrides imported successfully")
            
            # Test 2: Check if feature is enabled
            enabled = is_fixed_valuation_rate_enabled()
            print(f"✅ Fixed valuation rate feature enabled: {enabled}")
            
            # Test 3: Apply overrides manually
            print("🔄 Applying overrides manually...")
            apply_overrides()
            print("✅ Overrides applied successfully")
            
            # Test 4: Check if overrides are working
            print("🔄 Testing if overrides are working...")
            
            # Get a test item
            items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
            if not items:
                print("❌ No stock items found for testing")
                return False
            
            test_item = items[0].name
            print(f"✅ Using test item: {test_item}")
            
            # Set a test valuation rate
            test_rate = 777.0
            frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
            print(f"✅ Set Item valuation_rate to: {test_rate}")
            
            # Test our override function directly
            result_rate = get_valuation_rate(
                item_code=test_item,
                warehouse="Test Warehouse",
                voucher_type="Purchase Invoice",
                voucher_no="TEST-001"
            )
            
            print(f"✅ Our get_valuation_rate result: {result_rate}")
            print(f"✅ Expected rate: {test_rate}")
            
            if abs(result_rate - test_rate) < 0.01:
                print("✅ Our override function is working!")
            else:
                print("❌ Our override function is NOT working!")
                return False
            
            # Test 5: Check if ERPNext's function is overridden
            print("🔄 Testing if ERPNext's function is overridden...")
            
            # Import ERPNext's function to see if it's overridden
            import erpnext.stock.stock_ledger
            erpnext_result = erpnext.stock.stock_ledger.get_valuation_rate(
                item_code=test_item,
                warehouse="Test Warehouse",
                voucher_type="Purchase Invoice",
                voucher_no="TEST-002"
            )
            
            print(f"✅ ERPNext's get_valuation_rate result: {erpnext_result}")
            
            if abs(erpnext_result - test_rate) < 0.01:
                print("🎉 SUCCESS: ERPNext's function is overridden!")
                return True
            else:
                print("❌ ERPNext's function is NOT overridden!")
                
                # Try to apply overrides again
                print("🔄 Trying to apply overrides again...")
                apply_overrides()
                
                # Test again
                erpnext_result2 = erpnext.stock.stock_ledger.get_valuation_rate(
                    item_code=test_item,
                    warehouse="Test Warehouse",
                    voucher_type="Purchase Invoice",
                    voucher_no="TEST-003"
                )
                
                print(f"✅ ERPNext's get_valuation_rate result after re-apply: {erpnext_result2}")
                
                if abs(erpnext_result2 - test_rate) < 0.01:
                    print("🎉 SUCCESS: Overrides working after re-apply!")
                    return True
                else:
                    print("❌ Overrides still not working!")
                    return False
                
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            frappe.destroy()
        except:
            pass

if __name__ == "__main__":
    success = test_and_apply_overrides()
    sys.exit(0 if success else 1)
