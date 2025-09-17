# -*- coding: utf-8 -*-
"""
Test script to be run in bench console to verify fixed valuation rate overrides
"""

def test_fixed_valuation_rate():
    """
    Test if the fixed valuation rate overrides are working.
    Run this in bench console: bench --site development.localhost console
    Then: exec(open('apps/custom_erp/test_console.py').read())
    """
    
    print("=== Testing Fixed Valuation Rate Overrides ===")
    
    # Test 1: Import our functions
    try:
        from custom_erp.custom_erp.custom_erp.stock_valuation.stock_ledger_override import (
            get_valuation_rate,
            is_fixed_valuation_rate_enabled,
            force_apply_overrides
        )
        print("✅ Custom ERP overrides imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Check if feature is enabled
    enabled = is_fixed_valuation_rate_enabled()
    print(f"✅ Fixed valuation rate feature enabled: {enabled}")
    
    # Test 3: Force apply overrides
    print("🔄 Force applying overrides...")
    success = force_apply_overrides()
    if not success:
        print("❌ Failed to apply overrides")
        return False
    
    # Test 4: Get a test item
    items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
    if not items:
        print("❌ No stock items found for testing")
        return False
    
    test_item = items[0].name
    print(f"✅ Using test item: {test_item}")
    
    # Test 5: Set a test valuation rate
    test_rate = 888.0
    frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
    print(f"✅ Set Item valuation_rate to: {test_rate}")
    
    # Test 6: Test our override function directly
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
    
    # Test 7: Check if ERPNext's function is overridden
    print("🔄 Testing if ERPNext's function is overridden...")
    
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
        print("🎉 FIXED VALUATION RATE IS WORKING!")
        return True
    else:
        print("❌ ERPNext's function is NOT overridden!")
        print("❌ Overrides are not working properly!")
        return False

# Run the test
if __name__ == "__main__":
    test_fixed_valuation_rate()
