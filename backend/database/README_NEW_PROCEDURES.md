# New Stored Procedures - Quick Start Guide

## 🎉 What's Been Created

I've created **7 powerful stored procedures** for BrightBuy to enhance cart management, product listings, inventory tracking, sales analytics, and order management.

---

## 📦 Files Created

1. **`new_stored_procedures.sql`** - SQL file with all 7 procedures
2. **`apply_new_procedures.py`** - Python script to install procedures
3. **`test_new_procedures.py`** - Test script to verify procedures work
4. **`STORED_PROCEDURES_GUIDE.md`** - Complete documentation with examples

---

## 🚀 Quick Installation (3 Steps)

### Step 1: Install the Procedures
```bash
cd backend
python database/apply_new_procedures.py
```

Expected output:
```
✅ 1. GetUserCart
✅ 2. GetProductsByCategory
✅ 3. GetLowStockVariants
✅ 4. GetSalesReport
✅ 5. UpdateOrderStatus
✅ 6. GetTopSellingProducts
✅ 7. GetCustomerOrderHistory
```

### Step 2: Test the Procedures
```bash
python database/test_new_procedures.py
```

### Step 3: Start Using Them!
```sql
-- Example: Get user's cart
CALL GetUserCart(1);

-- Example: Get low stock items
CALL GetLowStockVariants(10);

-- Example: Sales report
CALL GetSalesReport('2025-01-01', '2025-10-16');
```

---

## 📋 Procedures Overview

### 1. **GetUserCart** 🛒
**What it does**: Fetches complete cart details with product info and stock status

**Usage**:
```sql
CALL GetUserCart(1);  -- Replace 1 with user_id
```

**Returns**: Cart items, prices, stock status, product details

**Use Case**: Display cart page, validate stock before checkout

---

### 2. **GetProductsByCategory** 📦
**What it does**: Gets products by category with pricing and variant counts

**Usage**:
```sql
CALL GetProductsByCategory(1);     -- Category 1
CALL GetProductsByCategory(NULL);  -- All products
```

**Returns**: Products with min/max prices, variant counts, stock totals

**Use Case**: Shop page, category filtering, product listings

---

### 3. **GetLowStockVariants** ⚠️
**What it does**: Identifies variants running low on stock

**Usage**:
```sql
CALL GetLowStockVariants(10);  -- Stock < 10
CALL GetLowStockVariants(50);  -- Stock < 50
```

**Returns**: Low stock items with alert levels (CRITICAL/LOW/OUT OF STOCK)

**Use Case**: Admin inventory dashboard, restock alerts

---

### 4. **GetSalesReport** 📊
**What it does**: Generates comprehensive sales analytics

**Usage**:
```sql
CALL GetSalesReport('2025-01-01', '2025-10-16');  -- Date range
CALL GetSalesReport(NULL, NULL);                   -- Last 30 days
```

**Returns**: Daily sales, revenue, orders, top products, payment methods

**Use Case**: Admin dashboard, business analytics, revenue tracking

---

### 5. **UpdateOrderStatus** 📦
**What it does**: Updates delivery status for orders

**Usage**:
```sql
CALL UpdateOrderStatus(1, 'Shipped');
CALL UpdateOrderStatus(2, 'Delivered');
```

**Valid Statuses**: Pending, Processing, Shipped, Out for Delivery, Delivered, Cancelled

**Use Case**: Order management, delivery tracking

---

### 6. **GetTopSellingProducts** 🏆 (BONUS)
**What it does**: Analyzes best-selling products

**Usage**:
```sql
CALL GetTopSellingProducts(10, 30);  -- Top 10, last 30 days
CALL GetTopSellingProducts(5, 7);    -- Top 5, last 7 days
```

**Returns**: Products ranked by sales with revenue and stock info

**Use Case**: Admin analytics, marketing insights, inventory planning

---

### 7. **GetCustomerOrderHistory** 📜 (BONUS)
**What it does**: Complete order history for a customer

**Usage**:
```sql
CALL GetCustomerOrderHistory(1);  -- User ID 1
```

**Returns**: All orders with items, delivery status, payment info

**Use Case**: Customer profile page, order tracking, customer service

---

## 🔌 FastAPI Integration Example

Create new route file `backend/app/routes/procedures.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db

router = APIRouter(prefix="/api", tags=["Procedures"])

@router.get("/cart/{user_id}/details")
def get_cart_details(user_id: int, db=Depends(get_db)):
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
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetLowStockVariants(%s)", (threshold,))
        items = cursor.fetchall()
        cursor.close()
        return {"low_stock": items, "count": len(items)}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
```

Then in `backend/app/utils/main.py`:
```python
from app.routes import procedures

app.include_router(procedures.router)
```

---

## 💡 Use Cases by Feature

### **Cart Management**
- ✅ `GetUserCart` - Display cart with real-time stock
- ✅ Validate stock before checkout
- ✅ Show "Limited Stock" warnings

### **Product Catalog**
- ✅ `GetProductsByCategory` - Shop page filtering
- ✅ Show price ranges
- ✅ Display variant counts

### **Inventory Management**
- ✅ `GetLowStockVariants` - Admin alerts
- ✅ Restock planning
- ✅ Track sales velocity

### **Admin Dashboard**
- ✅ `GetSalesReport` - Revenue analytics
- ✅ `GetTopSellingProducts` - Best sellers
- ✅ Track daily performance

### **Order Management**
- ✅ `UpdateOrderStatus` - Update delivery status
- ✅ `GetCustomerOrderHistory` - Customer service
- ✅ Order tracking

---

## 🎯 Benefits

| Benefit | Description |
|---------|-------------|
| **Performance** | Optimized SQL runs at database level |
| **Maintainability** | Business logic in one place |
| **Reusability** | Call from any app (FastAPI, mobile, etc.) |
| **Security** | Parameterized queries prevent SQL injection |
| **Scalability** | Database handles complex queries efficiently |

---

## 📊 Example Outputs

### GetUserCart
```json
{
  "cart_id": 1,
  "product_name": "iPhone 15 Pro",
  "variant_name": "256GB Black",
  "quantity": 2,
  "price": 999.99,
  "item_total": 1999.98,
  "stock_status": "In Stock"
}
```

### GetLowStockVariants
```json
{
  "variant_name": "MacBook Pro M3",
  "current_stock": 3,
  "stock_alert_level": "CRITICAL",
  "sold_last_30_days": 15
}
```

### GetSalesReport
```json
{
  "sale_date": "2025-10-16",
  "total_orders": 45,
  "total_revenue": 12450.50,
  "average_order_value": 276.68,
  "top_product": "iPhone 15 Pro"
}
```

---

## 🔧 Troubleshooting

### Issue: "Procedure not found"
**Solution**:
```bash
python database/apply_new_procedures.py
```

### Issue: "Access denied"
**Solution**: Check database credentials in `.env` file

### Issue: "Result set not cleared"
**Solution**: Add `cursor.nextset()` after `fetchall()`

---

## 📚 Documentation

- **Full Guide**: `STORED_PROCEDURES_GUIDE.md` - Complete documentation with all examples
- **SQL File**: `new_stored_procedures.sql` - Raw SQL code
- **Test Script**: `test_new_procedures.py` - Verify procedures work

---

## ✅ Checklist

- [ ] Install procedures (`python database/apply_new_procedures.py`)
- [ ] Test procedures (`python database/test_new_procedures.py`)
- [ ] Create FastAPI routes
- [ ] Update frontend to use new endpoints
- [ ] Build admin dashboard
- [ ] Add authentication to admin routes
- [ ] Implement caching for reports

---

## 🚀 Next Steps

1. **Install the procedures** (5 minutes)
2. **Test them** (2 minutes)
3. **Create FastAPI routes** (30 minutes)
4. **Build admin dashboard UI** (2-3 hours)
5. **Integrate with frontend** (1-2 hours)

---

## 📞 Support

If you encounter any issues:
1. Check `STORED_PROCEDURES_GUIDE.md` for detailed examples
2. Run `test_new_procedures.py` to verify installation
3. Check MySQL error logs
4. Verify database connection in `.env`

---

**Ready to get started?**

```bash
cd backend
python database/apply_new_procedures.py
```

🎉 **That's it! You now have 7 powerful stored procedures ready to use!**
