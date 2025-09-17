#!/usr/bin/env python3
"""
Bench command to remove all Payment Entries along with their linked data

This script will:
1. Remove all Payment Entries regardless of their status
2. Remove all linked GL Entries
3. Remove all linked Journal Entries
4. Remove all linked Payment Entry References
5. Show a comprehensive summary of what was removed

Usage:
    bench --site site1.localhost execute custom_erp.management.commands.remove_all_payments.remove_all_payments --dry-run
    bench --site site1.localhost execute custom_erp.management.commands.remove_all_payments.remove_all_payments --confirm
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def remove_all_payments(dry_run=False, confirm=True):
    """
    Remove all Payment Entries along with their linked data
    
    Args:
        dry_run (bool): If True, only show what would be removed without making changes
        confirm (bool): If True, actually remove the payment entries (overrides dry_run)
    """
    
    print("=" * 80)
    print("REMOVE ALL PAYMENT ENTRIES SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not confirm else 'REMOVING'}")
    print("=" * 80)
    
    # Get all payment entries
    payment_entries = get_all_payment_entries()
    
    if not payment_entries:
        print("✅ No payment entries found in the system.")
        return {
            "status": "success",
            "message": "No payment entries found",
            "total_payment_entries": 0,
            "total_gl_entries_removed": 0,
            "total_journal_entries_removed": 0,
            "total_payment_references_removed": 0
        }
    
    print(f"❌ Found {len(payment_entries)} payment entries to remove:")
    print("-" * 80)
    
    # Analyze payment entries by status
    status_counts = {}
    company_counts = {}
    total_amount = 0
    
    for payment_entry in payment_entries:
        status = payment_entry.status
        company = payment_entry.company
        amount = payment_entry.paid_amount or 0
        
        status_counts[status] = status_counts.get(status, 0) + 1
        company_counts[company] = company_counts.get(company, 0) + 1
        total_amount += amount
        
        # print(f"💰 {payment_entry.name}: {status} | {company} | {amount}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Total Payment Entries: {len(payment_entries)}")
    print(f"Total Amount: {total_amount}")
    
    print(f"\n📊 Status Distribution:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {status}: {count}")
    
    print(f"\n🏢 Company Distribution:")
    for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {company}: {count}")
    
    # Get linked data counts
    linked_data = get_linked_data_counts(payment_entries)
    
    print(f"\n🔗 Linked Data to be Removed:")
    print(f"   GL Entries: {linked_data['gl_entries']}")
    print(f"   Journal Entries: {linked_data['journal_entries']}")
    print(f"   Payment Entry References: {linked_data['payment_references']}")
    
    # Show warning
    print("\n" + "=" * 80)
    print("⚠️  WARNING")
    print("=" * 80)
    print("This operation will permanently delete:")
    print("1. All Payment Entries regardless of status")
    print("2. All linked GL Entries")
    print("3. All linked Journal Entries")
    print("4. All linked Payment Entry References")
    print("\nThis action cannot be undone!")
    
    if not confirm and not dry_run:
        print("\n❌ Operation cancelled. Use --confirm to proceed with removal.")
        return {
            "status": "cancelled",
            "message": "Operation cancelled - use --confirm to proceed",
            "total_payment_entries": len(payment_entries),
            "linked_data": linked_data
        }
    
    # Remove payment entries if confirmed
    if confirm or not dry_run:
        print(f"\n🗑️  REMOVING {len(payment_entries)} PAYMENT ENTRIES...")
        
        removal_results = remove_payment_entries_with_linked_data(payment_entries)
        
        print("\n" + "=" * 80)
        print("REMOVAL COMPLETE")
        print("=" * 80)
        print(f"✅ Payment Entries removed: {removal_results['payment_entries_removed']}")
        print(f"✅ GL Entries removed: {removal_results['gl_entries_removed']}")
        print(f"✅ Journal Entries removed: {removal_results['journal_entries_removed']}")
        print(f"✅ Payment References removed: {removal_results['payment_references_removed']}")
        
        return {
            "status": "success",
            "message": "All payment entries and linked data removed successfully",
            "total_payment_entries": len(payment_entries),
            "payment_entries_removed": removal_results['payment_entries_removed'],
            "gl_entries_removed": removal_results['gl_entries_removed'],
            "journal_entries_removed": removal_results['journal_entries_removed'],
            "payment_references_removed": removal_results['payment_references_removed'],
            "linked_data": linked_data
        }
    
    else:
        print(f"\n🔧 DRY RUN: Would remove {len(payment_entries)} payment entries")
        print("Run with --confirm to actually remove the payment entries")
        
        return {
            "status": "dry_run",
            "message": "Dry run completed - use --confirm to proceed",
            "total_payment_entries": len(payment_entries),
            "linked_data": linked_data
        }

def get_all_payment_entries():
    """
    Get all payment entries from the system regardless of status
    """
    try:
        payment_entries = frappe.get_all(
            "Payment Entry",
            fields=["name", "status", "company", "paid_amount", "party_type", "party", "posting_date"],
            order_by="creation desc"
        )
        return payment_entries
    except Exception as e:
        print(f"❌ Error getting payment entries: {e}")
        return []

def get_linked_data_counts(payment_entries):
    """
    Get counts of linked data that will be removed
    """
    payment_entry_names = [pe.name for pe in payment_entries]
    
    try:
        # Count GL Entries
        gl_entries_count = frappe.db.count("GL Entry", {
            "voucher_type": "Payment Entry",
            "voucher_no": ["in", payment_entry_names]
        })
        
        # Count Journal Entry Accounts that reference Payment Entries
        journal_entry_accounts = frappe.get_all("Journal Entry Account", 
            filters={
                "reference_type": "Payment Entry",
                "reference_name": ["in", payment_entry_names]
            }, 
            fields=["parent"], 
            distinct=True
        )
        
        journal_entries_count = len(journal_entry_accounts)
        
        # Count Payment Entry References
        payment_references_count = frappe.db.count("Payment Entry Reference", {
            "parent": ["in", payment_entry_names]
        })
        
        return {
            "gl_entries": gl_entries_count,
            "journal_entries": journal_entries_count,
            "payment_references": payment_references_count
        }
    except Exception as e:
        print(f"❌ Error getting linked data counts: {e}")
        return {
            "gl_entries": 0,
            "journal_entries": 0,
            "payment_references": 0
        }

def remove_payment_entries_with_linked_data(payment_entries):
    """
    Remove payment entries along with their linked data
    """
    payment_entries_removed = 0
    gl_entries_removed = 0
    journal_entries_removed = 0
    payment_references_removed = 0
    
    for payment_entry in payment_entries:
        try:
            print(f"🗑️  Processing Payment Entry: {payment_entry.name}")
            
            # Remove linked GL Entries first
            gl_entries = frappe.get_all("GL Entry", 
                filters={
                    "voucher_type": "Payment Entry",
                    "voucher_no": payment_entry.name
                }, 
                fields=["name"]
            )
            
            for gl_entry in gl_entries:
                try:
                    frappe.delete_doc("GL Entry", gl_entry.name, force=True)
                    gl_entries_removed += 1
                    print(f"   ✅ Removed GL Entry: {gl_entry.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove GL Entry {gl_entry.name}: {e}")
            
            # Remove linked Journal Entries
            journal_entry_accounts = frappe.get_all("Journal Entry Account", 
                filters={
                    "reference_type": "Payment Entry",
                    "reference_name": payment_entry.name
                }, 
                fields=["parent"], 
                distinct=True
            )
            
            for journal_entry_account in journal_entry_accounts:
                try:
                    frappe.delete_doc("Journal Entry", journal_entry_account.parent, force=True)
                    journal_entries_removed += 1
                    print(f"   ✅ Removed Journal Entry: {journal_entry_account.parent}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove Journal Entry {journal_entry_account.parent}: {e}")
            
            # Remove Payment Entry References
            payment_references = frappe.get_all("Payment Entry Reference", 
                filters={
                    "parent": payment_entry.name
                }, 
                fields=["name"]
            )
            
            for payment_reference in payment_references:
                try:
                    frappe.delete_doc("Payment Entry Reference", payment_reference.name, force=True)
                    payment_references_removed += 1
                    print(f"   ✅ Removed Payment Entry Reference: {payment_reference.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove Payment Entry Reference {payment_reference.name}: {e}")
            
            # Finally remove the Payment Entry itself
            try:
                # First try to cancel if it's submitted
                if payment_entry.status == "Submitted":
                    try:
                        doc = frappe.get_doc("Payment Entry", payment_entry.name)
                        doc.cancel()
                        print(f"   ✅ Cancelled Payment Entry: {payment_entry.name}")
                    except Exception as cancel_error:
                        print(f"   ⚠️  Could not cancel Payment Entry {payment_entry.name}: {cancel_error}")
                
                # Now try to delete
                frappe.delete_doc("Payment Entry", payment_entry.name, force=True)
                payment_entries_removed += 1
                print(f"✅ Successfully removed Payment Entry: {payment_entry.name}")
            except Exception as e:
                print(f"❌ Could not remove Payment Entry {payment_entry.name}: {e}")
                # Continue with next payment entry even if this one fails
            
        except Exception as e:
            print(f"❌ Error processing Payment Entry {payment_entry.name}: {e}")
            # Continue with next payment entry
    
    return {
        "payment_entries_removed": payment_entries_removed,
        "gl_entries_removed": gl_entries_removed,
        "journal_entries_removed": journal_entries_removed,
        "payment_references_removed": payment_references_removed
    }

def get_payment_entries_summary():
    """
    Get a summary of all payment entries in the system
    """
    print("=" * 80)
    print("PAYMENT ENTRIES SUMMARY REPORT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print("=" * 80)
    
    try:
        # Get all payment entries
        payment_entries = get_all_payment_entries()
        
        if not payment_entries:
            print("✅ No payment entries found in the system.")
            return {
                "total_payment_entries": 0,
                "status_distribution": {},
                "company_distribution": {},
                "total_amount": 0
            }
        
        # Analyze by status
        status_counts = {}
        company_counts = {}
        total_amount = 0
        
        for payment_entry in payment_entries:
            status = payment_entry.status
            company = payment_entry.company
            amount = payment_entry.paid_amount or 0
            
            status_counts[status] = status_counts.get(status, 0) + 1
            company_counts[company] = company_counts.get(company, 0) + 1
            total_amount += amount
        
        print(f"\n📊 PAYMENT ENTRIES OVERVIEW:")
        print(f"   Total Payment Entries: {len(payment_entries)}")
        print(f"   Total Amount: {total_amount}")
        
        print(f"\n📋 Status Distribution:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count}")
        
        print(f"\n🏢 Company Distribution:")
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count}")
        
        # Get linked data counts
        linked_data = get_linked_data_counts(payment_entries)
        
        print(f"\n🔗 Linked Data:")
        print(f"   GL Entries: {linked_data['gl_entries']}")
        print(f"   Journal Entries: {linked_data['journal_entries']}")
        print(f"   Payment Entry References: {linked_data['payment_references']}")
        
        return {
            "total_payment_entries": len(payment_entries),
            "status_distribution": status_counts,
            "company_distribution": company_counts,
            "total_amount": total_amount,
            "linked_data": linked_data
        }
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return {
            "error": str(e)
        }
