## Fonepay Dynamic QR Integration for Custom ERP

This document describes setup, configuration, and operations for the Fonepay dynamic QR integration delivered under `custom_erp`.

### Prerequisites

- Site: `development.localhost`
- Apps installed: `frappe`, `erpnext`, `payments`, `custom_erp`
- Configure site_config with Fonepay credentials.

### Site Config

Add this to `sites/development.localhost/site_config.json`:

```json
"fonepay": {
  "merchant_code": "2005260033",
  "secret_key": "<REDACTED>",
  "username": "9852676@fonepay.com",
  "password": "Shree@2025",
  "env": "dev",
  "ws_worker": "inprocess",
  "ws_timeout_seconds": 300,
  "scheduled_batch_size": 50,
  "scheduled_sleep_between": 0.2
}
```

Environment variables can override any values: `FONEPAY_SECRET_KEY`, etc.

### Install / Build

```
bench --site development.localhost install-app custom_erp
bench --site development.localhost migrate
bench build
bench restart
```

### Usage

- Open `/jsapp/qrpay` to generate and display dynamic QR codes.
- Admin UI at `/jsapp/qrpay-admin` for listing and manually processing unprocessed transactions.

### Manual processors

```
bench --site development.localhost execute custom_erp.custom_erp.api.fonepay.scheduled_process_unprocessed_qrs
```

### API Reference

- `custom_erp.custom_erp.api.fonepay.create_dynamic_qr(amount, customer=None, sales_invoice=None, remarks1="", remarks2="", metadata=None)`
- `custom_erp.custom_erp.api.fonepay.process_unprocessed_qrs(tx_names=None, limit=100, sleep_between=0.2)`
- `custom_erp.custom_erp.api.fonepay.finalize_payment_from_ws(tx_name)`

### Example curl to Fonepay (for reference)

```
curl -X POST https://dev-merchantapi.fonepay.com/api/merchant/merchantDetailsForThirdParty/thirdPartyDynamicQrDownload \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "200",
    "remarks1": "test1",
    "remarks2": "test2",
    "prn": "REPLACE_WITH_PRN",
    "merchantCode": "2005260033",
    "dataValidation": "REPLACE_WITH_HMAC",
    "username": "9852676@fonepay.com",
    "password": "Shree@2025"
  }'
```

### Acceptance tests

1. Generate QR from `/jsapp/qrpay` (Customer Payment) and confirm realtime update to SUCCESS after scanning using Fonepay dev app; verify `Payment Entry` created with correct customer and allocation.
2. Simulate no WS: run scheduler `bench --site development.localhost execute custom_erp.custom_erp.api.fonepay.scheduled_process_unprocessed_qrs` and confirm status resolution.
3. Run `finalize_payment_from_ws(tx_name)` twice and confirm only one `Payment Entry` exists.
4. Use `/jsapp/qrpay-admin` to process selected or all unprocessed; confirm summary and statuses.

### Flowchart

```
[User: Customer / SalesInvoice] -> create_dynamic_qr() -> Fonepay POST -> save TX
     -> render QR in /jsapp/qrpay
     -> WS listener (server or microservice) subscribes to thirdpartyQrWebSocketUrl
         -> receives events -> update TX.status -> publish_realtime -> UI updates
         -> on paymentSuccess -> finalize_payment_from_ws(tx)
             -> check_qr_status(prn)
             -> if success -> create Payment Entry -> submit -> tx.processed = 1 -> publish_realtime SUCCESS
             -> if failed -> tx.processed = 1 status FAILED -> publish_realtime FAILED
             -> if pending -> leave processed=0, await scheduler
Scheduler hourly -> scheduled_process_unprocessed_qrs -> loop finalize_payment_from_ws for unprocessed txs
Manual admin -> process_unprocessed_qrs(tx_names) -> same finalize flow
```

### Notes

- Secrets are never stored in DB; only request artifacts and responses are stored.
- Mode of Payment `Fonepay` is created automatically if missing.
- Websocket listener runs in-process by default; a microservice skeleton can be added if needed.


