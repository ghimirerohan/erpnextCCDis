import frappe
from frappe import _
from frappe.utils import get_datetime, today


@frappe.whitelist()
def get_field_summary(date=None):
	frappe.has_permission("Field Payment Entry", "read", throw=True)
	target_date = date or today()

	field_users = frappe.db.sql(
		"""
		SELECT e.name as employee, e.employee_name, e.user_id
		FROM `tabEmployee` e
		INNER JOIN `tabHas Role` hr ON hr.parent = e.user_id AND hr.role = 'Field User'
		WHERE e.status = 'Active'
	""",
		as_dict=True,
	)

	results = []
	for emp in field_users:
		payments = frappe.db.get_all(
			"Field Payment Entry",
			filters={
				"employee": emp.employee,
				"payment_date": target_date,
				"docstatus": 1,
			},
			fields=["payment_mode", "amount", "customer", "customer_name", "name"],
		)

		mode_totals = {}
		total = 0
		for p in payments:
			mode = p.payment_mode
			mode_totals[mode] = mode_totals.get(mode, 0) + (p.amount or 0)
			total += p.amount or 0

		driver = frappe.db.get_value("Driver", {"employee": emp.employee}, "name")
		expected_total = None
		reco_name = None
		if driver:
			reco = frappe.get_all(
				"Daily Sales Payment Reco",
				filters={"driver": driver, "settled": 0},
				fields=["name", "net_total_amount"],
				order_by="creation desc",
				limit=1,
				ignore_permissions=True,
			)
			if reco:
				expected_total = float(reco[0].net_total_amount or 0)
				reco_name = reco[0].name

		results.append(
			{
				"employee": emp.employee,
				"employee_name": emp.employee_name,
				"total_collected": total,
				"mode_totals": mode_totals,
				"transaction_count": len(payments),
				"expected_total": expected_total,
				"reco_name": reco_name,
				"payments": payments,
			}
		)

	return {"date": target_date, "employees": results}


@frappe.whitelist()
def get_employee_detail(employee, from_date=None, to_date=None):
	frappe.has_permission("Field Payment Entry", "read", throw=True)
	frappe.has_permission("Employee Advance CC", "read", throw=True)

	from_date = from_date or today()
	to_date = to_date or today()

	payments = frappe.db.get_all(
		"Field Payment Entry",
		filters={
			"employee": employee,
			"payment_date": ["between", [from_date, to_date]],
			"docstatus": 1,
		},
		fields=[
			"name",
			"customer",
			"customer_name",
			"payment_mode",
			"amount",
			"payment_date",
			"cheque_number",
			"sales_invoice",
		],
		order_by="payment_date desc, creation desc",
	)

	advances = frappe.db.get_all(
		"Employee Advance CC",
		filters={"employee": employee},
		fields=["name", "advance_date", "amount_given", "repaid_amount", "balance", "status"],
		order_by="advance_date desc",
	)

	attendance = []
	if frappe.db.exists("DocType", "Attendance"):
		attendance = frappe.db.get_all(
			"Attendance",
			filters={
				"employee": employee,
				"attendance_date": ["between", [from_date, to_date]],
			},
			fields=["attendance_date", "status", "in_time", "out_time"],
			order_by="attendance_date desc",
		)

	salary_slip = []
	if frappe.db.exists("DocType", "Salary Slip"):
		salary_slip = frappe.db.get_all(
			"Salary Slip",
			filters={"employee": employee, "docstatus": 1},
			fields=["name", "start_date", "end_date", "net_pay", "gross_pay"],
			order_by="start_date desc",
			limit=3,
		)

	return {
		"employee": employee,
		"payments": payments,
		"advances": advances,
		"attendance": attendance,
		"salary_slips": salary_slip,
	}


@frappe.whitelist()
def add_cash_register_entry(
	entry_type,
	topic,
	payment_mode,
	amount,
	employee_ref=None,
	customer_ref=None,
	advance_ref=None,
	remarks=None,
):
	frappe.has_permission("Admin Cash Register Entry", "create", throw=True)

	doc = frappe.new_doc("Admin Cash Register Entry")
	doc.entry_type = entry_type
	doc.topic = topic
	doc.payment_mode = payment_mode
	doc.amount = float(amount)
	doc.employee_ref = employee_ref
	doc.customer_ref = customer_ref
	doc.advance_ref = advance_ref
	doc.remarks = remarks
	doc.insert()

	return {"name": doc.name}


@frappe.whitelist()
def get_cash_register_summary(date=None):
	frappe.has_permission("Admin Cash Register Entry", "read", throw=True)
	target_date = date or today()

	start = get_datetime(f"{target_date} 00:00:00")
	end = get_datetime(f"{target_date} 23:59:59")

	entries = frappe.db.get_all(
		"Admin Cash Register Entry",
		filters={"entry_datetime": ["between", [start, end]]},
		fields=[
			"name",
			"entry_datetime",
			"entry_type",
			"topic",
			"payment_mode",
			"amount",
			"employee_ref",
			"customer_ref",
			"remarks",
		],
		order_by="entry_datetime desc",
	)

	total_in = sum(e.amount for e in entries if e.entry_type == "In")
	total_out = sum(e.amount for e in entries if e.entry_type == "Out")

	return {
		"date": target_date,
		"entries": entries,
		"total_in": total_in,
		"total_out": total_out,
		"net": total_in - total_out,
	}


@frappe.whitelist()
def give_advance(employee, amount, remarks=None):
	frappe.has_permission("Employee Advance CC", "create", throw=True)
	frappe.has_permission("Admin Cash Register Entry", "create", throw=True)

	doc = frappe.new_doc("Employee Advance CC")
	doc.employee = employee
	doc.amount_given = float(amount)
	doc.remarks = remarks
	doc.insert()

	frappe.get_doc(
		{
			"doctype": "Admin Cash Register Entry",
			"entry_type": "Out",
			"topic": "Employee Advance",
			"payment_mode": "Cash",
			"amount": float(amount),
			"employee_ref": employee,
			"advance_ref": doc.name,
			"remarks": remarks or _("Advance to {0}").format(employee),
		}
	).insert()

	return {"advance_name": doc.name}


@frappe.whitelist()
def get_advances_summary():
	frappe.has_permission("Employee Advance CC", "read", throw=True)

	advances = frappe.db.get_all(
		"Employee Advance CC",
		filters={"status": ["!=", "Cleared"]},
		fields=[
			"name",
			"employee",
			"employee_name",
			"advance_date",
			"amount_given",
			"repaid_amount",
			"balance",
			"status",
		],
		order_by="advance_date desc",
	)

	total_outstanding = sum(a.balance or 0 for a in advances)
	return {"advances": advances, "total_outstanding": total_outstanding}
