import json
import os
import time
import uuid
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import frappe
from frappe.utils import now_datetime

try:
    import requests
except Exception:  # pragma: no cover
    requests = None  # type: ignore


def _get_cfg() -> Dict[str, Any]:
    cfg = frappe.get_site_config().get("fonepay", {}) if frappe else {}
    # env fallbacks
    cfg.setdefault("merchant_code", os.environ.get("FONEPAY_MERCHANT_CODE"))
    cfg.setdefault("secret_key", os.environ.get("FONEPAY_SECRET_KEY"))
    cfg.setdefault("username", os.environ.get("FONEPAY_USERNAME"))
    cfg.setdefault("password", os.environ.get("FONEPAY_PASSWORD"))
    cfg.setdefault("env", os.environ.get("FONEPAY_ENV", "dev"))
    cfg.setdefault("ws_worker", os.environ.get("FONEPAY_WS_WORKER", "inprocess"))
    cfg.setdefault("ws_timeout_seconds", int(float(os.environ.get("FONEPAY_WS_TIMEOUT", "300"))))
    cfg.setdefault("scheduled_batch_size", int(float(os.environ.get("FONEPAY_SCHEDULED_BATCH_SIZE", "50"))))
    cfg.setdefault("scheduled_sleep_between", float(os.environ.get("FONEPAY_SCHEDULED_SLEEP", "0.2")))
    return cfg


def _base_urls(env: str) -> Dict[str, str]:
    # ADDED BY AI: FONEPAY LIVE SOCKET - Live endpoints for production
    if env == "live":
        return {
            "create": "https://merchantapi.fonepay.com/api/merchant/merchantDetailsForThirdParty/thirdPartyDynamicQrDownload",
            "status": "https://merchantapi.fonepay.com/api/merchant/merchantDetailsForThirdParty/thirdPartyDynamicQrGetStatus",
            "ws_base": "wss://ws.fonepay.com/convergent-webSocket-web/merchantEndPoint/",
        }
    return {
        "create": "https://dev-merchantapi.fonepay.com/api/merchant/merchantDetailsForThirdParty/thirdPartyDynamicQrDownload",
        "status": "https://dev-merchantapi.fonepay.com/api/merchant/merchantDetailsForThirdParty/thirdPartyDynamicQrGetStatus",
        "ws_base": "wss://dev-ws.fonepay.com/convergent-webSocket-web/merchantEndPoint/",
    }


def generate_hmac(secret_key: str, message: str) -> str:
    return hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha512).hexdigest()


def acquire_tx_lock(tx_name: str, timeout: int = 5) -> bool:
    # Use MySQL GET_LOCK if available
    try:
        res = frappe.db.sql("select GET_LOCK(%s, %s)", (f"fonepay:{tx_name}", timeout))
        return bool(res and res[0][0] == 1)
    except Exception:
        return False


def release_tx_lock(tx_name: str) -> None:
    try:
        frappe.db.sql("select RELEASE_LOCK(%s)", (f"fonepay:{tx_name}",))
    except Exception:
        pass


def _ensure_mode_of_payment():
    if not frappe.db.exists("Mode of Payment", "Fonepay"):
        mop = frappe.get_doc({
            "doctype": "Mode of Payment",
            "mode_of_payment": "Fonepay",
            "type": "Bank",
        })
        mop.insert(ignore_permissions=True)
        frappe.db.commit()


def _payment_entry_reference_keys() -> Dict[str, str]:
    # Compatibility across ERPNext versions
    return {
        "reference_doctype": "reference_doctype",
        "reference_name": "reference_name",
        "allocated_amount": "allocated_amount",
    }


def _create_payment_entry(customer: str, amount: float, sales_invoice: Optional[str] = None) -> str:
    _ensure_mode_of_payment()
    
    # Get customer's default company
    customer_doc = frappe.get_doc("Customer", customer)
    company = customer_doc.get("default_company") or frappe.defaults.get_defaults().get("company")
    
    if not company:
        # Fallback: get first company
        companies = frappe.get_all("Company", limit=1)
        if companies:
            company = companies[0].name
        else:
            frappe.throw("No company found in the system")
    
    # Get default accounts for the company
    company_doc = frappe.get_doc("Company", company)
    default_bank_account = company_doc.default_bank_account
    default_receivable_account = company_doc.default_receivable_account
    
    # If no default bank account, try to get any bank account for the company
    if not default_bank_account:
        bank_accounts = frappe.get_all(
            "Account",
            filters={
                "company": company,
                "account_type": "Bank",
                "is_group": 0,
                "disabled": 0
            },
            limit=1
        )
        if bank_accounts:
            default_bank_account = bank_accounts[0].name
        else:
            # Create a default bank account if none exists
            bank_account = frappe.get_doc({
                "doctype": "Account",
                "account_name": "Fonepay Bank",
                "account_type": "Bank",
                "parent_account": "Bank Accounts - " + company_doc.abbr,
                "company": company,
                "is_group": 0
            })
            bank_account.insert(ignore_permissions=True)
            default_bank_account = bank_account.name
    
    # If no default receivable account, get it
    if not default_receivable_account:
        receivable_accounts = frappe.get_all(
            "Account",
            filters={
                "company": company,
                "account_type": "Receivable",
                "is_group": 0,
                "disabled": 0
            },
            limit=1
        )
        if receivable_accounts:
            default_receivable_account = receivable_accounts[0].name
        else:
            frappe.throw(f"No Receivable account found for company {company}")
    
    pe = frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": "Receive",
        "mode_of_payment": "Fonepay",
        "party_type": "Customer",
        "party": customer,
        "company": company,
        "posting_date": frappe.utils.today(),
        "paid_from": default_receivable_account,  # Customer's account (debit)
        "paid_to": default_bank_account,  # Company's bank account (credit)
        "paid_amount": amount,
        "received_amount": amount,
        "target_exchange_rate": 1,  # NPR to NPR
        "source_exchange_rate": 1,
        "reference_no": f"FONEPAY-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}",
        "reference_date": frappe.utils.today(),
    })
    
    if sales_invoice:
        keys = _payment_entry_reference_keys()
        pe.append("references", {
            keys["reference_doctype"]: "Sales Invoice",
            keys["reference_name"]: sales_invoice,
            keys["allocated_amount"]: amount,
        })
    
    pe.insert(ignore_permissions=True)
    pe.submit()
    return pe.name


def _post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)  # type: ignore
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return {"raw": r.text}


def _address_display(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    try:
        return frappe.db.get_value("Address", name, "address_display")
    except Exception:
        return None


@frappe.whitelist()
def search_customers(query: str = "", limit: int = 10000) -> Dict[str, Any]:
    """Return up to ``limit`` customers matching name/code/contact details."""
    # Allow very high limit to ensure all customers are available
    limit = min(int(limit or 10000), 50000)
    like = f"%{query.strip()}%" if query else None
    filters = {"disabled": 0}
    or_filters = []
    if like:
        or_filters = [
            ["Customer", "name", "like", like],
            ["Customer", "customer_name", "like", like],
            ["Customer", "mobile_no", "like", like],
            ["Customer", "email_id", "like", like],
        ]
    fields = [
        "name",
        "customer_name",
        "customer_group",
        "territory",
        "customer_primary_address",
        "mobile_no",
        "email_id",
        "tax_id",
    ]
    customers = frappe.get_all(
        "Customer",
        fields=fields,
        filters=filters,
        or_filters=or_filters,
        limit_page_length=limit,
        order_by="customer_name asc",
    )
    for row in customers:
        row["address_display"] = _address_display(row.get("customer_primary_address"))
    return {"customers": customers}


@frappe.whitelist()
def create_dynamic_qr(amount: float, customer: Optional[str] = None, sales_invoice: Optional[str] = None,
                      remarks1: str = "", remarks2: str = "", metadata: Optional[str] = None) -> Dict[str, Any]:
    if not customer:
        frappe.throw("Customer is required for Fonepay QR")
    cfg = _get_cfg()
    env = cfg.get("env", "dev")
    urls = _base_urls(env)
    merchant_code = cfg.get("merchant_code")
    secret_key = cfg.get("secret_key")
    username = cfg.get("username")
    password = cfg.get("password")
    if not all([merchant_code, secret_key, username, password]):
        frappe.throw("Fonepay configuration missing in site_config")

    # default remarks with customer name, amount, and date
    customer_name = frappe.db.get_value("Customer", customer, "customer_name") or customer

    if not remarks2:
        remarks2 = f"{customer_name} - NPR {amount}"
    else:
        remarks2 = f"{remarks2} {customer_name}"
    if not remarks1:
        remarks1 = now_datetime().strftime("%Y-%m-%d %H:%M:%S")

    prn = str(uuid.uuid4())
    message = f"{amount},{prn},{merchant_code},{remarks1},{remarks2}"
    data_validation = generate_hmac(secret_key, message)
    payload = {
        "amount": str(amount),
        "remarks1": remarks1 or "",
        "remarks2": remarks2 or "",
        "prn": prn,
        "merchantCode": merchant_code,
        "dataValidation": data_validation,
        "username": username,
        "password": password,
    }
    resp = _post_json(urls["create"], payload)

    qr_message = resp.get("qrMessage") or resp.get("message") or ""
    merchant_ws_url = resp.get("merchantWebSocketUrl") or resp.get("merchantwebSocketUrl")
    ws_url = resp.get("thirdpartyQrWebSocketUrl") or resp.get("thirdPartyQrWebSocketUrl") or merchant_ws_url
    status = (resp.get("status") or "CREATED").upper()

    timeout_secs = int(cfg.get("ws_timeout_seconds", 300))
    timeout_at = now_datetime() + timedelta(seconds=timeout_secs)

    tx = frappe.get_doc({
        "doctype": "Fonepay QR Transaction",
        "prn": prn,
        "merchant_code": merchant_code,
        "amount": amount,
        "currency": "NPR",
        "customer": customer,
        "sales_invoice": None,
        "username": username,
        "data_validation": data_validation,
        "qr_message": qr_message,
        "thirdparty_qr_websocket_url": ws_url,
        "response_json": json.dumps(resp, default=str),
        "status": status,
        "processed": 0,
        "timeout_at": timeout_at,
        "env": env,
        "metadata": metadata or None,
    })
    tx.insert(ignore_permissions=True)
    frappe.db.commit()

    # enqueue listener if using inprocess worker
    if cfg.get("ws_worker", "inprocess") == "inprocess" and ws_url:
        try:
            frappe.enqueue("custom_erp.custom_erp.api.fonepay.listen_to_ws", queue="long", tx_name=tx.name, now=False)
        except Exception:
            pass

    return {
        "tx_name": tx.name,
        "prn": prn,
        "qr_message": qr_message,
        "websocket_url": ws_url,
        "status": status,
        "amount": amount,
        "customer": customer,
        "merchant_websocket_url": merchant_ws_url,
        "raw_response": resp,
    }


def _parse_ws_message(raw: str) -> Dict[str, Any]:
    try:
        obj = json.loads(raw)
    except Exception:
        return {"raw": raw}
    # Some payloads embed JSON strings inside fields
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
                try:
                    obj[k] = json.loads(v)
                except Exception:
                    pass
    
    # ADDED BY AI: FONEPAY LIVE SOCKET - Handle new field names from live API
    # Normalize transactionStatus field values for backward compatibility
    if isinstance(obj, dict):
        # Map new field names to internal format
        if "transactionStatus" in obj:
            ts = str(obj.get("transactionStatus", "")).upper()
            # Normalize status values
            if ts in ["SUCCESS", "COMPLETED"]:
                obj["paymentSuccess"] = True
                obj["normalized_status"] = "SUCCESS"
            elif ts == "FAILED":
                obj["normalized_status"] = "FAILED"
            elif ts == "INITIATED":
                obj["normalized_status"] = "INITIATED"
        
        # Store additional fields for reference
        if "txnRefId" in obj:
            obj["transaction_ref_id"] = obj["txnRefId"]
        if "merchantTxnId" in obj:
            obj["merchant_txn_id"] = obj["merchantTxnId"]
        if "responseCode" in obj:
            obj["response_code"] = obj["responseCode"]
        if "responseMessage" in obj:
            obj["response_message"] = obj["responseMessage"]
    
    return obj


@frappe.whitelist()
def listen_to_ws(tx_name: str):
    cfg = _get_cfg()
    # Lazy import to avoid dependency during tests if not installed
    try:
        from websocket import create_connection  # type: ignore
    except Exception as e:  # pragma: no cover
        frappe.log_error(f"websocket-client missing: {e}", "Fonepay WS")
        return

    tx = frappe.get_doc("Fonepay QR Transaction", tx_name)
    url = tx.thirdparty_qr_websocket_url
    if not url:
        return

    attempts = 0
    last_err = None
    while attempts < 3:
        attempts += 1
        try:
            ws = create_connection(url, timeout=30)
            while True:
                if tx.processed or (tx.timeout_at and now_datetime() > tx.timeout_at):
                    ws.close()
                    return
                try:
                    msg = ws.recv()
                except Exception:
                    break
                parsed = _parse_ws_message(msg)
                tx = frappe.get_doc("Fonepay QR Transaction", tx_name)
                tx.last_ws_message = json.dumps(parsed)
                new_status = None
                
                # ADDED BY AI: FONEPAY LIVE SOCKET - Detect new transactionStatus field
                if isinstance(parsed, dict):
                    # New format: transactionStatus field
                    if "transactionStatus" in parsed:
                        ts = str(parsed.get("transactionStatus", "")).upper()
                        if ts in ["SUCCESS", "COMPLETED"]:
                            new_status = "SUCCESS"
                        elif ts == "FAILED":
                            new_status = "FAILED"
                        elif ts == "INITIATED":
                            new_status = "SCANNED"
                    
                    # Old format: Map statuses
                    if not new_status:
                        if "qrVerified" in json.dumps(parsed):
                            new_status = "VERIFIED"
                        if "scan" in json.dumps(parsed):
                            new_status = "SCANNED"
                        # Success detection (old format)
                        if (
                            parsed.get("paymentSuccess") is True or
                            (isinstance(parsed.get("transactionStatus"), dict) and parsed.get("transactionStatus", {}).get("paymentSuccess") is True)
                        ):
                            new_status = "SUCCESS"
                
                if new_status:
                    tx.status = new_status
                tx.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.publish_realtime("fonepay_update", {
                    "tx": tx.name,
                    "prn": tx.prn,
                    "status": tx.status,
                    "message": f"WS update: {tx.status}",
                    "payment_entry": tx.payment_entry,
                    "raw": parsed,
                })
                if new_status == "SUCCESS":
                    finalize_payment_from_ws(tx.name)
                    return
        except Exception as e:  # pragma: no cover
            last_err = str(e)
            time.sleep(5)
            continue

    if last_err:
        frappe.db.set_value("Fonepay QR Transaction", tx_name, {
            "last_error": f"WS failed: {last_err}",
            "retries": frappe.db.get_value("Fonepay QR Transaction", tx_name, "retries") or 0 + 1
        })


@frappe.whitelist()
def check_qr_status(prn: str) -> Dict[str, Any]:
    cfg = _get_cfg()
    env = cfg.get("env", "dev")
    urls = _base_urls(env)
    merchant_code = cfg.get("merchant_code")
    secret_key = cfg.get("secret_key")
    username = cfg.get("username")
    password = cfg.get("password")
    if not all([merchant_code, secret_key, username, password]):
        frappe.throw("Fonepay configuration missing")
    message = f"{prn},{merchant_code}"
    data_validation = generate_hmac(secret_key, message)
    payload = {
        "prn": prn,
        "merchantCode": merchant_code,
        "dataValidation": data_validation,
        "username": username,
        "password": password
    }
    return _post_json(urls["status"], payload)


@frappe.whitelist()
def check_status(txn_ref_id: str) -> Dict[str, Any]:
    """
    ADDED BY AI: FONEPAY LIVE SOCKET
    Check payment status by transaction reference ID (PRN or tx_name).
    Returns normalized status for frontend consumption.
    """
    # Try to find transaction by name or PRN
    tx = None
    prn = None
    
    # First try as tx_name
    if frappe.db.exists("Fonepay QR Transaction", txn_ref_id):
        tx = frappe.get_doc("Fonepay QR Transaction", txn_ref_id)
        prn = tx.prn
    else:
        # Try as PRN directly
        tx_list = frappe.get_all("Fonepay QR Transaction", filters={"prn": txn_ref_id}, limit=1)
        if tx_list:
            tx = frappe.get_doc("Fonepay QR Transaction", tx_list[0].name)
            prn = txn_ref_id
        # else:
        #     # Assume it's a PRN that doesn't exist in our DB yet
        #     prn = txn_ref_id
    
    if not prn:
        return {
            "status": "ERROR",
            "message": "Transaction/Product Number : not found",
            "payment_entry": None,
        }
    
    # Call Fonepay API to check status
    try:
        frappe.logger().info(f"check_status: Checking PRN={prn}")
        response = check_qr_status(prn)
        frappe.logger().info(f"check_status: Fonepay API response: {json.dumps(response, default=str)}")
    except Exception as e:
        error_msg = f"Error checking status for {prn}: {str(e)}"
        frappe.logger().error(error_msg)
        frappe.log_error(error_msg, "Fonepay Check Status")
        return {
            "status": "ERROR",
            "message": f"API error: {str(e)}",
            "payment_entry": None,
            "error_details": str(e),
        }
    
    # Normalize status from response
    payment_status = (response.get("paymentStatus") or response.get("status") or "").lower()
    if not payment_status and isinstance(response.get("data"), dict):
        payment_status = str(response["data"].get("paymentStatus", "")).lower()
    
    # ADDED BY AI: FONEPAY LIVE SOCKET - Handle new transactionStatus field
    transaction_status_raw = None
    if "transactionStatus" in response:
        transaction_status_raw = response.get("transactionStatus")
        # Handle if it's a JSON string
        if isinstance(transaction_status_raw, str) and transaction_status_raw.startswith('{'):
            try:
                parsed_ts = json.loads(transaction_status_raw)
                transaction_status_raw = parsed_ts
            except:
                pass
        
        # Extract status from transaction status object or string
        if isinstance(transaction_status_raw, dict):
            # Check for verified but not paid
            if transaction_status_raw.get("qrVerified") is True and transaction_status_raw.get("paymentSuccess") is not True:
                payment_status = "verified_not_paid"
            elif transaction_status_raw.get("paymentSuccess") is True:
                payment_status = "success"
            elif transaction_status_raw.get("paymentSuccess") is False:
                payment_status = "failed"
        else:
            # String status
            transaction_status = str(transaction_status_raw).upper()
            if transaction_status in ["SUCCESS", "COMPLETED"]:
                payment_status = "success"
            elif transaction_status == "FAILED":
                payment_status = "failed"
            elif transaction_status in ["INITIATED", "VERIFIED"]:
                payment_status = "verified_not_paid"
            else:
                payment_status = "pending"
    
    # Default to pending if still not set
    if not payment_status:
        payment_status = "pending"
    
    # Normalize to standard status codes
    normalized_status = "PENDING"
    if payment_status == "success":
        normalized_status = "SUCCESS"
    elif payment_status == "failed":
        normalized_status = "FAILED"
    elif payment_status == "verified_not_paid":
        normalized_status = "VERIFIED_NOT_PAID"
    
    # ADDED BY AI: FONEPAY LIVE SOCKET - Trigger finalization if success and not yet processed
    if normalized_status == "SUCCESS" and tx and not tx.processed:
        frappe.logger().info(f"check_status: Triggering finalization for {tx.name}")
        try:
            finalize_result = finalize_payment_from_ws(tx.name)
            if finalize_result.get("payment_entry"):
                payment_entry = finalize_result["payment_entry"]
                frappe.logger().info(f"check_status: Payment Entry created: {payment_entry}")
        except Exception as e:
            frappe.log_error(f"Error finalizing payment in check_status: {str(e)}", "Fonepay Check Status Finalization")
    
    # Return status with payment entry if available
    payment_entry = None
    if tx:
        tx.reload()  # Reload to get latest data after finalization
        payment_entry = tx.payment_entry
    
    return {
        "status": normalized_status,
        "message": response.get("responseMessage") or response.get("message") or f"Status: {normalized_status}",
        "payment_entry": payment_entry,
        "amount": response.get("amount") or response.get("txnAmount"),
        "txn_ref_id": response.get("txnRefId") or prn,
        "raw_response": response,
    }


def safe_check_qr_status(prn: str, attempts: int = 3, sleep_seconds: float = 0.5) -> Dict[str, Any]:
    last = {}
    for i in range(attempts):
        try:
            last = check_qr_status(prn)  # type: ignore
            return last
        except Exception as e:  # pragma: no cover
            last = {"error": str(e)}
            time.sleep(sleep_seconds)
    return last


@frappe.whitelist()
def finalize_payment_from_ws(tx_name: str) -> Dict[str, Any]:
    tx = frappe.get_doc("Fonepay QR Transaction", tx_name)
    if tx.processed and tx.payment_entry:
        return {"status": tx.status, "payment_entry": tx.payment_entry}
    if not acquire_tx_lock(tx_name):
        return {"status": tx.status or "PENDING", "message": "Lock busy"}
    try:
        res = safe_check_qr_status(tx.prn)
        # Normalize status
        payment_status = (res.get("paymentStatus") or res.get("status") or "").lower()
        if not payment_status and isinstance(res.get("data"), dict):
            payment_status = str(res["data"].get("paymentStatus", "")).lower()
        
        # ADDED BY AI: FONEPAY LIVE SOCKET - Handle new transactionStatus field
        if not payment_status and "transactionStatus" in res:
            transaction_status = str(res.get("transactionStatus", "")).upper()
            if transaction_status in ["SUCCESS", "COMPLETED"]:
                payment_status = "success"
            elif transaction_status == "FAILED":
                payment_status = "failed"
            else:
                payment_status = "pending"

        if payment_status != "success":
            if payment_status == "failed":
                tx.status = "FAILED"
                tx.processed = 1
                tx.response_json = json.dumps(res)
                tx.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.publish_realtime("fonepay_update", {
                    "tx": tx.name, "prn": tx.prn, "status": "FAILED", "message": "Payment failed", "payment_entry": None, "raw": res
                })
                return {"status": "FAILED"}
            else:
                tx.status = "PENDING"
                tx.response_json = json.dumps(res)
                tx.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.publish_realtime("fonepay_update", {
                    "tx": tx.name, "prn": tx.prn, "status": "PENDING", "message": "Payment pending", "payment_entry": None, "raw": res
                })
                return {"status": "PENDING"}

        # success flow
        amount = tx.amount or 0.0
        fp_amount = None
        try:
            # ADDED BY AI: FONEPAY LIVE SOCKET - Handle multiple amount field names
            fp_amount = float(res.get("amount") or res.get("txnAmount") or res.get("transactionAmount") or 0)
        except Exception:
            fp_amount = None
        if fp_amount and abs(fp_amount - float(amount)) > 0.05:
            # prefer Fonepay amount, record discrepancy
            tx.last_error = f"Amount discrepancy: requested={amount} fonepay={fp_amount}"
            amount = fp_amount

        # determine customer
        customer = tx.customer
        if not customer and tx.sales_invoice:
            inv = frappe.get_doc("Sales Invoice", tx.sales_invoice)
            customer = inv.customer
            tx.customer = customer

        if not customer:
            tx.last_error = "Missing customer on finalize"
            tx.response_json = json.dumps(res)
            tx.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.publish_realtime("fonepay_update", {"tx": tx.name, "prn": tx.prn, "status": "FAILED", "message": "Missing customer", "raw": res})
            return {"status": "FAILED", "error": "Missing customer"}

        if tx.payment_entry:
            tx.processed = 1
            tx.status = "SUCCESS"
            tx.response_json = json.dumps(res)
            tx.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.publish_realtime("fonepay_update", {"tx": tx.name, "prn": tx.prn, "status": "SUCCESS", "payment_entry": tx.payment_entry, "raw": res})
            return {"status": "SUCCESS", "payment_entry": tx.payment_entry}

        try:
            pe_name = _create_payment_entry(customer, float(amount), tx.sales_invoice)
        except Exception as e:
            tx.last_error = f"Payment Entry error: {e}"
            tx.response_json = json.dumps(res)
            tx.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.publish_realtime("fonepay_update", {"tx": tx.name, "prn": tx.prn, "status": "FAILED", "message": str(e), "raw": res})
            return {"status": "FAILED", "error": str(e)}

        tx.payment_entry = pe_name
        tx.processed = 1
        tx.status = "SUCCESS"
        # ADDED BY AI: FONEPAY LIVE SOCKET - Handle multiple trace ID field names
        tx.fonepay_trace_id = str(res.get("traceId") or res.get("fonepayTraceId") or res.get("txnRefId") or "")
        tx.response_json = json.dumps(res)
        tx.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.publish_realtime("fonepay_update", {"tx": tx.name, "prn": tx.prn, "status": "SUCCESS", "payment_entry": pe_name, "raw": res})
        return {"status": "SUCCESS", "payment_entry": pe_name}
    finally:
        release_tx_lock(tx_name)


def _update_tx_metadata(tx_name: str, websocket_url: Optional[str]) -> None:
    if websocket_url:
        frappe.db.set_value("Fonepay QR Transaction", tx_name, {
            "thirdparty_qr_websocket_url": websocket_url,
            "last_ws_message": None,
        })
        frappe.db.commit()


@frappe.whitelist()
def process_unprocessed_qrs(tx_names: Optional[str] = None, limit: int = 100, sleep_between: float = 0.2) -> Dict[str, Any]:
    names = []
    if tx_names:
        names = [n.strip() for n in tx_names.split(',') if n.strip()]
    else:
        names = [r.name for r in frappe.get_all("Fonepay QR Transaction", filters={"processed": 0}, fields=["name"], order_by="creation asc", limit=limit)]
    results = []
    for n in names:
        try:
            res = finalize_payment_from_ws(n)
        except Exception as e:  # pragma: no cover
            res = {"status": "ERROR", "error": str(e)}
        results.append({"tx": n, **(res or {})})
        time.sleep(sleep_between)
    return {"count": len(results), "results": results}


def scheduled_process_unprocessed_qrs():
    cfg = _get_cfg()
    limit = int(cfg.get("scheduled_batch_size", 50))
    sleep_between = float(cfg.get("scheduled_sleep_between", 0.2))
    return process_unprocessed_qrs(limit=limit, sleep_between=sleep_between)


# =========================
# USER DASHBOARD ENDPOINTS
# =========================


def _today_bounds() -> Dict[str, Any]:
    """Return start and end datetime for today in system timezone."""
    start = frappe.utils.get_datetime(frappe.utils.today())
    end = start + timedelta(days=1)
    return {"start": start, "end": end}


@frappe.whitelist()
def get_user_today_summary() -> Dict[str, Any]:
    """
    Return today's QR stats for the logged-in user:
    - full_name
    - success_total_amount (NPR)
    - unprocessed_count
    - success_count
    - failed_count
    """
    user = frappe.session.user
    bounds = _today_bounds()

    # Successful total amount
    success_total = frappe.db.sql(
        """
        select coalesce(sum(amount), 0) from `tabFonepay QR Transaction`
        where owner = %s and status = 'SUCCESS'
          and creation >= %s and creation < %s
        """,
        (user, bounds["start"], bounds["end"]) ,
    )[0][0]

    # Unprocessed today count
    unprocessed_count = frappe.db.sql(
        """
        select count(*) from `tabFonepay QR Transaction`
        where owner = %s and processed = 0
          and creation >= %s and creation < %s
        """,
        (user, bounds["start"], bounds["end"]) ,
    )[0][0]

    # Success/Failed counts
    success_count = frappe.db.sql(
        """
        select count(*) from `tabFonepay QR Transaction`
        where owner = %s and status = 'SUCCESS'
          and creation >= %s and creation < %s
        """,
        (user, bounds["start"], bounds["end"]) ,
    )[0][0]
    failed_count = frappe.db.sql(
        """
        select count(*) from `tabFonepay QR Transaction`
        where owner = %s and status = 'FAILED'
          and creation >= %s and creation < %s
        """,
        (user, bounds["start"], bounds["end"]) ,
    )[0][0]

    full_name = frappe.db.get_value("User", user, "full_name") or user

    return {
        "full_name": full_name,
        "success_total_amount": float(success_total or 0),
        "unprocessed_count": int(unprocessed_count or 0),
        "success_count": int(success_count or 0),
        "failed_count": int(failed_count or 0),
    }


@frappe.whitelist()
def process_user_unprocessed_today() -> Dict[str, Any]:
    """
    Process today's unprocessed QR transactions created by the logged-in user.
    Returns a summary with how much SUCCESS was newly added and the updated totals.
    """
    user = frappe.session.user
    bounds = _today_bounds()

    # Fetch unprocessed transactions for today by this user
    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters={
            "owner": user,
            "processed": 0,
        },
        fields=["name", "amount", "processed", "status", "creation"],
        order_by="creation asc",
    )

    # Filter by today's window explicitly (creation is a Datetime)
    tx_names = [r["name"] for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]

    if not tx_names:
        summary = get_user_today_summary()
        summary.update({"processed_count": 0, "new_success_added": 0.0})
        return summary

    before = get_user_today_summary()

    # Process in batch via existing API
    res = process_unprocessed_qrs(tx_names=",".join(tx_names), limit=len(tx_names), sleep_between=0.05)

    # Count how many became SUCCESS with payment_entry
    processed_count = int(res.get("count") or 0)

    # Recompute totals
    after = get_user_today_summary()
    new_success_added = float(after.get("success_total_amount", 0)) - float(before.get("success_total_amount", 0))

    return {
        **after,
        "processed_count": processed_count,
        "new_success_added": new_success_added,
    }


@frappe.whitelist()
def list_user_transactions_today(filter_status: str = "all", limit: int = 5) -> Dict[str, Any]:
    """
    Return last N transactions for today by logged-in user.
    filter_status in {all, success, failed}
    """
    user = frappe.session.user
    bounds = _today_bounds()
    limit = max(1, min(int(limit or 5), 20))

    filters: Dict[str, Any] = {"owner": user}
    if filter_status.lower() == "success":
        filters["status"] = "SUCCESS"
    elif filter_status.lower() == "failed":
        filters["status"] = "FAILED"

    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters=filters,
        fields=["name", "customer", "amount", "status", "creation"],
        order_by="creation desc",
        limit=50,  # temp cap; we'll trim by date and then limit
    )

    # Filter by today's bounds and then take top N
    today_rows = [r for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]
    today_rows = today_rows[:limit]

    # Resolve customer names
    result = []
    for r in today_rows:
        customer_name = None
        if r.get("customer"):
            customer_name = frappe.db.get_value("Customer", r["customer"], "customer_name") or r["customer"]
        result.append({
            "name": r.get("name"),
            "customer": r.get("customer"),
            "customer_name": customer_name,
            "amount": float(r.get("amount") or 0),
            "status": r.get("status") or "",
            "time": frappe.utils.format_time(r.get("creation")),
        })

    return {"transactions": result}


# =========================
# PAY DASHBOARD ENDPOINTS
# =========================


@frappe.whitelist()
def get_pay_dashboard_summary() -> Dict[str, Any]:
    """
    Return today's overall stats for all users:
    - total_success_amount (NPR) - sum of all successful payments today
    - total_success_count - count of all successful payments today
    - current_user - logged in user info
    """
    user = frappe.session.user
    bounds = _today_bounds()
    
    # Total success amount for all users today
    total_success = frappe.db.sql(
        """
        select coalesce(sum(amount), 0), count(*) from `tabFonepay QR Transaction`
        where status = 'SUCCESS'
          and creation >= %s and creation < %s
        """,
        (bounds["start"], bounds["end"]),
    )[0]
    
    full_name = frappe.db.get_value("User", user, "full_name") or user
    
    return {
        "current_user": user,
        "current_user_full_name": full_name,
        "total_success_amount": float(total_success[0] or 0),
        "total_success_count": int(total_success[1] or 0),
    }


@frappe.whitelist()
def get_username_grouped_totals(username_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Return success amounts grouped by username for today.
    username_filter: optional username to filter by, None/empty = all users
    """
    bounds = _today_bounds()
    
    filters: Dict[str, Any] = {
        "status": "SUCCESS",
    }
    
    if username_filter and username_filter.strip():
        filters["owner"] = username_filter.strip()
    
    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters=filters,
        fields=["owner", "amount", "creation"],
        order_by="owner asc",
    )
    
    # Filter by today's bounds
    today_rows = [r for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]
    
    # Group by username
    grouped = {}
    for r in today_rows:
        owner = r.get("owner") or "Unknown"
        if owner not in grouped:
            grouped[owner] = {
                "username": owner,
                "total_amount": 0.0,
                "count": 0,
            }
        grouped[owner]["total_amount"] += float(r.get("amount") or 0)
        grouped[owner]["count"] += 1
    
    # Get full names for users
    result = []
    for username, data in grouped.items():
        full_name = frappe.db.get_value("User", username, "full_name") or username
        result.append({
            "username": username,
            "full_name": full_name,
            "total_amount": data["total_amount"],
            "count": data["count"],
        })
    
    # Sort by total_amount descending
    result.sort(key=lambda x: x["total_amount"], reverse=True)
    
    return {"grouped_totals": result}


@frappe.whitelist()
def get_customer_grouped_totals(customer_filter: Optional[str] = None, username_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Return success amounts grouped by customer for today.
    customer_filter: optional customer name/code to filter by
    username_filter: optional username to filter by
    """
    bounds = _today_bounds()
    
    filters: Dict[str, Any] = {
        "status": "SUCCESS",
    }
    
    if username_filter and username_filter.strip():
        filters["owner"] = username_filter.strip()
    
    if customer_filter and customer_filter.strip():
        filters["customer"] = customer_filter.strip()
    
    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters=filters,
        fields=["customer", "owner", "amount", "creation"],
        order_by="customer asc",
    )
    
    # Filter by today's bounds
    today_rows = [r for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]
    
    # Group by customer
    grouped = {}
    for r in today_rows:
        customer = r.get("customer")
        if not customer:
            continue
        if customer not in grouped:
            grouped[customer] = {
                "customer": customer,
                "total_amount": 0.0,
                "count": 0,
            }
        grouped[customer]["total_amount"] += float(r.get("amount") or 0)
        grouped[customer]["count"] += 1
    
    # Get customer names
    result = []
    for customer_code, data in grouped.items():
        customer_name = frappe.db.get_value("Customer", customer_code, "customer_name") or customer_code
        result.append({
            "customer": customer_code,
            "customer_name": customer_name,
            "total_amount": data["total_amount"],
            "count": data["count"],
        })
    
    # Sort by total_amount descending
    result.sort(key=lambda x: x["total_amount"], reverse=True)
    
    return {"grouped_totals": result}


@frappe.whitelist()
def get_transaction_list(
    username_filter: Optional[str] = None,
    customer_filter: Optional[str] = None,
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Return detailed transaction list with filters.
    username_filter: optional username to filter by
    customer_filter: optional customer code to filter by
    limit: max number of transactions to return
    """
    bounds = _today_bounds()
    limit = max(1, min(int(limit or 100), 500))
    
    filters: Dict[str, Any] = {
        "status": "SUCCESS",
    }
    
    if username_filter and username_filter.strip():
        filters["owner"] = username_filter.strip()
    
    if customer_filter and customer_filter.strip():
        filters["customer"] = customer_filter.strip()
    
    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters=filters,
        fields=["name", "customer", "owner", "amount", "status", "creation", "payment_entry"],
        order_by="creation desc",
        limit=limit * 2,  # Get more to filter by date
    )
    
    # Filter by today's bounds and take top N
    today_rows = [r for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]
    today_rows = today_rows[:limit]
    
    # Resolve customer names and user full names
    result = []
    for r in today_rows:
        customer_name = None
        if r.get("customer"):
            customer_name = frappe.db.get_value("Customer", r["customer"], "customer_name") or r["customer"]
        
        owner_full_name = None
        if r.get("owner"):
            owner_full_name = frappe.db.get_value("User", r["owner"], "full_name") or r["owner"]
        
        result.append({
            "name": r.get("name"),
            "customer": r.get("customer"),
            "customer_name": customer_name,
            "owner": r.get("owner"),
            "owner_full_name": owner_full_name,
            "amount": float(r.get("amount") or 0),
            "status": r.get("status") or "",
            "creation": r.get("creation"),
            "payment_entry": r.get("payment_entry"),
        })
    
    return {"transactions": result}


@frappe.whitelist()
def get_filter_customers_today() -> Dict[str, Any]:
    """
    Return list of customers with at least one success transaction today.
    Used for customer filter dropdown.
    """
    bounds = _today_bounds()
    
    rows = frappe.db.sql(
        """
        select distinct customer
        from `tabFonepay QR Transaction`
        where status = 'SUCCESS'
          and customer is not null
          and customer != ''
          and creation >= %s and creation < %s
        order by customer asc
        """,
        (bounds["start"], bounds["end"]),
        as_dict=True,
    )
    
    customers = []
    for r in rows:
        customer_code = r.get("customer")
        if customer_code:
            customer_name = frappe.db.get_value("Customer", customer_code, "customer_name") or customer_code
            customers.append({
                "value": customer_code,
                "label": f"{customer_name} ({customer_code})",
                "customer_name": customer_name,
            })
    
    return {"customers": customers}


@frappe.whitelist()
def get_filter_usernames_today() -> Dict[str, Any]:
    """
    Return list of usernames who created at least one transaction today.
    Used for username filter dropdown.
    """
    bounds = _today_bounds()
    
    rows = frappe.db.sql(
        """
        select distinct owner
        from `tabFonepay QR Transaction`
        where creation >= %s and creation < %s
        order by owner asc
        """,
        (bounds["start"], bounds["end"]),
        as_dict=True,
    )
    
    usernames = []
    for r in rows:
        username = r.get("owner")
        if username:
            full_name = frappe.db.get_value("User", username, "full_name") or username
            usernames.append({
                "value": username,
                "label": f"{full_name} ({username})",
                "full_name": full_name,
            })
    
    return {"usernames": usernames}


@frappe.whitelist()
def get_today_unprocessed_count() -> Dict[str, Any]:
    """
    Return count of unprocessed transactions for today (all users).
    """
    bounds = _today_bounds()
    
    count = frappe.db.sql(
        """
        select count(*) from `tabFonepay QR Transaction`
        where processed = 0
          and creation >= %s and creation < %s
        """,
        (bounds["start"], bounds["end"]),
    )[0][0]
    
    return {
        "unprocessed_count": int(count or 0),
    }


@frappe.whitelist()
def process_all_today_unprocessed() -> Dict[str, Any]:
    """
    Process all unprocessed transactions for today.
    Returns summary of processing results.
    """
    bounds = _today_bounds()
    
    # Get all unprocessed transactions for today
    rows = frappe.get_all(
        "Fonepay QR Transaction",
        filters={"processed": 0},
        fields=["name", "amount", "processed", "status", "creation"],
        order_by="creation asc",
    )
    
    # Filter by today's window
    tx_names = [r["name"] for r in rows if bounds["start"] <= r["creation"] < bounds["end"]]
    
    if not tx_names:
        return {
            "processed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "new_success_amount": 0.0,
            "message": "No unprocessed transactions found for today",
        }
    
    # Get summary before processing
    before_summary = get_pay_dashboard_summary()
    
    # Process all transactions
    res = process_unprocessed_qrs(tx_names=",".join(tx_names), limit=len(tx_names), sleep_between=0.05)
    
    # Get summary after processing
    after_summary = get_pay_dashboard_summary()
    
    # Count successes and failures
    success_count = sum(1 for r in res.get("results", []) if r.get("status") == "SUCCESS")
    failed_count = len(tx_names) - success_count
    new_success_amount = float(after_summary.get("total_success_amount", 0)) - float(before_summary.get("total_success_amount", 0))
    
    return {
        "processed_count": len(tx_names),
        "success_count": success_count,
        "failed_count": failed_count,
        "new_success_amount": new_success_amount,
        "before_total": before_summary.get("total_success_amount", 0),
        "after_total": after_summary.get("total_success_amount", 0),
        "message": f"Processed {len(tx_names)} transactions: {success_count} successful, {failed_count} failed",
    }

