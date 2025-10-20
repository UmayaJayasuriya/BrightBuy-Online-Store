"""
Check if favorite_product table exists and create if needed
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'brightbuy'),
    'port': int(os.getenv('DB_PORT', 3306))
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SHOW TABLES LIKE 'favorite_product'")
    result = cursor.fetchone()
    
    if result:
        print("✅ favorite_product table already exists!")
    else:
        print("❌ favorite_product table NOT found!")
        print("\n🔧 Creating favorite_product table...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_product (
                favorite_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_product (user_id, product_id),
                INDEX idx_user_id (user_id),
                INDEX idx_product_id (product_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
        print("✅ favorite_product table created successfully!")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Database check complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
