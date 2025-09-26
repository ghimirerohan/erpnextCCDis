#!/usr/bin/env python3
"""
Management command to fix GL entries for Stock Reconciliation documents
"""

import frappe
from frappe import _


def fix_stock_reconciliation_gl_entries():
    """Fix GL entries for all Stock Reconciliation documents"""
    print("=== FIXING GL ENTRIES FOR STOCK RECONCILIATION DOCUMENTS ===")
    
    # Get all submitted Stock Reconciliation documents
    sr_docs = frappe.get_all(
        "Stock Reconciliation",
        filters={"docstatus": 1},
        fields=["name", "company", "expense_account", "cost_center"],
        order_by="creation DESC"
    )
    
    print(f"Found {len(sr_docs)} submitted Stock Reconciliation documents")
    
    if not sr_docs:
        print("No submitted Stock Reconciliation documents found")
        return
    
    # Check which ones are missing GL entries
    docs_without_gl = []
    for sr_doc in sr_docs:
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={
                "voucher_type": "Stock Reconciliation",
                "voucher_no": sr_doc.name
            },
            fields=["name"]
        )
        
        if not gl_entries:
            docs_without_gl.append(sr_doc)
    
    print(f"Found {len(docs_without_gl)} documents without GL entries")
    
    if not docs_without_gl:
        print("✅ All Stock Reconciliation documents already have GL entries!")
        return
    
    # Get warehouse account map for the company
    from erpnext.stock import get_warehouse_account_map
    warehouse_account = get_warehouse_account_map(docs_without_gl[0]["company"])
    
    if not warehouse_account:
        print("❌ No warehouse accounts found. Cannot create GL entries.")
        print("Please ensure warehouses have accounts assigned.")
        return
    
    print(f"Warehouse Account Map: {warehouse_account}")
    
    success_count = 0
    error_count = 0
    
    for sr_doc_info in docs_without_gl:
        try:
            print(f"\n--- Processing: {sr_doc_info.name} ---")
            
            # Get the document
            sr_doc = frappe.get_doc("Stock Reconciliation", sr_doc_info.name)
            
            # Use our enhanced make_gl_entries method which handles everything
            try:
                sr_doc.make_gl_entries(warehouse_account)
                print(f"✅ GL entries created for {sr_doc_info.name}")
                success_count += 1
            except Exception as e:
                print(f"❌ Error creating GL entries for {sr_doc_info.name}: {str(e)}")
                error_count += 1
                continue
            
        except Exception as e:
            print(f"❌ Error processing {sr_doc_info.name}: {str(e)}")
            import traceback
            traceback.print_exc()
            error_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Successfully processed: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Total: {len(docs_without_gl)}")
    
    # Verify final count
    final_gl_count = frappe.db.sql("""
        SELECT COUNT(DISTINCT voucher_no) as count
        FROM `tabGL Entry` 
        WHERE voucher_type = 'Stock Reconciliation'
    """, as_dict=True)[0]
    
    print(f"Total Stock Reconciliation documents with GL entries: {final_gl_count['count']}")


if __name__ == "__main__":
    fix_stock_reconciliation_gl_entries()
