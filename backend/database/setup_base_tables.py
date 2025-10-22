import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Pegasus@0918',
        database='brightbuy'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Create User table first
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            UNIQUE INDEX idx_email (email),
            UNIQUE INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_user_table)
        connection.commit()
        print("✓ User table created successfully")
        
        # Now create admin verification table
        create_admin_table = """
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_admin_table)
        connection.commit()
        print("✓ Admin verification codes table created successfully")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")