# 🐛 Debugging Guide for QRPay Vue App

This guide will help you debug your Vue application with breakpoints directly in VS Code/Cursor.

## ✅ Setup Complete

The following has been configured for you:

1. **Source maps enabled** in `vite.config.js`
2. **VS Code/Cursor debugger configurations** in `.vscode/launch.json`
3. **Editor settings** optimized for Vue development

## 🚀 How to Debug with Breakpoints

### Method 1: One-Click Automated Debug (Recommended) ⚡

**Everything starts automatically - just press F5!**

1. **Open the file you want to debug** (e.g., `src/pages/QRPay.vue`)

2. **Set breakpoints** by clicking in the gutter (left of the line numbers) - a red dot will appear

3. **Press F5** (or click the "Run and Debug" icon in the sidebar)

4. **Select one of the AUTO START configurations**:
   - **"Debug Vue App (Chrome) - Auto Start"** ⭐ RECOMMENDED
   - **"Debug Vue App on Network (Chrome) - Auto Start"** (for 192.168.1.75:8080)

5. **Wait a moment** while:
   - The dev server starts automatically
   - Chrome launches automatically
   - The debugger connects automatically

6. **Debug!**
   - Your breakpoints will hit when the code executes
   - Inspect variables in the "Variables" panel
   - Use the debug toolbar to step through code:
     - **Continue** (F5)
     - **Step Over** (F10)
     - **Step Into** (F11)
     - **Step Out** (Shift+F11)
   - View the call stack, watch expressions, and more

7. **Stop debugging**:
   - Press **Shift+F5** or click the red stop button
   - The dev server will automatically stop too!

### Method 1b: Manual Start Debug (Alternative)

If you prefer to start the dev server manually:

1. **Start the development server first**:
   ```bash
   cd /workspace/development/frappe-bench/apps/custom_erp/frontend
   npm run dev
   ```

2. **Press F5** and select:
   - **"Debug Vue App (Chrome) - Manual Start"**
   - **"Debug Vue App (Edge)"**
   - **"Attach to Chrome"**

### Method 2: Debug in Browser DevTools

1. Start the dev server: `npm run dev`
2. Open your browser and navigate to the app
3. Press **F12** to open DevTools
4. Go to **Sources** tab
5. Find your file in the file tree (webpack:// or vite:// → src → pages → QRPay.vue)
6. Click line numbers to set breakpoints
7. Interact with the app to trigger your breakpoints

### Method 3: Use `debugger` statements

Add `debugger;` directly in your code:

```javascript
const generateQR = async () => {
  debugger; // Execution will pause here when DevTools are open
  if (!canGenerate.value || generating.value) {
    return
  }
  // ...
}
```

## 🎯 Debugging QRPay.vue Specifically

### Key Functions to Debug

Set breakpoints in these functions to understand the payment flow:

- **Line 355**: `generateQR()` - QR code generation
- **Line 433**: `connectMerchantSocket()` - WebSocket connection
- **Line 460**: `ws.onmessage` - WebSocket message handler (payment status updates)
- **Line 665**: `manuallyProcessPayment()` - Manual payment processing
- **Line 603**: `processRealtimeUpdate()` - Realtime update handler

### Common Debugging Scenarios

1. **Payment not being detected?**
   - Set breakpoint at line 460 (WebSocket message handler)
   - Check what messages are being received
   - Inspect `data.transactionStatus` and `data.paymentSuccess`

2. **Customer selection not working?**
   - Set breakpoint at line 303 (watch callback for selectedCustomerValue)
   - Check what value is being passed

3. **QR generation failing?**
   - Set breakpoint at line 355 (generateQR function start)
   - Step through to see where it fails

## 🔍 Debug Tips

1. **Console logs**: Your existing `console.log` statements (lines 292, 304, 440, etc.) help track execution flow

2. **Watch expressions**: Add expressions like `qrStatus.value`, `selectedCustomer.value`, `paymentAmount.value` to the Watch panel

3. **Call stack**: Use the call stack to understand how you got to a breakpoint

4. **Conditional breakpoints**: Right-click a breakpoint and add a condition (e.g., `qrStatus.value === 'SUCCESS'`)

5. **Logpoints**: Right-click in the gutter and select "Add Logpoint" to log without stopping execution

## 🛠️ Troubleshooting

### Breakpoints not hitting?

1. Make sure source maps are enabled (check `vite.config.js` line 185: `sourcemap: true`)
2. Rebuild the app: `npm run build` or restart `npm run dev`
3. Clear browser cache and hard reload (Ctrl+Shift+R)
4. Check that the file path in your breakpoint matches the actual file

### Can't see source files in DevTools?

1. Open DevTools
2. Go to Settings → Preferences
3. Enable "Enable JavaScript source maps"
4. Refresh the page

### Chrome remote debugging not working?

Start Chrome with remote debugging enabled:
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

Then use the "Attach to Chrome" configuration in VS Code.

## 📚 Additional Resources

- [Vue DevTools Extension](https://devtools.vuejs.org/) - Essential for Vue component inspection
- [VS Code Debugging Docs](https://code.visualstudio.com/docs/editor/debugging)
- [Chrome DevTools Docs](https://developer.chrome.com/docs/devtools/)

## 🎉 Happy Debugging!

You're all set to debug your Vue application with breakpoints. Good luck tracking down those bugs! 🐛➡️🎯

