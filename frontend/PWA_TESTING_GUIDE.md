# PWA Testing Guide - Scope Configuration

## ✅ What Was Fixed

The PWA scope has been properly configured:

```json
{
  "scope": "/jsapp/",
  "start_url": "/jsapp/",
  "icons": [
    { "src": "/frontend/icons/icon-*.png" }
  ]
}
```

### Key Points:
- **App Scope**: `/jsapp/` (only your Vue app)
- **Icon Path**: `/frontend/icons/` (where assets are built)
- **Start URL**: `/jsapp/` (app entry point)

## 🧪 How to Test

### Step 1: Clear Browser Cache
**IMPORTANT**: Before testing, clear your browser cache and uninstall any previous PWA:

#### On Chrome/Edge:
1. Open DevTools (F12)
2. Go to Application tab
3. Go to "Storage" section
4. Click "Clear site data"
5. If app was previously installed:
   - Go to `chrome://apps` (Chrome) or `edge://apps` (Edge)
   - Right-click the app → Uninstall

#### On Mobile:
1. Uninstall the previously installed app
2. Clear browser cache
3. Close and reopen browser

### Step 2: Test Installation from Different Routes

#### Test A: Install from `/jsapp/`
```
URL: http://localhost:8000/jsapp/
Expected: ✅ Install prompt appears
Expected: ✅ After install, opens at /jsapp/
Expected: ✅ Can navigate to /jsapp/qrpay within PWA
Expected: ✅ Navigating to / opens in browser (outside PWA)
```

#### Test B: Install from `/jsapp/qrpay`
```
URL: http://localhost:8000/jsapp/qrpay
Expected: ✅ Install prompt appears
Expected: ✅ After install, opens at /jsapp/ (start_url)
Expected: ✅ Can navigate to /jsapp/qrpay within PWA
Expected: ✅ All /jsapp/* routes stay in PWA
```

#### Test C: Install from `/jsapp/scanner`
```
URL: http://localhost:8000/jsapp/scanner
Expected: ✅ Install prompt appears
Expected: ✅ After install, opens at /jsapp/ (start_url)
Expected: ✅ Can navigate to /jsapp/scanner within PWA
```

#### Test D: Try from Root `/`
```
URL: http://localhost:8000/
Expected: ❌ Install prompt does NOT appear (outside scope)
Expected: ✅ Main Frappe site works normally
```

### Step 3: Verify Scope in DevTools

1. Open `http://localhost:8000/jsapp/`
2. Open DevTools (F12)
3. Go to **Application** tab
4. Click **Manifest** in left sidebar

**Verify these values:**
```
✅ Name: Frappe ERP
✅ Start URL: /jsapp/
✅ Scope: /jsapp/
✅ Display: standalone
✅ Icons: All 8 icons should be visible (72px to 512px)
```

### Step 4: Test Service Worker

1. Still in DevTools → Application tab
2. Click **Service Workers** in left sidebar

**Verify:**
```
✅ Status: activated and running
✅ Source: /frontend/sw.js
✅ Scope: should cover your app routes
```

### Step 5: Test Offline

1. Visit `http://localhost:8000/jsapp/` while online
2. Navigate to different routes (/jsapp/qrpay, /jsapp/scanner)
3. In DevTools → Network tab, check "Offline"
4. Refresh the page

**Expected:** ✅ App still works offline

### Step 6: Test on Mobile (Android)

1. Open Chrome on Android
2. Navigate to `http://your-ip:8000/jsapp/qrpay`
3. Wait for install banner or tap Menu → "Install app"
4. Install the app
5. Open from home screen

**Expected:**
```
✅ App opens in standalone mode (no browser UI)
✅ App starts at /jsapp/
✅ Can navigate to /jsapp/qrpay
✅ Status bar shows app color (white)
✅ Back button works within app
✅ External links open in browser
```

### Step 7: Test on Mobile (iOS)

1. Open Safari on iOS
2. Navigate to `http://your-ip:8000/jsapp/qrpay`
3. Tap Share button → "Add to Home Screen"
4. Tap "Add"
5. Open from home screen

**Expected:**
```
✅ App opens without Safari UI
✅ App starts at /jsapp/
✅ Shows splash screen briefly
✅ Can navigate to /jsapp/qrpay
✅ Back swipe works
✅ External links open in Safari
```

## 🔍 Troubleshooting

### Issue: Install prompt doesn't appear
**Solutions:**
1. Make sure you're accessing via HTTP/HTTPS (not file://)
2. Clear cache and reload
3. Check DevTools → Console for errors
4. Verify manifest is accessible: `http://localhost:8000/frontend/manifest.webmanifest`
5. Check service worker registered in DevTools → Application

### Issue: App opens at `/` instead of `/jsapp/`
**Solutions:**
1. Verify manifest has `"start_url": "/jsapp/"`
2. Check built manifest at: `/workspace/development/frappe-bench/apps/custom_erp/custom_erp/public/frontend/manifest.webmanifest`
3. Uninstall and reinstall the PWA
4. Clear all site data and try again

### Issue: Icons don't load
**Solutions:**
1. Verify icons exist at: `http://localhost:8000/frontend/icons/icon-192x192.png`
2. Check DevTools → Network tab to see if icons are 404
3. Verify paths in manifest are `/frontend/icons/...`
4. Rebuild: `npm run build`

### Issue: Service worker not registering
**Solutions:**
1. Check Console for errors
2. Verify SW file exists: `http://localhost:8000/frontend/sw.js`
3. Make sure you're using HTTP/HTTPS (not file://)
4. Try unregistering old SW in DevTools → Application → Service Workers

### Issue: App doesn't work offline
**Solutions:**
1. Visit the app online first (to cache assets)
2. Navigate to a few pages before going offline
3. Check DevTools → Application → Cache Storage
4. Verify assets are cached
5. Check Service Worker is active

## 📊 Expected Behavior Summary

| Scenario | Install Prompt | Opens At | Scope |
|----------|---------------|----------|-------|
| Visit `/jsapp/` | ✅ Yes | `/jsapp/` | All `/jsapp/*` |
| Visit `/jsapp/qrpay` | ✅ Yes | `/jsapp/` | All `/jsapp/*` |
| Visit `/jsapp/scanner` | ✅ Yes | `/jsapp/` | All `/jsapp/*` |
| Visit `/` (Frappe root) | ❌ No | N/A | Outside scope |

## 🎯 What This Means

1. **Single App, Multiple Routes**: The PWA treats `/jsapp/qrpay`, `/jsapp/scanner`, etc. as pages of ONE app
2. **Always Starts at `/jsapp/`**: This is intentional - it's the app's home page
3. **Navigate Within App**: Users can navigate to any `/jsapp/*` route after the app opens
4. **Isolation from Frappe**: Main Frappe site at `/` is completely separate

## 💡 If You Need Route-Specific PWAs

If you want `/jsapp/qrpay` to be a **completely separate** installable app that opens directly at that route, you need to:

1. Create multiple manifest files (manifest-qrpay.json, manifest-scanner.json)
2. Set different scopes and start URLs for each
3. Dynamically load the appropriate manifest based on the current route

See `PWA_SCOPE_CONFIGURATION.md` for detailed instructions.

## ✅ Verification Checklist

Before considering this complete, verify:

- [ ] Cleared browser cache and uninstalled old PWA
- [ ] Built with `npm run build`
- [ ] Manifest accessible at `/frontend/manifest.webmanifest`
- [ ] Icons accessible at `/frontend/icons/icon-192x192.png`
- [ ] Scope is `/jsapp/` in DevTools → Application → Manifest
- [ ] Start URL is `/jsapp/` in DevTools → Application → Manifest
- [ ] Service Worker registers successfully
- [ ] Install prompt appears when visiting `/jsapp/*`
- [ ] Install prompt does NOT appear when visiting `/`
- [ ] After install, app opens at `/jsapp/`
- [ ] Can navigate to all `/jsapp/*` routes within PWA
- [ ] External links (`/app`, `/desk`, etc.) open in browser
- [ ] App works offline after first visit
- [ ] Tested on mobile device (Android or iOS)

---

**Current Configuration Status**: ✅ READY TO TEST

Run `npm run build` and test following the steps above!

