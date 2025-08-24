from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
import frappe


def before_insert(doc, method=None):
    print("Custom before_insert method for Sales Invoice")

    # Skip any mutation for Opening Balance invoices created via Opening Invoice Tool
    # These carry only item_name (no item_code) and should not be altered
    if getattr(doc, "is_opening", None) == "Yes":
        return

    totalDiscountAmt = 0
    for item in doc.items:
        # Opening invoices or manual entries may not have item_code; guard against it
        if not getattr(item, "item_code", None):
            continue

        item_master = frappe.get_doc("Item", item.item_code)
        item.price_list_rate = item_master.standard_rate
        item.rate = item_master.standard_rate
        item.item_code = item_master.item_code
        if item.distributed_discount_amount > 0:
            totalDiscountAmt += item.distributed_discount_amount
        if item.uom != "Nos":
            conversion_factor = frappe.get_value(
                "UOM Conversion Detail", {"parent": item.item_code, "uom": item.uom}, "conversion_factor"
            )
            before, after = split_decimal_parts(item.qty)
            totalQTYinNos = before * conversion_factor + after
            item.uom = "Nos"
            item.qty = totalQTYinNos
        if doc.is_return:
            item.qty = -1 * item.qty

    if totalDiscountAmt > 0:
        if doc.is_return:
            doc.discount_amount = totalDiscountAmt * -1
        else:
            doc.discount_amount = totalDiscountAmt
        doc.apply_discount_on = "Net Total"
        doc.additional_discount_account = "Discount Allowed - RTAS"
    doc.validate()