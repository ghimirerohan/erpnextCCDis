# -*- coding: utf-8 -*-
"""
Patch to apply fixed valuation rate overrides.

This patch ensures that the fixed valuation rate logic is applied
to all stock transactions.
"""

import frappe

def execute():
    """
    Apply the fixed valuation rate overrides.
    """
    try:
        # Import our override functions
        from custom_erp.custom_erp.custom_erp.stock_valuation.stock_ledger_override import (
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
        
        frappe.logger().info("Custom ERP: Fixed valuation rate overrides applied successfully via patch")
        
    except Exception as e:
        frappe.logger().error(f"Custom ERP: Failed to apply overrides via patch: {e}")
        raise
