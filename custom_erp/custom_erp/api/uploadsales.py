# ADDED BY AI: UPLOAD_SALES
"""
Upload Sales Invoice API Module

This module handles CSV upload, transformation, preview, and bulk import of Sales Invoices.
"""

import frappe
from frappe import _
import csv
import io
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import traceback


# ADDED BY AI: UPLOAD_SALES - Nepali Date Conversion
def nepali_to_gregorian(nepali_date_str: str) -> str:
    """
    Convert Nepali date (YYYY.MM.DD) to Gregorian date (DD/MM/YYYY).
    
    Args:
        nepali_date_str: Nepali date in format "2082.07.09"
    
    Returns:
        Gregorian date in format "26/10/2025"
    """
    try:
        # Parse the Nepali date
        parts = nepali_date_str.strip().replace('"', '').split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid Nepali date format: {nepali_date_str}")
        
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        
        # Use frappe's nepali_date module if available
        # Otherwise use a simplified conversion table for common dates
        # This is a simplified approach - in production you'd use the full nepali date library
        
        # For now, using a basic offset calculation
        # Nepali calendar is roughly 56-57 years ahead
        gregorian_year = year - 56
        
        # Month mapping (approximate - varies by year)
        # This is simplified - real conversion needs day-by-day mapping
        month_offset_days = [0, 30, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        
        # Calculate approximate date
        import calendar
        from datetime import datetime, timedelta
        
        # Base date for conversion (approximate)
        base_gregorian = datetime(gregorian_year, 4, 14)  # Rough start of Nepali year
        
        # Add months and days
        days_to_add = month_offset_days[month - 1] if month <= 12 else 0
        days_to_add += day - 1
        
        gregorian_date = base_gregorian + timedelta(days=days_to_add)
        
        return gregorian_date.strftime("%d/%m/%Y")
        
    except Exception as e:
        frappe.log_error(f"Error converting Nepali date {nepali_date_str}: {str(e)}", "Nepali Date Conversion")
        # Return current date as fallback
        return datetime.now().strftime("%d/%m/%Y")


# ADDED BY AI: UPLOAD_SALES - Customer Lookup
def find_customer(customer_name: str, pan_no: Optional[str] = None) -> Optional[str]:
    """
    Find customer by name and optionally PAN number.
    
    Args:
        customer_name: Customer name from input CSV
        pan_no: PAN number (optional)
    
    Returns:
        Customer.name (ID) or None if not found
    """
    try:
        customer_name = customer_name.strip()
        
        # Try with both name and PAN if PAN is provided
        if pan_no and pan_no.strip():
            pan_no = pan_no.strip()
            customers = frappe.get_all(
                "Customer",
                filters={"customer_name": customer_name, "tax_id": pan_no},
                fields=["name"],
                limit=1
            )
            
            if customers:
                return customers[0].name
        
        # Fallback: search by name only
        customers = frappe.get_all(
            "Customer",
            filters={"customer_name": customer_name},
            fields=["name"],
            limit=1
        )
        
        if customers:
            return customers[0].name
        
        return None
        
    except Exception as e:
        frappe.log_error(f"Error finding customer {customer_name}: {str(e)}", "Customer Lookup")
        return None


# ADDED BY AI: UPLOAD_SALES - Item Lookup
def find_item(item_name: str) -> Optional[str]:
    """
    Find item by name and return item_code.
    
    Args:
        item_name: Item name from input CSV
    
    Returns:
        Item.item_code or None if not found
    """
    try:
        item_name = item_name.strip()
        items = frappe.get_all(
            "Item",
            filters={"item_name": item_name},
            fields=["name", "item_code"],
            limit=1
        )
        
        if items:
            return items[0].item_code
        
        return None
        
    except Exception as e:
        frappe.log_error(f"Error finding item {item_name}: {str(e)}", "Item Lookup")
        return None


# ADDED BY AI: UPLOAD_SALES - Parse CSV rows
def parse_csv_rows(csv_content: str) -> List[Dict[str, str]]:
    """
    Parse CSV content into list of dictionaries.
    
    Args:
        csv_content: CSV file content as string
    
    Returns:
        List of row dictionaries
    """
    rows = []
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)
    
    for row in reader:
        if row.get("InvoiceNo"):  # Skip empty rows
            rows.append(row)
    
    return rows


# ADDED BY AI: UPLOAD_SALES - Group rows by invoice
def group_rows_by_invoice(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """
    Group CSV rows by InvoiceNo.
    
    Returns:
        Dictionary mapping InvoiceNo to list of item rows
    """
    grouped = {}
    for row in rows:
        invoice_no = row.get("InvoiceNo", "").strip()
        if invoice_no:
            if invoice_no not in grouped:
                grouped[invoice_no] = []
            grouped[invoice_no].append(row)
    
    return grouped


# ADDED BY AI: UPLOAD_SALES - Transform invoice data
def transform_invoice_rows(invoice_rows: List[Dict[str, str]], validate_lookups: bool = True) -> Tuple[Dict[str, Any], List[str]]:
    """
    Transform invoice rows from input format to output format.
    
    Args:
        invoice_rows: List of rows for a single invoice
        validate_lookups: Whether to validate customer/item lookups
    
    Returns:
        Tuple of (transformed_data, errors)
    """
    errors = []
    
    if not invoice_rows:
        return {}, ["No rows provided"]
    
    first_row = invoice_rows[0]
    invoice_no = first_row.get("InvoiceNo", "").strip()
    
    # Detect if return
    is_return = "1" if invoice_no.startswith("SRV") else "-"
    
    # Convert date
    nepali_date = first_row.get("Date", "").strip()
    gregorian_date = nepali_to_gregorian(nepali_date)
    
    # Find customer
    customer_name = first_row.get("Name of Customer", "").strip()
    pan_no = first_row.get("PAN No", "").strip()
    
    customer_id = None
    if validate_lookups:
        customer_id = find_customer(customer_name, pan_no)
        if not customer_id:
            error_msg = f"Customer '{customer_name}'"
            if pan_no:
                error_msg += f" with PAN '{pan_no}'"
            error_msg += " not found"
            errors.append(error_msg)
    
    # Process items
    items = []
    for row in invoice_rows:
        item_name = row.get("Name of Product", "").strip()
        qty = row.get("QTY", "0").strip()
        discount = row.get("Discount", "0").strip()
        unit = row.get("Unit", "CS").strip()
        
        item_code = None
        if validate_lookups:
            item_code = find_item(item_name)
            if not item_code:
                errors.append(f"Item '{item_name}' not found")
                continue  # Skip this item
        
        items.append({
            "item_code": item_code or item_name,  # Use name as fallback for preview
            "item_name": item_name,
            "qty": float(qty) if qty else 0,
            "discount": float(discount) if discount else 0,
            "uom": unit
        })
    
    transformed = {
        "invoice_no": invoice_no,
        "is_return": is_return,
        "date": gregorian_date,
        "customer_id": customer_id or customer_name,
        "customer_name": customer_name,
        "items": items,
        "currency": "NPR",
        "update_stock": 1
    }
    
    return transformed, errors


# ADDED BY AI: UPLOAD_SALES - Generate output CSV rows
def generate_output_csv_rows(transformed_invoices: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Generate output CSV rows with proper grouping format.
    
    Returns:
        List of rows for output CSV
    """
    output_rows = []
    
    for invoice in transformed_invoices:
        first_item = True
        
        for item in invoice.get("items", []):
            row = {}
            
            # First row of invoice has all fields
            if first_item:
                row["Is Return (Credit Note)"] = invoice.get("is_return", "-")
                row["Date"] = invoice.get("date", "")
                row["ID"] = invoice.get("invoice_no", "")
                row["Customer"] = invoice.get("customer_id", "")
                row["Currency"] = "NPR"
                row["Update Stock"] = "1"
                row["Exchange Rate"] = "1"
                row["Price List Currency"] = "NPR"
                row["Price List Exchange Rate"] = "1"
                row["Update Outstanding for Self"] = "0"
                row["Update Billed Amount in Sales Order"] = "0"
                row["Update Billed Amount in Delivery Note"] = "1"
                row["Debit To"] = "Debtors - RTAS"
                row["Price List"] = "Standard Selling"
                row["Sales Taxes and Charges Template"] = "Nepal Tax - RTAS"
                row["Account Head (Sales Taxes and Charges)"] = "VAT - RTAS"
                row["Description (Sales Taxes and Charges)"] = "VAT @ 13.0"
                row["Type (Sales Taxes and Charges)"] = "On Net Total"
                row["Tax Rate (Sales Taxes and Charges)"] = "13"
                first_item = False
            else:
                # Subsequent rows have blanks for invoice-level fields
                row["Is Return (Credit Note)"] = ""
                row["Date"] = ""
                row["ID"] = ""
                row["Customer"] = ""
                row["Currency"] = ""
                row["Update Stock"] = ""
                row["Exchange Rate"] = ""
                row["Price List Currency"] = ""
                row["Price List Exchange Rate"] = ""
                row["Update Outstanding for Self"] = ""
                row["Update Billed Amount in Sales Order"] = ""
                row["Update Billed Amount in Delivery Note"] = ""
                row["Debit To"] = ""
                row["Price List"] = ""
                row["Sales Taxes and Charges Template"] = ""
                row["Account Head (Sales Taxes and Charges)"] = ""
                row["Description (Sales Taxes and Charges)"] = ""
                row["Type (Sales Taxes and Charges)"] = ""
                row["Tax Rate (Sales Taxes and Charges)"] = ""
            
            # Item fields always populated
            row["Item (Items)"] = item.get("item_code", "")
            row["Quantity (Items)"] = str(item.get("qty", 0))
            row["Distributed Discount Amount (Items)"] = str(item.get("discount", 0))
            row["Item Name (Items)"] = item.get("item_name", "")
            row["Cost Center (Items)"] = "Main - RTAS"
            row["Income Account (Items)"] = "Sales - RTAS"
            row["UOM (Items)"] = item.get("uom", "CS")
            
            output_rows.append(row)
    
    return output_rows


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Transform and Preview
@frappe.whitelist()
def transform_and_preview(csv_content):
    """
    Transform uploaded CSV and return preview of first 10 VALID invoices.
    Invoices with validation errors are skipped from preview.
    
    Args:
        csv_content: CSV file content as string
    
    Returns:
        Dict with preview_rows, total_invoices, valid_invoice_count, validation_errors
    """
    try:
        # Parse CSV
        rows = parse_csv_rows(csv_content)
        
        # Group by invoice
        grouped = group_rows_by_invoice(rows)
        
        # Transform ALL invoices to validate and collect errors
        valid_invoices = []
        validation_errors = []
        
        for invoice_no, invoice_rows in grouped.items():
            # ADDED BY AI: UPLOAD_SALES - Validate with lookups
            transformed, errors = transform_invoice_rows(invoice_rows, validate_lookups=True)
            
            if errors:
                # Format error message: "Invoice 8283-010755 skipped - Customer: Xyz not found in Customer table"
                error_details = []
                for error in errors:
                    if "Customer" in error and "not found" in error:
                        # Extract customer name from error
                        error_details.append(f"Customer name: {error.split('Customer')[1].split('not')[0].strip()} not found in Customer table")
                    elif "Item" in error and "not found" in error:
                        # Extract item name from error
                        error_details.append(f"Item name: {error.split('Item')[1].split('not')[0].strip()} not found in Item table")
                    else:
                        error_details.append(error)
                
                validation_errors.append(f"Invoice {invoice_no} skipped - {'; '.join(error_details)}")
            else:
                # Only add valid invoices
                if transformed:
                    valid_invoices.append(transformed)
        
        # Generate preview from first 10 valid invoices only
        preview_invoices = valid_invoices[:10]
        preview_rows = generate_output_csv_rows(preview_invoices)
        
        return {
            "success": True,
            "preview_rows": preview_rows[:20],  # Limit to 20 rows for display
            "total_invoices": len(grouped),
            "valid_invoice_count": len(valid_invoices),
            "validation_errors": validation_errors,
            "preview_invoice_count": len(preview_invoices)
        }
        
    except Exception as e:
        frappe.log_error(f"Error in transform_and_preview: {str(e)}\n{traceback.format_exc()}", "Upload Sales Preview")
        return {
            "success": False,
            "error": str(e)
        }


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Get Drivers
@frappe.whitelist()
def get_drivers():
    """
    Get list of drivers for dropdown selection.
    
    Returns:
        List of drivers with name and employee_name
    """
    try:
        # Try to get Driver doctype
        if frappe.db.exists("DocType", "Driver"):
            drivers = frappe.get_all(
                "Driver",
                fields=["name", "full_name as employee_name"],
                filters={"status": "Active"},
                order_by="full_name"
            )
        else:
            # Fallback to Employee
            drivers = frappe.get_all(
                "Employee",
                fields=["name", "employee_name"],
                filters={"status": "Active"},
                order_by="employee_name"
            )
        
        return {
            "success": True,
            "drivers": drivers
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_drivers: {str(e)}", "Upload Sales Get Drivers")
        return {
            "success": False,
            "error": str(e),
            "drivers": []
        }


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Get Vehicles
@frappe.whitelist()
def get_vehicles():
    """
    Get list of vehicles for dropdown selection.
    
    Returns:
        List of vehicles with name and license_plate
    """
    try:
        # Get Vehicle doctype
        if frappe.db.exists("DocType", "Vehicle"):
            vehicles = frappe.get_all(
                "Vehicle",
                fields=["name", "license_plate"],
                order_by="name"
            )
        else:
            vehicles = []
        
        return {
            "success": True,
            "vehicles": vehicles
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_vehicles: {str(e)}", "Upload Sales Get Vehicles")
        return {
            "success": False,
            "error": str(e),
            "vehicles": []
        }


# ADDED BY AI: UPLOAD_SALES - Test API Endpoint
@frappe.whitelist()
def test_api():
    """Simple test API to verify the endpoint is working."""
    print("=== TEST API CALLED ===")
    frappe.log_error("=== TEST API CALLED ===", "Upload Sales Test")
    return {
        "success": True,
        "message": "Test API is working",
        "timestamp": frappe.utils.now()
    }


# ADDED BY AI: UPLOAD_SALES - NEW Test API to verify code changes are loaded
@frappe.whitelist()
def test_api_v2():
    """Brand new test API to verify code is being updated."""
    print("=== TEST API V2 CALLED - NEW CODE IS RUNNING ===")
    return {
        "success": True,
        "message": "NEW CODE IS LOADED",
        "version": "v2",
        "timestamp": frappe.utils.now()
    }

# ADDED BY AI: UPLOAD_SALES - Debug API to check Data Import status
@frappe.whitelist()
def debug_import_status(job_id):
    """Debug API to check what's happening with Data Import status."""
    try:
        print(f"=== DEBUG IMPORT STATUS FOR: {job_id} ===")
        
        if not frappe.db.exists("Data Import", job_id):
            return {
                "success": False,
                "error": "Data Import not found",
                "job_id": job_id
            }
        
        data_import = frappe.get_doc("Data Import", job_id)
        
        # Get logs
        logs = frappe.get_all(
            "Data Import Log",
            filters={"data_import": job_id},
            fields=["success", "message"],
            order_by="log_index"
        )
        
        success = len([l for l in logs if l.success])
        failed = len([l for l in logs if not l.success])
        processed = len(logs)
        
        print(f"Data Import Status: {data_import.status}")
        print(f"Payload Count: {data_import.payload_count}")
        print(f"Logs Count: {len(logs)}")
        print(f"Success Count: {success}")
        print(f"Failed Count: {failed}")
        
        return {
            "success": True,
            "data": {
                "status": data_import.status,
                "payload_count": data_import.payload_count,
                "logs_count": len(logs),
                "success_count": success,
                "failed_count": failed,
                "processed": processed,
                "completed": data_import.status in ["Success", "Partial Success", "Error"]
            }
        }
        
    except Exception as e:
        print(f"Error in debug_import_status: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Enqueue Import Job (Using Frappe Data Import)
@frappe.whitelist()
def enqueue_import_job(driver_id, vehicle_id, csv_content):
    """
    Create and start a Data Import using Frappe's built-in import system.
    
    Args:
        driver_id: Selected driver ID
        vehicle_id: Selected vehicle ID (optional)
        csv_content: CSV file content
    
    Returns:
        Import name for tracking
    """
    try:
        print("=== UPLOAD SALES IMPORT STARTED ===")
        frappe.log_error(f"=== UPLOAD SALES IMPORT STARTED ===", "Upload Sales Import")
        frappe.log_error(f"Driver ID: {driver_id}, Vehicle ID: {vehicle_id}", "Upload Sales Import")
        frappe.log_error(f"CSV Content Length: {len(csv_content) if csv_content else 0}", "Upload Sales Import")
        
        # Write to file for debugging
        with open("/tmp/uploadsales_debug.log", "a") as f:
            f.write(f"[{frappe.utils.now()}] UPLOAD SALES IMPORT STARTED\n")
            f.write(f"[{frappe.utils.now()}] Driver ID: {driver_id}, Vehicle ID: {vehicle_id}\n")
            f.write(f"[{frappe.utils.now()}] CSV Content Length: {len(csv_content) if csv_content else 0}\n")
            f.flush()
        
        # Parse and transform CSV to Frappe import format
        rows = parse_csv_rows(csv_content)
        grouped = group_rows_by_invoice(rows)
        
        frappe.log_error(f"Parsed {len(rows)} rows into {len(grouped)} invoices", "Upload Sales Import")
        
        # Transform to import-ready format
        import_data = []
        error_count = 0
        
        for invoice_no, invoice_rows in grouped.items():
            transformed, errors = transform_invoice_rows(invoice_rows, validate_lookups=True)
            
            if errors:
                error_count += 1
                continue
            
            # Convert to flat format for import - EXACTLY matching output sheet format
            for i, item in enumerate(transformed.get("items", [])):
                # First row has all header data, subsequent rows have blank cells for header data
                if i == 0:
                    # First item row - include all header data
                    import_row = {
                        "Is Return": "1" if transformed.get("is_return") == "1" else "-",  # "1" for SRV**, "-" for normal
                        "Date": transformed.get("date"),
                        "ID": invoice_no,
                        "Customer": transformed.get("customer_id"),
                        "Item Code": item.get("item_code"),
                        "Quantity": item.get("qty"),
                        "Discount Amount": item.get("discount") or 0,
                        "Item Name": item.get("item_name"),
                        "Currency": "NPR",
                        "Update Stock": "1",
                        "Exchange Rate": "1",
                        "Price List Currency": "NPR",
                        "Price List Exchange Rate": "1",
                        "Update Outstanding for Self": "0",
                        "Update Billed Amount in Sales Order": "0",
                        "Update Billed Amount in Delivery Note": "1",
                        "Debit To": "Debtors - RTAS",
                        "Price List": "Standard Selling",
                        "Sales Taxes and Charges Template": "Nepal Tax - RTAS",
                        "Account Head (Sales Taxes and Charges)": "VAT - RTAS",
                        "Description (Sales Taxes and Charges)": "VAT @ 13.0",
                        "Type (Sales Taxes and Charges)": "On Net Total",
                        "Tax Rate (Sales Taxes and Charges)": "13",
                        "Cost Center (Items)": "Main - RTAS",
                        "Income Account (Items)": "Sales - RTAS",
                        "UOM (Items)": "CS",
                        "Driver For Vehicle": driver_id,  # Custom field
                        "Vehicle For Delivery": vehicle_id or ""  # Custom field
                    }
                else:
                    # Subsequent item rows - ALL parent table fields are blank, only item fields have values
                    import_row = {
                        "Is Return": "",  # Blank
                        "Date": "",       # Blank
                        "ID": "",         # Blank
                        "Customer": "",   # Blank
                        "Item Code": item.get("item_code"),
                        "Quantity": item.get("qty"),
                        "Discount Amount": item.get("discount") or 0,
                        "Item Name": item.get("item_name"),
                        "Currency": "",   # Blank - parent field
                        "Update Stock": "", # Blank - parent field
                        "Exchange Rate": "", # Blank - parent field
                        "Price List Currency": "", # Blank - parent field
                        "Price List Exchange Rate": "", # Blank - parent field
                        "Update Outstanding for Self": "", # Blank - parent field
                        "Update Billed Amount in Sales Order": "", # Blank - parent field
                        "Update Billed Amount in Delivery Note": "", # Blank - parent field
                        "Debit To": "",   # Blank - parent field
                        "Price List": "", # Blank - parent field
                        "Sales Taxes and Charges Template": "", # Blank - parent field
                        "Account Head (Sales Taxes and Charges)": "", # Blank - parent field
                        "Description (Sales Taxes and Charges)": "", # Blank - parent field
                        "Type (Sales Taxes and Charges)": "", # Blank - parent field
                        "Tax Rate (Sales Taxes and Charges)": "", # Blank - parent field
                        "Cost Center (Items)": "Main - RTAS",  # Keep static values - item field
                        "Income Account (Items)": "Sales - RTAS",  # Keep static values - item field
                        "UOM (Items)": "CS",  # Keep static values - item field
                        "Driver For Vehicle": "",  # Blank - custom field
                        "Vehicle For Delivery": ""  # Blank - custom field
                    }
                    
                import_data.append(import_row)
        
        if not import_data:
            return {
                "success": False,
                "error": "No valid data to import"
            }
        
        # Create CSV content for Data Import
        import_csv = create_import_csv(import_data)
        
        # Create Data Import document
        data_import = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": "Sales Invoice",
            "import_type": "Insert New Records",
            "submit_after_import": 0,
            "mute_emails": 1
        })
        data_import.insert(ignore_permissions=True)
        
        # Save the import file
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"sales_import_{data_import.name}.csv",
            "content": import_csv,
            "is_private": 1,
            "attached_to_doctype": "Data Import",
            "attached_to_name": data_import.name
        })
        file_doc.save(ignore_permissions=True)
        
        # Start the import
        data_import.import_file = file_doc.file_url
        data_import.save(ignore_permissions=True)
        
        # Enqueue the import in background
        frappe.enqueue(
            method="custom_erp.custom_erp.api.uploadsales.run_data_import",
            queue="default",
            timeout=3600,
            data_import_name=data_import.name
        )
        
        frappe.log_error(f"=== UPLOAD SALES IMPORT COMPLETED ===", "Upload Sales Import")
        frappe.log_error(f"Data Import created: {data_import.name}", "Upload Sales Import")
        frappe.log_error(f"Background job enqueued successfully", "Upload Sales Import")
        
        return {
            "success": True,
            "import_name": data_import.name,
            "message": "Import started successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error starting import: {str(e)}\n{traceback.format_exc()}", "Upload Sales Import")
        return {
            "success": False,
            "error": str(e)
        }


# ADDED BY AI: UPLOAD_SALES - Run Data Import in Background
def run_data_import(data_import_name):
    """
    Run the Data Import in background.
    """
    try:
        frappe.log_error(f"Starting data import: {data_import_name}", "Upload Sales Data Import")
        
        # Get the Data Import document
        data_import = frappe.get_doc("Data Import", data_import_name)
        frappe.log_error(f"Data Import found: {data_import.name}, Status: {data_import.status}", "Upload Sales Data Import")
        
        # Use the Importer class to run the import
        from frappe.core.doctype.data_import.importer import Importer
        importer = Importer(data_import.reference_doctype, data_import=data_import)
        frappe.log_error(f"Importer created, starting import_data()", "Upload Sales Data Import")
        
        importer.import_data()
        frappe.log_error(f"Import completed successfully", "Upload Sales Data Import")
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Error running data import: {str(e)}\n{traceback.format_exc()}", "Upload Sales Data Import")
        # Update status to Error
        try:
            data_import = frappe.get_doc("Data Import", data_import_name)
            data_import.status = "Error"
            data_import.save(ignore_permissions=True)
            frappe.db.commit()
        except:
            pass


# ADDED BY AI: UPLOAD_SALES - Background Job: Process Upload
def process_upload_sales_job(driver_id, vehicle_id, csv_content, job_id, user):
    """
    Background job to process sales invoice upload.
    
    This runs in a background worker and publishes real-time progress.
    """
    frappe.set_user(user)
    
    # Initialize counters
    processed = 0
    imported = 0
    skipped = 0
    errors = 0
    total_amount = 0.0
    error_rows = []
    
    try:
        # Parse CSV
        rows = parse_csv_rows(csv_content)
        grouped = group_rows_by_invoice(rows)
        total = len(grouped)
        
        # Publish initial progress
        publish_progress(job_id, processed, total, "Starting import...", imported, skipped, errors, total_amount)
        
        # Process each invoice
        for invoice_no, invoice_rows in grouped.items():
            try:
                processed += 1
                
                # Check if already exists
                if frappe.db.exists("Sales Invoice", invoice_no):
                    skipped += 1
                    publish_progress(job_id, processed, total, f"Skipped existing: {invoice_no}", imported, skipped, errors, total_amount)
                    continue
                
                # Transform invoice
                transformed, transform_errors = transform_invoice_rows(invoice_rows, validate_lookups=True)
                
                if transform_errors:
                    errors += 1
                    for row in invoice_rows:
                        error_row = dict(row)
                        error_row["Error Message"] = "; ".join(transform_errors)
                        error_rows.append(error_row)
                    publish_progress(job_id, processed, total, f"Validation errors: {invoice_no}", imported, skipped, errors, total_amount)
                    continue
                
                # Create Sales Invoice - ADDED BY AI: UPLOAD_SALES - Now includes vehicle_id
                result = create_sales_invoice_doc(transformed, driver_id, vehicle_id)
                
                if result.get("success"):
                    imported += 1
                    total_amount += result.get("grand_total", 0)
                    publish_progress(job_id, processed, total, f"Imported: {invoice_no}", imported, skipped, errors, total_amount)
                else:
                    errors += 1
                    for row in invoice_rows:
                        error_row = dict(row)
                        error_row["Error Message"] = result.get("error", "Unknown error")
                        error_rows.append(error_row)
                    publish_progress(job_id, processed, total, f"Error importing: {invoice_no}", imported, skipped, errors, total_amount)
                
            except Exception as e:
                errors += 1
                error_msg = str(e)
                frappe.log_error(f"Error processing invoice {invoice_no}: {error_msg}\n{traceback.format_exc()}", "Upload Sales Processing")
                for row in invoice_rows:
                    error_row = dict(row)
                    error_row["Error Message"] = error_msg
                    error_rows.append(error_row)
                publish_progress(job_id, processed, total, f"Exception: {invoice_no}", imported, skipped, errors, total_amount)
        
        # Save error CSV if there are errors
        error_csv_path = None
        if error_rows:
            error_csv_path = save_error_csv(error_rows, job_id)
        
        # Final progress
        publish_progress(
            job_id, processed, total, "Import completed",
            imported, skipped, errors, total_amount,
            completed=True, error_csv_path=error_csv_path
        )
        
        frappe.db.commit()
        
    except Exception as e:
        error_msg = f"Fatal error in import job: {str(e)}"
        frappe.log_error(f"{error_msg}\n{traceback.format_exc()}", "Upload Sales Job Error")
        publish_progress(job_id, processed, total, error_msg, imported, skipped, errors, total_amount, completed=True, error=error_msg)


# ADDED BY AI: UPLOAD_SALES - Create Sales Invoice Document
def create_sales_invoice_doc(transformed_data: Dict[str, Any], driver_id: str, vehicle_id: str = None) -> Dict[str, Any]:
    """
    Create Sales Invoice document in ERPNext.
    
    Args:
        transformed_data: Transformed invoice data
        driver_id: Driver ID to assign
        vehicle_id: Vehicle ID to assign (optional)
    
    Returns:
        Dict with success status and grand_total or error
    """
    try:
        invoice_no = transformed_data.get("invoice_no")
        
        # Build invoice doc - ADDED BY AI: UPLOAD_SALES - Now includes vehicle
        doc_data = {
            "doctype": "Sales Invoice",
            "naming_series": "SI-",
            "customer": transformed_data.get("customer_id"),
            "posting_date": transformed_data.get("date"),
            "update_stock": 1,
            "driver": driver_id,
            "is_return": 1 if transformed_data.get("is_return") == "1" else 0,
            "items": []
        }
        
        # Add vehicle if provided
        if vehicle_id:
            doc_data["vehicle_for_delivery"] = vehicle_id
        
        doc = frappe.get_doc(doc_data)
        
        # Add items
        for item in transformed_data.get("items", []):
            doc.append("items", {
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "qty": item.get("qty"),
                "uom": item.get("uom"),
                "rate": 0,  # Will be set by system from item master
                "distributed_discount_amount": item.get("discount")
            })
        
        # Insert (do not submit)
        doc.insert(ignore_permissions=True)
        
        # Rename to match invoice_no if different
        if doc.name != invoice_no:
            frappe.rename_doc("Sales Invoice", doc.name, invoice_no, force=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "name": invoice_no,
            "grand_total": doc.grand_total
        }
        
    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e)
        frappe.log_error(f"Error creating sales invoice: {error_msg}\n{traceback.format_exc()}", "Upload Sales Create Invoice")
        return {
            "success": False,
            "error": error_msg
        }


# ADDED BY AI: UPLOAD_SALES - Publish Progress
def publish_progress(job_id, processed, total, message, imported, skipped, errors, total_amount, completed=False, error=None, error_csv_path=None):
    """
    Publish real-time progress update via WebSocket AND cache for polling.
    """
    data = {
        "job_id": job_id,
        "processed": processed,
        "total": total,
        "current_message": message,
        "imported_count": imported,
        "skipped_count": skipped,
        "error_count": errors,
        "total_amount": total_amount,
        "completed": completed,
        "error": error,
        "error_csv_path": error_csv_path
    }
    
    # Store in cache for polling (expires in 1 hour)
    cache_key = f"uploadsales_progress_{job_id}"
    frappe.cache().set_value(cache_key, data, expires_in_sec=3600)
    
    # Also publish via WebSocket for realtime updates
    try:
        frappe.publish_realtime(
            event="uploadsales_progress",
            message=data,
            user=frappe.session.user
        )
    except Exception as e:
        # WebSocket might not be available, but cache is still working
        frappe.log_error(f"Error publishing realtime: {str(e)}", "Upload Sales Realtime")


# ADDED BY AI: UPLOAD_SALES - Save Error CSV
def save_error_csv(error_rows: List[Dict], job_id: str) -> str:
    """
    Save error rows to CSV file.
    
    Returns:
        File path
    """
    try:
        # Generate CSV content
        if not error_rows:
            return None
        
        output = io.StringIO()
        fieldnames = list(error_rows[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(error_rows)
        
        csv_content = output.getvalue()
        
        # Save as file
        filename = f"upload_sales_errors_{job_id}.csv"
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "content": csv_content,
            "is_private": 1
        })
        file_doc.save(ignore_permissions=True)
        
        return file_doc.file_url
        
    except Exception as e:
        frappe.log_error(f"Error saving error CSV: {str(e)}", "Upload Sales Error CSV")
        return None


# ADDED BY AI: UPLOAD_SALES - Create Import CSV
def create_import_csv(import_data):
    """Create CSV content for Data Import matching the exact output format."""
    if not import_data:
        return ""
    
    import io
    import csv
    
    output = io.StringIO()
    
    # Define the EXACT column headers as they appear in the output sheet + custom fields
    headers = [
        "Is Return (Credit Note)", "Date", "ID", "Customer", "Item (Items)", 
        "Quantity (Items)", "Distributed Discount Amount (Items)", "Item Name (Items)", 
        "Currency", "Update Stock", "Exchange Rate", "Price List Currency", 
        "Price List Exchange Rate", "Update Outstanding for Self", 
        "Update Billed Amount in Sales Order", "Update Billed Amount in Delivery Note", 
        "Debit To", "Price List", "Sales Taxes and Charges Template", 
        "Account Head (Sales Taxes and Charges)", "Description (Sales Taxes and Charges)", 
        "Type (Sales Taxes and Charges)", "Tax Rate (Sales Taxes and Charges)", 
        "Cost Center (Items)", "Income Account (Items)", "UOM (Items)",
        "Driver For Vehicle", "Vehicle For Delivery"  # Custom fields
    ]
    
    writer = csv.writer(output)
    writer.writerow(headers)
    
    for row in import_data:
        # Convert to the exact format matching the output sheet + custom fields
        writer.writerow([
            row.get("Is Return", ""),  # Will be "-" or "1" based on SRV pattern
            row.get("Date", ""),
            row.get("ID", ""),
            row.get("Customer", ""),
            row.get("Item Code", ""),
            row.get("Quantity", ""),
            row.get("Discount Amount", ""),
            row.get("Item Name", ""),
            row.get("Currency", "NPR"),  # Static value or blank
            row.get("Update Stock", "1"),    # Static value or blank
            row.get("Exchange Rate", "1"),    # Static value or blank
            row.get("Price List Currency", "NPR"),  # Static value or blank
            row.get("Price List Exchange Rate", "1"),    # Static value or blank
            row.get("Update Outstanding for Self", "0"),    # Static value or blank
            row.get("Update Billed Amount in Sales Order", "0"),    # Static value or blank
            row.get("Update Billed Amount in Delivery Note", "1"),    # Static value or blank
            row.get("Debit To", "Debtors - RTAS"),  # Static value or blank
            row.get("Price List", "Standard Selling"),  # Static value or blank
            row.get("Sales Taxes and Charges Template", "Nepal Tax - RTAS"),  # Static value or blank
            row.get("Account Head (Sales Taxes and Charges)", "VAT - RTAS"),  # Static value or blank
            row.get("Description (Sales Taxes and Charges)", "VAT @ 13.0"),  # Static value or blank
            row.get("Type (Sales Taxes and Charges)", "On Net Total"),  # Static value or blank
            row.get("Tax Rate (Sales Taxes and Charges)", "13"),   # Static value or blank
            row.get("Cost Center (Items)", "Main - RTAS"),  # Static value
            row.get("Income Account (Items)", "Sales - RTAS"),  # Static value
            row.get("UOM (Items)", "CS"),    # Static value
            row.get("Driver For Vehicle", ""),  # Custom field
            row.get("Vehicle For Delivery", "")  # Custom field
        ])
    
    return output.getvalue()


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Get Import Progress (for polling)
@frappe.whitelist()
def get_job_progress(job_id):
    """
    Get current progress of a Data Import.
    
    Args:
        job_id: Data Import name
    
    Returns:
        Dict with current progress data
    """
    try:
        # Get the Data Import document
        if not frappe.db.exists("Data Import", job_id):
            return {
                "success": True,
                "data": {
                    "processed": 0,
                    "total": 0,
                    "current_message": "Import not found",
                    "imported_count": 0,
                    "skipped_count": 0,
                    "error_count": 0,
                    "total_amount": 0,
                    "completed": True
                }
            }
        
        data_import = frappe.get_doc("Data Import", job_id)
        
        # Get total from payload_count
        total = data_import.payload_count or 0
        
        # Get logs to calculate success/failure and error details
        logs = frappe.get_all(
            "Data Import Log",
            filters={"data_import": job_id},
            fields=["success", "message"],
            order_by="log_index"
        )
        
        success = len([l for l in logs if l.success])
        failed = len([l for l in logs if not l.success])
        processed = len(logs)
        
        # Get error details for frontend display
        error_details = []
        for i, log in enumerate(logs):
            if not log.success and log.message:
                error_details.append(f"Row {i+1}: {log.message}")
        
        # Determine status message
        if data_import.status == "Success":
            message = "Import completed successfully"
            completed = True
        elif data_import.status == "Partial Success":
            message = f"Import completed with {failed} errors"
            completed = True
        elif data_import.status == "Error":
            message = "Import failed"
            completed = True
        elif data_import.status == "In Progress":
            message = f"Importing... {processed}/{total}"
            completed = False
        else:
            message = data_import.status or "Pending"
            completed = False
        
        return {
            "success": True,
            "data": {
                "processed": processed,
                "total": total,
                "current_message": message,
                "imported_count": success,
                "skipped_count": 0,
                "error_count": failed,
                "total_amount": 0,
                "completed": completed,
                "import_log_url": f"/app/data-import/{job_id}" if completed else None,
                "error_details": error_details
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting import progress: {str(e)}", "Upload Sales Get Progress")
        return {
            "success": False,
            "error": str(e)
        }


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Download Error CSV
@frappe.whitelist()
def download_error_csv(job_id):
    """
    Get error CSV file path for download.
    
    Args:
        job_id: Job ID
    
    Returns:
        File path or error
    """
    try:
        filename = f"upload_sales_errors_{job_id}.csv"
        files = frappe.get_all(
            "File",
            filters={"file_name": filename},
            fields=["file_url"],
            limit=1
        )
        
        if files:
            return {
                "success": True,
                "file_url": files[0].file_url
            }
        else:
            return {
                "success": False,
                "error": "Error file not found"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

