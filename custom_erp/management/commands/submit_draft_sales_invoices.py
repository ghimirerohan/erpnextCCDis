#!/usr/bin/env python3
"""
Bench command to submit draft Sales Invoices with comprehensive logging.
Usage: bench --site your-site.com execute custom_erp.management.commands.submit_draft_sales_invoices.submit_draft_sales_invoices
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def submit_draft_sales_invoices():
    """
    Submit all draft Sales Invoices with comprehensive logging
    """
    
    print("=" * 80)
    print("SUBMIT DRAFT SALES INVOICES SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print("Mode: DRY RUN (use submit_draft_sales_invoices_confirm() for actual submission)")
    print("=" * 80)
    
    # Get all draft sales invoices
    draft_invoices = get_draft_sales_invoices()
    
    if not draft_invoices:
        print("✅ No draft sales invoices found.")
        return {
            "status": "success",
            "message": "No draft sales invoices found",
            "total_invoices": 0,
            "submitted_invoices": 0,
            "failed_invoices": 0,
            "summary": {}
        }
    
    print(f"📄 Found {len(draft_invoices)} draft sales invoices to submit:")
    print("-" * 80)
    
    # Analyze draft invoices
    company_counts = {}
    customer_counts = {}
    total_amount = 0
    return_counts = {"returns": 0, "non_returns": 0}
    
    for invoice in draft_invoices:
        company = invoice.company
        customer = invoice.customer
        amount = invoice.grand_total or 0
        is_return = invoice.is_return
        
        company_counts[company] = company_counts.get(company, 0) + 1
        customer_counts[customer] = customer_counts.get(customer, 0) + 1
        total_amount += amount
        
        if is_return:
            return_counts["returns"] += 1
        else:
            return_counts["non_returns"] += 1
        
        print(f"📄 {invoice.name}: {company} | {customer} | {amount} | Return: {is_return}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Total Draft Invoices: {len(draft_invoices)}")
    print(f"Total Amount: {total_amount}")
    print(f"Returns: {return_counts['returns']}")
    print(f"Non-Returns: {return_counts['non_returns']}")
    
    print(f"\n📊 Company Distribution:")
    for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {company}: {count}")
    
    print(f"\n👥 Customer Distribution:")
    for customer, count in sorted(customer_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {customer}: {count}")
    if len(customer_counts) > 10:
        print(f"   ... and {len(customer_counts) - 10} more customers")
    
    # Show warning
    print("\n" + "=" * 80)
    print("⚠️  WARNING")
    print("=" * 80)
    print("This operation will:")
    print("1. Submit all draft Sales Invoices")
    print("2. Create GL Entries for all invoices")
    print("3. Update stock levels (if update_stock=True)")
    print("4. Create Stock Ledger Entries")
    print("5. Update customer balances")
    print("6. Generate accounting entries")
    
    print(f"\n🔧 DRY RUN: Would submit {len(draft_invoices)} draft invoices")
    print("Run submit_draft_sales_invoices_confirm() to actually submit the invoices")
    
    return {
        "status": "dry_run",
        "message": "Dry run completed - use submit_draft_sales_invoices_confirm() to proceed",
        "total_invoices": len(draft_invoices),
        "summary": {
            "company_counts": company_counts,
            "customer_counts": customer_counts,
            "return_counts": return_counts,
            "total_amount": total_amount
        }
    }

def submit_draft_sales_invoices_confirm():
    """
    Actually submit all draft Sales Invoices (confirmation required)
    """
    
    print("=" * 80)
    print("SUBMIT DRAFT SALES INVOICES SCRIPT - CONFIRMED")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print("Mode: SUBMITTING (ACTUAL SUBMISSION)")
    print("=" * 80)
    
    # Get all draft sales invoices
    draft_invoices = get_draft_sales_invoices()
    
    if not draft_invoices:
        print("✅ No draft sales invoices found.")
        return {
            "status": "success",
            "message": "No draft sales invoices found",
            "total_invoices": 0,
            "submitted_invoices": 0,
            "failed_invoices": 0,
            "summary": {}
        }
    
    print(f"📤 SUBMITTING {len(draft_invoices)} DRAFT SALES INVOICES...")
    
    submission_results = submit_invoices_with_logging(draft_invoices, dry_run=False)
    
    print("\n" + "=" * 80)
    print("SUBMISSION COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully submitted: {submission_results['successful_submissions']}")
    print(f"❌ Failed submissions: {submission_results['failed_submissions']}")
    print(f"📊 Total GL Entries created: {submission_results['gl_entries_created']}")
    print(f"📦 Total Stock Ledger Entries created: {submission_results['stock_ledger_entries_created']}")
    print(f"💰 Total amount processed: {submission_results['total_amount_processed']}")
    
    # Show failed submissions
    if submission_results['failed_submissions'] > 0:
        print(f"\n❌ FAILED SUBMISSIONS:")
        for failed in submission_results['failed_details']:
            print(f"   {failed['invoice_name']}: {failed['error']}")
    
    # Final verification
    print(f"\n🔍 FINAL VERIFICATION:")
    remaining_draft = frappe.db.count("Sales Invoice", {"docstatus": 0})
    total_invoices = frappe.db.count("Sales Invoice")
    print(f"   Remaining draft invoices: {remaining_draft}")
    print(f"   Total invoices in system: {total_invoices}")
    
    return {
        "status": "success",
        "message": "Sales invoice submission completed",
        "total_invoices": len(draft_invoices),
        "successful_submissions": submission_results['successful_submissions'],
        "failed_submissions": submission_results['failed_submissions'],
        "gl_entries_created": submission_results['gl_entries_created'],
        "stock_ledger_entries_created": submission_results['stock_ledger_entries_created'],
        "total_amount_processed": submission_results['total_amount_processed'],
        "failed_details": submission_results['failed_details']
    }

def submit_draft_sales_invoices_test(limit=5):
    """
    Test submission with limited invoices
    """
    
    print("=" * 80)
    print("SUBMIT DRAFT SALES INVOICES SCRIPT - TEST MODE")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: TEST (Limit: {limit} invoices)")
    print("=" * 80)
    
    # Get limited draft sales invoices
    draft_invoices = get_draft_sales_invoices(limit)
    
    if not draft_invoices:
        print("✅ No draft sales invoices found.")
        return {
            "status": "success",
            "message": "No draft sales invoices found",
            "total_invoices": 0,
            "submitted_invoices": 0,
            "failed_invoices": 0,
            "summary": {}
        }
    
    print(f"📤 SUBMITTING {len(draft_invoices)} DRAFT SALES INVOICES (TEST MODE)...")
    
    submission_results = submit_invoices_with_logging(draft_invoices, dry_run=False)
    
    print("\n" + "=" * 80)
    print("TEST SUBMISSION COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully submitted: {submission_results['successful_submissions']}")
    print(f"❌ Failed submissions: {submission_results['failed_submissions']}")
    print(f"📊 Total GL Entries created: {submission_results['gl_entries_created']}")
    print(f"📦 Total Stock Ledger Entries created: {submission_results['stock_ledger_entries_created']}")
    print(f"💰 Total amount processed: {submission_results['total_amount_processed']}")
    
    return {
        "status": "success",
        "message": "Test submission completed",
        "total_invoices": len(draft_invoices),
        "successful_submissions": submission_results['successful_submissions'],
        "failed_submissions": submission_results['failed_submissions'],
        "gl_entries_created": submission_results['gl_entries_created'],
        "stock_ledger_entries_created": submission_results['stock_ledger_entries_created'],
        "total_amount_processed": submission_results['total_amount_processed'],
        "failed_details": submission_results['failed_details']
    }

def get_draft_sales_invoices(limit=None):
    """
    Get all draft sales invoices from the system
    """
    try:
        filters = {"docstatus": 0}  # Draft status
        
        fields = [
            "name", "company", "customer", "grand_total", "posting_date", 
            "is_return", "is_pos", "update_stock", "total_qty", "total"
        ]
        
        draft_invoices = frappe.get_all(
            "Sales Invoice",
            filters=filters,
            fields=fields,
            order_by="creation asc",
            limit=limit
        )
        
        print(f"🔍 Debug: Found {len(draft_invoices)} draft invoices")
        
        return draft_invoices
    except Exception as e:
        print(f"❌ Error getting draft sales invoices: {e}")
        return []

def submit_invoices_with_logging(draft_invoices, dry_run=False):
    """
    Submit sales invoices with comprehensive logging
    """
    successful_submissions = 0
    failed_submissions = 0
    gl_entries_created = 0
    stock_ledger_entries_created = 0
    total_amount_processed = 0
    failed_details = []
    
    total_to_process = len(draft_invoices)
    processed_count = 0
    
    print(f"\n📋 SUBMISSION LOG:")
    print("-" * 80)
    
    for invoice in draft_invoices:
        processed_count += 1
        try:
            print(f"📤 Processing Invoice: {invoice.name} ({processed_count}/{total_to_process})")
            print(f"   Company: {invoice.company}")
            print(f"   Customer: {invoice.customer}")
            print(f"   Amount: {invoice.grand_total}")
            print(f"   Update Stock: {invoice.update_stock}")
            
            if dry_run:
                print(f"   🔧 DRY RUN: Would submit {invoice.name}")
                successful_submissions += 1
                total_amount_processed += invoice.grand_total or 0
                continue
            
            # Check if invoice still exists and is still draft
            if not frappe.db.exists("Sales Invoice", invoice.name):
                print(f"   ⚠️  Invoice {invoice.name} no longer exists, skipping")
                failed_submissions += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": "Invoice no longer exists"
                })
                continue
            
            # Get the document
            doc = frappe.get_doc("Sales Invoice", invoice.name)
            
            if doc.docstatus != 0:
                print(f"   ⚠️  Invoice {invoice.name} is not in draft status (docstatus: {doc.docstatus}), skipping")
                failed_submissions += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": f"Invoice not in draft status (docstatus: {doc.docstatus})"
                })
                continue
            
            # Count existing GL entries before submission
            gl_entries_before = frappe.db.count("GL Entry", {
                "voucher_type": "Sales Invoice",
                "voucher_no": invoice.name
            })
            
            # Count existing Stock Ledger Entries before submission
            stock_ledger_entries_before = frappe.db.count("Stock Ledger Entry", {
                "voucher_type": "Sales Invoice",
                "voucher_no": invoice.name
            })
            
            print(f"   📊 Before submission - GL Entries: {gl_entries_before}, SLE: {stock_ledger_entries_before}")
            
            # Submit the invoice
            try:
                doc.submit()
                print(f"   ✅ Successfully submitted: {invoice.name}")
                
                # Count new GL entries created
                gl_entries_after = frappe.db.count("GL Entry", {
                    "voucher_type": "Sales Invoice",
                    "voucher_no": invoice.name
                })
                new_gl_entries = gl_entries_after - gl_entries_before
                gl_entries_created += new_gl_entries
                
                # Count new Stock Ledger Entries created
                stock_ledger_entries_after = frappe.db.count("Stock Ledger Entry", {
                    "voucher_type": "Sales Invoice",
                    "voucher_no": invoice.name
                })
                new_sle = stock_ledger_entries_after - stock_ledger_entries_before
                stock_ledger_entries_created += new_sle
                
                print(f"   📊 After submission - New GL Entries: {new_gl_entries}, New SLE: {new_sle}")
                
                successful_submissions += 1
                total_amount_processed += invoice.grand_total or 0
                
                # Log GL entries created
                if new_gl_entries > 0:
                    gl_entries = frappe.get_all("GL Entry", 
                        filters={
                            "voucher_type": "Sales Invoice",
                            "voucher_no": invoice.name
                        }, 
                        fields=["name", "account", "debit", "credit"]
                    )
                    
                    print(f"   💰 GL Entries created:")
                    for gl in gl_entries:
                        print(f"      - {gl.name}: {gl.account} | Debit: {gl.debit} | Credit: {gl.credit}")
                
                # Log Stock Ledger Entries created
                if new_sle > 0 and invoice.update_stock:
                    sle_entries = frappe.get_all("Stock Ledger Entry", 
                        filters={
                            "voucher_type": "Sales Invoice",
                            "voucher_no": invoice.name
                        }, 
                        fields=["name", "item_code", "warehouse", "actual_qty"]
                    )
                    
                    print(f"   📦 Stock Ledger Entries created:")
                    for sle in sle_entries:
                        print(f"      - {sle.name}: {sle.item_code} | {sle.warehouse} | Qty: {sle.actual_qty}")
                
            except Exception as submit_error:
                print(f"   ❌ Failed to submit {invoice.name}: {submit_error}")
                failed_submissions += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": str(submit_error)
                })
                
                # Log detailed error information
                print(f"   🔍 Error details: {submit_error}")
                if hasattr(submit_error, 'args') and submit_error.args:
                    print(f"   🔍 Error args: {submit_error.args}")
            
        except Exception as e:
            print(f"❌ Error processing invoice {invoice.name}: {e}")
            failed_submissions += 1
            failed_details.append({
                "invoice_name": invoice.name,
                "error": str(e)
            })
    
    return {
        "successful_submissions": successful_submissions,
        "failed_submissions": failed_submissions,
        "gl_entries_created": gl_entries_created,
        "stock_ledger_entries_created": stock_ledger_entries_created,
        "total_amount_processed": total_amount_processed,
        "failed_details": failed_details
    }

def get_draft_invoices_summary():
    """
    Get a summary of all draft sales invoices in the system
    """
    print("=" * 80)
    print("DRAFT SALES INVOICES SUMMARY REPORT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print("=" * 80)
    
    try:
        # Get all draft sales invoices
        draft_invoices = get_draft_sales_invoices()
        
        if not draft_invoices:
            print("✅ No draft sales invoices found.")
            return {
                "total_invoices": 0,
                "company_distribution": {},
                "customer_distribution": {},
                "return_distribution": {},
                "total_amount": 0
            }
        
        # Analyze by company and customer
        company_counts = {}
        customer_counts = {}
        return_counts = {"returns": 0, "non_returns": 0}
        total_amount = 0
        
        for invoice in draft_invoices:
            company = invoice.company
            customer = invoice.customer
            amount = invoice.grand_total or 0
            is_return = invoice.is_return
            
            company_counts[company] = company_counts.get(company, 0) + 1
            customer_counts[customer] = customer_counts.get(customer, 0) + 1
            total_amount += amount
            
            if is_return:
                return_counts["returns"] += 1
            else:
                return_counts["non_returns"] += 1
        
        print(f"\n📊 DRAFT INVOICES OVERVIEW:")
        print(f"   Total Draft Invoices: {len(draft_invoices)}")
        print(f"   Total Amount: {total_amount}")
        print(f"   Returns: {return_counts['returns']}")
        print(f"   Non-Returns: {return_counts['non_returns']}")
        
        print(f"\n📋 Company Distribution:")
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count}")
        
        print(f"\n👥 Customer Distribution (Top 10):")
        for customer, count in sorted(customer_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {customer}: {count}")
        if len(customer_counts) > 10:
            print(f"   ... and {len(customer_counts) - 10} more customers")
        
        return {
            "total_invoices": len(draft_invoices),
            "company_distribution": company_counts,
            "customer_distribution": customer_counts,
            "return_distribution": return_counts,
            "total_amount": total_amount
        }
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return {
            "error": str(e)
        }
