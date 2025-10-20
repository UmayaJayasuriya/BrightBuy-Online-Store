"""
Apply Report Views to Database
Run this script to create all report views
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'brightbuy')
DB_PORT = int(os.getenv('DB_PORT', 3306))

def apply_views():
    """Apply all report views to the database"""
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        
        # Read SQL file
        with open('database/views/reports_views.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        print("Applying report views...")
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if statement.startswith('--') or not statement:
                continue
            
            try:
                cursor.execute(statement)
                if 'CREATE VIEW' in statement.upper() or 'DROP VIEW' in statement.upper():
                    view_name = statement.split('VIEW')[-1].split()[0] if 'VIEW' in statement else ''
                    print(f"✓ Processed: {view_name}")
            except mysql.connector.Error as err:
                print(f"✗ Error in statement {i}: {err}")
                continue
        
        connection.commit()
        print("\n✅ All report views applied successfully!")
        
        # Verify views
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        print(f"\n📊 Total views in database: {len(views)}")
        for view in views:
            print(f"  - {view[0]}")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except FileNotFoundError:
        print("❌ SQL file not found. Make sure reports_views.sql exists.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_views()
