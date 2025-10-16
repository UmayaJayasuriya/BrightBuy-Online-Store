import sys
sys.path.insert(0, '.')
from sqlalchemy import text
from app.database import engine

conn = engine.connect()
try:
    print('Attempting to insert invalid CVV...')
    conn.execute(text("INSERT INTO card (order_id, card_number, card_name, expiry_date, CVV) VALUES (NULL, '4111111111111111', 'TEST', '12/25', '12A')"))
    conn.commit()
    print('Insert succeeded (unexpected)')
except Exception as e:
    print('Insert failed as expected:')
    print(str(e))
finally:
    conn.close()
