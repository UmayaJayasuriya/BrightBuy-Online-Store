"""Check admin users in database"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'brightbuy')
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT user_id, user_name, email, user_type FROM user WHERE user_type = 'admin' LIMIT 5")
users = cursor.fetchall()

print("\n" + "="*60)
print("ADMIN USERS IN DATABASE")
print("="*60)

if users:
    for user in users:
        print(f"\n✅ Admin User Found:")
        print(f"   Username: {user['user_name']}")
        print(f"   Email: {user['email']}")
        print(f"   User ID: {user['user_id']}")
else:
    print("\n❌ No admin users found!")
    print("\nYou need to create an admin user first.")

cursor.close()
conn.close()

print("\n" + "="*60)
print("\n💡 To login in Swagger:")
print('   Use: {"identifier": "USERNAME_HERE", "password": "PASSWORD_HERE"}')
print("="*60 + "\n")
