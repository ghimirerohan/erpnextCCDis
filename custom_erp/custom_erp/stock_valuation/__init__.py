# -*- coding: utf-8 -*-
"""
Custom ERP Stock Valuation Override Module

This module applies overrides to ERPNext's stock valuation functions
to ensure fixed valuation rates are always used from Item master.
"""

import frappe

def apply_overrides():
    """
    Apply all the overrides when this module is imported.
    This ensures the fixed valuation rate logic is active.
    """
    try:
        # Import our override functions
        from .stock_ledger_override import (
            get_valuation_rate,
            get_incoming_rate,
            is_fixed_valuation_rate_enabled
        )
        
        # Apply monkey patching to core ERPNext modules
        import erpnext.stock.stock_ledger
        import erpnext.stock.utils
        import erpnext.stock.get_item_details
        
        # Override the core functions
        erpnext.stock.stock_ledger.get_valuation_rate = get_valuation_rate
        erpnext.stock.utils.get_incoming_rate = get_incoming_rate
        erpnext.stock.get_item_details.get_valuation_rate = get_valuation_rate
        
        frappe.logger().info("Custom ERP: Fixed valuation rate overrides applied successfully")
        
    except Exception as e:
        frappe.logger().error(f"Custom ERP: Failed to apply overrides: {e}")

# Apply overrides when module is imported
apply_overrides()
