#!/usr/bin/env python3
"""
Bench command to identify and fix submitted Payment Entries without GL Entries

Usage:
    bench --site site1.localhost execute custom_erp.management.commands.fix_payment_entry_gl_entries.fix_payment_entries_without_gl_entries --dry-run
    bench --site site1.localhost execute custom_erp.management.commands.fix_payment_entry_gl_entries.fix_payment_entries_without_gl_entries --fix
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def fix_payment_entries_without_gl_entries(dry_run=True, fix=False):
    """
    Identify and fix submitted Payment Entries without GL Entries
    
    Args:
        dry_run (bool): If True, only show what would be fixed without making changes
        fix (bool): If True, actually fix the payment entries (overrides dry_run)
    """
    
    print("=" * 80)
    print("PAYMENT ENTRY GL ENTRIES FIX SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not fix else 'FIXING'}")
    print("=" * 80)
    
    # Get submitted payment entries without GL entries
    payment_entries = get_submitted_payment_entries_without_gl_entries()
    
    if not payment_entries:
        print("✅ No submitted payment entries found without GL entries.")
        return {
            "status": "success",
            "message": "No payment entries found without GL entries",
            "total_payment_entries": 0,
            "fixable_payment_entries": 0,
            "problematic_payment_entries": 0,
            "fixed_payment_entries": 0
        }
    
    print(f"❌ Found {len(payment_entries)} submitted payment entries without GL entries:")
    print("-" * 80)
    
    # Analyze each payment entry
    fixable_payment_entries = []
    problematic_payment_entries = []
    
    for payment_entry in payment_entries:
        issues = analyze_payment_entry_for_gl_entry_creation(payment_entry)
        
        print(f"\n💰 Payment Entry: {payment_entry.name}")
        print(f"   Party Type: {payment_entry.party_type}")
        print(f"   Party: {payment_entry.party}")
        print(f"   Company: {payment_entry.company}")
        print(f"   Posting Date: {payment_entry.posting_date}")
        print(f"   Paid Amount: {payment_entry.paid_amount}")
        print(f"   Base Paid Amount: {payment_entry.base_paid_amount}")
        print(f"   Payment Type: {payment_entry.payment_type}")
        print(f"   Mode of Payment: {payment_entry.mode_of_payment}")
        print(f"   Status: {payment_entry.status}")
        
        if issues:
            print(f"   ⚠️  Issues found: {', '.join(issues)}")
            problematic_payment_entries.append((payment_entry, issues))
        else:
            print(f"   ✅ No obvious issues found - can be fixed")
            fixable_payment_entries.append(payment_entry)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total payment entries without GL entries: {len(payment_entries)}")
    print(f"Fixable payment entries: {len(fixable_payment_entries)}")
    print(f"Problematic payment entries: {len(problematic_payment_entries)}")
    
    if problematic_payment_entries:
        print("\n⚠️  PROBLEMATIC PAYMENT ENTRIES (require manual review):")
        for payment_entry, issues in problematic_payment_entries:
            print(f"   {payment_entry.name}: {', '.join(issues)}")
    
    # Fix payment entries if requested
    fixed_count = 0
    if fixable_payment_entries and (fix or not dry_run):
        print(f"\n🔧 FIXING {len(fixable_payment_entries)} PAYMENT ENTRIES...")
        
        for payment_entry in fixable_payment_entries:
            if create_gl_entries_for_payment_entry(payment_entry.name):
                fixed_count += 1
        
        print(f"\n✅ Successfully fixed {fixed_count} out of {len(fixable_payment_entries)} payment entries")
    
    elif fixable_payment_entries and dry_run and not fix:
        print(f"\n🔧 DRY RUN: Would fix {len(fixable_payment_entries)} payment entries")
        print("Run with --fix to actually fix the payment entries")
    
    # Provide recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if problematic_payment_entries:
        print("1. Review problematic payment entries manually before fixing")
        print("2. Ensure all required fields are populated")
        print("3. Check if payment entries are valid for GL entry creation")
    
    print("4. Consider implementing validation to prevent this issue in the future")
    print("5. Add a check in the payment entry submit process to ensure GL entries are created")
    print("6. Monitor for this issue in production environments")
    
    return {
        "status": "success",
        "total_payment_entries": len(payment_entries),
        "fixable_payment_entries": len(fixable_payment_entries),
        "problematic_payment_entries": len(problematic_payment_entries),
        "fixed_payment_entries": fixed_count,
        "problematic_payment_entry_details": [
            {"name": pe.name, "issues": issues} 
            for pe, issues in problematic_payment_entries
        ]
    }

def get_submitted_payment_entries_without_gl_entries():
    """
    Get all submitted Payment Entries that don't have GL Entries
    
    Note: Submitted payment entries can have various statuses:
    - Submitted, Unpaid, Paid, Partly Paid, Overdue, Cancelled
    """
    try:
        # Query to find submitted payment entries without GL entries
        # Include all statuses that a submitted payment entry can have
        query = """
        SELECT 
            pe.name,
            pe.party_type,
            pe.party,
            pe.company,
            pe.posting_date,
            pe.paid_amount,
            pe.base_paid_amount,
            pe.docstatus,
            pe.status,
            pe.payment_type,
            pe.mode_of_payment,
            pe.paid_from,
            pe.paid_to,
            pe.creation,
            pe.modified
        FROM `tabPayment Entry` pe
        LEFT JOIN `tabGL Entry` gle ON gle.voucher_no = pe.name AND gle.voucher_type = 'Payment Entry'
        WHERE pe.docstatus = 1  -- Submitted
        AND pe.status IN (
            'Submitted', 'Unpaid', 'Paid', 'Partly Paid', 'Overdue', 'Cancelled'
        )
        AND gle.name IS NULL   -- No GL entries exist
        ORDER BY pe.posting_date DESC, pe.name
        """
        
        payment_entries = frappe.db.sql(query, as_dict=True)
        return payment_entries
    
    except Exception as e:
        print(f"Error querying database: {e}")
        return []

def analyze_payment_entry_for_gl_entry_creation(payment_entry):
    """
    Analyze why GL entries might be missing for a specific payment entry
    """
    issues = []
    
    # Check if required fields are present
    if not payment_entry.paid_from:
        issues.append("Missing paid_from account")
    
    if not payment_entry.paid_to:
        issues.append("Missing paid_to account")
    
    if not payment_entry.party:
        issues.append("Missing party")
    
    if not payment_entry.company:
        issues.append("Missing company")
    
    if not payment_entry.paid_amount or payment_entry.paid_amount == 0:
        issues.append("Zero or missing paid amount")
    
    if not payment_entry.base_paid_amount or payment_entry.base_paid_amount == 0:
        issues.append("Zero or missing base paid amount")
    
    if not payment_entry.party_type:
        issues.append("Missing party type")
    
    if not payment_entry.payment_type:
        issues.append("Missing payment type")
    
    # Check status-specific issues
    if payment_entry.status == "Cancelled":
        issues.append("Cancelled status - verify if this should have GL entries")
    
    if payment_entry.status == "Overdue":
        issues.append("Overdue status - verify payment status")
    
    if payment_entry.payment_type == "Internal Transfer":
        issues.append("Internal Transfer - may have different GL logic")
    
    return issues

def create_gl_entries_for_payment_entry(payment_entry_name):
    """
    Create GL entries for a specific payment entry
    """
    try:
        # Get the payment entry document
        pe_doc = frappe.get_doc("Payment Entry", payment_entry_name)
        
        # Check if GL entries already exist
        existing_gl_entries = frappe.get_all(
            "GL Entry",
            filters={
                "voucher_type": "Payment Entry",
                "voucher_no": payment_entry_name
            },
            fields=["name"]
        )
        
        if existing_gl_entries:
            print(f"GL entries already exist for {payment_entry_name}")
            return False
        
        # Create GL entries
        pe_doc.make_gl_entries()
        
        print(f"✅ Successfully created GL entries for {payment_entry_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating GL entries for {payment_entry_name}: {e}")
        return False
