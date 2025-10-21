"""
Apply report views to the database
This script creates all the database views needed for PDF report generation
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'brightbuy'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def apply_views():
    """Apply all report views to the database"""
    try:
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'database', 'views', 'reports_views.sql')
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        print(f"Applying views from: {sql_file_path}")
        print("-" * 60)
        
        # Split by semicolons and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if statement.startswith('--') or statement.startswith('/*') or not statement:
                continue
            
            # Skip USE statement (already connected to database)
            if statement.upper().startswith('USE'):
                continue
                
            try:
                cursor.execute(statement)
                
                # Print progress for CREATE VIEW statements
                if 'CREATE VIEW' in statement.upper():
                    view_name = statement.split('CREATE VIEW')[1].split('AS')[0].strip()
                    print(f"✓ Created view: {view_name}")
                elif 'DROP VIEW' in statement.upper():
                    view_name = statement.split('DROP VIEW IF EXISTS')[1].strip()
                    print(f"  Dropped existing view: {view_name}")
                    
            except mysql.connector.Error as err:
                print(f"✗ Error executing statement {i}: {err}")
                print(f"  Statement preview: {statement[:100]}...")
                continue
        
        connection.commit()
        print("-" * 60)
        print("✓ All views applied successfully!")
        
        # Verify views
        print("\nVerifying views...")
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        
        print(f"\nTotal views in database: {len(views)}")
        for view in views:
            print(f"  - {view[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Could not find SQL file at {sql_file_path}")
        return False
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("BrightBuy Database Views Installer")
    print("=" * 60)
    print()
    
    success = apply_views()
    
    if success:
        print("\n✓ Setup complete! Report endpoints should now work.")
        print("\nYou can test the reports at:")
        print("  - http://127.0.0.1:8020/reports/quarterly-sales/2025")
        print("  - http://127.0.0.1:8020/reports/top-selling-products")
        print("  - http://127.0.0.1:8020/reports/category-orders")
        print("  - http://127.0.0.1:8020/reports/all-customers-summary")
        print("  - http://127.0.0.1:8020/reports/customer-orders/1")
    else:
        print("\n✗ Setup failed. Please check the errors above.")
