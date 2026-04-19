import frappe
from frappe.model.document import Document


class FieldPaymentEntry(Document):
	def validate(self):
		if self.amount <= 0:
			frappe.throw("Amount must be greater than zero")
		if self.payment_mode == "Cheque" and not self.cheque_number:
			frappe.throw("Cheque number is required for cheque payments")

	def on_submit(self):
		frappe.publish_realtime(
			"ccdis:field_payment_submitted",
			{
				"employee": self.employee,
				"payment_mode": self.payment_mode,
				"amount": self.amount,
				"customer": self.customer,
				"name": self.name,
			},
			room="ccdis_admin",
		)
