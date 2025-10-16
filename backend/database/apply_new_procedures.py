"""
Apply New Stored Procedures to BrightBuy Database
This script installs all the enhanced stored procedures for cart, products, inventory, and sales management.
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'brightbuy'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def apply_procedures():
    """Apply all stored procedures from the SQL file"""
    
    print("=" * 80)
    print("BrightBuy - Installing New Stored Procedures")
    print("=" * 80)
    
    try:
        # Connect to database
        print("\n📡 Connecting to database...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print(f"✅ Connected to {DB_CONFIG['database']} database")
        
        # Read SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'new_stored_procedures.sql')
        
        print(f"\n📄 Reading SQL file: {sql_file_path}")
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split by delimiter and execute
        print("\n🔧 Installing stored procedures...")
        print("-" * 80)
        
        # Remove DELIMITER statements and split by $$
        sql_content = sql_content.replace('DELIMITER $$', '')
        sql_content = sql_content.replace('DELIMITER ;', '')
        
        # Split by $$ and filter out empty statements
        statements = [stmt.strip() for stmt in sql_content.split('$$') if stmt.strip()]
        
        procedure_count = 0
        for statement in statements:
            if statement.startswith('USE') or statement.startswith('--'):
                continue
                
            if 'DROP PROCEDURE' in statement or 'CREATE PROCEDURE' in statement:
                try:
                    cursor.execute(statement)
                    
                    if 'CREATE PROCEDURE' in statement:
                        # Extract procedure name
                        proc_name = statement.split('PROCEDURE')[1].split('(')[0].strip().replace('`', '')
                        procedure_count += 1
                        print(f"✅ {procedure_count}. {proc_name}")
                        
                except mysql.connector.Error as e:
                    print(f"⚠️  Warning: {e}")
        
        conn.commit()
        
        print("-" * 80)
        print(f"\n✅ Successfully installed {procedure_count} stored procedures!")
        
        # Verify installation
        print("\n🔍 Verifying installation...")
        cursor.execute("""
            SELECT ROUTINE_NAME, ROUTINE_TYPE 
            FROM information_schema.ROUTINES 
            WHERE ROUTINE_SCHEMA = %s 
            AND ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_NAME
        """, (DB_CONFIG['database'],))
        
        procedures = cursor.fetchall()
        
        print(f"\n📋 Total procedures in database: {len(procedures)}")
        print("-" * 80)
        for proc in procedures:
            print(f"   • {proc[0]}")
        
        print("\n" + "=" * 80)
        print("🎉 Installation Complete!")
        print("=" * 80)
        
        print("\n📚 Available Procedures:")
        print("   1. GetUserCart(user_id) - Fetch user's cart details")
        print("   2. GetProductsByCategory(category_id) - Get products by category")
        print("   3. GetLowStockVariants(threshold) - Low stock alerts")
        print("   4. GetSalesReport(start_date, end_date) - Sales analytics")
        print("   5. UpdateOrderStatus(order_id, status) - Update delivery status")
        print("   6. GetTopSellingProducts(limit, days) - Best sellers (BONUS)")
        print("   7. GetCustomerOrderHistory(user_id) - Order history (BONUS)")
        
        print("\n💡 Example Usage:")
        print("   CALL GetUserCart(1);")
        print("   CALL GetProductsByCategory(2);")
        print("   CALL GetLowStockVariants(10);")
        print("   CALL GetSalesReport('2025-01-01', '2025-10-16');")
        print("   CALL UpdateOrderStatus(1, 'Shipped');")
        print("   CALL GetTopSellingProducts(10, 30);")
        print("   CALL GetCustomerOrderHistory(1);")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"\n❌ Error: SQL file not found at {sql_file_path}")
        print("   Make sure 'new_stored_procedures.sql' exists in the database folder.")
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\nTroubleshooting:")
        print("   1. Check database credentials in .env file")
        print("   2. Ensure MySQL server is running")
        print("   3. Verify database 'brightbuy' exists")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    apply_procedures()
