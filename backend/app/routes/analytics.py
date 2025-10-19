"""
Analytics Routes - Stored Procedures Implementation
Provides endpoints for cart details, inventory management, sales reports, and analytics
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from datetime import date, timedelta
from pydantic import BaseModel
from app.database import get_db
import mysql.connector

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ============================================
# Pydantic Models
# ============================================

class CartItemDetail(BaseModel):
    cart_id: int
    user_id: int
    cart_total: float
    cart_item_id: Optional[int] = None
    variant_id: Optional[int] = None
    quantity: Optional[int] = None
    variant_name: Optional[str] = None
    price: Optional[float] = None
    SKU: Optional[str] = None
    stock_available: Optional[int] = None
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    description: Optional[str] = None
    category_name: Optional[str] = None
    item_total: Optional[float] = None
    stock_status: Optional[str] = None


class ProductByCategory(BaseModel):
    product_id: int
    product_name: str
    description: Optional[str] = None
    category_id: int
    category_name: str
    variant_count: int
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    total_stock: Optional[int] = None
    availability_status: str


class LowStockVariant(BaseModel):
    variant_id: int
    variant_name: str
    current_stock: int
    price: float
    SKU: str
    product_id: int
    product_name: str
    category_id: int
    category_name: str
    threshold: int
    stock_alert_level: str
    sold_last_30_days: int


class SalesReportDay(BaseModel):
    sale_date: date
    total_orders: int
    unique_customers: int
    total_revenue: float
    average_order_value: float
    total_items_sold: int
    top_product: Optional[str] = None
    card_revenue: Optional[float] = None
    cash_revenue: Optional[float] = None


class OrderStatusUpdate(BaseModel):
    status: str


class TopSellingProduct(BaseModel):
    product_id: int
    product_name: str
    category_name: str
    times_ordered: int
    total_quantity_sold: int
    total_revenue: float
    average_price: float
    lowest_variant_stock: int


class CustomerOrder(BaseModel):
    order_id: int
    order_date: date
    total_amount: float
    delivery_status: Optional[str] = None
    delivery_date: Optional[date] = None
    payment_method: Optional[str] = None
    total_items: int
    total_quantity: int
    order_items: Optional[str] = None
    days_since_order: int


# ============================================
# 1. GetUserCart - Cart Details
# ============================================

@router.get("/cart/{user_id}", response_model=dict)
def get_user_cart_details(
    user_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Get complete cart details for a user with product information and stock status
    
    - **user_id**: User ID to fetch cart for
    
    Returns cart items with:
    - Product details
    - Pricing information
    - Stock availability
    - Stock status (In Stock/Limited Stock/Out of Stock)
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Call stored procedure
        cursor.execute("CALL GetUserCart(%s)", (user_id,))
        cart_items = cursor.fetchall()
        
        # Calculate summary
        total_items = len([item for item in cart_items if item.get('cart_item_id')])
        total_quantity = sum(item.get('quantity', 0) or 0 for item in cart_items)
        cart_total = cart_items[0].get('cart_total', 0) if cart_items else 0
        
        # Check for out of stock items
        out_of_stock = [item for item in cart_items if item.get('stock_status') == 'Out of Stock']
        low_stock = [item for item in cart_items if item.get('stock_status') == 'Limited Stock']
        
        cursor.close()
        
        return {
            "user_id": user_id,
            "cart_total": float(cart_total) if cart_total else 0.0,
            "total_items": total_items,
            "total_quantity": total_quantity,
            "cart_items": cart_items,
            "warnings": {
                "out_of_stock_count": len(out_of_stock),
                "low_stock_count": len(low_stock),
                "out_of_stock_items": [item.get('product_name') for item in out_of_stock],
                "low_stock_items": [item.get('product_name') for item in low_stock]
            }
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching cart: {str(e)}")


# ============================================
# 2. GetProductsByCategory - Product Listing
# ============================================

@router.get("/products/category", response_model=dict)
def get_products_by_category(
    category_id: Optional[int] = Query(None, description="Category ID (NULL for all products)"),
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Get products by category with pricing information and variant counts
    
    - **category_id**: Category ID (omit or pass null for all products)
    
    Returns:
    - Product details
    - Price range (min/max)
    - Variant count
    - Total stock
    - Availability status
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Call stored procedure
        cursor.execute("CALL GetProductsByCategory(%s)", (category_id,))
        products = cursor.fetchall()
        
        # Calculate statistics
        total_products = len(products)
        available_products = len([p for p in products if p.get('availability_status') == 'Available'])
        out_of_stock = len([p for p in products if p.get('availability_status') == 'Out of Stock'])
        
        cursor.close()
        
        return {
            "category_id": category_id,
            "total_products": total_products,
            "available_products": available_products,
            "out_of_stock_products": out_of_stock,
            "products": products
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


# ============================================
# 3. GetLowStockVariants - Inventory Management
# ============================================

@router.get("/inventory/low-stock", response_model=dict)
def get_low_stock_variants(
    threshold: int = Query(10, description="Stock level threshold", ge=1),
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Get variants with stock below threshold for inventory management
    
    - **threshold**: Stock level threshold (default: 10)
    
    Returns variants with:
    - Current stock level
    - Alert level (OUT OF STOCK/CRITICAL/LOW)
    - Sales velocity (last 30 days)
    - Product and category information
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Call stored procedure
        cursor.execute("CALL GetLowStockVariants(%s)", (threshold,))
        low_stock_items = cursor.fetchall()
        
        # Categorize by alert level
        out_of_stock = [item for item in low_stock_items if item.get('stock_alert_level') == 'OUT OF STOCK']
        critical = [item for item in low_stock_items if item.get('stock_alert_level') == 'CRITICAL']
        low = [item for item in low_stock_items if item.get('stock_alert_level') == 'LOW']
        
        # Calculate total value at risk
        total_value_at_risk = sum(
            (item.get('current_stock', 0) or 0) * (item.get('price', 0) or 0) 
            for item in low_stock_items
        )
        
        cursor.close()
        
        return {
            "threshold": threshold,
            "total_low_stock_items": len(low_stock_items),
            "summary": {
                "out_of_stock": len(out_of_stock),
                "critical": len(critical),
                "low": len(low),
                "total_value_at_risk": round(total_value_at_risk, 2)
            },
            "low_stock_items": low_stock_items,
            "urgent_action_required": out_of_stock + critical  # Items needing immediate attention
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching low stock: {str(e)}")


# ============================================
# 4. GetSalesReport - Sales Analytics
# ============================================

@router.get("/sales/report", response_model=dict)
def get_sales_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Generate comprehensive sales report for a date range
    
    - **start_date**: Start date (default: 30 days ago)
    - **end_date**: End date (default: today)
    
    Returns:
    - Daily sales breakdown
    - Revenue metrics
    - Order statistics
    - Top products
    - Payment method breakdown
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Set defaults
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Call stored procedure
        cursor.execute("CALL GetSalesReport(%s, %s)", (start_date, end_date))
        daily_sales = cursor.fetchall()
        
        # Calculate summary statistics
        total_revenue = sum(float(day.get('total_revenue', 0) or 0) for day in daily_sales)
        total_orders = sum(int(day.get('total_orders', 0) or 0) for day in daily_sales)
        total_customers = len(set(day.get('unique_customers', 0) for day in daily_sales if day.get('unique_customers')))
        total_items_sold = sum(int(day.get('total_items_sold', 0) or 0) for day in daily_sales)
        
        # Calculate averages
        num_days = len(daily_sales) if daily_sales else 1
        avg_daily_revenue = total_revenue / num_days
        avg_daily_orders = total_orders / num_days
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Payment breakdown
        total_card_revenue = sum(float(day.get('card_revenue', 0) or 0) for day in daily_sales)
        total_cash_revenue = sum(float(day.get('cash_revenue', 0) or 0) for day in daily_sales)
        
        cursor.close()
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date,
                "days": num_days
            },
            "summary": {
                "total_revenue": round(total_revenue, 2),
                "total_orders": total_orders,
                "unique_customers": total_customers,
                "total_items_sold": total_items_sold,
                "average_daily_revenue": round(avg_daily_revenue, 2),
                "average_daily_orders": round(avg_daily_orders, 2),
                "average_order_value": round(avg_order_value, 2)
            },
            "payment_breakdown": {
                "card_revenue": round(total_card_revenue, 2),
                "cash_revenue": round(total_cash_revenue, 2),
                "card_percentage": round((total_card_revenue / total_revenue * 100) if total_revenue > 0 else 0, 2),
                "cash_percentage": round((total_cash_revenue / total_revenue * 100) if total_revenue > 0 else 0, 2)
            },
            "daily_sales": daily_sales
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating sales report: {str(e)}")


# ============================================
# 5. UpdateOrderStatus - Order Management
# ============================================

@router.put("/orders/{order_id}/status", response_model=dict)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Update delivery status for an order
    
    - **order_id**: Order ID to update
    - **status**: New delivery status
    
    Valid statuses:
    - Pending
    - Processing
    - Shipped
    - Out for Delivery
    - Delivered
    - Cancelled
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Validate status
        valid_statuses = ['Pending', 'Processing', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled']
        if status_update.status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Try stored procedure first; if missing, fallback to direct UPDATE
        result = None
        try:
            cursor.execute("CALL UpdateOrderStatus(%s, %s)", (order_id, status_update.status))
            result = cursor.fetchone()
        except mysql.connector.Error as proc_err:
            # ER_SP_DOES_NOT_EXIST: 1305 - procedure does not exist
            if proc_err.errno == 1305 or "does not exist" in str(proc_err):
                # Perform direct update on delivery table
                # Ensure delivery row exists for order
                cursor.execute("SELECT delivery_id FROM delivery WHERE order_id = %s", (order_id,))
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
                # Update delivery status directly
                cursor.execute(
                    "UPDATE delivery SET delivery_status = %s WHERE order_id = %s",
                    (status_update.status, order_id)
                )
            else:
                raise
        
        db.commit()
        cursor.close()
        
        return {
            "success": True,
            "order_id": order_id,
            "new_status": status_update.status,
            "message": result.get('message', 'Status updated successfully') if result else 'Status updated successfully',
            "updated_at": result.get('updated_at') if result else None
        }
        
    except mysql.connector.Error as e:
        db.rollback()
        if cursor:
            cursor.close()
        
        # Handle specific errors
        if "Order not found" in str(e):
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error updating order status: {str(e)}")


# ============================================
# 6. GetTopSellingProducts - Best Sellers (BONUS)
# ============================================

@router.get("/products/top-selling", response_model=dict)
def get_top_selling_products(
    limit: int = Query(10, description="Number of products to return", ge=1, le=100),
    days: int = Query(30, description="Number of days to look back", ge=1, le=365),
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Get best-selling products by quantity or revenue
    
    - **limit**: Number of products to return (default: 10, max: 100)
    - **days**: Number of days to look back (default: 30, max: 365)
    
    Returns:
    - Top selling products
    - Sales metrics
    - Revenue data
    - Current stock levels
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Call stored procedure
        cursor.execute("CALL GetTopSellingProducts(%s, %s)", (limit, days))
        top_products = cursor.fetchall()
        
        # Calculate totals
        total_quantity_sold = sum(int(p.get('total_quantity_sold', 0) or 0) for p in top_products)
        total_revenue = sum(float(p.get('total_revenue', 0) or 0) for p in top_products)
        
        cursor.close()
        
        return {
            "period_days": days,
            "limit": limit,
            "total_products": len(top_products),
            "summary": {
                "total_quantity_sold": total_quantity_sold,
                "total_revenue": round(total_revenue, 2)
            },
            "top_products": top_products
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching top selling products: {str(e)}")


# ============================================
# 7. GetCustomerOrderHistory - Order History (BONUS)
# ============================================

@router.get("/customers/{user_id}/order-history", response_model=dict)
def get_customer_order_history(
    user_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    """
    Get complete order history for a customer
    
    - **user_id**: User ID to fetch order history for
    
    Returns:
    - All orders with details
    - Delivery status
    - Payment information
    - Order items
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Call stored procedure
        cursor.execute("CALL GetCustomerOrderHistory(%s)", (user_id,))
        orders = cursor.fetchall()
        
        # Calculate statistics
        total_orders = len(orders)
        total_spent = sum(float(order.get('total_amount', 0) or 0) for order in orders)
        total_items = sum(int(order.get('total_quantity', 0) or 0) for order in orders)
        
        # Order status breakdown
        delivered = len([o for o in orders if o.get('delivery_status') == 'Delivered'])
        pending = len([o for o in orders if o.get('delivery_status') in ['Pending', 'Processing']])
        in_transit = len([o for o in orders if o.get('delivery_status') in ['Shipped', 'Out for Delivery']])
        
        cursor.close()
        
        return {
            "user_id": user_id,
            "total_orders": total_orders,
            "summary": {
                "total_spent": round(total_spent, 2),
                "total_items_purchased": total_items,
                "average_order_value": round(total_spent / total_orders, 2) if total_orders > 0 else 0
            },
            "order_status_breakdown": {
                "delivered": delivered,
                "in_transit": in_transit,
                "pending": pending
            },
            "orders": orders
        }
        
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching order history: {str(e)}")
