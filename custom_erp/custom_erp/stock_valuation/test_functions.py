# -*- coding: utf-8 -*-
"""
Test functions for Fixed Valuation Rate Override
"""

import frappe

def test_gl_entries_with_fixed_rate():
    """
    Test that GL entries use the fixed valuation rate.
    """
    print("\nTesting GL entries with fixed valuation rate...")
    
    try:
        # Get a test item
        items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
        if not items:
            print("   ⚠️  No stock items found for testing")
            return False
        
        test_item = items[0].name
        print(f"   Using test item: {test_item}")
        
        # Set a test valuation rate
        test_rate = 250.0
        frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
        
        # Create a test Purchase Invoice
        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = frappe.get_all("Supplier", limit=1)[0].name
        pi.company = frappe.get_all("Company", limit=1)[0].name
        
        pi.append("items", {
            "item_code": test_item,
            "qty": 5,
            "rate": 100,  # This should be overridden by our fixed rate
            "warehouse": frappe.get_all("Warehouse", limit=1)[0].name
        })
        
        # Save and submit the document
        pi.save()
        pi.submit()
        
        # Check Stock Ledger Entry
        sle = frappe.get_all("Stock Ledger Entry", 
                            filters={"voucher_no": pi.name, "item_code": test_item},
                            fields=["valuation_rate", "stock_value_difference", "actual_qty"])
        
        if sle:
            sle = sle[0]
            print(f"   SLE valuation_rate: {sle.valuation_rate}")
            print(f"   SLE stock_value_difference: {sle.stock_value_difference}")
            print(f"   Expected valuation_rate: {test_rate}")
            print(f"   Expected stock_value_difference: {test_rate * 5}")
            
            if abs(sle.valuation_rate - test_rate) < 0.01:
                print("   ✅ SLE using fixed valuation rate!")
            else:
                print("   ❌ SLE not using fixed valuation rate!")
                return False
        
        # Check General Ledger Entry
        gl_entries = frappe.get_all("GL Entry", 
                                   filters={"voucher_no": pi.name},
                                   fields=["account", "debit", "credit", "remarks"])
        
        if gl_entries:
            print(f"   Found {len(gl_entries)} GL entries")
            for gl in gl_entries:
                print(f"   GL Entry: {gl.account} - Debit: {gl.debit}, Credit: {gl.credit}")
                if "Stock" in gl.remarks:
                    print(f"   Stock GL Entry amount: {gl.debit or gl.credit}")
                    expected_amount = test_rate * 5
                    if abs((gl.debit or gl.credit) - expected_amount) < 0.01:
                        print("   ✅ GL Entry using fixed valuation rate!")
                    else:
                        print("   ❌ GL Entry not using fixed valuation rate!")
                        return False
        
        # Clean up
        pi.cancel()
        pi.delete()
        
    except Exception as e:
        print(f"   ❌ Error testing GL entries: {e}")
        return False
    
    return True

def test_comprehensive_fixed_rate():
    """
    Comprehensive test to verify all aspects of fixed valuation rate are working.
    """
    print("\n=== COMPREHENSIVE FIXED VALUATION RATE TEST ===")
    
    try:
        # Get a test item
        items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
        if not items:
            print("   ⚠️  No stock items found for testing")
            return False
        
        test_item = items[0].name
        print(f"   Using test item: {test_item}")
        
        # Set a test valuation rate
        test_rate = 300.0
        frappe.db.set_value("Item", test_item, "valuation_rate", test_rate)
        print(f"   Set Item valuation_rate to: {test_rate}")
        
        # Test 1: Purchase Invoice
        print("\n1. Testing Purchase Invoice...")
        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = frappe.get_all("Supplier", limit=1)[0].name
        pi.company = frappe.get_all("Company", limit=1)[0].name
        
        pi.append("items", {
            "item_code": test_item,
            "qty": 10,
            "rate": 50,  # This should be overridden
            "warehouse": frappe.get_all("Warehouse", limit=1)[0].name
        })
        
        pi.save()
        print(f"   PI Item rate after save: {pi.items[0].rate}")
        
        pi.submit()
        
        # Check SLE
        sle = frappe.get_all("Stock Ledger Entry", 
                            filters={"voucher_no": pi.name, "item_code": test_item},
                            fields=["valuation_rate", "stock_value_difference", "actual_qty"])
        
        if sle:
            sle = sle[0]
            print(f"   SLE valuation_rate: {sle.valuation_rate}")
            print(f"   SLE stock_value_difference: {sle.stock_value_difference}")
            expected_sle_value = test_rate * 10
            print(f"   Expected SLE value: {expected_sle_value}")
            
            if abs(sle.valuation_rate - test_rate) < 0.01 and abs(sle.stock_value_difference - expected_sle_value) < 0.01:
                print("   ✅ Purchase Invoice SLE using fixed rate!")
            else:
                print("   ❌ Purchase Invoice SLE not using fixed rate!")
                return False
        
        # Check GL entries
        gl_entries = frappe.get_all("GL Entry", 
                                   filters={"voucher_no": pi.name},
                                   fields=["account", "debit", "credit", "remarks"])
        
        stock_gl_found = False
        for gl in gl_entries:
            if "Stock" in gl.remarks:
                stock_gl_found = True
                gl_amount = gl.debit or gl.credit
                expected_gl_amount = test_rate * 10
                print(f"   Stock GL Entry amount: {gl_amount}")
                print(f"   Expected GL amount: {expected_gl_amount}")
                
                if abs(gl_amount - expected_gl_amount) < 0.01:
                    print("   ✅ Purchase Invoice GL using fixed rate!")
                else:
                    print("   ❌ Purchase Invoice GL not using fixed rate!")
                    return False
        
        if not stock_gl_found:
            print("   ⚠️  No stock GL entries found")
        
        # Test 2: Sales Invoice (COGS)
        print("\n2. Testing Sales Invoice (COGS)...")
        si = frappe.new_doc("Sales Invoice")
        si.customer = frappe.get_all("Customer", limit=1)[0].name
        si.company = frappe.get_all("Company", limit=1)[0].name
        
        si.append("items", {
            "item_code": test_item,
            "qty": 5,
            "rate": 400,  # Selling rate
            "warehouse": frappe.get_all("Warehouse", limit=1)[0].name
        })
        
        si.save()
        si.submit()
        
        # Check COGS GL entries
        cogs_gl_entries = frappe.get_all("GL Entry", 
                                        filters={"voucher_no": si.name, "remarks": ["like", "%COGS%"]},
                                        fields=["account", "debit", "credit", "remarks"])
        
        if cogs_gl_entries:
            for gl in cogs_gl_entries:
                cogs_amount = gl.debit or gl.credit
                expected_cogs = test_rate * 5
                print(f"   COGS GL Entry amount: {cogs_amount}")
                print(f"   Expected COGS amount: {expected_cogs}")
                
                if abs(cogs_amount - expected_cogs) < 0.01:
                    print("   ✅ Sales Invoice COGS using fixed rate!")
                else:
                    print("   ❌ Sales Invoice COGS not using fixed rate!")
                    return False
        
        print("\n🎉 ALL TESTS PASSED! Fixed valuation rate is working correctly!")
        print(f"   - SLE using fixed rate: {test_rate}")
        print(f"   - GL entries using fixed rate: {test_rate}")
        print(f"   - COGS using fixed rate: {test_rate}")
        
        # Clean up
        si.cancel()
        si.delete()
        pi.cancel()
        pi.delete()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in comprehensive test: {e}")
        return False
