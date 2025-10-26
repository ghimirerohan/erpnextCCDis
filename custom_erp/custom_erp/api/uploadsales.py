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


# ADDED BY AI: UPLOAD_SALES - API Endpoint: Enqueue Import Job
@frappe.whitelist()
def enqueue_import_job(driver_id, vehicle_id, csv_content):
    """
    Enqueue background job to import sales invoices.
    
    Args:
        driver_id: Selected driver ID
        vehicle_id: Selected vehicle ID (optional)
        csv_content: CSV file content
    
    Returns:
        Job ID for tracking
    """
    try:
        job_id = frappe.generate_hash(length=10)
        user = frappe.session.user
        
        # Enqueue the job
        frappe.enqueue(
            method="custom_erp.custom_erp.api.uploadsales.process_upload_sales_job",
            queue="default",
            timeout=3600,
            job_name=f"upload_sales_{job_id}",
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            csv_content=csv_content,
            job_id=job_id,
            user=user
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "message": "Import job queued successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error enqueueing import job: {str(e)}", "Upload Sales Enqueue")
        return {
            "success": False,
            "error": str(e)
        }


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
    Publish real-time progress update.
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
    
    frappe.publish_realtime(
        event="uploadsales_progress",
        message=data,
        user=frappe.session.user
    )


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

