import mysql.connector
import bcrypt

def create_test_users():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pegasus@0918',
            database='brightbuy'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Create regular test user
        test_user = {
            'username': 'testuser',
            'email': 'test@brightbuy.com',
            'password': 'test123',
            'user_type': 'customer'
        }
        
        # Create admin user
        admin_user = {
            'username': 'admin',
            'email': 'admin@brightbuy.com',
            'password': 'admin123',
            'user_type': 'admin'
        }
        
        for user in [test_user, admin_user]:
            # Check if user exists
            cursor.execute("SELECT * FROM user WHERE email = %s", (user['email'],))
            if not cursor.fetchone():
                # Hash password
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
                
                # Insert user
                cursor.execute("""
                    INSERT INTO user 
                    (user_name, email, password_hash, user_type)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user['username'],
                    user['email'],
                    hashed_password.decode(),
                    user['user_type']
                ))
                
                print(f"✓ Created {user['user_type']} user:")
                print(f"  Email: {user['email']}")
                print(f"  Password: {user['password']}\n")
        
        connection.commit()
        print("✓ User setup complete!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_test_users()