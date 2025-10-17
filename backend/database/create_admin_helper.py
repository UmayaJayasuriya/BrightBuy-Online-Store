"""
Create Admin User Helper Script
Connects to the database and creates an admin user or upgrades an existing user to admin
"""
import bcrypt
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'brightbuy'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def create_admin_user(username, email, name, password):
    """Create a new admin user"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Check if user already exists
        cursor.execute("SELECT user_id FROM user WHERE email = %s OR user_name = %s", (email, username))
        existing = cursor.fetchone()
        
        if existing:
            print(f"❌ User with email '{email}' or username '{username}' already exists.")
            print(f"   Use upgrade_to_admin() function instead.")
            cursor.close()
            conn.close()
            return False
        
        # Hash password
        password_bytes = password.encode('utf-8')[:72]
        hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        # Insert user (without address for simplicity)
        cursor.execute(
            """INSERT INTO user (user_name, email, name, password_hash, user_type) 
               VALUES (%s, %s, %s, %s, %s)""",
            (username, email, name, hashed_pw, 'admin')
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        print(f"✅ Admin user created successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Name: {name}")
        print(f"   Type: admin")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def upgrade_to_admin(identifier):
    """Upgrade an existing user to admin by email or username"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Find user
        cursor.execute(
            "SELECT user_id, user_name, email, user_type FROM user WHERE email = %s OR user_name = %s",
            (identifier, identifier)
        )
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User '{identifier}' not found.")
            cursor.close()
            conn.close()
            return False
        
        if user['user_type'] == 'admin':
            print(f"ℹ️  User '{user['user_name']}' is already an admin.")
            cursor.close()
            conn.close()
            return True
        
        # Upgrade to admin
        cursor.execute("UPDATE user SET user_type = 'admin' WHERE user_id = %s", (user['user_id'],))
        conn.commit()
        
        print(f"✅ User upgraded to admin successfully!")
        print(f"   User ID: {user['user_id']}")
        print(f"   Username: {user['user_name']}")
        print(f"   Email: {user['email']}")
        print(f"   Old Type: {user['user_type']}")
        print(f"   New Type: admin")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def list_admin_users():
    """List all admin users"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT user_id, user_name, email, name, user_type FROM user WHERE user_type = 'admin'")
        admins = cursor.fetchall()
        
        if not admins:
            print("ℹ️  No admin users found.")
        else:
            print(f"\n📋 Admin Users ({len(admins)}):")
            print("-" * 80)
            for admin in admins:
                print(f"ID: {admin['user_id']:4} | Username: {admin['user_name']:20} | Email: {admin['email']:30}")
            print("-" * 80)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print("BrightBuy Admin User Manager")
    print("=" * 80)
    
    while True:
        print("\nOptions:")
        print("1. Create new admin user")
        print("2. Upgrade existing user to admin")
        print("3. List all admin users")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n--- Create New Admin User ---")
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            name = input("Full Name: ").strip()
            password = input("Password: ").strip()
            
            if username and email and name and password:
                create_admin_user(username, email, name, password)
            else:
                print("❌ All fields are required.")
        
        elif choice == "2":
            print("\n--- Upgrade User to Admin ---")
            identifier = input("Enter email or username: ").strip()
            
            if identifier:
                upgrade_to_admin(identifier)
            else:
                print("❌ Email or username is required.")
        
        elif choice == "3":
            list_admin_users()
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")
