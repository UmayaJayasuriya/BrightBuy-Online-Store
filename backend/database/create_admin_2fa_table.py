"""
Create table for storing admin 2FA verification codes
"""
import mysql.connector
import sys
from pathlib import Path

# Add project root to path
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from app.database import DB_CONFIG

def create_admin_verification_table():
    """Create table to store admin 2FA verification codes"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create table for storing verification codes
        create_table_query = """
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
        
        cursor.execute(create_table_query)
        connection.commit()
        
        print("✓ admin_verification_codes table created successfully")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"✗ Error creating table: {err}")
        sys.exit(1)

if __name__ == "__main__":
    create_admin_verification_table()
