"""
Fix only the quarterly_sales_report view
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_connection

def fix_quarterly_view():
    """Fix the quarterly sales report view"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        print("🔄 Fixing quarterly_sales_report view...")
        
        # Drop the view
        cursor.execute("DROP VIEW IF EXISTS quarterly_sales_report")
        print("   ✓ Dropped old view")
        
        # Create the fixed view
        create_view_sql = """
        CREATE VIEW quarterly_sales_report AS
        SELECT 
            year,
            quarter,
            CONCAT('Q', quarter, ' ', year) AS quarter_label,
            total_orders,
            unique_customers,
            total_revenue,
            average_order_value,
            total_items_sold
        FROM (
            SELECT 
                YEAR(o.order_date) AS year,
                QUARTER(o.order_date) AS quarter,
                COUNT(DISTINCT o.order_id) AS total_orders,
                COUNT(DISTINCT o.user_id) AS unique_customers,
                SUM(o.total_amount) AS total_revenue,
                AVG(o.total_amount) AS average_order_value,
                SUM(oi.quantity) AS total_items_sold
            FROM orders o
            LEFT JOIN order_item oi ON o.order_id = oi.order_id
            GROUP BY YEAR(o.order_date), QUARTER(o.order_date)
        ) AS quarterly_data
        ORDER BY year DESC, quarter DESC
        """
        
        cursor.execute(create_view_sql)
        print("   ✅ Created fixed view")
        
        connection.commit()
        
        # Test the view
        cursor.execute("SELECT * FROM quarterly_sales_report LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            print("\n✅ View is working! Sample data:")
            print(f"   Year: {result[0]}, Quarter: {result[1]}, Label: {result[2]}")
        else:
            print("\n⚠️  View created but no data found (this is okay if no orders exist)")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Quarterly sales report view fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_quarterly_view()
