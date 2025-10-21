"""
Order Routes - MySQL Connector Version
"""
from fastapi import APIRouter, HTTPException, status
from app.database import get_connection
from app.schemas.order import OrderOut, CreateOrderRequest, OrderItemOut
from typing import List
from datetime import datetime, timedelta
from app.services.email_service import send_order_confirmation

router = APIRouter(prefix="/orders", tags=["orders"])



@router.post("/checkout", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(request: CreateOrderRequest):
    """
    Create an order from the user's cart with payment and delivery information
    Converts cart items to order items and clears the cart
    """
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Start transaction
        conn.start_transaction()
        
        # Handle address creation if new address details provided
        address_id = request.address_id
        if request.delivery_method == "home_delivery":
            if request.address_details:
                # Find city_id from location table
                cursor.execute(
                    "SELECT city_id, Is_main_city FROM location WHERE city = %s",
                    (request.address_details.city,)
                )
                location = cursor.fetchone()
                
                if not location:
                    raise HTTPException(
                        status_code=400,
                        detail=f"City '{request.address_details.city}' not found in location database"
                    )
                
                # Create new address
                cursor.execute(
                    """INSERT INTO address (house_number, street, city, state, city_id) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        request.address_details.house_number,
                        request.address_details.street,
                        request.address_details.city,
                        request.address_details.state,
                        location['city_id']
                    )
                )
                address_id = cursor.lastrowid
            elif not address_id:
                raise HTTPException(
                    status_code=400,
                    detail="Address is required for home delivery"
                )
        
        # Get user's cart
        cursor.execute(
            "SELECT cart_id, total_amount FROM cart WHERE user_id = %s",
            (request.user_id,)
        )
        cart = cursor.fetchone()
        
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        # Get cart items with variant details
        cursor.execute(
            """SELECT ci.cart_item_id, ci.variant_id, ci.quantity, 
                      v.variant_name, v.price, v.quantity as stock_quantity
               FROM cart_item ci
               JOIN variant v ON ci.variant_id = v.variant_id
               WHERE ci.cart_id = %s""",
            (cart['cart_id'],)
        )
        cart_items = cursor.fetchall()
        
        if not cart_items or len(cart_items) == 0:
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        # Calculate total amount and check stock
        total_amount = 0.0
        for item in cart_items:
            # Check stock
            if item['stock_quantity'] < item['quantity']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {item['variant_name']}. Available: {item['stock_quantity']}, Requested: {item['quantity']}"
                )
            total_amount += float(item['price']) * item['quantity']
        
        # Create order
        cursor.execute(
            """INSERT INTO orders (cart_id, user_id, order_date, total_amount) 
               VALUES (%s, %s, %s, %s)""",
            (cart['cart_id'], request.user_id, datetime.utcnow(), total_amount)
        )
        order_id = cursor.lastrowid
        
        # Create order items and reduce variant quantities
        for cart_item in cart_items:
            item_price = float(cart_item['price'])
            
            # Insert order item
            cursor.execute(
                """INSERT INTO order_item (order_id, variant_id, quantity, price) 
                   VALUES (%s, %s, %s, %s)""",
                (order_id, cart_item['variant_id'], cart_item['quantity'], item_price)
            )
            
            # Reduce variant quantity
            cursor.execute(
                """UPDATE variant SET quantity = quantity - %s 
                   WHERE variant_id = %s""",
                (cart_item['quantity'], cart_item['variant_id'])
            )
        
        # Create payment record
        payment_status = "completed" if request.payment_method == "card" else "pending"
        cursor.execute(
            """INSERT INTO payment (order_id, payment_method, payment_status, payment_date) 
               VALUES (%s, %s, %s, %s)""",
            (order_id, request.payment_method, payment_status, datetime.utcnow())
        )
        
        # Store card details if card payment
        if request.payment_method == "card" and request.card_details:
            cursor.execute(
                """INSERT INTO card (order_id, card_number, card_name, expiry_date, CVV) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (
                    order_id,
                    request.card_details.card_number,
                    request.card_details.card_name,
                    request.card_details.expiry_date,
                    request.card_details.cvv
                )
            )
        
        # Calculate estimated delivery date
        estimated_date = None
        estimated_days = 0
        is_main_city = False
        
        if request.delivery_method == "home_delivery" and address_id:
            # Get Is_main_city for the address
            cursor.execute(
                """SELECT l.Is_main_city 
                   FROM address a 
                   JOIN location l ON a.city_id = l.city_id 
                   WHERE a.address_id = %s""",
                (address_id,)
            )
            location_info = cursor.fetchone()
            if location_info:
                is_main_city = location_info['Is_main_city']
            
            # Calculate base delivery days based on city type
            base_days = 5 if is_main_city else 7
            
            # Check for low stock variants (quantity < 10)
            has_low_stock = False
            for cart_item in cart_items:
                if cart_item['stock_quantity'] < 10:
                    has_low_stock = True
                    break
            
            # Add 3 days if any variant has low stock
            if has_low_stock:
                base_days += 3
            
            estimated_days = base_days
            estimated_date = (datetime.utcnow() + timedelta(days=base_days)).date()
            
        elif request.delivery_method == "store_pickup":
            # Store pickup: 2 days
            estimated_days = 2
            estimated_date = (datetime.utcnow() + timedelta(days=2)).date()
        
        # Create delivery record
        cursor.execute(
            """INSERT INTO delivery (order_id, delivery_method, address_id, estimated_delivery_date, delivery_status) 
               VALUES (%s, %s, %s, %s, %s)""",
            (order_id, request.delivery_method, address_id, estimated_date, "pending")
        )
        
        # Clear cart items
        cursor.execute("DELETE FROM cart_item WHERE cart_id = %s", (cart['cart_id'],))
        
        # Reset cart total
        cursor.execute("UPDATE cart SET total_amount = 0 WHERE cart_id = %s", (cart['cart_id'],))

        # Commit transaction
        conn.commit()

        # Get order items with product details for response
        cursor.execute(
            """SELECT oi.order_item_id, oi.order_id, oi.variant_id, oi.quantity, oi.price,
                      v.variant_name, v.product_id, p.product_name
               FROM order_item oi
               JOIN variant v ON oi.variant_id = v.variant_id
               JOIN product p ON v.product_id = p.product_id
               WHERE oi.order_id = %s""",
            (order_id,)
        )
        order_items = cursor.fetchall()
        
        # Build order items response
        order_items_out = []
        for item in order_items:
            order_items_out.append(OrderItemOut(
                order_item_id=item['order_item_id'],
                order_id=item['order_id'],
                variant_id=item['variant_id'],
                quantity=item['quantity'],
                price=float(item['price']),
                variant_name=item['variant_name'],
                product_name=item['product_name'],
                product_id=item['product_id']
            ))

        # Attempt to send order confirmation email (best-effort)
        try:
            # Fetch user email and name
            cursor.execute("SELECT user_name, email, name FROM user WHERE user_id = %s", (request.user_id,))
            user_row = cursor.fetchone()
            to_email = user_row['email'] if user_row and user_row.get('email') else None
            user_name = user_row.get('name') or user_row.get('user_name') if user_row else "Customer"

            if to_email:
                # Prepare items payload for email
                items_for_email = [
                    {
                        'product_name': it['product_name'],
                        'variant_name': it['variant_name'],
                        'quantity': it['quantity'],
                        'price': float(it['price'])
                    }
                    for it in order_items
                ]

                send_order_confirmation(
                    to_email=to_email,
                    user_name=user_name,
                    order_id=order_id,
                    items=items_for_email,
                    total_amount=total_amount,
                    payment_method=request.payment_method,
                    delivery_method=request.delivery_method,
                    estimated_date=estimated_date.isoformat() if estimated_date else None,
                    estimated_days=estimated_days if estimated_days else None,
                )
        except Exception:
            # Do not fail the request on email issues
            pass
        
        return OrderOut(
            order_id=order_id,
            cart_id=cart['cart_id'],
            user_id=request.user_id,
            order_date=datetime.utcnow(),
            total_amount=total_amount,
            estimated_delivery_date=estimated_date.isoformat() if estimated_date else None,
            estimated_delivery_days=estimated_days if estimated_days > 0 else None,
            order_items=order_items_out
        )
        
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating order: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: int):
    """
    Get all orders for a specific user
    """
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all orders for the user
        cursor.execute(
            """SELECT order_id, cart_id, user_id, order_date, total_amount
               FROM orders
               WHERE user_id = %s
               ORDER BY order_date DESC""",
            (user_id,)
        )
        orders = cursor.fetchall()
        
        if not orders:
            return []
        
        # For each order, get its items
        result_orders = []
        for order in orders:
            cursor.execute(
                """SELECT oi.order_item_id, oi.order_id, oi.variant_id, oi.quantity, oi.price,
                          v.variant_name, v.product_id, p.product_name
                   FROM order_item oi
                   JOIN variant v ON oi.variant_id = v.variant_id
                   JOIN product p ON v.product_id = p.product_id
                   WHERE oi.order_id = %s""",
                (order['order_id'],)
            )
            order_items = cursor.fetchall()
            
            # Build order items
            order_items_out = []
            for item in order_items:
                order_items_out.append(OrderItemOut(
                    order_item_id=item['order_item_id'],
                    order_id=item['order_id'],
                    variant_id=item['variant_id'],
                    quantity=item['quantity'],
                    price=float(item['price']),
                    variant_name=item['variant_name'],
                    product_name=item['product_name'],
                    product_id=item['product_id']
                ))
            
            result_orders.append(OrderOut(
                order_id=order['order_id'],
                cart_id=order['cart_id'],
                user_id=order['user_id'],
                order_date=order['order_date'],
                total_amount=float(order['total_amount']),
                order_items=order_items_out
            ))
        
        return result_orders
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching orders: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
