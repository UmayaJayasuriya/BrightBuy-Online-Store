from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    # Check if product table exists and get its structure
    result = db.execute(text("DESCRIBE product"))
    print("\n=== Product Table Structure ===")
    for row in result.fetchall():
        print(f"{row[0]}: {row[1]}")
    
    # Get sample data
    print("\n=== Sample Product Data ===")
    result = db.execute(text("SELECT * FROM product LIMIT 3"))
    for row in result.fetchall():
        print(row)
        
except Exception as e:
    print(f"Error: {e}")
    print("\nProduct table might not exist. Here's the SQL to create it:")
    print("""
CREATE TABLE IF NOT EXISTS product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    category_id INT NOT NULL,
    image_url VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
    """)
finally:
    db.close()
