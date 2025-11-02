# Custom ERP App

A comprehensive ERP application built with Frappe Framework and Vue.js, featuring enhanced sales invoice management capabilities.

## Features

### Sales Invoice Dashboard
- **Filtered Data View**: Filter sales invoices by customer name and date range
- **Two View Modes**:
  - **Bill-wise View**: Shows individual invoices with detailed item breakdowns
  - **Summary View**: Groups invoices by customer and date with aggregated totals
- **Responsive Design**: Beautiful, modern UI that works on all devices
- **Real-time Data**: Live data from ERPNext database

### Key Components

#### Backend API Endpoints
- `get_sales_invoices`: Retrieves filtered sales invoice data
- `get_sales_invoice_summary`: Provides grouped summary data
- `get_customers`: Returns customer list for filter dropdown

#### Frontend Features
- **Filter Section**: Customer dropdown and date range picker
- **View Toggle**: Switch between bill-wise and summary views
- **Data Tables**: Responsive tables with sorting and formatting
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

### Technology Stack
- **Backend**: Frappe Framework (Python)
- **Frontend**: Vue.js 3 with Frappe UI components
- **Styling**: Tailwind CSS
- **Build Tool**: Vite

## Installation

### Automatic Installation (Recommended)

The installation process is **fully automated**. The frontend will be built automatically during installation.

#### For Frappe Manager Users

If you're using [Frappe Manager](https://github.com/rtCamp/Frappe-Manager) to manage your Frappe instances:

```bash
# In your Frappe Manager environment
fm shell [your-site-name]
bench get-app custom_erp https://github.com/ghimirerohan/erpnextCCDis.git
bench install-app custom_erp
```

The installation hook will automatically:
- ✅ Check HRMS dependencies (Driver & Vehicle doctypes)
- ✅ Build the frontend with all PWA assets
- ✅ Verify custom fields installation
- ✅ Verify frontend build output

**Requirements:**
- Node.js and npm must be available in your container/environment
- HRMS app should be installed for Driver/Vehicle fields to work

#### Standard Bench Installation

```bash
bench get-app custom_erp https://github.com/ghimirerohan/erpnextCCDis.git
bench install-app custom_erp
```

The installation is fully automatic - no manual steps required!

### Manual Installation (Fallback)

If automatic installation fails, you can manually build the frontend:

1. Clone the repository
2. Build the frontend:
   ```bash
   cd frappe-bench/apps/custom_erp/frontend
   npm ci --no-audit --no-fund --prefer-offline
   npm run build
   ```
3. Install backend dependencies:
   ```bash
   cd ../custom_erp
   pip install -r requirements.txt
   ```
4. Install the app:
   ```bash
   bench --site [your-site-name] install-app custom_erp
   ```

### Post-Installation Verification

After installation, verify everything is working:

```bash
# Check custom fields were created
bench --site [your-site-name] console
>>> import frappe
>>> frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_driver_for_vehicle"})
True
>>> frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_vehicle_for_delivery"})
True

# Check frontend build
>>> import os
>>> os.path.exists("apps/custom_erp/custom_erp/public/frontend/index.html")
True
```

### Troubleshooting Installation

#### Frontend Build Fails

**Error:** `Node.js not found` or `npm not found`
- **Solution:** Install Node.js (v16 or higher) in your environment
- **For Docker/Frappe Manager:** Ensure Node.js is available in the container

**Error:** `Frontend build timed out`
- **Solution:** This usually indicates resource constraints. Increase memory/CPU allocation or build manually

**Error:** `Frontend build failed with errors`
- **Solution:** Check the error output. Common issues:
  - Missing dependencies: Run `npm ci` manually
  - Permission issues: Check file permissions
  - Disk space: Ensure sufficient disk space

#### Custom Fields Not Created

**Issue:** Driver/Vehicle fields not visible in Sales Invoice
- **Check:** Verify HRMS is installed (Driver and Vehicle doctypes exist)
- **Fix:** Install HRMS app if missing: `bench get-app hrms`
- **Re-run:** `bench --site [site-name] migrate`

#### HRMS Dependency Warnings

**Warning:** `Driver doctype not found` or `Vehicle doctype not found`
- **Impact:** Custom fields will be created but won't work until HRMS is installed
- **Solution:** Install HRMS app before using Driver/Vehicle features

### Configuration

#### Fonepay Credentials Setup

To use Fonepay payment integration, add the following configuration to your site's `site_config.json` file:

**Location:** `frappe-bench/sites/[your-site-name]/site_config.json`

```json
{
  "fonepay": {
    "merchant_code": "YOUR_MERCHANT_CODE",
    "secret_key": "YOUR_SECRET_KEY",
    "username": "YOUR_USERNAME@fonepay.com",
    "password": "YOUR_PASSWORD",
    "env": "live",
    "ws_worker": "inprocess",
    "ws_timeout_seconds": 300,
    "scheduled_batch_size": 50,
    "scheduled_sleep_between": 0.2
  }
}
```

**Configuration Parameters:**

- `merchant_code`: Your Fonepay merchant code
- `secret_key`: Your Fonepay secret key for HMAC signing
- `username`: Your Fonepay merchant username (format: `username@fonepay.com`)
- `password`: Your Fonepay merchant password
- `env`: Environment mode - use `"live"` for production or `"dev"` for development/testing
- `ws_worker`: WebSocket worker type - `"inprocess"` for single-process, or `"celery"` for distributed
- `ws_timeout_seconds`: WebSocket connection timeout (default: 300 seconds)
- `scheduled_batch_size`: Batch size for scheduled payment processing (default: 50)
- `scheduled_sleep_between`: Sleep interval between batches in seconds (default: 0.2)

**Example (Production):**
```json
{
  "fonepay": {
    "merchant_code": "2005260033",
    "secret_key": "your-secret-key-here",
    "username": "yourusername@fonepay.com",
    "password": "YourSecurePassword",
    "env": "live",
    "ws_worker": "inprocess",
    "ws_timeout_seconds": 300,
    "scheduled_batch_size": 50,
    "scheduled_sleep_between": 0.2
  }
}
```

**Security Note:** Keep your `site_config.json` file secure and never commit it to version control. The `.gitignore` should exclude `site_config.json` files.

#### CSRF Configuration for Production

**Important for Production Deployments:** When deploying to production, you may need to configure CSRF settings based on your deployment architecture.

**Understanding CSRF in Frappe:**
- Frappe Framework includes CSRF (Cross-Site Request Forgery) protection by default
- All API endpoints marked with `@frappe.whitelist()` are automatically protected
- Frontend apps making API calls must include CSRF tokens in requests

**Configuration Options:**

1. **Standard Configuration (Recommended for Most Cases):**
   - All API endpoints in this app are properly whitelisted
   - Frappe UI automatically handles CSRF tokens
   - No additional configuration needed

2. **Production with `ignore_csrf` (Use with Caution):**
   
   In some production scenarios (e.g., reverse proxy, load balancer, or specific network configurations), you may encounter CSRF issues. If necessary, you can disable CSRF checking:
   
   **Location:** `frappe-bench/sites/[your-site-name]/site_config.json`
   
   ```json
   {
     "ignore_csrf": 1
   }
   ```
   
   **⚠️ Security Warning:** Only use `ignore_csrf: 1` if:
   - You have other security measures in place (WAF, API gateway, etc.)
   - You fully understand the security implications
   - You're behind a trusted network/proxy
   - Alternative solutions don't work
   
   **Better Alternatives:**
   - Configure your reverse proxy/load balancer properly
   - Ensure CSRF tokens are properly forwarded
   - Use proper CORS configuration
   - Consider using API keys for external integrations

3. **Verifying CSRF Configuration:**
   
   Check if CSRF is being enforced:
   ```bash
   bench --site [your-site-name] console
   >>> import frappe
   >>> frappe.conf.get("ignore_csrf")
   # Returns 1 if CSRF is disabled, 0 or None if enabled
   ```
   
   All whitelisted methods in this app:
   - ✅ All Fonepay API endpoints (`custom_erp.custom_erp.api.fonepay.*`)
   - ✅ All UploadSales API endpoints (`custom_erp.custom_erp.api.uploadsales.*`)
   
   These endpoints work with or without `ignore_csrf` setting, as they're properly decorated with `@frappe.whitelist()`.

## Frontend App Installation

The frontend app is included in the `frontend/` directory and will be automatically installed when you install the main app. However, if you need to set up the frontend separately:

```bash
cd frontend
npm install
npm run build
```

### Frontend Development

To run the frontend in development mode:

```bash
cd frontend
npm run dev
```

This will start the Vite development server on `http://localhost:5173`.

## Development

### Running the Frontend
```bash
cd frontend
npm run dev
```

### API Endpoints

#### Get Sales Invoices
```
POST /api/method/custom_erp.custom_erp.sales_invoice.api.get_sales_invoices
```

Parameters:
- `filters`: JSON object with customer, from_date, to_date

#### Get Sales Invoice Summary
```
POST /api/method/custom_erp.custom_erp.sales_invoice.api.get_sales_invoice_summary
```

#### Get Customers
```
POST /api/method/custom_erp.custom_erp.sales_invoice.api.get_customers
```

## UI Components Used

- **Button**: Primary action buttons with loading states
- **Alert**: Error and success message display
- **Badge**: Status indicators for invoice states
- **Form Controls**: Input fields and select dropdowns

## Responsive Design

The dashboard is fully responsive with:
- Mobile-first design approach
- Flexible grid layouts
- Touch-friendly interface elements
- Optimized table scrolling for mobile devices

## Data Formatting

- **Currency**: Properly formatted currency values
- **Dates**: Localized date display
- **Status**: Color-coded status badges
- **Numbers**: Formatted quantities and amounts

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
