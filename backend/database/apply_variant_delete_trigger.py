"""
Apply variant deletion protection trigger
This trigger prevents deletion of variants that are referenced in order_item table
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection


def apply_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing trigger (if any)...")
        try:
            cursor.execute("DROP TRIGGER IF EXISTS prevent_variant_delete_if_in_order;")
            conn.commit()
        except Exception as drop_err:
            # Ignore if trigger doesn't exist
            print(f"  Note: {drop_err}")
            conn.rollback()
        
        print("Creating variant deletion protection trigger...")
        
        trigger_sql = """
        CREATE TRIGGER prevent_variant_delete_if_in_order
        BEFORE DELETE ON variant
        FOR EACH ROW
        BEGIN
            -- Check if this variant is referenced in any order_item
            IF EXISTS (
                SELECT 1
                FROM order_item
                WHERE variant_id = OLD.variant_id
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Cannot delete variant: This variant is part of existing orders and cannot be removed.';
            END IF;
        END;
        """
        
        cursor.execute(trigger_sql)
        conn.commit()
        
        print("✅ Variant deletion protection trigger created successfully!")
        print("\nTrigger Details:")
        print("  - Name: prevent_variant_delete_if_in_order")
        print("  - Type: BEFORE DELETE")
        print("  - Table: variant")
        print("  - Purpose: Prevents deletion of variants referenced in orders")
        
        # Verify trigger was created
        cursor.execute("""
            SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING
            FROM information_schema.TRIGGERS
            WHERE TRIGGER_SCHEMA = 'brightbuy'
            AND TRIGGER_NAME = 'prevent_variant_delete_if_in_order'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"\n✅ Trigger verified in database:")
            print(f"   Trigger: {result[0]}")
            print(f"   Event: {result[1]}")
            print(f"   Table: {result[2]}")
            print(f"   Timing: {result[3]}")
        else:
            print("\n⚠️ Warning: Trigger created but could not be verified")
        
    except Exception as e:
        print(f"❌ Error creating trigger: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    apply_trigger()
