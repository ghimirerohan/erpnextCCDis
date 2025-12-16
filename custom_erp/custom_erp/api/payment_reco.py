# ADDED BY AI: DAILY_PAYMENT_RECO
"""
Daily Payment Reconciliation API Module

This module handles CSV upload, driver assignment, and payment entry for daily sales reconciliation.
"""

import frappe
from frappe import _
import csv
import io
import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import traceback


@frappe.whitelist()
def parse_and_validate_csv(csv_content: str) -> Dict[str, Any]:
    """
    Parse CSV file and validate that customers exist in the system.
    
    Args:
        csv_content: CSV file content as string
    
    Returns:
        {
            "success": bool,
            "data": {
                "parsed_rows": List of parsed CSV rows,
                "grouped_by_loadsheet": Dict of loadsheet -> rows,
                "unmatched_customers": List of outlet codes not found
            },
            "message": str
        }
    """
    try:
        # Parse CSV
        csv_file = io.StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        
        parsed_rows = []
        unmatched_customers = []
        grouped = {}
        
        for row in csv_reader:
            outlet_code = row.get("Outlet Code", "").strip().strip('"')
            outlet_name = row.get("Outlet Name", "").strip().strip('"')
            reference_no = row.get("Reference No", "").strip().strip('"')
            amount = float(row.get("Amount", "0").strip().strip('"').replace(',', ''))
            salesman_name = row.get("Salesman Name", "").strip().strip('"')
            
            # Validate customer exists
            customer_exists = frappe.db.exists("Customer", outlet_code)
            
            parsed_row = {
                "outlet_code": outlet_code,
                "outlet_name": outlet_name,
                "reference_no": reference_no,
                "amount": amount,
                "salesman_name": salesman_name,
                "customer_exists": bool(customer_exists)
            }
            
            parsed_rows.append(parsed_row)
            
            if not customer_exists:
                unmatched_customers.append({
                    "outlet_code": outlet_code,
                    "outlet_name": outlet_name
                })
            
            # Group by load sheet (reference_no)
            if reference_no not in grouped:
                grouped[reference_no] = []
            grouped[reference_no].append(parsed_row)
        
        return {
            "success": True,
            "data": {
                "parsed_rows": parsed_rows,
                "grouped_by_loadsheet": grouped,
                "unmatched_customers": unmatched_customers
            },
            "message": f"Parsed {len(parsed_rows)} rows, {len(grouped)} load sheets"
        }
        
    except Exception as e:
        frappe.log_error(f"Error parsing CSV: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error parsing CSV: {str(e)}"
        }


@frappe.whitelist()
def get_territories_list() -> Dict[str, Any]:
    """
    Get list of all territories for dropdown selection.
    
    Returns:
        {
            "success": bool,
            "data": List of {"name": territory_name},
            "message": str
        }
    """
    try:
        territories = frappe.get_all(
            "Territory",
            fields=["name"],
            filters={"is_group": 0},
            order_by="name"
        )
        
        return {
            "success": True,
            "data": territories,
            "message": f"Retrieved {len(territories)} territories"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting territories: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error getting territories: {str(e)}"
        }


@frappe.whitelist()
def create_customer_from_csv(
    outlet_code: str,
    outlet_name: str,
    territory: str,
    tax_id: str,
    phone_number: str
) -> Dict[str, Any]:
    """
    Create a new Customer from CSV unmatched data.
    
    Args:
        outlet_code: Customer ID (will be used as name)
        outlet_name: Customer name
        territory: Territory name
        tax_id: Tax ID / PAN number
        phone_number: Mobile/Phone number (must be 10 digits)
    
    Returns:
        {
            "success": bool,
            "data": {"name": customer_id, "customer_name": customer_name},
            "message": str
        }
    """
    try:
        # Validate required fields
        if not outlet_code:
            raise ValueError("Outlet Code is required")
        if not outlet_name:
            raise ValueError("Outlet Name is required")
        if not territory:
            raise ValueError("Territory is required")
        if not tax_id:
            raise ValueError("Tax ID is required")
        if not phone_number:
            raise ValueError("Phone Number is required")
        
        # Validate phone number - must be exactly 10 digits
        phone_clean = ''.join(filter(str.isdigit, phone_number))
        if len(phone_clean) != 10:
            raise ValueError("Phone Number must be exactly 10 digits")
        
        # Check if customer already exists
        if frappe.db.exists("Customer", outlet_code):
            return {
                "success": False,
                "data": None,
                "message": f"Customer with code '{outlet_code}' already exists"
            }
        
        # Create the customer document
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": outlet_name,
            "customer_type": "Company",
            "territory": territory,
            "tax_id": tax_id,
            "mobile_no": phone_clean,
            "customer_group": "Commercial"  # Default customer group
        })
        
        # Bypass permission checks since this is a whitelisted API method
        frappe.flags.ignore_permissions = True
        try:
            # Use set_name parameter to force the customer name/ID to be outlet_code
            customer_doc.insert(ignore_permissions=True, set_name=outlet_code)
        finally:
            frappe.flags.ignore_permissions = False
        
        frappe.db.commit()
        
        # Verify the customer was created with correct name
        if customer_doc.name != outlet_code:
            # If Frappe changed the name, we need to rename it
            frappe.rename_doc("Customer", customer_doc.name, outlet_code, force=True)
            frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                "name": outlet_code,
                "customer_name": outlet_name
            },
            "message": f"Customer '{outlet_name}' created successfully with ID: {outlet_code}"
        }
        
    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e) if str(e) else repr(e)
        error_traceback = traceback.format_exc()
        frappe.log_error(f"Error creating customer: {error_msg}\n{error_traceback}", "Payment Reco API Error")
        return {
            "success": False,
            "data": None,
            "message": f"Error creating customer: {error_msg}" if error_msg else "Error creating customer: Unknown error occurred"
        }


@frappe.whitelist()
def get_drivers_list() -> Dict[str, Any]:
    """
    Get list of all drivers for dropdown selection.
    
    Returns:
        {
            "success": bool,
            "data": List of {"name": driver_id, "driver_name": driver_full_name},
            "message": str
        }
    """
    try:
        # Get drivers from HRMS Driver doctype
        drivers = frappe.get_all(
            "Driver",
            fields=["name", "full_name"],
            filters={"status": "Active"},
            order_by="full_name"
        )
        
        # Rename full_name to driver_name for frontend compatibility
        formatted_drivers = []
        for driver in drivers:
            formatted_drivers.append({
                "name": driver.name,
                "driver_name": driver.full_name or driver.name
            })
        
        return {
            "success": True,
            "data": formatted_drivers,
            "message": f"Retrieved {len(formatted_drivers)} drivers"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting drivers: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error getting drivers: {str(e)}"
        }


@frappe.whitelist()
def create_payment_recos(driver_assignments: str, csv_data: str) -> Dict[str, Any]:
    """
    Create Daily Sales Payment Reco records based on driver assignments.
    
    Args:
        driver_assignments: JSON string of {driver_name: [loadsheet_numbers]}
        csv_data: JSON string of grouped CSV data
    
    Returns:
        {
            "success": bool,
            "data": {"created_recos": [list of created document names]},
            "message": str
        }
    """
    try:
        assignments = json.loads(driver_assignments)
        grouped_data = json.loads(csv_data)
        
        created_recos = []
        
        for driver_name, loadsheets in assignments.items():
            # Get driver document (HRMS Driver uses full_name field)
            driver = frappe.db.get_value("Driver", {"full_name": driver_name}, "name")
            if not driver:
                frappe.throw(_(f"Driver not found: {driver_name}"))
            
            # Aggregate data for this driver's load sheets
            customer_amounts = {}  # {customer: total_amount}
            total_amount = 0
            
            for loadsheet in loadsheets:
                if loadsheet in grouped_data:
                    for row in grouped_data[loadsheet]:
                        customer = row["outlet_code"]
                        amount = row["amount"]
                        
                        if customer not in customer_amounts:
                            customer_amounts[customer] = 0
                        customer_amounts[customer] += amount
                        total_amount += amount
            
            # Create parent document
            reco_doc = frappe.get_doc({
                "doctype": "Daily Sales Payment Reco",
                "driver": driver,
                "loadsheet_number": ", ".join(loadsheets),
                "initial_total_amount": total_amount,
                "net_total_amount": total_amount,
                "remaining_amount": total_amount,
                "additional_amount": 0,
                "return_amount": 0,
                "qr_amount": 0,
                "cheque_amount": 0,
                "cash_amount": 0,
                "credit_amount": 0,
                "expense_amount": 0,
                "settled": 0
            })
            
            # Add child table rows
            for customer, amount in customer_amounts.items():
                reco_doc.append("daily_sales_payment_reco_line", {
                    "customer": customer,
                    "initial_total_amount": amount,
                    "net_total_amount": amount,
                    "remaining_amount": amount,
                    "additional_amount": 0,
                    "return_amount": 0,
                    "qr_amount": 0,
                    "cheque_amount": 0,
                    "cash_amount": 0,
                    "credit_amount": 0,
                    "settled": 0
                })
            
            reco_doc.insert()
            frappe.db.commit()
            
            created_recos.append(reco_doc.name)
        
        return {
            "success": True,
            "data": {"created_recos": created_recos},
            "message": f"Created {len(created_recos)} reconciliation records"
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating payment recos: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error creating payment recos: {str(e)}"
        }


@frappe.whitelist()
def get_all_active_recos() -> Dict[str, Any]:
    """
    Get all active Daily Sales Payment Recos (for administrators).
    
    Returns:
        {
            "success": bool,
            "data": [{"driver": name, "driver_name": full_name, "count": int}],
            "message": str
        }
    """
    try:
        # Check if user is administrator
        if not frappe.has_permission("Daily Sales Payment Reco", "read"):
            return {
                "success": False,
                "data": [],
                "message": "Permission denied"
            }
        
        # Get all unsettled recos with driver info
        recos = frappe.db.sql("""
            SELECT DISTINCT
                r.driver,
                d.full_name as driver_name,
                COUNT(*) as count
            FROM `tabDaily Sales Payment Reco` r
            LEFT JOIN `tabDriver` d ON r.driver = d.name
            WHERE r.settled = 0
            GROUP BY r.driver, d.full_name
            ORDER BY d.full_name
        """, as_dict=True)
        
        return {
            "success": True,
            "data": recos,
            "message": f"Found {len(recos)} active reconciliations"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting all recos: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error: {str(e)}"
        }


@frappe.whitelist()
def get_driver_reco_data(driver_name: str = None) -> Dict[str, Any]:
    """
    Get active Daily Sales Payment Reco for a driver.
    For administrators: can specify any driver_name
    For regular users: returns their own driver data
    
    Args:
        driver_name: Driver's full name (matched from User.full_name)
    
    Returns:
        {
            "success": bool,
            "is_admin": bool,
            "data": {
                "reco": parent document data,
                "lines": child table rows,
                "summary": aggregated amounts
            },
            "message": str
        }
    """
    try:
        user = frappe.session.user
        is_admin = "System Manager" in frappe.get_roles(user) or "Administrator" in frappe.get_roles(user)
        
        # If no driver_name provided, use current user's full name
        if not driver_name:
            driver_name = frappe.db.get_value("User", user, "full_name")
        
        # Find driver by full_name (HRMS Driver doctype uses full_name, not driver_name)
        driver = frappe.db.get_value("Driver", {"full_name": driver_name}, "name")
        if not driver:
            return {
                "success": False,
                "is_admin": is_admin,
                "data": None,
                "message": f"No driver found for: {driver_name}"
            }
        
        # Get most recent unsettled reco for this driver
        recos = frappe.get_all(
            "Daily Sales Payment Reco",
            filters={
                "driver": driver,
                "settled": 0
            },
            fields=["name"],
            order_by="creation desc",
            limit=1
        )
        
        if not recos:
            return {
                "success": False,
                "data": None,
                "message": "No active reconciliation found for this driver"
            }
        
        # Get full document with child table
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", recos[0].name)
        
        # Format child table data
        lines = []
        for line in reco_doc.daily_sales_payment_reco_line:
            customer_name = frappe.db.get_value("Customer", line.customer, "customer_name")
            lines.append({
                "name": line.name,
                "customer": line.customer,
                "customer_name": customer_name,
                "initial_total_amount": line.initial_total_amount,
                "additional_amount": line.additional_amount,
                "net_total_amount": line.net_total_amount,
                "return_amount": line.return_amount,
                "qr_amount": line.qr_amount,
                "cheque_amount": line.cheque_amount,
                "cash_amount": line.cash_amount,
                "credit_amount": line.credit_amount,
                "remaining_amount": line.remaining_amount,
                "settled": line.settled,
                "remarks": line.remarks,
                "fonepay_qr_transaction": line.fonepay_qr_transaction,
                "cheques_taageta": line.cheques_taageta
            })
        
        # Summary data
        summary = {
            "initial_total_amount": reco_doc.initial_total_amount,
            "net_total_amount": reco_doc.net_total_amount,
            "cash_amount": reco_doc.cash_amount,
            "qr_amount": reco_doc.qr_amount,
            "cheque_amount": reco_doc.cheque_amount,
            "return_amount": reco_doc.return_amount,
            "credit_amount": reco_doc.credit_amount,
            "expense_amount": reco_doc.expense_amount,
            "remaining_amount": reco_doc.remaining_amount
        }
        
        return {
            "success": True,
            "is_admin": is_admin,
            "data": {
                "reco": {
                    "name": reco_doc.name,
                    "driver": reco_doc.driver,
                    "driver_name": driver_name,
                    "loadsheet_number": reco_doc.loadsheet_number
                },
                "lines": lines,
                "summary": summary
            },
            "message": "Reconciliation data retrieved successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting driver reco data: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error getting driver reco data: {str(e)}"
        }


@frappe.whitelist()
def update_payment_entry(
    line_name: str,
    return_amount: float = 0,
    additional_amount: float = 0,
    credit_amount: float = 0,
    cash_amount: float = 0,
    qr_amount: float = 0,
    cheque_amount: float = 0,
    fonepay_qr_transaction: str = None,
    cheques_taageta: str = None,
    remarks: str = None
) -> Dict[str, Any]:
    """
    Update child row payment details and aggregate to parent.
    
    Args:
        line_name: Child table row name
        return_amount: Return amount
        additional_amount: Additional amount
        credit_amount: Credit amount
        cash_amount: Cash amount
        qr_amount: QR amount
        cheque_amount: Cheque amount
        fonepay_qr_transaction: Fonepay QR Transaction reference
        cheques_taageta: Cheques Taageta reference
        remarks: Remarks
    
    Returns:
        {
            "success": bool,
            "data": {"updated_line": line_name, "parent_name": parent_name},
            "message": str
        }
    """
    try:
        # Validate line_name
        if not line_name:
            raise ValueError("line_name is required")
        
        # Convert string amounts to floats (in case they come as strings from frontend)
        return_amount = float(return_amount or 0)
        additional_amount = float(additional_amount or 0)
        credit_amount = float(credit_amount or 0)
        cash_amount = float(cash_amount or 0)
        qr_amount = float(qr_amount or 0)
        cheque_amount = float(cheque_amount or 0)
        
        # Handle null/None values for references
        if fonepay_qr_transaction in [None, 'null', 'None', '']:
            fonepay_qr_transaction = None
        if cheques_taageta in [None, 'null', 'None', '']:
            cheques_taageta = None
        if remarks in [None, 'null', 'None', '']:
            remarks = None
        
        # Get the child line
        try:
            line_doc = frappe.get_doc("Daily Sales Payment Reco Line", line_name)
        except frappe.DoesNotExistError:
            raise ValueError(f"Payment line '{line_name}' not found")
        except Exception as e:
            raise ValueError(f"Error loading payment line '{line_name}': {str(e)}")
        
        # Update amounts
        line_doc.return_amount = return_amount
        line_doc.additional_amount = additional_amount
        line_doc.credit_amount = credit_amount
        line_doc.cash_amount = cash_amount
        line_doc.qr_amount = qr_amount
        line_doc.cheque_amount = cheque_amount
        
        # Update references - only set if not None
        if fonepay_qr_transaction is not None:
            line_doc.fonepay_qr_transaction = fonepay_qr_transaction
        else:
            # Explicitly clear the field if it was set before
            if hasattr(line_doc, 'fonepay_qr_transaction'):
                line_doc.fonepay_qr_transaction = None
        
        if cheques_taageta is not None:
            line_doc.cheques_taageta = cheques_taageta
        else:
            # Explicitly clear the field if it was set before
            if hasattr(line_doc, 'cheques_taageta'):
                line_doc.cheques_taageta = None
        
        if remarks is not None:
            line_doc.remarks = remarks
        else:
            # Explicitly clear the field if it was set before
            if hasattr(line_doc, 'remarks'):
                line_doc.remarks = None
        
        # Calculate net and remaining
        line_doc.net_total_amount = line_doc.initial_total_amount + additional_amount - return_amount
        line_doc.remaining_amount = line_doc.net_total_amount - cash_amount - qr_amount - cheque_amount - credit_amount
        
        # Mark as settled if remaining is 0
        if line_doc.remaining_amount == 0:
            line_doc.settled = 1
        
        # Save the child line with detailed error handling
        # Bypass permission checks since this is a whitelisted API method
        try:
            frappe.flags.ignore_permissions = True
            line_doc.save(ignore_permissions=True)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e) if str(e) else repr(e)
            error_trace = traceback.format_exc()
            raise ValueError(f"Error saving payment line ({error_type}): {error_msg}\nTraceback: {error_trace[:500]}")
        finally:
            frappe.flags.ignore_permissions = False
        
        # Get parent and update aggregated amounts
        parent_name = line_doc.parent
        try:
            parent_doc = frappe.get_doc("Daily Sales Payment Reco", parent_name)
        except frappe.DoesNotExistError:
            raise ValueError(f"Parent reconciliation '{parent_name}' not found")
        except Exception as e:
            raise ValueError(f"Error loading parent reconciliation: {str(e)}")
        
        # Aggregate all child rows
        total_return = 0
        total_additional = 0
        total_credit = 0
        total_cash = 0
        total_qr = 0
        total_cheque = 0
        total_remaining = 0
        all_settled = True
        
        for line in parent_doc.daily_sales_payment_reco_line:
            total_return += line.return_amount or 0
            total_additional += line.additional_amount or 0
            total_credit += line.credit_amount or 0
            total_cash += line.cash_amount or 0
            total_qr += line.qr_amount or 0
            total_cheque += line.cheque_amount or 0
            total_remaining += line.remaining_amount or 0
            if not line.settled:
                all_settled = False
        
        # Update parent
        parent_doc.return_amount = total_return
        parent_doc.additional_amount = total_additional
        parent_doc.credit_amount = total_credit
        parent_doc.cash_amount = total_cash
        parent_doc.qr_amount = total_qr
        parent_doc.cheque_amount = total_cheque
        parent_doc.net_total_amount = parent_doc.initial_total_amount + total_additional - total_return
        parent_doc.remaining_amount = total_remaining
        
        if all_settled:
            parent_doc.settled = 1
            parent_doc.settled_at = datetime.now()
        
        # Save the parent with detailed error handling
        # Bypass permission checks since this is a whitelisted API method
        try:
            frappe.flags.ignore_permissions = True
            parent_doc.save(ignore_permissions=True)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e) if str(e) else repr(e)
            error_trace = traceback.format_exc()
            raise ValueError(f"Error saving parent reconciliation ({error_type}): {error_msg}\nTraceback: {error_trace[:500]}")
        finally:
            frappe.flags.ignore_permissions = False
        
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                "updated_line": line_name,
                "parent_name": parent_name
            },
            "message": "Payment entry updated successfully"
        }
        
    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e) if str(e) else repr(e)
        error_traceback = traceback.format_exc()
        frappe.log_error(f"Error updating payment entry: {error_msg}\n{error_traceback}", "Payment Reco API Error")
        return {
            "success": False,
            "data": None,
            "message": f"Error updating payment entry: {error_msg}" if error_msg else "Error updating payment entry: Unknown error occurred"
        }


@frappe.whitelist()
def generate_qr_no_payment_entry(customer: str, amount: float) -> Dict[str, Any]:
    """
    Generate Fonepay QR code without creating Payment Entry.
    Uses the existing create_dynamic_qr function from fonepay module.
    
    Args:
        customer: Customer ID
        amount: Amount for QR code
    
    Returns:
        {
            "success": bool,
            "data": {
                "qr_code": base64 QR image,
                "transaction_id": Fonepay QR Transaction reference
            },
            "message": str
        }
    """
    try:
        # Use the existing create_dynamic_qr function which properly handles all validations
        from custom_erp.custom_erp.api import fonepay
        
        result = fonepay.create_dynamic_qr(
            amount=amount,
            customer=customer,
            sales_invoice=None,
            remarks1="",
            remarks2="Daily Reconciliation Payment",
            metadata="Daily Payment Reconciliation"
        )
        
        return {
            "success": True,
            "data": {
                "qr_code": result.get("qr_message", ""),
                "transaction_id": result.get("tx_name", "")
            },
            "message": "QR code generated successfully"
        }
            
    except Exception as e:
        frappe.log_error(f"Error generating QR: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error generating QR: {str(e)}"
        }


@frappe.whitelist()
def compress_and_attach_image(
    image_data: str,
    reference_doctype: str,
    reference_name: str,
    filename: str = None
) -> Dict[str, Any]:
    """
    Compress photo and create attachment.
    
    Args:
        image_data: Base64 encoded image data
        reference_doctype: Reference doctype name
        reference_name: Reference document name
        filename: Optional filename
    
    Returns:
        {
            "success": bool,
            "data": {"file_url": file URL},
            "message": str
        }
    """
    try:
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Compress image using PIL
        from PIL import Image
        import io
        
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGB")
        
        # Calculate resize dimensions to keep under 500KB
        max_size = (1920, 1920)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Compress to JPEG
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        compressed_bytes = output.getvalue()
        
        # If still too large, reduce quality
        quality = 85
        while len(compressed_bytes) > 500000 and quality > 40:
            quality -= 10
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=quality, optimize=True)
            compressed_bytes = output.getvalue()
        
        # Generate filename
        if not filename:
            filename = f"cheque_{reference_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Create File document
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "attached_to_doctype": reference_doctype,
            "attached_to_name": reference_name,
            "content": compressed_bytes,
            "is_private": 1
        })
        file_doc.save()
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {"file_url": file_doc.file_url},
            "message": "Image compressed and attached successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error compressing image: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error compressing image: {str(e)}"
        }


@frappe.whitelist()
def create_cheque_taageta(
    customer: str,
    cheque_no: str,
    cheque_date_nepali: str,
    bank_name: str,
    amount: float,
    promised_date: str = None,
    brought_by: str = None
) -> Dict[str, Any]:
    """
    Create a Cheques Taageta record with permission bypass.
    This is a whitelisted method for the dailyrecoentry app.
    
    Args:
        customer: Customer ID
        cheque_no: Cheque number
        cheque_date_nepali: Cheque date in Nepali format (YYYY.MM.DD) - stored as string
        bank_name: Institute/Bank name
        amount: Cheque amount
        promised_date: Promised date in English AD format (YYYY-MM-DD) - stored as Date field
        brought_by: User who brought the cheque (optional)
    
    Returns:
        {
            "success": bool,
            "data": {"name": cheque document name},
            "message": str
        }
    """
    try:
        # Validate required fields
        if not customer:
            raise ValueError("Customer is required")
        if not cheque_no:
            raise ValueError("Cheque number is required")
        if not bank_name:
            raise ValueError("Institute name is required")
        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Create the Cheques Taageta document
        cheque_doc_data = {
            "doctype": "Cheques Taageta",
            "customer": customer,
            "cheque_no": cheque_no,
            "cheque_date_nepali": cheque_date_nepali,
            "bank_name": bank_name,
            "amount": amount,
            "brought_by": brought_by or frappe.session.user
        }
        
        # Add promised_date if provided (AD date from date picker)
        if promised_date:
            cheque_doc_data["promised_date"] = promised_date
        
        cheque_doc = frappe.get_doc(cheque_doc_data)
        
        # Bypass permission checks since this is a whitelisted API method
        frappe.flags.ignore_permissions = True
        try:
            cheque_doc.insert(ignore_permissions=True)
        finally:
            frappe.flags.ignore_permissions = False
        
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {"name": cheque_doc.name},
            "message": "Cheque created successfully"
        }
        
    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e) if str(e) else repr(e)
        error_traceback = traceback.format_exc()
        frappe.log_error(f"Error creating cheque: {error_msg}\n{error_traceback}", "Payment Reco API Error")
        return {
            "success": False,
            "data": None,
            "message": f"Error creating cheque: {error_msg}" if error_msg else "Error creating cheque: Unknown error occurred"
        }


# ============================================================================
# EXPENSE MANAGEMENT API
# ============================================================================

@frappe.whitelist()
def save_expense_amount(
    reco_name: str,
    expense_amount: float
) -> Dict[str, Any]:
    """
    Save expense amount for a Daily Sales Payment Reco.
    Since expense is paid from cash, it subtracts from cash_amount.
    
    Args:
        reco_name: Name of the Daily Sales Payment Reco document
        expense_amount: Amount of expense to record
    
    Returns:
        {
            "success": bool,
            "data": updated summary,
            "message": str
        }
    """
    try:
        if not reco_name:
            return {
                "success": False,
                "data": None,
                "message": "Reco name is required"
            }
        
        expense_amount = float(expense_amount or 0)
        if expense_amount < 0:
            return {
                "success": False,
                "data": None,
                "message": "Expense amount cannot be negative"
            }
        
        # Get the reco document
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        
        # Calculate the difference from previous expense
        previous_expense = float(reco_doc.expense_amount or 0)
        expense_diff = expense_amount - previous_expense
        
        # Update expense amount
        reco_doc.expense_amount = expense_amount
        
        # Since expense is paid from cash, adjust cash_amount
        # When expense increases, cash decreases (and vice versa)
        current_cash = float(reco_doc.cash_amount or 0)
        new_cash = current_cash - expense_diff
        
        # Ensure cash doesn't go negative
        if new_cash < 0:
            return {
                "success": False,
                "data": None,
                "message": f"Insufficient cash. Available cash: NPR {current_cash:,.0f}. Cannot set expense to NPR {expense_amount:,.0f}"
            }
        
        reco_doc.cash_amount = new_cash
        
        # Recalculate remaining amount
        # remaining = net_total - (cash + qr + cheque + credit + return)
        total_collected = (
            new_cash +
            float(reco_doc.qr_amount or 0) +
            float(reco_doc.cheque_amount or 0) +
            float(reco_doc.credit_amount or 0) +
            float(reco_doc.return_amount or 0)
        )
        reco_doc.remaining_amount = float(reco_doc.net_total_amount or 0) - total_collected
        
        # Save the document
        reco_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Return updated summary
        return {
            "success": True,
            "data": {
                "expense_amount": reco_doc.expense_amount,
                "cash_amount": reco_doc.cash_amount,
                "remaining_amount": reco_doc.remaining_amount,
                "initial_total_amount": reco_doc.initial_total_amount,
                "net_total_amount": reco_doc.net_total_amount,
                "qr_amount": reco_doc.qr_amount,
                "cheque_amount": reco_doc.cheque_amount,
                "return_amount": reco_doc.return_amount,
                "credit_amount": reco_doc.credit_amount
            },
            "message": f"Expense of NPR {expense_amount:,.0f} saved successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error saving expense: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error saving expense: {str(e)}"
        }


# ============================================================================
# DAILY TRANSACTIONS DASHBOARD API METHODS
# ============================================================================

@frappe.whitelist()
def get_daily_transactions_summary(date: str = None) -> Dict[str, Any]:
    """
    Get summary totals for Daily Sales Payment Reco for a specific date.
    
    Args:
        date: Date in AD format (YYYY-MM-DD). If None, uses today's date.
    
    Returns:
        {
            "success": bool,
            "data": {
                "net_total_amount": float,
                "cash_amount": float,
                "qr_amount": float,
                "cheque_amount": float,
                "credit_amount": float,
                "return_amount": float,
                "expense_amount": float,
                "remaining_amount": float,
                "total_records": int,
                "cash_count": int,
                "qr_count": int,
                "cheque_count": int,
                "credit_count": int,
                "return_count": int,
                "drivers": List of unique drivers,
                "customers": List of unique customers
            },
            "message": str
        }
    """
    try:
        # Default to today if no date provided
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get parent records created on the specified date
        parent_records = frappe.get_all(
            "Daily Sales Payment Reco",
            filters=[
                ["creation", ">=", f"{date} 00:00:00"],
                ["creation", "<=", f"{date} 23:59:59"]
            ],
            fields=["name", "driver", "net_total_amount", "cash_amount", "qr_amount", 
                    "cheque_amount", "credit_amount", "return_amount", "expense_amount", 
                    "remaining_amount"]
        )
        
        if not parent_records:
            return {
                "success": True,
                "data": {
                    "net_total_amount": 0,
                    "cash_amount": 0,
                    "qr_amount": 0,
                    "cheque_amount": 0,
                    "credit_amount": 0,
                    "return_amount": 0,
                    "expense_amount": 0,
                    "remaining_amount": 0,
                    "total_records": 0,
                    "cash_count": 0,
                    "qr_count": 0,
                    "cheque_count": 0,
                    "credit_count": 0,
                    "return_count": 0,
                    "drivers": [],
                    "customers": []
                },
                "message": "No records found for this date"
            }
        
        parent_names = [p.name for p in parent_records]
        
        # Get all child lines from these parents
        lines = frappe.get_all(
            "Daily Sales Payment Reco Line",
            filters={"parent": ["in", parent_names]},
            fields=["name", "customer", "net_total_amount", "cash_amount", "qr_amount",
                    "cheque_amount", "credit_amount", "return_amount", "remaining_amount", "settled"]
        )
        
        # Aggregate totals
        totals = {
            "net_total_amount": 0,
            "cash_amount": 0,
            "qr_amount": 0,
            "cheque_amount": 0,
            "credit_amount": 0,
            "return_amount": 0,
            "expense_amount": 0,
            "remaining_amount": 0,
        }
        
        cash_count = 0
        qr_count = 0
        cheque_count = 0
        credit_count = 0
        return_count = 0
        
        customers_set = set()
        
        for line in lines:
            totals["net_total_amount"] += line.net_total_amount or 0
            totals["cash_amount"] += line.cash_amount or 0
            totals["qr_amount"] += line.qr_amount or 0
            totals["cheque_amount"] += line.cheque_amount or 0
            totals["credit_amount"] += line.credit_amount or 0
            totals["return_amount"] += line.return_amount or 0
            totals["remaining_amount"] += line.remaining_amount or 0
            
            if line.cash_amount and line.cash_amount > 0:
                cash_count += 1
            if line.qr_amount and line.qr_amount > 0:
                qr_count += 1
            if line.cheque_amount and line.cheque_amount > 0:
                cheque_count += 1
            if line.credit_amount and line.credit_amount > 0:
                credit_count += 1
            if line.return_amount and line.return_amount > 0:
                return_count += 1
            
            customers_set.add(line.customer)
        
        # Aggregate expense from parent records
        for parent in parent_records:
            totals["expense_amount"] += parent.expense_amount or 0
        
        # Get unique drivers with names
        drivers_set = set()
        for parent in parent_records:
            if parent.driver:
                drivers_set.add(parent.driver)
        
        drivers_list = []
        for driver_id in drivers_set:
            driver_name = frappe.db.get_value("Driver", driver_id, "full_name") or driver_id
            drivers_list.append({
                "driver": driver_id,
                "driver_name": driver_name
            })
        
        # Get customer names
        customers_list = []
        for customer_id in customers_set:
            customer_name = frappe.db.get_value("Customer", customer_id, "customer_name") or customer_id
            customers_list.append({
                "customer": customer_id,
                "customer_name": customer_name
            })
        
        return {
            "success": True,
            "data": {
                **totals,
                "total_records": len(lines),
                "cash_count": cash_count,
                "qr_count": qr_count,
                "cheque_count": cheque_count,
                "credit_count": credit_count,
                "return_count": return_count,
                "drivers": drivers_list,
                "customers": customers_list
            },
            "message": f"Found {len(lines)} line items from {len(parent_records)} reconciliation records"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting daily transactions summary: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": None,
            "message": f"Error: {str(e)}"
        }


@frappe.whitelist()
def get_daily_transactions_by_user(
    date: str = None,
    driver_filter: str = None,
    status_filter: str = None
) -> Dict[str, Any]:
    """
    Get daily transactions grouped by driver/user.
    Uses summarized values from parent document (not line items).
    
    Args:
        date: Date in AD format (YYYY-MM-DD). If None, uses today's date.
        driver_filter: Optional driver ID to filter by.
        status_filter: Optional 'settled' or 'pending' filter.
    
    Returns:
        {
            "success": bool,
            "data": List of driver aggregates with totals from parent documents,
            "message": str
        }
    """
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Build filters for parent records
        filters = [
            ["creation", ">=", f"{date} 00:00:00"],
            ["creation", "<=", f"{date} 23:59:59"]
        ]
        
        if driver_filter:
            filters.append(["driver", "=", driver_filter])
        
        if status_filter == "settled":
            filters.append(["settled", "=", 1])
        elif status_filter == "pending":
            filters.append(["settled", "=", 0])
        
        # Fetch parent records with ALL summary fields from parent document
        parent_records = frappe.get_all(
            "Daily Sales Payment Reco",
            filters=filters,
            fields=[
                "name", "driver",
                "net_total_amount", "cash_amount", "qr_amount", "cheque_amount",
                "credit_amount", "return_amount", "expense_amount", "remaining_amount"
            ]
        )
        
        if not parent_records:
            return {
                "success": True,
                "data": [],
                "message": "No records found"
            }
        
        # Group by driver - use parent document summary values
        driver_data = {}
        
        for parent in parent_records:
            driver_id = parent.driver or "Unknown"
            
            if driver_id not in driver_data:
                driver_name = frappe.db.get_value("Driver", driver_id, "full_name") or driver_id
                driver_data[driver_id] = {
                    "driver": driver_id,
                    "driver_name": driver_name,
                    "net_total_amount": 0,
                    "cash_amount": 0,
                    "qr_amount": 0,
                    "cheque_amount": 0,
                    "credit_amount": 0,
                    "return_amount": 0,
                    "expense_amount": 0,
                    "remaining_amount": 0,
                    "line_count": 0,
                    "parent_names": []
                }
            
            # Sum values from parent document (not lines)
            driver_data[driver_id]["net_total_amount"] += parent.net_total_amount or 0
            driver_data[driver_id]["cash_amount"] += parent.cash_amount or 0
            driver_data[driver_id]["qr_amount"] += parent.qr_amount or 0
            driver_data[driver_id]["cheque_amount"] += parent.cheque_amount or 0
            driver_data[driver_id]["credit_amount"] += parent.credit_amount or 0
            driver_data[driver_id]["return_amount"] += parent.return_amount or 0
            driver_data[driver_id]["expense_amount"] += parent.expense_amount or 0
            driver_data[driver_id]["remaining_amount"] += parent.remaining_amount or 0
            driver_data[driver_id]["parent_names"].append(parent.name)
        
        # Get line count for each driver
        for driver_id, data in driver_data.items():
            line_count = frappe.db.count(
                "Daily Sales Payment Reco Line",
                filters={"parent": ["in", data["parent_names"]]}
            )
            data["line_count"] = line_count
            # Remove parent_names from output
            del data["parent_names"]
        
        # Sort by net total descending
        result = sorted(driver_data.values(), key=lambda x: x["net_total_amount"], reverse=True)
        
        return {
            "success": True,
            "data": result,
            "message": f"Found {len(result)} drivers"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting daily transactions by user: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error: {str(e)}"
        }


@frappe.whitelist()
def get_daily_transactions_by_customer(
    date: str = None,
    driver_filter: str = None,
    customer_filter: str = None,
    status_filter: str = None
) -> Dict[str, Any]:
    """
    Get daily transactions grouped by customer.
    
    Args:
        date: Date in AD format (YYYY-MM-DD). If None, uses today's date.
        driver_filter: Optional driver ID to filter by.
        customer_filter: Optional customer ID to filter by.
        status_filter: Optional 'settled' or 'pending' filter.
    
    Returns:
        {
            "success": bool,
            "data": List of customer details with amounts,
            "message": str
        }
    """
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Build filters for parent records
        parent_filters = [
            ["creation", ">=", f"{date} 00:00:00"],
            ["creation", "<=", f"{date} 23:59:59"]
        ]
        
        if driver_filter:
            parent_filters.append(["driver", "=", driver_filter])
        
        parent_records = frappe.get_all(
            "Daily Sales Payment Reco",
            filters=parent_filters,
            fields=["name", "driver"]
        )
        
        if not parent_records:
            return {
                "success": True,
                "data": [],
                "message": "No records found"
            }
        
        parent_names = [p.name for p in parent_records]
        
        # Build driver lookup
        driver_lookup = {p.name: p.driver for p in parent_records}
        
        # Build filters for child lines
        line_filters = {"parent": ["in", parent_names]}
        
        if customer_filter:
            line_filters["customer"] = customer_filter
        
        if status_filter == "settled":
            line_filters["settled"] = 1
        elif status_filter == "pending":
            line_filters["settled"] = 0
        
        lines = frappe.get_all(
            "Daily Sales Payment Reco Line",
            filters=line_filters,
            fields=["name", "parent", "customer", "net_total_amount", "cash_amount", "qr_amount",
                    "cheque_amount", "credit_amount", "return_amount", "remaining_amount", "settled", "remarks"]
        )
        
        # Format response with customer names and driver names
        result = []
        for line in lines:
            customer_name = frappe.db.get_value("Customer", line.customer, "customer_name") or line.customer
            driver_id = driver_lookup.get(line.parent, "")
            driver_name = frappe.db.get_value("Driver", driver_id, "full_name") if driver_id else "Unknown"
            
            result.append({
                "name": line.name,
                "customer": line.customer,
                "customer_name": customer_name,
                "driver": driver_id,
                "driver_name": driver_name,
                "net_total_amount": line.net_total_amount or 0,
                "cash_amount": line.cash_amount or 0,
                "qr_amount": line.qr_amount or 0,
                "cheque_amount": line.cheque_amount or 0,
                "credit_amount": line.credit_amount or 0,
                "return_amount": line.return_amount or 0,
                "remaining_amount": line.remaining_amount or 0,
                "settled": line.settled,
                "remarks": line.remarks
            })
        
        # Sort by net total descending
        result = sorted(result, key=lambda x: x["net_total_amount"], reverse=True)
        
        return {
            "success": True,
            "data": result,
            "message": f"Found {len(result)} customer records"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting daily transactions by customer: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error: {str(e)}"
        }


@frappe.whitelist()
def get_daily_transactions_details(
    date: str = None,
    driver_filter: str = None,
    customer_filter: str = None,
    category_filter: str = None,
    status_filter: str = None,
    limit: int = 200
) -> Dict[str, Any]:
    """
    Get detailed daily transaction line items with all filters.
    
    Args:
        date: Date in AD format (YYYY-MM-DD). If None, uses today's date.
        driver_filter: Optional driver ID to filter by.
        customer_filter: Optional customer ID to filter by.
        category_filter: Optional category filter ('cash', 'qr', 'cheque', 'credit', 'return').
        status_filter: Optional 'settled' or 'pending' filter.
        limit: Maximum number of records to return.
    
    Returns:
        {
            "success": bool,
            "data": List of line item details,
            "message": str
        }
    """
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Build filters for parent records
        parent_filters = [
            ["creation", ">=", f"{date} 00:00:00"],
            ["creation", "<=", f"{date} 23:59:59"]
        ]
        
        if driver_filter:
            parent_filters.append(["driver", "=", driver_filter])
        
        parent_records = frappe.get_all(
            "Daily Sales Payment Reco",
            filters=parent_filters,
            fields=["name", "driver"]
        )
        
        if not parent_records:
            return {
                "success": True,
                "data": [],
                "message": "No records found"
            }
        
        parent_names = [p.name for p in parent_records]
        driver_lookup = {p.name: p.driver for p in parent_records}
        
        # Build filters for child lines
        line_filters = {"parent": ["in", parent_names]}
        
        if customer_filter:
            line_filters["customer"] = customer_filter
        
        if status_filter == "settled":
            line_filters["settled"] = 1
        elif status_filter == "pending":
            line_filters["settled"] = 0
        
        lines = frappe.get_all(
            "Daily Sales Payment Reco Line",
            filters=line_filters,
            fields=["name", "parent", "customer", "initial_total_amount", "additional_amount",
                    "net_total_amount", "cash_amount", "qr_amount", "cheque_amount",
                    "credit_amount", "return_amount", "remaining_amount", "settled", "remarks",
                    "fonepay_qr_transaction", "cheques_taageta"],
            limit=limit
        )
        
        # Apply category filter (post-query filter since it's complex)
        if category_filter:
            filtered_lines = []
            for line in lines:
                if category_filter == "cash" and line.cash_amount and line.cash_amount > 0:
                    filtered_lines.append(line)
                elif category_filter == "qr" and line.qr_amount and line.qr_amount > 0:
                    filtered_lines.append(line)
                elif category_filter == "cheque" and line.cheque_amount and line.cheque_amount > 0:
                    filtered_lines.append(line)
                elif category_filter == "credit" and line.credit_amount and line.credit_amount > 0:
                    filtered_lines.append(line)
                elif category_filter == "return" and line.return_amount and line.return_amount > 0:
                    filtered_lines.append(line)
            lines = filtered_lines
        
        # Format response with names
        result = []
        for line in lines:
            customer_name = frappe.db.get_value("Customer", line.customer, "customer_name") or line.customer
            driver_id = driver_lookup.get(line.parent, "")
            driver_name = frappe.db.get_value("Driver", driver_id, "full_name") if driver_id else "Unknown"
            
            result.append({
                "name": line.name,
                "parent": line.parent,
                "customer": line.customer,
                "customer_name": customer_name,
                "driver": driver_id,
                "driver_name": driver_name,
                "initial_total_amount": line.initial_total_amount or 0,
                "additional_amount": line.additional_amount or 0,
                "net_total_amount": line.net_total_amount or 0,
                "cash_amount": line.cash_amount or 0,
                "qr_amount": line.qr_amount or 0,
                "cheque_amount": line.cheque_amount or 0,
                "credit_amount": line.credit_amount or 0,
                "return_amount": line.return_amount or 0,
                "remaining_amount": line.remaining_amount or 0,
                "settled": line.settled,
                "remarks": line.remarks,
                "fonepay_qr_transaction": line.fonepay_qr_transaction,
                "cheques_taageta": line.cheques_taageta
            })
        
        # Sort by net total descending
        result = sorted(result, key=lambda x: x["net_total_amount"], reverse=True)
        
        return {
            "success": True,
            "data": result,
            "message": f"Found {len(result)} line items"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting daily transactions details: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "message": f"Error: {str(e)}"
        }
