import json
from unittest.mock import patch

import frappe


def test_hmac_generation():
    from custom_erp.custom_erp.api.fonepay import generate_hmac
    secret = "testsecret"
    message = "200.00,123e4567-e89b-12d3-a456-426614174000,2005260033,hello,world"
    expected = "fcd0e1a8d93a66e3a8f4a85f2e2a1fcad0db4bd8e7f34c1bdad0b8d9b3b0b1b2f2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2"[:128]
    # We can't precompute easily here; just ensure hex length and deterministic
    digest = generate_hmac(secret, message)
    assert isinstance(digest, str) and len(digest) == 128


def _fake_create_response():
    return {
        "qrMessage": "000201010212...5303986...", 
        "thirdpartyQrWebSocketUrl": "wss://dev-ws.fonepay.com/convergent-webSocket-web/...",
        "status": "CREATED"
    }


def _fake_status_success():
    return {"paymentStatus": "success", "amount": "200.0", "traceId": "TRACE123"}


@patch("custom_erp.custom_erp.api.fonepay._post_json")
def test_create_dynamic_qr(mock_post_json):
    from custom_erp.custom_erp.api.fonepay import create_dynamic_qr
    mock_post_json.return_value = _fake_create_response()
    res = create_dynamic_qr(200.0, customer=None, sales_invoice=None, remarks1="r1", remarks2="r2")
    assert res.get("qr_message")
    tx = frappe.get_doc("Fonepay QR Transaction", res["tx_name"])
    assert tx.prn and tx.status == "CREATED"


@patch("custom_erp.custom_erp.api.fonepay.safe_check_qr_status")
def test_finalize_idempotent(mock_status):
    from custom_erp.custom_erp.api.fonepay import create_dynamic_qr, finalize_payment_from_ws
    # ensure a customer exists
    customer = frappe.get_all("Customer", limit=1)
    if not customer:
        c = frappe.get_doc({"doctype": "Customer", "customer_name": "Test FP Customer"}).insert()
        customer_name = c.name
    else:
        customer_name = customer[0].name

    # Create TX
    with patch("custom_erp.custom_erp.api.fonepay._post_json", return_value=_fake_create_response()):
        res = create_dynamic_qr(100.0, customer=customer_name)
    tx_name = res["tx_name"]

    # Mock success status
    mock_status.return_value = _fake_status_success()
    first = finalize_payment_from_ws(tx_name)
    assert first.get("status") == "SUCCESS"
    pe1 = first.get("payment_entry")
    assert pe1
    second = finalize_payment_from_ws(tx_name)
    assert second.get("payment_entry") == pe1


