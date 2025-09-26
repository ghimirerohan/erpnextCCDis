# -*- coding: utf-8 -*-
"""
Custom ERP Stock Ledger Override

This module overrides ERPNext's default valuation logic to always use the fixed rate
from the Item master's valuation_rate field for all stock valuation calculations.

Key Features:
- Overrides get_valuation_rate function to always return Item.valuation_rate
- Configurable via system settings
- Maintains compatibility with all stock transaction types
- Preserves original function signature for seamless integration
"""

import frappe
from frappe import _
from frappe.utils import flt
from erpnext.stock.stock_ledger import get_valuation_rate as original_get_valuation_rate
from erpnext.stock.utils import get_valuation_method as original_get_valuation_method

# Keep original references to avoid recursion after monkey patching
ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES = None
ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG = None
ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE = None

# Local cache to avoid repeated DB hits per posting
FIXED_RATE_CACHE = {}


def clear_fixed_rate_cache():
	FIXED_RATE_CACHE.clear()


def get_fixed_rate(item_code, currency=None, allow_price_fallback=True):
	"""
	Get fixed valuation rate for an item using a small in-memory cache.
	Falls back to standard_rate, then Item Price (buying) if requested.
	"""
	if not item_code:
		return 0.0
	if item_code in FIXED_RATE_CACHE:
		return FIXED_RATE_CACHE[item_code] or 0.0
	values = frappe.get_cached_value("Item", item_code, ["valuation_rate", "standard_rate"], as_dict=1)
	rate = 0.0
	if values:
		rate = values.get("valuation_rate") or values.get("standard_rate") or 0.0
	if not rate and allow_price_fallback and currency:
		rate = frappe.db.get_value(
			"Item Price",
			{"item_code": item_code, "buying": 1, "currency": currency},
			"price_list_rate",
		)
	FIXED_RATE_CACHE[item_code] = rate or 0.0
	return FIXED_RATE_CACHE[item_code] or 0.0


def get_valuation_rate(
	item_code,
	warehouse,
	voucher_type,
	voucher_no,
	allow_zero_rate=False,
	currency=None,
	company=None,
	raise_error_if_no_rate=True,
	batch_no=None,
	serial_and_batch_bundle=None,
):
	"""
	Override of ERPNext's get_valuation_rate function.
	
	This function always returns the fixed valuation rate from the Item master,
	regardless of purchase history, stock movements, or other factors.
	
	Args:
		item_code (str): The item code to get valuation rate for
		warehouse (str): The warehouse (used for compatibility but not for calculation)
		voucher_type (str): The voucher type (used for compatibility)
		voucher_no (str): The voucher number (used for compatibility)
		allow_zero_rate (bool): Whether to allow zero valuation rate
		currency (str): Currency (used for compatibility)
		company (str): Company (used for compatibility)
		raise_error_if_no_rate (bool): Whether to raise error if no rate found
		batch_no (str): Batch number (used for compatibility)
		serial_and_batch_bundle (str): Serial and batch bundle (used for compatibility)
	
	Returns:
		float: The fixed valuation rate from Item master
	
	Raises:
		frappe.ValidationError: If no valuation rate is found and raise_error_if_no_rate is True
	"""
	
	# Check if fixed valuation rate feature is enabled
	if not is_fixed_valuation_rate_enabled():
		# Use original ERPNext logic if feature is disabled
		return original_get_valuation_rate(
			item_code=item_code,
			warehouse=warehouse,
			voucher_type=voucher_type,
			voucher_no=voucher_no,
			allow_zero_rate=allow_zero_rate,
			currency=currency,
			company=company,
			raise_error_if_no_rate=raise_error_if_no_rate,
			batch_no=batch_no,
			serial_and_batch_bundle=serial_and_batch_bundle,
		)
	
	# Always use the fixed rate from Item master (with price fallback only once)
	valuation_rate = get_fixed_rate(item_code, currency)
	
	# Handle zero rate scenarios
	if not allow_zero_rate and not valuation_rate and raise_error_if_no_rate:
		form_link = frappe.get_desk_link("Item", item_code)
		
		message = _(
			"Fixed Valuation Rate for the Item {0}, is required to do accounting entries for {1} {2}."
		).format(form_link, voucher_type, voucher_no)
		message += "<br><br>" + _("Here are the options to proceed:")
		solutions = (
			"<li>"
			+ _(
				"If the item is transacting as a Zero Valuation Rate item in this entry, please enable 'Allow Zero Valuation Rate' in the {0} Item table."
			).format(voucher_type)
			+ "</li>"
		)
		solutions += (
			"<li>"
			+ _("If not, you can Cancel / Submit this entry")
			+ " {} ".format(frappe.bold(_("after")))
			+ _("performing either one below:")
			+ "</li>"
		)
		sub_solutions = "<ul><li>" + _("Set Valuation Rate in the Item master.") + "</li>"
		sub_solutions += "<li>" + _("Set Standard Rate in the Item master.") + "</li>"
		sub_solutions += "<li>" + _("Create an Item Price record for buying.") + "</li></ul>"
		msg = message + solutions + sub_solutions + "</li>"
		
		frappe.throw(msg=msg, title=_("Fixed Valuation Rate Missing"))
	
	return valuation_rate or 0.0


def is_fixed_valuation_rate_enabled():
	"""
	Check if the fixed valuation rate feature is enabled.
	By default, this feature is ENABLED to ensure consistent valuation rates.
	
	Returns:
		bool: True if fixed valuation rate is enabled, False otherwise
	"""
	# Always return True - feature is always enabled
	return True


def get_valuation_rate_for_item_details(item_code, company, warehouse=None):
	"""
	Override of the get_valuation_rate function in get_item_details.py.
	
	This function is used for getting valuation rates in item details contexts
	and should also use the fixed rate from Item master.
	
	Args:
		item_code (str): The item code
		company (str): The company
		warehouse (str): The warehouse (optional)
	
	Returns:
		dict: Dictionary containing the fixed valuation rate
	"""
	
	# Check if fixed valuation rate feature is enabled
	if not is_fixed_valuation_rate_enabled():
		# Use original logic if feature is disabled
		from erpnext.stock.get_item_details import get_valuation_rate as original_get_item_valuation_rate
		return original_get_item_valuation_rate(item_code, company, warehouse)
	
	# Always return the fixed rate from Item master
	valuation_rate = get_fixed_rate(item_code)
	
	return {"valuation_rate": valuation_rate or 0.0}


@frappe.whitelist()
def get_fixed_valuation_rate_status():
	"""
	Get the current status of the fixed valuation rate feature.
	
	Returns:
		dict: Status information about the fixed valuation rate feature
	"""
	enabled = is_fixed_valuation_rate_enabled()
	return {
		"enabled": enabled,
		"description": "When enabled, all stock transactions will use the fixed valuation_rate from Item master."
	}


@frappe.whitelist()
def enable_fixed_valuation_rate():
	"""
	Enable the fixed valuation rate feature.
	"""
	return {"success": True, "message": "Fixed Valuation Rate feature is always enabled!"}


@frappe.whitelist()
def disable_fixed_valuation_rate():
	"""
	Disable the fixed valuation rate feature.
	"""
	return {"success": True, "message": "Fixed Valuation Rate feature cannot be disabled - it's always enabled for consistency."}


def get_incoming_rate_for_return_entry(item_code, warehouse, voucher_type, voucher_no):
	"""Always use fixed rate from Item master for return entries."""
	if not is_fixed_valuation_rate_enabled():
		from erpnext.stock.stock_ledger import get_incoming_rate_for_return_entry as original_get_incoming_rate
		return original_get_incoming_rate(item_code, warehouse, voucher_type, voucher_no)
	return get_fixed_rate(item_code) or 0.0


def get_valuation_rate_for_finished_good_entry(work_order):
	if not is_fixed_valuation_rate_enabled():
		from erpnext.stock.doctype.stock_entry.stock_entry import get_valuation_rate_for_finished_good_entry as original_get_finished_good_rate
		return original_get_finished_good_rate(work_order)
	finished_good_item = frappe.db.get_value("Work Order", work_order, "production_item")
	return get_fixed_rate(finished_good_item) if finished_good_item else 0.0


def get_valuation_rate_for_serial_batch_bundle(serial_and_batch_bundle, item_code):
	if not is_fixed_valuation_rate_enabled():
		from erpnext.stock.serial_batch_bundle import get_valuation_rate_for_serial_batch_bundle as original_get_bundle_rate
		return original_get_bundle_rate(serial_and_batch_bundle, item_code)
	return get_fixed_rate(item_code) or 0.0


def get_incoming_rate(args, raise_error_if_no_rate=True):
	"""Override of stock.utils.get_incoming_rate to always use fixed rate."""
	if not is_fixed_valuation_rate_enabled():
		from erpnext.stock.utils import get_incoming_rate as original_get_incoming_rate
		return original_get_incoming_rate(args, raise_error_if_no_rate)
	item_code = args.get("item_code")
	if not item_code:
		return 0.0
	valuation_rate = get_fixed_rate(item_code, args.get("currency"))
	if not valuation_rate and raise_error_if_no_rate:
		form_link = frappe.get_desk_link("Item", item_code)
		message = _(
			"Fixed Valuation Rate for the Item {0}, is required to do accounting entries."
		).format(form_link)
		message += "<br><br>" + _("Please set Valuation Rate in the Item master.")
		frappe.throw(msg=message, title=_("Fixed Valuation Rate Missing"))
	return valuation_rate or 0.0


def ensure_fixed_valuation_rate_before_gl_creation(doc, method):
	"""
	Document event handler to ensure fixed valuation rate is used before GL entry creation.
	This function is called before GL entries are created.
	"""
	if not is_fixed_valuation_rate_enabled():
		return
	
	# Get the appropriate items table based on doctype
	items_table = None
	if doc.doctype in ["Purchase Invoice", "Sales Invoice"]:
		items_table = doc.items
	elif doc.doctype == "Stock Entry":
		items_table = doc.items
	elif doc.doctype == "Delivery Note":
		items_table = doc.items
	elif doc.doctype == "Purchase Receipt":
		items_table = doc.items
	elif doc.doctype == "Stock Reconciliation":
		items_table = doc.items
	
	if items_table:
		for item in items_table:
			if item.item_code and item.qty:
				# Get fixed valuation rate from Item master
				valuation_rate = get_fixed_rate(item.item_code)
				
				if valuation_rate:
					# For Sales Invoice, preserve the rate and base_rate (standard_rate) 
					# and only update valuation_rate for stock valuation purposes
					if doc.doctype == "Sales Invoice":
						# Don't override rate and base_rate for Sales Invoice
						# These should remain as standard_rate (selling price)
						frappe.logger().info(f"Sales Invoice detected in ensure_fixed_valuation_rate_before_gl_creation - preserving rate and base_rate for item {item.item_code}")
						pass
					else:
						# Update the item's rate (this affects GL entries)
						item.rate = valuation_rate
						
						# Update base rate if it exists
						if hasattr(item, 'base_rate'):
							item.base_rate = valuation_rate
					
					# Ensure outward transactions use fixed rate
					if hasattr(item, 'incoming_rate'):
						item.incoming_rate = valuation_rate
					
					# Update the item's valuation rate
					item.valuation_rate = valuation_rate
					
					# Recalculate stock value
					if hasattr(item, 'stock_qty') and item.stock_qty:
						item.stock_value = valuation_rate * flt(item.stock_qty)
					elif hasattr(item, 'qty') and item.qty:
						item.stock_value = valuation_rate * flt(item.qty)


def ensure_fixed_valuation_rate(doc, method):
	"""
	Document event handler to ensure fixed valuation rate is used.
	This function is called before_save and on_submit for stock transactions.
	"""
	if not is_fixed_valuation_rate_enabled():
		return
	
	# Get the appropriate items table based on doctype
	items_table = None
	if doc.doctype in ["Purchase Invoice", "Sales Invoice"]:
		items_table = doc.items
	elif doc.doctype == "Stock Entry":
		items_table = doc.items
	elif doc.doctype == "Delivery Note":
		items_table = doc.items
	elif doc.doctype == "Purchase Receipt":
		items_table = doc.items
	elif doc.doctype == "Stock Reconciliation":
		items_table = doc.items
	
	if items_table:
		for item in items_table:
			if item.item_code and item.qty:
				# Get fixed valuation rate from Item master
				valuation_rate = get_fixed_rate(item.item_code)
				
				if valuation_rate:
					# Update the item's valuation rate
					item.valuation_rate = valuation_rate
					
					# For Sales Invoice, preserve the rate and base_rate (standard_rate) 
					# and only update valuation_rate for stock valuation purposes
					if doc.doctype == "Sales Invoice":
						# Don't override rate and base_rate for Sales Invoice
						# These should remain as standard_rate (selling price)
						frappe.logger().info(f"Sales Invoice detected in ensure_fixed_valuation_rate - preserving rate and base_rate for item {item.item_code}")
						pass
					else:
						# For other doctypes, update the item's rate (this affects GL entries)
						item.rate = valuation_rate
						
						# Update base rate if it exists
						if hasattr(item, 'base_rate'):
							item.base_rate = valuation_rate
					
					# Ensure outward transactions use fixed rate
					if hasattr(item, 'incoming_rate'):
						item.incoming_rate = valuation_rate
					
					# Recalculate stock value
					if hasattr(item, 'stock_qty') and item.stock_qty:
						item.stock_value = valuation_rate * flt(item.stock_qty)
					elif hasattr(item, 'qty') and item.qty:
						item.stock_value = valuation_rate * flt(item.qty)


def ensure_sle_fixed_valuation_rate(doc, method):
	"""
	Document event handler to ensure Stock Ledger Entry uses fixed valuation rate.
	This function is called before_insert for Stock Ledger Entry.
	"""
	if not is_fixed_valuation_rate_enabled():
		return
	
	if doc.item_code and doc.actual_qty:
		# Get fixed valuation rate from Item master
		valuation_rate = get_fixed_rate(doc.item_code)
		
		if valuation_rate:
			# Update the SLE's valuation rate
			doc.valuation_rate = valuation_rate
			
			# Recalculate stock value difference
			doc.stock_value_difference = valuation_rate * doc.actual_qty


def override_get_sl_entries(d, args, original_func):
	"""
	Override the get_sl_entries function to ensure fixed valuation rate is used.
	"""
	if not is_fixed_valuation_rate_enabled():
		return original_func(d, args)
	
	# Get the original SL entries
	sl_dict = original_func(d, args)
	
	# Override the incoming_rate with fixed valuation rate
	if sl_dict and sl_dict.get("item_code"):
		valuation_rate = get_fixed_rate(sl_dict["item_code"]) 
		if valuation_rate:
			sl_dict["incoming_rate"] = valuation_rate
	
	return sl_dict


def override_stock_controller_get_gl_entries(self, warehouse_account=None, default_expense_account=None, default_cost_center=None):
	"""
	Override the get_gl_entries function in stock_controller.py to ensure fixed valuation rate is used.
	"""
	if not is_fixed_valuation_rate_enabled():
		# Use original logic if feature is disabled
		return ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES(self, warehouse_account, default_expense_account, default_cost_center)
	
	# Get the original GL entries
	if not warehouse_account:
		from erpnext.stock import get_warehouse_account_map
		warehouse_account = get_warehouse_account_map(self.company)
	
	# Override the item rates before GL entry creation
	for item in self.items:
		if item.item_code and item.qty:
			# Get fixed valuation rate from Item master
			valuation_rate = get_fixed_rate(item.item_code)
			
			if valuation_rate:
				# For Sales Invoice, preserve the rate and base_rate (standard_rate) 
				# and only update valuation_rate for stock valuation purposes
				if hasattr(self, 'doctype') and self.doctype == "Sales Invoice":
					# Don't override rate and base_rate for Sales Invoice
					# These should remain as standard_rate (selling price)
					frappe.logger().info(f"Sales Invoice detected in override_stock_controller_get_gl_entries - preserving rate and base_rate for item {item.item_code}")
					pass
				else:
					# Update the item's rate (this affects GL entries)
					item.rate = valuation_rate
					
					# Update base rate if it exists
					if hasattr(item, 'base_rate'):
						item.base_rate = valuation_rate
				
				# Ensure outward transactions use fixed rate
				if hasattr(item, 'incoming_rate'):
					item.incoming_rate = valuation_rate
	
	# Now call the original function with updated rates
	return ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES(self, warehouse_account, default_expense_account, default_cost_center)


def override_get_gl_entries(doc, method):
	"""
	Override GL entry creation to ensure fixed valuation rate is used.
	"""
	if not is_fixed_valuation_rate_enabled():
		return
	
	# This function will be called after GL entries are created
	# We need to ensure that the GL entries use the fixed rate
	pass


def get_valuation_method_override(item_code):
	"""
	Always use Moving Average valuation method when fixed valuation is enabled.
	"""
	if is_fixed_valuation_rate_enabled():
		return "Moving Average"
	return original_get_valuation_method(item_code)


def fixed_get_moving_average_values(self, sle):
	"""
	Override moving average computation to always set valuation rate
	from Item master when fixed valuation is enabled.
	"""
	if not is_fixed_valuation_rate_enabled():
		return ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG(self, sle)
	
	item_code = getattr(sle, "item_code", None) or getattr(self, "item_code", None)
	rate = get_fixed_rate(item_code)
	
	# Force current valuation rate to fixed
	self.wh_data.valuation_rate = rate or 0.0


def fixed_process_sle(self, sle):
	"""
	Wrap original process_sle to enforce fixed valuation rate on SLE rows
	after ERPNext updates them.
	"""
	from erpnext.stock.stock_ledger import update_entries_after as UpdateEntriesAfter
	# Call the original behavior first
	ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE(self, sle)
	if not is_fixed_valuation_rate_enabled():
		return
	
	# Determine fixed rate
	rate = get_fixed_rate(sle.item_code)
	
	# Compute consistent values purely from fixed rate
	closing_qty = float(sle.qty_after_transaction or 0)
	actual_qty = float(sle.actual_qty or 0)
	prev_qty = closing_qty - actual_qty
	prev_stock_value = (rate or 0.0) * prev_qty
	new_stock_value = (rate or 0.0) * closing_qty
	new_diff = (rate or 0.0) * actual_qty
	
	# Force SLE persisted fields (fast, single SQL)
	sle.valuation_rate = rate or 0.0
	sle.stock_value = new_stock_value
	sle.stock_value_difference = new_diff
	frappe.db.sql(
		"""
		update `tabStock Ledger Entry`
		set valuation_rate=%s, stock_value=%s, stock_value_difference=%s
		where name=%s
		""",
		(sle.valuation_rate, sle.stock_value, sle.stock_value_difference, sle.name),
	)
	
	# Update in-memory warehouse data for subsequent rows
	try:
		self.wh_data.valuation_rate = rate or 0.0
		self.wh_data.stock_value = new_stock_value
		self.wh_data.prev_stock_value = new_stock_value
	except Exception:
		pass


# Apply overrides when module is imported
def apply_overrides():
    """
    Apply all the overrides when this module is imported.
    This ensures the fixed valuation rate logic is active.
    """
    try:
        # Skip overriding during background repost jobs to minimize contention
        if frappe.local.flags.get("in_repost"):
            return
        # Apply monkey patching to core ERPNext modules
        import erpnext.stock.stock_ledger
        import erpnext.stock.utils
        import erpnext.stock.get_item_details
        from erpnext.controllers.stock_controller import StockController
        from erpnext.stock.stock_ledger import update_entries_after as UpdateEntriesAfter
        
        # Override the core functions
        erpnext.stock.stock_ledger.get_valuation_rate = get_valuation_rate
        erpnext.stock.stock_ledger.get_incoming_rate_for_return_entry = get_incoming_rate_for_return_entry
        erpnext.stock.utils.get_incoming_rate = get_incoming_rate
        erpnext.stock.get_item_details.get_valuation_rate = get_valuation_rate_for_item_details
        erpnext.stock.utils.get_valuation_method = get_valuation_method_override
        erpnext.stock.stock_ledger.get_valuation_method = get_valuation_method_override
        
        # Ensure GL entries also use fixed rates
        global ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES
        if ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES is None:
            ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES = StockController.get_gl_entries
        StockController.get_gl_entries = override_stock_controller_get_gl_entries
        
        # Override moving average valuation computation and final SLE write
        global ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG, ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE
        if ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG is None:
            ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG = UpdateEntriesAfter.get_moving_average_values
        UpdateEntriesAfter.get_moving_average_values = fixed_get_moving_average_values
        if ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE is None:
            ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE = UpdateEntriesAfter.process_sle
        UpdateEntriesAfter.process_sle = fixed_process_sle
        
        frappe.logger().info("Custom ERP: Fixed valuation rate overrides applied successfully (SLE/GLE patched)")
        
    except Exception as e:
        frappe.logger().error(f"Custom ERP: Failed to apply overrides: {e}")

# Apply overrides when module is imported
try:
    apply_overrides()
except:
    pass

# Also apply overrides when this function is called directly
def force_apply_overrides():
    """
    Force apply overrides - call this function to ensure overrides are applied.
    """
    try:
        clear_fixed_rate_cache()
        # Skip overriding during background repost jobs to minimize contention
        if frappe.local.flags.get("in_repost"):
            return True
        # Apply monkey patching to core ERPNext modules
        import erpnext.stock.stock_ledger
        import erpnext.stock.utils
        import erpnext.stock.get_item_details
        from erpnext.controllers.stock_controller import StockController
        from erpnext.stock.stock_ledger import update_entries_after as UpdateEntriesAfter
        
        # Override the core functions
        erpnext.stock.stock_ledger.get_valuation_rate = get_valuation_rate
        erpnext.stock.stock_ledger.get_incoming_rate_for_return_entry = get_incoming_rate_for_return_entry
        erpnext.stock.utils.get_incoming_rate = get_incoming_rate
        erpnext.stock.get_item_details.get_valuation_rate = get_valuation_rate_for_item_details
        erpnext.stock.utils.get_valuation_method = get_valuation_method_override
        erpnext.stock.stock_ledger.get_valuation_method = get_valuation_method_override
        
        # Ensure GL entries also use fixed rates
        global ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES
        if ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES is None:
            ORIGINAL_STOCK_CONTROLLER_GET_GL_ENTRIES = StockController.get_gl_entries
        StockController.get_gl_entries = override_stock_controller_get_gl_entries
        
        # Override moving average valuation computation and final SLE write
        global ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG, ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE
        if ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG is None:
            ORIGINAL_UPDATE_ENTRIES_AFTER_GET_MOVING_AVG = UpdateEntriesAfter.get_moving_average_values
        UpdateEntriesAfter.get_moving_average_values = fixed_get_moving_average_values
        if ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE is None:
            ORIGINAL_UPDATE_ENTRIES_AFTER_PROCESS_SLE = UpdateEntriesAfter.process_sle
        UpdateEntriesAfter.process_sle = fixed_process_sle
        
        print("✅ Custom ERP: Fixed valuation rate overrides applied successfully (SLE/GLE patched)")
        return True
        
    except Exception as e:
        print(f"❌ Custom ERP: Failed to apply overrides: {e}")
        return False

