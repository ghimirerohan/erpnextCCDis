import frappe


def on_payment_entry_submit(doc, method):
	"""Hook: fires when any Payment Entry is submitted. Notifies admin room."""
	amount = getattr(doc, "paid_amount", None) or getattr(doc, "received_amount", None)
	mode = getattr(doc, "mode_of_payment", None)
	frappe.publish_realtime(
		"ccdis:erp_payment_submitted",
		{
			"payment_entry": doc.name,
			"party_type": getattr(doc, "party_type", None),
			"party": getattr(doc, "party", None),
			"amount": amount,
			"mode": mode,
		},
		room="ccdis_admin",
	)
