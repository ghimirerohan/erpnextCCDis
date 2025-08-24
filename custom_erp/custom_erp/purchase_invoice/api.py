import base64
from datetime import datetime
import os
import base64 as _b64
import json as _json
import requests
from typing import Any, Dict, List, Optional

import frappe
from frappe import _
from frappe.utils.file_manager import save_file


def _parse_date(date_str: Optional[str]) -> Optional[str]:
    """Parse common date formats to YYYY-MM-DD string for DocType fields."""
    if not date_str:
        return None
    # Try common formats
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except Exception:
            continue
    # Fallback: let Frappe handle invalid format gracefully by returning original
    return date_str


def _ensure_supplier(supplier_name: str) -> str:
    """Return a Supplier name; create minimal supplier if not exists."""
    if not supplier_name:
        frappe.throw(_("Supplier is required"))

    existing = frappe.db.get_value("Supplier", {"supplier_name": supplier_name})
    if existing:
        return existing

    # Create a new supplier with minimal fields
    supplier = frappe.get_doc({
        "doctype": "Supplier",
        "supplier_name": supplier_name,
        "supplier_group": "All Supplier Groups",
        "supplier_type": "Company",
    })
    supplier.insert(ignore_permissions=True)
    return supplier.name


def _build_pi_items(items: List[Dict[str, Any]], isReturn: bool = False) -> List[Dict[str, Any]]:
    built: List[Dict[str, Any]] = []
    for idx, item in enumerate(items or []):
        qty = item.get("qty") or item.get("salesQty") or 0
        rate = item.get("rate") or item.get("unitPrice")
        amount = item.get("amount") or item.get("lineTotal")
        uom = item.get("uom") or item.get("UOM")
        # Normalize common cases UOM labels
        if isinstance(uom, str):
            u = uom.strip().lower()
            if "case" in u or u == "cs":
                uom = "CS"
            elif u in ("nos", "no", "number", "pc", "pcs"):
                uom = "Nos"
        
        # Use materialCode for item_code and materialDescription for item_name
        item_code = item.get("materialCode") or item.get("item_code") or ""
        item_name_from_master = frappe.get_value("Item", item_code, "item_name")
        item_name =item_name_from_master or  item.get("materialDescription") or item.get("item_name") or item_code
        
        # For returns, make quantities and amounts negative in the backend
        # This ensures proper accounting while keeping frontend quantities positive
        if isReturn:
            qty = -abs(qty)  # Make negative but preserve absolute value
            if amount is not None:
                amount = -abs(amount)  # Make negative but preserve absolute value
        
        built.append({
            "doctype": "Purchase Invoice Item",
            "item_code": item_code,  # Use materialCode as item_code
            "item_name": item_name,  # Use materialDescription as item_name
            "qty": qty,
            **({"uom": uom} if uom else {}),
            **({"rate": rate} if rate is not None else {}),
            **({"amount": amount} if amount is not None else {}),
            # Custom fields
            **({"cust_leakage_qty": int(item.get("cust_leakage_qty") or item.get("leakages") or 0)}),
            **({"cust_burst_qty": int(item.get("cust_burst_qty") or item.get("bursts") or 0)}),
        })
    return built


def _attach_photo(docname: str, photo_base64: Optional[str], filename: str = "invoice_photo.jpg") -> Optional[str]:
    if not photo_base64:
        return None

    # Accept both full data URLs and raw base64
    if photo_base64.startswith("data:"):
        try:
            header, b64data = photo_base64.split(",", 1)
        except ValueError:
            b64data = photo_base64
    else:
        b64data = photo_base64

    try:
        content = base64.b64decode(b64data)
    except Exception:
        frappe.throw(_("Invalid photo data provided"))

    filedoc = save_file(
        filename,
        content,
        "Purchase Invoice",
        docname,
        is_private=1,
    )
    return getattr(filedoc, "file_url", None)


@frappe.whitelist()
def create_purchase_invoice(payload: Dict[str, Any] | str = None) -> Dict[str, Any]:
    """
    Create a draft Purchase Invoice from structured payload.

    Expected payload structure (keys are case-sensitive):
    {
      "supplier": "Supplier Name",                 # optional if supplier_name is provided
      "supplier_name": "Supplier Name",            # used when supplier is not system name
      "bill_no": "INV-001",
      "bill_date": "2025-08-10",
      "posting_date": "2025-08-10",                # optional
      "discount_amount": 0,                          # optional
      "cust_bill_actual_amount": 1234.56,            # custom field on Purchase Invoice
      "items": [
         {"item_code": "ITEM-001", "item_name": "Item 1", "qty": 2, "rate": 10, "amount": 20,
          "cust_leakage_qty": 1, "cust_burst_qty": 0},
          ...
      ],
      "photo_base64": "data:image/png;base64,...",  # optional attachment
      "photo_filename": "invoice.png"               # optional
    }
    """
    try:
        # Parse payload string if needed
        if isinstance(payload, str):
            import json
            payload = json.loads(payload)
        if not payload:
            frappe.throw(_("Payload is required"))

        supplier_input = payload.get("supplier") or payload.get("supplier_name") or payload.get("customerName")
        supplier_name = _ensure_supplier(supplier_input)

        bill_no = payload.get("bill_no") or payload.get("invoiceNumber")
        bill_date = _parse_date(payload.get("bill_date") or payload.get("invoiceDate"))
        # Force posting_date to equal bill/invoice date per requirement

        # Build the Purchase Invoice document
        isReturn = payload.get("isReturn", False)
        
        # For returns, make discount amount negative in the backend
        discount_amount = payload.get("discount_amount")
        if isReturn and discount_amount is not None:
            discount_amount = -abs(discount_amount)  # Make negative but preserve absolute value
        
        doc = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": supplier_name,
            "update_stock": 1,
            "set_posting_time": 1,
            "is_return": isReturn,  # Set the return flag for Credit Notes
            **({"bill_no": bill_no} if bill_no else {}),
            **({"bill_date": bill_date} if bill_date else {}),
            **({"posting_date": bill_date} if bill_date else {}),
            **({"discount_amount": discount_amount} if discount_amount is not None else {}),
            **({"cust_bill_actual_amount": payload.get("cust_bill_actual_amount")} if payload.get("cust_bill_actual_amount") is not None else {}),
            # Set default Taxes and Charges template
            # "taxes_and_charges": "Nepal Tax - RTAS",
        })

        # Add items
        for item in _build_pi_items(payload.get("items") or [], payload.get("isReturn", False)):
            doc.append("items", item)

        # Ensure sane defaults to avoid math on NoneType in overrides
        for it in doc.items:
            if getattr(it, "qty", None) is None:
                it.qty = 0
            if not getattr(it, "uom", None):
                it.uom = "Nos"

        # Load taxes from template BEFORE inserting the document
        try:
            doc.append("taxes", {
                "charge_type": "On Net Total",
                "account_head": "VAT - RTAS",
                "rate": 13,
                "description": "VAT 13%",
            })
        except Exception:
            # Never fail on taxes append
            frappe.log_error(frappe.get_traceback(), "Failed to append VAT row on PI")

        # Run validations and calculations once, then insert as draft
        doc.insert()

        # Attach photo if provided
        file_url = None
        if payload.get("photo_base64"):
            try:
                file_url = _attach_photo(doc.name, payload.get("photo_base64"), payload.get("photo_filename") or "invoice_photo.jpg")
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Attach photo failed in create_purchase_invoice")

        return {
            "success": True,
            "name": doc.name,
            "file_url": file_url,
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_purchase_invoice failed")
        # Always return JSON error (not HTML) to frontend
        return {"success": False, "error": str(e)}


def _load_gemini_api_key() -> Optional[str]:
    # Prefer site_config, fallback to env var
    try:
        conf = frappe.get_conf()
        key = conf.get("google_generative_ai_api_key")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")


def _coerce_invoice_type(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = str(s).strip().lower()
    if s.startswith("p"):
        return "purchase"
    if s.startswith("s"):
        return "sales"
    return None


@frappe.whitelist()
def extract_invoice(image_data: Optional[str] = None, file_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract structured invoice data using Google Generative Language API (Gemini) server-side.
    Provide either `image_data` (data URL or base64) or an already uploaded `file_url`.

    Returns: { success: True, data: InvoiceData, invoiceType: 'purchase'|'sales' } on success.
    """
    api_key = _load_gemini_api_key()
    if not api_key:
        return {"success": False, "error": "Gemini API key not configured. Set google_generative_ai_api_key in site_config.json or GOOGLE_GENERATIVE_AI_API_KEY env."}

    # Accept data URL or raw base64
    if image_data:
        if image_data.startswith("data:"):
            try:
                header, data_part = image_data.split(",", 1)
            except ValueError:
                return {"success": False, "error": "Invalid data URL provided"}
            mime = header.split(";")[0].replace("data:", "") or "image/jpeg"
            b64 = data_part
        else:
            # Default assume jpeg
            mime = "image/jpeg"
            b64 = image_data
    elif file_url:
        # Read file content and base64 encode
        try:
            # File may be private; use Frappe file API to read
            file_doc = frappe.get_doc("File", {"file_url": file_url})
            content = file_doc.get_content()
            b64 = _b64.b64encode(content).decode()
            # Guess mime from extension
            if str(file_url).lower().endswith(".png"):
                mime = "image/png"
            elif str(file_url).lower().endswith(".webp"):
                mime = "image/webp"
            else:
                mime = "image/jpeg"
        except Exception:
            # Fallback: try HTTP fetch if not a File doc url
            try:
                resp = requests.get(file_url, timeout=15)
                resp.raise_for_status()
                content = resp.content
                b64 = _b64.b64encode(content).decode()
                mime = resp.headers.get("Content-Type", "image/jpeg")
            except Exception as e:
                return {"success": False, "error": f"Failed to fetch file: {e}"}
    else:
        return {"success": False, "error": "Provide image_data or file_url"}

    # Build prompt and call Gemini (v1beta generateContent)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    params = {"key": api_key}
    system_prompt = (
        "You will receive an image of a supplier invoice (often Purchase Invoice). "
        "Extract JSON with these keys only: "
        "title (string - the main document title like 'TAX INVOICE' or 'CREDIT NOTE'), "
        "invoiceNumber (string), invoiceDate (string), customerName (string), "
        "items (array of { materialCode (string), materialDescription (string), salesQty (number), uom (string), unitPrice (number, optional), lineTotal (number, optional) }), "
        "totalAmount (number), totalDiscountAmount (number), discountQty (number), invoiceType ('purchase'|'sales'). "
        "CRITICAL INSTRUCTIONS: "
        "1. EXTRACT THE DOCUMENT TITLE: Look for the main title at the top/center of the document. This will be 'TAX INVOICE' or 'CREDIT NOTE' or similar. This is crucial for determining the invoice type. "
        "2. Material descriptions may span multiple lines. When you see text like '500MLPLASN1X12 KINLEY CLUB SODA' on one line and 'ASSP 75' on the next line, "
        "this is ONE SINGLE PRODUCT with description '500MLPLASN1X12 KINLEY CLUB SODA ASSP 75'. Do NOT create separate items for multi-line descriptions. "
        "3. For each item, extract BOTH materialCode (the actual item code/sku) AND materialDescription (the human-readable description). These are DIFFERENT fields. "
        "4. totalDiscountAmount must be extracted STRICTLY from the 'Amount' column of the row labeled 'Discount' - NOT from the quantity column. "
        "5. discountQty should be extracted from the 'Qty' column of the 'Discount' row if present. "
        "Guidance: Quantities are in cases (cs). The billed Actual Total equals the second last row labeled 'Total', just above 'Amount in Words'. "
        "Suppliers are typically 'bntl'. Use 0 if a numeric field is not present. Only output JSON (no extra text)."
    )

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": system_prompt},
                    {"inline_data": {"mime_type": mime, "data": b64}},
                ],
            }
        ],
        "generationConfig": {"response_mime_type": "application/json"},
    }

    try:
        resp = requests.post(url, params=params, data=_json.dumps(body), headers={"Content-Type": "application/json"}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Parse JSON text from model output
        text = None
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass
        if not text:
            return {"success": False, "error": "No extraction text received from model"}

        try:
            obj = _json.loads(text)
        except Exception:
            # Attempt to strip code fences if present
            text2 = text.strip().strip("` ")
            obj = _json.loads(text2)

        # Coerce and validate
        inv_type = _coerce_invoice_type(obj.get("invoiceType"))
        obj["invoiceType"] = inv_type or obj.get("invoiceType")
        if not isinstance(obj.get("items"), list):
            obj["items"] = []
        # Make sure numeric fields are numbers
        try:
            if obj.get("totalAmount") is not None:
                obj["totalAmount"] = float(obj["totalAmount"])
        except Exception:
            obj["totalAmount"] = 0.0
        try:
            if obj.get("totalDiscountAmount") is not None:
                obj["totalDiscountAmount"] = float(obj["totalDiscountAmount"])
        except Exception:
            obj["totalDiscountAmount"] = 0.0
        # try:
        #     if obj.get("discountQty") is not None:
        #         obj["discountQty"] = float(obj["discountQty"])
        # except Exception:
        #     obj["discountQty"] = 0.0
        for it in obj["items"]:
            if isinstance(it, dict) and it.get("salesQty") is not None:
                try:
                    it["salesQty"] = float(it["salesQty"])
                except Exception:
                    it["salesQty"] = 0
            # Normalize UOM
            u = (it.get("uom") or it.get("UOM") or "").strip().lower()
            if u:
                if "case" in u or u == "cs":
                    it["uom"] = "CS"
                elif u in ("nos", "no", "number", "pc", "pcs"):
                    it["uom"] = "Nos"
                else:
                    it["uom"] = it.get("uom") or it.get("UOM")

        return {"success": True, "data": obj, "invoiceType": obj.get("invoiceType")}
    except requests.HTTPError as e:
        return {"success": False, "error": f"Gemini HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Gemini error: {str(e)}"}


def _create_new_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new item in the master data with proper UOM conversion and price list.
    
    Args:
        item_data: Dictionary containing item_code, item_name, selling_price, valuation_price, uom_conversion
        
    Returns:
        Dict with success status and item details
    """
    try:
        item_code = item_data.get("item_code", "").strip()
        item_name = item_data.get("item_name", "").strip()
        selling_price = float(item_data.get("selling_price", 0))
        valuation_price = float(item_data.get("valuation_price", 0))
        uom_conversion = int(item_data.get("uom_conversion", 1))
        
        if not item_code or not item_name:
            return {"success": False, "error": "Item code and name are required"}
        
        # Check if item already exists
        if frappe.db.exists("Item", item_code):
            return {"success": False, "error": f"Item with code '{item_code}' already exists"}
        
        # Create the new item
        item_doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_name,
            "item_group": "Consumable",
            "default_unit_of_measure": "Nos",
            "maintain_stock": 1,
            "valuation_rate": valuation_price,
            "standard_rate": selling_price,
            "is_stock_item": 1,
            "is_purchase_item": 1,
            "is_sales_item": 1,
        })
        
        item_doc.insert(ignore_permissions=True)
        
        # Add UOM conversion for CS (Case)
        if uom_conversion > 1:
            uom_doc = frappe.get_doc({
                "doctype": "UOM Conversion Detail",
                "parent": item_code,
                "parenttype": "Item",
                "parentfield": "uoms",
                "uom": "CS",
                "conversion_factor": uom_conversion,
            })
            uom_doc.insert(ignore_permissions=True)
        
        # Add buying price to price list
        try:
            price_list_name = "Standard Buying"
            if not frappe.db.exists("Price List", price_list_name):
                # Create price list if it doesn't exist
                price_list_doc = frappe.get_doc({
                    "doctype": "Price List",
                    "price_list_name": price_list_name,
                    "currency": frappe.defaults.get_global_default("currency"),
                    "buying": 1,
                    "selling": 0,
                })
                price_list_doc.insert(ignore_permissions=True)
            
            # Add item price
            item_price_doc = frappe.get_doc({
                "doctype": "Item Price",
                "price_list": price_list_name,
                "item_code": item_code,
                "price_list_rate": valuation_price,
                "uom": "Nos",
            })
            item_price_doc.insert(ignore_permissions=True)
            
        except Exception as e:
            frappe.log_error(f"Failed to add price list entry for {item_code}: {str(e)}", "Item Price Creation")
        
        frappe.logger().info(f"Successfully created new item: {item_code} with UOM conversion CS={uom_conversion}")
        
        return {
            "success": True,
            "item_code": item_code,
            "item_name": item_name,
            "message": f"Item '{item_code}' created successfully"
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Failed to create new item: {str(e)}")
        return {"success": False, "error": f"Failed to create item: {str(e)}"}


def _validate_items_in_master(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate if all items exist in the master data.
    
    Returns:
        Dict with validation results and list of missing items
    """
    missing_items = []
    valid_items = []
    
    for item in items:
        item_code = item.get("materialCode") or item.get("item_code") or ""
        if item_code and not frappe.db.exists("Item", item_code):
            missing_items.append({
                "materialCode": item_code,
                "materialDescription": item.get("materialDescription") or item.get("item_name") or item_code,
                "salesQty": item.get("salesQty") or 0,
                "uom": item.get("uom") or "CS",
                "unitPrice": item.get("unitPrice") or 0,
                "lineTotal": item.get("lineTotal") or 0,
            })
        else:
            valid_items.append(item)
    
    return {
        "all_valid": len(missing_items) == 0,
        "missing_items": missing_items,
        "valid_items": valid_items
    }


@frappe.whitelist()
def validate_items_master(items=None) -> Dict[str, Any]:
    """
    Validate items before creating purchase invoice (new function name).
    
    Args:
        items: List of items to validate (can be string or list)
        
    Returns:
        Validation results with missing items list
    """
    try:
        # Debug: Log what we received
        frappe.logger().info(f"validate_items_master called with items: {items}")
        frappe.logger().info(f"Items type: {type(items)}")
        
        # Handle the case where items might be passed as a string in the request body
        if isinstance(items, str) and items.startswith('{'):
            import json
            try:
                # Try to parse as JSON first
                parsed = json.loads(items)
                if 'items' in parsed:
                    items = parsed['items']
                    frappe.logger().info("Extracted items from JSON wrapper")
            except json.JSONDecodeError:
                pass
        
        if not items:
            frappe.logger().error("No items parameter provided")
            return {"success": False, "error": "Items parameter is required"}
        
        # Handle both string and list inputs
        if isinstance(items, str):
            import json
            try:
                items = json.loads(items)
                frappe.logger().info(f"Parsed JSON string to list with {len(items)} items")
            except json.JSONDecodeError as e:
                frappe.logger().error(f"JSON decode error: {e}")
                return {"success": False, "error": "Invalid JSON in items parameter"}
        
        if not isinstance(items, list):
            frappe.logger().error(f"Items is not a list: {type(items)}")
            return {"success": False, "error": "Items must be a list"}
        
        frappe.logger().info(f"Validating {len(items)} items")
        validation_result = _validate_items_in_master(items)
        return {
            "success": True,
            "validation": validation_result
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "validate_items_master failed")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def validate_purchase_invoice_items(items=None) -> Dict[str, Any]:
    """
    Validate items before creating purchase invoice.
    
    Args:
        items: List of items to validate (can be string or list)
        
    Returns:
        Validation results with missing items list
    """
    try:
        # Debug: Log what we received
        frappe.logger().info(f"validate_purchase_invoice_items called with items: {items}")
        frappe.logger().info(f"Items type: {type(items)}")
        
        # Handle the case where items might be passed as a string in the request body
        if isinstance(items, str) and items.startswith('{'):
            import json
            try:
                # Try to parse as JSON first
                parsed = json.loads(items)
                if 'items' in parsed:
                    items = parsed['items']
                    frappe.logger().info("Extracted items from JSON wrapper")
            except json.JSONDecodeError:
                pass
        
        if not items:
            frappe.logger().error("No items parameter provided")
            return {"success": False, "error": "Items parameter is required"}
        
        # Handle both string and list inputs
        if isinstance(items, str):
            import json
            try:
                items = json.loads(items)
                frappe.logger().info(f"Parsed JSON string to list with {len(items)} items")
            except json.JSONDecodeError as e:
                frappe.logger().error(f"JSON decode error: {e}")
                return {"success": False, "error": "Invalid JSON in items parameter"}
        
        if not isinstance(items, list):
            frappe.logger().error(f"Items is not a list: {type(items)}")
            return {"success": False, "error": "Items must be a list"}
        
        frappe.logger().info(f"Validating {len(items)} items")
        validation_result = _validate_items_in_master(items)
        return {
            "success": True,
            "validation": validation_result
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "validate_purchase_invoice_items failed")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_new_item_for_invoice(item_data=None) -> Dict[str, Any]:
    """
    Create a new item for purchase invoice.
    
    Args:
        item_data: Item data (can be string or dict)
        
    Returns:
        Creation result
    """
    try:
        # Debug: Log what we received
        frappe.logger().info(f"create_new_item_for_invoice called with item_data: {item_data}")
        frappe.logger().info(f"Item data type: {type(item_data)}")
        
        if not item_data:
            frappe.logger().error("No item_data parameter provided")
            return {"success": False, "error": "Item data parameter is required"}
        
        # Handle both string and dict inputs
        if isinstance(item_data, str):
            import json
            try:
                item_data_dict = json.loads(item_data)
                frappe.logger().info("Parsed JSON string to dict")
            except json.JSONDecodeError as e:
                frappe.logger().error(f"JSON decode error: {e}")
                return {"success": False, "error": "Invalid JSON in item_data parameter"}
        else:
            item_data_dict = item_data
            
        if not isinstance(item_data_dict, dict):
            frappe.logger().error(f"Item data is not a dict: {type(item_data_dict)}")
            return {"success": False, "error": "Item data must be a dictionary"}
            
        result = _create_new_item(item_data_dict)
        return result
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_new_item_for_invoice failed")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def check_duplicate_invoice(supplier=None, invoice_number=None, invoice_date=None, invoice_type=None) -> Dict[str, Any]:
    """
    Check if an invoice with the same supplier, invoice number, and date already exists.
    
    Args:
        supplier: Supplier name
        invoice_number: Invoice number
        invoice_date: Invoice date
        invoice_type: Type of invoice (purchase/sales)
        
    Returns:
        Duplicate check result
    """
    try:
        if not supplier or not invoice_number or not invoice_date:
            return {"success": False, "error": "Supplier, invoice number, and date are required"}
        
        # Parse the date to ensure consistency
        parsed_date = _parse_date(invoice_date)
        if not parsed_date:
            return {"success": False, "error": "Invalid date format"}
        
        # Check for existing invoice
        doctype = "Purchase Invoice" if invoice_type == "purchase" else "Sales Invoice"
        
        existing_invoice = frappe.db.get_value(
            doctype,
            {
                "supplier": supplier,
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
        frappe.log_error(frappe.get_traceback(), "check_duplicate_invoice failed")
        return {"success": False, "error": str(e)}


