import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_connection

def fix_variant_autoincrement():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        print("=" * 60)
        print("CHECKING VARIANT TABLE STRUCTURE")
        print("=" * 60)
        
        # Check current structure
        cursor.execute("DESCRIBE variant")
        columns = cursor.fetchall()
        
        print("\nCurrent variant table structure:")
        for col in columns:
            print(f"  {col['Field']}: {col['Type']} {col['Key']} {col['Extra']}")
        
        # Check if variant_id already has AUTO_INCREMENT
        cursor.execute("""
            SELECT COLUMN_NAME, EXTRA 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = 'brightbuy' 
            AND TABLE_NAME = 'variant' 
            AND COLUMN_NAME = 'variant_id'
        """)
        result = cursor.fetchone()
        
        if result and 'auto_increment' in result['EXTRA'].lower():
            print("\n✓ variant_id already has AUTO_INCREMENT enabled")
            return
        
        print("\n" + "=" * 60)
        print("ADDING AUTO_INCREMENT TO variant_id")
        print("=" * 60)
        
        # Get current max variant_id
        cursor.execute("SELECT MAX(variant_id) as max_id FROM variant")
        max_result = cursor.fetchone()
        max_id = max_result['max_id'] if max_result and max_result['max_id'] else 0
        print(f"\nCurrent max variant_id: {max_id}")
        
        # Disable foreign key checks temporarily
        print("\nDisabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Modify the column to add AUTO_INCREMENT
        print("Modifying variant_id column to add AUTO_INCREMENT...")
        cursor.execute("""
            ALTER TABLE variant 
            MODIFY COLUMN variant_id INT NOT NULL AUTO_INCREMENT
        """)
        
        # Re-enable foreign key checks
        print("Re-enabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print("\nvariant_id now has AUTO_INCREMENT enabled")
        print(f"Next auto-increment value will be: {max_id + 1}")
        
        # Verify the change
        print("\n" + "=" * 60)
        print("VERIFYING CHANGES")
        print("=" * 60)
        
        cursor.execute("DESCRIBE variant")
        columns = cursor.fetchall()
        
        print("\nUpdated variant table structure:")
        for col in columns:
            extra = f" [{col['Extra']}]" if col['Extra'] else ""
            print(f"  {col['Field']}: {col['Type']} {col['Key']}{extra}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
        
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        
    finally:
        cursor.close()
        conn.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    fix_variant_autoincrement()
