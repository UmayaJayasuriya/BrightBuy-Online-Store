import mysql.connector
from mysql.connector import Error

def fix_product_deletion_trigger():
    """
    Fix the PreventProductDeletion trigger that references
    the non-existent 'OrderDetails' table.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='brightbuy',
            user='himak',
            password='root'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("=" * 60)
            print("FIXING PreventProductDeletion TRIGGER")
            print("=" * 60)
            
            # Drop the existing broken trigger
            print("\n1. Dropping existing trigger...")
            cursor.execute("DROP TRIGGER IF EXISTS `PreventProductDeletion`")
            print("   ✓ Trigger dropped successfully")
            
            # Create the corrected trigger
            print("\n2. Creating corrected trigger...")
            trigger_sql = """
            CREATE TRIGGER `PreventProductDeletion` 
            BEFORE DELETE ON `product` 
            FOR EACH ROW 
            BEGIN
                -- Check if product variants exist in order_item table
                IF EXISTS (
                    SELECT 1 FROM order_item oi
                    JOIN variant v ON oi.variant_id = v.variant_id
                    WHERE v.product_id = OLD.product_id
                ) THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Cannot delete product with existing orders';
                END IF;
            END
            """
            cursor.execute(trigger_sql)
            print("   ✓ Trigger created successfully")
            
            # Verify the trigger was created
            print("\n3. Verifying trigger...")
            cursor.execute("SHOW TRIGGERS WHERE `Trigger` = 'PreventProductDeletion'")
            trigger = cursor.fetchone()
            
            if trigger:
                print("   ✓ Trigger verified:")
                print(f"     Name: {trigger[0]}")
                print(f"     Event: {trigger[1]}")
                print(f"     Table: {trigger[2]}")
                print(f"     Timing: {trigger[4]}")
            else:
                print("   ✗ Trigger not found after creation")
            
            connection.commit()
            print("\n" + "=" * 60)
            print("TRIGGER FIX COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nYou can now delete products from the admin dashboard.")
            
    except Error as e:
        print(f"\n✗ Error: {e}")
        if connection:
            connection.rollback()
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    fix_product_deletion_trigger()
