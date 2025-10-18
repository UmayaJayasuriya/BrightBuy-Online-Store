"""
Apply MySQL Functions to BrightBuy Database
This script installs all custom MySQL functions from mysql_functions.sql
"""

import mysql.connector
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path to import database config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def apply_functions():
    """Apply all MySQL functions to the database"""
    
    # Load environment variables
    load_dotenv()
    
    # Database connection
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'brightbuy')
        )
        cursor = db.cursor()
        print("✅ Connected to database")
        
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        return
    
    # Read the SQL file
    sql_file_path = os.path.join(os.path.dirname(__file__), 'mysql_functions.sql')
    
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        print("✅ SQL file loaded")
    except FileNotFoundError:
        print(f"❌ SQL file not found: {sql_file_path}")
        cursor.close()
        db.close()
        return
    
    # Split SQL statements by delimiter
    statements = []
    current_statement = []
    in_delimiter_block = False
    
    for line in sql_content.split('\n'):
        line_stripped = line.strip()
        
        # Skip comments and empty lines
        if line_stripped.startswith('--') or not line_stripped:
            continue
            
        # Handle DELIMITER changes
        if line_stripped.startswith('DELIMITER'):
            if '$$' in line_stripped:
                in_delimiter_block = True
            else:
                in_delimiter_block = False
            continue
        
        current_statement.append(line)
        
        # Check for statement end
        if in_delimiter_block:
            if line_stripped.endswith('$$'):
                statements.append('\n'.join(current_statement))
                current_statement = []
        else:
            if line_stripped.endswith(';'):
                statements.append('\n'.join(current_statement))
                current_statement = []
    
    # Execute each statement
    function_names = [
        "CalculateCartTotal",
        "GetProductStockStatus",
        "CalculateOrderItemTotal",
        "GetCustomerLifetimeValue",
        "GetProductAverageRating",
        "IsVariantAvailable",
        "GetProductPriceRange",
        "CalculateDeliveryDays",
        "GetOrderStatus",
        "ValidateEmail",
        "GetDiscountedPrice",
        "GetCategoryPath"
    ]
    
    print("\n📦 Installing MySQL Functions...")
    print("=" * 50)
    
    success_count = 0
    for i, statement in enumerate(statements):
        if not statement.strip():
            continue
            
        try:
            # Remove trailing $$ if present
            statement = statement.replace('$$', '')
            cursor.execute(statement)
            
            # Check if this is a CREATE FUNCTION statement
            if 'CREATE FUNCTION' in statement.upper():
                success_count += 1
                if success_count <= len(function_names):
                    print(f"✅ {success_count}. {function_names[success_count - 1]}")
                    
        except mysql.connector.Error as err:
            # Only show errors for CREATE FUNCTION statements
            if 'CREATE FUNCTION' in statement.upper():
                print(f"⚠️  Error in statement: {err}")
    
    db.commit()
    print("=" * 50)
    print(f"\n🎉 Successfully installed {success_count} functions!")
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    cursor.execute("""
        SELECT ROUTINE_NAME 
        FROM information_schema.ROUTINES 
        WHERE ROUTINE_SCHEMA = %s 
        AND ROUTINE_TYPE = 'FUNCTION'
        ORDER BY ROUTINE_NAME
    """, (os.getenv('DB_NAME', 'brightbuy'),))
    
    functions = cursor.fetchall()
    print(f"✅ Found {len(functions)} functions in database:")
    for func in functions:
        print(f"   • {func[0]}")
    
    cursor.close()
    db.close()
    print("\n✅ Done!")

if __name__ == "__main__":
    print("=" * 50)
    print("BrightBuy MySQL Functions Installer")
    print("=" * 50)
    apply_functions()
