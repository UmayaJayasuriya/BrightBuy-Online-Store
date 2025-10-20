-- Trigger to prevent deletion of variants that are referenced in orders
-- This ensures data integrity by blocking variant deletion if order_item references exist

DELIMITER $$

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
END$$

DELIMITER ;
