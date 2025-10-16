# BrightBuy Stored Procedures Guide

## Overview

This guide covers all stored procedures available in the BrightBuy database, including usage examples and integration with FastAPI.

---

## 📋 Table of Contents

1. [GetUserCart](#1-getusercart)
2. [GetProductsByCategory](#2-getproductsbycategory)
3. [GetLowStockVariants](#3-getlowstockvariants)
4. [GetSalesReport](#4-getsalesreport)
5. [UpdateOrderStatus](#5-updateorderstatus)
6. [GetTopSellingProducts](#6-gettopsellingproducts-bonus)
7. [GetCustomerOrderHistory](#7-getcustomerorderhistory-bonus)
8. [Installation](#installation)
9. [FastAPI Integration](#fastapi-integration)

---

## 1. GetUserCart

**Purpose**: Fetch complete cart details for a user with product information and stock status.

### Parameters
- `p_user_id` (INT) - User ID

### Returns
- `cart_id` - Cart identifier
- `user_id` - User identifier
- `cart_total` - Total cart amount
- `cart_item_id` - Cart item identifier
- `variant_id` - Product variant ID
- `quantity` - Quantity in cart
- `variant_name` - Variant name
- `price` - Unit price
- `SKU` - Stock keeping unit
- `stock_available` - Available stock
- `product_id` - Product identifier
- `product_name` - Product name
- `description` - Product description
- `category_name` - Category name
- `item_total` - Line item total (quantity × price)
- `stock_status` - In Stock / Limited Stock / Out of Stock

### SQL Usage
```sql
CALL GetUserCart(1);
```

### FastAPI Example
```python
@router.get("/cart/{user_id}/details")
def get_cart_details(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetUserCart(%s)", (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        return {"cart_items": cart_items}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 2. GetProductsByCategory

**Purpose**: Get all products in a category with pricing information and variant counts.

### Parameters
- `p_category_id` (INT) - Category ID (NULL for all products)

### Returns
- `product_id` - Product identifier
- `product_name` - Product name
- `description` - Product description
- `category_id` - Category identifier
- `category_name` - Category name
- `variant_count` - Number of variants
- `min_price` - Lowest variant price
- `max_price` - Highest variant price
- `total_stock` - Total stock across all variants
- `availability_status` - Available / Out of Stock

### SQL Usage
```sql
-- Get products in category 1
CALL GetProductsByCategory(1);

-- Get all products
CALL GetProductsByCategory(NULL);
```

### FastAPI Example
```python
@router.get("/products/category/{category_id}")
def get_products_by_category(
    category_id: Optional[int] = None,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetProductsByCategory(%s)", (category_id,))
        products = cursor.fetchall()
        cursor.close()
        return {"products": products}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 3. GetLowStockVariants

**Purpose**: Identify variants with stock below a threshold for inventory management.

### Parameters
- `p_threshold` (INT) - Stock level threshold (default: 10)

### Returns
- `variant_id` - Variant identifier
- `variant_name` - Variant name
- `current_stock` - Current stock level
- `price` - Variant price
- `SKU` - Stock keeping unit
- `product_id` - Product identifier
- `product_name` - Product name
- `category_id` - Category identifier
- `category_name` - Category name
- `threshold` - Threshold used
- `stock_alert_level` - OUT OF STOCK / CRITICAL / LOW
- `sold_last_30_days` - Sales in last 30 days

### SQL Usage
```sql
-- Get variants with stock < 10
CALL GetLowStockVariants(10);

-- Get variants with stock < 50
CALL GetLowStockVariants(50);
```

### FastAPI Example
```python
@router.get("/inventory/low-stock")
def get_low_stock(
    threshold: int = 10,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetLowStockVariants(%s)", (threshold,))
        low_stock = cursor.fetchall()
        cursor.close()
        return {
            "threshold": threshold,
            "low_stock_items": low_stock,
            "count": len(low_stock)
        }
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 4. GetSalesReport

**Purpose**: Generate comprehensive sales report for a date range.

### Parameters
- `p_start_date` (DATE) - Start date (default: 30 days ago)
- `p_end_date` (DATE) - End date (default: today)

### Returns
- `sale_date` - Date of sales
- `total_orders` - Number of orders
- `unique_customers` - Number of unique customers
- `total_revenue` - Total revenue
- `average_order_value` - Average order value
- `total_items_sold` - Total items sold
- `top_product` - Most popular product of the day
- `card_revenue` - Revenue from card payments
- `cash_revenue` - Revenue from cash payments

### SQL Usage
```sql
-- Last 30 days (default)
CALL GetSalesReport(NULL, NULL);

-- Specific date range
CALL GetSalesReport('2025-01-01', '2025-10-16');

-- Last 7 days
CALL GetSalesReport(DATE_SUB(CURDATE(), INTERVAL 7 DAY), CURDATE());
```

### FastAPI Example
```python
from datetime import date, timedelta

@router.get("/admin/sales-report")
def get_sales_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        # Set defaults
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        cursor.execute(
            "CALL GetSalesReport(%s, %s)",
            (start_date, end_date)
        )
        report = cursor.fetchall()
        cursor.close()
        
        # Calculate totals
        total_revenue = sum(float(r['total_revenue'] or 0) for r in report)
        total_orders = sum(int(r['total_orders'] or 0) for r in report)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "daily_sales": report,
            "summary": {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "average_daily_revenue": total_revenue / len(report) if report else 0
            }
        }
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 5. UpdateOrderStatus

**Purpose**: Update delivery status for an order.

### Parameters
- `p_order_id` (INT) - Order ID
- `p_new_status` (VARCHAR) - New delivery status

### Valid Status Values
- `Pending`
- `Processing`
- `Shipped`
- `Out for Delivery`
- `Delivered`
- `Cancelled`

### Returns
- `message` - Success message
- `order_id` - Order identifier
- `new_status` - Updated status
- `updated_at` / `created_at` - Timestamp

### SQL Usage
```sql
-- Update order status
CALL UpdateOrderStatus(1, 'Shipped');
CALL UpdateOrderStatus(2, 'Delivered');
```

### FastAPI Example
```python
from pydantic import BaseModel

class OrderStatusUpdate(BaseModel):
    status: str

@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "CALL UpdateOrderStatus(%s, %s)",
            (order_id, status_update.status)
        )
        result = cursor.fetchone()
        db.commit()
        cursor.close()
        return result
    except Exception as e:
        db.rollback()
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 6. GetTopSellingProducts (BONUS)

**Purpose**: Analyze best-selling products by quantity or revenue.

### Parameters
- `p_limit` (INT) - Number of products to return (default: 10)
- `p_days` (INT) - Number of days to look back (default: 30)

### Returns
- `product_id` - Product identifier
- `product_name` - Product name
- `category_name` - Category name
- `times_ordered` - Number of orders containing this product
- `total_quantity_sold` - Total units sold
- `total_revenue` - Total revenue generated
- `average_price` - Average selling price
- `lowest_variant_stock` - Lowest stock among variants

### SQL Usage
```sql
-- Top 10 products (last 30 days)
CALL GetTopSellingProducts(10, 30);

-- Top 5 products (last 7 days)
CALL GetTopSellingProducts(5, 7);
```

### FastAPI Example
```python
@router.get("/admin/top-selling")
def get_top_selling_products(
    limit: int = 10,
    days: int = 30,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "CALL GetTopSellingProducts(%s, %s)",
            (limit, days)
        )
        products = cursor.fetchall()
        cursor.close()
        return {
            "period_days": days,
            "top_products": products
        }
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 7. GetCustomerOrderHistory (BONUS)

**Purpose**: Get complete order history for a customer with full details.

### Parameters
- `p_user_id` (INT) - User ID

### Returns
- `order_id` - Order identifier
- `order_date` - Order date
- `total_amount` - Order total
- `delivery_status` - Current delivery status
- `delivery_date` - Delivery date (if delivered)
- `payment_method` - Payment method used
- `total_items` - Number of different items
- `total_quantity` - Total quantity of items
- `order_items` - Comma-separated list of items
- `days_since_order` - Days since order was placed

### SQL Usage
```sql
CALL GetCustomerOrderHistory(1);
```

### FastAPI Example
```python
@router.get("/users/{user_id}/order-history")
def get_customer_order_history(
    user_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetCustomerOrderHistory(%s)", (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        return {
            "user_id": user_id,
            "order_count": len(orders),
            "orders": orders
        }
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Installation

### Step 1: Install Procedures
```bash
cd backend
python database/apply_new_procedures.py
```

### Step 2: Verify Installation
```bash
python database/test_new_procedures.py
```

### Step 3: Check Database
```sql
-- List all procedures
SHOW PROCEDURE STATUS WHERE Db = 'brightbuy';

-- View specific procedure
SHOW CREATE PROCEDURE GetUserCart;
```

---

## FastAPI Integration

### Complete Route Example

Create `backend/app/routes/analytics.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import date, timedelta
from app.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/cart/{user_id}")
def get_user_cart(user_id: int, db=Depends(get_db)):
    """Get user's cart with full details"""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetUserCart(%s)", (user_id,))
        cart = cursor.fetchall()
        cursor.close()
        return {"cart": cart}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory/low-stock")
def get_low_stock(threshold: int = 10, db=Depends(get_db)):
    """Get low stock variants"""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetLowStockVariants(%s)", (threshold,))
        items = cursor.fetchall()
        cursor.close()
        return {"low_stock": items, "count": len(items)}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales/report")
def get_sales_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db=Depends(get_db)
):
    """Generate sales report"""
    cursor = db.cursor(dictionary=True)
    try:
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
            
        cursor.execute("CALL GetSalesReport(%s, %s)", (start_date, end_date))
        report = cursor.fetchall()
        cursor.close()
        return {"report": report}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

### Register Routes in `main.py`

```python
from app.routes import analytics

app.include_router(analytics.router)
```

---

## Benefits

✅ **Performance**: Optimized SQL queries executed at database level  
✅ **Maintainability**: Business logic centralized in database  
✅ **Reusability**: Can be called from any application layer  
✅ **Security**: Parameterized queries prevent SQL injection  
✅ **Consistency**: Same logic across all applications  

---

## Troubleshooting

### Procedure Not Found
```sql
-- Check if procedure exists
SELECT ROUTINE_NAME FROM information_schema.ROUTINES 
WHERE ROUTINE_SCHEMA = 'brightbuy' AND ROUTINE_NAME = 'GetUserCart';
```

### Permission Denied
```sql
-- Grant execute permission
GRANT EXECUTE ON PROCEDURE brightbuy.GetUserCart TO 'your_user'@'localhost';
```

### Clear Result Sets in Python
```python
# Always clear result sets when using stored procedures
cursor.execute("CALL GetUserCart(%s)", (user_id,))
results = cursor.fetchall()
cursor.nextset()  # Important: Clear remaining result sets
```

---

## Next Steps

1. ✅ Install all procedures
2. ✅ Test procedures
3. 🔲 Create FastAPI routes
4. 🔲 Update frontend to use new endpoints
5. 🔲 Build admin dashboard
6. 🔲 Add authentication middleware
7. 🔲 Implement caching for reports

---

**Created**: October 16, 2025  
**Version**: 1.0  
**Author**: BrightBuy Development Team
