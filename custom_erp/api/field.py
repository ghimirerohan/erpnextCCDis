import frappe
from frappe import _
from frappe.utils import today


def _get_employee_for_user(user):
	return frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "name")


def _get_driver_for_user(user):
	employee = _get_employee_for_user(user)
	if not employee:
		return None
	return frappe.db.get_value("Driver", {"employee": employee}, "name")


def _can_preview_field_without_employee(user):
	"""Desk-style roles that may open the field SPA for smoke-testing without an Employee row."""
	return bool(set(frappe.get_roles(user)) & {"Administrator", "System Manager"})


@frappe.whitelist()
def get_my_dashboard():
	"""
	Returns the logged-in field user's dashboard data:
	- Active Daily Sales Payment Reco for their driver (unsettled)
	- Field Payment Entry rows for today
	- Summary totals by payment mode
	"""
	user = frappe.session.user
	employee = _get_employee_for_user(user)
	if not employee:
		if _can_preview_field_without_employee(user):
			return {
				"employee": None,
				"driver": None,
				"reco": None,
				"assigned_customers": [],
				"payments": [],
				"mode_totals": {},
				"total_collected": 0,
				"field_preview": True,
				"field_preview_message": _(
					"No Employee is linked to this user. Link an active Employee to your user to see assignments and record payments."
				),
			}
		frappe.throw(_("No Employee linked to your user account. Contact admin."))

	driver_id = _get_driver_for_user(user)
	reco_data = None
	assigned_customers = []

	if driver_id:
		reco = frappe.get_all(
			"Daily Sales Payment Reco",
			filters={"driver": driver_id, "settled": 0},
			fields=["name"],
			order_by="creation desc",
			limit=1,
			ignore_permissions=True,
		)
		if reco:
			reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco[0].name)
			if reco_doc.driver != driver_id:
				frappe.throw(_("Not allowed to view this reconciliation."))
			reco_data = {
				"name": reco_doc.name,
				"total_expected": float(reco_doc.net_total_amount or 0),
				"status": "Open" if not reco_doc.settled else "Settled",
			}
			for row in reco_doc.daily_sales_payment_reco_line or []:
				cust_name = frappe.db.get_value("Customer", row.customer, "customer_name") or row.customer
				assigned_customers.append(
					{
						"customer": row.customer,
						"customer_name": cust_name,
						"expected_amount": float(row.net_total_amount or 0),
						"outstanding_amount": float(row.remaining_amount or 0),
					}
				)

	frappe.has_permission("Field Payment Entry", "read", throw=True)
	payments = frappe.db.get_all(
		"Field Payment Entry",
		filters={
			"employee": employee,
			"payment_date": today(),
			"docstatus": ["!=", 2],
		},
		fields=[
			"name",
			"customer",
			"customer_name",
			"payment_mode",
			"amount",
			"payment_date",
			"docstatus",
			"sales_invoice",
		],
		order_by="creation desc",
	)

	mode_totals = {}
	total_collected = 0
	for p in payments:
		mode = p.payment_mode
		mode_totals[mode] = mode_totals.get(mode, 0) + (p.amount or 0)
		total_collected += p.amount or 0

	return {
		"employee": employee,
		"driver": driver_id,
		"reco": reco_data,
		"assigned_customers": assigned_customers,
		"payments": payments,
		"mode_totals": mode_totals,
		"total_collected": total_collected,
	}


@frappe.whitelist()
def submit_payment(
	customer,
	payment_mode,
	amount,
	sales_invoice=None,
	reco_reference=None,
	cheque_number=None,
	cheque_date=None,
	cheque_bank=None,
	fonepay_prn=None,
	remarks=None,
):
	frappe.has_permission("Field Payment Entry", "create", throw=True)
	user = frappe.session.user
	employee = _get_employee_for_user(user)
	if not employee:
		frappe.throw(_("No Employee linked to your user account."))

	doc = frappe.new_doc("Field Payment Entry")
	doc.employee = employee
	doc.customer = customer
	doc.payment_date = today()
	doc.payment_mode = payment_mode
	doc.amount = float(amount)
	doc.sales_invoice = sales_invoice
	doc.reco_reference = reco_reference
	doc.cheque_number = cheque_number
	doc.cheque_date = cheque_date
	doc.cheque_bank = cheque_bank
	doc.fonepay_prn = fonepay_prn
	doc.remarks = remarks
	doc.insert()
	doc.submit()

	return {"name": doc.name, "status": "submitted"}


@frappe.whitelist()
def get_customer_outstanding(customer):
	frappe.has_permission("Sales Invoice", "read", throw=True)

	invoices = frappe.db.get_all(
		"Sales Invoice",
		filters={
			"customer": customer,
			"outstanding_amount": [">", 0],
			"docstatus": 1,
		},
		fields=["name", "posting_date", "grand_total", "outstanding_amount", "status"],
		order_by="posting_date desc",
		limit=50,
	)

	frappe.has_permission("Field Payment Entry", "read", throw=True)
	cheques = frappe.db.get_all(
		"Field Payment Entry",
		filters={
			"customer": customer,
			"payment_mode": "Cheque",
			"docstatus": 1,
		},
		fields=["name", "amount", "cheque_number", "cheque_date", "cheque_bank", "payment_date"],
		order_by="creation desc",
		limit=20,
	)

	return {"invoices": invoices, "cheques": cheques}


@frappe.whitelist()
def submit_cash_count(denomination_counts, expense_amount=None, expense_remarks=None):
	import json as json_lib

	frappe.has_permission("Field Payment Entry", "read", throw=True)
	user = frappe.session.user
	employee = _get_employee_for_user(user)
	if not employee:
		frappe.throw(_("No Employee linked to your user account."))

	if isinstance(denomination_counts, str):
		denomination_counts = json_lib.loads(denomination_counts)

	physical_total = sum(int(denom) * int(count) for denom, count in denomination_counts.items())

	system_total = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(amount), 0) as total
		FROM `tabField Payment Entry`
		WHERE employee = %s AND payment_date = %s
		  AND payment_mode = 'Cash' AND docstatus = 1
	""",
		(employee, today()),
		as_dict=True,
	)[0].total

	variance = physical_total - float(system_total)

	expense_logged = False
	if expense_amount and float(expense_amount) > 0:
		frappe.log_error(
			message=f"user={user} employee={employee} amount={expense_amount} remarks={expense_remarks!r}",
			title="CCDIS field expense (day close — manual office entry may be required)",
		)
		expense_logged = True

	return {
		"physical_total": physical_total,
		"system_total": float(system_total),
		"variance": variance,
		"expense_note_logged": expense_logged,
	}


@frappe.whitelist()
def search_customers_for_field(query=""):
	"""Thin wrapper so the field SPA can search customers via createResource (permissions apply)."""
	frappe.has_permission("Customer", "read", throw=True)
	from custom_erp.api.fonepay import search_customers

	return search_customers(query=query or "", limit=200)


@frappe.whitelist()
def get_field_payment_history(days=30):
	"""Recent Field Payment Entry documents for the logged-in field user."""
	frappe.has_permission("Field Payment Entry", "read", throw=True)
	user = frappe.session.user
	employee = _get_employee_for_user(user)
	if not employee:
		if _can_preview_field_without_employee(user):
			return []
		frappe.throw(_("No Employee linked to your user account."))

	days = int(days or 30)
	since = frappe.utils.add_days(today(), -days)
	return frappe.get_all(
		"Field Payment Entry",
		filters={"employee": employee, "payment_date": [">=", since], "docstatus": ["!=", 2]},
		fields=[
			"name",
			"customer",
			"customer_name",
			"payment_mode",
			"amount",
			"payment_date",
			"docstatus",
		],
		order_by="payment_date desc, creation desc",
		limit=200,
	)
