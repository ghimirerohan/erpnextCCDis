from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice as ERPNextPurchaseInvoice
from erpnext.stock import get_warehouse_account_map
import frappe
from frappe.utils import add_months, flt
from erpnext.accounts.general_ledger import make_gl_entries

class PurchaseInvoiceOverride(ERPNextPurchaseInvoice):

    def validate(self):
        print("Custom validate method for Purchase Invoice")
        if(self.is_new()):
            for item in self.items:
                try:
                    item_master = frappe.get_doc("Item", item.item_code)
                    valuation_rate = getattr(item_master, "valuation_rate", 0) or 0
                    item_code = getattr(item_master, "item_code", item.item_code)
                except Exception:
                    # Item might not exist yet during draft creation; fall back safely
                    valuation_rate = frappe.get_value("Item", item.item_code, "valuation_rate") or 0
                    item_code = frappe.get_value("Item", item.item_code, "name") or item.item_code
                # Apply safe defaults without throwing
                item.price_list_rate = valuation_rate
                item.rate = valuation_rate
                item.net_rate = valuation_rate
                item.item_code = item_code
                # Normalize UOM
                if not getattr(item, "uom", None):
                    item.uom = "Nos"
                if item.uom != "Nos":
                    conversion_factor = frappe.get_value(
                        "UOM Conversion Detail",
                        {"parent": item.item_code, "uom": item.uom},
                        "conversion_factor",
                    ) or 1
                    before, after = split_decimal_parts(getattr(item, "qty", 0) or 0)
                    totalQTYinNos = before * conversion_factor + after
                    item.uom = "Nos"
                    item.qty = totalQTYinNos
            if not self.due_date:
                self.due_date = add_months(self.posting_date, 1)
        # Ensure discount account is set when discount is present (applies on submit too)
        if abs(self.discount_amount or 0) > 0:
            self.apply_discount_on = "Net Total"
            if not getattr(self, "custom_discount_account", None):
                self.custom_discount_account = "Discount Received - RTAS"
        # Call the parent validate method to run standard validations and calculations
        super().validate()
        # Guard bill_date when setting posting_date
        try:
            if getattr(self, "bill_date", None):
                self.posting_date = self.bill_date
        except Exception:
            pass
    

    def get_gl_entries(self, warehouse_account=None):
        """Return adjusted GL rows so preview reflects final posting:
        - Remove COGS stock-adjustment lines
        - Add back discount into Stock In Hand
        - Post discount to Discount Received account (credit on PI, debit on Return)
        """
        try:
            base_gl_entries = ERPNextPurchaseInvoice.get_gl_entries(self)
            return self._adjust_gl_entries(base_gl_entries)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "PI get_gl_entries override failed; falling back to core")
            return super().get_gl_entries(warehouse_account)
    
    
    def make_gl_entries(self, gl_entries=None, from_repost=False):
        """Post GL ensuring:
        - No COGS stock-adjustment lines
        - Inventory equals pre-discount total (discount added back to stock)
        - Discount posted to Discount Received account (and reversed on return)
        """
        try:
            adjusted_gl_entries = self.get_gl_entries()
            return super().make_gl_entries(gl_entries=adjusted_gl_entries, from_repost=from_repost)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "PI make_gl_entries override failed; falling back to core")
            return super().make_gl_entries(gl_entries=gl_entries, from_repost=from_repost)

    def on_submit(self):
        # Use standard submit flow; our GL adjustments are already applied in make_gl_entries
        super().on_submit()

    # ----------------------
    # Internal helpers
    # ----------------------
    def _adjust_gl_entries(self, base_gl_entries: list[dict]) -> list[dict]:
        """Adjust base GL rows to match business rules.

        - Remove COGS stock-adjustment rows posted by core
        - Bring Stock In Hand to pre-discount total
        - Post discount to Discount Received account with correct sign
        """
        gl_entries: list[dict] = list(base_gl_entries or [])

        # Identify inventory accounts in play for this invoice
        inventory_accounts = set()
        try:
            warehouse_account = get_warehouse_account_map(self.company)
        except Exception:
            warehouse_account = {}

        try:
            stock_items = set(self.get_stock_items())
        except Exception:
            stock_items = set()

        for item in self.items:
            if getattr(self, "update_stock", 0) and (
                (getattr(item, "item_code", None) in stock_items) or getattr(item, "is_fixed_asset", 0)
            ) and getattr(item, "warehouse", None):
                acc = (warehouse_account.get(item.warehouse, {}) or {}).get("account")
                if acc:
                    inventory_accounts.add(acc)

        # Remove COGS-style stock adjustment rows (small rounding differences)
        # Only when perpetual inventory is on and stock is updated
        if getattr(self, "update_stock", 0):
            try:
                default_expense_account = self.get_company_default("default_expense_account")
            except Exception:
                default_expense_account = None

            if default_expense_account:
                filtered = []
                for e in gl_entries:
                    remarks_text = (e.get("remarks") or "")
                    if (
                        e.get("account") == default_expense_account
                        and (abs(flt(e.get("debit", 0))) > 0 or abs(flt(e.get("credit", 0))) > 0)
                        and (e.get("against") in inventory_accounts or "Stock Adjustment" in remarks_text)
                    ):
                        # drop this stock-adjustment entry
                        continue
                    filtered.append(e)
                gl_entries = filtered

        # Compute stock add-back so inventory reflects pre-discount total
        stock_gl_entries = [e for e in gl_entries if e.get("account") in inventory_accounts]

        if stock_gl_entries:
            target_stock_amount_base = flt(self.total) * flt(self.conversion_rate or 1)
            current_stock_amount_base = sum(
                flt(e.get("debit", 0)) - flt(e.get("credit", 0)) for e in stock_gl_entries
            )
            delta_base = flt(target_stock_amount_base - current_stock_amount_base)

            if abs(delta_base) > 1e-6:
                # Distribute proportionally across existing stock entries (by absolute amounts)
                weights = [abs(flt(e.get("debit", 0)) - flt(e.get("credit", 0))) for e in stock_gl_entries]
                total_weight = sum(weights)
                for idx, e in enumerate(stock_gl_entries):
                    portion = (weights[idx] / total_weight) if total_weight > 1e-12 else (1.0 / len(stock_gl_entries))
                    portion_amount = delta_base * portion

                    if abs(portion_amount) < 1e-9:
                        continue

                    if portion_amount > 0:
                        gl_entries.append(
                            self.get_gl_dict(
                                {
                                    "account": e.get("account"),
                                    "against": self.supplier,
                                    "debit": portion_amount,
                                    "debit_in_transaction_currency": portion_amount / flt(self.conversion_rate or 1),
                                    "remarks": "Inventory add-back for discount/rounding",
                                    "cost_center": e.get("cost_center") or self.cost_center,
                                    "project": e.get("project") or self.project,
                                }
                            )
                        )
                    else:
                        credit_amount = abs(portion_amount)
                        gl_entries.append(
                            self.get_gl_dict(
                                {
                                    "account": e.get("account"),
                                    "against": self.supplier,
                                    "credit": credit_amount,
                                    "credit_in_transaction_currency": credit_amount / flt(self.conversion_rate or 1),
                                    "remarks": "Inventory add-back for discount/rounding",
                                    "cost_center": e.get("cost_center") or self.cost_center,
                                    "project": e.get("project") or self.project,
                                }
                            )
                        )

        # Ensure discount entry exists with proper sign
        discount_amount = flt(self.discount_amount or 0)
        base_discount_amount = flt(discount_amount * flt(self.conversion_rate or 1))
        discount_account = getattr(self, "custom_discount_account", None)

        if discount_account and abs(base_discount_amount) > 0:
            cost_center = getattr(self, "cost_center", None)
            if not cost_center:
                for it in self.items:
                    if getattr(it, "cost_center", None):
                        cost_center = it.cost_center
                        break

            # Fallback to company's default cost center if still not found
            if not cost_center:
                try:
                    cost_center = self.get_company_default("cost_center")
                except Exception:
                    cost_center = None

            if not cost_center:
                frappe.throw("Cost Center is required for Discount entry. Please set it in the Purchase Invoice or Company.")

            # Check if a discount row already exists
            has_discount = any(gle.get("account") == discount_account for gle in gl_entries)
            if not has_discount:
                if base_discount_amount > 0:
                    gl_entries.append(
                        self.get_gl_dict(
                            {
                                "account": discount_account,
                                "against": self.credit_to,
                                "credit": base_discount_amount,
                                "remarks": "Purchase Discount",
                                "cost_center": cost_center,
                            }
                        )
                    )
                elif base_discount_amount < 0:
                    gl_entries.append(
                        self.get_gl_dict(
                            {
                                "account": discount_account,
                                "against": self.credit_to,
                                "debit": abs(base_discount_amount),
                                "remarks": "Reversal of Purchase Discount (Return)",
                                "cost_center": cost_center,
                            }
                        )
                    )

        return gl_entries