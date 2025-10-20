"""
Force update database views by dropping and recreating them
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_connection

def force_update_views():
    """Drop and recreate all report views"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        print("🔄 Force updating report views...")
        
        # Drop all views
        views_to_drop = [
            'quarterly_sales_report',
            'top_selling_products',
            'category_order_summary',
            'customer_order_payment_summary',
            'customer_summary_statistics'
        ]
        
        for view in views_to_drop:
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view}")
                print(f"   ✓ Dropped {view}")
            except Exception as e:
                print(f"   ⚠ Warning dropping {view}: {e}")
        
        connection.commit()
        
        # Read and execute SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'views', 'reports_views.sql')
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolon and filter out empty statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print("\n📝 Creating views...")
        for i, statement in enumerate(statements, 1):
            if statement and 'CREATE VIEW' in statement.upper():
                try:
                    cursor.execute(statement)
                    view_name = statement.split('CREATE VIEW')[1].split('AS')[0].strip()
                    print(f"   ✅ Created {view_name}")
                except Exception as e:
                    print(f"   ❌ Error creating view: {e}")
        
        connection.commit()
        
        # Verify views
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        
        print(f"\n✅ Force update complete!")
        print(f"📊 Total views in database: {len(views)}")
        for view in views:
            print(f"   - {view[0]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_update_views()
