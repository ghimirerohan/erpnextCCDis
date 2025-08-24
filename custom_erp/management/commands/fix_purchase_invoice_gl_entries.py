#!/usr/bin/env python3
"""
Bench command to identify and fix submitted Purchase Invoices without GL Entries

Usage:
    bench --site site1.localhost execute custom_erp.management.commands.fix_purchase_invoice_gl_entries.fix_purchase_invoices_without_gl_entries --dry-run
    bench --site site1.localhost execute custom_erp.management.commands.fix_purchase_invoice_gl_entries.fix_purchase_invoices_without_gl_entries --fix
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def fix_purchase_invoices_without_gl_entries(dry_run=True, fix=False):
    """
    Identify and fix submitted Purchase Invoices without GL Entries
    
    Args:
        dry_run (bool): If True, only show what would be fixed without making changes
        fix (bool): If True, actually fix the purchase invoices (overrides dry_run)
    """
    
    print("=" * 80)
    print("PURCHASE INVOICE GL ENTRIES FIX SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not fix else 'FIXING'}")
    print("=" * 80)
    
    # Get submitted purchase invoices without GL entries
    purchase_invoices = get_submitted_purchase_invoices_without_gl_entries()
    
    if not purchase_invoices:
        print("✅ No submitted purchase invoices found without GL entries.")
        return {
            "status": "success",
            "message": "No purchase invoices found without GL entries",
            "total_purchase_invoices": 0,
            "fixable_purchase_invoices": 0,
            "problematic_purchase_invoices": 0,
            "fixed_purchase_invoices": 0
        }
    
    print(f"❌ Found {len(purchase_invoices)} submitted purchase invoices without GL entries:")
    print("-" * 80)
    
    # Analyze each purchase invoice
    fixable_purchase_invoices = []
    problematic_purchase_invoices = []
    
    for purchase_invoice in purchase_invoices:
        issues = analyze_purchase_invoice_for_gl_entry_creation(purchase_invoice)
        
        print(f"\n📋 Purchase Invoice: {purchase_invoice.name}")
        print(f"   Supplier: {purchase_invoice.supplier}")
        print(f"   Company: {purchase_invoice.company}")
        print(f"   Posting Date: {purchase_invoice.posting_date}")
        print(f"   Grand Total: {purchase_invoice.grand_total}")
        print(f"   Base Grand Total: {purchase_invoice.base_grand_total}")
        print(f"   Credit To: {purchase_invoice.credit_to}")
        print(f"   Is Return: {purchase_invoice.is_return}")
        print(f"   Is Debit Note: {purchase_invoice.is_debit_note}")
        print(f"   Status: {purchase_invoice.status}")
        
        if issues:
            print(f"   ⚠️  Issues found: {', '.join(issues)}")
            problematic_purchase_invoices.append((purchase_invoice, issues))
        else:
            print(f"   ✅ No obvious issues found - can be fixed")
            fixable_purchase_invoices.append(purchase_invoice)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total purchase invoices without GL entries: {len(purchase_invoices)}")
    print(f"Fixable purchase invoices: {len(fixable_purchase_invoices)}")
    print(f"Problematic purchase invoices: {len(problematic_purchase_invoices)}")
    
    if problematic_purchase_invoices:
        print("\n⚠️  PROBLEMATIC PURCHASE INVOICES (require manual review):")
        for purchase_invoice, issues in problematic_purchase_invoices:
            print(f"   {purchase_invoice.name}: {', '.join(issues)}")
    
    # Fix purchase invoices if requested
    fixed_count = 0
    if fixable_purchase_invoices and (fix or not dry_run):
        print(f"\n🔧 FIXING {len(fixable_purchase_invoices)} PURCHASE INVOICES...")
        
        for purchase_invoice in fixable_purchase_invoices:
            if create_gl_entries_for_purchase_invoice(purchase_invoice.name):
                fixed_count += 1
        
        print(f"\n✅ Successfully fixed {fixed_count} out of {len(fixable_purchase_invoices)} purchase invoices")
    
    elif fixable_purchase_invoices and dry_run and not fix:
        print(f"\n🔧 DRY RUN: Would fix {len(fixable_purchase_invoices)} purchase invoices")
        print("Run with --fix to actually fix the purchase invoices")
    
    # Provide recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if problematic_purchase_invoices:
        print("1. Review problematic purchase invoices manually before fixing")
        print("2. Ensure all required fields are populated")
        print("3. Check if purchase invoices are valid for GL entry creation")
    
    print("4. Consider implementing validation to prevent this issue in the future")
    print("5. Add a check in the purchase invoice submit process to ensure GL entries are created")
    print("6. Monitor for this issue in production environments")
    
    return {
        "status": "success",
        "total_purchase_invoices": len(purchase_invoices),
        "fixable_purchase_invoices": len(fixable_purchase_invoices),
        "problematic_purchase_invoices": len(problematic_purchase_invoices),
        "fixed_purchase_invoices": fixed_count,
        "problematic_purchase_invoice_details": [
            {"name": pi.name, "issues": issues} 
            for pi, issues in problematic_purchase_invoices
        ]
    }

def get_submitted_purchase_invoices_without_gl_entries():
    """
    Get all submitted Purchase Invoices that don't have GL Entries
    
    Note: Submitted purchase invoices can have various statuses:
    - Submitted, Paid, Partly Paid, Unpaid, Unpaid and Discounted
    - Partly Paid and Discounted, Overdue and Discounted, Overdue
    - Return, Debit Note Issued, Internal Transfer
    """
    try:
        # Query to find submitted purchase invoices without GL entries
        # Include all statuses that a submitted purchase invoice can have
        query = """
        SELECT 
            pi.name,
            pi.supplier,
            pi.company,
            pi.posting_date,
            pi.grand_total,
            pi.base_grand_total,
            pi.docstatus,
            pi.status,
            pi.credit_to,
            pi.against_expense_account,
            pi.is_return,
            pi.update_stock,
            pi.creation,
            pi.modified
        FROM `tabPurchase Invoice` pi
        LEFT JOIN `tabGL Entry` gle ON gle.voucher_no = pi.name AND gle.voucher_type = 'Purchase Invoice'
        WHERE pi.docstatus = 1  -- Submitted
        AND pi.status IN (
            'Submitted', 'Paid', 'Partly Paid', 'Unpaid', 
            'Unpaid and Discounted', 'Partly Paid and Discounted', 
            'Overdue and Discounted', 'Overdue', 'Return', 
            'Debit Note Issued', 'Internal Transfer'
        )
        AND gle.name IS NULL   -- No GL entries exist
        ORDER BY pi.posting_date DESC, pi.name
        """
        
        purchase_invoices = frappe.db.sql(query, as_dict=True)
        return purchase_invoices
    
    except Exception as e:
        print(f"Error querying database: {e}")
        return []

def analyze_purchase_invoice_for_gl_entry_creation(purchase_invoice):
    """
    Analyze why GL entries might be missing for a specific purchase invoice
    """
    issues = []
    
    # Check if required fields are present
    if not purchase_invoice.credit_to:
        issues.append("Missing credit_to account")
    
    if not purchase_invoice.supplier:
        issues.append("Missing supplier")
    
    if not purchase_invoice.company:
        issues.append("Missing company")
    
    if not purchase_invoice.grand_total or purchase_invoice.grand_total == 0:
        issues.append("Zero or missing grand total")
    
    if not purchase_invoice.base_grand_total or purchase_invoice.base_grand_total == 0:
        issues.append("Zero or missing base grand total")
    
    # Check if it's a return invoice
    if purchase_invoice.is_return:
        issues.append("Return invoice - may need special handling")
    
    # Check if it's a debit note
    if purchase_invoice.is_debit_note:
        issues.append("Debit note - may need special handling")
    
    # Check status-specific issues
    if purchase_invoice.status == "Return":
        issues.append("Return status - verify if this should have GL entries")
    
    if purchase_invoice.status == "Debit Note Issued":
        issues.append("Debit Note Issued status - may need special handling")
    
    if purchase_invoice.status == "Internal Transfer":
        issues.append("Internal Transfer status - may have different GL logic")
    
    if "Overdue" in purchase_invoice.status:
        issues.append("Overdue status - verify payment status")
    
    if "Discounted" in purchase_invoice.status:
        issues.append("Discounted status - may affect GL entry amounts")
    
    return issues

def create_gl_entries_for_purchase_invoice(purchase_invoice_name):
    """
    Create GL entries for a specific purchase invoice
    """
    try:
        # Get the purchase invoice document
        pi_doc = frappe.get_doc("Purchase Invoice", purchase_invoice_name)
        
        # Check if GL entries already exist
        existing_gl_entries = frappe.get_all(
            "GL Entry",
            filters={
                "voucher_type": "Purchase Invoice",
                "voucher_no": purchase_invoice_name
            },
            fields=["name"]
        )
        
        if existing_gl_entries:
            print(f"GL entries already exist for {purchase_invoice_name}")
            return False
        
        # Create GL entries
        pi_doc.make_gl_entries()
        
        print(f"✅ Successfully created GL entries for {purchase_invoice_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating GL entries for {purchase_invoice_name}: {e}")
        return False
