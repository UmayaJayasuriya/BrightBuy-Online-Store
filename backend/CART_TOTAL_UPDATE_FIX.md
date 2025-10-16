# Cart Total Update Fix

## Issue

When updating cart item quantities from the frontend, the `total_amount` in the cart table was not being recalculated, causing:

- The cart summary total on the right side to show incorrect value
- The cart badge count in the header to not update

## Root Cause

All cart modification endpoints (add, update, remove, clear) were updating the `cart_item` table but not recalculating and updating the `total_amount` column in the `cart` table.

## Solution

Added total recalculation logic to all cart modification endpoints:

### 1. **Add to Cart** (`POST /cart/add`)

```python
# After adding/updating item, recalculate total
cursor.execute("""
    SELECT SUM(ci.quantity * v.price) as total
    FROM cart_item ci
    JOIN variant v ON ci.variant_id = v.variant_id
    WHERE ci.cart_id = %s
""", (cart_id,))
total_result = cursor.fetchone()
new_total = float(total_result['total']) if total_result and total_result['total'] else 0.0

# Update cart total
cursor.execute(
    "UPDATE cart SET total_amount = %s WHERE cart_id = %s",
    (new_total, cart_id)
)
```

### 2. **Update Cart Item** (`PUT /cart/update/{cart_item_id}`)

- Gets `cart_id` from the cart_item before updating
- Updates the quantity
- Recalculates total using SUM query
- Updates `cart.total_amount`
- Returns `new_total` in response

### 3. **Remove Cart Item** (`DELETE /cart/remove/{cart_item_id}`)

- Gets `cart_id` before deleting
- Deletes the item
- Recalculates remaining total
- Updates `cart.total_amount`
- Returns `new_total` in response

### 4. **Clear Cart** (`DELETE /cart/clear/{user_id}`)

- Deletes all cart items
- Sets `cart.total_amount` to 0
- Returns `new_total: 0.0`

## Test Results ✅

### Before Fix:

```
Initial cart total: $2518.99
Update item quantity from 1 to 3
Cart total: $2518.99 (unchanged ❌)
```

### After Fix:

```
Initial cart total: $2518.99
Update item quantity from 1 to 3
Cart total: $6575.97 (correctly updated ✅)
```

## API Response Changes

All modification endpoints now return `new_total` in their response:

```json
{
  "message": "Cart item updated successfully",
  "new_total": 6575.97
}
```

This allows the frontend to immediately update the UI with the new total without making an additional GET request.

## Impact

- ✅ Cart summary total updates immediately
- ✅ Header cart badge shows correct total
- ✅ No need for frontend to refetch entire cart
- ✅ Database stays in sync
- ✅ Better user experience
