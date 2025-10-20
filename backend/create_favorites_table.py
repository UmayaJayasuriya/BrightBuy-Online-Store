import mysql.connector
from mysql.connector import Error

def create_favorites_table():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            database='brightbuy',
            user='himak',
            password='root'  # Change if different
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if table already exists
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'brightbuy' 
                AND table_name = 'favorite_product'
            """)
            
            exists = cursor.fetchone()[0] > 0
            
            if exists:
                print("✓ favorite_product table already exists")
            else:
                print("Creating favorite_product table...")
                
                # Create the favorite_product table
                cursor.execute("""
                    CREATE TABLE favorite_product (
                        favorite_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        product_id INT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE KEY unique_user_product (user_id, product_id),
                        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
                    )
                """)
                
                connection.commit()
                print("✓ favorite_product table created successfully!")
            
            # Show table structure
            cursor.execute("DESCRIBE favorite_product")
            print("\nTable structure:")
            for row in cursor.fetchall():
                print(f"  {row}")
                
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    create_favorites_table()
