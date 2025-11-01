# PWA Independence Verification Guide

## Overview
Each route `/jsapp/{{pathname}}` is configured as an independent PWA that can be installed separately on mobile devices.

## Routes and Their Manifests

| Route | Manifest File | App Name | Scope | Start URL |
|-------|--------------|----------|------|-----------|
| `/jsapp/` | `manifest-home.json` | Custom ERP | `/jsapp/` | `/jsapp/` |
| `/jsapp/qrpay` | `manifest-qrpay.json` | QRPay | `/jsapp/qrpay/` | `/jsapp/qrpay/` |
| `/jsapp/pay-dashboard` | `manifest-pay-dashboard.json` | Pay Dashboard | `/jsapp/pay-dashboard/` | `/jsapp/pay-dashboard/` |
| `/jsapp/uploadsales` | `manifest-uploadsales.json` | Upload Sales | `/jsapp/uploadsales/` | `/jsapp/uploadsales/` |
| `/jsapp/scanner` | `manifest-scanner.json` | Scanner | `/jsapp/scanner/` | `/jsapp/scanner/` |
| `/jsapp/qrpay-admin` | `manifest-qrpay-admin.json` | QRPay Admin | `/jsapp/qrpay-admin/` | `/jsapp/qrpay-admin/` |

## How It Works

1. **Initial Load**: The manifest is set in `index.html` based on the current URL path
2. **Route Changes**: `App.vue` watches for route changes and updates the manifest link dynamically
3. **PWA Installation**: When user clicks "Install" on mobile, the browser uses the current manifest's scope
4. **Service Worker**: Each app scope has its own service worker registered with route-specific scope

## Testing PWA Independence

### Mobile Testing Steps:

1. **QRPay App**:
   - Navigate to: `https://your-domain.com/jsapp/qrpay`
   - Open browser menu → "Add to Home Screen" or "Install App"
   - Verify app name shows as "QRPay"
   - After installation, verify it opens only `/jsapp/qrpay/` scope
   - Verify app cannot access other routes outside its scope

2. **Pay Dashboard App**:
   - Navigate to: `https://your-domain.com/jsapp/pay-dashboard`
   - Install as PWA
   - Verify app name shows as "Pay Dashboard"
   - Verify it's independent from QRPay app

3. **Repeat for all routes** to confirm each installs independently

### Desktop Browser Testing:

1. Open Chrome DevTools → Application → Manifest
2. Navigate to each route and verify:
   - Correct manifest file is loaded
   - Scope matches the route path
   - Start URL matches the scope
   - App name is route-specific

### Verification Checklist:

- [ ] Each route loads its own manifest file
- [ ] Manifest scope is locked to route path (e.g., `/jsapp/qrpay/`)
- [ ] Service worker scope matches manifest scope
- [ ] Each route can be installed independently
- [ ] Installed apps show correct name in app drawer
- [ ] Installed apps are isolated to their scope
- [ ] PWA install prompt shows correct app name

## Implementation Details

### Files Involved:

1. **Manifest Files**: `frontend/public/manifest-*.json`
2. **Dynamic Loading**: `frontend/index.html` (initial) + `frontend/src/App.vue` (updates)
3. **Service Worker**: `frontend/src/register-sw.js`
4. **Install Prompt**: `frontend/src/components/PWAInstallPrompt.vue` (route-aware)

### Key Features:

- ✅ Each route has unique manifest with isolated scope
- ✅ Manifest link updates automatically on route navigation
- ✅ Install prompt shows route-specific app name
- ✅ Service worker registration is route-aware
- ✅ Independent PWA installation per route

## Notes

- When installing on mobile, the browser will use the manifest that's currently loaded in the page
- The manifest scope determines what URLs the PWA can access
- Each installed PWA is completely independent and can coexist on the device

