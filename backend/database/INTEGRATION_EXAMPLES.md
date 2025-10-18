# FastAPI Integration Examples for MySQL Functions

This guide shows you exactly how to integrate the new MySQL functions into your existing FastAPI routes.

---

## 📁 File: `app/routes/product.py`

### Add Enhanced Product Details Endpoint

```python
@router.get("/{product_id}/enhanced")
def get_enhanced_product_details(product_id: int, db=Depends(get_db)):
    """
    Get product details with calculated fields using MySQL functions
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                p.product_id,
                p.product_name,
                p.description,
                c.category_name,
                GetCategoryPath(p.category_id) as full_category_path,
                GetProductStockStatus(p.product_id) as stock_status,
                GetProductPriceRange(p.product_id) as price_range,
                GetProductAverageRating(p.product_id) as rating,
                COUNT(DISTINCT v.variant_id) as variant_count,
                SUM(v.quantity) as total_stock
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN variant v ON p.product_id = v.product_id
            WHERE p.product_id = %s
            GROUP BY p.product_id, p.product_name, p.description, 
                     c.category_name, p.category_id
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

### Add Product Variants with Availability Check

```python
@router.get("/{product_id}/variants/availability")
def check_variants_availability(
    product_id: int, 
    quantity: int = 1,
    db=Depends(get_db)
):
    """
    Get all variants for a product with availability check
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                v.variant_id,
                v.variant_name,
                v.price,
                v.quantity as stock,
                v.SKU,
                IsVariantAvailable(v.variant_id, %s) as is_available,
                CASE 
                    WHEN IsVariantAvailable(v.variant_id, %s) = 1 
                    THEN 'Available'
                    ELSE 'Out of Stock'
                END as availability_message
            FROM variant v
            WHERE v.product_id = %s
            ORDER BY v.price ASC
        """, (quantity, quantity, product_id))
        
        variants = cursor.fetchall()
        cursor.close()
        
        # Convert boolean to Python bool
        for variant in variants:
            variant['is_available'] = bool(variant['is_available'])
        
        return {
            "product_id": product_id,
            "requested_quantity": quantity,
            "variants": variants
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

### Add Sale/Discount Endpoint

```python
@router.get("/{product_id}/sale")
def get_product_with_discount(
    product_id: int,
    discount_percent: float = 0,
    db=Depends(get_db)
):
    """
    Get product variants with discounted prices
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                v.variant_id,
                v.variant_name,
                v.price as original_price,
                GetDiscountedPrice(v.price, %s) as sale_price,
                (v.price - GetDiscountedPrice(v.price, %s)) as savings,
                ROUND(((v.price - GetDiscountedPrice(v.price, %s)) / v.price * 100), 2) as savings_percent,
                v.quantity as stock,
                IsVariantAvailable(v.variant_id, 1) as in_stock
            FROM variant v
            WHERE v.product_id = %s
            ORDER BY v.price ASC
        """, (discount_percent, discount_percent, discount_percent, product_id))
        
        variants = cursor.fetchall()
        cursor.close()
        
        return {
            "product_id": product_id,
            "discount_percent": discount_percent,
            "variants": variants
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📁 File: `app/routes/cart.py`

### Add Cart Summary with Calculated Total

```python
@router.get("/{cart_id}/summary")
def get_cart_summary(cart_id: int, db=Depends(get_db)):
    """
    Get cart summary with calculated total using MySQL function
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                c.cart_id,
                c.user_id,
                c.total_amount as stored_total,
                CalculateCartTotal(c.cart_id) as calculated_total,
                c.created_date,
                COUNT(ci.cart_item_id) as item_count
            FROM cart c
            LEFT JOIN cart_item ci ON c.cart_id = ci.cart_id
            WHERE c.cart_id = %s
            GROUP BY c.cart_id, c.user_id, c.total_amount, c.created_date
        """, (cart_id,))
        
        summary = cursor.fetchone()
        cursor.close()
        
        if not summary:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        return summary
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

### Add Cart Items with Calculated Totals

```python
@router.get("/{cart_id}/items/detailed")
def get_cart_items_detailed(cart_id: int, db=Depends(get_db)):
    """
    Get cart items with calculated totals and availability
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                ci.cart_item_id,
                ci.variant_id,
                ci.quantity,
                v.variant_name,
                v.price,
                v.quantity as stock_available,
                (ci.quantity * v.price) as item_total,
                IsVariantAvailable(ci.variant_id, ci.quantity) as is_available,
                p.product_name,
                GetProductStockStatus(p.product_id) as product_stock_status
            FROM cart_item ci
            JOIN variant v ON ci.variant_id = v.variant_id
            JOIN product p ON v.product_id = p.product_id
            WHERE ci.cart_id = %s
            ORDER BY ci.cart_item_id DESC
        """, (cart_id,))
        
        items = cursor.fetchall()
        cursor.close()
        
        # Convert boolean
        for item in items:
            item['is_available'] = bool(item['is_available'])
        
        return {
            "cart_id": cart_id,
            "items": items,
            "total_items": len(items)
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📁 File: `app/routes/order.py`

### Add Enhanced Order Details

```python
@router.get("/{order_id}/enhanced")
def get_enhanced_order_details(order_id: int, db=Depends(get_db)):
    """
    Get order details with calculated fields and status
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                o.order_id,
                o.order_date,
                o.total_amount,
                o.user_id,
                u.user_name,
                u.email,
                GetOrderStatus(o.order_id) as comprehensive_status,
                d.delivery_status,
                d.delivery_date,
                pm.payment_method,
                a.city,
                a.state,
                CalculateDeliveryDays(a.city_id) as estimated_delivery_days,
                DATEDIFF(COALESCE(d.delivery_date, NOW()), o.order_date) as days_since_order
            FROM orders o
            JOIN user u ON o.user_id = u.user_id
            LEFT JOIN delivery d ON o.order_id = d.order_id
            LEFT JOIN payment pm ON o.order_id = pm.order_id
            LEFT JOIN address a ON u.address_id = a.address_id
            WHERE o.order_id = %s
        """, (order_id,))
        
        order = cursor.fetchone()
        cursor.close()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return order
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

### Add Order Items with Calculated Totals

```python
@router.get("/{order_id}/items/calculated")
def get_order_items_with_totals(order_id: int, db=Depends(get_db)):
    """
    Get order items with calculated totals
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                oi.order_item_id,
                oi.variant_id,
                oi.quantity,
                oi.price,
                CalculateOrderItemTotal(oi.order_item_id) as calculated_total,
                v.variant_name,
                p.product_name,
                p.product_id
            FROM order_item oi
            JOIN variant v ON oi.variant_id = v.variant_id
            JOIN product p ON v.product_id = p.product_id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        items = cursor.fetchall()
        cursor.close()
        
        # Calculate order total
        order_total = sum(float(item['calculated_total']) for item in items)
        
        return {
            "order_id": order_id,
            "items": items,
            "item_count": len(items),
            "order_total": order_total
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📁 File: `app/routes/user.py`

### Add Customer Analytics Endpoint

```python
@router.get("/{user_id}/analytics")
def get_customer_analytics(user_id: int, db=Depends(get_db)):
    """
    Get customer analytics using MySQL functions
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                u.user_id,
                u.user_name,
                u.email,
                ValidateEmail(u.email) as email_is_valid,
                GetCustomerLifetimeValue(u.user_id) as lifetime_value,
                COUNT(DISTINCT o.order_id) as total_orders,
                COALESCE(AVG(o.total_amount), 0) as average_order_value,
                MAX(o.order_date) as last_order_date,
                DATEDIFF(NOW(), MAX(o.order_date)) as days_since_last_order
            FROM user u
            LEFT JOIN orders o ON u.user_id = o.user_id
            WHERE u.user_id = %s
            GROUP BY u.user_id, u.user_name, u.email
        """, (user_id,))
        
        analytics = cursor.fetchone()
        cursor.close()
        
        if not analytics:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert boolean
        analytics['email_is_valid'] = bool(analytics['email_is_valid'])
        
        return analytics
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

### Add Top Customers Endpoint

```python
@router.get("/customers/top")
def get_top_customers(limit: int = 10, db=Depends(get_db)):
    """
    Get top customers by lifetime value
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                u.user_id,
                u.user_name,
                u.email,
                GetCustomerLifetimeValue(u.user_id) as lifetime_value,
                COUNT(DISTINCT o.order_id) as total_orders
            FROM user u
            LEFT JOIN orders o ON u.user_id = o.user_id
            WHERE u.user_type = 'customer'
            GROUP BY u.user_id, u.user_name, u.email
            HAVING lifetime_value > 0
            ORDER BY lifetime_value DESC
            LIMIT %s
        """, (limit,))
        
        customers = cursor.fetchall()
        cursor.close()
        
        return {
            "top_customers": customers,
            "count": len(customers)
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📁 File: `app/routes/location.py`

### Add Delivery Estimate Endpoint

```python
@router.get("/delivery-estimate/{city_id}")
def get_delivery_estimate(city_id: int, db=Depends(get_db)):
    """
    Get delivery estimate for a city using MySQL function
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                l.city_id,
                l.city_name,
                l.delivery_time as stored_delivery_time,
                CalculateDeliveryDays(l.city_id) as calculated_delivery_days,
                DATE_ADD(CURDATE(), INTERVAL CalculateDeliveryDays(l.city_id) DAY) as estimated_delivery_date
            FROM location l
            WHERE l.city_id = %s
        """, (city_id,))
        
        estimate = cursor.fetchone()
        cursor.close()
        
        if not estimate:
            raise HTTPException(status_code=404, detail="City not found")
        
        return estimate
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📁 File: `app/routes/admin.py`

### Add Inventory Alerts with Functions

```python
@router.get("/inventory/alerts")
def get_inventory_alerts(db=Depends(get_db)):
    """
    Get inventory alerts using both procedures and functions
    """
    cursor = db.cursor(dictionary=True)
    try:
        # Use stored procedure for low stock variants
        cursor.execute("CALL GetLowStockVariants(20)")
        low_stock = cursor.fetchall()
        cursor.nextset()  # Clear result set
        
        # Enhance with functions
        cursor.execute("""
            SELECT 
                p.product_id,
                p.product_name,
                GetProductStockStatus(p.product_id) as stock_status,
                SUM(v.quantity) as total_stock,
                COUNT(v.variant_id) as variant_count
            FROM product p
            JOIN variant v ON p.product_id = v.product_id
            GROUP BY p.product_id, p.product_name
            HAVING stock_status IN ('Low Stock', 'Out of Stock')
            ORDER BY total_stock ASC
        """)
        
        products_at_risk = cursor.fetchall()
        cursor.close()
        
        return {
            "low_stock_variants": low_stock,
            "products_at_risk": products_at_risk,
            "total_alerts": len(low_stock) + len(products_at_risk)
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🔧 Validation Endpoint

### Add Email Validation

```python
# In app/routes/auth.py or user.py

from pydantic import BaseModel

class EmailValidation(BaseModel):
    email: str

@router.post("/validate-email")
def validate_email_format(data: EmailValidation, db=Depends(get_db)):
    """
    Validate email format using MySQL function
    """
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT ValidateEmail(%s) as is_valid
        """, (data.email,))
        
        result = cursor.fetchone()
        cursor.close()
        
        return {
            "email": data.email,
            "is_valid": bool(result['is_valid']),
            "message": "Valid email format" if result['is_valid'] else "Invalid email format"
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🎯 Complete Example: Enhanced Product Listing

```python
# In app/routes/product.py

@router.get("/")
def get_all_products_enhanced(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
    db=Depends(get_db)
):
    """
    Get all products with enhanced information using MySQL functions
    """
    cursor = db.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.description,
                c.category_name,
                GetCategoryPath(p.category_id) as full_category_path,
                GetProductStockStatus(p.product_id) as stock_status,
                GetProductPriceRange(p.product_id) as price_range,
                GetProductAverageRating(p.product_id) as rating,
                COUNT(DISTINCT v.variant_id) as variant_count,
                MIN(v.price) as min_price,
                MAX(v.price) as max_price,
                SUM(v.quantity) as total_stock
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN variant v ON p.product_id = v.product_id
            WHERE 1=1
        """
        
        params = []
        
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        query += " GROUP BY p.product_id, p.product_name, p.description, c.category_name, p.category_id"
        
        if in_stock_only:
            query += " HAVING stock_status != 'Out of Stock'"
        
        if min_price:
            query += " AND min_price >= %s" if "HAVING" in query else " HAVING min_price >= %s"
            params.append(min_price)
        
        if max_price:
            query += " AND max_price <= %s" if "HAVING" in query else " HAVING max_price <= %s"
            params.append(max_price)
        
        query += " ORDER BY p.product_name"
        
        cursor.execute(query, params)
        products = cursor.fetchall()
        cursor.close()
        
        return {
            "products": products,
            "count": len(products),
            "filters": {
                "category_id": category_id,
                "min_price": min_price,
                "max_price": max_price,
                "in_stock_only": in_stock_only
            }
        }
        
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📝 Notes

1. **Always close cursors** after use
2. **Convert MySQL BOOLEAN** (0/1) to Python bool using `bool()`
3. **Handle NULL values** appropriately
4. **Use parameterized queries** to prevent SQL injection
5. **Add error handling** for all database operations
6. **Test endpoints** thoroughly before deployment

---

**Ready to use!** Copy these examples into your routes and customize as needed.
