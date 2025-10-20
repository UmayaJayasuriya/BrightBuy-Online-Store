"""
Fix product_id AUTO_INCREMENT
Run this script to add AUTO_INCREMENT to product_id field
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'brightbuy'),
    'port': int(os.getenv('DB_PORT', 3306))
}

try:
    # Connect to database
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("Connected to database successfully!")
    
    # Disable foreign key checks temporarily
    print("\nDisabling foreign key checks...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # Fix product_id AUTO_INCREMENT
    print("Fixing product_id AUTO_INCREMENT...")
    cursor.execute("""
        ALTER TABLE product 
        MODIFY COLUMN product_id INT NOT NULL AUTO_INCREMENT
    """)
    
    # Re-enable foreign key checks
    print("Re-enabling foreign key checks...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    connection.commit()
    
    print("✅ Successfully added AUTO_INCREMENT to product_id!")
    
    # Verify the change
    cursor.execute("SHOW CREATE TABLE product")
    result = cursor.fetchone()
    print("\n✅ Product table structure updated:")
    print(result[1])
    
    cursor.close()
    connection.close()
    
    print("\n✅ Fix completed successfully!")
    print("You can now create products from the admin dashboard.")
    
except mysql.connector.Error as error:
    print(f"❌ Error: {error}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
