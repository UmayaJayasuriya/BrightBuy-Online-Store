"""
Apply GetOrderSummary Stored Procedure
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection


procedure_drop = "DROP PROCEDURE IF EXISTS GetOrderSummary;"

procedure_create = """
CREATE PROCEDURE GetOrderSummary (
    IN p_user_id INT
)
BEGIN
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        oi.quantity,
        oi.price,
        p.product_name,
        v.variant_name,
        d.delivery_status
    FROM Orders o
    JOIN Order_Item oi ON o.order_id = oi.order_id
    LEFT JOIN Cart c ON o.cart_id = c.cart_id
    LEFT JOIN Variant v ON oi.variant_id = v.variant_id
    LEFT JOIN Product p ON v.product_id = p.product_id
    LEFT JOIN Delivery d ON o.order_id = d.order_id
    WHERE o.user_id = p_user_id
    ORDER BY o.order_date DESC;
END;
"""


def apply_procedure():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing GetOrderSummary procedure (if any)...")
        cursor.execute(procedure_drop)
        conn.commit()

        print("Creating GetOrderSummary stored procedure...")
        cursor.execute(procedure_create)
        conn.commit()

        print("✅ GetOrderSummary stored procedure created successfully!")
        print("   - Input: p_user_id (INT)")
        print("   - Returns: Order summary with items and delivery status")
        
    except Exception as e:
        print(f"❌ Error creating procedure: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    apply_procedure()
