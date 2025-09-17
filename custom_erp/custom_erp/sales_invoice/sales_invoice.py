from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
import frappe

"""
Sales Invoice Custom Override

This module ensures that Sales Invoice items use standard_rate (selling price) 
instead of valuation_rate (purchase price) for the rate and base_rate fields.

IMPORTANT: The stock valuation hooks in stock_ledger_override.py have been modified
to NOT override rate and base_rate for Sales Invoice documents, preserving the
standard_rate values set here in before_insert.
"""


def _normalize_sales_invoice_items(doc):
    """Normalize Sales Invoice items so core validations pass consistently.

    - Set standard rate from Item master
    - Convert UOM to 'Nos' using conversion factor
    - Enforce quantity sign based on return flag (negative for returns)
    - Aggregate distributed discount to header discount_amount
    """
    # Skip any mutation for Opening Balance invoices created via Opening Invoice Tool
    # These carry only item_name (no item_code) and should not be altered
    if getattr(doc, "is_opening", None) == "Yes":
        return
    doc.ignore_pricing_rule = True
    totalDiscountAmt = 0
    for item in getattr(doc, "items", []):
        if not getattr(item, "item_code", None):
            continue

        item_master = frappe.get_doc("Item", item.item_code)
        item.price_list_rate = item_master.standard_rate
        item.rate = item_master.standard_rate
        item.base_rate = item_master.standard_rate
        item.item_code = item_master.item_code
        
        # Log the rate setting for debugging
        frappe.logger().info(f"Sales Invoice before_insert: Set rate={item.rate}, base_rate={item.base_rate}, standard_rate={item_master.standard_rate} for item {item.item_code}")

        if getattr(item, "distributed_discount_amount", 0) > 0:
            totalDiscountAmt += item.distributed_discount_amount

        # Handle UOM conversion to Nos if provided UOM differs
        if getattr(item, "uom", None) and item.uom != "Nos":
            conversion_factor = frappe.get_value(
                "UOM Conversion Detail", {"parent": item.item_code, "uom": item.uom}, "conversion_factor"
            )
            if conversion_factor is None:
                raise frappe.ValidationError(
                    f"No conversion rate found between '{item.uom}' and 'Nos' for item '{item.item_code}'. "
                    f"Please set up the UOM conversion in the Item master."
                )

            qty_for_conversion = abs(item.qty)
            before, after = split_decimal_parts(qty_for_conversion)
            totalQTYinNos = before * conversion_factor + after
            item.uom = "Nos"
            item.qty = totalQTYinNos
        elif not getattr(item, "uom", None) or item.uom == "":
            # If UOM is empty/None, assume it's already in Nos and set it explicitly
            print(f"Info: Item {item.item_code} has no UOM specified. Assuming UOM is 'Nos'.")
            item.uom = "Nos"
        if doc.is_return:
            item.qty = -1 * item.qty

    if totalDiscountAmt > 0:
        doc.discount_amount = -totalDiscountAmt if doc.is_return else totalDiscountAmt
        doc.apply_discount_on = "Net Total"
        doc.additional_discount_account = "Discount Allowed - RTAS"


# def before_validate(doc, method=None):
#     # Run early so ERPNext core validate_qty sees the corrected sign
#     _normalize_sales_invoice_items(doc)


def before_insert(doc, method=None):
    print("Custom before_insert method for Sales Invoice")
    _normalize_sales_invoice_items(doc)