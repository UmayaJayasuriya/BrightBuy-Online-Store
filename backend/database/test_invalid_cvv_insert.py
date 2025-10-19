import sys
sys.path.insert(0, '.')
from app.database import get_connection

conn = None
cursor = None
try:
    conn = get_connection()
    cursor = conn.cursor()
    print('Attempting to insert invalid CVV...')
    cursor.execute("INSERT INTO card (order_id, card_number, card_name, expiry_date, CVV) VALUES (NULL, '4111111111111111', 'TEST', '12/25', '12A')")
    conn.commit()
    print('Insert succeeded (unexpected)')
except Exception as e:
    print('Insert failed as expected:')
    print(str(e))
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
