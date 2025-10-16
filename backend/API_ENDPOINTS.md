# BrightBuy API Endpoints - Complete Reference

## 🎉 New Analytics Endpoints (Stored Procedures)

All analytics endpoints are now available at: `http://127.0.0.1:8020/analytics/`

---

## 📋 Table of Contents

1. [Cart Details](#1-cart-details)
2. [Products by Category](#2-products-by-category)
3. [Low Stock Inventory](#3-low-stock-inventory)
4. [Sales Report](#4-sales-report)
5. [Update Order Status](#5-update-order-status)
6. [Top Selling Products](#6-top-selling-products)
7. [Customer Order History](#7-customer-order-history)

---

## 1. Cart Details

### `GET /analytics/cart/{user_id}`

Get complete cart details for a user with product information and stock status.

**Parameters:**
- `user_id` (path) - User ID

**Response:**
```json
{
  "user_id": 1,
  "cart_total": 1999.98,
  "total_items": 2,
  "total_quantity": 3,
  "cart_items": [
    {
      "cart_id": 1,
      "user_id": 1,
      "cart_total": 1999.98,
      "cart_item_id": 1,
      "variant_id": 5,
      "quantity": 2,
      "variant_name": "iPhone 15 Pro 256GB Black",
      "price": 999.99,
      "SKU": "IP15P-256-BLK",
      "stock_available": 50,
      "product_id": 1,
      "product_name": "iPhone 15 Pro",
      "description": "Latest iPhone with A17 Pro chip",
      "category_name": "Smart Phones",
      "item_total": 1999.98,
      "stock_status": "In Stock"
    }
  ],
  "warnings": {
    "out_of_stock_count": 0,
    "low_stock_count": 0,
    "out_of_stock_items": [],
    "low_stock_items": []
  }
}
```

**cURL Example:**
```bash
curl http://127.0.0.1:8020/analytics/cart/1
```

---

## 2. Products by Category

### `GET /analytics/products/category`

Get products by category with pricing information and variant counts.

**Query Parameters:**
- `category_id` (optional) - Category ID (omit for all products)

**Response:**
```json
{
  "category_id": 1,
  "total_products": 15,
  "available_products": 12,
  "out_of_stock_products": 3,
  "products": [
    {
      "product_id": 1,
      "product_name": "iPhone 15 Pro",
      "description": "Latest iPhone",
      "category_id": 1,
      "category_name": "Smart Phones",
      "variant_count": 4,
      "min_price": 899.99,
      "max_price": 1299.99,
      "total_stock": 150,
      "availability_status": "Available"
    }
  ]
}
```

**cURL Examples:**
```bash
# Get products in category 1
curl "http://127.0.0.1:8020/analytics/products/category?category_id=1"

# Get all products
curl "http://127.0.0.1:8020/analytics/products/category"
```

---

## 3. Low Stock Inventory

### `GET /analytics/inventory/low-stock`

Get variants with stock below threshold for inventory management.

**Query Parameters:**
- `threshold` (optional, default: 10) - Stock level threshold

**Response:**
```json
{
  "threshold": 10,
  "total_low_stock_items": 8,
  "summary": {
    "out_of_stock": 2,
    "critical": 3,
    "low": 3,
    "total_value_at_risk": 15420.50
  },
  "low_stock_items": [
    {
      "variant_id": 15,
      "variant_name": "MacBook Pro M3 512GB",
      "current_stock": 3,
      "price": 2499.99,
      "SKU": "MBP-M3-512",
      "product_id": 5,
      "product_name": "MacBook Pro",
      "category_id": 2,
      "category_name": "Laptops",
      "threshold": 10,
      "stock_alert_level": "CRITICAL",
      "sold_last_30_days": 15
    }
  ],
  "urgent_action_required": [
    // Items with CRITICAL or OUT OF STOCK status
  ]
}
```

**cURL Examples:**
```bash
# Default threshold (10)
curl "http://127.0.0.1:8020/analytics/inventory/low-stock"

# Custom threshold
curl "http://127.0.0.1:8020/analytics/inventory/low-stock?threshold=50"
```

---

## 4. Sales Report

### `GET /analytics/sales/report`

Generate comprehensive sales report for a date range.

**Query Parameters:**
- `start_date` (optional, default: 30 days ago) - Start date (YYYY-MM-DD)
- `end_date` (optional, default: today) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "period": {
    "start_date": "2025-09-16",
    "end_date": "2025-10-16",
    "days": 30
  },
  "summary": {
    "total_revenue": 125450.75,
    "total_orders": 342,
    "unique_customers": 156,
    "total_items_sold": 1245,
    "average_daily_revenue": 4181.69,
    "average_daily_orders": 11.4,
    "average_order_value": 366.81
  },
  "payment_breakdown": {
    "card_revenue": 98360.60,
    "cash_revenue": 27090.15,
    "card_percentage": 78.4,
    "cash_percentage": 21.6
  },
  "daily_sales": [
    {
      "sale_date": "2025-10-16",
      "total_orders": 15,
      "unique_customers": 12,
      "total_revenue": 5420.50,
      "average_order_value": 361.37,
      "total_items_sold": 45,
      "top_product": "iPhone 15 Pro",
      "card_revenue": 4200.00,
      "cash_revenue": 1220.50
    }
  ]
}
```

**cURL Examples:**
```bash
# Last 30 days (default)
curl "http://127.0.0.1:8020/analytics/sales/report"

# Specific date range
curl "http://127.0.0.1:8020/analytics/sales/report?start_date=2025-01-01&end_date=2025-10-16"

# Last 7 days
curl "http://127.0.0.1:8020/analytics/sales/report?start_date=2025-10-09&end_date=2025-10-16"
```

---

## 5. Update Order Status

### `PUT /analytics/orders/{order_id}/status`

Update delivery status for an order.

**Parameters:**
- `order_id` (path) - Order ID

**Request Body:**
```json
{
  "status": "Shipped"
}
```

**Valid Statuses:**
- `Pending`
- `Processing`
- `Shipped`
- `Out for Delivery`
- `Delivered`
- `Cancelled`

**Response:**
```json
{
  "success": true,
  "order_id": 1,
  "new_status": "Shipped",
  "message": "Status updated successfully",
  "updated_at": "2025-10-16T18:30:00"
}
```

**cURL Example:**
```bash
curl -X PUT "http://127.0.0.1:8020/analytics/orders/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "Shipped"}'
```

---

## 6. Top Selling Products

### `GET /analytics/products/top-selling`

Get best-selling products by quantity or revenue.

**Query Parameters:**
- `limit` (optional, default: 10, max: 100) - Number of products to return
- `days` (optional, default: 30, max: 365) - Number of days to look back

**Response:**
```json
{
  "period_days": 30,
  "limit": 10,
  "total_products": 10,
  "summary": {
    "total_quantity_sold": 450,
    "total_revenue": 125420.50
  },
  "top_products": [
    {
      "product_id": 1,
      "product_name": "iPhone 15 Pro",
      "category_name": "Smart Phones",
      "times_ordered": 85,
      "total_quantity_sold": 120,
      "total_revenue": 119999.00,
      "average_price": 999.99,
      "lowest_variant_stock": 15
    }
  ]
}
```

**cURL Examples:**
```bash
# Top 10 products (last 30 days)
curl "http://127.0.0.1:8020/analytics/products/top-selling"

# Top 5 products (last 7 days)
curl "http://127.0.0.1:8020/analytics/products/top-selling?limit=5&days=7"

# Top 20 products (last 90 days)
curl "http://127.0.0.1:8020/analytics/products/top-selling?limit=20&days=90"
```

---

## 7. Customer Order History

### `GET /analytics/customers/{user_id}/order-history`

Get complete order history for a customer.

**Parameters:**
- `user_id` (path) - User ID

**Response:**
```json
{
  "user_id": 1,
  "total_orders": 12,
  "summary": {
    "total_spent": 8450.75,
    "total_items_purchased": 35,
    "average_order_value": 704.23
  },
  "order_status_breakdown": {
    "delivered": 9,
    "in_transit": 2,
    "pending": 1
  },
  "orders": [
    {
      "order_id": 15,
      "order_date": "2025-10-14",
      "total_amount": 999.99,
      "delivery_status": "Shipped",
      "delivery_date": null,
      "payment_method": "card",
      "total_items": 2,
      "total_quantity": 3,
      "order_items": "iPhone 15 Pro (256GB Black) x2, AirPods Pro x1",
      "days_since_order": 2
    }
  ]
}
```

**cURL Example:**
```bash
curl "http://127.0.0.1:8020/analytics/customers/1/order-history"
```

---

## 🚀 Testing the Endpoints

### 1. Start the Server
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8020 --reload
```

### 2. Install Stored Procedures (First Time Only)
```bash
cd backend
python database/apply_new_procedures.py
```

### 3. Test Endpoints

**Using Browser:**
- Open: `http://127.0.0.1:8020/docs`
- Interactive API documentation (Swagger UI)

**Using cURL:**
```bash
# Test cart endpoint
curl http://127.0.0.1:8020/analytics/cart/1

# Test low stock
curl "http://127.0.0.1:8020/analytics/inventory/low-stock?threshold=10"

# Test sales report
curl "http://127.0.0.1:8020/analytics/sales/report"
```

**Using Python:**
```python
import requests

# Get cart details
response = requests.get("http://127.0.0.1:8020/analytics/cart/1")
cart = response.json()
print(cart)

# Get low stock items
response = requests.get("http://127.0.0.1:8020/analytics/inventory/low-stock", 
                       params={"threshold": 10})
low_stock = response.json()
print(low_stock)
```

---

## 📊 Frontend Integration Examples

### React/Axios Example

```javascript
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8020/analytics';

// Get cart details
export const getCartDetails = async (userId) => {
  const response = await axios.get(`${API_BASE}/cart/${userId}`);
  return response.data;
};

// Get low stock items
export const getLowStock = async (threshold = 10) => {
  const response = await axios.get(`${API_BASE}/inventory/low-stock`, {
    params: { threshold }
  });
  return response.data;
};

// Get sales report
export const getSalesReport = async (startDate, endDate) => {
  const response = await axios.get(`${API_BASE}/sales/report`, {
    params: { start_date: startDate, end_date: endDate }
  });
  return response.data;
};

// Update order status
export const updateOrderStatus = async (orderId, status) => {
  const response = await axios.put(`${API_BASE}/orders/${orderId}/status`, {
    status
  });
  return response.data;
};

// Get top selling products
export const getTopSelling = async (limit = 10, days = 30) => {
  const response = await axios.get(`${API_BASE}/products/top-selling`, {
    params: { limit, days }
  });
  return response.data;
};

// Get customer order history
export const getOrderHistory = async (userId) => {
  const response = await axios.get(`${API_BASE}/customers/${userId}/order-history`);
  return response.data;
};
```

---

## 🔒 Security Considerations

**Current Status:** All endpoints are public (no authentication)

**Recommended:**
1. Add authentication middleware
2. Protect admin endpoints (sales reports, inventory, order status updates)
3. Validate user access (users can only see their own cart/orders)

**Example Protection:**
```python
from fastapi import Depends, HTTPException
from app.middleware.auth import get_current_user

@router.get("/cart/{user_id}")
def get_cart(user_id: int, current_user = Depends(get_current_user)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # ... rest of code
```

---

## 📈 Performance Tips

1. **Caching:** Cache sales reports and top-selling products
2. **Pagination:** Add pagination for large result sets
3. **Indexes:** Ensure database indexes on frequently queried columns
4. **Connection Pooling:** Already implemented in `database.py`

---

## 🐛 Troubleshooting

### Error: "Procedure not found"
**Solution:** Run `python database/apply_new_procedures.py`

### Error: "Module 'analytics' has no attribute 'router'"
**Solution:** Check that `analytics.py` is in `backend/app/routes/`

### Error: "Database connection failed"
**Solution:** Check `.env` file and ensure MySQL is running

### Empty Results
**Solution:** Check if you have data in the database. Run test data scripts if needed.

---

## ✅ Complete Endpoint List

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/cart/{user_id}` | Get cart details |
| GET | `/analytics/products/category` | Products by category |
| GET | `/analytics/inventory/low-stock` | Low stock alerts |
| GET | `/analytics/sales/report` | Sales analytics |
| PUT | `/analytics/orders/{order_id}/status` | Update order status |
| GET | `/analytics/products/top-selling` | Best sellers |
| GET | `/analytics/customers/{user_id}/order-history` | Order history |

---

**API Documentation:** `http://127.0.0.1:8020/docs`  
**Alternative Docs:** `http://127.0.0.1:8020/redoc`

🎉 **All 7 stored procedure endpoints are now live and ready to use!**
