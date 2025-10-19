"""
Show the actual stored procedure SQL
"""

import sys
sys.path.insert(0, '.')
from app.database import get_connection

def show_procedure():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SHOW CREATE PROCEDURE GetOrderSummary")
        row = cursor.fetchone()
        
        if row:
            print("Current GetOrderSummary Procedure:")
            print("=" * 80)
            print(row[2])  # The SQL is in the 3rd column
            print("=" * 80)
        else:
            print("Procedure not found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    show_procedure()
