# PWA Scope Configuration

## Important: App Scope is Set to `/jsapp/`

This PWA is configured to work specifically with your Vue.js application mounted at `/jsapp/`, not the root Frappe site.

## Understanding PWA Scope

### What is Scope?
The `scope` in a PWA manifest defines which URLs the PWA "owns" or can handle. Any navigation outside the scope will open in the regular browser.

### Current Configuration

```json
{
  "scope": "/jsapp/",
  "start_url": "/jsapp/"
}
```

This means:
- **✅ Handled by PWA**: `/jsapp/`, `/jsapp/scanner`, `/jsapp/qrpay`, `/jsapp/qrpay-admin`
- **❌ NOT handled by PWA**: `/`, `/app`, `/desk`, or any other Frappe routes

## How This Works

### Scenario 1: Installing from `/jsapp/`
When a user visits `https://yoursite.com:8000/jsapp/` and installs the PWA:
- The PWA will open at `/jsapp/` (the start_url)
- All routes under `/jsapp/*` will stay within the PWA
- Navigation to `/` (main Frappe site) will open in browser

### Scenario 2: Installing from `/jsapp/qrpay`
When a user visits `https://yoursite.com:8000/jsapp/qrpay` and installs the PWA:
- The PWA will STILL open at `/jsapp/` (the start_url)
- But the user can navigate to `/jsapp/qrpay` within the app
- This is by design - the PWA encompasses ALL routes under `/jsapp/`

### Scenario 3: Installing from Root `/`
If a user visits `https://yoursite.com:8000/` (main Frappe site):
- The PWA install prompt **will not appear** (different scope)
- The manifest is scoped only to `/jsapp/`

## Why This Configuration?

This configuration is correct because:

1. **Separation of Concerns**: The Vue.js app is separate from the main Frappe application
2. **Router Base Path**: Your Vue router is configured with base path `/jsapp`
3. **Asset Paths**: All Vue app assets are served under `/jsapp`
4. **Service Worker Scope**: Service worker needs to match the app's scope

## If You Want Each Route as a Separate PWA

If you want `/jsapp/qrpay`, `/jsapp/scanner`, etc. to be **completely separate** installable PWAs, you need to:

### Option 1: Multiple Manifests (Recommended)
Create separate manifest files for each app section:

**For QR Pay App:**
```json
// public/manifest-qrpay.json
{
  "name": "QR Pay",
  "short_name": "QRPay",
  "scope": "/jsapp/qrpay/",
  "start_url": "/jsapp/qrpay/"
}
```

**For Scanner App:**
```json
// public/manifest-scanner.json
{
  "name": "Scanner",
  "short_name": "Scanner",
  "scope": "/jsapp/scanner/",
  "start_url": "/jsapp/scanner/"
}
```

Then conditionally load the appropriate manifest based on the current route:

```javascript
// In your app entry point or router
const currentPath = window.location.pathname;
let manifestPath = '/manifest.json'; // default

if (currentPath.startsWith('/jsapp/qrpay')) {
  manifestPath = '/manifest-qrpay.json';
} else if (currentPath.startsWith('/jsapp/scanner')) {
  manifestPath = '/manifest-scanner.json';
}

// Dynamically set manifest
const manifestLink = document.querySelector('link[rel="manifest"]');
manifestLink.setAttribute('href', manifestPath);
```

### Option 2: Query Parameters (Alternative)
Use query parameters to differentiate installations:

```json
{
  "scope": "/jsapp/qrpay/",
  "start_url": "/jsapp/qrpay/?standalone=true"
}
```

### Option 3: Separate Deployments (Best for Truly Independent Apps)
Deploy each app section as a completely separate application:
- `/qrpay/` → Separate PWA
- `/scanner/` → Separate PWA
- `/erp/` → Separate PWA

## Current Router Configuration

Your Vue router is configured as:
```javascript
const router = createRouter({
  history: createWebHistory("/jsapp"),
  routes: [
    { path: "/", name: "Home" },           // → /jsapp/
    { path: "/scanner", name: "Scanner" }, // → /jsapp/scanner
    { path: "/qrpay", name: "QRPay" },     // → /jsapp/qrpay
    // ...
  ]
})
```

This means all routes are under the `/jsapp` base, which matches our PWA scope.

## Testing the Scope

### Test 1: Install from Vue App
1. Navigate to `https://yoursite.com:8000/jsapp/`
2. Install prompt should appear
3. Install the PWA
4. PWA opens at `/jsapp/`
5. Navigate to `/jsapp/qrpay` - stays in PWA ✅
6. Navigate to `/` (click external link) - opens in browser ✅

### Test 2: Direct Route Access
1. Navigate to `https://yoursite.com:8000/jsapp/qrpay`
2. Install prompt should appear (if not already installed)
3. Install the PWA
4. PWA opens at `/jsapp/` (start_url)
5. You can then navigate to `/jsapp/qrpay` within the app

### Test 3: Scope Boundaries
1. Open installed PWA
2. Try to navigate to `/app` or `/desk` (Frappe routes)
3. Should open in regular browser, not in PWA ✅

## Verification

Check your manifest in DevTools:
1. Open Chrome DevTools (F12)
2. Go to Application → Manifest
3. Verify:
   - **Scope**: `/jsapp/`
   - **Start URL**: `/jsapp/`

## Recommended Approach

Based on your use case, I recommend:

### If routes are different features of ONE app:
**✅ Keep current configuration** (scope: `/jsapp/`)
- Users install once
- Can access all features within the PWA
- Simpler maintenance
- Better user experience

### If routes are COMPLETELY separate apps:
**✅ Implement Option 1** (Multiple manifests)
- Each route gets its own PWA identity
- Separate install prompts
- Independent updates
- Requires more complex manifest management

## Quick Fix for Specific Route Installation

If you want users who visit `/jsapp/qrpay` to see a PWA specific to QR Pay, update the manifest dynamically:

```javascript
// Add to src/main.js before mounting the app
import { useRoute } from 'vue-router';

// Determine which manifest to use based on current path
const updateManifest = () => {
  const path = window.location.pathname;
  const manifestLink = document.querySelector('link[rel="manifest"]');
  
  if (!manifestLink) return;
  
  if (path.includes('/qrpay')) {
    // Update manifest meta tags for QR Pay
    document.querySelector('meta[name="application-name"]')?.setAttribute('content', 'QR Pay');
    document.querySelector('meta[name="apple-mobile-web-app-title"]')?.setAttribute('content', 'QR Pay');
    document.title = 'QR Pay';
  } else if (path.includes('/scanner')) {
    document.querySelector('meta[name="application-name"]')?.setAttribute('content', 'Scanner');
    document.querySelector('meta[name="apple-mobile-web-app-title"]')?.setAttribute('content', 'Scanner');
    document.title = 'Scanner';
  }
};

updateManifest();
```

## Summary

✅ **Current Configuration**: Scope set to `/jsapp/` - correct for a single-app multi-route architecture  
✅ **Install Behavior**: PWA installs the entire `/jsapp/*` application  
✅ **Start URL**: Always starts at `/jsapp/`, users navigate to sub-routes  
✅ **Isolation**: Main Frappe site (`/`) is separate from the PWA  

If you need different behavior, please see the options above or let me know your specific requirements!

