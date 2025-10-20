# BrightBuy Stored Procedures Documentation

## 📋 Overview

This document provides a complete reference of all stored procedures in the BrightBuy Online Store application, including their locations, parameters, return values, and usage examples.

**Last Updated**: October 20, 2025  
**Database**: MySQL 8.0 (brightbuy)

---

## ⚡ Quick Answer: Are These Procedures Actually Used?

**YES! They are actively used in your running application.** Here's the breakdown:

### ✅ **Currently Active in Production** (7 procedures):

These procedures are called through the `/analytics` API endpoints and are accessible in your live application:

1. **GetUserCart** - Used by analytics endpoint, can be accessed at `GET /analytics/cart/{user_id}`
2. **GetProductsByCategory** - Used by analytics endpoint, can be accessed at `GET /analytics/products/category`
3. **GetLowStockVariants** - Used by analytics endpoint, can be accessed at `GET /analytics/inventory/low-stock`
4. **GetSalesReport** - Used by analytics endpoint, can be accessed at `GET /analytics/sales/report`
5. **UpdateOrderStatus** - **ACTIVELY USED BY FRONTEND!** Called from `Admin.jsx` line 217 to mark orders as delivered
6. **GetTopSellingProducts** - Used by analytics endpoint, can be accessed at `GET /analytics/products/top-selling`
7. **GetCustomerOrderHistory** - Used by analytics endpoint, can be accessed at `GET /analytics/customers/{user_id}/order-history`

### ⚠️ **Available But Not Currently Used** (2 procedures):

These are defined in the database but not actively called in your current application:

1. **AddUserWithAddress** - Code exists but is commented out in `user.py`
2. **GetOrderSummary** - Only used in test scripts, not in production routes

### 🎯 **Confirmed Frontend Usage**:

- **Admin Dashboard** (`frontend/src/pages/Admin.jsx` line 217) uses `UpdateOrderStatus` procedure to mark orders as delivered
- The analytics router is registered in `main.py` (line 53), making all 7 analytics procedures accessible
- API is running on `http://127.0.0.1:8020`

### 📊 **Architecture Flow**:

```
┌─────────────────────┐
│   Frontend (React)  │
│   Admin.jsx         │
└──────────┬──────────┘
           │ HTTP PUT Request
           │ /analytics/orders/1/status
           ▼
┌─────────────────────┐
│   Backend (FastAPI) │
│   analytics.py      │
│   Line 415          │
└──────────┬──────────┘
           │ CALL UpdateOrderStatus(1, 'Delivered')
           ▼
┌─────────────────────┐
│   Database (MySQL)  │
│   Stored Procedure  │
│   UpdateOrderStatus │
└─────────────────────┘
```

**This means**: When an admin clicks "Mark as Delivered" in your admin dashboard, it triggers a chain that ultimately calls the `UpdateOrderStatus` stored procedure in your MySQL database!

---

## 📦 Table of Contents

1. [Stored Procedures List](#stored-procedures-list)
2. [Detailed Documentation](#detailed-documentation)
3. [Usage in Backend Routes](#usage-in-backend-routes)
4. [Testing Files](#testing-files)
5. [Quick Reference](#quick-reference)

---

## Stored Procedures List

| #   | Procedure Name            | Purpose                                     | Used In                                                                                                                                 | Status                    |
| --- | ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | `AddUserWithAddress`      | Create user with address in one transaction | `backend/app/routes/user.py` (commented out)                                                                                            | ⚠️ Not Active             |
| 2   | `GetOrderSummary`         | Get user's order history with details       | `backend/database/test_order_summary_procedure.py`, `backend/database/debug_order_summary.py`, `backend/database/check_users_orders.py` | ⚠️ Testing Only           |
| 3   | `GetUserCart`             | Get complete cart details with stock status | `backend/app/routes/analytics.py` (line 131)                                                                                            | ✅ **ACTIVE**             |
| 4   | `GetProductsByCategory`   | Get products by category with pricing       | `backend/app/routes/analytics.py` (line 195)                                                                                            | ✅ **ACTIVE**             |
| 5   | `GetLowStockVariants`     | Identify low stock inventory items          | `backend/app/routes/analytics.py` (line 248)                                                                                            | ✅ **ACTIVE**             |
| 6   | `GetSalesReport`          | Generate sales report for date range        | `backend/app/routes/analytics.py` (line 321)                                                                                            | ✅ **ACTIVE**             |
| 7   | `UpdateOrderStatus`       | Update order delivery status                | `backend/app/routes/analytics.py` (line 415) + **`Admin.jsx` (line 217)**                                                               | ✅ **ACTIVE IN FRONTEND** |
| 8   | `GetTopSellingProducts`   | Get best-selling products                   | `backend/app/routes/analytics.py` (line 491)                                                                                            | ✅ **ACTIVE**             |
| 9   | `GetCustomerOrderHistory` | Get customer's complete order history       | `backend/app/routes/analytics.py` (line 546)                                                                                            | ✅ **ACTIVE**             |

---

## Detailed Documentation

### 1. AddUserWithAddress

**Purpose**: Create a user and their address in a single atomic transaction.

**Location**: `backend/app/database/exports/procedures_20251016_165400.sql`

**Parameters**:

```sql
IN p_user_id INT
IN p_user_name VARCHAR(50)
IN p_email VARCHAR(100)
IN p_name VARCHAR(50)
IN p_password_hash VARCHAR(100)
IN p_user_type VARCHAR(30)
IN p_city_id INT
IN p_house_number INT
IN p_street VARCHAR(100)
IN p_city VARCHAR(100)
IN p_state VARCHAR(100)
```

**Returns**: None (performs INSERT operations)

**Logic**:

1. Insert address into `Address` table
2. Get the new `address_id` using `LAST_INSERT_ID()`
3. Insert user into `User` table with the new `address_id`

**Used In**:

- `backend/app/routes/user.py` - Line 40 (commented as "Step 2: Call stored procedure")

**Example Usage**:

```python
# In user.py (commented out)
cursor.execute(
    "CALL AddUserWithAddress(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (user_id, username, email, name, password_hash, user_type,
     city_id, house_number, street, city, state)
)
```

**Status**: ⚠️ Currently not active (code is commented out in user.py)

**Note**: This procedure exists in the database but is not being called in the current production code. The user creation logic in `user.py` currently uses direct SQL queries instead of this procedure.

---

### 2. GetOrderSummary

**Purpose**: Retrieve comprehensive order summary for a specific user.

**Location**:

- Definition: `backend/app/database/exports/procedures_20251016_165400.sql`
- Creation script: `backend/database/apply_order_summary_procedure.py`

**Parameters**:

```sql
IN p_user_id INT
```

**Returns**:

```sql
order_id          INT
order_date        DATE
total_amount      DECIMAL
quantity          INT
price             DECIMAL
product_name      VARCHAR
variant_name      VARCHAR
delivery_status   VARCHAR
```

**Logic**:

- Joins: `orders` → `order_item` → `variant` → `product` → `delivery`
- Filters by `user_id`
- Orders by `order_date DESC`

**Used In**:

1. `backend/database/test_order_summary_procedure.py` - Line 25
2. `backend/database/debug_order_summary.py` - Line 24
3. `backend/database/check_users_orders.py` - Line 50

**Example Usage**:

```python
cursor.execute("CALL GetOrderSummary(%s)", (user_id,))
results = cursor.fetchall()

for row in results:
    print(f"Order #{row['order_id']}: {row['product_name']} - {row['delivery_status']}")
```

**Status**: ⚠️ Testing only - Not used in production routes

**Note**: This procedure is only called in testing scripts. It's not exposed through any API endpoint in the running application. The main order fetching logic uses different queries in `order.py` and `admin.py`.

---

### 3. GetUserCart

**Purpose**: Get complete cart details with product info and stock availability.

**Location**: Part of analytics stored procedures

**Parameters**:

```sql
IN p_user_id INT
```

**Returns**:

```sql
cart_id           INT
user_id           INT
cart_total        DECIMAL
cart_item_id      INT
variant_id        INT
quantity          INT
variant_name      VARCHAR
price             DECIMAL
SKU               VARCHAR
stock_available   INT
product_id        INT
product_name      VARCHAR
description       TEXT
category_name     VARCHAR
item_total        DECIMAL
stock_status      VARCHAR  -- 'In Stock' / 'Limited Stock' / 'Out of Stock'
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 131
  - Endpoint: `GET /analytics/cart/{user_id}`
  - Function: `get_user_cart_details()`

**Example Usage**:

```python
@router.get("/analytics/cart/{user_id}")
def get_user_cart_details(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetUserCart(%s)", (user_id,))
    cart_items = cursor.fetchall()

    total_items = len([item for item in cart_items if item.get('cart_item_id')])
    out_of_stock = [item for item in cart_items if item.get('stock_status') == 'Out of Stock']

    return {
        "cart_total": cart_items[0].get('cart_total', 0),
        "total_items": total_items,
        "cart_items": cart_items,
        "warnings": {
            "out_of_stock_count": len(out_of_stock)
        }
    }
```

**Status**: ✅ **ACTIVE** - Analytics endpoint available

**Real-World Usage**: This endpoint can be accessed at `http://127.0.0.1:8020/analytics/cart/{user_id}` and provides detailed cart information including stock status warnings.

---

### 4. GetProductsByCategory

**Purpose**: Get all products in a category with pricing and availability information.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_category_id INT  -- NULL for all products
```

**Returns**:

```sql
product_id            INT
product_name          VARCHAR
description           TEXT
category_id           INT
category_name         VARCHAR
variant_count         INT
min_price             DECIMAL
max_price             DECIMAL
total_stock           INT
availability_status   VARCHAR  -- 'Available' / 'Out of Stock'
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 195
  - Endpoint: `GET /analytics/products/category`
  - Function: `get_products_by_category()`

**Example Usage**:

```python
# Get products in category 1
cursor.execute("CALL GetProductsByCategory(%s)", (1,))

# Get all products
cursor.execute("CALL GetProductsByCategory(%s)", (None,))
```

**Status**: ✅ Active - Analytics endpoint

---

### 5. GetLowStockVariants

**Purpose**: Identify product variants below stock threshold for inventory management.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_threshold INT  -- Stock level threshold (default: 10)
```

**Returns**:

```sql
variant_id           INT
variant_name         VARCHAR
current_stock        INT
price                DECIMAL
SKU                  VARCHAR
product_id           INT
product_name         VARCHAR
category_id          INT
category_name        VARCHAR
threshold            INT
stock_alert_level    VARCHAR  -- 'OUT OF STOCK' / 'CRITICAL' / 'LOW'
sold_last_30_days    INT
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 248
  - Endpoint: `GET /analytics/inventory/low-stock`
  - Function: `get_low_stock_variants()`

**Example Usage**:

```python
@router.get("/analytics/inventory/low-stock")
def get_low_stock_variants(threshold: int = 10, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetLowStockVariants(%s)", (threshold,))
    low_stock_items = cursor.fetchall()

    # Categorize by alert level
    out_of_stock = [item for item in low_stock_items
                    if item.get('stock_alert_level') == 'OUT OF STOCK']
    critical = [item for item in low_stock_items
                if item.get('stock_alert_level') == 'CRITICAL']

    return {
        "threshold": threshold,
        "total_low_stock_items": len(low_stock_items),
        "urgent_action_required": out_of_stock + critical
    }
```

**Status**: ✅ Active - Analytics endpoint

---

### 6. GetSalesReport

**Purpose**: Generate comprehensive daily sales report for a date range.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_start_date DATE  -- Default: 30 days ago
IN p_end_date DATE    -- Default: today
```

**Returns**:

```sql
sale_date              DATE
total_orders           INT
unique_customers       INT
total_revenue          DECIMAL
average_order_value    DECIMAL
total_items_sold       INT
top_product            VARCHAR
card_revenue           DECIMAL
cash_revenue           DECIMAL
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 321
  - Endpoint: `GET /analytics/sales/report`
  - Function: `get_sales_report()`

**Example Usage**:

```python
from datetime import date, timedelta

@router.get("/analytics/sales/report")
def get_sales_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db=Depends(get_db)
):
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()

    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetSalesReport(%s, %s)", (start_date, end_date))
    daily_sales = cursor.fetchall()

    total_revenue = sum(float(day['total_revenue'] or 0) for day in daily_sales)
    total_orders = sum(int(day['total_orders'] or 0) for day in daily_sales)

    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "summary": {"total_revenue": total_revenue, "total_orders": total_orders},
        "daily_sales": daily_sales
    }
```

**Status**: ✅ Active - Analytics endpoint

---

### 7. UpdateOrderStatus

**Purpose**: Update the delivery status of an order.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_order_id INT
IN p_new_status VARCHAR
```

**Valid Status Values**:

- `Pending`
- `Processing`
- `Shipped`
- `Out for Delivery`
- `Delivered`
- `Cancelled`

**Returns**:

```sql
message        VARCHAR
order_id       INT
new_status     VARCHAR
updated_at     TIMESTAMP
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 415
  - Endpoint: `PUT /analytics/orders/{order_id}/status`
  - Function: `update_order_status()`

**Example Usage**:

```python
@router.put("/analytics/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db=Depends(get_db)
):
    valid_statuses = ['Pending', 'Processing', 'Shipped',
                      'Out for Delivery', 'Delivered', 'Cancelled']

    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL UpdateOrderStatus(%s, %s)",
                   (order_id, status_update.status))
    result = cursor.fetchone()
    db.commit()

    return {
        "success": True,
        "order_id": order_id,
        "new_status": status_update.status
    }
```

**Status**: ✅ Active - Analytics endpoint (with fallback to direct UPDATE)

---

### 8. GetTopSellingProducts

**Purpose**: Analyze and return best-selling products by quantity or revenue.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_limit INT  -- Number of products to return (default: 10, max: 100)
IN p_days INT   -- Look-back period in days (default: 30, max: 365)
```

**Returns**:

```sql
product_id            INT
product_name          VARCHAR
category_name         VARCHAR
times_ordered         INT
total_quantity_sold   INT
total_revenue         DECIMAL
average_price         DECIMAL
lowest_variant_stock  INT
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 491
  - Endpoint: `GET /analytics/products/top-selling`
  - Function: `get_top_selling_products()`

**Example Usage**:

```python
@router.get("/analytics/products/top-selling")
def get_top_selling_products(
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(30, ge=1, le=365),
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetTopSellingProducts(%s, %s)", (limit, days))
    top_products = cursor.fetchall()

    total_quantity_sold = sum(int(p['total_quantity_sold'] or 0)
                              for p in top_products)
    total_revenue = sum(float(p['total_revenue'] or 0)
                        for p in top_products)

    return {
        "period_days": days,
        "limit": limit,
        "summary": {
            "total_quantity_sold": total_quantity_sold,
            "total_revenue": round(total_revenue, 2)
        },
        "top_products": top_products
    }
```

**Status**: ✅ Active - Analytics endpoint (BONUS feature)

---

### 9. GetCustomerOrderHistory

**Purpose**: Get complete order history for a customer with delivery and payment details.

**Location**: Analytics stored procedures

**Parameters**:

```sql
IN p_user_id INT
```

**Returns**:

```sql
order_id          INT
order_date        DATE
total_amount      DECIMAL
delivery_status   VARCHAR
delivery_date     DATE
payment_method    VARCHAR
total_items       INT
total_quantity    INT
order_items       TEXT  -- Comma-separated list
days_since_order  INT
```

**Used In**:

- `backend/app/routes/analytics.py` - Line 546
  - Endpoint: `GET /analytics/customers/{user_id}/order-history`
  - Function: `get_customer_order_history()`

**Example Usage**:

```python
@router.get("/analytics/customers/{user_id}/order-history")
def get_customer_order_history(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetCustomerOrderHistory(%s)", (user_id,))
    orders = cursor.fetchall()

    total_orders = len(orders)
    total_spent = sum(float(order['total_amount'] or 0) for order in orders)

    # Order status breakdown
    delivered = len([o for o in orders if o['delivery_status'] == 'Delivered'])
    pending = len([o for o in orders if o['delivery_status'] in ['Pending', 'Processing']])

    return {
        "user_id": user_id,
        "total_orders": total_orders,
        "summary": {
            "total_spent": round(total_spent, 2),
            "average_order_value": round(total_spent / total_orders, 2) if total_orders > 0 else 0
        },
        "order_status_breakdown": {
            "delivered": delivered,
            "pending": pending
        },
        "orders": orders
    }
```

**Status**: ✅ Active - Analytics endpoint (BONUS feature)

---

## Usage in Backend Routes

### Analytics Router (`backend/app/routes/analytics.py`)

The analytics router provides RESTful API endpoints for all stored procedures:

| Endpoint                                       | Method | Procedure                 | Description                        |
| ---------------------------------------------- | ------ | ------------------------- | ---------------------------------- |
| `/analytics/cart/{user_id}`                    | GET    | `GetUserCart`             | Get cart details with stock status |
| `/analytics/products/category`                 | GET    | `GetProductsByCategory`   | List products by category          |
| `/analytics/inventory/low-stock`               | GET    | `GetLowStockVariants`     | Inventory management               |
| `/analytics/sales/report`                      | GET    | `GetSalesReport`          | Sales analytics report             |
| `/analytics/orders/{order_id}/status`          | PUT    | `UpdateOrderStatus`       | Update order status                |
| `/analytics/products/top-selling`              | GET    | `GetTopSellingProducts`   | Best sellers analysis              |
| `/analytics/customers/{user_id}/order-history` | GET    | `GetCustomerOrderHistory` | Customer order history             |

**Base URL**: `http://127.0.0.1:8020/analytics`

**Authentication**: Not currently enforced (should add `Depends(get_current_user)` for production)

---

## Testing Files

### 1. `backend/database/test_order_summary_procedure.py`

**Purpose**: Test the `GetOrderSummary` stored procedure

**Key Code**:

```python
cursor.execute("CALL GetOrderSummary(%s)", (test_user_id,))
results = cursor.fetchall()
```

**Usage**: `python backend/database/test_order_summary_procedure.py`

---

### 2. `backend/database/debug_order_summary.py`

**Purpose**: Debug and verify `GetOrderSummary` with detailed output

**Key Code**:

```python
cursor.execute("CALL GetOrderSummary(%s)", (test_user_id,))
results = cursor.fetchall()
print(f"Found {len(results)} orders for user {test_user_id}")
```

**Usage**: `python backend/database/debug_order_summary.py`

---

### 3. `backend/database/check_users_orders.py`

**Purpose**: Check orders for multiple users using the procedure

**Key Code**:

```python
cursor.execute("CALL GetOrderSummary(%s)", (test_user_id,))
results = cursor.fetchall()
```

**Usage**: `python backend/database/check_users_orders.py`

---

### 4. `backend/database/apply_order_summary_procedure.py`

**Purpose**: Install/update the `GetOrderSummary` stored procedure

**Key Code**:

```python
cursor.execute("DROP PROCEDURE IF EXISTS GetOrderSummary;")
cursor.execute(procedure_create)
```

**Usage**: `python backend/database/apply_order_summary_procedure.py`

---

### 5. `backend/database/test_new_procedures.py`

**Purpose**: Test all analytics stored procedures

**Key Code**:

```python
cursor.execute("CALL GetUserCart(1)")
cursor.execute("CALL GetLowStockVariants(20)")
```

**Usage**: `python backend/database/test_new_procedures.py`

---

## Quick Reference

### How to Call a Stored Procedure in Python

```python
import mysql.connector
from app.database import get_db

# Method 1: Using FastAPI Depends
def my_endpoint(db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetUserCart(%s)", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    return results

# Method 2: Direct connection
def standalone_script():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("CALL GetOrderSummary(%s)", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
```

### Important Notes

⚠️ **Always use parameterized queries** to prevent SQL injection:

```python
# Good ✅
cursor.execute("CALL GetUserCart(%s)", (user_id,))

# Bad ❌
cursor.execute(f"CALL GetUserCart({user_id})")
```

⚠️ **Close cursors after fetching results**:

```python
cursor = db.cursor(dictionary=True)
cursor.execute("CALL GetUserCart(%s)", (user_id,))
results = cursor.fetchall()
cursor.close()  # Always close!
```

⚠️ **Commit changes for UPDATE/INSERT procedures**:

```python
cursor.execute("CALL UpdateOrderStatus(%s, %s)", (order_id, status))
db.commit()  # Required for data modifications
```

---

## SQL Commands Reference

### List All Procedures

```sql
SHOW PROCEDURE STATUS WHERE Db = 'brightbuy';
```

### View Procedure Definition

```sql
SHOW CREATE PROCEDURE GetUserCart;
```

### Drop a Procedure

```sql
DROP PROCEDURE IF EXISTS GetUserCart;
```

### Grant Execute Permission

```sql
GRANT EXECUTE ON PROCEDURE brightbuy.GetUserCart TO 'username'@'localhost';
```

---

## Benefits of Using Stored Procedures

✅ **Performance**: Queries are pre-compiled and optimized  
✅ **Security**: Prevents SQL injection through parameterization  
✅ **Maintainability**: Centralized business logic in database  
✅ **Reusability**: Can be called from multiple applications  
✅ **Consistency**: Same logic across all application layers  
✅ **Network Efficiency**: Reduces data transfer between app and DB

---

## Maintenance Checklist

- [ ] Backup procedures before modifications: `mysqldump --routines`
- [ ] Test procedures with sample data before production deployment
- [ ] Document parameter changes in this file
- [ ] Update FastAPI routes when procedure signatures change
- [ ] Monitor procedure execution time for performance issues
- [ ] Review and optimize slow procedures (use `EXPLAIN`)
- [ ] Add indexes on frequently joined columns
- [ ] Version control procedure definitions in SQL files

---

## Support and Documentation

**Related Files**:

- Procedure definitions: `backend/app/database/exports/procedures_20251016_165400.sql`
- Analytics routes: `backend/app/routes/analytics.py`
- User routes: `backend/app/routes/user.py`
- Integration guide: `backend/database/STORED_PROCEDURES_GUIDE.md`
- Integration examples: `backend/database/INTEGRATION_EXAMPLES.md`
- New procedures README: `backend/database/README_NEW_PROCEDURES.md`

**Database Connection**:

- Host: `localhost:3306`
- Database: `brightbuy`
- Connection file: `backend/app/database.py`

**API Documentation**: When backend is running, visit:

- Swagger UI: `http://127.0.0.1:8020/docs`
- ReDoc: `http://127.0.0.1:8020/redoc`

---

## 🎯 Final Summary: What's Actually Running in Your Application

### ✅ **ACTIVE PROCEDURES** (7 of 9):

These stored procedures are **currently being used** in your live BrightBuy application:

| Procedure                 | Endpoint                                           | Frontend Usage                                          |
| ------------------------- | -------------------------------------------------- | ------------------------------------------------------- |
| `GetUserCart`             | `GET /analytics/cart/{user_id}`                    | Available via API                                       |
| `GetProductsByCategory`   | `GET /analytics/products/category`                 | Available via API                                       |
| `GetLowStockVariants`     | `GET /analytics/inventory/low-stock`               | Admin inventory management                              |
| `GetSalesReport`          | `GET /analytics/sales/report`                      | Admin sales analytics                                   |
| **`UpdateOrderStatus`**   | `PUT /analytics/orders/{order_id}/status`          | **✨ Used by Admin Dashboard** to mark orders delivered |
| `GetTopSellingProducts`   | `GET /analytics/products/top-selling`              | Admin analytics                                         |
| `GetCustomerOrderHistory` | `GET /analytics/customers/{user_id}/order-history` | Customer order tracking                                 |

### ⚠️ **NOT ACTIVE** (2 of 9):

These are defined in the database but not called in production:

- `AddUserWithAddress` - Code commented out in user.py
- `GetOrderSummary` - Only used in test scripts

### 💡 **How to Verify**:

```bash
# Check if your backend is running
curl http://127.0.0.1:8020/ping-db

# Test an analytics endpoint
curl http://127.0.0.1:8020/analytics/inventory/low-stock?threshold=10

# Test the one used by frontend
curl -X PUT http://127.0.0.1:8020/analytics/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Delivered"}'
```

### 📍 **Where to Find Them**:

- **Backend Code**: `backend/app/routes/analytics.py` (lines 131, 195, 248, 321, 415, 491, 546)
- **Frontend Code**: `frontend/src/pages/Admin.jsx` (line 217 - calls UpdateOrderStatus)
- **Main App**: `backend/app/main.py` (line 53 - analytics router registered)

**Confirmation**: Yes, these procedures are **actively running** and powering your analytics features! 🚀

---

**Document Version**: 1.0  
**Last Updated**: October 20, 2025  
**Maintained By**: BrightBuy Development Team
