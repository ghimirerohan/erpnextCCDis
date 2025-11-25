# -*- coding: utf-8 -*-
"""
Simple test for fixed valuation rate
"""

import frappe

def test_simple():
    """
    Simple test to verify fixed valuation rate is working.
    """
    print("Testing Fixed Valuation Rate...")
    
    try:
        # Get a test item
        items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
        if not items:
            print("   ⚠️  No stock items found for testing")
            return False
        
        test_item = items[0].name
        print(f"   Using test item: {test_item}")
        
        # Set a test valuation rate
        test_rate = 500.0
        frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
        print(f"   Set Item valuation_rate to: {test_rate}")
        
        # Test the override function directly
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import get_valuation_rate
        
        result_rate = get_valuation_rate(
            item_code=test_item,
            warehouse="Test Warehouse",
            voucher_type="Purchase Invoice",
            voucher_no="TEST-001"
        )
        
        print(f"   get_valuation_rate result: {result_rate}")
        print(f"   Expected rate: {test_rate}")
        
        if abs(result_rate - test_rate) < 0.01:
            print("   ✅ Fixed valuation rate override is working!")
            return True
        else:
            print("   ❌ Fixed valuation rate override is NOT working!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
