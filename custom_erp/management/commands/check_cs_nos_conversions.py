#!/usr/bin/env python3
"""
Bench command to check and list items that don't have CS to Nos conversion factors.
Usage: bench --site your-site.com execute custom_erp.management.commands.check_cs_nos_conversions.check_cs_nos_conversions
"""

import frappe
from frappe import _
from frappe.utils import cstr
from datetime import datetime
import csv
import os

def check_cs_nos_conversions():
    """
    Check all items and list those that don't have CS to Nos conversion factors.
    """
    print("Checking for items missing CS to Nos conversion factors...")
    print("=" * 60)
    
    # Get all active items
    items = frappe.get_all(
        "Item", 
        fields=["name", "item_code", "item_name"], 
        filters={"disabled": 0}
    )
    
    missing_conversions = []
    total_items = len(items)
    
    print(f"Total items to check: {total_items}")
    
    for i, item in enumerate(items, 1):
        if i % 100 == 0:
            print(f"Processed {i}/{total_items} items...")
        
        # Check if this item has CS to Nos conversion factor
        conversion_factor = frappe.get_value(
            "UOM Conversion Detail", 
            {"parent": item.name, "uom": "CS"}, 
            "conversion_factor"
        )
        
        if conversion_factor is None:
            missing_conversions.append(item)
    
    print(f"\nCompleted checking {total_items} items.")
    print("=" * 60)
    
    if missing_conversions:
        print(f"Found {len(missing_conversions)} items missing CS to Nos conversion factors:")
        print("-" * 60)
        
        for item in missing_conversions:
            print(f"Item Code: {item.item_code}")
            print(f"Item Name: {item.item_name}")
            print(f"Item DocName: {item.name}")
            print("-" * 40)
        
        print(f"\nTotal items missing CS to Nos conversion: {len(missing_conversions)}")
        
        # Export to CSV
        export_to_csv(missing_conversions)
        
        print(f"\nTo fix missing conversions, you need to:")
        print("1. Go to each item's master data")
        print("2. Add UOM Conversion Detail with:")
        print("   - UOM: CS")
        print("   - Conversion Factor: (e.g., 24 if 1 CS = 24 Nos)")
        print("3. Save the item")
        
    else:
        print("✓ All items have CS to Nos conversion factors configured!")
    
    return missing_conversions

def export_to_csv(missing_conversions):
    """
    Export the list of missing conversions to a CSV file.
    """
    # Create exports directory if it doesn't exist
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    filename = os.path.join(exports_dir, f"missing_cs_nos_conversions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Item Code', 'Item Name', 'Item DocName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in missing_conversions:
            writer.writerow({
                'Item Code': item.item_code,
                'Item Name': item.item_name,
                'Item DocName': item.name
            })
    
    print(f"✓ Exported list to: {filename}")

def check_specific_item(item_code):
    """
    Check a specific item for CS to Nos conversion factor.
    """
    print(f"Checking conversion factor for item: {item_code}")
    print("-" * 40)
    
    try:
        # Get item details
        item = frappe.get_doc("Item", item_code)
        print(f"Item Name: {item.item_name}")
        print(f"Item DocName: {item.name}")
        
        # Check conversion factor
        conversion_factor = frappe.get_value(
            "UOM Conversion Detail", 
            {"parent": item.name, "uom": "CS"}, 
            "conversion_factor"
        )
        
        if conversion_factor is not None:
            print(f"✓ CS to Nos conversion factor: {conversion_factor}")
        else:
            print("✗ No CS to Nos conversion factor found!")
            
            # Show existing UOM conversions for this item
            existing_conversions = frappe.get_all(
                "UOM Conversion Detail",
                fields=["uom", "conversion_factor"],
                filters={"parent": item.name}
            )
            
            if existing_conversions:
                print("\nExisting UOM conversions for this item:")
                for conv in existing_conversions:
                    print(f"  - {conv.uom}: {conv.conversion_factor}")
            else:
                print("\nNo UOM conversions configured for this item.")
                
    except frappe.DoesNotExistError:
        print(f"✗ Item '{item_code}' not found!")
    except Exception as e:
        print(f"✗ Error checking item: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        check_specific_item(sys.argv[1])
    else:
        check_cs_nos_conversions()
