#!/usr/bin/env python3
"""
Bench command to repost all submitted Sales Invoices and Return Invoices with updated purchase prices.
This script completely removes all previous postings and creates fresh ones with updated rates.

Usage: bench --site your-site.com execute custom_erp.management.commands.repost_sales_invoices_with_updated_prices.repost_sales_invoices_with_updated_prices

Features:
- Handles all submitted sales invoices and return invoices
- Completely removes all previous GL entries, Stock Ledger Entries, and other postings
- Updates item rates from Item Master valuation rate
- Recalculates all totals (total, net total, taxable amount, grand total)
- Preserves tax rates and additional discount amounts
- Comprehensive logging and summary reporting
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, flt
import json
from datetime import datetime

def repost_sales_invoices_with_updated_prices():
    """
    Main function to repost all submitted sales invoices with updated purchase prices
    """
    print("=" * 100)
    print("REPOST SALES INVOICES WITH UPDATED PURCHASE PRICES")
    print("=" * 100)
    print(f"Timestamp: {now_datetime()}")
    print("Mode: DRY RUN (use repost_sales_invoices_with_updated_prices_confirm() for actual reposting)")
    print("=" * 100)
    
    # Get all submitted sales invoices
    submitted_invoices = get_submitted_sales_invoices()
    
    if not submitted_invoices:
        print("✅ No submitted sales invoices found.")
        return {
            "status": "success",
            "message": "No submitted sales invoices found",
            "total_invoices": 0,
            "processed_invoices": 0,
            "summary": {}
        }
    
    print(f"📄 Found {len(submitted_invoices)} submitted sales invoices to repost:")
    print("-" * 100)
    
    # Analyze submitted invoices
    analysis = analyze_submitted_invoices(submitted_invoices)
    
    print_analysis_summary(analysis)
    
    # Show warning
    print("\n" + "=" * 100)
    print("⚠️  WARNING - THIS OPERATION WILL:")
    print("=" * 100)
    print("1. ❌ COMPLETELY REMOVE all existing GL Entries for these invoices")
    print("2. ❌ COMPLETELY REMOVE all existing Stock Ledger Entries for these invoices")
    print("3. ❌ COMPLETELY REMOVE all existing Payment Ledger Entries for these invoices")
    print("4. ❌ COMPLETELY REMOVE all existing Sales Invoice Advance entries")
    print("5. ❌ COMPLETELY REMOVE all existing Sales Invoice Payment entries")
    print("6. ✅ Update item rates from Item Master valuation rates")
    print("7. ✅ Recalculate all totals with new rates")
    print("8. ✅ Create completely fresh GL Entries")
    print("9. ✅ Create completely fresh Stock Ledger Entries")
    print("10. ✅ Create completely fresh Payment Ledger Entries")
    print("11. ✅ Update customer balances with new amounts")
    
    print(f"\n🔧 DRY RUN: Would repost {len(submitted_invoices)} submitted invoices")
    print("Run repost_sales_invoices_with_updated_prices_confirm() to actually proceed")
    
    return {
        "status": "dry_run",
        "message": "Dry run completed - use repost_sales_invoices_with_updated_prices_confirm() to proceed",
        "total_invoices": len(submitted_invoices),
        "summary": analysis
    }

def repost_sales_invoices_with_updated_prices_confirm():
    """
    Actually repost all submitted sales invoices with updated purchase prices
    """
    print("=" * 100)
    print("REPOST SALES INVOICES WITH UPDATED PURCHASE PRICES - CONFIRMED")
    print("=" * 100)
    print(f"Timestamp: {now_datetime()}")
    print("Mode: REPOSTING (ACTUAL REPOSTING)")
    print("=" * 100)
    
    # Get all submitted sales invoices
    submitted_invoices = get_submitted_sales_invoices()
    
    if not submitted_invoices:
        print("✅ No submitted sales invoices found.")
        return {
            "status": "success",
            "message": "No submitted sales invoices found",
            "total_invoices": 0,
            "processed_invoices": 0,
            "summary": {}
        }
    
    print(f"🔄 REPOSTING {len(submitted_invoices)} SUBMITTED SALES INVOICES...")
    
    repost_results = repost_invoices_with_logging(submitted_invoices, dry_run=False)
    
    print("\n" + "=" * 100)
    print("REPOSTING COMPLETE")
    print("=" * 100)
    print(f"✅ Successfully reposted: {repost_results['successful_reposts']}")
    print(f"❌ Failed reposts: {repost_results['failed_reposts']}")
    print(f"📊 Total GL Entries recreated: {repost_results['gl_entries_recreated']}")
    print(f"📦 Total Stock Ledger Entries recreated: {repost_results['stock_ledger_entries_recreated']}")
    print(f"💰 Total amount processed: {repost_results['total_amount_processed']}")
    print(f"🔄 Total items updated with new rates: {repost_results['items_updated']}")
    
    # Show failed reposts
    if repost_results['failed_reposts'] > 0:
        print(f"\n❌ FAILED REPOSTS:")
        for failed in repost_results['failed_details']:
            print(f"   {failed['invoice_name']}: {failed['error']}")
    
    # Final verification
    print(f"\n🔍 FINAL VERIFICATION:")
    total_submitted = frappe.db.count("Sales Invoice", {"docstatus": 1})
    total_invoices = frappe.db.count("Sales Invoice")
    print(f"   Total submitted invoices: {total_submitted}")
    print(f"   Total invoices in system: {total_invoices}")
    
    return {
        "status": "success",
        "message": "Sales invoice reposting completed",
        "total_invoices": len(submitted_invoices),
        "successful_reposts": repost_results['successful_reposts'],
        "failed_reposts": repost_results['failed_reposts'],
        "gl_entries_recreated": repost_results['gl_entries_recreated'],
        "stock_ledger_entries_recreated": repost_results['stock_ledger_entries_recreated'],
        "total_amount_processed": repost_results['total_amount_processed'],
        "items_updated": repost_results['items_updated'],
        "failed_details": repost_results['failed_details']
    }

def get_submitted_sales_invoices():
    """
    Get all submitted sales invoices from the system
    """
    try:
        filters = {"docstatus": 1}  # Submitted status
        
        # Start with basic fields that should always exist
        fields = [
            "name", "company", "customer", "grand_total", "posting_date", 
            "is_return", "is_pos", "update_stock", "total_qty", "total"
        ]
        
        # Try to add optional fields, but don't fail if they don't exist
        try:
            test_invoice = frappe.get_all("Sales Invoice", filters=filters, fields=["net_total"], limit=1)
            if test_invoice:
                fields.extend(["net_total", "total_taxes_and_charges", "discount_amount"])
        except:
            print("   ⚠️  Some optional fields not available, using basic fields only")
        
        submitted_invoices = frappe.get_all(
            "Sales Invoice",
            filters=filters,
            fields=fields,
            order_by="posting_date asc, creation asc"
        )
        
        print(f"🔍 Debug: Found {len(submitted_invoices)} submitted invoices")
        print(f"   Fields being retrieved: {fields}")
        
        return submitted_invoices
    except Exception as e:
        print(f"❌ Error getting submitted sales invoices: {e}")
        print(f"   Error details: {str(e)}")
        return []

def analyze_submitted_invoices(submitted_invoices):
    """
    Analyze submitted invoices for comprehensive reporting
    """
    company_counts = {}
    customer_counts = {}
    total_amount = 0
    return_counts = {"returns": 0, "non_returns": 0}
    stock_update_counts = {"with_stock": 0, "without_stock": 0}
    pos_counts = {"pos": 0, "non_pos": 0}
    
    for invoice in submitted_invoices:
        company = invoice.company
        customer = invoice.customer
        amount = invoice.grand_total or 0
        is_return = invoice.is_return
        update_stock = invoice.update_stock
        is_pos = invoice.is_pos
        
        company_counts[company] = company_counts.get(company, 0) + 1
        customer_counts[customer] = customer_counts.get(customer, 0) + 1
        total_amount += amount
        
        if is_return:
            return_counts["returns"] += 1
        else:
            return_counts["non_returns"] += 1
            
        if update_stock:
            stock_update_counts["with_stock"] += 1
        else:
            stock_update_counts["without_stock"] += 1
            
        if is_pos:
            pos_counts["pos"] += 1
        else:
            pos_counts["non_pos"] += 1
    
    return {
        "total_invoices": len(submitted_invoices),
        "total_amount": total_amount,
        "return_counts": return_counts,
        "stock_update_counts": stock_update_counts,
        "pos_counts": pos_counts,
        "company_counts": company_counts,
        "customer_counts": customer_counts
    }

def print_analysis_summary(analysis):
    """
    Print comprehensive analysis summary
    """
    print(f"\n📊 ANALYSIS SUMMARY:")
    print(f"   Total Submitted Invoices: {analysis['total_invoices']}")
    print(f"   Total Amount: {analysis['total_amount']}")
    print(f"   Returns: {analysis['return_counts']['returns']}")
    print(f"   Non-Returns: {analysis['return_counts']['non_returns']}")
    print(f"   With Stock Updates: {analysis['stock_update_counts']['with_stock']}")
    print(f"   Without Stock Updates: {analysis['stock_update_counts']['without_stock']}")
    print(f"   POS Invoices: {analysis['pos_counts']['pos']}")
    print(f"   Non-POS Invoices: {analysis['pos_counts']['non_pos']}")
    
    print(f"\n📋 Company Distribution:")
    for company, count in sorted(analysis['company_counts'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {company}: {count}")
    
    print(f"\n👥 Customer Distribution (Top 10):")
    for customer, count in sorted(analysis['customer_counts'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {customer}: {count}")
    if len(analysis['customer_counts']) > 10:
        print(f"   ... and {len(analysis['customer_counts']) - 10} more customers")

def repost_invoices_with_logging(submitted_invoices, dry_run=False):
    """
    Repost sales invoices with comprehensive logging
    """
    successful_reposts = 0
    failed_reposts = 0
    gl_entries_recreated = 0
    stock_ledger_entries_recreated = 0
    total_amount_processed = 0
    items_updated = 0
    failed_details = []
    
    total_to_process = len(submitted_invoices)
    processed_count = 0
    
    print(f"\n📋 REPOSTING LOG:")
    print("-" * 100)
    
    for invoice in submitted_invoices:
        processed_count += 1
        try:
            print(f"🔄 Processing Invoice: {invoice.name} ({processed_count}/{total_to_process})")
            print(f"   Company: {invoice.company}")
            print(f"   Customer: {invoice.customer}")
            print(f"   Amount: {invoice.grand_total}")
            print(f"   Update Stock: {invoice.update_stock}")
            print(f"   Is Return: {invoice.is_return}")
            
            if dry_run:
                print(f"   🔧 DRY RUN: Would repost {invoice.name}")
                successful_reposts += 1
                total_amount_processed += invoice.grand_total or 0
                continue
            
            # Check if invoice still exists and is still submitted
            if not frappe.db.exists("Sales Invoice", invoice.name):
                print(f"   ⚠️  Invoice {invoice.name} no longer exists, skipping")
                failed_reposts += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": "Invoice no longer exists"
                })
                continue
            
            # Get the document
            doc = frappe.get_doc("Sales Invoice", invoice.name)
            
            if doc.docstatus != 1:
                print(f"   ⚠️  Invoice {invoice.name} is not in submitted status (docstatus: {doc.docstatus}), skipping")
                failed_reposts += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": f"Invoice not in submitted status (docstatus: {doc.docstatus})"
                })
                continue
            
            # Count existing entries before reposting
            entries_before = count_existing_entries(invoice.name)
            print(f"   📊 Before reposting - GL: {entries_before['gl']}, SLE: {entries_before['sle']}, PLE: {entries_before['ple']}")
            
            # Repost the invoice
            try:
                repost_result = repost_single_invoice(doc)
                
                if repost_result['success']:
                    print(f"   ✅ Successfully reposted: {invoice.name}")
                    
                    # Count new entries created
                    entries_after = count_existing_entries(invoice.name)
                    new_gl = entries_after['gl'] - entries_before['gl']
                    new_sle = entries_after['sle'] - entries_before['sle']
                    new_ple = entries_after['ple'] - entries_before['ple']
                    
                    gl_entries_recreated += new_gl
                    stock_ledger_entries_recreated += new_sle
                    items_updated += repost_result['items_updated']
                    
                    print(f"   📊 After reposting - New GL: {new_gl}, New SLE: {new_sle}, New PLE: {new_ple}")
                    print(f"   🔄 Items updated with new rates: {repost_result['items_updated']}")
                    print(f"   💰 New total amount: {repost_result['new_total']}")
                    
                    successful_reposts += 1
                    total_amount_processed += repost_result['new_total'] or 0
                    
                else:
                    print(f"   ❌ Failed to repost {invoice.name}: {repost_result['error']}")
                    failed_reposts += 1
                    failed_details.append({
                        "invoice_name": invoice.name,
                        "error": repost_result['error']
                    })
                
            except Exception as repost_error:
                print(f"   ❌ Failed to repost {invoice.name}: {repost_error}")
                failed_reposts += 1
                failed_details.append({
                    "invoice_name": invoice.name,
                    "error": str(repost_error)
                })
                
                # Log detailed error information
                print(f"   🔍 Error details: {repost_error}")
                if hasattr(repost_error, 'args') and repost_error.args:
                    print(f"   🔍 Error args: {repost_error.args}")
            
        except Exception as e:
            print(f"❌ Error processing invoice {invoice.name}: {e}")
            failed_reposts += 1
            failed_details.append({
                "invoice_name": invoice.name,
                "error": str(e)
            })
    
    return {
        "successful_reposts": successful_reposts,
        "failed_reposts": failed_reposts,
        "gl_entries_recreated": gl_entries_recreated,
        "stock_ledger_entries_recreated": stock_ledger_entries_recreated,
        "total_amount_processed": total_amount_processed,
        "items_updated": items_updated,
        "failed_details": failed_details
    }

def count_existing_entries(invoice_name):
    """
    Count existing entries for an invoice
    """
    try:
        gl_count = frappe.db.count("GL Entry", {
            "voucher_type": "Sales Invoice",
            "voucher_no": invoice_name
        })
        
        sle_count = frappe.db.count("Stock Ledger Entry", {
            "voucher_type": "Sales Invoice",
            "voucher_no": invoice_name
        })
        
        ple_count = frappe.db.count("Payment Ledger Entry", {
            "voucher_type": "Sales Invoice",
            "voucher_no": invoice_name
        })
        
        return {
            "gl": gl_count,
            "sle": sle_count,
            "ple": ple_count
        }
    except Exception as e:
        print(f"   ⚠️  Error counting entries: {e}")
        return {"gl": 0, "sle": 0, "ple": 0}

def repost_single_invoice(doc):
    """
    Repost a single sales invoice with updated purchase prices
    """
    try:
        print(f"      🔄 Starting repost for {doc.name}")
        
        # Store original values for comparison
        original_total = getattr(doc, 'total', 0) or 0
        original_net_total = getattr(doc, 'net_total', 0) or 0
        original_grand_total = getattr(doc, 'grand_total', 0) or 0
        original_taxable_amount = getattr(doc, 'total_taxes_and_charges', 0) or 0
        
        # Store original tax and discount amounts
        original_tax_amount = getattr(doc, 'total_taxes_and_charges', 0) or 0
        original_discount = getattr(doc, 'discount_amount', 0) or 0
        
        print(f"      📊 Original values - Total: {original_total}, Net: {original_net_total}, Grand: {original_grand_total}")
        
        # Step 1: Cancel the invoice to remove all postings
        print(f"      ❌ Cancelling invoice to remove existing postings...")
        doc.cancel()
        
        # Step 2: Update item rates from Item Master valuation rates
        print(f"      🔄 Updating item rates from Item Master...")
        items_updated = update_item_rates_from_master(doc)
        
        # Step 3: Recalculate totals
        print(f"      🧮 Recalculating totals with new rates...")
        recalculate_invoice_totals(doc)
        
        # Step 4: Restore tax and discount amounts
        print(f"      💰 Restoring tax and discount amounts...")
        restore_tax_and_discount_amounts(doc, original_tax_amount, original_discount)
        
        # Step 5: Submit the invoice to create fresh postings
        print(f"      ✅ Submitting invoice with new rates...")
        doc.submit()
        
        # Get new values for comparison
        new_total = getattr(doc, 'total', 0) or 0
        new_net_total = getattr(doc, 'net_total', 0) or 0
        new_grand_total = getattr(doc, 'grand_total', 0) or 0
        
        print(f"      📊 New values - Total: {new_total}, Net: {new_net_total}, Grand: {new_grand_total}")
        print(f"      🔄 Rate change impact - Total: {new_total - original_total}, Net: {new_net_total - original_net_total}, Grand: {new_grand_total - original_grand_total}")
        
        return {
            "success": True,
            "items_updated": items_updated,
            "new_total": new_grand_total,
            "original_total": original_grand_total,
            "rate_change_impact": new_grand_total - original_grand_total
        }
        
    except Exception as e:
        print(f"      ❌ Error during repost: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def update_item_rates_from_master(doc):
    """
    Update item rates from Item Master valuation rates
    """
    items_updated = 0
    
    try:
        for item in doc.items:
            # Get current item rate
            old_rate = getattr(item, 'rate', 0) or 0
            
            try:
                # Get valuation rate from Item Master
                item_master = frappe.get_doc("Item", item.item_code)
                new_rate = getattr(item_master, 'valuation_rate', 0) or getattr(item_master, 'standard_rate', 0) or old_rate
                
                if new_rate != old_rate:
                    print(f"         🔄 Item {getattr(item, 'item_code', 'Unknown')}: {old_rate} → {new_rate}")
                    item.rate = new_rate
                    items_updated += 1
                else:
                    print(f"         ✅ Item {getattr(item, 'item_code', 'Unknown')}: Rate unchanged ({old_rate})")
            except Exception as item_error:
                print(f"         ⚠️  Error updating item {getattr(item, 'item_code', 'Unknown')}: {item_error}")
                # Continue with next item
        
        # Save the document to update the rates
        doc.save()
        
        print(f"         📝 Updated rates for {items_updated} items")
        return items_updated
        
    except Exception as e:
        print(f"         ❌ Error updating item rates: {e}")
        return 0

def recalculate_invoice_totals(doc):
    """
    Recalculate all invoice totals with new rates
    """
    try:
        # Recalculate item totals
        for item in doc.items:
            item.amount = flt(getattr(item, 'rate', 0) * getattr(item, 'qty', 0), 2)
            print(f"         🧮 Item {getattr(item, 'item_code', 'Unknown')}: {getattr(item, 'rate', 0)} × {getattr(item, 'qty', 0)} = {item.amount}")
        
        # Recalculate invoice totals
        doc.total = sum(flt(getattr(item, 'amount', 0)) for item in doc.items)
        doc.net_total = doc.total - flt(getattr(doc, 'discount_amount', 0) or 0)
        
        # Recalculate taxes (preserve tax rates, recalculate taxable amounts)
        if hasattr(doc, 'taxes') and doc.taxes:
            for tax in doc.taxes:
                if hasattr(tax, 'charge_type') and tax.charge_type == "On Net Total":
                    tax.tax_amount = flt(doc.net_total * flt(getattr(tax, 'rate', 0)) / 100, 2)
                elif hasattr(tax, 'charge_type') and tax.charge_type == "On Grand Total":
                    # This will be calculated after all other taxes
                    pass
                print(f"         🧮 Tax {getattr(tax, 'description', 'Unknown')}: {getattr(tax, 'tax_amount', 0)}")
        
        # Calculate total taxes
        if hasattr(doc, 'taxes') and doc.taxes:
            doc.total_taxes_and_charges = sum(flt(getattr(tax, 'tax_amount', 0)) for tax in doc.taxes)
        else:
            doc.total_taxes_and_charges = 0
        
        # Calculate grand total
        doc.grand_total = doc.net_total + doc.total_taxes_and_charges
        
        print(f"         📊 Recalculated totals - Total: {doc.total}, Net: {doc.net_total}, Taxes: {doc.total_taxes_and_charges}, Grand: {doc.grand_total}")
        
    except Exception as e:
        print(f"         ❌ Error recalculating totals: {e}")
        raise e

def restore_tax_and_discount_amounts(doc, original_tax_amount, original_discount):
    """
    Restore original tax and discount amounts
    """
    try:
        # Restore discount amount
        if original_discount:
            doc.discount_amount = original_discount
            print(f"         💰 Restored discount: {original_discount}")
        
        # Restore tax amounts if they were manually set
        if hasattr(doc, 'taxes') and doc.taxes and original_tax_amount:
            # Find the main tax entry (usually the first one)
            for tax in doc.taxes:
                if hasattr(tax, 'charge_type') and tax.charge_type == "On Net Total":
                    # Adjust the tax rate to match the original amount
                    if doc.net_total > 0:
                        adjusted_rate = flt((original_tax_amount / doc.net_total) * 100, 2)
                        tax.rate = adjusted_rate
                        tax.tax_amount = original_tax_amount
                        print(f"         💰 Restored tax amount: {original_tax_amount} (rate: {adjusted_rate}%)")
                    break
        
        # Recalculate grand total with restored amounts
        doc.grand_total = doc.net_total + getattr(doc, 'total_taxes_and_charges', 0)
        print(f"         📊 Final grand total: {doc.grand_total}")
        
    except Exception as e:
        print(f"         ❌ Error restoring tax and discount amounts: {e}")
        raise e

def get_submitted_invoices_summary():
    """
    Get a summary of all submitted sales invoices in the system
    """
    print("=" * 100)
    print("SUBMITTED SALES INVOICES SUMMARY REPORT")
    print("=" * 100)
    print(f"Timestamp: {now_datetime()}")
    print("=" * 100)
    
    try:
        # Get all submitted sales invoices
        submitted_invoices = get_submitted_sales_invoices()
        
        if not submitted_invoices:
            print("✅ No submitted sales invoices found.")
            return {
                "total_invoices": 0,
                "company_distribution": {},
                "customer_distribution": {},
                "return_distribution": {},
                "total_amount": 0
            }
        
        # Analyze by company and customer
        analysis = analyze_submitted_invoices(submitted_invoices)
        
        print(f"\n📊 SUBMITTED INVOICES OVERVIEW:")
        print(f"   Total Submitted Invoices: {analysis['total_invoices']}")
        print(f"   Total Amount: {analysis['total_amount']}")
        print(f"   Returns: {analysis['return_counts']['returns']}")
        print(f"   Non-Returns: {analysis['return_counts']['non_returns']}")
        print(f"   With Stock Updates: {analysis['stock_update_counts']['with_stock']}")
        print(f"   Without Stock Updates: {analysis['stock_update_counts']['without_stock']}")
        
        print(f"\n📋 Company Distribution:")
        for company, count in sorted(analysis['company_counts'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count}")
        
        print(f"\n👥 Customer Distribution (Top 10):")
        for customer, count in sorted(analysis['customer_counts'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {customer}: {count}")
        if len(analysis['customer_counts']) > 10:
            print(f"   ... and {len(analysis['customer_counts']) - 10} more customers")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return {
            "error": str(e)
        }

def test_repost_single_invoice(invoice_name):
    """
    Test reposting a single invoice (for testing purposes)
    """
    print("=" * 100)
    print(f"TEST REPOSTING SINGLE INVOICE: {invoice_name}")
    print("=" * 100)
    print(f"Timestamp: {now_datetime()}")
    print("=" * 100)
    
    try:
        if not frappe.db.exists("Sales Invoice", invoice_name):
            print(f"❌ Invoice {invoice_name} does not exist")
            return {"success": False, "error": "Invoice does not exist"}
        
        doc = frappe.get_doc("Sales Invoice", invoice_name)
        
        if doc.docstatus != 1:
            print(f"❌ Invoice {invoice_name} is not submitted (docstatus: {doc.docstatus})")
            return {"success": False, "error": f"Invoice not submitted (docstatus: {doc.docstatus})"}
        
        print(f"📄 Invoice Details:")
        print(f"   Company: {doc.company}")
        print(f"   Customer: {doc.customer}")
        print(f"   Total: {doc.total}")
        print(f"   Net Total: {doc.net_total}")
        print(f"   Grand Total: {doc.grand_total}")
        print(f"   Update Stock: {doc.update_stock}")
        print(f"   Is Return: {doc.is_return}")
        
        print(f"\n📦 Items:")
        for item in doc.items:
            print(f"   {item.item_code}: {item.qty} × {item.rate} = {item.amount}")
        
        print(f"\n🧮 Taxes:")
        for tax in doc.taxes:
            print(f"   {tax.description}: {tax.rate}% = {tax.tax_amount}")
        
        # Test the repost
        repost_result = repost_single_invoice(doc)
        
        if repost_result['success']:
            print(f"\n✅ Test repost successful!")
            print(f"   Items updated: {repost_result['items_updated']}")
            print(f"   Rate change impact: {repost_result['rate_change_impact']}")
        else:
            print(f"\n❌ Test repost failed: {repost_result['error']}")
        
        return repost_result
        
    except Exception as e:
        print(f"❌ Error during test repost: {e}")
        return {"success": False, "error": str(e)}

# Main execution functions
if __name__ == "__main__":
    # These functions can be called directly from the command line
    pass
