# BrightBuy MySQL Functions Guide

## Overview

This guide covers all custom MySQL functions available in the BrightBuy database. Functions are reusable SQL routines that return a single value and can be used in SELECT statements, WHERE clauses, and other SQL expressions.

---

## 📋 Table of Contents

1. [CalculateCartTotal](#1-calculatecarttotal)
2. [GetProductStockStatus](#2-getproductstockstatus)
3. [CalculateOrderItemTotal](#3-calculateorderitemtotal)
4. [GetCustomerLifetimeValue](#4-getcustomerlifetimevalue)
5. [GetProductAverageRating](#5-getproductaveragerating)
6. [IsVariantAvailable](#6-isvariantavailable)
7. [GetProductPriceRange](#7-getproductpricerange)
8. [CalculateDeliveryDays](#8-calculatedeliverydays)
9. [GetOrderStatus](#9-getorderstatus)
10. [ValidateEmail](#10-validateemail)
11. [GetDiscountedPrice](#11-getdiscountedprice)
12. [GetCategoryPath](#12-getcategorypath)
13. [Installation](#installation)
14. [FastAPI Integration](#fastapi-integration)

---

## 1. CalculateCartTotal

**Purpose**: Calculate the total amount for a cart based on all items and their quantities.

### Parameters
- `p_cart_id` (INT) - Cart ID

### Returns
- `DECIMAL(10,2)` - Total cart amount

### SQL Usage
```sql
-- Get cart total
SELECT CalculateCartTotal(1) as cart_total;

-- Use in query
SELECT 
    cart_id,
    user_id,
    CalculateCartTotal(cart_id) as calculated_total,
    total_amount as stored_total
FROM cart
WHERE user_id = 1;
```

### FastAPI Example
```python
@router.get("/cart/{cart_id}/total")
def get_cart_total(cart_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT CalculateCartTotal(%s) as total", (cart_id,))
    result = cursor.fetchone()
    cursor.close()
    return {"cart_id": cart_id, "total": float(result['total'])}
```

---

## 2. GetProductStockStatus

**Purpose**: Get the overall stock status for a product across all its variants.

### Parameters
- `p_product_id` (INT) - Product ID

### Returns
- `VARCHAR(20)` - 'In Stock', 'Low Stock', or 'Out of Stock'

### Logic
- **Out of Stock**: Total stock = 0
- **Low Stock**: Total stock < 20
- **In Stock**: Total stock >= 20

### SQL Usage
```sql
-- Get stock status for a product
SELECT GetProductStockStatus(1) as stock_status;

-- Use in product listing
SELECT 
    product_id,
    product_name,
    GetProductStockStatus(product_id) as stock_status
FROM product
ORDER BY product_name;
```

### FastAPI Example
```python
@router.get("/products/{product_id}/stock-status")
def get_product_stock_status(product_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            product_id,
            product_name,
            GetProductStockStatus(product_id) as stock_status
        FROM product
        WHERE product_id = %s
    """, (product_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

---

## 3. CalculateOrderItemTotal

**Purpose**: Calculate the total amount for a specific order item (quantity × price).

### Parameters
- `p_order_item_id` (INT) - Order Item ID

### Returns
- `DECIMAL(10,2)` - Item total

### SQL Usage
```sql
-- Get order item total
SELECT CalculateOrderItemTotal(1) as item_total;

-- Use in order details
SELECT 
    order_item_id,
    variant_id,
    quantity,
    price,
    CalculateOrderItemTotal(order_item_id) as total
FROM order_item
WHERE order_id = 1;
```

---

## 4. GetCustomerLifetimeValue

**Purpose**: Calculate the total amount a customer has spent across all orders.

### Parameters
- `p_user_id` (INT) - User ID

### Returns
- `DECIMAL(10,2)` - Total lifetime spending

### SQL Usage
```sql
-- Get customer lifetime value
SELECT GetCustomerLifetimeValue(10) as lifetime_value;

-- Find top customers
SELECT 
    user_id,
    user_name,
    email,
    GetCustomerLifetimeValue(user_id) as lifetime_value
FROM user
WHERE user_type = 'customer'
ORDER BY lifetime_value DESC
LIMIT 10;
```

### FastAPI Example
```python
@router.get("/customers/{user_id}/lifetime-value")
def get_customer_lifetime_value(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            u.user_id,
            u.user_name,
            u.email,
            GetCustomerLifetimeValue(u.user_id) as lifetime_value,
            COUNT(o.order_id) as total_orders
        FROM user u
        LEFT JOIN orders o ON u.user_id = o.user_id
        WHERE u.user_id = %s
        GROUP BY u.user_id, u.user_name, u.email
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

---

## 5. GetProductAverageRating

**Purpose**: Get the average rating for a product (placeholder for future ratings feature).

### Parameters
- `p_product_id` (INT) - Product ID

### Returns
- `DECIMAL(3,2)` - Average rating (currently returns 0.00)

### Note
This is a placeholder function. Update the function body when you implement a product ratings table.

### SQL Usage
```sql
-- Get product rating
SELECT GetProductAverageRating(1) as rating;
```

---

## 6. IsVariantAvailable

**Purpose**: Check if a variant has sufficient stock for a requested quantity.

### Parameters
- `p_variant_id` (INT) - Variant ID
- `p_quantity` (INT) - Requested quantity

### Returns
- `BOOLEAN` - TRUE (1) if available, FALSE (0) if not

### SQL Usage
```sql
-- Check if 5 units are available
SELECT IsVariantAvailable(1, 5) as is_available;

-- Filter available variants
SELECT 
    variant_id,
    variant_name,
    quantity,
    IsVariantAvailable(variant_id, 10) as can_order_10
FROM variant
WHERE product_id = 1;
```

### FastAPI Example
```python
@router.get("/variants/{variant_id}/check-availability")
def check_variant_availability(
    variant_id: int, 
    quantity: int = 1,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            variant_id,
            variant_name,
            quantity as stock,
            IsVariantAvailable(%s, %s) as is_available
        FROM variant
        WHERE variant_id = %s
    """, (variant_id, quantity, variant_id))
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        result['is_available'] = bool(result['is_available'])
    return result
```

---

## 7. GetProductPriceRange

**Purpose**: Get a formatted price range string for a product.

### Parameters
- `p_product_id` (INT) - Product ID

### Returns
- `VARCHAR(50)` - Formatted price range (e.g., "$10.00 - $50.00" or "$25.00")

### SQL Usage
```sql
-- Get price range
SELECT GetProductPriceRange(1) as price_range;

-- Use in product listing
SELECT 
    product_id,
    product_name,
    GetProductPriceRange(product_id) as price_range
FROM product;
```

---

## 8. CalculateDeliveryDays

**Purpose**: Calculate estimated delivery days based on the city.

### Parameters
- `p_city_id` (INT) - City ID

### Returns
- `INT` - Estimated delivery days (defaults to 7 if city not found)

### SQL Usage
```sql
-- Get delivery estimate
SELECT CalculateDeliveryDays(1) as delivery_days;

-- Use in address query
SELECT 
    address_id,
    city,
    CalculateDeliveryDays(city_id) as estimated_delivery_days
FROM address
WHERE address_id = 1;
```

### FastAPI Example
```python
@router.get("/delivery-estimate/{city_id}")
def get_delivery_estimate(city_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            city_id,
            city_name,
            CalculateDeliveryDays(city_id) as delivery_days
        FROM location
        WHERE city_id = %s
    """, (city_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

---

## 9. GetOrderStatus

**Purpose**: Get a comprehensive order status message combining delivery and payment info.

### Parameters
- `p_order_id` (INT) - Order ID

### Returns
- `VARCHAR(100)` - Status message (e.g., "Shipped (card)" or "Order Placed")

### SQL Usage
```sql
-- Get order status
SELECT GetOrderStatus(1) as status;

-- Use in order listing
SELECT 
    order_id,
    order_date,
    total_amount,
    GetOrderStatus(order_id) as status
FROM orders
WHERE user_id = 10;
```

---

## 10. ValidateEmail

**Purpose**: Validate email format using regex.

### Parameters
- `p_email` (VARCHAR) - Email address

### Returns
- `BOOLEAN` - TRUE (1) if valid, FALSE (0) if invalid

### SQL Usage
```sql
-- Validate email
SELECT ValidateEmail('test@example.com') as is_valid;

-- Find invalid emails
SELECT 
    user_id,
    email,
    ValidateEmail(email) as is_valid
FROM user
WHERE ValidateEmail(email) = FALSE;
```

### FastAPI Example
```python
@router.post("/validate-email")
def validate_email(email: str, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT ValidateEmail(%s) as is_valid", (email,))
    result = cursor.fetchone()
    cursor.close()
    return {"email": email, "is_valid": bool(result['is_valid'])}
```

---

## 11. GetDiscountedPrice

**Purpose**: Calculate discounted price based on percentage.

### Parameters
- `p_price` (DECIMAL) - Original price
- `p_discount_percent` (DECIMAL) - Discount percentage (0-100)

### Returns
- `DECIMAL(10,2)` - Discounted price

### SQL Usage
```sql
-- Calculate 20% discount on $100
SELECT GetDiscountedPrice(100.00, 20) as discounted_price;

-- Apply discount to variants
SELECT 
    variant_id,
    variant_name,
    price as original_price,
    GetDiscountedPrice(price, 15) as sale_price
FROM variant
WHERE product_id = 1;
```

### FastAPI Example
```python
@router.get("/products/{product_id}/with-discount")
def get_product_with_discount(
    product_id: int,
    discount_percent: float = 0,
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            v.variant_id,
            v.variant_name,
            v.price as original_price,
            GetDiscountedPrice(v.price, %s) as discounted_price,
            v.quantity
        FROM variant v
        WHERE v.product_id = %s
    """, (discount_percent, product_id))
    results = cursor.fetchall()
    cursor.close()
    return {"discount_percent": discount_percent, "variants": results}
```

---

## 12. GetCategoryPath

**Purpose**: Get the full hierarchical path for a category.

### Parameters
- `p_category_id` (INT) - Category ID

### Returns
- `VARCHAR(500)` - Category path (e.g., "Electronics > Laptops > Gaming Laptops")

### SQL Usage
```sql
-- Get category path
SELECT GetCategoryPath(5) as category_path;

-- Use in product listing
SELECT 
    p.product_id,
    p.product_name,
    GetCategoryPath(p.category_id) as category_path
FROM product p;
```

### FastAPI Example
```python
@router.get("/categories/{category_id}/path")
def get_category_path(category_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            category_id,
            category_name,
            GetCategoryPath(category_id) as full_path
        FROM category
        WHERE category_id = %s
    """, (category_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

---

## Installation

### Step 1: Install Functions
```bash
cd backend
python database/apply_functions.py
```

Expected output:
```
✅ 1. CalculateCartTotal
✅ 2. GetProductStockStatus
✅ 3. CalculateOrderItemTotal
✅ 4. GetCustomerLifetimeValue
✅ 5. GetProductAverageRating
✅ 6. IsVariantAvailable
✅ 7. GetProductPriceRange
✅ 8. CalculateDeliveryDays
✅ 9. GetOrderStatus
✅ 10. ValidateEmail
✅ 11. GetDiscountedPrice
✅ 12. GetCategoryPath
```

### Step 2: Test Functions
```bash
python database/test_functions.py
```

### Step 3: Verify in MySQL
```sql
-- List all functions
SHOW FUNCTION STATUS WHERE Db = 'brightbuy';

-- View specific function
SHOW CREATE FUNCTION CalculateCartTotal;
```

---

## FastAPI Integration

### Complete Example Route

Create or update `backend/app/routes/product.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}/details")
def get_product_details(product_id: int, db=Depends(get_db)):
    """Get product details with calculated fields using MySQL functions"""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                p.product_id,
                p.product_name,
                p.description,
                GetCategoryPath(p.category_id) as category_path,
                GetProductStockStatus(p.product_id) as stock_status,
                GetProductPriceRange(p.product_id) as price_range,
                GetProductAverageRating(p.product_id) as rating,
                COUNT(DISTINCT v.variant_id) as variant_count
            FROM product p
            LEFT JOIN variant v ON p.product_id = v.product_id
            WHERE p.product_id = %s
            GROUP BY p.product_id, p.product_name, p.description, p.category_id
        """, (product_id,))
        
        product = cursor.fetchone()
        cursor.close()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Benefits

✅ **Reusability**: Write once, use anywhere in queries  
✅ **Performance**: Executed at database level  
✅ **Consistency**: Same calculation logic across all queries  
✅ **Maintainability**: Update logic in one place  
✅ **Readability**: Cleaner SQL queries  

---

## Differences: Functions vs Procedures

| Feature | Functions | Procedures |
|---------|-----------|------------|
| Returns | Single value | Result sets |
| Usage | In SELECT, WHERE | CALL statement |
| Transactions | No COMMIT/ROLLBACK | Can use transactions |
| Output | RETURN value | OUT parameters |
| Side Effects | Read-only (usually) | Can modify data |

---

## Best Practices

1. **Use functions for calculations** that return a single value
2. **Use procedures for complex operations** that return multiple rows
3. **Keep functions deterministic** when possible for better optimization
4. **Document parameters** and return types clearly
5. **Test thoroughly** before using in production
6. **Handle NULL values** appropriately
7. **Consider performance** for functions used in WHERE clauses

---

## Troubleshooting

### Function Not Found
```sql
-- Check if function exists
SELECT ROUTINE_NAME 
FROM information_schema.ROUTINES 
WHERE ROUTINE_SCHEMA = 'brightbuy' 
AND ROUTINE_NAME = 'CalculateCartTotal';
```

### Permission Denied
```sql
-- Grant execute permission
GRANT EXECUTE ON FUNCTION brightbuy.CalculateCartTotal TO 'your_user'@'localhost';
```

### Function Returns NULL
- Check if input parameters are valid
- Verify data exists in referenced tables
- Add COALESCE for default values

---

**Created**: October 18, 2025  
**Version**: 1.0  
**Author**: BrightBuy Development Team
