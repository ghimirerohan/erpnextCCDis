import frappe
from frappe.utils import flt


class OpeningInvoiceCreationToolOverride(
    frappe.get_attr(
        "erpnext.accounts.doctype.opening_invoice_creation_tool.opening_invoice_creation_tool.OpeningInvoiceCreationTool"
    )
):
    """Override that
    - normalizes numeric fields coming from CSV/bulk edit (commas, symbols),
    - auto-fills a default placeholder item name when item fields are blank,
    - and ensures party auto-creation uses sensible defaults.
    """

    def set_missing_values(self, row):  # type: ignore[override]
        super().set_missing_values(row)

        # normalize outstanding_amount and qty (strip commas, currency text)
        if row.get("outstanding_amount") is not None:
            try:
                # support inputs like "Rs 55,880.00" or "55,880.00"
                amount_text = frappe.as_unicode(row.outstanding_amount)
                for token in ("Rs", "रु", "NPR", "INR", "USD", "रु."):
                    amount_text = amount_text.replace(token, "")
                row.outstanding_amount = flt(amount_text)
            except Exception:
                row.outstanding_amount = flt(row.outstanding_amount)

        row.qty = flt(row.get("qty") or 1) or 1

        # default placeholder item name from Selling Settings if present
        default_item = frappe.db.get_single_value(
            "Selling Settings", "default_placeholder_item"
        )
        if default_item:
            if not row.get("item_name"):
                # keep UI friendly name but ensure description/rate computed later
                row.item_name = frappe.db.get_value("Item", default_item, "item_name") or default_item

    def add_party(self, party_type, party):  # type: ignore[override]
        """Extend party auto-creation to set required defaults.
        If required master defaults are missing, raise a helpful error.
        """
        if party_type == "Customer":
            # Ensure customer group and territory defaults are set
            customer_group = frappe.db.get_single_value("Selling Settings", "customer_group")
            territory = frappe.db.get_single_value("Selling Settings", "territory")
            if not customer_group:
                # attempt to fall back to "All Customer Groups"
                cg = frappe.db.get_value("Customer Group", {"is_group": 1, "name": "All Customer Groups"})
                if not cg:
                    names = frappe.db.get_all("Customer Group", pluck="name", limit=1)
                    cg = names[0] if names else None
                customer_group = cg

            if not territory:
                tr = frappe.db.get_value("Territory", {"is_group": 1, "name": "All Territories"})
                if not tr:
                    names = frappe.db.get_all("Territory", pluck="name", limit=1)
                    tr = names[0] if names else None
                territory = tr

            doc = frappe.new_doc("Customer")
            doc.customer_name = party
            if customer_group:
                doc.customer_group = customer_group
            if territory:
                doc.territory = territory
            doc.flags.ignore_mandatory = True
            doc.insert(ignore_permissions=True)
            # ensure subsequent logic uses the actual document name
            try:
                if getattr(self, "_current_row", None):
                    self._current_row.party = doc.name
            except Exception:
                pass
        else:
            super().add_party(party_type, party)

    def validate_mandatory_invoice_fields(self, row):  # type: ignore[override]
        # stash a reference for add_party to update when naming by series
        self._current_row = row
        if not frappe.db.exists(row.party_type, row.party):
            if self.create_missing_party:
                self.add_party(row.party_type, row.party)
                # if still not found (naming by series), map by name field
                if not frappe.db.exists(row.party_type, row.party):
                    if row.party_type == "Customer":
                        mapped = frappe.db.get_value("Customer", {"customer_name": row.party}, "name")
                        if mapped:
                            row.party = mapped
                    elif row.party_type == "Supplier":
                        mapped = frappe.db.get_value("Supplier", {"supplier_name": row.party}, "name")
                        if mapped:
                            row.party = mapped
            else:
                frappe.throw(
                    "Row #{}: {} {} does not exist.".format(
                        row.idx, frappe.bold(row.party_type), frappe.bold(row.party)
                    )
                )

        for d in ("Party", "Outstanding Amount", "Temporary Opening Account"):
            if not row.get(frappe.scrub(d)):
                frappe.throw(
                    "Row #{0}: {1} is required to create the Opening {2} Invoices".format(
                        row.idx, d, self.invoice_type
                    )
                )


