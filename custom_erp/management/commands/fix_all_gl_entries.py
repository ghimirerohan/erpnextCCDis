#!/usr/bin/env python3
"""
Master script to identify and fix submitted documents without GL Entries for all doctypes

This script handles:
1. Sales Invoice
2. Payment Entry  
3. Purchase Invoice

Usage:
    bench --site site1.localhost execute custom_erp.management.commands.fix_all_gl_entries.fix_all_gl_entries --dry-run
    bench --site site1.localhost execute custom_erp.management.commands.fix_all_gl_entries.fix_all_gl_entries --fix
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def fix_all_gl_entries(dry_run=True, fix=False):
    """
    Identify and fix submitted documents without GL Entries for all doctypes
    
    Args:
        dry_run (bool): If True, only show what would be fixed without making changes
        fix (bool): If True, actually fix the documents (overrides dry_run)
    """
    
    print("=" * 80)
    print("COMPREHENSIVE GL ENTRIES FIX SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not fix else 'FIXING'}")
    print("=" * 80)
    
    # Import the individual fix functions
    from custom_erp.management.commands.fix_sales_invoice_gl_entries import fix_sales_invoices_without_gl_entries
    from custom_erp.management.commands.fix_payment_entry_gl_entries import fix_payment_entries_without_gl_entries
    from custom_erp.management.commands.fix_purchase_invoice_gl_entries import fix_purchase_invoices_without_gl_entries
    
    # Run fixes for each doctype
    results = {}
    
    print("\n" + "=" * 80)
    print("1. SALES INVOICE GL ENTRIES")
    print("=" * 80)
    results['sales_invoice'] = fix_sales_invoices_without_gl_entries(dry_run=dry_run, fix=fix)
    
    print("\n" + "=" * 80)
    print("2. PAYMENT ENTRY GL ENTRIES")
    print("=" * 80)
    results['payment_entry'] = fix_payment_entries_without_gl_entries(dry_run=dry_run, fix=fix)
    
    print("\n" + "=" * 80)
    print("3. PURCHASE INVOICE GL ENTRIES")
    print("=" * 80)
    results['purchase_invoice'] = fix_purchase_invoices_without_gl_entries(dry_run=dry_run, fix=fix)
    
    # Generate comprehensive summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 80)
    
    total_documents = 0
    total_fixable = 0
    total_problematic = 0
    total_fixed = 0
    
    for doctype, result in results.items():
        if result:
            total_documents += result.get('total_sales_invoices', result.get('total_payment_entries', result.get('total_purchase_invoices', 0)))
            total_fixable += result.get('fixable_sales_invoices', result.get('fixable_payment_entries', result.get('fixable_purchase_invoices', 0)))
            total_problematic += result.get('problematic_sales_invoices', result.get('problematic_payment_entries', result.get('problematic_purchase_invoices', 0)))
            total_fixed += result.get('fixed_sales_invoices', result.get('fixed_payment_entries', result.get('fixed_purchase_invoices', 0)))
    
    print(f"📊 OVERALL STATISTICS:")
    print(f"   Total documents without GL entries: {total_documents}")
    print(f"   Fixable documents: {total_fixable}")
    print(f"   Problematic documents: {total_problematic}")
    print(f"   Fixed documents: {total_fixed}")
    
    print(f"\n📋 BREAKDOWN BY DOCTYPE:")
    for doctype, result in results.items():
        if result:
            doc_count = result.get('total_sales_invoices', result.get('total_payment_entries', result.get('total_purchase_invoices', 0)))
            fixable_count = result.get('fixable_sales_invoices', result.get('fixable_payment_entries', result.get('fixable_purchase_invoices', 0)))
            problematic_count = result.get('problematic_sales_invoices', result.get('problematic_payment_entries', result.get('problematic_purchase_invoices', 0)))
            fixed_count = result.get('fixed_sales_invoices', result.get('fixed_payment_entries', result.get('fixed_purchase_invoices', 0)))
            
            print(f"   {doctype.replace('_', ' ').title()}: {doc_count} total, {fixable_count} fixable, {problematic_count} problematic, {fixed_count} fixed")
    
    # Provide recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if total_problematic > 0:
        print("1. Review problematic documents manually before fixing")
        print("2. Ensure all required fields are populated")
        print("3. Check if documents are valid for GL entry creation")
    
    print("4. Consider implementing validation to prevent this issue in the future")
    print("5. Add checks in the submit process to ensure GL entries are created")
    print("6. Monitor for this issue in production environments")
    print("7. Set up regular automated checks for missing GL entries")
    
    # Return comprehensive results
    return {
        "status": "success",
        "timestamp": str(now_datetime()),
        "mode": "DRY RUN" if dry_run and not fix else "FIXING",
        "total_documents": total_documents,
        "total_fixable": total_fixable,
        "total_problematic": total_problematic,
        "total_fixed": total_fixed,
        "results_by_doctype": results
    }

def get_comprehensive_status():
    """
    Get a comprehensive status report of all documents without GL entries
    """
    print("=" * 80)
    print("COMPREHENSIVE GL ENTRIES STATUS REPORT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print("=" * 80)
    
    # Import the individual query functions
    from custom_erp.management.commands.fix_sales_invoice_gl_entries import get_submitted_sales_invoices_without_gl_entries
    from custom_erp.management.commands.fix_payment_entry_gl_entries import get_submitted_payment_entries_without_gl_entries
    from custom_erp.management.commands.fix_purchase_invoice_gl_entries import get_submitted_purchase_invoices_without_gl_entries
    
    # Get counts for each doctype
    sales_invoices = get_submitted_sales_invoices_without_gl_entries()
    payment_entries = get_submitted_payment_entries_without_gl_entries()
    purchase_invoices = get_submitted_purchase_invoices_without_gl_entries()
    
    print(f"\n📊 DOCUMENT COUNTS WITHOUT GL ENTRIES:")
    print(f"   Sales Invoices: {len(sales_invoices)}")
    print(f"   Payment Entries: {len(payment_entries)}")
    print(f"   Purchase Invoices: {len(purchase_invoices)}")
    print(f"   TOTAL: {len(sales_invoices) + len(payment_entries) + len(purchase_invoices)}")
    
    # Show status distribution for each doctype
    if sales_invoices:
        print(f"\n📋 Sales Invoice Status Distribution:")
        status_counts = {}
        for si in sales_invoices:
            status = si.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count}")
    
    if payment_entries:
        print(f"\n💰 Payment Entry Status Distribution:")
        status_counts = {}
        for pe in payment_entries:
            status = pe.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count}")
    
    if purchase_invoices:
        print(f"\n📋 Purchase Invoice Status Distribution:")
        status_counts = {}
        for pi in purchase_invoices:
            status = pi.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count}")
    
    # Show company distribution
    print(f"\n🏢 Company Distribution:")
    company_counts = {}
    
    for si in sales_invoices:
        company = si.company
        company_counts[company] = company_counts.get(company, 0) + 1
    
    for pe in payment_entries:
        company = pe.company
        company_counts[company] = company_counts.get(company, 0) + 1
    
    for pi in purchase_invoices:
        company = pi.company
        company_counts[company] = company_counts.get(company, 0) + 1
    
    for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {company}: {count}")
    
    return {
        "sales_invoices": len(sales_invoices),
        "payment_entries": len(payment_entries),
        "purchase_invoices": len(purchase_invoices),
        "total": len(sales_invoices) + len(payment_entries) + len(purchase_invoices)
    }
