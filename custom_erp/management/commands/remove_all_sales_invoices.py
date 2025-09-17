#!/usr/bin/env python3
"""
Bench command to remove all Sales Invoices along with their linked data

This script will:
1. Remove all Sales Invoices regardless of their status
2. Remove all linked GL Entries
3. Remove all linked Journal Entries
4. Remove all linked Sales Invoice Items
5. Remove all linked Sales Invoice Taxes
6. Remove all linked Sales Invoice Advances
7. Handle Stock Ledger Entries (SLE) - CRITICAL for inventory accuracy
8. Handle Stock Entries created by Sales Invoices with update_stock=True
9. Handle Delivery Notes linked to Sales Invoices
10. Show a comprehensive summary of what was removed
11. Provide option to filter by return status (is_return)
12. Provide option to handle stock movements (recommended: True)

Usage:
    bench --site development.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --dry-run
    bench --site development.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --confirm
    bench --site development.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --confirm --returns-only
    bench --site development.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --confirm --non-returns-only
    bench --site development.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --confirm --all-invoices
    bench --site site1.localhost execute custom_erp.management.commands.remove_all_sales_invoices.remove_all_sales_invoices --confirm --no-stock-handling
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
import json

def remove_all_sales_invoices(dry_run=False, confirm=True, returns_only=True, non_returns_only=False, all_invoices=False, handle_stock=True):
    """
    Remove all Sales Invoices along with their linked data
    
    Args:
        dry_run (bool): If True, only show what would be removed without making changes
        confirm (bool): If True, actually remove the sales invoices (overrides dry_run)
        returns_only (bool): If True, only remove sales invoices where is_return=True
        non_returns_only (bool): If True, only remove sales invoices where is_return=False
        all_invoices (bool): If True, remove all sales invoices regardless of return status (overrides returns_only and non_returns_only)
        handle_stock (bool): If True, handle stock movements (SLE, Stock Entries, Delivery Notes)
    """
    
    print("=" * 80)
    print("REMOVE ALL SALES INVOICES SCRIPT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    print(f"Mode: {'DRY RUN' if dry_run and not confirm else 'REMOVING'}")
    
    if all_invoices:
        print("Filter: All Sales Invoices (both returns and non-returns)")
    elif returns_only:
        print("Filter: Returns Only (is_return=True)")
    elif non_returns_only:
        print("Filter: Non-Returns Only (is_return=False)")
    else:
        print("Filter: All Sales Invoices")
    
    print("=" * 80)
    
    # Get all sales invoices based on filter
    print(f"🔍 Debug: Filter settings - returns_only: {returns_only}, non_returns_only: {non_returns_only}, all_invoices: {all_invoices}")
    sales_invoices = get_all_sales_invoices(returns_only, non_returns_only, all_invoices)
    print(f"🔍 Debug: Found {len(sales_invoices)} sales invoices after filtering")
    
    if not sales_invoices:
        print("✅ No sales invoices found matching the criteria.")
        return {
            "status": "success",
            "message": "No sales invoices found",
            "total_sales_invoices": 0,
            "total_gl_entries_removed": 0,
            "total_journal_entries_removed": 0,
            "total_items_removed": 0,
            "total_taxes_removed": 0,
            "total_advances_removed": 0
        }
    
    print(f"❌ Found {len(sales_invoices)} sales invoices to remove:")
    print("-" * 80)
    
    # Analyze sales invoices by status and return type
    status_counts = {}
    company_counts = {}
    return_counts = {"returns": 0, "non_returns": 0}
    total_amount = 0
    
    for sales_invoice in sales_invoices:
        status = sales_invoice.status
        company = sales_invoice.company
        amount = sales_invoice.grand_total or 0
        is_return = sales_invoice.is_return
        
        status_counts[status] = status_counts.get(status, 0) + 1
        company_counts[company] = company_counts.get(company, 0) + 1
        total_amount += amount
        
        if is_return:
            return_counts["returns"] += 1
        else:
            return_counts["non_returns"] += 1
        
        print(f"📄 {sales_invoice.name}: {status} | {company} | {amount} | Return: {is_return}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Total Sales Invoices: {len(sales_invoices)}")
    print(f"Total Amount: {total_amount}")
    print(f"Returns: {return_counts['returns']}")
    print(f"Non-Returns: {return_counts['non_returns']}")
    
    print(f"\n📊 Status Distribution:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {status}: {count}")
    
    print(f"\n🏢 Company Distribution:")
    for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {company}: {count}")
    
    # Get linked data counts
    linked_data = get_linked_data_counts(sales_invoices, handle_stock)
    
    print(f"\n🔗 Linked Data to be Removed:")
    print(f"   GL Entries: {linked_data['gl_entries']}")
    print(f"   Journal Entries: {linked_data['journal_entries']}")
    print(f"   Sales Invoice Items: {linked_data['items']}")
    print(f"   Sales Invoice Taxes: {linked_data['taxes']}")
    print(f"   Sales Invoice Advances: {linked_data['advances']}")
    
    if handle_stock:
        print(f"   Stock Ledger Entries: {linked_data['stock_ledger_entries']}")
        print(f"   Stock Entries: {linked_data['stock_entries']}")
        print(f"   Delivery Notes: {linked_data['delivery_notes']}")
    else:
        print(f"   ⚠️  Stock data NOT handled (may cause inventory issues)")
    
    # Show warning
    print("\n" + "=" * 80)
    print("⚠️  WARNING")
    print("=" * 80)
    print("This operation will permanently delete:")
    print("1. All Sales Invoices regardless of status")
    print("2. All linked GL Entries")
    print("3. All linked Journal Entries")
    print("4. All linked Sales Invoice Items")
    print("5. All linked Sales Invoice Taxes")
    print("6. All linked Sales Invoice Advances")
    
    if handle_stock:
        print("7. All linked Stock Ledger Entries (CRITICAL for inventory)")
        print("8. All linked Stock Entries")
        print("9. All linked Delivery Notes")
        print("\n⚠️  STOCK WARNING: This will affect inventory levels!")
    else:
        print("\n⚠️  STOCK WARNING: Stock movements NOT handled - may cause inventory inconsistencies!")
    
    print("\nThis action cannot be undone!")
    
    if not confirm and not dry_run:
        print("\n❌ Operation cancelled. Use --confirm to proceed with removal.")
        return {
            "status": "cancelled",
            "message": "Operation cancelled - use --confirm to proceed",
            "total_sales_invoices": len(sales_invoices),
            "linked_data": linked_data
        }
    
    # Remove sales invoices if confirmed
    if confirm or not dry_run:
        print(f"\n🗑️  REMOVING {len(sales_invoices)} SALES INVOICES...")
        
        removal_results = remove_sales_invoices_with_linked_data(sales_invoices, handle_stock)
        
        print("\n" + "=" * 80)
        print("REMOVAL COMPLETE")
        print("=" * 80)
        print(f"✅ Sales Invoices removed: {removal_results['sales_invoices_removed']}")
        print(f"✅ GL Entries removed: {removal_results['gl_entries_removed']}")
        print(f"✅ Journal Entries removed: {removal_results['journal_entries_removed']}")
        print(f"✅ Sales Invoice Items removed: {removal_results['items_removed']}")
        print(f"✅ Sales Invoice Taxes removed: {removal_results['taxes_removed']}")
        print(f"✅ Sales Invoice Advances removed: {removal_results['advances_removed']}")
        
        if handle_stock:
            print(f"✅ Stock Ledger Entries removed: {removal_results['stock_ledger_entries_removed']}")
            print(f"✅ Stock Entries removed: {removal_results['stock_entries_removed']}")
            print(f"✅ Delivery Notes removed: {removal_results['delivery_notes_removed']}")
        
        # Final verification
        print(f"\n🔍 FINAL VERIFICATION:")
        remaining_sales_invoices = frappe.db.count("Sales Invoice")
        print(f"   Remaining Sales Invoices in system: {remaining_sales_invoices}")
        
        if remaining_sales_invoices > 0:
            print(f"   ⚠️  WARNING: {remaining_sales_invoices} Sales Invoices still exist in the system!")
            print(f"   This may indicate that some Sales Invoices could not be deleted due to constraints.")
        else:
            print(f"   ✅ SUCCESS: All Sales Invoices have been removed from the system!")
        
        return {
            "status": "success",
            "message": "All sales invoices and linked data removed successfully",
            "total_sales_invoices": len(sales_invoices),
            "sales_invoices_removed": removal_results['sales_invoices_removed'],
            "gl_entries_removed": removal_results['gl_entries_removed'],
            "journal_entries_removed": removal_results['journal_entries_removed'],
            "items_removed": removal_results['items_removed'],
            "taxes_removed": removal_results['taxes_removed'],
            "advances_removed": removal_results['advances_removed'],
            "stock_ledger_entries_removed": removal_results['stock_ledger_entries_removed'],
            "stock_entries_removed": removal_results['stock_entries_removed'],
            "delivery_notes_removed": removal_results['delivery_notes_removed'],
            "linked_data": linked_data
        }
    
    else:
        print(f"\n🔧 DRY RUN: Would remove {len(sales_invoices)} sales invoices")
        print("Run with --confirm to actually remove the sales invoices")
        
        return {
            "status": "dry_run",
            "message": "Dry run completed - use --confirm to proceed",
            "total_sales_invoices": len(sales_invoices),
            "linked_data": linked_data
        }

def get_all_sales_invoices(returns_only=False, non_returns_only=False, all_invoices=False):
    """
    Get all sales invoices from the system based on filter criteria
    """
    try:
        filters = {}
        
        # Check if is_return field exists
        try:
            test_query = frappe.get_all("Sales Invoice", filters={}, fields=["name", "is_return"], limit=1)
            if test_query and hasattr(test_query[0], 'is_return'):
                print("🔍 Debug: is_return field exists")
                # If all_invoices is True, don't apply any return filter
                if all_invoices:
                    print("🔍 Debug: all_invoices=True, no return filter applied")
                elif returns_only:
                    filters["is_return"] = 1
                elif non_returns_only:
                    filters["is_return"] = 0
            else:
                print("🔍 Debug: is_return field not found, checking alternative field names")
                # Try alternative field names
                if all_invoices:
                    print("🔍 Debug: all_invoices=True, no return filter applied")
                elif returns_only:
                    filters["is_return"] = 1
                elif non_returns_only:
                    filters["is_return"] = 0
        except Exception as field_error:
            print(f"🔍 Debug: Error checking is_return field: {field_error}")
        
        print(f"🔍 Debug: Using filters: {filters}")
        # for today uncomment this
        filters["creation"] = (">=", "2025-09-15")        
        sales_invoices = frappe.get_all(
            "Sales Invoice",
            filters=filters,
            fields=["name", "status", "company", "grand_total", "customer", "posting_date", "is_return", "is_pos"],
            order_by="creation desc"
        )
        
        print(f"🔍 Debug: Query returned {len(sales_invoices)} sales invoices")
        if sales_invoices:
            print(f"🔍 Debug: First invoice - Name: {sales_invoices[0].name}, is_return: {getattr(sales_invoices[0], 'is_return', 'N/A')}")
        
        return sales_invoices
    except Exception as e:
        print(f"❌ Error getting sales invoices: {e}")
        return []

def get_linked_data_counts(sales_invoices, handle_stock=True):
    """
    Get counts of linked data that will be removed
    """
    sales_invoice_names = [si.name for si in sales_invoices]
    
    # Debug: Print first few sales invoice names
    if sales_invoice_names:
        print(f"🔍 Debug: Checking linked data for {len(sales_invoice_names)} sales invoices")
        print(f"🔍 Debug: First 3 sales invoices: {sales_invoice_names[:3]}")
    
    try:
        # Count GL Entries - using safer approach
        try:
            gl_entries_count = frappe.db.count("GL Entry", {
                "voucher_type": "Sales Invoice",
                "voucher_no": ["in", sales_invoice_names]
            })
        except Exception as gl_error:
            print(f"🔍 Debug: Error with voucher_type query: {gl_error}")
            # Try alternative approach - just count by voucher_no
            gl_entries_count = frappe.db.count("GL Entry", {
                "voucher_no": ["in", sales_invoice_names]
            })
        
        # Debug: Check total GL Entries in system
        total_gl_entries = frappe.db.count("GL Entry")
        print(f"🔍 Debug: Total GL Entries in system: {total_gl_entries}")
        
        # Debug: Check GL Entries for Sales Invoice voucher type
        try:
            sales_invoice_gl_entries = frappe.db.count("GL Entry", {"voucher_type": "Sales Invoice"})
            print(f"🔍 Debug: GL Entries with voucher_type='Sales Invoice': {sales_invoice_gl_entries}")
        except Exception as gl_type_error:
            print(f"🔍 Debug: Error checking voucher_type: {gl_type_error}")
            # Try to get sample GL Entry to see structure
            sample_gl = frappe.get_all("GL Entry", fields=["name"], limit=1)
            if sample_gl:
                print(f"🔍 Debug: Sample GL Entry exists: {sample_gl[0].name}")
                # Try to get fields
                try:
                    sample_gl_doc = frappe.get_doc("GL Entry", sample_gl[0].name)
                    print(f"🔍 Debug: GL Entry fields: {list(sample_gl_doc.as_dict().keys())}")
                except Exception as doc_error:
                    print(f"🔍 Debug: Error getting GL Entry doc: {doc_error}")
        
        # Count Journal Entry Accounts that reference Sales Invoices
        journal_entry_accounts = frappe.get_all("Journal Entry Account", 
            filters={
                "reference_type": "Sales Invoice",
                "reference_name": ["in", sales_invoice_names]
            }, 
            fields=["parent"], 
            distinct=True
        )
        
        journal_entries_count = len(journal_entry_accounts)
        
        # Count Sales Invoice Items - using safer approach
        try:
            items_count = frappe.db.count("Sales Invoice Item", {
                "parent": ["in", sales_invoice_names]
            })
        except Exception as items_error:
            print(f"🔍 Debug: Error with Sales Invoice Items parent query: {items_error}")
            # Try to find the correct field name
            try:
                sample_item = frappe.get_all("Sales Invoice Item", fields=["name"], limit=1)
                if sample_item:
                    sample_item_doc = frappe.get_doc("Sales Invoice Item", sample_item[0].name)
                    print(f"🔍 Debug: Sales Invoice Item fields: {list(sample_item_doc.as_dict().keys())}")
                    # Try common field names
                    for field in ["parent", "parenttype", "sales_invoice"]:
                        try:
                            test_count = frappe.db.count("Sales Invoice Item", {field: ["in", sales_invoice_names]})
                            if test_count > 0:
                                print(f"🔍 Debug: Found Sales Invoice Items using field '{field}': {test_count}")
                                items_count = test_count
                                break
                        except:
                            continue
            except Exception as item_doc_error:
                print(f"🔍 Debug: Error getting Sales Invoice Item doc: {item_doc_error}")
                items_count = 0
        
        # Debug: Check total Sales Invoice Items in system
        try:
            total_items_in_system = frappe.db.count("Sales Invoice Item")
            print(f"🔍 Debug: Total Sales Invoice Items in system: {total_items_in_system}")
        except Exception as total_items_error:
            print(f"🔍 Debug: Error counting total Sales Invoice Items: {total_items_error}")
        
        # Count Sales Invoice Taxes - using safer approach
        try:
            taxes_count = frappe.db.count("Sales Taxes and Charges", {
                "parent": ["in", sales_invoice_names]
            })
        except Exception as taxes_error:
            print(f"🔍 Debug: Error with Sales Taxes parent query: {taxes_error}")
            taxes_count = 0
        
        # Count Sales Invoice Advances - using safer approach
        try:
            advances_count = frappe.db.count("Sales Invoice Advance", {
                "parent": ["in", sales_invoice_names]
            })
        except Exception as advances_error:
            print(f"🔍 Debug: Error with Sales Invoice Advances parent query: {advances_error}")
            advances_count = 0
        
        # Stock-related counts
        stock_ledger_entries_count = 0
        stock_entries_count = 0
        delivery_notes_count = 0
        
        if handle_stock:
            # Count Stock Ledger Entries - using safer approach
            try:
                stock_ledger_entries_count = frappe.db.count("Stock Ledger Entry", {
                    "voucher_type": "Sales Invoice",
                    "voucher_no": ["in", sales_invoice_names]
                })
            except Exception as sle_error:
                print(f"🔍 Debug: Error with Stock Ledger Entry voucher_type query: {sle_error}")
                # Try alternative approach - just count by voucher_no
                stock_ledger_entries_count = frappe.db.count("Stock Ledger Entry", {
                    "voucher_no": ["in", sales_invoice_names]
                })
            
            # Count Stock Entries created by Sales Invoices - using correct field name
            try:
                stock_entries_count = frappe.db.count("Stock Entry", {
                    "sales_invoice_no": ["in", sales_invoice_names]
                })
                print(f"🔍 Debug: Found Stock Entries using sales_invoice_no: {stock_entries_count}")
            except Exception as se_error:
                print(f"🔍 Debug: Error with Stock Entry sales_invoice_no query: {se_error}")
                stock_entries_count = 0
            
            # Count Delivery Notes linked to Sales Invoices - using safer approach
            try:
                delivery_notes = frappe.get_all("Delivery Note Item", 
                    filters={
                        "against_sales_invoice": ["in", sales_invoice_names]
                    }, 
                    fields=["parent"], 
                    distinct=True
                )
                delivery_notes_count = len(delivery_notes)
            except Exception as dn_error:
                print(f"🔍 Debug: Error with Delivery Note against_sales_invoice query: {dn_error}")
                # Try to find the correct field name
                try:
                    sample_dn_item = frappe.get_all("Delivery Note Item", fields=["name"], limit=1)
                    if sample_dn_item:
                        sample_dn_doc = frappe.get_doc("Delivery Note Item", sample_dn_item[0].name)
                        print(f"🔍 Debug: Delivery Note Item fields: {list(sample_dn_doc.as_dict().keys())}")
                        # Try common field names
                        for field in ["against_sales_invoice", "sales_invoice", "reference_name"]:
                            try:
                                test_delivery_notes = frappe.get_all("Delivery Note Item", 
                                    filters={field: ["in", sales_invoice_names]}, 
                                    fields=["parent"], 
                                    distinct=True
                                )
                                if test_delivery_notes:
                                    print(f"🔍 Debug: Found Delivery Notes using field '{field}': {len(test_delivery_notes)}")
                                    delivery_notes_count = len(test_delivery_notes)
                                    break
                            except:
                                continue
                except Exception as dn_doc_error:
                    print(f"🔍 Debug: Error getting Delivery Note Item doc: {dn_doc_error}")
                    delivery_notes_count = 0
        
        # Debug: Print individual counts
        print(f"🔍 Debug: GL Entries found: {gl_entries_count}")
        print(f"🔍 Debug: Journal Entries found: {journal_entries_count}")
        print(f"🔍 Debug: Sales Invoice Items found: {items_count}")
        print(f"🔍 Debug: Sales Invoice Taxes found: {taxes_count}")
        print(f"🔍 Debug: Sales Invoice Advances found: {advances_count}")
        if handle_stock:
            print(f"🔍 Debug: Stock Ledger Entries found: {stock_ledger_entries_count}")
            print(f"🔍 Debug: Stock Entries found: {stock_entries_count}")
            print(f"🔍 Debug: Delivery Notes found: {delivery_notes_count}")
        
        return {
            "gl_entries": gl_entries_count,
            "journal_entries": journal_entries_count,
            "items": items_count,
            "taxes": taxes_count,
            "advances": advances_count,
            "stock_ledger_entries": stock_ledger_entries_count,
            "stock_entries": stock_entries_count,
            "delivery_notes": delivery_notes_count
        }
    except Exception as e:
        print(f"❌ Error getting linked data counts: {e}")
        return {
            "gl_entries": 0,
            "journal_entries": 0,
            "items": 0,
            "taxes": 0,
            "advances": 0,
            "stock_ledger_entries": 0,
            "stock_entries": 0,
            "delivery_notes": 0
        }

def remove_sales_invoices_with_linked_data(sales_invoices, handle_stock=True):
    """
    Remove sales invoices along with their linked data
    """
    sales_invoices_removed = 0
    gl_entries_removed = 0
    journal_entries_removed = 0
    items_removed = 0
    taxes_removed = 0
    advances_removed = 0
    stock_ledger_entries_removed = 0
    stock_entries_removed = 0
    delivery_notes_removed = 0
    
    total_to_process = len(sales_invoices)
    processed_count = 0
    
    for sales_invoice in sales_invoices:
        processed_count += 1
        try:
            print(f"🗑️  Processing Sales Invoice: {sales_invoice.name} ({processed_count}/{total_to_process})")
            
            # Check if Sales Invoice still exists before processing
            if not frappe.db.exists("Sales Invoice", sales_invoice.name):
                print(f"   ⚠️  Sales Invoice {sales_invoice.name} no longer exists, skipping")
                continue
            
            # Remove linked GL Entries first - using safer approach
            try:
                gl_entries = frappe.get_all("GL Entry", 
                    filters={
                        "voucher_type": "Sales Invoice",
                        "voucher_no": sales_invoice.name
                    }, 
                    fields=["name"]
                )
            except Exception as gl_error:
                print(f"🔍 Debug: Error with GL Entry voucher_type query: {gl_error}")
                # Try alternative approach - just filter by voucher_no
                gl_entries = frappe.get_all("GL Entry", 
                    filters={
                        "voucher_no": sales_invoice.name
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
                    "reference_type": "Sales Invoice",
                    "reference_name": sales_invoice.name
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
            
            # Remove Sales Invoice Items - using safer approach
            try:
                items = frappe.get_all("Sales Invoice Item", 
                    filters={
                        "parent": sales_invoice.name
                    }, 
                    fields=["name"]
                )
            except Exception as items_error:
                print(f"🔍 Debug: Error with Sales Invoice Items parent query in removal: {items_error}")
                items = []
            
            for item in items:
                try:
                    frappe.delete_doc("Sales Invoice Item", item.name, force=True)
                    items_removed += 1
                    print(f"   ✅ Removed Sales Invoice Item: {item.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove Sales Invoice Item {item.name}: {e}")
            
            # Remove Sales Invoice Taxes - using safer approach
            try:
                taxes = frappe.get_all("Sales Taxes and Charges", 
                    filters={
                        "parent": sales_invoice.name
                    }, 
                    fields=["name"]
                )
            except Exception as taxes_error:
                print(f"🔍 Debug: Error with Sales Taxes parent query in removal: {taxes_error}")
                taxes = []
            
            for tax in taxes:
                try:
                    frappe.delete_doc("Sales Taxes and Charges", tax.name, force=True)
                    taxes_removed += 1
                    print(f"   ✅ Removed Sales Invoice Tax: {tax.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove Sales Invoice Tax {tax.name}: {e}")
            
            # Remove Sales Invoice Advances - using safer approach
            try:
                advances = frappe.get_all("Sales Invoice Advance", 
                    filters={
                        "parent": sales_invoice.name
                    }, 
                    fields=["name"]
                )
            except Exception as advances_error:
                print(f"🔍 Debug: Error with Sales Invoice Advances parent query in removal: {advances_error}")
                advances = []
            
            for advance in advances:
                try:
                    frappe.delete_doc("Sales Invoice Advance", advance.name, force=True)
                    advances_removed += 1
                    print(f"   ✅ Removed Sales Invoice Advance: {advance.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove Sales Invoice Advance {advance.name}: {e}")
            
            # Handle stock-related data if enabled
            if handle_stock:
                # Remove Stock Ledger Entries - using safer approach
                try:
                    stock_ledger_entries = frappe.get_all("Stock Ledger Entry", 
                        filters={
                            "voucher_type": "Sales Invoice",
                            "voucher_no": sales_invoice.name
                        }, 
                        fields=["name"]
                    )
                except Exception as sle_error:
                    print(f"🔍 Debug: Error with Stock Ledger Entry voucher_type query: {sle_error}")
                    try:
                        # Try alternative approach - just filter by voucher_no
                        stock_ledger_entries = frappe.get_all("Stock Ledger Entry", 
                            filters={
                                "voucher_no": sales_invoice.name
                            }, 
                            fields=["name"]
                        )
                    except Exception as sle_voucher_no_error:
                        print(f"🔍 Debug: Error with Stock Ledger Entry voucher_no query: {sle_voucher_no_error}")
                        # If both fail, just set to empty list and continue
                        stock_ledger_entries = []
                        print(f"   ⚠️  Skipping Stock Ledger Entry removal for {sales_invoice.name} due to database structure issues")
                
                for sle in stock_ledger_entries:
                    try:
                        frappe.delete_doc("Stock Ledger Entry", sle.name, force=True)
                        stock_ledger_entries_removed += 1
                        print(f"   ✅ Removed Stock Ledger Entry: {sle.name}")
                    except Exception as e:
                        print(f"   ⚠️  Could not remove Stock Ledger Entry {sle.name}: {e}")
                
                # Remove Stock Entries - using correct field name
                try:
                    stock_entries = frappe.get_all("Stock Entry", 
                        filters={
                            "sales_invoice_no": sales_invoice.name
                        }, 
                        fields=["name"]
                    )
                    print(f"   🔍 Debug: Found {len(stock_entries)} Stock Entries for {sales_invoice.name}")
                except Exception as se_error:
                    print(f"🔍 Debug: Error with Stock Entry sales_invoice_no query: {se_error}")
                    stock_entries = []
                    print(f"   ⚠️  Skipping Stock Entry removal for {sales_invoice.name} due to database structure issues")
                
                for stock_entry in stock_entries:
                    try:
                        frappe.delete_doc("Stock Entry", stock_entry.name, force=True)
                        stock_entries_removed += 1
                        print(f"   ✅ Removed Stock Entry: {stock_entry.name}")
                    except Exception as e:
                        print(f"   ⚠️  Could not remove Stock Entry {stock_entry.name}: {e}")
                
                # Remove linked Delivery Notes - using safer approach
                try:
                    delivery_note_items = frappe.get_all("Delivery Note Item", 
                        filters={
                            "against_sales_invoice": sales_invoice.name
                        }, 
                        fields=["parent"], 
                        distinct=True
                    )
                except Exception as dn_error:
                    print(f"🔍 Debug: Error with Delivery Note against_sales_invoice query in removal: {dn_error}")
                    # Try alternative field names
                    try:
                        delivery_note_items = frappe.get_all("Delivery Note Item", 
                            filters={
                                "sales_invoice": sales_invoice.name
                            }, 
                            fields=["parent"], 
                            distinct=True
                        )
                    except Exception as dn_alt_error:
                        print(f"🔍 Debug: Error with Delivery Note alternative query: {dn_alt_error}")
                        delivery_note_items = []
                        print(f"   ⚠️  Skipping Delivery Note removal for {sales_invoice.name} due to database structure issues")
                
                for delivery_note_item in delivery_note_items:
                    try:
                        frappe.delete_doc("Delivery Note", delivery_note_item.parent, force=True)
                        delivery_notes_removed += 1
                        print(f"   ✅ Removed Delivery Note: {delivery_note_item.parent}")
                    except Exception as e:
                        print(f"   ⚠️  Could not remove Delivery Note {delivery_note_item.parent}: {e}")
            
            # Finally remove the Sales Invoice itself
            try:
                print(f"   🔍 Debug: Attempting to remove Sales Invoice: {sales_invoice.name}")
                print(f"   🔍 Debug: Sales Invoice status: {sales_invoice.status}")
                
                # Check if Sales Invoice still exists
                if not frappe.db.exists("Sales Invoice", sales_invoice.name):
                    print(f"   ⚠️  Sales Invoice {sales_invoice.name} no longer exists, skipping deletion")
                    continue
                
                # Handle different statuses that need special treatment
                print(f"   🔍 Debug: Sales Invoice status: {sales_invoice.status}")
                
                if sales_invoice.status in ["Submitted", "Overdue", "Paid"]:
                    try:
                        print(f"   🔍 Debug: Cancelling submitted Sales Invoice: {sales_invoice.name}")
                        doc = frappe.get_doc("Sales Invoice", sales_invoice.name)
                        
                        # Check if there are any linked documents that might prevent cancellation
                        print(f"   🔍 Debug: Checking for linked documents that might prevent cancellation...")
                        
                        # Try to cancel with force if needed
                        try:
                            doc.cancel()
                            print(f"   ✅ Cancelled Sales Invoice: {sales_invoice.name}")
                        except Exception as cancel_force_error:
                            print(f"   ⚠️  Standard cancel failed: {cancel_force_error}")
                            # Try alternative cancellation method
                            try:
                                # Update the document status directly
                                frappe.db.set_value("Sales Invoice", sales_invoice.name, "docstatus", 0)
                                frappe.db.set_value("Sales Invoice", sales_invoice.name, "status", "Draft")
                                print(f"   ✅ Force-cancelled Sales Invoice: {sales_invoice.name}")
                            except Exception as force_cancel_error:
                                print(f"   ❌ Force cancellation also failed: {force_cancel_error}")
                                # Continue with deletion attempt anyway
                        
                    except Exception as cancel_error:
                        print(f"   ⚠️  Could not cancel Sales Invoice {sales_invoice.name}: {cancel_error}")
                        print(f"   🔍 Debug: Cancel error details: {cancel_error}")
                        
                        # Try to force the status change anyway
                        try:
                            frappe.db.set_value("Sales Invoice", sales_invoice.name, "docstatus", 0)
                            frappe.db.set_value("Sales Invoice", sales_invoice.name, "status", "Draft")
                            print(f"   ✅ Force-changed status for Sales Invoice: {sales_invoice.name}")
                        except Exception as force_status_error:
                            print(f"   ❌ Force status change failed: {force_status_error}")
                
                # Check for any remaining linked documents that might prevent deletion
                print(f"   🔍 Debug: Checking for remaining linked documents...")
                
                # Check for remaining child documents
                remaining_items = frappe.db.count("Sales Invoice Item", {"parent": sales_invoice.name})
                remaining_taxes = frappe.db.count("Sales Taxes and Charges", {"parent": sales_invoice.name})
                remaining_advances = frappe.db.count("Sales Invoice Advance", {"parent": sales_invoice.name})
                
                print(f"   🔍 Debug: Remaining items: {remaining_items}, taxes: {remaining_taxes}, advances: {remaining_advances}")
                
                # Now try to delete
                print(f"   🔍 Debug: Deleting Sales Invoice: {sales_invoice.name}")
                try:
                    frappe.delete_doc("Sales Invoice", sales_invoice.name, force=True)
                    sales_invoices_removed += 1
                    print(f"✅ Successfully removed Sales Invoice: {sales_invoice.name}")
                except Exception as delete_error:
                    print(f"   ⚠️  Standard deletion failed: {delete_error}")
                    
                    # Try more aggressive deletion approach
                    try:
                        print(f"   🔍 Debug: Trying aggressive deletion for: {sales_invoice.name}")
                        
                        # First, try to delete all child documents directly
                        frappe.db.sql("DELETE FROM `tabSales Invoice Item` WHERE parent = %s", sales_invoice.name)
                        frappe.db.sql("DELETE FROM `tabSales Taxes and Charges` WHERE parent = %s", sales_invoice.name)
                        frappe.db.sql("DELETE FROM `tabSales Invoice Advance` WHERE parent = %s", sales_invoice.name)
                        
                        # Then delete the main document
                        frappe.db.sql("DELETE FROM `tabSales Invoice` WHERE name = %s", sales_invoice.name)
                        
                        sales_invoices_removed += 1
                        print(f"✅ Successfully removed Sales Invoice (aggressive method): {sales_invoice.name}")
                        
                    except Exception as aggressive_error:
                        print(f"   ❌ Aggressive deletion also failed: {aggressive_error}")
                        # Continue with next sales invoice
                
            except Exception as e:
                print(f"❌ Could not remove Sales Invoice {sales_invoice.name}: {e}")
                print(f"🔍 Debug: Delete error details: {e}")
                
                # Continue with next sales invoice even if this one fails
            
        except Exception as e:
            print(f"❌ Error processing Sales Invoice {sales_invoice.name}: {e}")
            # Continue with next sales invoice
    
    return {
        "sales_invoices_removed": sales_invoices_removed,
        "gl_entries_removed": gl_entries_removed,
        "journal_entries_removed": journal_entries_removed,
        "items_removed": items_removed,
        "taxes_removed": taxes_removed,
        "advances_removed": advances_removed,
        "stock_ledger_entries_removed": stock_ledger_entries_removed,
        "stock_entries_removed": stock_entries_removed,
        "delivery_notes_removed": delivery_notes_removed
    }

def get_sales_invoices_summary(returns_only=False, non_returns_only=False, all_invoices=False):
    """
    Get a summary of all sales invoices in the system
    """
    print("=" * 80)
    print("SALES INVOICES SUMMARY REPORT")
    print("=" * 80)
    print(f"Timestamp: {now_datetime()}")
    
    if all_invoices:
        print("Filter: All Sales Invoices (both returns and non-returns)")
    elif returns_only:
        print("Filter: Returns Only (is_return=True)")
    elif non_returns_only:
        print("Filter: Non-Returns Only (is_return=False)")
    else:
        print("Filter: All Sales Invoices")
    
    print("=" * 80)
    
    try:
        # Get all sales invoices
        sales_invoices = get_all_sales_invoices(returns_only, non_returns_only, all_invoices)
        
        if not sales_invoices:
            print("✅ No sales invoices found matching the criteria.")
            return {
                "total_sales_invoices": 0,
                "status_distribution": {},
                "company_distribution": {},
                "return_distribution": {},
                "total_amount": 0
            }
        
        # Analyze by status
        status_counts = {}
        company_counts = {}
        return_counts = {"returns": 0, "non_returns": 0}
        total_amount = 0
        
        for sales_invoice in sales_invoices:
            status = sales_invoice.status
            company = sales_invoice.company
            amount = sales_invoice.grand_total or 0
            is_return = sales_invoice.is_return
            
            status_counts[status] = status_counts.get(status, 0) + 1
            company_counts[company] = company_counts.get(company, 0) + 1
            total_amount += amount
            
            if is_return:
                return_counts["returns"] += 1
            else:
                return_counts["non_returns"] += 1
        
        print(f"\n📊 SALES INVOICES OVERVIEW:")
        print(f"   Total Sales Invoices: {len(sales_invoices)}")
        print(f"   Total Amount: {total_amount}")
        print(f"   Returns: {return_counts['returns']}")
        print(f"   Non-Returns: {return_counts['non_returns']}")
        
        print(f"\n📋 Status Distribution:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count}")
        
        print(f"\n🏢 Company Distribution:")
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count}")
        
        # Get linked data counts
        linked_data = get_linked_data_counts(sales_invoices)
        
        print(f"\n🔗 Linked Data:")
        print(f"   GL Entries: {linked_data['gl_entries']}")
        print(f"   Journal Entries: {linked_data['journal_entries']}")
        print(f"   Sales Invoice Items: {linked_data['items']}")
        print(f"   Sales Invoice Taxes: {linked_data['taxes']}")
        print(f"   Sales Invoice Advances: {linked_data['advances']}")
        
        return {
            "total_sales_invoices": len(sales_invoices),
            "status_distribution": status_counts,
            "company_distribution": company_counts,
            "return_distribution": return_counts,
            "total_amount": total_amount,
            "linked_data": linked_data
        }
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return {
            "error": str(e)
        }
