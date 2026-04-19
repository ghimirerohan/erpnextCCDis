import frappe
from frappe.model.document import Document


class AdminCashRegisterEntry(Document):
	def validate(self):
		if self.amount <= 0:
			frappe.throw("Amount must be greater than zero")
