#!/usr/bin/env python3
"""
Bench command to identify and fix submitted Sales Invoices without GL Entries

Usage:
    bench --site site1.localhost execute custom_erp.management.commands.fix_sales_invoice_gl_entries.fix_sales_invoices_without_gl_entries --dry-run
    bench --site development.localhost execute custom_erp.management.commands.fix_sales_invoice_gl_entries.fix_sales_invoices_without_gl_entries --fix
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def fix_sales_invoices_without_gl_entries(dry_run=True, fix=False):
    """
    Identify and fix submitted Sales Invoices without GL Entries
    """
    
    print("=" * 80)
    print("SALES INVOICE GL ENTRIES FIX SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not fix else 'FIXING'}")
    print("=" * 80)
    
    # Get submitted sales invoices without GL entries
    invoices = get_submitted_sales_invoices_without_gl_entries()
    
    if not invoices:
        print("✅ No submitted sales invoices found without GL entries.")
        return {
            "status": "success",
            "message": "No invoices found without GL entries",
            "total_invoices": 0,
            "fixable_invoices": 0,
            "problematic_invoices": 0,
            "fixed_invoices": 0
        }
    
    print(f"❌ Found {len(invoices)} submitted sales invoices without GL entries:")
    print("-" * 80)
    
    # Analyze each invoice
    fixable_invoices = []
    problematic_invoices = []
    
    for invoice in invoices:
        issues = analyze_invoice_for_gl_entry_creation(invoice)
        
        print(f"\n📄 Invoice: {invoice.name}")
        print(f"   Customer: {invoice.customer}")
        print(f"   Company: {invoice.company}")
        print(f"   Posting Date: {invoice.posting_date}")
        print(f"   Grand Total: {invoice.grand_total}")
        print(f"   Base Grand Total: {invoice.base_grand_total}")
        print(f"   Debit To: {invoice.debit_to}")
        print(f"   Is Return: {invoice.is_return}")
        print(f"   Is POS: {invoice.is_pos}")
        fixable_invoices.append(invoice)
        
        # if issues:
        #     print(f"   ⚠️  Issues found: {', '.join(issues)}")
        #     problematic_invoices.append((invoice, issues))
        # else:
        #     print(f"   ✅ No obvious issues found - can be fixed")
        #     fixable_invoices.append(invoice)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total invoices without GL entries: {len(invoices)}")
    print(f"Fixable invoices: {len(fixable_invoices)}")
    print(f"Problematic invoices: {len(problematic_invoices)}")
    
    if problematic_invoices:
        print("\n⚠️  PROBLEMATIC INVOICES (require manual review):")
        for invoice, issues in problematic_invoices:
            print(f"   {invoice.name}: {', '.join(issues)}")
    
    # Fix invoices if requested
    fixed_count = 0
    if fixable_invoices and (fix or not dry_run):
        print(f"\n🔧 FIXING {len(fixable_invoices)} INVOICES...")
        
        for invoice in fixable_invoices:
            if create_gl_entries_for_invoice(invoice.name):
                fixed_count += 1
        
        print(f"\n✅ Successfully fixed {fixed_count} out of {len(fixable_invoices)} invoices")
    
    elif fixable_invoices and dry_run and not fix:
        print(f"\n🔧 DRY RUN: Would fix {len(fixable_invoices)} invoices")
        print("Run with --fix to actually fix the invoices")
    
    # Provide recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if problematic_invoices:
        print("1. Review problematic invoices manually before fixing")
        print("2. Ensure all required fields are populated")
        print("3. Check if invoices are valid for GL entry creation")
    
    print("4. Consider implementing validation to prevent this issue in the future")
    print("5. Add a check in the sales invoice submit process to ensure GL entries are created")
    print("6. Monitor for this issue in production environments")
    
    return {
        "status": "success",
        "total_invoices": len(invoices),
        "fixable_invoices": len(fixable_invoices),
        "problematic_invoices": len(problematic_invoices),
        "fixed_invoices": fixed_count,
        "problematic_invoice_details": [
            {"name": inv.name, "issues": issues} 
            for inv, issues in problematic_invoices
        ]
    }

def get_submitted_sales_invoices_without_gl_entries():
    """
    Get all submitted Sales Invoices that don't have GL Entries
    
    Note: Submitted invoices can have various statuses:
    - Submitted, Paid, Partly Paid, Unpaid, Unpaid and Discounted
    - Partly Paid and Discounted, Overdue and Discounted, Overdue
    - Return, Credit Note Issued, Internal Transfer
    """
    try:
        # Query to find submitted sales invoices without GL entries
        # Include all statuses that a submitted invoice can have
        query = """
        SELECT 
            si.name,
            si.customer,
            si.company,
            si.posting_date,
            si.grand_total,
            si.base_grand_total,
            si.docstatus,
            si.status,
            si.debit_to,
            si.against_income_account,
            si.is_return,
            si.is_pos,
            si.update_stock,
            si.currency,
            si.conversion_rate,
            si.creation,
            si.modified
        FROM `tabSales Invoice` si
        LEFT JOIN `tabGL Entry` gle ON gle.voucher_no = si.name AND gle.voucher_type = 'Sales Invoice'
        WHERE si.docstatus = 1  -- Submitted
        AND si.status IN (
            'Submitted', 'Paid', 'Partly Paid', 'Unpaid', 
            'Unpaid and Discounted', 'Partly Paid and Discounted', 
            'Overdue and Discounted', 'Overdue', 'Return', 
            'Credit Note Issued', 'Internal Transfer'
        )
        AND gle.name IS NULL   -- No GL entries exist
        ORDER BY si.posting_date DESC, si.name
        """
        
        invoices = frappe.db.sql(query, as_dict=True)
        return invoices
    
    except Exception as e:
        print(f"Error querying database: {e}")
        return []

def analyze_invoice_for_gl_entry_creation(invoice):
    """
    Analyze why GL entries might be missing for a specific invoice
    """
    issues = []
    
    # Check if required fields are present
    if not invoice.debit_to:
        issues.append("Missing debit_to account")
    
    if not invoice.customer:
        issues.append("Missing customer")
    
    if not invoice.company:
        issues.append("Missing company")
    
    if not invoice.grand_total or invoice.grand_total == 0:
        issues.append("Zero or missing grand total")
    
    if not invoice.base_grand_total or invoice.base_grand_total == 0:
        issues.append("Zero or missing base grand total")
    
    # Check if it's a return invoice
    if invoice.is_return:
        issues.append("Return invoice - may need special handling")
    
    # Check if it's a POS invoice
    if invoice.is_pos:
        issues.append("POS invoice - may have different GL entry logic")
    
    # Check status-specific issues
    if invoice.status == "Return":
        issues.append("Return status - verify if this should have GL entries")
    
    if invoice.status == "Credit Note Issued":
        issues.append("Credit Note Issued status - may need special handling")
    
    if invoice.status == "Internal Transfer":
        issues.append("Internal Transfer status - may have different GL logic")
    
    if "Overdue" in invoice.status:
        issues.append("Overdue status - verify payment status")
    
    if "Discounted" in invoice.status:
        issues.append("Discounted status - may affect GL entry amounts")
    
    return issues

def create_gl_entries_for_invoice(invoice_name):
    """
    Create GL entries for a specific sales invoice
    """
    try:
        # Get the sales invoice document
        si_doc = frappe.get_doc("Sales Invoice", invoice_name)
        
        # Check if GL entries already exist
        existing_gl_entries = frappe.get_all(
            "GL Entry",
            filters={
                "voucher_type": "Sales Invoice",
                "voucher_no": invoice_name
            },
            fields=["name"]
        )
        
        if existing_gl_entries:
            print(f"GL entries already exist for {invoice_name}")
            return False
        
        # Create GL entries
        si_doc.make_gl_entries()
        
        print(f"✅ Successfully created GL entries for {invoice_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating GL entries for {invoice_name}: {e}")
        return False
