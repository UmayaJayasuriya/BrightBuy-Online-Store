# Quick Setup Guide - PDF Reports

## Step-by-Step Setup

### 1. Install ReportLab Library

```powershell
cd backend
pip install reportlab
```

### 2. Apply Database Views

```powershell
cd backend
python database/apply_report_views.py
```

Expected output:

```
Applying report views...
✓ Processed: quarterly_sales_report
✓ Processed: top_selling_products
✓ Processed: category_order_summary
✓ Processed: customer_order_payment_summary
✓ Processed: customer_summary_statistics

✅ All report views applied successfully!

📊 Total views in database: 5
  - quarterly_sales_report
  - top_selling_products
  - category_order_summary
  - customer_order_payment_summary
  - customer_summary_statistics
```

### 3. Restart Backend Server

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8020
```

### 4. Test the Endpoints

Open browser: `http://127.0.0.1:8020/docs`

Look for `/reports` section with 5 endpoints:

- ✅ GET `/reports/quarterly-sales/{year}`
- ✅ GET `/reports/top-selling-products`
- ✅ GET `/reports/category-orders`
- ✅ GET `/reports/customer-orders/{user_id}`
- ✅ GET `/reports/all-customers-summary`

### 5. Get Admin Token

1. Go to `/docs` → `/auth/login` endpoint
2. Login with admin credentials
3. Copy the `access_token` from response
4. Click "Authorize" button at top
5. Enter: `Bearer {your_token}`

### 6. Generate Your First Report

1. Find `/reports/quarterly-sales/{year}`
2. Click "Try it out"
3. Enter year: `2025`
4. Click "Execute"
5. Click "Download file" to get PDF

---

## Available Reports

### 1. Quarterly Sales Report

**URL:** `/reports/quarterly-sales/2025`

Shows Q1, Q2, Q3, Q4 breakdown with:

- Total orders per quarter
- Unique customers
- Revenue
- Average order value
- Items sold

### 2. Top Selling Products

**URL:** `/reports/top-selling-products?limit=20`

Optional filters:

- `start_date=2025-01-01`
- `end_date=2025-12-31`
- `limit=20`

### 3. Category Orders

**URL:** `/reports/category-orders`

Shows all categories with:

- Total orders
- Items sold
- Revenue
- Number of products

### 4. Customer Orders (Individual)

**URL:** `/reports/customer-orders/10`

Replace `10` with actual user_id.

Shows:

- Customer info
- All orders
- Payment status
- Delivery status

### 5. All Customers Summary

**URL:** `/reports/all-customers-summary`

Top 50 customers by spending with:

- Total orders
- Total spent
- Payment status
- Delivery status

---

## Troubleshooting

### Error: "reportlab not found"

```powershell
pip install reportlab
```

### Error: "No view named quarterly_sales_report"

```powershell
python database/apply_report_views.py
```

### Error: "Not authenticated"

- Get admin token from `/auth/login`
- Click "Authorize" in `/docs`
- Enter: `Bearer {token}`

### Error: "No data found"

- Check if orders exist in database
- Try different year/date range
- Verify user_id exists

---

## Testing with Sample Data

If you need test data, you can:

1. Create sample orders through the website
2. Or insert test data directly

---

## PDF Features

✅ Professional formatting  
✅ Color-coded tables  
✅ Summary statistics  
✅ Alternating row colors  
✅ Timestamps  
✅ Company branding  
✅ Proper spacing and alignment

---

## Complete Documentation

See `PDF_REPORTS_DOCUMENTATION.md` for:

- Detailed API reference
- View schemas
- Error handling
- Security notes
- Performance tips

---

**Ready to use!** 🎉
