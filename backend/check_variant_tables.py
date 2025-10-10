from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    # Check variant table structure
    print("\n=== Variant Table Structure ===")
    result = db.execute(text("DESCRIBE variant"))
    for row in result.fetchall():
        print(f"{row[0]}: {row[1]}")
    
    # Check variant_attribute table
    print("\n=== Variant_Attribute Table Structure ===")
    result = db.execute(text("DESCRIBE variant_attribute"))
    for row in result.fetchall():
        print(f"{row[0]}: {row[1]}")
    
    # Check variant_attribute_value table
    print("\n=== Variant_Attribute_Value Table Structure ===")
    result = db.execute(text("DESCRIBE variant_attribute_value"))
    for row in result.fetchall():
        print(f"{row[0]}: {row[1]}")
    
    # Get sample data
    print("\n=== Sample Variant Data ===")
    result = db.execute(text("SELECT * FROM variant LIMIT 3"))
    for row in result.fetchall():
        print(row)
    
    print("\n=== Sample Variant_Attribute Data ===")
    result = db.execute(text("SELECT * FROM variant_attribute LIMIT 5"))
    for row in result.fetchall():
        print(row)
        
    print("\n=== Sample Variant_Attribute_Value Data ===")
    result = db.execute(text("SELECT * FROM variant_attribute_value LIMIT 5"))
    for row in result.fetchall():
        print(row)
        
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
