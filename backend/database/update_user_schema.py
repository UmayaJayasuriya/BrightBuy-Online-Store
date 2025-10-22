import mysql.connector

def update_user_table():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pegasus@0918',
            database='brightbuy'
        )
        
        cursor = connection.cursor()
        
        # Alter the user table to match the expected schema
        alter_queries = [
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS user_name VARCHAR(50) UNIQUE,
            ADD COLUMN IF NOT EXISTS user_type ENUM('admin', 'customer') DEFAULT 'customer',
            ADD COLUMN IF NOT EXISTS name VARCHAR(100)
            """,
            
            # Update existing username column to user_name if needed
            """
            UPDATE user 
            SET user_name = username 
            WHERE user_name IS NULL AND username IS NOT NULL
            """,
            
            # Create admin_verification_codes table if it doesn't exist
            """
            CREATE TABLE IF NOT EXISTS admin_verification_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                verification_code VARCHAR(6) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_used BOOLEAN DEFAULT FALSE,
                attempts INT DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                INDEX idx_user_code (user_id, verification_code),
                INDEX idx_expires (expires_at)
            )
            """
        ]
        
        # Execute each query
        for query in alter_queries:
            cursor.execute(query)
            
        # Create admin user if it doesn't exist
        admin_check_query = "SELECT * FROM user WHERE email = 'admin@brightbuy.com'"
        cursor.execute(admin_check_query)
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            # Hash the password 'admin123'
            import bcrypt
            password = 'admin123'
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            admin_insert_query = """
            INSERT INTO user (user_name, email, password_hash, user_type, name)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(admin_insert_query, 
                         ('admin', 'admin@brightbuy.com', hashed_password.decode(), 'admin', 'Admin User'))
        
        # Commit the changes
        connection.commit()
        print("✓ User table structure updated successfully")
        print("✓ Admin verification table created successfully")
        if not admin_exists:
            print("✓ Admin user created successfully")
            print("   Email: admin@brightbuy.com")
            print("   Password: admin123")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_user_table()