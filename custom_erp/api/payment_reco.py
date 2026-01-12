# ADDED BY AI: DAILY_PAYMENT_RECO
"""
Daily Payment Reconciliation API Module

This module handles CSV upload, driver assignment, and payment entry for daily sales reconciliation.
"""

import frappe
from frappe import _
import csv
import io
import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import traceback
import nepali_datetime


@frappe.whitelist()
def get_current_nepali_date() -> Dict[str, Any]:
    """
    Get current date in Nepali (BS) format.
    """
    try:
        import nepali_datetime
        now_bs = nepali_datetime.date.today()
        month_names = ["Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"]
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        formatted = f"{month_names[now_bs.month - 1]} {now_bs.day}, {now_bs.year}"
        return {
            "success": True,
            "data": {
                "year": now_bs.year, "month": now_bs.month, "day": now_bs.day,
                "formatted": formatted, "weekday": weekday_names[now_bs.weekday()]
            },
            "message": "Current Nepali date retrieved"
        }
    except Exception as e:
        frappe.log_error(f"Error getting Nepali date: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": f"Error: {str(e)}"}


@frappe.whitelist()
def parse_and_validate_csv(csv_content: str) -> Dict[str, Any]:
    """
    Parse CSV file and validate that customers exist in the system.
    """
    try:
        csv_file = io.StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        parsed_rows = []
        unmatched_customers = []
        grouped = {}
        for row in csv_reader:
            raw_outlet_code = row.get("Outlet Code", "").strip().strip('"')
            outlet_code = raw_outlet_code.lstrip('0')
            if not outlet_code and raw_outlet_code:
                # If it was all zeros, e.g., "000", make it "0"
                outlet_code = "0"
                
            outlet_name = row.get("Outlet Name", "").strip().strip('"')
            reference_no = row.get("Reference No", "").strip().strip('"')
            amount = float(row.get("Amount", "0").strip().strip('"').replace(',', ''))
            salesman_name = row.get("Salesman Name", "").strip().strip('"')
            customer_exists = frappe.db.exists("Customer", outlet_code)
            parsed_row = {
                "outlet_code": outlet_code, "outlet_name": outlet_name,
                "reference_no": reference_no, "amount": amount,
                "salesman_name": salesman_name, "customer_exists": bool(customer_exists)
            }
            parsed_rows.append(parsed_row)
            if not customer_exists:
                unmatched_customers.append({"outlet_code": outlet_code, "outlet_name": outlet_name})
            if reference_no not in grouped:
                grouped[reference_no] = []
            grouped[reference_no].append(parsed_row)
        return {
            "success": True,
            "data": {"parsed_rows": parsed_rows, "grouped_by_loadsheet": grouped, "unmatched_customers": unmatched_customers},
            "message": f"Parsed {len(parsed_rows)} rows, {len(grouped)} load sheets"
        }
    except Exception as e:
        frappe.log_error(f"Error parsing CSV: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": f"Error parsing CSV: {str(e)}"}


@frappe.whitelist()
def get_territories_list() -> Dict[str, Any]:
    try:
        territories = frappe.get_all("Territory", fields=["name"], filters={"is_group": 0}, order_by="name")
        return {"success": True, "data": territories, "message": f"Retrieved {len(territories)} territories"}
    except Exception as e:
        frappe.log_error(f"Error getting territories: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": [], "message": f"Error getting territories: {str(e)}"}


@frappe.whitelist()
def create_customer_from_csv(outlet_code: str, outlet_name: str, territory: str, tax_id: str, phone_number: str) -> Dict[str, Any]:
    try:
        if not all([outlet_code, outlet_name, territory, tax_id, phone_number]):
            raise ValueError("All fields are required")
        phone_clean = ''.join(filter(str.isdigit, phone_number))
        if len(phone_clean) != 10:
            raise ValueError("Phone Number must be exactly 10 digits")
        if frappe.db.exists("Customer", outlet_code):
            return {"success": False, "data": None, "message": f"Customer with code '{outlet_code}' already exists"}
        customer_doc = frappe.get_doc({
            "doctype": "Customer", "customer_name": outlet_name, "customer_type": "Company",
            "territory": territory, "tax_id": tax_id, "mobile_no": phone_clean, "customer_group": "Commercial"
        })
        customer_doc.insert(ignore_permissions=True, set_name=outlet_code)
        frappe.db.commit()
        if customer_doc.name != outlet_code:
            frappe.rename_doc("Customer", customer_doc.name, outlet_code, force=True)
            frappe.db.commit()
        return {"success": True, "data": {"name": outlet_code, "customer_name": outlet_name}, "message": f"Customer created successfully"}
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating customer: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": f"Error creating customer: {str(e)}"}


@frappe.whitelist()
def get_drivers_list() -> Dict[str, Any]:
    try:
        drivers = frappe.get_all("Driver", fields=["name", "full_name"], filters={"status": "Active"}, order_by="full_name")
        return {"success": True, "data": [{"name": d.name, "driver_name": d.full_name or d.name} for d in drivers], "message": f"Retrieved {len(drivers)} drivers"}
    except Exception as e:
        frappe.log_error(f"Error getting drivers: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": [], "message": f"Error getting drivers: {str(e)}"}


@frappe.whitelist()
def create_payment_recos(driver_assignments: str, csv_data: str) -> Dict[str, Any]:
    try:
        assignments = json.loads(driver_assignments)
        grouped_data = json.loads(csv_data)
        created_recos = []
        for driver_name, loadsheets in assignments.items():
            driver = frappe.db.get_value("Driver", {"full_name": driver_name}, "name")
            if not driver: frappe.throw(_(f"Driver not found: {driver_name}"))
            customer_amounts = {}
            total_amount = 0
            for loadsheet in loadsheets:
                if loadsheet in grouped_data:
                    for row in grouped_data[loadsheet]:
                        customer = row["outlet_code"]
                        amount = row["amount"]
                        customer_amounts[customer] = customer_amounts.get(customer, 0) + amount
                        total_amount += amount
            reco_doc = frappe.get_doc({
                "doctype": "Daily Sales Payment Reco", "driver": driver, "loadsheet_number": ", ".join(loadsheets),
                "initial_total_amount": total_amount, "net_total_amount": total_amount, "remaining_amount": total_amount,
                "additional_amount": 0, "return_amount": 0, "qr_amount": 0, "cheque_amount": 0, "cash_amount": 0,
                "credit_amount": 0, "expense_amount": 0, "settled": 0
            })
            for customer, amount in customer_amounts.items():
                reco_doc.append("daily_sales_payment_reco_line", {
                    "customer": customer, "initial_total_amount": amount, "net_total_amount": amount,
                    "remaining_amount": amount, "settled": 0
                })
            reco_doc.insert()
            frappe.db.commit()
            created_recos.append(reco_doc.name)
        return {"success": True, "data": {"created_recos": created_recos}, "message": f"Created {len(created_recos)} records"}
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating payment recos: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": f"Error: {str(e)}"}


@frappe.whitelist()
def settle_all_pending_as_cash(reco_name: str) -> Dict[str, Any]:
    try:
        if not reco_name: raise ValueError("Reco name is required")
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        updated_count = 0
        for line in reco_doc.daily_sales_payment_reco_line:
            if not line.settled:
                remaining = float(line.remaining_amount or 0)
                if remaining > 0:
                    line.cash_amount = float(line.cash_amount or 0) + remaining
                    line.remaining_amount = 0
                    line.settled = 1
                    line.remarks = (line.remarks or "") + " [Auto-settled as Cash]"
                    updated_count += 1
        if updated_count > 0:
            total_cash = sum([float(l.cash_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
            reco_doc.cash_amount = total_cash
            reco_doc.remaining_amount = 0
            reco_doc.save(ignore_permissions=True)
            frappe.db.commit()
        return {"success": True, "message": f"Settled {updated_count} items"}
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error settling as cash: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


# --- DASHBOARD API METHODS ---

def get_cheque_settlement_summary():
    """Helper to get cheque settlement info using direct SQL for reliability and performance"""
    try:
        # Get today's date in BS
        today_bs = nepali_datetime.date.today().strftime('%Y-%m-%d')
        
        # 1. Total pending cheques
        pending_res = frappe.db.sql("""
            SELECT COUNT(*) as count, IFNULL(SUM(amount), 0) as amount
            FROM `tabCheques Taageta`
            WHERE settled = 0
        """, as_dict=True)[0]
        
        # 2. Due today or late (pending)
        due_res = frappe.db.sql("""
            SELECT COUNT(*) as count, IFNULL(SUM(amount), 0) as amount
            FROM `tabCheques Taageta`
            WHERE settled = 0 AND cheque_date_nepali <= %s
        """, (today_bs,), as_dict=True)[0]
        
        return {
            "total_pending_count": int(pending_res.count),
            "total_pending_amount": float(pending_res.amount),
            "due_today_count": int(due_res.count),
            "due_today_amount": float(due_res.amount),
            "today_bs": today_bs
        }
    except Exception as e:
        frappe.log_error(f"Error in get_cheque_settlement_summary: {str(e)}\n{traceback.format_exc()}")
        return {
            "total_pending_count": 0,
            "total_pending_amount": 0,
            "due_today_count": 0,
            "due_today_amount": 0,
            "today_bs": ""
        }


@frappe.whitelist()
def get_daily_transactions_summary(date: str = None) -> Dict[str, Any]:
    try:
        from frappe.utils import nowdate
        if not date: date = nowdate()
        
        # SQL for fast aggregation, ignoring timezone/permission complexities for the summary
        query = """
            SELECT 
                IFNULL(SUM(net_total_amount), 0) as net_total_amount,
                IFNULL(SUM(cash_amount), 0) as cash_amount,
                IFNULL(SUM(qr_amount), 0) as qr_amount,
                IFNULL(SUM(cheque_amount), 0) as cheque_amount,
                IFNULL(SUM(credit_amount), 0) as credit_amount,
                IFNULL(SUM(return_amount), 0) as return_amount,
                IFNULL(SUM(expense_amount), 0) as expense_amount,
                IFNULL(SUM(remaining_amount), 0) as remaining_amount,
                COUNT(*) as total_count
            FROM `tabDaily Sales Payment Reco`
            WHERE creation >= %s AND creation <= %s
        """
        params = (f"{date} 00:00:00", f"{date} 23:59:59")
        summary_res = frappe.db.sql(query, params, as_dict=True)[0]
        
        # Get parent names for child aggregation
        parent_records = frappe.get_all("Daily Sales Payment Reco", filters=[["creation", ">=", f"{date} 00:00:00"], ["creation", "<=", f"{date} 23:59:59"]], fields=["name", "driver"], ignore_permissions=True)
        
        if not parent_records:
            return {"success": True, "data": {"net_total_amount": 0, "total_records": 0, "cheque_settlement_info": get_cheque_settlement_summary()}, "message": "No records"}

        parent_names = [p.name for p in parent_records]
        
        # Child aggregation
        counts_res = frappe.db.sql(f"""
            SELECT 
                COUNT(CASE WHEN cash_amount > 0 THEN 1 END) as cash_count,
                COUNT(CASE WHEN qr_amount > 0 THEN 1 END) as qr_count,
                COUNT(CASE WHEN cheque_amount > 0 THEN 1 END) as cheque_count,
                COUNT(CASE WHEN credit_amount > 0 THEN 1 END) as credit_count,
                COUNT(CASE WHEN return_amount > 0 THEN 1 END) as return_count,
                COUNT(*) as total_records
            FROM `tabDaily Sales Payment Reco Line`
            WHERE parent IN ({','.join(['%s']*len(parent_names))})
        """, tuple(parent_names), as_dict=True)[0]
        
        drivers_list = []
        driver_ids = list(set([p.driver for p in parent_records if p.driver]))
        for d_id in driver_ids:
            d_name = frappe.db.get_value("Driver", d_id, "full_name") or d_id
            drivers_list.append({"driver": d_id, "driver_name": d_name})
            
        customers_res = frappe.db.sql(f"""
            SELECT DISTINCT l.customer, c.customer_name
            FROM `tabDaily Sales Payment Reco Line` l
            LEFT JOIN `tabCustomer` c ON l.customer = c.name
            WHERE l.parent IN ({','.join(['%s']*len(parent_names))})
        """, tuple(parent_names), as_dict=True)
        
        return {
            "success": True,
            "data": {
                "net_total_amount": float(summary_res.net_total_amount),
                "cash_amount": float(summary_res.cash_amount),
                "qr_amount": float(summary_res.qr_amount),
                "cheque_amount": float(summary_res.cheque_amount),
                "credit_amount": float(summary_res.credit_amount),
                "return_amount": float(summary_res.return_amount),
                "expense_amount": float(summary_res.expense_amount),
                "remaining_amount": float(summary_res.remaining_amount),
                "total_records": int(counts_res.total_records),
                "cash_count": int(counts_res.cash_count),
                "qr_count": int(counts_res.qr_count),
                "cheque_count": int(counts_res.cheque_count),
                "credit_count": int(counts_res.credit_count),
                "return_count": int(counts_res.return_count),
                "drivers": drivers_list,
                "customers": [{"customer": c.customer, "customer_name": c.customer_name or c.customer} for c in customers_res],
                "cheque_settlement_info": get_cheque_settlement_summary()
            }
        }
    except Exception as e:
        frappe.log_error(f"Error in summary: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_daily_transactions_by_user(date: str = None, driver_filter: str = None, status_filter: str = None) -> Dict[str, Any]:
    try:
        from frappe.utils import nowdate
        if not date: date = nowdate()
        filters = [["creation", ">=", f"{date} 00:00:00"], ["creation", "<=", f"{date} 23:59:59"]]
        if driver_filter: filters.append(["driver", "=", driver_filter])
        if status_filter == "settled": filters.append(["settled", "=", 1])
        elif status_filter == "pending": filters.append(["settled", "=", 0])
        
        parent_records = frappe.get_all("Daily Sales Payment Reco", filters=filters, fields=["*"], ignore_permissions=True)
        if not parent_records: return {"success": True, "data": []}
        
        driver_data = {}
        for parent in parent_records:
            d_id = parent.driver or "Unknown"
            if d_id not in driver_data:
                driver_data[d_id] = {
                    "driver": d_id, "driver_name": frappe.db.get_value("Driver", d_id, "full_name") or d_id,
                    "initial_total_amount": 0, "additional_amount": 0, "net_total_amount": 0, 
                    "cash_amount": 0, "qr_amount": 0, "cheque_amount": 0,
                    "credit_amount": 0, "return_amount": 0, "expense_amount": 0, "remaining_amount": 0,
                    "cash_received": 0, "cash_difference": 0, "line_count": 0, "parent_names": []
                }
            for field in ["initial_total_amount", "additional_amount", "net_total_amount", "cash_amount", "qr_amount", "cheque_amount", "credit_amount", "return_amount", "expense_amount", "remaining_amount", "cash_received", "cash_difference"]:
                driver_data[d_id][field] += float(parent.get(field) or 0)
            driver_data[d_id]["parent_names"].append(parent.name)
            
        for d_id, data in driver_data.items():
            data["line_count"] = frappe.db.count("Daily Sales Payment Reco Line", filters={"parent": ["in", data["parent_names"]]})
            del data["parent_names"]
            
        return {"success": True, "data": sorted(driver_data.values(), key=lambda x: x["net_total_amount"], reverse=True)}
    except Exception as e:
        frappe.log_error(f"Error in by_user: {str(e)}")
        return {"success": False, "data": []}


@frappe.whitelist()
def get_daily_transactions_by_customer(date: str = None, driver_filter: str = None, customer_filter: str = None, status_filter: str = None) -> Dict[str, Any]:
    try:
        from frappe.utils import nowdate
        if not date: date = nowdate()
        p_filters = [["creation", ">=", f"{date} 00:00:00"], ["creation", "<=", f"{date} 23:59:59"]]
        if driver_filter: p_filters.append(["driver", "=", driver_filter])
        
        parent_records = frappe.get_all("Daily Sales Payment Reco", filters=p_filters, fields=["name", "driver"], ignore_permissions=True)
        if not parent_records: return {"success": True, "data": []}
        
        p_names = [p.name for p in parent_records]
        driver_lookup = {p.name: p.driver for p in parent_records}
        
        l_filters = [["parent", "in", p_names]]
        if customer_filter: l_filters.append(["customer", "=", customer_filter])
        if status_filter == "settled": l_filters.append(["settled", "=", 1])
        elif status_filter == "pending": l_filters.append(["settled", "=", 0])
        
        lines = frappe.get_all("Daily Sales Payment Reco Line", filters=l_filters, fields=["*"], ignore_permissions=True)
        result = []
        for l in lines:
            d_id = driver_lookup.get(l.parent)
            result.append({
                "name": l.name, "customer": l.customer, "customer_name": frappe.db.get_value("Customer", l.customer, "customer_name") or l.customer,
                "driver": d_id, "driver_name": frappe.db.get_value("Driver", d_id, "full_name") or "Unknown",
                "net_total_amount": float(l.net_total_amount or 0), "cash_amount": float(l.cash_amount or 0),
                "qr_amount": float(l.qr_amount or 0), "cheque_amount": float(l.cheque_amount or 0),
                "credit_amount": float(l.credit_amount or 0), "return_amount": float(l.return_amount or 0),
                "remaining_amount": float(l.remaining_amount or 0), "settled": l.settled, "remarks": l.remarks
            })
        return {"success": True, "data": sorted(result, key=lambda x: x["net_total_amount"], reverse=True)}
    except Exception as e:
        frappe.log_error(f"Error in by_customer: {str(e)}")
        return {"success": False, "data": []}


@frappe.whitelist()
def get_daily_transactions_details(date: str = None, driver_filter: str = None, customer_filter: str = None, category_filter: str = None, status_filter: str = None, limit: int = 200) -> Dict[str, Any]:
    try:
        from frappe.utils import nowdate
        if not date: date = nowdate()
        p_filters = [["creation", ">=", f"{date} 00:00:00"], ["creation", "<=", f"{date} 23:59:59"]]
        if driver_filter: p_filters.append(["driver", "=", driver_filter])
        
        parent_records = frappe.get_all("Daily Sales Payment Reco", filters=p_filters, fields=["name", "driver"], ignore_permissions=True)
        if not parent_records: return {"success": True, "data": []}
        
        p_names = [p.name for p in parent_records]
        driver_lookup = {p.name: p.driver for p in parent_records}
        
        l_filters = [["parent", "in", p_names]]
        if customer_filter: l_filters.append(["customer", "=", customer_filter])
        if status_filter == "settled": l_filters.append(["settled", "=", 1])
        elif status_filter == "pending": l_filters.append(["settled", "=", 0])
        
        lines = frappe.get_all("Daily Sales Payment Reco Line", filters=l_filters, fields=["*"], limit=limit, ignore_permissions=True)
        if category_filter:
            lines = [l for l in lines if float(l.get(f"{category_filter}_amount") or 0) > 0]
            
        result = []
        for l in lines:
            d_id = driver_lookup.get(l.parent)
            result.append({
                "name": l.name, "parent": l.parent, "customer": l.customer, "customer_name": frappe.db.get_value("Customer", l.customer, "customer_name") or l.customer,
                "driver": d_id, "driver_name": frappe.db.get_value("Driver", d_id, "full_name") or "Unknown",
                "initial_total_amount": float(l.initial_total_amount or 0), "additional_amount": float(l.additional_amount or 0),
                "net_total_amount": float(l.net_total_amount or 0), "cash_amount": float(l.cash_amount or 0),
                "qr_amount": float(l.qr_amount or 0), "cheque_amount": float(l.cheque_amount or 0),
                "credit_amount": float(l.credit_amount or 0), "return_amount": float(l.return_amount or 0),
                "remaining_amount": float(l.remaining_amount or 0), "settled": l.settled, "remarks": l.remarks,
                "fonepay_qr_transaction": l.fonepay_qr_transaction, "cheques_taageta": l.cheques_taageta
            })
        return {"success": True, "data": sorted(result, key=lambda x: x["net_total_amount"], reverse=True)}
    except Exception as e:
        frappe.log_error(f"Error in details: {str(e)}")
        return {"success": False, "data": []}


@frappe.whitelist()
def get_today_reco_summary(driver: str = None) -> Dict[str, Any]:
    """
    Get summary of today's payment reconciliation records.
    Filterable by driver.
    """
    try:
        from frappe.utils import nowdate
        today = nowdate()
        
        filters = [
            ["creation", ">=", f"{today} 00:00:00"],
            ["creation", "<=", f"{today} 23:59:59"]
        ]
        if driver:
            filters.append(["driver", "=", driver])
            
        recos = frappe.get_all("Daily Sales Payment Reco", filters=filters, fields=["name"], ignore_permissions=True)
        
        if not recos:
            return {
                "success": True,
                "data": {
                    "settled_count": 0,
                    "settled_amount": 0,
                    "unsettled_count": 0,
                    "unsettled_amount": 0
                },
                "message": "No records found for today"
            }
            
        parent_names = [r.name for r in recos]
        
        # Get line statistics
        lines = frappe.db.sql(f"""
            SELECT 
                settled,
                SUM(net_total_amount) as total_net,
                SUM(remaining_amount) as total_remaining,
                COUNT(*) as count
            FROM `tabDaily Sales Payment Reco Line`
            WHERE parent IN ({','.join(['%s']*len(parent_names))})
            GROUP BY settled
        """, tuple(parent_names), as_dict=True)
        
        stats = {
            "settled_count": 0,
            "settled_amount": 0,
            "unsettled_count": 0,
            "unsettled_amount": 0
        }
        
        for row in lines:
            if row.settled:
                stats["settled_count"] = int(row.count)
                stats["settled_amount"] = float(row.total_net)
            else:
                stats["unsettled_count"] = int(row.count)
                stats["unsettled_amount"] = float(row.total_remaining)
                
        return {
            "success": True,
            "data": stats,
            "message": "Today's summary retrieved"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_today_reco_summary: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_due_cheques(filters: str = None) -> Dict[str, Any]:
    try:
        conditions = {"settled": 0}
        if filters:
            try:
                extra = json.loads(filters)
                if extra.get("customer"): conditions["customer"] = extra["customer"]
            except: pass
        cheques = frappe.get_all("Cheques Taageta", fields=["*"], filters=conditions, order_by="cheque_date_nepali asc", ignore_permissions=True)
        for c in cheques: 
            c["customer_name"] = frappe.db.get_value("Customer", c.customer, "customer_name")
            # Get the full name of the user who brought the cheque
            if c.get("brought_by"):
                c["brought_by_full_name"] = frappe.db.get_value("User", c.brought_by, "full_name") or c.brought_by
            else:
                c["brought_by_full_name"] = None
        return {"success": True, "data": cheques}
    except Exception as e:
        frappe.log_error(f"Error in due_cheques: {str(e)}")
        return {"success": False, "data": []}


@frappe.whitelist()
def save_expense_amount(reco_name: str, expense_amount: float) -> Dict[str, Any]:
    try:
        if not reco_name: raise ValueError("Reco name required")
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        expense_amount = float(expense_amount or 0)
        cash_amount = float(reco_doc.cash_amount or 0)
        cash_received = float(reco_doc.cash_received or 0)
        
        # Calculate cash expected and difference
        cash_expected = cash_amount - expense_amount
        cash_difference = cash_received - cash_expected
        
        # Update using db_set for immediate effect
        reco_doc.db_set("expense_amount", expense_amount)
        reco_doc.db_set("cash_expected", cash_expected)
        reco_doc.db_set("cash_difference", cash_difference)
        
        frappe.db.commit()
        
        # Return updated summary data for real-time UI update
        return {
            "success": True, 
            "message": "Expense saved",
            "data": {
                "initial_total_amount": float(reco_doc.initial_total_amount or 0),
                "additional_amount": float(reco_doc.additional_amount or 0),
                "net_total_amount": float(reco_doc.net_total_amount or 0),
                "return_amount": float(reco_doc.return_amount or 0),
                "qr_amount": float(reco_doc.qr_amount or 0),
                "cheque_amount": float(reco_doc.cheque_amount or 0),
                "cash_amount": cash_amount,
                "credit_amount": float(reco_doc.credit_amount or 0),
                "expense_amount": expense_amount,
                "cash_expected": cash_expected,
                "remaining_amount": float(reco_doc.remaining_amount or 0),
                "cash_received": cash_received,
                "cash_difference": cash_difference
            }
        }
    except Exception as e:
        frappe.log_error(f"Error saving expense: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def save_cash_received(reco_name: str, cash_received: float) -> Dict[str, Any]:
    try:
        if not reco_name: raise ValueError("Reco name required")
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        cash_received = float(cash_received or 0)
        cash_amount = float(reco_doc.cash_amount or 0)
        expense_amount = float(reco_doc.expense_amount or 0)
        
        # Calculate cash expected and difference
        cash_expected = cash_amount - expense_amount
        cash_difference = cash_received - cash_expected
        
        # Update using db_set for immediate effect
        reco_doc.db_set("cash_received", cash_received)
        reco_doc.db_set("cash_expected", cash_expected)
        reco_doc.db_set("cash_difference", cash_difference)
        
        frappe.db.commit()
        
        # Return updated summary data for real-time UI update
        return {
            "success": True, 
            "message": "Cash received saved",
            "data": {
                "initial_total_amount": float(reco_doc.initial_total_amount or 0),
                "additional_amount": float(reco_doc.additional_amount or 0),
                "net_total_amount": float(reco_doc.net_total_amount or 0),
                "return_amount": float(reco_doc.return_amount or 0),
                "qr_amount": float(reco_doc.qr_amount or 0),
                "cheque_amount": float(reco_doc.cheque_amount or 0),
                "cash_amount": cash_amount,
                "credit_amount": float(reco_doc.credit_amount or 0),
                "expense_amount": expense_amount,
                "cash_expected": cash_expected,
                "remaining_amount": float(reco_doc.remaining_amount or 0),
                "cash_received": cash_received,
                "cash_difference": cash_difference
            }
        }
    except Exception as e:
        frappe.log_error(f"Error saving cash: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_payment_entry(line_name: str, **kwargs) -> Dict[str, Any]:
    try:
        if not line_name: raise ValueError("line_name required")
        line_doc = frappe.get_doc("Daily Sales Payment Reco Line", line_name)
        for field in ["return_amount", "additional_amount", "credit_amount", "cash_amount", "qr_amount", "cheque_amount"]:
            if field in kwargs: setattr(line_doc, field, float(kwargs[field] or 0))
        for field in ["fonepay_qr_transaction", "cheques_taageta", "remarks"]:
            if field in kwargs: setattr(line_doc, field, kwargs[field])
        line_doc.net_total_amount = line_doc.initial_total_amount + (line_doc.additional_amount or 0) - (line_doc.return_amount or 0)
        line_doc.remaining_amount = line_doc.net_total_amount - (line_doc.cash_amount or 0) - (line_doc.qr_amount or 0) - (line_doc.cheque_amount or 0) - (line_doc.credit_amount or 0)
        line_doc.settled = 1 if line_doc.remaining_amount == 0 else 0
        line_doc.save(ignore_permissions=True)
        parent_doc = frappe.get_doc("Daily Sales Payment Reco", line_doc.parent)
        for field in ["return_amount", "additional_amount", "credit_amount", "cash_amount", "qr_amount", "cheque_amount"]:
            setattr(parent_doc, field, sum([float(l.get(field) or 0) for l in parent_doc.daily_sales_payment_reco_line]))
        parent_doc.net_total_amount = parent_doc.initial_total_amount + parent_doc.additional_amount - parent_doc.return_amount
        parent_doc.remaining_amount = sum([float(l.remaining_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "Updated"}
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error updating entry: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def generate_qr_no_payment_entry(customer: str, amount: float) -> Dict[str, Any]:
    try:
        from custom_erp.api import fonepay
        result = fonepay.create_dynamic_qr(amount=amount, customer=customer, sales_invoice=None, remarks2="Daily Reco", metadata="Daily Reco")
        return {"success": True, "data": {"qr_code": result.get("qr_message", ""), "transaction_id": result.get("tx_name", "")}}
    except Exception as e:
        frappe.log_error(f"Error generating QR: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def compress_and_attach_image(image_data: str, reference_doctype: str, reference_name: str, filename: str = None) -> Dict[str, Any]:
    try:
        if ',' in image_data: image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        if not filename: filename = f"img_{reference_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        file_doc = frappe.get_doc({"doctype": "File", "file_name": filename, "attached_to_doctype": reference_doctype, "attached_to_name": reference_name, "content": image_bytes, "is_private": 1})
        file_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "data": {"file_url": file_doc.file_url}}
    except Exception as e:
        frappe.log_error(f"Error attaching image: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def create_cheque_taageta(customer: str, cheque_no: str, cheque_date_nepali: str, bank_name: str, amount: float, promised_date: str = None) -> Dict[str, Any]:
    """
    Create a new Cheques Taageta record.
    
    Args:
        customer: Customer ID (required)
        cheque_no: Cheque number (required)
        cheque_date_nepali: Nepali date string (optional)
        bank_name: Institute/Bank name (required)
        amount: Cheque amount (required)
        promised_date: AD date for promised date field (optional)
    
    Returns:
        Success response with cheque record name or error message
    """
    try:
        if not customer:
            raise ValueError("Customer is required")
        if not cheque_no:
            raise ValueError("Cheque number is required")
        if not bank_name:
            raise ValueError("Institute name is required")
        
        amount = float(amount or 0)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Verify customer exists
        if not frappe.db.exists("Customer", customer):
            raise ValueError(f"Customer '{customer}' does not exist")
        
        # Create the Cheques Taageta document
        cheque_doc = frappe.get_doc({
            "doctype": "Cheques Taageta",
            "customer": customer,
            "cheque_no": cheque_no,
            "cheque_date_nepali": cheque_date_nepali or "",
            "bank_name": bank_name,
            "amount": amount,
            "promised_date": promised_date if promised_date else None,
            "brought_by": frappe.session.user,
            "settled": 0,
            "attempts": 0
        })
        
        cheque_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                "name": cheque_doc.name,
                "customer": cheque_doc.customer,
                "cheque_no": cheque_doc.cheque_no,
                "amount": float(cheque_doc.amount)
            },
            "message": f"Cheque record created successfully: {cheque_doc.name}"
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating cheque taageta: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": str(e)}

@frappe.whitelist()
def get_all_active_recos() -> Dict[str, Any]:
    """
    Get all unsettled payment reconciliation records grouped by driver.
    """
    try:
        recos = frappe.db.sql("""
            SELECT 
                d.full_name as driver_name,
                r.driver,
                COUNT(l.name) as count
            FROM `tabDaily Sales Payment Reco` r
            JOIN `tabDriver` d ON r.driver = d.name
            LEFT JOIN `tabDaily Sales Payment Reco Line` l ON l.parent = r.name
            WHERE r.settled = 0
            GROUP BY r.name
            ORDER BY d.full_name ASC
        """, as_dict=True)
        
        return {
            "success": True,
            "data": recos,
            "message": f"Retrieved {len(recos)} active reconciliations"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_all_active_recos: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": [], "message": str(e)}


def get_driver_for_user(user: str) -> Optional[str]:
    """
    Find driver linked to a user via: Driver.employee -> Employee.user_id
    Returns driver name (ID) or None if not found.
    """
    try:
        # First find the employee linked to this user
        employee = frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "name")
        if not employee:
            return None
        
        # Then find the driver linked to this employee
        driver_id = frappe.db.get_value("Driver", {"employee": employee}, "name")
        return driver_id
    except Exception:
        return None


@frappe.whitelist()
def get_driver_reco_data(driver_name: str = None) -> Dict[str, Any]:
    """
    Get reconciliation data for a specific driver or the current user.
    
    Logic:
    - If driver_name is provided (admin selecting), find that driver
    - If no driver_name, find driver via: Driver.employee -> Employee.user_id = current user
    - Admins can see all drivers, non-admins only see their own
    """
    try:
        user = frappe.session.user
        roles = frappe.get_roles(user)
        is_admin = "System Manager" in roles or "Administrator" in roles
        
        driver_id = None
        if driver_name:
            # Admin selecting a specific driver by full name
            driver_id = frappe.db.get_value("Driver", {"full_name": driver_name}, "name")
        else:
            # Find driver linked to current user via Employee
            driver_id = get_driver_for_user(user)
            
        if not driver_id and not is_admin:
            return {"success": False, "is_admin": is_admin, "message": "No driver linked to your account. Please ensure your Employee record is linked to your user and a Driver record is linked to that Employee."}
            
        # Find active (unsettled) reco for this driver
        filters = {"settled": 0}
        if driver_id:
            filters["driver"] = driver_id
            
        reco = frappe.get_all("Daily Sales Payment Reco", 
                             filters=filters, 
                             fields=["name"], 
                             order_by="creation desc", 
                             limit=1)
        
        if not reco:
            return {"success": False, "is_admin": is_admin, "message": "No active reconciliation found"}
            
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco[0].name)
        
        # Format data for frontend
        data = {
            "reco": {
                "name": reco_doc.name,
                "driver": reco_doc.driver,
                "driver_name": frappe.db.get_value("Driver", reco_doc.driver, "full_name") or reco_doc.driver,
                "loadsheet_number": reco_doc.loadsheet_number,
                "creation": str(reco_doc.creation)
            },
            "summary": {
                "initial_total_amount": float(reco_doc.initial_total_amount or 0),
                "additional_amount": float(reco_doc.additional_amount or 0),
                "net_total_amount": float(reco_doc.net_total_amount or 0),
                "return_amount": float(reco_doc.return_amount or 0),
                "qr_amount": float(reco_doc.qr_amount or 0),
                "cheque_amount": float(reco_doc.cheque_amount or 0),
                "cash_amount": float(reco_doc.cash_amount or 0),
                "credit_amount": float(reco_doc.credit_amount or 0),
                "expense_amount": float(reco_doc.expense_amount or 0),
                "cash_expected": float(reco_doc.cash_expected or 0) if reco_doc.cash_expected else float(reco_doc.cash_amount or 0) - float(reco_doc.expense_amount or 0),
                "remaining_amount": float(reco_doc.remaining_amount or 0),
                "cash_received": float(reco_doc.cash_received or 0),
                "cash_difference": float(reco_doc.cash_difference or 0)
            },
            "lines": []
        }
        
        for line in reco_doc.daily_sales_payment_reco_line:
            data["lines"].append({
                "name": line.name,
                "customer": line.customer,
                "customer_name": frappe.db.get_value("Customer", line.customer, "customer_name") or line.customer,
                "initial_total_amount": float(line.initial_total_amount or 0),
                "additional_amount": float(line.additional_amount or 0),
                "net_total_amount": float(line.net_total_amount or 0),
                "return_amount": float(line.return_amount or 0),
                "qr_amount": float(line.qr_amount or 0),
                "cheque_amount": float(line.cheque_amount or 0),
                "cash_amount": float(line.cash_amount or 0),
                "credit_amount": float(line.credit_amount or 0),
                "remaining_amount": float(line.remaining_amount or 0),
                "settled": line.settled,
                "remarks": line.remarks,
                "updated_later": line.updated_later if hasattr(line, 'updated_later') else 0
            })
            
        return {
            "success": True,
            "is_admin": is_admin,
            "data": data
        }
    except Exception as e:
        error_msg = str(e)[:100]  # Truncate for error log title
        frappe.log_error(message=traceback.format_exc(), title=f"get_driver_reco_data: {error_msg}")
        return {"success": False, "is_admin": False, "message": str(e)}


@frappe.whitelist()
def get_all_customers() -> Dict[str, Any]:
    """
    Get all customers for dropdown selection.
    """
    try:
        customers = frappe.get_all(
            "Customer",
            fields=["name", "customer_name"],
            order_by="customer_name",
            limit=5000
        )
        return {
            "success": True,
            "data": [{"name": c.name, "customer_name": c.customer_name or c.name} for c in customers],
            "message": f"Retrieved {len(customers)} customers"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_all_customers: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": [], "message": str(e)}


@frappe.whitelist()
def add_new_reco_entry(reco_name: str, customer: str, amount: float) -> Dict[str, Any]:
    """
    Add a new entry to an existing Daily Sales Payment Reco.
    
    If customer already exists in the reco:
      - Add amount to the existing record
      - Update status to pending if it was settled
      - Mark as updated_later
    
    If customer is new:
      - Create a new line with updated_later=1
    
    Always recalculates all parent totals.
    """
    try:
        if not reco_name:
            raise ValueError("Reco name is required")
        if not customer:
            raise ValueError("Customer is required")
        
        amount = float(amount or 0)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Verify customer exists
        if not frappe.db.exists("Customer", customer):
            raise ValueError(f"Customer '{customer}' does not exist")
        
        # Get the reco document
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        
        # Check if customer already exists in the reco lines
        existing_line = None
        for line in reco_doc.daily_sales_payment_reco_line:
            if line.customer == customer:
                existing_line = line
                break
        
        customer_name = frappe.db.get_value("Customer", customer, "customer_name") or customer
        
        if existing_line:
            # Customer exists - update the existing line
            old_initial = float(existing_line.initial_total_amount or 0)
            new_initial = old_initial + amount
            
            # Update amounts
            existing_line.initial_total_amount = new_initial
            existing_line.net_total_amount = new_initial + float(existing_line.additional_amount or 0) - float(existing_line.return_amount or 0)
            
            # Recalculate remaining
            total_paid = (
                float(existing_line.cash_amount or 0) +
                float(existing_line.qr_amount or 0) +
                float(existing_line.cheque_amount or 0) +
                float(existing_line.credit_amount or 0)
            )
            existing_line.remaining_amount = existing_line.net_total_amount - total_paid
            
            # If it was settled and now has remaining > 0, mark as pending
            if existing_line.settled and existing_line.remaining_amount > 0:
                existing_line.settled = 0
            
            # Mark as updated later
            existing_line.updated_later = 1
            
            # Update remarks
            existing_line.remarks = (existing_line.remarks or "") + f" [+{amount} added later]"
            
            action = "updated"
        else:
            # Customer is new - create a new line
            reco_doc.append("daily_sales_payment_reco_line", {
                "customer": customer,
                "initial_total_amount": amount,
                "net_total_amount": amount,
                "remaining_amount": amount,
                "additional_amount": 0,
                "return_amount": 0,
                "qr_amount": 0,
                "cheque_amount": 0,
                "cash_amount": 0,
                "credit_amount": 0,
                "settled": 0,
                "updated_later": 1,
                "remarks": "[Added later]"
            })
            action = "added"
        
        # Recalculate all parent totals from lines
        reco_doc.initial_total_amount = sum([float(l.initial_total_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.additional_amount = sum([float(l.additional_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.return_amount = sum([float(l.return_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.net_total_amount = reco_doc.initial_total_amount + reco_doc.additional_amount - reco_doc.return_amount
        reco_doc.qr_amount = sum([float(l.qr_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.cheque_amount = sum([float(l.cheque_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.cash_amount = sum([float(l.cash_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.credit_amount = sum([float(l.credit_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.remaining_amount = sum([float(l.remaining_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        
        # Update cash expected and difference if expense is set
        expense_amount = float(reco_doc.expense_amount or 0)
        reco_doc.cash_expected = reco_doc.cash_amount - expense_amount
        cash_received = float(reco_doc.cash_received or 0)
        reco_doc.cash_difference = cash_received - reco_doc.cash_expected
        
        # Check if all lines are settled
        all_settled = all([l.settled for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.settled = 1 if all_settled else 0
        
        # Save the document
        reco_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Return updated summary for frontend
        return {
            "success": True,
            "message": f"Customer '{customer_name}' {action} successfully with amount {amount}",
            "action": action,
            "data": {
                "initial_total_amount": float(reco_doc.initial_total_amount or 0),
                "additional_amount": float(reco_doc.additional_amount or 0),
                "net_total_amount": float(reco_doc.net_total_amount or 0),
                "return_amount": float(reco_doc.return_amount or 0),
                "qr_amount": float(reco_doc.qr_amount or 0),
                "cheque_amount": float(reco_doc.cheque_amount or 0),
                "cash_amount": float(reco_doc.cash_amount or 0),
                "credit_amount": float(reco_doc.credit_amount or 0),
                "expense_amount": float(reco_doc.expense_amount or 0),
                "cash_expected": float(reco_doc.cash_expected or 0),
                "remaining_amount": float(reco_doc.remaining_amount or 0),
                "cash_received": float(reco_doc.cash_received or 0),
                "cash_difference": float(reco_doc.cash_difference or 0)
            }
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in add_new_reco_entry: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_reco_lines_for_driver(driver_name: str = None) -> Dict[str, Any]:
    """
    Get reco lines for a specific driver (by full name).
    Used for the uploadreco view/edit interface.
    """
    try:
        if not driver_name:
            return {"success": False, "data": None, "message": "Driver name is required"}
        
        # Find driver by full name
        driver_id = frappe.db.get_value("Driver", {"full_name": driver_name}, "name")
        if not driver_id:
            return {"success": False, "data": None, "message": f"Driver '{driver_name}' not found"}
        
        # Find active (unsettled) reco for this driver
        reco = frappe.get_all(
            "Daily Sales Payment Reco",
            filters={"driver": driver_id, "settled": 0},
            fields=["name"],
            order_by="creation desc",
            limit=1
        )
        
        if not reco:
            return {"success": False, "data": None, "message": "No active reconciliation found for this driver"}
        
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco[0].name)
        
        lines = []
        for line in reco_doc.daily_sales_payment_reco_line:
            lines.append({
                "name": line.name,
                "customer": line.customer,
                "customer_name": frappe.db.get_value("Customer", line.customer, "customer_name") or line.customer,
                "initial_total_amount": float(line.initial_total_amount or 0),
                "additional_amount": float(line.additional_amount or 0),
                "net_total_amount": float(line.net_total_amount or 0),
                "return_amount": float(line.return_amount or 0),
                "qr_amount": float(line.qr_amount or 0),
                "cheque_amount": float(line.cheque_amount or 0),
                "cash_amount": float(line.cash_amount or 0),
                "credit_amount": float(line.credit_amount or 0),
                "remaining_amount": float(line.remaining_amount or 0),
                "settled": line.settled,
                "updated_later": line.updated_later if hasattr(line, 'updated_later') else 0,
                "remarks": line.remarks
            })
        
        return {
            "success": True,
            "data": {
                "reco_name": reco_doc.name,
                "driver_name": driver_name,
                "lines": lines,
                "summary": {
                    "initial_total_amount": float(reco_doc.initial_total_amount or 0),
                    "net_total_amount": float(reco_doc.net_total_amount or 0),
                    "remaining_amount": float(reco_doc.remaining_amount or 0),
                    "total_lines": len(lines),
                    "settled_count": sum([1 for l in lines if l["settled"]]),
                    "pending_count": sum([1 for l in lines if not l["settled"]])
                }
            },
            "message": f"Retrieved {len(lines)} lines for {driver_name}"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_reco_lines_for_driver: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": str(e)}


@frappe.whitelist()
def get_unprocessed_qr_count_for_reco(reco_name: str) -> Dict[str, Any]:
    """
    Get count of unprocessed Fonepay QR Transactions linked to a reco's lines.
    Returns count of QRs with status=SUCCESS and processed=0.
    """
    try:
        if not reco_name:
            raise ValueError("Reco name is required")
        
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        line_names = [line.name for line in reco_doc.daily_sales_payment_reco_line]
        
        if not line_names:
            return {"success": True, "data": {"count": 0, "total_amount": 0}, "message": "No lines in reco"}
        
        # Get unprocessed QR transactions with SUCCESS status linked to these lines
        qr_count = frappe.db.sql("""
            SELECT COUNT(*) as count, IFNULL(SUM(amount), 0) as total_amount
            FROM `tabFonepay QR Transaction`
            WHERE daily_sales_payment_reco_line IN ({})
              AND status = 'SUCCESS'
              AND processed = 0
        """.format(','.join(['%s'] * len(line_names))), tuple(line_names), as_dict=True)[0]
        
        return {
            "success": True,
            "data": {
                "count": int(qr_count.count or 0),
                "total_amount": float(qr_count.total_amount or 0)
            },
            "message": f"Found {qr_count.count} unprocessed QR transactions"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_unprocessed_qr_count_for_reco: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": str(e)}


@frappe.whitelist()
def process_qr_logs_for_reco(reco_name: str) -> Dict[str, Any]:
    """
    Process unprocessed Fonepay QR Transactions linked to a reco's lines.
    
    For each successful QR transaction:
    - If QR amount = line's initial_total_amount: normal QR payment process
    - If QR amount > line's initial_total_amount: difference goes to additional_amount
    
    Returns details of processed QR logs.
    """
    try:
        if not reco_name:
            raise ValueError("Reco name is required")
        
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        line_names = [line.name for line in reco_doc.daily_sales_payment_reco_line]
        
        if not line_names:
            return {"success": True, "data": {"processed": []}, "message": "No lines in reco"}
        
        # Get unprocessed QR transactions with SUCCESS status linked to these lines
        qr_transactions = frappe.db.sql("""
            SELECT name, amount, daily_sales_payment_reco_line, customer, prn
            FROM `tabFonepay QR Transaction`
            WHERE daily_sales_payment_reco_line IN ({})
              AND status = 'SUCCESS'
              AND processed = 0
            ORDER BY creation ASC
        """.format(','.join(['%s'] * len(line_names))), tuple(line_names), as_dict=True)
        
        if not qr_transactions:
            return {"success": True, "data": {"processed": []}, "message": "No unprocessed QR transactions found"}
        
        processed_results = []
        
        for qr_tx in qr_transactions:
            try:
                line_name = qr_tx.daily_sales_payment_reco_line
                qr_amount = float(qr_tx.amount or 0)
                
                # Get the line document
                line_doc = frappe.get_doc("Daily Sales Payment Reco Line", line_name)
                initial_amount = float(line_doc.initial_total_amount or 0)
                
                # Calculate amounts
                additional_from_qr = 0
                qr_to_apply = qr_amount
                
                if qr_amount > initial_amount:
                    # QR amount is more than initial - difference goes to additional
                    additional_from_qr = qr_amount - initial_amount
                    qr_to_apply = initial_amount
                
                # Update line amounts
                current_qr = float(line_doc.qr_amount or 0)
                current_additional = float(line_doc.additional_amount or 0)
                
                line_doc.qr_amount = current_qr + qr_to_apply
                line_doc.additional_amount = current_additional + additional_from_qr
                
                # Recalculate net and remaining
                line_doc.net_total_amount = float(line_doc.initial_total_amount or 0) + line_doc.additional_amount - float(line_doc.return_amount or 0)
                total_paid = line_doc.qr_amount + float(line_doc.cash_amount or 0) + float(line_doc.cheque_amount or 0) + float(line_doc.credit_amount or 0)
                line_doc.remaining_amount = line_doc.net_total_amount - total_paid
                
                # Check if settled
                line_doc.settled = 1 if line_doc.remaining_amount == 0 else 0
                
                # Link the QR transaction
                line_doc.fonepay_qr_transaction = qr_tx.name
                
                # Update remarks
                existing_remarks = line_doc.remarks or ""
                line_doc.remarks = f"{existing_remarks} [QR processed: {qr_tx.name}]".strip()
                
                line_doc.save(ignore_permissions=True)
                
                # Mark QR transaction as processed
                frappe.db.set_value("Fonepay QR Transaction", qr_tx.name, "processed", 1)
                
                processed_results.append({
                    "qr_name": qr_tx.name,
                    "prn": qr_tx.prn,
                    "line_name": line_name,
                    "customer": qr_tx.customer,
                    "customer_name": frappe.db.get_value("Customer", qr_tx.customer, "customer_name") or qr_tx.customer,
                    "qr_amount": qr_amount,
                    "qr_applied": qr_to_apply,
                    "additional_from_qr": additional_from_qr,
                    "initial_amount": initial_amount,
                    "new_qr_amount": line_doc.qr_amount,
                    "new_additional": line_doc.additional_amount,
                    "new_remaining": line_doc.remaining_amount,
                    "settled": line_doc.settled,
                    "status": "success"
                })
                
            except Exception as line_error:
                processed_results.append({
                    "qr_name": qr_tx.name,
                    "prn": qr_tx.prn,
                    "line_name": qr_tx.daily_sales_payment_reco_line,
                    "status": "error",
                    "error": str(line_error)
                })
        
        # Recalculate parent totals
        reco_doc.reload()
        for field in ["return_amount", "additional_amount", "credit_amount", "cash_amount", "qr_amount", "cheque_amount"]:
            setattr(reco_doc, field, sum([float(l.get(field) or 0) for l in reco_doc.daily_sales_payment_reco_line]))
        reco_doc.net_total_amount = reco_doc.initial_total_amount + reco_doc.additional_amount - reco_doc.return_amount
        reco_doc.remaining_amount = sum([float(l.remaining_amount or 0) for l in reco_doc.daily_sales_payment_reco_line])
        reco_doc.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        success_count = sum(1 for r in processed_results if r.get("status") == "success")
        error_count = sum(1 for r in processed_results if r.get("status") == "error")
        total_qr_applied = sum(r.get("qr_applied", 0) for r in processed_results if r.get("status") == "success")
        total_additional = sum(r.get("additional_from_qr", 0) for r in processed_results if r.get("status") == "success")
        
        return {
            "success": True,
            "data": {
                "processed": processed_results,
                "summary": {
                    "success_count": success_count,
                    "error_count": error_count,
                    "total_qr_applied": total_qr_applied,
                    "total_additional": total_additional,
                    "new_qr_amount": float(reco_doc.qr_amount or 0),
                    "new_additional_amount": float(reco_doc.additional_amount or 0),
                    "new_remaining_amount": float(reco_doc.remaining_amount or 0)
                }
            },
            "message": f"Processed {success_count} QR transactions, {error_count} errors"
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in process_qr_logs_for_reco: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": str(e)}


@frappe.whitelist()
def recalculate_line_amounts(line_name: str) -> Dict[str, Any]:
    """
    Recalculate amounts for a single line based on Initial Total Amount.
    
    Formula:
    1. Net Total = Initial Total + Additional Amount
    2. Remaining = Net Total - (QR + Cash + Return + Cheque + Credit)
    
    Returns error if remaining would go negative (doesn't update in that case).
    """
    try:
        if not line_name:
            raise ValueError("Line name is required")
        
        line_doc = frappe.get_doc("Daily Sales Payment Reco Line", line_name)
        
        # Get current values
        initial = float(line_doc.initial_total_amount or 0)
        additional = float(line_doc.additional_amount or 0)
        return_amt = float(line_doc.return_amount or 0)
        qr = float(line_doc.qr_amount or 0)
        cash = float(line_doc.cash_amount or 0)
        cheque = float(line_doc.cheque_amount or 0)
        credit = float(line_doc.credit_amount or 0)
        
        # Step 1: Calculate Net Total = Initial + Additional
        net_total = initial + additional
        
        # Step 2: Calculate Remaining = Net Total - sum(QR, Cash, Return, Cheque, Credit)
        total_deductions = qr + cash + return_amt + cheque + credit
        remaining = net_total - total_deductions
        
        # Check if remaining would be negative - if so, return error and DON'T update
        if remaining < 0:
            return {
                "success": False,
                "message": f"Cannot recalculate: Remaining amount would be negative (Rs. {remaining:.2f}).\n\n" +
                          f"Net Total: Rs. {net_total:.2f} (Initial: {initial:.2f} + Additional: {additional:.2f})\n" +
                          f"Total Deductions: Rs. {total_deductions:.2f} (QR: {qr:.2f} + Cash: {cash:.2f} + Return: {return_amt:.2f} + Cheque: {cheque:.2f} + Credit: {credit:.2f})"
            }
        
        # Update line document
        line_doc.net_total_amount = net_total
        line_doc.remaining_amount = remaining
        line_doc.settled = 1 if remaining == 0 else 0
        
        line_doc.save(ignore_permissions=True)
        
        # Also update parent summary
        parent_doc = frappe.get_doc("Daily Sales Payment Reco", line_doc.parent)
        
        # Sum all line amounts for parent
        parent_doc.initial_total_amount = sum([float(l.initial_total_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.additional_amount = sum([float(l.additional_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.return_amount = sum([float(l.return_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.qr_amount = sum([float(l.qr_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.cheque_amount = sum([float(l.cheque_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.cash_amount = sum([float(l.cash_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.credit_amount = sum([float(l.credit_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        
        # Parent net total and remaining follow same formula
        parent_doc.net_total_amount = parent_doc.initial_total_amount + parent_doc.additional_amount
        parent_doc.remaining_amount = sum([float(l.remaining_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        
        # Update cash expected and difference
        expense_amount = float(parent_doc.expense_amount or 0)
        parent_doc.cash_expected = parent_doc.cash_amount - expense_amount
        cash_received = float(parent_doc.cash_received or 0)
        parent_doc.cash_difference = cash_received - parent_doc.cash_expected
        
        parent_doc.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                "initial_total_amount": initial,
                "additional_amount": additional,
                "net_total_amount": net_total,
                "return_amount": return_amt,
                "qr_amount": qr,
                "cash_amount": cash,
                "cheque_amount": cheque,
                "credit_amount": credit,
                "remaining_amount": remaining,
                "settled": line_doc.settled
            },
            "message": f"Line recalculated: Net Total = Rs. {net_total:.2f}, Remaining = Rs. {remaining:.2f}"
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in recalculate_line_amounts: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def recalculate_reco_summary(reco_name: str) -> Dict[str, Any]:
    """
    Recalculate all summary-level amounts in the Daily Sales Payment Reco
    by summing up all individual line amounts.
    
    Formula for each line:
    1. Net Total = Initial Total + Additional Amount
    2. Remaining = Net Total - (QR + Cash + Return + Cheque + Credit)
    
    Parent totals are sums of all line totals.
    """
    try:
        if not reco_name:
            raise ValueError("Reco name is required")
        
        reco_doc = frappe.get_doc("Daily Sales Payment Reco", reco_name)
        
        # Sum up all line amounts
        totals = {
            "initial_total_amount": 0,
            "additional_amount": 0,
            "return_amount": 0,
            "qr_amount": 0,
            "cheque_amount": 0,
            "cash_amount": 0,
            "credit_amount": 0,
            "remaining_amount": 0
        }
        
        for line in reco_doc.daily_sales_payment_reco_line:
            totals["initial_total_amount"] += float(line.initial_total_amount or 0)
            totals["additional_amount"] += float(line.additional_amount or 0)
            totals["return_amount"] += float(line.return_amount or 0)
            totals["qr_amount"] += float(line.qr_amount or 0)
            totals["cheque_amount"] += float(line.cheque_amount or 0)
            totals["cash_amount"] += float(line.cash_amount or 0)
            totals["credit_amount"] += float(line.credit_amount or 0)
            totals["remaining_amount"] += float(line.remaining_amount or 0)
        
        # Calculate net total: Net Total = Initial + Additional
        totals["net_total_amount"] = totals["initial_total_amount"] + totals["additional_amount"]
        
        # Update reco document
        for field, value in totals.items():
            setattr(reco_doc, field, value)
        
        # Recalculate cash expected and difference
        expense_amount = float(reco_doc.expense_amount or 0)
        reco_doc.cash_expected = totals["cash_amount"] - expense_amount
        cash_received = float(reco_doc.cash_received or 0)
        reco_doc.cash_difference = cash_received - reco_doc.cash_expected
        
        reco_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                **totals,
                "expense_amount": expense_amount,
                "cash_expected": reco_doc.cash_expected,
                "cash_received": cash_received,
                "cash_difference": reco_doc.cash_difference
            },
            "message": "Reco summary recalculated successfully"
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in recalculate_reco_summary: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_unprocessed_qr_count_for_line(line_name: str) -> Dict[str, Any]:
    """
    Get count of unprocessed Fonepay QR Transactions linked to a specific line.
    Returns count of QRs with status=SUCCESS and processed=0.
    """
    try:
        if not line_name:
            raise ValueError("Line name is required")
        
        # Get unprocessed QR transactions with SUCCESS status linked to this line
        qr_count = frappe.db.sql("""
            SELECT COUNT(*) as count, IFNULL(SUM(amount), 0) as total_amount
            FROM `tabFonepay QR Transaction`
            WHERE daily_sales_payment_reco_line = %s
              AND status = 'SUCCESS'
              AND processed = 0
        """, (line_name,), as_dict=True)[0]
        
        return {
            "success": True,
            "data": {
                "count": int(qr_count.count or 0),
                "total_amount": float(qr_count.total_amount or 0)
            },
            "message": f"Found {qr_count.count} unprocessed QR transactions"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_unprocessed_qr_count_for_line: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "data": None, "message": str(e)}


@frappe.whitelist()
def process_qr_logs_for_line(line_name: str) -> Dict[str, Any]:
    """
    Process unprocessed Fonepay QR Transactions linked to a specific line.
    Same logic as process_qr_logs_for_reco but for a single line.
    """
    try:
        if not line_name:
            raise ValueError("Line name is required")
        
        line_doc = frappe.get_doc("Daily Sales Payment Reco Line", line_name)
        
        # Get unprocessed QR transactions with SUCCESS status linked to this line
        qr_transactions = frappe.db.sql("""
            SELECT name, amount, customer, prn
            FROM `tabFonepay QR Transaction`
            WHERE daily_sales_payment_reco_line = %s
              AND status = 'SUCCESS'
              AND processed = 0
            ORDER BY creation ASC
        """, (line_name,), as_dict=True)
        
        if not qr_transactions:
            return {"success": True, "data": {"processed": []}, "message": "No unprocessed QR transactions found for this line"}
        
        processed_results = []
        initial_amount = float(line_doc.initial_total_amount or 0)
        
        for qr_tx in qr_transactions:
            try:
                qr_amount = float(qr_tx.amount or 0)
                
                # Calculate amounts
                additional_from_qr = 0
                qr_to_apply = qr_amount
                
                if qr_amount > initial_amount:
                    additional_from_qr = qr_amount - initial_amount
                    qr_to_apply = initial_amount
                
                # Update line amounts
                current_qr = float(line_doc.qr_amount or 0)
                current_additional = float(line_doc.additional_amount or 0)
                
                line_doc.qr_amount = current_qr + qr_to_apply
                line_doc.additional_amount = current_additional + additional_from_qr
                
                # Recalculate
                line_doc.net_total_amount = float(line_doc.initial_total_amount or 0) + line_doc.additional_amount - float(line_doc.return_amount or 0)
                total_paid = line_doc.qr_amount + float(line_doc.cash_amount or 0) + float(line_doc.cheque_amount or 0) + float(line_doc.credit_amount or 0)
                line_doc.remaining_amount = line_doc.net_total_amount - total_paid
                line_doc.settled = 1 if line_doc.remaining_amount == 0 else 0
                
                line_doc.fonepay_qr_transaction = qr_tx.name
                
                # Mark QR as processed
                frappe.db.set_value("Fonepay QR Transaction", qr_tx.name, "processed", 1)
                
                processed_results.append({
                    "qr_name": qr_tx.name,
                    "prn": qr_tx.prn,
                    "customer": qr_tx.customer,
                    "qr_amount": qr_amount,
                    "qr_applied": qr_to_apply,
                    "additional_from_qr": additional_from_qr,
                    "status": "success"
                })
                
            except Exception as qr_error:
                processed_results.append({
                    "qr_name": qr_tx.name,
                    "status": "error",
                    "error": str(qr_error)
                })
        
        line_doc.save(ignore_permissions=True)
        
        # Update parent
        parent_doc = frappe.get_doc("Daily Sales Payment Reco", line_doc.parent)
        for field in ["return_amount", "additional_amount", "credit_amount", "cash_amount", "qr_amount", "cheque_amount"]:
            setattr(parent_doc, field, sum([float(l.get(field) or 0) for l in parent_doc.daily_sales_payment_reco_line]))
        parent_doc.net_total_amount = parent_doc.initial_total_amount + parent_doc.additional_amount - parent_doc.return_amount
        parent_doc.remaining_amount = sum([float(l.remaining_amount or 0) for l in parent_doc.daily_sales_payment_reco_line])
        parent_doc.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "data": {
                "processed": processed_results,
                "line_data": {
                    "qr_amount": float(line_doc.qr_amount or 0),
                    "additional_amount": float(line_doc.additional_amount or 0),
                    "remaining_amount": float(line_doc.remaining_amount or 0),
                    "settled": line_doc.settled
                }
            },
            "message": f"Processed {len([r for r in processed_results if r.get('status') == 'success'])} QR transactions"
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in process_qr_logs_for_line: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "message": str(e)}
