# Variant Quantity Management System

## Overview

Automatic inventory management system that reduces variant quantities when orders are placed and prevents negative stock levels.

## Components

### 1. Database Trigger

**File:** `backend/database/triggers/variant_quantity_trigger.sql`

```sql
CREATE TRIGGER check_variant_quantity
BEFORE UPDATE ON variant
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity cannot be negative';
    END IF;
END
```

**Purpose:** Prevents variant quantities from going negative at the database level.

### 2. Backend Logic

**File:** `backend/app/routes/order.py`

**Location:** `create_order_from_cart()` function

**Implementation:**

```python
# Check stock availability
if variant and variant.quantity < cart_item.quantity:
    raise HTTPException(
        status_code=400,
        detail=f"Insufficient stock for {variant.variant_name}"
    )

# Reduce variant quantity
if variant:
    variant.quantity -= cart_item.quantity
    db.add(variant)  # Mark for update
```

## How It Works

### Order Flow

1. **User places order**

   - Frontend sends order request to `/orders/checkout`

2. **Stock validation** (Application Layer)

   - System checks each cart item against variant stock
   - If `variant.quantity < requested_quantity`:
     - ❌ Order rejected
     - Returns HTTP 400: "Insufficient stock"

3. **Quantity reduction** (Application Layer)

   - For each order item:
     - `variant.quantity -= ordered_quantity`
     - Variant marked for database update

4. **Database validation** (Database Layer)

   - Trigger `check_variant_quantity` fires BEFORE UPDATE
   - Checks if `NEW.quantity < 0`
   - If true:
     - ❌ Update rejected
     - SQLSTATE '45000' error raised
     - Transaction rolled back

5. **Success**
   - ✅ Variant quantities updated
   - ✅ Order created
   - ✅ Cart cleared

## Multi-Layer Protection

### Layer 1: Frontend (Future Enhancement)

- Could add client-side stock display
- Show "Only X left!" messages
- Disable checkout if out of stock

### Layer 2: Backend Application

**File:** `backend/app/routes/order.py`

- Checks stock before processing order
- Provides specific error messages
- Prevents unnecessary database calls

```python
if variant.quantity < cart_item.quantity:
    raise HTTPException(
        status_code=400,
        detail=f"Insufficient stock for {variant.variant_name}. "
               f"Available: {variant.quantity}, "
               f"Requested: {cart_item.quantity}"
    )
```

### Layer 3: Database Trigger ⭐

**File:** `backend/database/triggers/variant_quantity_trigger.sql`

- Final safety net
- Protects against:
  - Direct SQL updates
  - Concurrent order race conditions
  - Application bugs
- Cannot be bypassed

## Error Handling

### Insufficient Stock Error

**HTTP Status:** 400 Bad Request

**Scenario:** Cart item quantity > variant stock

**Response:**

```json
{
  "detail": "Insufficient stock for iPhone 17 Pro. Available: 5, Requested: 10"
}
```

### Negative Quantity Trigger Error

**HTTP Status:** 400 Bad Request

**Scenario:** Update would make quantity negative (edge case/race condition)

**Response:**

```json
{
  "detail": "Insufficient stock. One or more items in your cart are out of stock."
}
```

**Code:**

```python
except Exception as e:
    error_msg = str(e)
    if "Quantity cannot be negative" in error_msg or "45000" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock. One or more items in your cart are out of stock."
        )
```

## Installation

### 1. Apply Trigger

```bash
cd backend
python database/apply_variant_trigger.py
```

### 2. Verify Installation

```bash
python database/verify_variant_trigger.py
```

Expected output:

```
✅ Variant trigger verified!
   Name: check_variant_quantity
   Event: UPDATE
   Table: variant
   Timing: BEFORE
```

### 3. Test System

```bash
python database/test_variant_reduction.py
```

## Testing

### Manual Test: Place Order

1. **Check variant stock**

```sql
SELECT variant_id, variant_name, quantity FROM variant WHERE variant_id = 1;
```

2. **Add to cart and checkout**

- Add variant to cart
- Proceed to checkout
- Complete order

3. **Verify quantity reduced**

```sql
SELECT variant_id, variant_name, quantity FROM variant WHERE variant_id = 1;
```

Expected: Quantity reduced by ordered amount

### Test Insufficient Stock

1. **Set low stock**

```sql
UPDATE variant SET quantity = 2 WHERE variant_id = 1;
```

2. **Try to order 5 units**

- Add 5 units to cart
- Attempt checkout

Expected: HTTP 400 error with "Insufficient stock" message

### Test Negative Quantity Protection

1. **Direct SQL attempt** (will fail)

```sql
UPDATE variant SET quantity = -5 WHERE variant_id = 1;
```

Expected: Error "Quantity cannot be negative"

## Database Schema Impact

### Variant Table

No schema changes required. Uses existing `quantity` column.

```sql
CREATE TABLE variant (
    variant_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    variant_name VARCHAR(100),
    price DECIMAL(10, 2),
    quantity INT,  -- ← Reduced when orders placed
    ...
);
```

## Benefits

✅ **Automatic Inventory Management**

- No manual stock updates needed
- Real-time quantity tracking

✅ **Prevents Overselling**

- Stock checked before order confirmation
- Database trigger as final protection

✅ **Race Condition Protection**

- Trigger prevents concurrent orders from overselling
- Transaction rollback on stock conflicts

✅ **User-Friendly Errors**

- Clear messages about stock availability
- Specific product names in error messages

✅ **Data Integrity**

- Quantities always accurate
- No negative stock values possible

## Integration Points

### 1. Cart System

- Shows available stock (future enhancement)
- Validates quantities on add to cart

### 2. Order Creation

- `POST /orders/checkout`
- Reduces quantities automatically
- Validates stock before processing

### 3. Product Display

- Can show current stock levels
- "In Stock" / "Out of Stock" badges

### 4. Admin Panel (Future)

- Manual stock adjustments
- Inventory reports
- Low stock alerts

## Maintenance

### View Current Stock

```sql
SELECT
    v.variant_id,
    v.variant_name,
    v.quantity,
    p.product_name
FROM variant v
JOIN product p ON v.product_id = p.product_id
ORDER BY v.quantity ASC;
```

### Check Low Stock

```sql
SELECT * FROM variant WHERE quantity < 10;
```

### Restock Variant

```sql
UPDATE variant
SET quantity = quantity + 50
WHERE variant_id = 1;
```

### View Order Impact

```sql
SELECT
    oi.variant_id,
    v.variant_name,
    SUM(oi.quantity) as total_sold,
    v.quantity as current_stock
FROM order_item oi
JOIN variant v ON oi.variant_id = v.variant_id
WHERE oi.order_id IN (
    SELECT order_id FROM orders
    WHERE order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
)
GROUP BY oi.variant_id;
```

## Related Files

- `backend/app/routes/order.py` - Order creation with quantity reduction
- `backend/database/triggers/variant_quantity_trigger.sql` - SQL trigger
- `backend/database/apply_variant_trigger.py` - Trigger installation
- `backend/database/verify_variant_trigger.py` - Trigger verification
- `backend/database/test_variant_reduction.py` - Testing script

## Troubleshooting

### Issue: Trigger not firing

**Solution:**

```bash
cd backend
python database/apply_variant_trigger.py
python database/verify_variant_trigger.py
```

### Issue: Stock not reducing

**Check:**

1. Trigger installed? `SHOW TRIGGERS LIKE 'check_variant_quantity';`
2. Order created? Check `orders` and `order_item` tables
3. Variant updated? Check variant table

### Issue: False "out of stock" errors

**Check:**

1. Current stock: `SELECT quantity FROM variant WHERE variant_id = ?`
2. Cart quantities
3. Concurrent orders (race condition)

## Future Enhancements

- [ ] Add stock reservation during checkout process
- [ ] Implement low stock notifications
- [ ] Add restock alerts for admins
- [ ] Show real-time stock on product pages
- [ ] Add stock history/audit trail
- [ ] Implement backorder system
- [ ] Add bulk stock import/export
