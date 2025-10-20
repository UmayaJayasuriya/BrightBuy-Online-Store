import mysql.connector
from mysql.connector import Error

def check_orderdetails_references():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='brightbuy',
            user='himak',
            password='root'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("=" * 60)
            print("CHECKING FOR 'OrderDetails' REFERENCES IN DATABASE")
            print("=" * 60)
            
            # Check all table names
            print("\n1. ALL TABLES IN DATABASE:")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for table in tables:
                print(f"   - {table[0]}")
                if 'order' in table[0].lower():
                    print(f"     ^^^ ORDER-RELATED TABLE")
            
            # Check for triggers
            print("\n2. CHECKING TRIGGERS:")
            cursor.execute("SHOW TRIGGERS FROM brightbuy")
            triggers = cursor.fetchall()
            if triggers:
                for trigger in triggers:
                    print(f"   Trigger: {trigger[0]}")
                    print(f"   Event: {trigger[1]}")
                    print(f"   Table: {trigger[2]}")
                    print(f"   Statement: {trigger[3]}")
                    print()
            else:
                print("   No triggers found")
            
            # Check for views
            print("\n3. CHECKING VIEWS:")
            cursor.execute("""
                SELECT TABLE_NAME, VIEW_DEFINITION 
                FROM INFORMATION_SCHEMA.VIEWS 
                WHERE TABLE_SCHEMA = 'brightbuy'
            """)
            views = cursor.fetchall()
            if views:
                for view in views:
                    print(f"   View: {view[0]}")
                    print(f"   Definition: {view[1][:100]}...")
                    print()
            else:
                print("   No views found")
            
            # Check foreign key constraints
            print("\n4. CHECKING FOREIGN KEY CONSTRAINTS ON product TABLE:")
            cursor.execute("""
                SELECT 
                    CONSTRAINT_NAME,
                    TABLE_NAME,
                    COLUMN_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = 'brightbuy'
                AND REFERENCED_TABLE_NAME = 'product'
            """)
            fks = cursor.fetchall()
            if fks:
                for fk in fks:
                    print(f"   Constraint: {fk[0]}")
                    print(f"   Table: {fk[1]}.{fk[2]} -> {fk[3]}.{fk[4]}")
                    print()
            else:
                print("   No foreign keys referencing product table")
            
            # Check for stored procedures
            print("\n5. CHECKING STORED PROCEDURES:")
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'brightbuy'")
            procedures = cursor.fetchall()
            if procedures:
                for proc in procedures:
                    print(f"   Procedure: {proc[1]}")
            else:
                print("   No stored procedures found")
            
            # Check for stored functions
            print("\n6. CHECKING STORED FUNCTIONS:")
            cursor.execute("SHOW FUNCTION STATUS WHERE Db = 'brightbuy'")
            functions = cursor.fetchall()
            if functions:
                for func in functions:
                    print(f"   Function: {func[1]}")
            else:
                print("   No stored functions found")
            
            print("\n" + "=" * 60)
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    check_orderdetails_references()
