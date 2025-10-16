"""
Show the actual stored procedure SQL
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/brightbuy')

def show_procedure():
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            result = conn.execute(text("SHOW CREATE PROCEDURE GetOrderSummary"))
            row = result.fetchone()
            
            if row:
                print("Current GetOrderSummary Procedure:")
                print("=" * 80)
                print(row[2])  # The SQL is in the 3rd column
                print("=" * 80)
            else:
                print("Procedure not found")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_procedure()
