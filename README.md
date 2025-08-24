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

### Using bench get-app (Recommended)

To install this app in any Frappe bench environment:

```bash
bench get-app custom_erp https://github.com/ghimirerohan/erpnextCCDis.git
bench install-app custom_erp
```

### Manual Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd frappe-bench/apps/custom_erp
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Build the frontend:
   ```bash
   npm run build
   ```

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
