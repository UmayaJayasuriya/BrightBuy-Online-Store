# PDF Reports System Documentation

## Overview

This system generates professionally formatted PDF reports for business analytics using database views and the ReportLab library.

---

## Setup Instructions

### 1. Install Required Dependencies

```bash
cd backend
pip install reportlab
```

Add to `requirements.txt`:

```
reportlab==4.0.7
```

### 2. Apply Database Views

Run the script to create all necessary views:

```bash
cd backend
python database/apply_report_views.py
```

This will create 5 database views:

- ✅ `quarterly_sales_report` - Quarterly sales data
- ✅ `top_selling_products` - Product sales rankings
- ✅ `category_order_summary` - Category-wise statistics
- ✅ `customer_order_payment_summary` - Detailed customer orders
- ✅ `customer_summary_statistics` - Customer aggregate data

### 3. Restart Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8020
```

---

## API Endpoints

All endpoints require **admin authentication** (Bearer token).

### 1. Quarterly Sales Report

**GET** `/reports/quarterly-sales/{year}`

Generate a quarterly sales breakdown for a specific year.

**Parameters:**

- `year` (path parameter): Year to generate report for (e.g., 2025)

**Example:**

```bash
GET http://127.0.0.1:8020/reports/quarterly-sales/2025
Authorization: Bearer {admin_token}
```

**PDF Content:**

- Annual summary (total revenue, orders, average order value)
- Quarterly breakdown table
- Orders, customers, revenue per quarter
- Items sold per quarter

**Download:** `quarterly_sales_2025.pdf`

---

### 2. Top Selling Products Report

**GET** `/reports/top-selling-products`

Generate a report of best-selling products.

**Query Parameters:**

- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `limit` (optional): Number of products to show (default: 20)

**Examples:**

All-time top products:

```bash
GET http://127.0.0.1:8020/reports/top-selling-products?limit=10
```

Date range:

```bash
GET http://127.0.0.1:8020/reports/top-selling-products?start_date=2025-01-01&end_date=2025-12-31&limit=20
```

**PDF Content:**

- Summary (total units, revenue)
- Ranking table with:
  - Product name
  - Category
  - Variant
  - Units sold
  - Total revenue
  - Average price

**Download:** `top_selling_products_{date_range}.pdf`

---

### 3. Category-wise Orders Report

**GET** `/reports/category-orders`

Generate category performance analysis.

**Example:**

```bash
GET http://127.0.0.1:8020/reports/category-orders
Authorization: Bearer {admin_token}
```

**PDF Content:**

- Overall summary (total categories, orders, revenue)
- Category breakdown table:
  - Total orders per category
  - Items sold
  - Total revenue
  - Average order value
  - Number of unique products

**Download:** `category_orders_summary.pdf`

---

### 4. Customer Orders Report (Individual)

**GET** `/reports/customer-orders/{user_id}`

Generate detailed order history for a specific customer.

**Parameters:**

- `user_id` (path parameter): Customer's user ID

**Example:**

```bash
GET http://127.0.0.1:8020/reports/customer-orders/10
Authorization: Bearer {admin_token}
```

**PDF Content:**

- Customer information (name, email, ID)
- Order statistics:
  - Total orders and spending
  - Average order value
  - Completed vs pending payments
  - Delivered orders count
- Detailed orders table:
  - Order ID, date, amount
  - Payment method and status
  - Delivery status
  - Number of items

**Download:** `customer_orders_10.pdf`

---

### 5. All Customers Summary Report

**GET** `/reports/all-customers-summary`

Generate summary of all customers (top 50 by spending).

**Example:**

```bash
GET http://127.0.0.1:8020/reports/all-customers-summary
Authorization: Bearer {admin_token}
```

**PDF Content:**

- Overview (total customers, orders, revenue)
- Customer ranking table:
  - Name and email
  - Total orders
  - Total spending
  - Average order value
  - Completed payments
  - Pending payments

**Download:** `all_customers_summary.pdf`

---

## Database Views

### 1. quarterly_sales_report

```sql
SELECT year, quarter, quarter_label,
       total_orders, unique_customers,
       total_revenue, average_order_value,
       total_items_sold
FROM quarterly_sales_report
WHERE year = 2025;
```

**Columns:**

- `year` - Year
- `quarter` - Quarter number (1-4)
- `quarter_label` - Formatted label (e.g., "Q1 2025")
- `total_orders` - Number of orders
- `unique_customers` - Distinct customers
- `total_revenue` - Sum of order amounts
- `average_order_value` - Average order amount
- `total_items_sold` - Total items sold

---

### 2. top_selling_products

```sql
SELECT * FROM top_selling_products
ORDER BY total_quantity_sold DESC
LIMIT 10;
```

**Columns:**

- `product_id`, `product_name`
- `category_name`
- `variant_id`, `variant_name`, `SKU`
- `total_quantity_sold` - Units sold
- `total_revenue` - Revenue generated
- `average_price` - Average selling price
- `number_of_orders` - Orders containing this product
- `first_sale_date`, `last_sale_date`

---

### 3. category_order_summary

```sql
SELECT * FROM category_order_summary
ORDER BY total_revenue DESC;
```

**Columns:**

- `category_name`, `category_id`
- `total_orders` - Orders in category
- `total_items_sold` - Items sold
- `total_revenue` - Revenue
- `average_order_value` - Average per order
- `unique_products` - Product count
- `first_order_date`, `last_order_date`

---

### 4. customer_order_payment_summary

```sql
SELECT * FROM customer_order_payment_summary
WHERE user_id = 10
ORDER BY order_date DESC;
```

**Columns:**

- User: `user_id`, `user_name`, `email`, `full_name`
- Order: `order_id`, `order_date`, `total_amount`
- Payment: `payment_method`, `payment_status`, `payment_date`
- Delivery: `delivery_status`, `delivery_method`, `estimated_delivery_date`
- Items: `items_in_order`, `total_quantity`

---

### 5. customer_summary_statistics

```sql
SELECT * FROM customer_summary_statistics
ORDER BY total_spent DESC
LIMIT 50;
```

**Columns:**

- User: `user_id`, `user_name`, `email`, `full_name`
- Orders: `total_orders`
- Spending: `total_spent`, `average_order_value`
- Dates: `first_order_date`, `last_order_date`
- Payment: `completed_payments`, `pending_payments`
- Delivery: `delivered_orders`, `pending_deliveries`

---

## PDF Formatting Features

### Design Elements

1. **Professional Header**

   - Large, bold title with company branding
   - Subtitle with report period/description
   - Consistent spacing

2. **Color Scheme**

   - Quarterly Sales: Blue (#3498DB)
   - Top Products: Green (#27AE60)
   - Categories: Red (#E74C3C)
   - Customer Reports: Purple (#9B59B6)
   - All Customers: Dark Gray (#34495E)

3. **Tables**

   - Colored header rows
   - Alternating row backgrounds
   - Grid borders
   - Center-aligned text
   - Proper padding

4. **Summary Statistics**

   - Key metrics highlighted
   - Bold values for emphasis
   - Formatted currency and numbers

5. **Footer**
   - Timestamp of generation
   - Company branding

### Typography

- **Headers:** Helvetica-Bold, 24pt
- **Subtitles:** Regular, 12pt
- **Body Text:** Regular, 10-11pt
- **Table Headers:** Bold, 10-11pt
- **Table Data:** Regular, 8-10pt
- **Footer:** Regular, 8pt

---

## Testing the Reports

### Using cURL

```bash
# Quarterly Sales Report
curl -X GET "http://127.0.0.1:8020/reports/quarterly-sales/2025" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  --output quarterly_sales_2025.pdf

# Top Selling Products (with date range)
curl -X GET "http://127.0.0.1:8020/reports/top-selling-products?start_date=2025-01-01&end_date=2025-12-31&limit=20" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  --output top_products.pdf

# Category Orders
curl -X GET "http://127.0.0.1:8020/reports/category-orders" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  --output category_orders.pdf

# Customer Orders (User ID 10)
curl -X GET "http://127.0.0.1:8020/reports/customer-orders/10" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  --output customer_10_orders.pdf

# All Customers Summary
curl -X GET "http://127.0.0.1:8020/reports/all-customers-summary" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  --output all_customers.pdf
```

### Using Browser

1. Get admin token from login
2. Navigate to: `http://127.0.0.1:8020/docs`
3. Click "Authorize" and enter Bearer token
4. Find `/reports/*` endpoints
5. Click "Try it out" and execute
6. Download the generated PDF

---

## Error Handling

### Common Errors

**404 - No Data Found**

```json
{
  "detail": "No sales data found for year 2025"
}
```

**Solution:** Check if orders exist for the specified period.

**401 - Unauthorized**

```json
{
  "detail": "Not authenticated"
}
```

**Solution:** Ensure admin Bearer token is provided.

**500 - Server Error**

```json
{
  "detail": "Error generating report: [error details]"
}
```

**Solution:** Check database views exist and data is valid.

---

## Maintenance

### Updating Views

To modify a view:

1. Edit `backend/database/views/reports_views.sql`
2. Run: `python backend/database/apply_report_views.py`
3. Restart backend server

### Adding New Reports

1. Create new view in `reports_views.sql`
2. Apply views using the script
3. Add new endpoint in `backend/app/routes/reports.py`
4. Follow existing patterns for:
   - Query execution
   - PDF generation
   - Table styling
   - Error handling

---

## Performance Considerations

1. **Views are indexed** - Fast query performance
2. **Limit large reports** - Use LIMIT clause for customer lists
3. **Date ranges** - Always filter by dates when possible
4. **PDF size** - Large tables may take time to render
5. **Concurrent requests** - Connection pool handles multiple requests

---

## Security

1. ✅ **Admin-only access** - All endpoints require admin authentication
2. ✅ **Input validation** - Date formats and IDs validated
3. ✅ **SQL injection prevention** - Parameterized queries
4. ✅ **Error messages** - Don't expose sensitive data

---

## File Structure

```
backend/
├── app/
│   └── routes/
│       └── reports.py          # PDF generation endpoints
├── database/
│   ├── views/
│   │   └── reports_views.sql   # Database views
│   └── apply_report_views.py   # View installation script
└── requirements.txt             # Add reportlab
```

---

## Next Steps

1. ✅ Install reportlab: `pip install reportlab`
2. ✅ Apply views: `python database/apply_report_views.py`
3. ✅ Restart backend
4. ✅ Test endpoints with admin token
5. ✅ Integrate with frontend (optional)

---

**Version:** 1.0  
**Last Updated:** October 20, 2025  
**Author:** BrightBuy Development Team
