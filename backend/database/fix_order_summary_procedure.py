"""
Fix GetOrderSummary Stored Procedure
Corrects the JOIN condition to prevent Cartesian product
"""

import sys
sys.path.insert(0, '.')
from app.database import get_connection

def fix_procedure():
    """Fix the GetOrderSummary procedure with correct JOIN"""
    
    procedure_sql = """
CREATE PROCEDURE GetOrderSummary(
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
    FROM orders o
    JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN variant v ON oi.variant_id = v.variant_id
    LEFT JOIN product p ON v.product_id = p.product_id
    LEFT JOIN delivery d ON o.order_id = d.order_id
    WHERE o.user_id = p_user_id
    ORDER BY o.order_date DESC;
END
"""
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("🔧 Fixing GetOrderSummary procedure...")
        print("-" * 80)
        
        # Drop existing procedure
        print("Dropping existing procedure...")
        cursor.execute("DROP PROCEDURE IF EXISTS GetOrderSummary")
        conn.commit()
        print("✅ Dropped")
        
        # Create corrected procedure
        print("\nCreating corrected procedure...")
        cursor.execute(procedure_sql)
        conn.commit()
        print("✅ Created with correct JOIN condition")
        
        print("\n" + "=" * 80)
        print("✅ GetOrderSummary procedure fixed successfully!")
        print("=" * 80)
        print("\nKey fix:")
        print("  OLD: LEFT JOIN Variant v ON oi.order_id = o.order_id")
        print("  NEW: LEFT JOIN variant v ON oi.variant_id = v.variant_id")
        print("\nThis prevents the Cartesian product that was creating duplicates.")
        
    except Exception as e:
        print(f"\n❌ Error fixing procedure: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_procedure()
