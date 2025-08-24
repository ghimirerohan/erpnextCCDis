import frappe
from frappe import _
from frappe.utils import getdate, flt
from datetime import datetime, timedelta

@frappe.whitelist()
def get_sales_invoices(filters=None):
    """Get sales invoices with filters"""
    try:
        # Handle different input formats
        if isinstance(filters, str):
            import json
            try:
                filters = json.loads(filters)
            except json.JSONDecodeError:
                filters = {}
        elif filters is None:
            filters = {}
        
        # Default filters
        if not filters:
            filters = {}
        
        # Build query conditions
        conditions = ["si.docstatus = 1"]  # Only submitted invoices
        
        if filters.get("customer"):
            conditions.append(f"si.customer = '{filters['customer']}'")
        
        if filters.get("from_date"):
            conditions.append(f"si.posting_date >= '{filters['from_date']}'")
        
        if filters.get("to_date"):
            conditions.append(f"si.posting_date <= '{filters['to_date']}'")
        
        # Build the query
        query = f"""
            SELECT 
                si.name,
                si.posting_date,
                si.customer,
                si.customer_name,
                si.grand_total,
                si.total,
                si.total_taxes_and_charges,
                si.discount_amount,
                si.currency,
                si.conversion_rate,
                si.status,
                si.due_date,
                si.outstanding_amount
            FROM `tabSales Invoice` si
            WHERE {' AND '.join(conditions)}
            ORDER BY si.posting_date DESC
        """
        
        invoices = frappe.db.sql(query, as_dict=True)
        
        # Get items for each invoice
        for invoice in invoices:
            invoice['items'] = get_invoice_items(invoice['name'])
        
        return {
            "success": True,
            "data": invoices,
            "total_count": len(invoices)
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_sales_invoices: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def get_sales_invoice_summary(filters=None):
    """Get sales invoice summary grouped by customer and date"""
    try:
        # Handle different input formats
        if isinstance(filters, str):
            import json
            try:
                filters = json.loads(filters)
            except json.JSONDecodeError:
                filters = {}
        elif filters is None:
            filters = {}
        
        if not filters:
            filters = {}
        
        conditions = ["si.docstatus = 1"]
        
        if filters.get("customer"):
            conditions.append(f"si.customer = '{filters['customer']}'")
        
        if filters.get("from_date"):
            conditions.append(f"si.posting_date >= '{filters['from_date']}'")
        
        if filters.get("to_date"):
            conditions.append(f"si.posting_date <= '{filters['to_date']}'")
        
        # Get summary data
        summary_query = f"""
            SELECT 
                si.customer,
                si.customer_name,
                DATE(si.posting_date) as posting_date,
                COUNT(si.name) as invoice_count,
                SUM(si.grand_total) as total_amount,
                SUM(si.total) as net_total,
                SUM(si.total_taxes_and_charges) as total_taxes,
                SUM(si.discount_amount) as total_discount,
                SUM(si.outstanding_amount) as outstanding_amount
            FROM `tabSales Invoice` si
            WHERE {' AND '.join(conditions)}
            GROUP BY si.customer, DATE(si.posting_date)
            ORDER BY si.customer, si.posting_date DESC
        """
        
        summary = frappe.db.sql(summary_query, as_dict=True)
        
        # Get item summary for each group
        for group in summary:
            group['items'] = get_item_summary_by_customer_date(
                group['customer'], 
                group['posting_date']
            )
        
        return {
            "success": True,
            "data": summary,
            "total_count": len(summary)
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_sales_invoice_summary: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def get_invoice_items(invoice_name):
    """Get items for a specific invoice"""
    items_query = """
        SELECT 
            item_code,
            item_name,
            description,
            qty,
            rate,
            amount,
            uom,
            discount_amount,
            discount_percentage
        FROM `tabSales Invoice Item`
        WHERE parent = %s
        ORDER BY idx
    """
    
    return frappe.db.sql(items_query, invoice_name, as_dict=True)

def get_item_summary_by_customer_date(customer, posting_date):
    """Get item summary for a specific customer and date"""
    items_query = """
        SELECT 
            sii.item_code,
            sii.item_name,
            sii.description,
            SUM(sii.qty) as total_qty,
            AVG(sii.rate) as avg_rate,
            SUM(sii.amount) as total_amount,
            sii.uom,
            SUM(sii.discount_amount) as total_discount
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        WHERE si.customer = %s 
        AND DATE(si.posting_date) = %s
        AND si.docstatus = 1
        GROUP BY sii.item_code, sii.item_name, sii.uom
        ORDER BY total_amount DESC
    """
    
    return frappe.db.sql(items_query, (customer, posting_date), as_dict=True)

@frappe.whitelist()
def get_customers():
    """Get list of customers for filter dropdown"""
    try:
        customers = frappe.db.sql("""
            SELECT DISTINCT 
                customer,
                customer_name
            FROM `tabSales Invoice`
            WHERE docstatus = 1
            ORDER BY customer_name
        """, as_dict=True)
        
        return {
            "success": True,
            "data": customers
        }
    except Exception as e:
        frappe.log_error(f"Error in get_customers: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }



@frappe.whitelist()
def create_sales_invoice(payload: dict | str = None):
    """Create a draft Sales Invoice from structured payload (similar to Data Import)."""
    try:
        if isinstance(payload, str):
            import json
            payload = json.loads(payload)
        if not payload:
            frappe.throw("Payload is required")

        customer = payload.get("customer") or payload.get("customer_name")
        if not customer:
            frappe.throw("Customer is required")

        doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            **({"posting_date": payload.get("posting_date")} if payload.get("posting_date") else {}),
            **({"discount_amount": payload.get("discount_amount")} if payload.get("discount_amount") is not None else {}),
        })

        # For returns, make discount amount negative in the backend
        isReturn = payload.get("isReturn", False)
        if isReturn and payload.get("discount_amount") is not None:
            doc.discount_amount = -abs(payload.get("discount_amount"))

        for item in (payload.get("items") or []):
            code = item.get("item_code") or item.get("materialCode") or ""
            qty = item.get("qty") or item.get("salesQty") or 0
            amount = item.get("amount") or item.get("lineTotal")
            
            # Make quantity and amount negative for credit notes/returns
            if isReturn:
                if qty > 0:
                    qty = -qty
                if amount is not None:
                    amount = -abs(amount)
            
            doc.append("items", {
                "doctype": "Sales Invoice Item",
                "item_code": code,
                # Server override expects item_name to be an Item docname
                "item_name": item.get("item_name") or code,
                "qty": qty,
                **({"rate": item.get("rate") or item.get("unitPrice")} if (item.get("rate") or item.get("unitPrice")) is not None else {}),
                **({"amount": amount} if amount is not None else {}),
            })

        doc.insert()
        return {"success": True, "name": doc.name}
    except Exception as e:
        frappe.log_error(f"create_sales_invoice failed: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def check_duplicate_invoice(customer=None, invoice_number=None, invoice_date=None, invoice_type=None):
    """
    Check if a sales invoice with the same customer, invoice number, and date already exists.
    
    Args:
        customer: Customer name
        invoice_number: Invoice number
        invoice_date: Invoice date
        invoice_type: Type of invoice (purchase/sales)
        
    Returns:
        Duplicate check result
    """
    try:
        if not customer or not invoice_number or not invoice_date:
            return {"success": False, "error": "Customer, invoice number, and date are required"}
        
        # Parse the date to ensure consistency
        from datetime import datetime
        try:
            # Try common formats
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%d.%m.%Y"):
                try:
                    parsed_date = datetime.strptime(invoice_date, fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
            else:
                return {"success": False, "error": "Invalid date format"}
        except Exception:
            return {"success": False, "error": "Invalid date format"}
        
        # Check for existing invoice
        doctype = "Sales Invoice" if invoice_type == "sales" else "Purchase Invoice"
        
        if invoice_type == "sales":
            existing_invoice = frappe.db.get_value(
                doctype,
                {
                    "customer": customer,
                    "bill_no": invoice_number,
                    "posting_date": parsed_date
                },
                "name"
            )
        else:
            existing_invoice = frappe.db.get_value(
                doctype,
                {
                    "supplier": customer,
                    "bill_no": invoice_number,
                    "posting_date": parsed_date
                },
                "name"
            )
        
        return {
            "success": True,
            "isDuplicate": bool(existing_invoice),
            "existing_invoice": existing_invoice
        }
        
    except Exception as e:
        frappe.log_error(f"check_duplicate_invoice failed: {str(e)}")
        return {"success": False, "error": str(e)}
        
    except Exception as e:
        frappe.log_error(f"Error in get_customers: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
