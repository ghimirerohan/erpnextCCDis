# Paste this into: bench --site your-site-name console
import frappe
from frappe.utils import nowdate
from frappe import _
# import the helper that creates the journal/adjustment entry for Stock Reconciliation
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import make_adjustment_entry

def recreate_stock_reco_gl_entries(dry_run=True, limit=None, only_company=None):
    """
    Find submitted Stock Reconciliations that have SLEs but no GL Entries,
    and create the missing GL entries using make_adjustment_entry(doc).

    Parameters:
      dry_run (bool): If True, don't create anything; only report.
      limit (int|None): Limit number of Stock Reconciliation docs to process.
      only_company (str|None): If set, only process docs for this company.
    """
    out = {"checked":0, "skipped_no_sle":0, "skipped_has_gl":0, "created":0, "errors":0, "candidates":[]}
    filters = {"docstatus": 1}  # only submitted
    if only_company:
        filters["company"] = only_company

    recs = frappe.get_all("Stock Reconciliation", filters=filters, fields=["name","posting_date","company"], order_by="posting_date asc")
    if limit:
        recs = recs[:limit]

    print("Found {} submitted Stock Reconciliation(s) to inspect.".format(len(recs)))

    for r in recs:
        out["checked"] += 1
        name = r.get("name")
        company = r.get("company")

        # quick check: does company have Perpetual Inventory enabled?
        perpetual = frappe.get_value("Company", company, "enable_perpetual_inventory")
        if not perpetual:
            # still allow creation (script will run), but warn
            warning = "Company '{}' does not have Perpetual Inventory enabled. GL creation may be unexpected.".format(company)
        else:
            warning = None

        # check there is at least one Stock Ledger Entry for this voucher
        sle_exists = frappe.db.exists("Stock Ledger Entry", {"voucher_no": name})
        if not sle_exists:
            out["skipped_no_sle"] += 1
            print("SKIP (no SLE)  :", name, "| posting_date:", r.get("posting_date"), "| company:", company)
            continue

        # check whether GL entries already exist for this voucher
        gl_exists = frappe.db.exists("GL Entry", {"voucher_type": "Stock Reconciliation", "voucher_no": name})
        if gl_exists:
            out["skipped_has_gl"] += 1
            print("SKIP (has GL)  :", name, "| posting_date:", r.get("posting_date"), "| company:", company)
            continue

        # candidate to create GL entries
        out["candidates"].append(name)
        print("CANDIDATE      : ", name, "| posting_date:", r.get("posting_date"), "| company:", company, "|" , "perpetual:", bool(perpetual))
        if warning:
            print("    WARNING:", warning)

        if dry_run:
            # do not create; just report
            continue

        # create GL entries using built-in function
        try:
            doc = frappe.get_doc("Stock Reconciliation", name)
            # ensure doc is submitted
            if doc.docstatus != 1:
                print("   SKIP (not submitted at runtime):", name)
                continue

            # call the function that creates the adjustment JE (this is what ERPNext uses)
            make_adjustment_entry(doc)

            # commit after each successful creation to keep DB consistent
            frappe.db.commit()
            out["created"] += 1
            print("   CREATED GL  :", name)
        except Exception as e:
            # rollback and log error
            frappe.db.rollback()
            out["errors"] += 1
            frappe.log_error(message=frappe.get_traceback(), title="Stock Reco GL Creation Error: {}".format(name))
            print("   ERROR while creating GL for {}: {}".format(name, e))

    print("---- Summary ----")
    print("Checked:", out["checked"])
    print("Skipped (no SLE):", out["skipped_no_sle"])
    print("Skipped (already has GL):", out["skipped_has_gl"])
    print("Candidates (would-create):", len(out["candidates"]))
    print("Created:", out["created"])
    print("Errors:", out["errors"])

    return out

# # Run a DRY RUN first
# result = recreate_stock_reco_gl_entries(dry_run=True, limit=None, only_company=None)
# result
