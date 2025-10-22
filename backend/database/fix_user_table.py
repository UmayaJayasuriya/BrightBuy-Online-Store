import mysql.connector

def fix_user_table():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pegasus@0918',
            database='brightbuy'
        )
        
        cursor = connection.cursor()
        
        # Drop and recreate user table with correct structure
        cursor.execute("""
            DROP TABLE IF EXISTS admin_verification_codes;
            DROP TABLE IF EXISTS user_address;
            DROP TABLE IF EXISTS user;
            
            CREATE TABLE user (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                user_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                user_type ENUM('admin', 'customer') DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                UNIQUE INDEX idx_email (email),
                UNIQUE INDEX idx_user_name (user_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            
            CREATE TABLE admin_verification_codes (
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
        """)
        
        connection.commit()
        print("✓ User table structure fixed!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    fix_user_table()