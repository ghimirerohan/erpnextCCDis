from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
import frappe
from frappe.utils import flt


def before_save(doc, method=None):
    """Custom before_save method for Stock Reconciliation"""
    print("=== CUSTOM STOCK RECONCILIATION BEFORE_SAVE CALLED ===")
    print(f"Document: {doc.name or 'New'}, Items count: {len(doc.items) if doc.items else 0}")
    if doc.is_new():
        for item in doc.items:
            item_name_from_master = frappe.get_value("Item", item.item_code, "item_name")
            item_master = frappe.get_doc("Item", item.item_code)

            entered_uom = getattr(item, "entered_uom", None)
            stock_uom = getattr(item, "stock_uom", None)

            # # If user entered a different UOM than stock UOM, convert qty to stock UOM
            # if entered_uom and stock_uom and entered_uom != stock_uom:
            #     conversion_factor = frappe.get_value(
            #         "UOM Conversion Detail",
            #         {"parent": item.item_code, "uom": entered_uom},
            #         "conversion_factor",
            #     )
            #     if conversion_factor:
            #         # Special handling for Cases -> Nos with compound quantity like C.S
            #         if entered_uom == "CS" and stock_uom == "Nos":
            #             before, after = split_decimal_parts(item.qty)
            #             if after >= conversion_factor:
            #                 before += after // conversion_factor
            #                 after = after % conversion_factor
            #             item.qty = before * conversion_factor + after
            #         else:
            #             item.qty = flt(item.qty) * flt(conversion_factor)

            # Preserve existing behaviour if nothing entered explicitly but item is in Nos
            # if stock_uom == "Nos" and entered_uom == "CS":
            #     conversion_factor = frappe.get_value(
            #         "UOM Conversion Detail",
            #         {"parent": item.item_code, "uom": "CS"},
            #         "conversion_factor",
            #     )
            #     if conversion_factor:
            #         before, after = split_decimal_parts(item.qty)
            #         if after >= conversion_factor:
            #             before += after // conversion_factor
            #             after = after % conversion_factor
            #         item.qty = before * conversion_factor + after

        if doc.items:
            # Clear any empty serial/batch bundle fields to avoid validation errors
            for item in doc.items:
                if not item.serial_and_batch_bundle:
                    item.serial_and_batch_bundle = None
                if not item.current_serial_and_batch_bundle:
                    item.current_serial_and_batch_bundle = None
                if not item.batch_no:
                    item.batch_no = None
            
            doc.validate()