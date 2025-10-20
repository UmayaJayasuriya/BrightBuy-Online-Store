import mysql.connector
from mysql.connector import Error

def check_database_objects():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='brightbuy',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("=" * 60)
            print("CHECKING FOR DATABASE TRIGGERS")
            print("=" * 60)
            
            # Check for triggers on product table
            cursor.execute("SHOW TRIGGERS WHERE `Table` = 'product'")
            triggers = cursor.fetchall()
            if triggers:
                print("\nTriggers on 'product' table:")
                for trigger in triggers:
                    print(f"  - {trigger}")
            else:
                print("\nNo triggers found on 'product' table")
            
            # Check for triggers on variant table
            cursor.execute("SHOW TRIGGERS WHERE `Table` = 'variant'")
            triggers = cursor.fetchall()
            if triggers:
                print("\nTriggers on 'variant' table:")
                for trigger in triggers:
                    print(f"  - {trigger}")
            else:
                print("\nNo triggers found on 'variant' table")
            
            print("\n" + "=" * 60)
            print("CHECKING FOR VIEWS")
            print("=" * 60)
            
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM information_schema.VIEWS 
                WHERE TABLE_SCHEMA = 'brightbuy'
            """)
            views = cursor.fetchall()
            if views:
                print("\nViews in database:")
                for view in views:
                    print(f"  - {view[0]}")
            else:
                print("\nNo views found")
            
            print("\n" + "=" * 60)
            print("CHECKING FOR STORED PROCEDURES")
            print("=" * 60)
            
            cursor.execute("""
                SELECT ROUTINE_NAME 
                FROM information_schema.ROUTINES 
                WHERE ROUTINE_SCHEMA = 'brightbuy' 
                AND ROUTINE_TYPE = 'PROCEDURE'
            """)
            procedures = cursor.fetchall()
            if procedures:
                print("\nStored procedures:")
                for proc in procedures:
                    print(f"  - {proc[0]}")
            else:
                print("\nNo stored procedures found")
            
            print("\n" + "=" * 60)
            print("CHECKING ALL TABLES")
            print("=" * 60)
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nAll tables in brightbuy database:")
            for table in tables:
                print(f"  - {table[0]}")
            
            print("\n" + "=" * 60)
            print("CHECKING FOR 'OrderDetails' REFERENCES")
            print("=" * 60)
            
            # Check if OrderDetails exists (with different cases)
            for table_name in ['OrderDetails', 'orderdetails', 'order_details', 'Orderdetails']:
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = 'brightbuy' 
                    AND TABLE_NAME = '{table_name}'
                """)
                if cursor.fetchone()[0] > 0:
                    print(f"\n✓ Found table: {table_name}")
                else:
                    print(f"\n✗ Table not found: {table_name}")
            
            print("\n" + "=" * 60)
            print("CHECKING FOREIGN KEY CONSTRAINTS ON PRODUCT TABLE")
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
                print("\nForeign keys referencing 'product' table:")
                for fk in fks:
                    print(f"  - {fk[1]}.{fk[2]} -> {fk[3]}.{fk[4]} (constraint: {fk[0]})")
            else:
                print("\nNo foreign keys reference the 'product' table")
                
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n" + "=" * 60)
            print("MySQL connection closed.")

if __name__ == "__main__":
    check_database_objects()
