import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_connection

def check_constraints():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        print("=" * 60)
        print("CHECKING ALL TABLES IN DATABASE")
        print("=" * 60)
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\nTables in brightbuy database:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
        
        print("\n" + "=" * 60)
        print("CHECKING FOR TRIGGERS ON PRODUCT TABLE")
        print("=" * 60)
        cursor.execute("SHOW TRIGGERS WHERE `Table` = 'product'")
        triggers = cursor.fetchall()
        if triggers:
            print("\nTriggers found:")
            for trigger in triggers:
                print(f"\nTrigger: {trigger['Trigger']}")
                print(f"  Event: {trigger['Event']}")
                print(f"  Timing: {trigger['Timing']}")
                print(f"  Statement: {trigger['Statement']}")
        else:
            print("\nNo triggers found on 'product' table")
        
        print("\n" + "=" * 60)
        print("CHECKING FOREIGN KEYS REFERENCING PRODUCT")
        print("=" * 60)
        cursor.execute("""
            SELECT 
                CONSTRAINT_NAME,
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'brightbuy'
            AND REFERENCED_TABLE_NAME = 'product'
        """)
        
        fks = cursor.fetchall()
        if fks:
            print("\nForeign keys referencing 'product':")
            for fk in fks:
                print(f"  - {fk['TABLE_NAME']}.{fk['COLUMN_NAME']} -> {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}")
                print(f"    Constraint: {fk['CONSTRAINT_NAME']}")
        else:
            print("\nNo foreign keys reference 'product'")
        
        print("\n" + "=" * 60)
        print("TRYING TO DELETE PRODUCT 42 (DRY RUN)")
        print("=" * 60)
        
        # Start a transaction
        conn.start_transaction()
        
        try:
            print("\n1. Checking if product exists...")
            cursor.execute("SELECT * FROM product WHERE product_id = 42")
            product = cursor.fetchone()
            if product:
                print(f"   ✓ Product found: {product['product_name']}")
            else:
                print("   ✗ Product not found")
                return
            
            print("\n2. Checking variants...")
            cursor.execute("SELECT COUNT(*) as count FROM variant WHERE product_id = 42")
            variant_count = cursor.fetchone()['count']
            print(f"   Found {variant_count} variants")
            
            print("\n3. Checking order_item references...")
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM order_item oi 
                JOIN variant v ON oi.variant_id = v.variant_id 
                WHERE v.product_id = 42
            """)
            order_count = cursor.fetchone()['count']
            print(f"   Found {order_count} order items")
            
            print("\n4. Checking favorite_product references...")
            try:
                cursor.execute("SELECT COUNT(*) as count FROM favorite_product WHERE product_id = 42")
                fav_count = cursor.fetchone()['count']
                print(f"   Found {fav_count} favorites")
            except Exception as e:
                print(f"   Error checking favorites: {e}")
            
            print("\n5. Attempting DELETE FROM variant...")
            cursor.execute("DELETE FROM variant WHERE product_id = 42")
            print(f"   Would delete {cursor.rowcount} variants")
            
            print("\n6. Attempting DELETE FROM favorite_product...")
            try:
                cursor.execute("DELETE FROM favorite_product WHERE product_id = 42")
                print(f"   Would delete {cursor.rowcount} favorites")
            except Exception as e:
                print(f"   Error: {e}")
            
            print("\n7. Attempting DELETE FROM product...")
            cursor.execute("DELETE FROM product WHERE product_id = 42")
            print(f"   Would delete product (affected rows: {cursor.rowcount})")
            
            print("\n8. Rolling back transaction (dry run)...")
            conn.rollback()
            print("   ✓ Transaction rolled back successfully")
            
            print("\n" + "=" * 60)
            print("DRY RUN COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n✗ ERROR during dry run: {e}")
            print(f"   Error type: {type(e).__name__}")
            if hasattr(e, 'errno'):
                print(f"   MySQL Error Number: {e.errno}")
            if hasattr(e, 'msg'):
                print(f"   MySQL Error Message: {e.msg}")
            conn.rollback()
            
            import traceback
            print("\nFull traceback:")
            traceback.print_exc()
        
    finally:
        cursor.close()
        conn.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    check_constraints()
