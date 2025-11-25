#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test for fixed valuation rate overrides
"""

import sys
import os

# Add the frappe-bench directory to the Python path
sys.path.insert(0, '/workspace/development/frappe-bench')

def test_fixed_valuation_rate():
    """
    Test if the fixed valuation rate overrides are working.
    """
    try:
        import frappe
        
        # Initialize Frappe
        frappe.init(site='development.localhost')
        frappe.connect()
        
        print("✅ Frappe connected successfully")
        
        # Test if our app is working
        try:
            from custom_erp.custom_erp.custom_erp.stock_valuation.stock_ledger_override import (
                get_valuation_rate,
                is_fixed_valuation_rate_enabled
            )
            print("✅ Custom ERP overrides imported successfully")
            
            # Test if feature is enabled
            enabled = is_fixed_valuation_rate_enabled()
            print(f"✅ Fixed valuation rate feature enabled: {enabled}")
            
            # Get a test item
            items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
            if not items:
                print("❌ No stock items found for testing")
                return False
            
            test_item = items[0].name
            print(f"✅ Using test item: {test_item}")
            
            # Set a test valuation rate
            test_rate = 999.0
            frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
            print(f"✅ Set Item valuation_rate to: {test_rate}")
            
            # Test the override function
            result_rate = get_valuation_rate(
                item_code=test_item,
                warehouse="Test Warehouse",
                voucher_type="Purchase Invoice",
                voucher_no="TEST-001"
            )
            
            print(f"✅ get_valuation_rate result: {result_rate}")
            print(f"✅ Expected rate: {test_rate}")
            
            if abs(result_rate - test_rate) < 0.01:
                print("🎉 SUCCESS: Fixed valuation rate override is working!")
                return True
            else:
                print("❌ FAILED: Fixed valuation rate override is NOT working!")
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
    success = test_fixed_valuation_rate()
    sys.exit(0 if success else 1)
