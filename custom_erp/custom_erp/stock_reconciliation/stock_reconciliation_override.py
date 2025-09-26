from custom_erp.custom_erp.utils.split_uom_cs_nos import split_decimal_parts
import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import StockReconciliation


class StockReconciliationOverride(StockReconciliation):
    # def validate(self):
    #     """Override validate to handle UOM conversion and serial/batch bundle validation"""
    #     print("=== CUSTOM STOCK RECONCILIATION VALIDATE CALLED ===")
    #     print(f"Document: {self.name or 'New'}, Items count: {len(self.items) if self.items else 0}")
        
    #     # Handle UOM conversion for new documents
    #     if self.is_new():
    #         for item in self.items:
    #             item_name_from_master = frappe.get_value("Item", item.item_code, "item_name")
    #             item_master = frappe.get_doc("Item", item.item_code)

    #             entered_uom = getattr(item, "entered_uom", None)
    #             stock_uom = getattr(item, "stock_uom", None)

    #             # If user entered a different UOM than stock UOM, convert qty to stock UOM
    #             if entered_uom and stock_uom and entered_uom != stock_uom:
    #                 conversion_factor = frappe.get_value(
    #                     "UOM Conversion Detail",
    #                     {"parent": item.item_code, "uom": entered_uom},
    #                     "conversion_factor",
    #                 )
    #                 if conversion_factor:
    #                     # Special handling for Cases -> Nos with compound quantity like C.S
    #                     if entered_uom == "CS" and stock_uom == "Nos":
    #                         before, after = split_decimal_parts(item.qty)
    #                         if after >= conversion_factor:
    #                             before += after // conversion_factor
    #                             after = after % conversion_factor
    #                         item.qty = before * conversion_factor + after
    #                     else:
    #                         item.qty = flt(item.qty) * flt(conversion_factor)

    #     # Clear any empty serial/batch bundle fields to avoid validation errors
    #     if self.items:
    #         for item in self.items:
    #             if not item.serial_and_batch_bundle:
    #                 item.serial_and_batch_bundle = None
    #             if not item.current_serial_and_batch_bundle:
    #                 item.current_serial_and_batch_bundle = None
    #             if not item.batch_no:
    #                 item.batch_no = None
        
    #     # Call the parent's validate method
    #     super().validate()

    def before_save(self):
        """Override before_save to handle additional UOM conversion logic"""
        print("=== CUSTOM STOCK RECONCILIATION BEFORE_SAVE CALLED ===")
        print(f"Document: {self.name or 'New'}, Items count: {len(self.items) if self.items else 0}")
        
        if self.is_new():
            for item in self.items:
                item_name_from_master = frappe.get_value("Item", item.item_code, "item_name")
                item_master = frappe.get_doc("Item", item.item_code)

                entered_uom = getattr(item, "entered_uom", None)
                stock_uom = getattr(item, "stock_uom", None)

                # # Preserve existing behaviour if nothing entered explicitly but item is in Nos
                # if stock_uom == "Nos":
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

            if self.items:
                # Clear any empty serial/batch bundle fields to avoid validation errors
                for item in self.items:
                    if not item.serial_and_batch_bundle:
                        item.serial_and_batch_bundle = None
                    if not item.current_serial_and_batch_bundle:
                        item.current_serial_and_batch_bundle = None
                    if not item.batch_no:
                        item.batch_no = None
                
                self.validate()

    def on_cancel(self):
        """Override on_cancel to prevent automatic repost item valuation while preserving core cancellation logic"""
        print("=== CUSTOM STOCK RECONCILIATION ON_CANCEL CALLED ===")
        print(f"Document: {self.name}, Cancelling without triggering repost item valuation")
        
        # Call core validation and cancellation logic from parent class
        # but override the repost method to prevent it from running
        
        # Store original repost method
        original_repost = getattr(self, 'repost_future_sle_and_gle', None)
        
        # Override repost method to do nothing
        def no_repost(*args, **kwargs):
            print("=== SKIPPING REPOST ITEM VALUATION AS REQUESTED ===")
            pass
        
        # Temporarily replace the repost method
        self.repost_future_sle_and_gle = no_repost
        
        try:
            # Call parent's on_cancel which handles all the core cancellation logic
            super().on_cancel()
            print("=== STOCK RECONCILIATION CANCELLED SUCCESSFULLY WITHOUT REPOST ===")
        except Exception as e:
            print(f"=== ERROR DURING CANCELLATION: {str(e)} ===")
            raise
        finally:
            # Restore original repost method (though it won't be needed after cancellation)
            if original_repost:
                self.repost_future_sle_and_gle = original_repost

    def make_gl_entries(self, gl_entries=None, from_repost=False, via_landed_cost_voucher=False):
        """Override make_gl_entries to ensure GL entries are always created for Stock Reconciliation"""
        print("=== CUSTOM STOCK RECONCILIATION MAKE_GL_ENTRIES CALLED ===")
        print(f"Document: {self.name}, Status: {self.docstatus}")
        print(f"Purpose: {getattr(self, 'purpose', 'Not set')}")
        print(f"Items count: {len(self.items) if self.items else 0}")
        
        if self.docstatus == 2:
            # Handle cancellation
            from erpnext.accounts.general_ledger import make_reverse_gl_entries
            make_reverse_gl_entries(voucher_type=self.doctype, voucher_no=self.name)
            return
        
        if self.docstatus != 1:
            print("Document not submitted, skipping GL entry creation")
            return
        
        # Always create GL entries for Stock Reconciliation regardless of other conditions
        print("=== FORCING GL ENTRY CREATION FOR STOCK RECONCILIATION ===")
        
        try:
            # Get warehouse account map
            from erpnext.stock import get_warehouse_account_map
            warehouse_account = get_warehouse_account_map(self.company)
            
            if not warehouse_account:
                print("❌ No warehouse accounts found. Cannot create GL entries.")
                return
            
            print(f"Warehouse Account Map: {warehouse_account}")
            
            # Always use manual GL entry creation for Stock Reconciliation
            print("Using manual GL entry creation for Stock Reconciliation...")
            gl_entries = self.create_manual_gl_entries(warehouse_account)
            
            if not gl_entries:
                print("❌ Manual GL entry creation failed. Cannot create GL entries.")
                return
            
            # Create GL entries directly in database
            self.create_gl_entries_directly(gl_entries)
            print("✅ GL entries created successfully!")
            
        except Exception as e:
            print(f"❌ Error creating GL entries: {str(e)}")
            import traceback
            traceback.print_exc()
            # Don't raise the exception to avoid breaking the submission process
            # Just log the error

    def create_manual_gl_entries(self, warehouse_account):
        """Create GL entries manually when standard method fails"""
        print("=== CREATING MANUAL GL ENTRIES ===")
        
        gl_entries = []
        total_debit = 0
        total_credit = 0
        
        # Check if this is an Opening Stock reconciliation
        if self.purpose == "Opening Stock":
            print("Creating GL entries for Opening Stock reconciliation based on document items")
            
            # Get items from the document
            if not self.items:
                print("No items found in document. Cannot create GL entries.")
                return []
            
            # Group items by warehouse
            warehouse_totals = {}
            for item in self.items:
                if item.warehouse not in warehouse_totals:
                    warehouse_totals[item.warehouse] = 0
                warehouse_totals[item.warehouse] += item.amount
            
            # Create GL entries for each warehouse
            for warehouse, amount in warehouse_totals.items():
                if warehouse in warehouse_account and amount != 0:
                    account = warehouse_account[warehouse]['account']
                    
                    # For opening stock, debit warehouse account
                    gl_entries.append(frappe._dict({
                        "account": account,
                        "debit": amount,
                        "credit": 0,
                        "cost_center": self.cost_center,
                        "posting_date": self.posting_date,
                        "posting_time": self.posting_time,
                        "voucher_type": "Stock Reconciliation",
                        "voucher_no": self.name,
                        "company": self.company
                    }))
                    total_debit += amount
            
            # Create offsetting entry for expense account
            if total_debit > 0:
                gl_entries.append(frappe._dict({
                    "account": self.expense_account,
                    "debit": 0,
                    "credit": total_debit,
                    "cost_center": self.cost_center,
                    "posting_date": self.posting_date,
                    "posting_time": self.posting_time,
                    "voucher_type": "Stock Reconciliation",
                    "voucher_no": self.name,
                    "company": self.company
                }))
                total_credit = total_debit
        
        else:
            # Regular stock reconciliation - use Stock Ledger Entries
            print("Creating GL entries for regular stock reconciliation based on Stock Ledger Entries")
            
            # Get stock ledger entries for this document
            sle_entries = frappe.db.sql("""
                SELECT item_code, warehouse, actual_qty, stock_value_difference, posting_date, posting_time
                FROM `tabStock Ledger Entry` 
                WHERE voucher_type = 'Stock Reconciliation' 
                AND voucher_no = %s
                ORDER BY item_code
            """, (self.name,), as_dict=True)
            
            print(f"Found {len(sle_entries)} Stock Ledger Entries")
            
            if not sle_entries:
                print("No Stock Ledger Entries found. Cannot create GL entries.")
                return []
            
            for sle in sle_entries:
                if sle.stock_value_difference != 0:
                    warehouse = sle.warehouse
                    if warehouse in warehouse_account:
                        account = warehouse_account[warehouse]['account']
                        
                        # Create GL entry for warehouse account
                        if sle.stock_value_difference > 0:
                            # Increase in stock value - debit warehouse account
                            gl_entries.append(frappe._dict({
                                "account": account,
                                "debit": sle.stock_value_difference,
                                "credit": 0,
                                "cost_center": self.cost_center,
                                "posting_date": sle.posting_date,
                                "posting_time": sle.posting_time,
                                "voucher_type": "Stock Reconciliation",
                                "voucher_no": self.name,
                                "company": self.company
                            }))
                            total_debit += sle.stock_value_difference
                        else:
                            # Decrease in stock value - credit warehouse account
                            gl_entries.append(frappe._dict({
                                "account": account,
                                "debit": 0,
                                "credit": abs(sle.stock_value_difference),
                                "cost_center": self.cost_center,
                                "posting_date": sle.posting_date,
                                "posting_time": sle.posting_time,
                                "voucher_type": "Stock Reconciliation",
                                "voucher_no": self.name,
                                "company": self.company
                            }))
                            total_credit += abs(sle.stock_value_difference)
            
            # Create offsetting entry for expense account
            if total_debit != total_credit:
                difference = total_debit - total_credit
                if difference > 0:
                    # More debit than credit - credit expense account
                    gl_entries.append(frappe._dict({
                        "account": self.expense_account,
                        "debit": 0,
                        "credit": difference,
                        "cost_center": self.cost_center,
                        "posting_date": self.posting_date,
                        "posting_time": self.posting_time,
                        "voucher_type": "Stock Reconciliation",
                        "voucher_no": self.name,
                        "company": self.company
                    }))
                else:
                    # More credit than debit - debit expense account
                    gl_entries.append(frappe._dict({
                        "account": self.expense_account,
                        "debit": abs(difference),
                        "credit": 0,
                        "cost_center": self.cost_center,
                        "posting_date": self.posting_date,
                        "posting_time": self.posting_time,
                        "voucher_type": "Stock Reconciliation",
                        "voucher_no": self.name,
                        "company": self.company
                    }))
        
        print(f"Created {len(gl_entries)} manual GL entries")
        print(f"Total Debit: {total_debit}")
        print(f"Total Credit: {total_credit}")
        
        return gl_entries

    def on_submit(self):
        """Override on_submit to ensure GL entries are created"""
        print("=== CUSTOM STOCK RECONCILIATION ON_SUBMIT CALLED ===")
        print(f"Document: {self.name}, Purpose: {getattr(self, 'purpose', 'Not set')}")
        
        # Call parent's on_submit first
        super().on_submit()
        
        # Ensure GL entries are created (our make_gl_entries override should handle this)
        print("=== ON_SUBMIT COMPLETED ===")

    def create_gl_entries_directly(self, gl_entries):
        """Create GL entries directly in the database"""
        print("=== CREATING GL ENTRIES DIRECTLY ===")
        
        for gl_entry in gl_entries:
            try:
                # Create GL Entry document
                gl_doc = frappe.get_doc({
                    "doctype": "GL Entry",
                    "account": gl_entry.account,
                    "debit": gl_entry.debit,
                    "credit": gl_entry.credit,
                    "cost_center": gl_entry.cost_center,
                    "posting_date": gl_entry.posting_date,
                    "posting_time": gl_entry.posting_time,
                    "voucher_type": gl_entry.voucher_type,
                    "voucher_no": gl_entry.voucher_no,
                    "company": gl_entry.company,
                    "is_cancelled": 0
                })
                
                gl_doc.insert(ignore_permissions=True)
                gl_doc.submit()
                print(f"Created GL Entry: {gl_entry.account} - Debit: {gl_entry.debit}, Credit: {gl_entry.credit}")
                
            except Exception as e:
                print(f"Error creating GL entry: {str(e)}")
                raise
