import mysql.connector
import bcrypt

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Pegasus@0918',
        database='brightbuy'
    )
    
    cursor = connection.cursor()
    
    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS admin_verification_codes")
    cursor.execute("DROP TABLE IF EXISTS cart")
    cursor.execute("DROP TABLE IF EXISTS user")
    
    # Create user table
    cursor.execute("""
        CREATE TABLE user (
            user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            user_type ENUM('admin', 'customer') DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            UNIQUE KEY idx_email (email),
            UNIQUE KEY idx_user_name (user_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    
    # Create test users
    test_users = [
        {
            'user_name': 'testuser',
            'email': 'test@brightbuy.com',
            'password': 'test123',
            'user_type': 'customer'
        },
        {
            'user_name': 'admin',
            'email': 'admin@brightbuy.com',
            'password': 'admin123',
            'user_type': 'admin'
        }
    ]
    
    for user in test_users:
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
        
        # Insert user
        cursor.execute("""
            INSERT INTO user 
            (user_name, email, password_hash, user_type)
            VALUES (%s, %s, %s, %s)
        """, (
            user['user_name'],
            user['email'],
            hashed_password.decode(),
            user['user_type']
        ))
        
        print(f"✓ Created {user['user_type']} user:")
        print(f"  Email: {user['email']}")
        print(f"  Password: {user['password']}\n")
    
    # Enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    connection.commit()
    print("✓ Database setup complete!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    if 'connection' in locals() and connection.is_connected():
        connection.rollback()
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()