"""
Script to create payment and delivery tables
"""
import sys
sys.path.insert(0, '.')
from sqlalchemy import text
from app.database import engine

# Create payment table
payment_table_sql = """
CREATE TABLE IF NOT EXISTS payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payment_date DATETIME NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)
"""

# Create delivery table
delivery_table_sql = """
CREATE TABLE IF NOT EXISTS delivery (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_method VARCHAR(50) NOT NULL,
    address_id INT,
    estimated_delivery_date DATE,
    delivery_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE SET NULL
)
"""

conn = engine.connect()
try:
    conn.execute(text(payment_table_sql))
    conn.execute(text(delivery_table_sql))
    conn.commit()
    print("✅ Payment and Delivery tables created successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()
