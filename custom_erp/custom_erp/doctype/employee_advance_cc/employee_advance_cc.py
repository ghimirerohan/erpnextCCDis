import frappe
from frappe.model.document import Document


class EmployeeAdvanceCC(Document):
	def validate(self):
		self.balance = self.amount_given - (self.repaid_amount or 0)
		if self.balance <= 0:
			self.status = "Cleared"
		elif self.repaid_amount and self.repaid_amount > 0:
			self.status = "Partially Repaid"
		else:
			self.status = "Outstanding"
