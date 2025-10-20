# Test Commands for PDF Reports

## Setup Commands

```powershell
# Navigate to backend
cd "C:\UOM\CSE - 3rd semester\FastApi\BrightBuy-Online-Store\backend"

# Install reportlab
pip install reportlab

# Apply database views
python database/apply_report_views.py

# Start server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8020
```

---

## Test with cURL (After getting admin token)

### Get Admin Token First

```powershell
# Login as admin
curl -X POST "http://127.0.0.1:8020/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'

# Copy the access_token from response
```

### 1. Quarterly Sales Report

```powershell
curl -X GET "http://127.0.0.1:8020/reports/quarterly-sales/2025" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o quarterly_sales_2025.pdf
```

### 2. Top Selling Products (All Time)

```powershell
curl -X GET "http://127.0.0.1:8020/reports/top-selling-products?limit=10" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o top_products.pdf
```

### 3. Top Selling Products (Date Range)

```powershell
curl -X GET "http://127.0.0.1:8020/reports/top-selling-products?start_date=2025-01-01&end_date=2025-12-31&limit=20" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o top_products_2025.pdf
```

### 4. Category Orders

```powershell
curl -X GET "http://127.0.0.1:8020/reports/category-orders" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o category_orders.pdf
```

### 5. Customer Orders (User ID 10)

```powershell
curl -X GET "http://127.0.0.1:8020/reports/customer-orders/10" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o customer_10_orders.pdf
```

### 6. All Customers Summary

```powershell
curl -X GET "http://127.0.0.1:8020/reports/all-customers-summary" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -o all_customers.pdf
```

---

## Test with Browser (Swagger UI)

1. Open: http://127.0.0.1:8020/docs

2. Login to get token:

   - Go to `/auth/login`
   - Click "Try it out"
   - Enter admin credentials
   - Copy `access_token`

3. Authorize:

   - Click "Authorize" button (top right)
   - Enter: `Bearer YOUR_TOKEN`
   - Click "Authorize"

4. Test endpoints:
   - Find `/reports` section
   - Click any endpoint
   - Click "Try it out"
   - Fill parameters
   - Click "Execute"
   - Click "Download file"

---

## Verify Database Views

```powershell
# Run Python script to verify
python -c "
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'brightbuy')
)

cursor = conn.cursor()
cursor.execute(\"SHOW FULL TABLES WHERE Table_type = 'VIEW'\")
views = cursor.fetchall()

print('Database Views:')
for view in views:
    print(f'  ✓ {view[0]}')

cursor.close()
conn.close()
"
```

Expected output:

```
Database Views:
  ✓ quarterly_sales_report
  ✓ top_selling_products
  ✓ category_order_summary
  ✓ customer_order_payment_summary
  ✓ customer_summary_statistics
```

---

## Test View Queries

```sql
-- Test quarterly sales
SELECT * FROM quarterly_sales_report WHERE year = 2025;

-- Test top products
SELECT * FROM top_selling_products LIMIT 10;

-- Test categories
SELECT * FROM category_order_summary;

-- Test customer summary
SELECT * FROM customer_summary_statistics LIMIT 5;

-- Test customer orders
SELECT * FROM customer_order_payment_summary WHERE user_id = 10;
```

---

## Troubleshooting

### Error: "reportlab not found"

```powershell
pip install reportlab
pip list | Select-String reportlab
```

### Error: "View doesn't exist"

```powershell
python database/apply_report_views.py
```

### Error: "Not authenticated"

```powershell
# Make sure to:
# 1. Login as admin
# 2. Copy access_token
# 3. Add header: Authorization: Bearer {token}
```

### Error: "No data found"

```sql
-- Check if orders exist
SELECT COUNT(*) FROM orders;

-- Check if order_items exist
SELECT COUNT(*) FROM order_item;

-- Check specific year
SELECT COUNT(*) FROM orders WHERE YEAR(order_date) = 2025;
```

---

## Expected PDF Files

After running all tests, you should have:

```
📄 quarterly_sales_2025.pdf
📄 top_products.pdf
📄 top_products_2025.pdf
📄 category_orders.pdf
📄 customer_10_orders.pdf
📄 all_customers.pdf
```

Each PDF should be:

- ✅ Properly formatted
- ✅ Professional looking
- ✅ Color-coded tables
- ✅ Readable text
- ✅ Proper spacing
- ✅ Company branding

---

## Quick Test Script

Save as `test_reports.ps1`:

```powershell
# Test all report endpoints
$token = "YOUR_ADMIN_TOKEN_HERE"
$base_url = "http://127.0.0.1:8020/reports"

Write-Host "Testing PDF Reports..." -ForegroundColor Cyan

# Test 1
Write-Host "1. Quarterly Sales..." -ForegroundColor Yellow
curl -X GET "$base_url/quarterly-sales/2025" `
  -H "Authorization: Bearer $token" `
  -o quarterly_sales.pdf
Write-Host "✓ Done" -ForegroundColor Green

# Test 2
Write-Host "2. Top Products..." -ForegroundColor Yellow
curl -X GET "$base_url/top-selling-products?limit=10" `
  -H "Authorization: Bearer $token" `
  -o top_products.pdf
Write-Host "✓ Done" -ForegroundColor Green

# Test 3
Write-Host "3. Category Orders..." -ForegroundColor Yellow
curl -X GET "$base_url/category-orders" `
  -H "Authorization: Bearer $token" `
  -o category_orders.pdf
Write-Host "✓ Done" -ForegroundColor Green

# Test 4
Write-Host "4. Customer Orders..." -ForegroundColor Yellow
curl -X GET "$base_url/customer-orders/10" `
  -H "Authorization: Bearer $token" `
  -o customer_orders.pdf
Write-Host "✓ Done" -ForegroundColor Green

# Test 5
Write-Host "5. All Customers..." -ForegroundColor Yellow
curl -X GET "$base_url/all-customers-summary" `
  -H "Authorization: Bearer $token" `
  -o all_customers.pdf
Write-Host "✓ Done" -ForegroundColor Green

Write-Host "`nAll tests complete! Check PDF files." -ForegroundColor Cyan
```

Run with:

```powershell
# Update token in script, then:
.\test_reports.ps1
```

---

**Ready to test!** 🚀
