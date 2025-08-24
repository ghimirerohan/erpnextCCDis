import frappe

@frappe.whitelist()
def enqueue_bulk_submit():
    job = frappe.enqueue(
        "custom_erp.custom_erp.sales_invoice.bulk_submit_sales_invoice.run",
        queue="long",
        job_name="bulk_submit_sales_invoice",
        timeout=60 * 60,
    )
    try:
        return job.get_id()
    except Exception:
        return str(job)

def run():
    invoices = frappe.get_all("Sales Invoice", filters={"docstatus": 0}, pluck="name")
    for inv in invoices:
        try:
            doc = frappe.get_doc("Sales Invoice", inv)
            doc.submit()
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to submit {inv}: {str(e)}")
