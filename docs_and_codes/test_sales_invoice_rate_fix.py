#!/usr/bin/env python3
"""
Test script to verify Sales Invoice rate fix

This script tests that Sales Invoice items correctly use standard_rate 
instead of valuation_rate for rate and base_rate fields.
"""

import frappe
import sys
import os

def test_sales_invoice_rate_fix():
    """Test that Sales Invoice uses standard_rate instead of valuation_rate"""
    
    print("Testing Sales Invoice rate fix...")
    
    try:
        # Get a test item
        items = frappe.get_all("Item", filters={"is_stock_item": 1}, limit=1)
        if not items:
            print("No stock items found. Please create at least one stock item.")
            return False
            
        item_code = items[0].name
        item_doc = frappe.get_doc("Item", item_code)
        
        print(f"Testing with item: {item_code}")
        print(f"  Standard Rate: {item_doc.standard_rate}")
        print(f"  Valuation Rate: {item_doc.valuation_rate}")
        
        # Create a test Sales Invoice
        si = frappe.new_doc("Sales Invoice")
        si.customer = frappe.get_all("Customer", limit=1)[0].name
        si.company = frappe.get_all("Company", limit=1)[0].name
        si.posting_date = frappe.utils.today()
        si.due_date = frappe.utils.add_days(frappe.utils.today(), 30)
        
        # Add item
        si.append("items", {
            "item_code": item_code,
            "qty": 1,
            "uom": "Nos"
        })
        
        print("\nBefore insert:")
        print(f"  Item rate: {si.items[0].rate}")
        print(f"  Item base_rate: {si.items[0].base_rate}")
        print(f"  Item valuation_rate: {si.items[0].valuation_rate}")
        
        # Trigger before_insert
        si.before_insert()
        
        print("\nAfter before_insert:")
        print(f"  Item rate: {si.items[0].rate}")
        print(f"  Item base_rate: {si.items[0].base_rate}")
        print(f"  Item valuation_rate: {si.items[0].valuation_rate}")
        
        # Check if rates are correct
        if si.items[0].rate == item_doc.standard_rate:
            print("✓ Rate correctly set to standard_rate")
        else:
            print(f"✗ Rate incorrectly set to {si.items[0].rate}, expected {item_doc.standard_rate}")
            return False
            
        if si.items[0].base_rate == item_doc.standard_rate:
            print("✓ Base rate correctly set to standard_rate")
        else:
            print(f"✗ Base rate incorrectly set to {si.items[0].base_rate}, expected {item_doc.standard_rate}")
            return False
            
        # Test stock valuation hooks (they should preserve rates for Sales Invoice)
        from custom_erp.custom_erp.stock_valuation.stock_ledger_override import ensure_fixed_valuation_rate
        
        print("\nTesting stock valuation hooks...")
        ensure_fixed_valuation_rate(si, "test")
        
        print("After ensure_fixed_valuation_rate:")
        print(f"  Item rate: {si.items[0].rate}")
        print(f"  Item base_rate: {si.items[0].base_rate}")
        print(f"  Item valuation_rate: {si.items[0].valuation_rate}")
        
        # Check that rates are still preserved
        if si.items[0].rate == item_doc.standard_rate:
            print("✓ Rate still preserved as standard_rate after stock valuation hook")
        else:
            print(f"✗ Rate was changed to {si.items[0].rate}, expected {item_doc.standard_rate}")
            return False
            
        if si.items[0].base_rate == item_doc.standard_rate:
            print("✓ Base rate still preserved as standard_rate after stock valuation hook")
        else:
            print(f"✗ Base rate was changed to {si.items[0].base_rate}, expected {item_doc.standard_rate}")
            return False
            
        # Check that valuation_rate was updated for stock purposes
        if si.items[0].valuation_rate == item_doc.valuation_rate:
            print("✓ Valuation rate correctly updated for stock purposes")
        else:
            print(f"✗ Valuation rate not updated, got {si.items[0].valuation_rate}, expected {item_doc.valuation_rate}")
            return False
        
        print("\n🎉 All tests passed! Sales Invoice rate fix is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up Frappe environment
    if not os.path.exists("frappe-bench"):
        print("Please run this script from the frappe-bench directory")
        sys.exit(1)
        
    # Initialize Frappe
    try:
        import frappe
        frappe.init(site="localhost")
        frappe.connect()
        
        success = test_sales_invoice_rate_fix()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"Failed to initialize Frappe: {e}")
        sys.exit(1)
    finally:
        try:
            frappe.destroy()
        except:
            pass
