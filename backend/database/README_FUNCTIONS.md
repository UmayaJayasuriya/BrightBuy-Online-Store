# MySQL Functions - Quick Start Guide

## 🎉 What's Been Created

I've created **12 powerful MySQL functions** for BrightBuy to enhance calculations, validations, and data transformations.

---

## 📦 Files Created

1. **`mysql_functions.sql`** - SQL file with all 12 functions
2. **`apply_functions.py`** - Python script to install functions
3. **`test_functions.py`** - Test script to verify functions work
4. **`MYSQL_FUNCTIONS_GUIDE.md`** - Complete documentation with examples

---

## 🚀 Quick Installation (3 Steps)

### Step 1: Install the Functions
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

### Step 2: Test the Functions
```bash
python database/test_functions.py
```

### Step 3: Start Using Them!
```sql
-- Example: Calculate cart total
SELECT CalculateCartTotal(1);

-- Example: Check stock status
SELECT GetProductStockStatus(5);

-- Example: Validate email
SELECT ValidateEmail('test@example.com');
```

---

## 📚 Function Categories

### 💰 Financial Calculations
- **CalculateCartTotal** - Calculate cart total amount
- **CalculateOrderItemTotal** - Calculate order item total
- **GetCustomerLifetimeValue** - Customer lifetime value
- **GetDiscountedPrice** - Calculate discounted prices

### 📦 Inventory & Stock
- **GetProductStockStatus** - Get stock status (In Stock/Low/Out)
- **IsVariantAvailable** - Check if variant has enough stock

### 📊 Product Information
- **GetProductPriceRange** - Get formatted price range
- **GetProductAverageRating** - Get product rating (placeholder)
- **GetCategoryPath** - Get full category hierarchy

### 🚚 Order & Delivery
- **GetOrderStatus** - Get comprehensive order status
- **CalculateDeliveryDays** - Calculate delivery estimate

### ✅ Validation
- **ValidateEmail** - Email format validation

---

## 🔥 Quick Examples

### Example 1: Enhanced Product Listing
```sql
SELECT 
    p.product_id,
    p.product_name,
    GetProductStockStatus(p.product_id) as stock_status,
    GetProductPriceRange(p.product_id) as price_range,
    GetCategoryPath(p.category_id) as category_path
FROM product p
ORDER BY p.product_name;
```

### Example 2: Cart with Calculated Total
```sql
SELECT 
    c.cart_id,
    c.user_id,
    CalculateCartTotal(c.cart_id) as calculated_total,
    c.total_amount as stored_total
FROM cart c
WHERE c.user_id = 1;
```

### Example 3: Top Customers by Lifetime Value
```sql
SELECT 
    u.user_id,
    u.user_name,
    u.email,
    GetCustomerLifetimeValue(u.user_id) as lifetime_value
FROM user u
WHERE u.user_type = 'customer'
ORDER BY lifetime_value DESC
LIMIT 10;
```

### Example 4: Check Variant Availability
```sql
SELECT 
    v.variant_id,
    v.variant_name,
    v.quantity as stock,
    IsVariantAvailable(v.variant_id, 5) as can_order_5_units
FROM variant v
WHERE v.product_id = 1;
```

### Example 5: Products with Discount
```sql
SELECT 
    v.variant_id,
    v.variant_name,
    v.price as original_price,
    GetDiscountedPrice(v.price, 20) as sale_price,
    (v.price - GetDiscountedPrice(v.price, 20)) as savings
FROM variant v
WHERE v.product_id = 1;
```

---

## 🔧 FastAPI Integration Examples

### Use in Product Routes
```python
@router.get("/products/{product_id}")
def get_product(product_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.product_id,
            p.product_name,
            GetProductStockStatus(p.product_id) as stock_status,
            GetProductPriceRange(p.product_id) as price_range
        FROM product p
        WHERE p.product_id = %s
    """, (product_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

### Use in Cart Routes
```python
@router.get("/cart/{cart_id}/summary")
def get_cart_summary(cart_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            cart_id,
            user_id,
            CalculateCartTotal(cart_id) as total
        FROM cart
        WHERE cart_id = %s
    """, (cart_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

### Use in Order Routes
```python
@router.get("/orders/{order_id}/status")
def get_order_status(order_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            order_id,
            order_date,
            total_amount,
            GetOrderStatus(order_id) as status
        FROM orders
        WHERE order_id = %s
    """, (order_id,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

---

## 📊 All Functions Summary

| # | Function Name | Purpose | Returns |
|---|---------------|---------|---------|
| 1 | `CalculateCartTotal` | Calculate cart total | DECIMAL |
| 2 | `GetProductStockStatus` | Get stock status | VARCHAR |
| 3 | `CalculateOrderItemTotal` | Calculate item total | DECIMAL |
| 4 | `GetCustomerLifetimeValue` | Customer lifetime value | DECIMAL |
| 5 | `GetProductAverageRating` | Product rating | DECIMAL |
| 6 | `IsVariantAvailable` | Check availability | BOOLEAN |
| 7 | `GetProductPriceRange` | Formatted price range | VARCHAR |
| 8 | `CalculateDeliveryDays` | Delivery estimate | INT |
| 9 | `GetOrderStatus` | Order status message | VARCHAR |
| 10 | `ValidateEmail` | Email validation | BOOLEAN |
| 11 | `GetDiscountedPrice` | Calculate discount | DECIMAL |
| 12 | `GetCategoryPath` | Category hierarchy | VARCHAR |

---

## 💡 When to Use Functions vs Procedures

### Use Functions When:
- ✅ You need a **single calculated value**
- ✅ You want to use it in **SELECT, WHERE, or JOIN** clauses
- ✅ You need **reusable calculations** across queries
- ✅ The operation is **read-only**

### Use Procedures When:
- ✅ You need to return **multiple rows** or result sets
- ✅ You need to **modify data** (INSERT, UPDATE, DELETE)
- ✅ You need **complex business logic** with transactions
- ✅ You need **multiple output parameters**

---

## 🎯 Benefits

✅ **Cleaner Code**: Replace complex calculations with simple function calls  
✅ **Consistency**: Same logic everywhere  
✅ **Performance**: Database-level execution  
✅ **Maintainability**: Update once, apply everywhere  
✅ **Reusability**: Use in any SQL query or stored procedure  

---

## 🔍 Verify Installation

```sql
-- List all functions
SHOW FUNCTION STATUS WHERE Db = 'brightbuy';

-- Test a function
SELECT CalculateCartTotal(1) as total;

-- View function definition
SHOW CREATE FUNCTION CalculateCartTotal;
```

---

## 📖 Next Steps

1. ✅ Install functions using `apply_functions.py`
2. ✅ Test functions using `test_functions.py`
3. 🔲 Integrate functions into your FastAPI routes
4. 🔲 Update frontend to display calculated values
5. 🔲 Add more custom functions as needed

---

## 📚 Full Documentation

For complete documentation with detailed examples, see:
- **[MYSQL_FUNCTIONS_GUIDE.md](MYSQL_FUNCTIONS_GUIDE.md)** - Complete guide with all examples

---

**Created**: October 18, 2025  
**Version**: 1.0  
**Functions**: 12  
**Status**: Ready to Use ✅
