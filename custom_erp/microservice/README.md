# Optional WebSocket Microservice (FastAPI skeleton)

This optional component can manage persistent WebSocket connections to Fonepay and POST updates back to ERPNext as webhooks.

- Recommended only if in-process listeners are insufficient.

## Run (Docker-friendly)

```
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn websocket-client requests
uvicorn service:app --host 0.0.0.0 --port 8081
```

## Behavior

- Accepts an HTTP POST with `{ tx_name, websocket_url }` to start a background WS listener.
- On messages, it POSTS to ERPNext webhook endpoint you configure (e.g., `/api/method/custom_erp.custom_erp.api.fonepay.finalize_payment_from_ws`).

> Note: The current app ships with an in-process WS listener, so this is optional.


