import mysql.connector

def check_user_table():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pegasus@0918',
            database='brightbuy'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Check table structure
        print("Checking user table structure...")
        cursor.execute("DESCRIBE user")
        columns = cursor.fetchall()
        print("\nTable Structure:")
        for column in columns:
            print(f"Column: {column['Field']}, Type: {column['Type']}")
            
        # Check existing users
        print("\nChecking existing users...")
        cursor.execute("SELECT user_id, username, user_name, email, user_type FROM user")
        users = cursor.fetchall()
        print("\nExisting Users:")
        for user in users:
            print(f"ID: {user['user_id']}, Email: {user['email']}, Type: {user.get('user_type', 'customer')}")
            
        # Create test user if no users exist
        if not users:
            print("\nNo users found. Creating test user...")
            import bcrypt
            
            # Hash password
            password = "test123"
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Insert test user
            cursor.execute("""
                INSERT INTO user (username, user_name, email, password_hash, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """, ('testuser', 'testuser', 'test@brightbuy.com', hashed_password.decode(), 'customer'))
            
            connection.commit()
            print("✓ Test user created successfully!")
            print("Email: test@brightbuy.com")
            print("Password: test123")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    check_user_table()