import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_connection

def drop_trigger():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("DROPPING PreventProductDeletion TRIGGER")
        print("=" * 60)
        
        # Drop the trigger
        cursor.execute("DROP TRIGGER IF EXISTS PreventProductDeletion")
        conn.commit()
        
        print("\n✓ Trigger 'PreventProductDeletion' has been dropped successfully!")
        print("\nYou can now delete products from the admin dashboard.")
        print("\nNote: The delete endpoint in admin.py already checks for")
        print("order references, so this trigger was redundant anyway.")
        
    except Exception as e:
        print(f"\n✗ Error dropping trigger: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    drop_trigger()
