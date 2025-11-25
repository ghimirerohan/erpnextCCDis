#!/usr/bin/env python3
"""
Installation script for Fixed Valuation Rate Override

This script helps set up the fixed valuation rate feature in the Custom ERP app.
"""

import frappe
import os
import sys

def install_fixed_valuation_rate():
    """
    Install and configure the fixed valuation rate feature.
    """
    print("Installing Fixed Valuation Rate Override...")
    
    try:
        # Check if Custom ERP Settings doctype exists
        if not frappe.db.exists("DocType", "Custom ERP Settings"):
            print("Creating Custom ERP Settings doctype...")
            create_custom_erp_settings()
        
        # Create default settings
        if not frappe.db.exists("Custom ERP Settings", "Custom ERP Settings"):
            print("Creating default Custom ERP Settings...")
            create_default_settings()
        
        # Enable the feature
        enable_fixed_valuation_rate()
        
        print("✅ Fixed Valuation Rate Override installed successfully!")
        print("\nNext steps:")
        print("1. Set valuation_rate in your Item masters")
        print("2. Test with a stock transaction")
        print("3. Access settings at: /custom-erp-settings")
        
    except Exception as e:
        print(f"❌ Error installing Fixed Valuation Rate Override: {e}")
        return False
    
    return True

def create_custom_erp_settings():
    """
    Create the Custom ERP Settings doctype.
    """
    # This would typically be done via fixtures, but we can create it programmatically
    settings_doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Custom ERP Settings",
        "module": "Custom ERP",
        "custom": 0,
        "istable": 0,
        "issingle": 1,
        "fields": [
            {
                "fieldname": "enable_fixed_valuation_rate",
                "fieldtype": "Check",
                "label": "Enable Fixed Valuation Rate",
                "description": "When enabled, the system will always use the valuation_rate from Item master for all stock valuation calculations.",
                "default": 0
            },
            {
                "fieldname": "fixed_valuation_rate_description",
                "fieldtype": "Small Text",
                "label": "Fixed Valuation Rate Description",
                "description": "Description of how the fixed valuation rate feature works.",
                "read_only": 1,
                "default": "When enabled, all stock transactions will use the fixed valuation_rate from Item master."
            }
        ]
    })
    settings_doc.insert()

def create_default_settings():
    """
    Create default Custom ERP Settings.
    """
    settings_doc = frappe.get_doc({
        "doctype": "Custom ERP Settings",
        "name": "Custom ERP Settings",
        "enable_fixed_valuation_rate": 0
    })
    settings_doc.insert()

def enable_fixed_valuation_rate():
    """
    Enable the fixed valuation rate feature.
    """
    if frappe.db.exists("Custom ERP Settings", "Custom ERP Settings"):
        settings = frappe.get_doc("Custom ERP Settings", "Custom ERP Settings")
        settings.enable_fixed_valuation_rate = 1
        settings.save()
        print("✅ Fixed Valuation Rate feature enabled!")

def check_items_without_valuation_rate():
    """
    Check for items that don't have valuation_rate set.
    """
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
        print("\n⚠️  Warning: Found items without valuation_rate:")
        for item in items:
            print(f"   - {item.item_name} ({item.name})")
        print("\nPlease set valuation_rate or standard_rate for these items.")
    else:
        print("\n✅ All stock items have valuation rates set.")

if __name__ == "__main__":
    # This script should be run from the Frappe bench
    if not frappe.db:
        print("❌ This script must be run from within Frappe bench")
        sys.exit(1)
    
    install_fixed_valuation_rate()
    check_items_without_valuation_rate()
