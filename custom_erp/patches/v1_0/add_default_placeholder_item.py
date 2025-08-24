import frappe


def execute():
    """Create a Selling Settings custom field `default_placeholder_item`,
    ensure a non-stock Item named 'Opening Invoice Item' exists, and set the
    setting to that item if empty.
    """

    # 1) Ensure Custom Field exists on Selling Settings
    if not frappe.db.exists(
        "Custom Field", {"dt": "Selling Settings", "fieldname": "default_placeholder_item"}
    ):
        frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Selling Settings",
                "label": "Default Placeholder Item",
                "fieldname": "default_placeholder_item",
                "fieldtype": "Link",
                "options": "Item",
                "insert_after": "territory",
            }
        ).insert(ignore_permissions=True)

    # 2) Ensure placeholder Item exists
    item_code = "Opening Invoice Item"
    if not frappe.db.exists("Item", {"item_code": item_code}):
        item_doc = frappe.get_doc(
            {
                "doctype": "Item",
                "item_code": item_code,
                "item_name": item_code,
                "is_stock_item": 0,
                "is_sales_item": 1,
                "stock_uom": "Nos",
                "disabled": 0,
            }
        ).insert(ignore_permissions=True)
    else:
        item_doc = frappe.get_last_doc("Item", {"item_code": item_code})

    # 3) Set Selling Settings value if empty
    ss = frappe.get_single("Selling Settings")
    if not ss.get("default_placeholder_item"):
        # Link fields store the document name, not necessarily the item_code
        item_name = item_doc.name
        ss.default_placeholder_item = item_name
        ss.save()
    frappe.db.commit()


