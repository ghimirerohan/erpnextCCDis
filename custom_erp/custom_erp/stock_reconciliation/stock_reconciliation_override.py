from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import StockReconciliation


class StockReconciliationOverride(StockReconciliation):
    def validate(self):
        """Override validate to handle UOM conversion and serial/batch bundle validation"""
        print("=== CUSTOM STOCK RECONCILIATION VALIDATE CALLED ===")
        print(f"Document: {self.name or 'New'}, Items count: {len(self.items) if self.items else 0}")
        
        # Handle UOM conversion for new documents
        if self.is_new():
            for item in self.items:
                item_name_from_master = frappe.get_value("Item", item.item_code, "item_name")
                item_master = frappe.get_doc("Item", item.item_code)

                entered_uom = getattr(item, "entered_uom", None)
                stock_uom = getattr(item, "stock_uom", None)

                # If user entered a different UOM than stock UOM, convert qty to stock UOM
                if entered_uom and stock_uom and entered_uom != stock_uom:
                    conversion_factor = frappe.get_value(
                        "UOM Conversion Detail",
                        {"parent": item.item_code, "uom": entered_uom},
                        "conversion_factor",
                    )
                    if conversion_factor:
                        # Special handling for Cases -> Nos with compound quantity like C.S
                        if entered_uom == "CS" and stock_uom == "Nos":
                            before, after = split_decimal_parts(item.qty)
                            if after >= conversion_factor:
                                before += after // conversion_factor
                                after = after % conversion_factor
                            item.qty = before * conversion_factor + after
                        else:
                            item.qty = flt(item.qty) * flt(conversion_factor)

        # Clear any empty serial/batch bundle fields to avoid validation errors
        if self.items:
            for item in self.items:
                if not item.serial_and_batch_bundle:
                    item.serial_and_batch_bundle = None
                if not item.current_serial_and_batch_bundle:
                    item.current_serial_and_batch_bundle = None
                if not item.batch_no:
                    item.batch_no = None
        
        # Call the parent's validate method
        super().validate()
